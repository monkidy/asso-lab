#!/usr/bin/env python3
"""ACE Publishing Pipeline, full automation.

Chaine complete en un seul lancement :
  1. briefing_orchestrator_v0.py  ->  brief DRAFT du jour
  2. generate_x_draft()           ->  X post (EN, 280 chars) via Gemini
  3. telegram_gate.py             ->  envoi du draft a Asso_CM, attente ok/non
  4. affichage du texte final     ->  l'operateur poste manuellement depuis Telegram

Usage:
  python run_pipeline.py                   # pipeline complet (lance par le scheduler)
  python run_pipeline.py --dry-run         # gate actif, post en dry-run seulement
  python run_pipeline.py --skip-brief      # saute l'etape 1 (brief deja genere)
  python run_pipeline.py --post-text "..." # X post custom, bypass etapes 1-3

Doctrine ACE : human bounds before autonomy.
Aucune publication sans confirmation explicite de l'operateur via Telegram.
"""
import argparse
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    from dotenv import load_dotenv
    _env = Path(__file__).parent / ".env"
    if not load_dotenv(_env):
        load_dotenv()
except ImportError:
    pass

ROOT   = Path(__file__).parent.resolve()
PUBDIR = ROOT / "publications"
DRAFTS = ROOT / "drafts"
MODEL  = "gemini-2.5-flash"

X_DRAFT_PROMPT = """You are writing a post for X (Twitter) for @ace_prooflayer about AI agent governance.

HARD RULES, any violation is a failure:
- English only
- NEVER use an em-dash (the — character). Use a comma, colon, or period instead.
- Length: TARGET 200-235 characters. Hard maximum: 265 characters. Hard minimum: 180 characters. Count every single character including spaces and punctuation. When in doubt, write fewer words, never more.
- No URLs or links anywhere in the post
- Structure: (1) contrarian hook built on a concrete failure mode or number, (2) the deny-path / admissibility angle: who holds the refusal, model proposes and kernel disposes, (3) one proof: a number, a fact, or a failure mode, (4) closing principle
- End with a variant of "Receipts over claims."
- Voice: declarative, dry, technical. No marketing language. Short sentences.

Output ONLY the post text. No explanation, no quotes, no prefix.

Source brief (use the key insight, do not copy verbatim):
"""


# -----------------------------------------------------------------------------
def _today() -> str:
    return datetime.now(timezone.utc).date().isoformat()


def _run(cmd: list[str], label: str) -> int:
    print(f"\n[PIPELINE] {label}")
    print(f"[PIPELINE] > {' '.join(cmd)}")
    return subprocess.run(cmd, cwd=ROOT).returncode


def _brief_for_today() -> str | None:
    path = PUBDIR / f"{_today()}-briefing.md"
    return path.read_text(encoding="utf-8") if path.exists() else None


# -----------------------------------------------------------------------------
def generate_x_draft(brief: str) -> str:
    """Genere un X post EN (max 280 chars) depuis le brief via Gemini."""
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        sys.stderr.write("[PIPELINE] ERROR: GEMINI_API_KEY absent.\n")
        sys.exit(1)

    from openai import OpenAI
    client = OpenAI(
        api_key=api_key,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    )

    # On coupe le brief a 3000 chars pour rester dans les limites du prompt
    source = brief[:3000] + ("..." if len(brief) > 3000 else "")

    import time

    MAX_ATTEMPTS = 5        # tentatives de CONTENU (un overshoot consomme une tentative)
    RL_PAUSE = 25           # pause sur 429/503 (free tier = 5 req/min), retry sans consommer
    last_text = ""
    attempts = 0
    while attempts < MAX_ATTEMPTS:
        try:
            resp = client.chat.completions.create(
                model=MODEL,
                messages=[{"role": "user", "content": X_DRAFT_PROMPT + source}],
                # gemini-2.5-flash est un modele a raisonnement : un budget trop bas
                # est englouti par le thinking avant que le post ne soit ecrit.
                # On laisse large, la longueur reelle est bornee par les validations.
                max_tokens=2048,
            )
        except Exception as e:
            # 429 (quota/min) ou 503 (surcharge) : transitoire, on attend et on retente
            # SANS consommer de tentative, plutot que de crasher tout le pipeline.
            msg = str(e)
            if any(k in msg for k in ("429", "RESOURCE_EXHAUSTED", "503", "UNAVAILABLE")):
                sys.stderr.write(f"[PIPELINE] Gemini transitoire (quota/dispo), pause {RL_PAUSE}s puis retry.\n")
                time.sleep(RL_PAUSE)
                continue
            sys.stderr.write(f"[PIPELINE] ERROR appel LLM non transitoire: {e}\n")
            sys.exit(1)

        attempts += 1
        text = (resp.choices[0].message.content or "").strip().strip('"').strip("'")
        last_text = text

        # Validations
        if "—" in text or "―" in text:
            sys.stderr.write(f"[PIPELINE] Tentative {attempts}: em-dash detecte, on regenere.\n")
            time.sleep(3)
            continue
        if len(text) > 280:
            sys.stderr.write(f"[PIPELINE] Tentative {attempts}: {len(text)} chars > 280, on regenere.\n")
            time.sleep(3)   # espace les appels pour rester sous 5 req/min
            continue
        if len(text) < 100:
            sys.stderr.write(f"[PIPELINE] Tentative {attempts}: draft trop court ({len(text)} chars), on regenere.\n")
            time.sleep(3)
            continue

        return text

    sys.stderr.write(
        f"[PIPELINE] ERROR: aucun draft valide apres {MAX_ATTEMPTS} tentatives. "
        f"Dernier ({len(last_text)} chars) non poste.\n"
    )
    sys.exit(1)


# -----------------------------------------------------------------------------
def step_brief() -> int:
    rc = _run([sys.executable, "briefing_orchestrator_v0.py"], "Etape 1 : generation du brief")
    if rc != 0:
        print(f"[PIPELINE] Orchestrateur sorti avec code {rc}.")
    return rc


def step_gate(draft_path: Path, dry_run: bool, timeout: int) -> int:
    cmd = [
        sys.executable, "telegram_gate.py",
        "--file", str(draft_path),
        "--channel", "X",
        "--timeout", str(timeout),
    ]
    rc = _run(cmd, "Etape 3 : gate Telegram, en attente de ta validation")
    if rc == 0:
        print("[PIPELINE] APPROUVE.")
    elif rc == 1:
        print("[PIPELINE] REFUSE. Draft conserve, aucune publication.")
    else:
        print("[PIPELINE] TIMEOUT ou ERREUR. Draft conserve, aucune publication.")
    return rc


def step_post(draft_path: Path, dry_run: bool) -> int:
    cmd = [sys.executable, "post_to_x.py", "--file", str(draft_path)]
    if dry_run:
        cmd.append("--dry-run")
    return _run(cmd, "Etape 4 : publication X" + (" (DRY RUN)" if dry_run else ""))


# -----------------------------------------------------------------------------
def main() -> None:
    ap = argparse.ArgumentParser(description="ACE Publishing Pipeline")
    ap.add_argument("--skip-brief", action="store_true",
                    help="Saute l'etape 1 (brief deja genere aujourd'hui)")
    ap.add_argument("--dry-run",    action="store_true",
                    help="Gate actif, post en dry-run seulement (aucune publication reelle)")
    ap.add_argument("--post-text",  help="X post custom, bypass etapes 1 a 3, poste directement")
    ap.add_argument("--timeout",    type=int, default=1800,
                    help="Timeout gate Telegram en secondes (defaut 1800 = 30 min)")
    args = ap.parse_args()

    print(f"\n[PIPELINE] ACE Publishing Pipeline, {_today()}")
    print(f"[PIPELINE] dry-run={args.dry_run} | skip-brief={args.skip_brief}")

    DRAFTS.mkdir(exist_ok=True)
    draft_path = DRAFTS / f"{_today()}-x.txt"

    # Mode post direct ---------------------------------------------------
    if args.post_text:
        draft_path.write_text(args.post_text.strip(), encoding="utf-8")
        sys.exit(step_post(draft_path, args.dry_run))

    # Etape 1 : brief ----------------------------------------------------
    if not args.skip_brief:
        rc = step_brief()
        if rc != 0 and _brief_for_today() is None:
            sys.exit(rc)
        if rc != 0:
            print("[PIPELINE] Brief deja present, on continue.")
    else:
        print("[PIPELINE] Etape 1 sautee (--skip-brief).")

    brief = _brief_for_today()
    if brief is None:
        print(f"[PIPELINE] STOP : aucun brief pour {_today()}.")
        sys.exit(1)

    # Etape 2 : generation du X draft ------------------------------------
    if draft_path.exists():
        print(f"[PIPELINE] Draft X existant : {draft_path.name}")
        x_text = draft_path.read_text(encoding="utf-8").strip()
    else:
        print("[PIPELINE] Etape 2 : generation du X post via Gemini...")
        x_text = generate_x_draft(brief)
        draft_path.write_text(x_text, encoding="utf-8")
        print(f"[PIPELINE] Draft genere ({len(x_text)} chars) :\n{x_text}\n")

    # Etape 3 : gate Telegram --------------------------------------------
    rc = step_gate(draft_path, args.dry_run, args.timeout)
    if rc != 0:
        sys.exit(rc)

    # Etape 4 : post manuel ----------------------------------------------
    # Le texte a ete envoye sur Telegram a l'etape 3.
    # Copie-le depuis le message Telegram et poste-le manuellement sur X.
    x_text = draft_path.read_text(encoding="utf-8").strip()
    print("\n[PIPELINE] APPROUVE. Poste ce texte manuellement sur X :")
    print(f"\n{'-' * 60}")
    print(x_text)
    print(f"{'-' * 60}")
    print(f"\n[PIPELINE] {len(x_text)} caracteres | draft : {draft_path.name}")
    print("[PIPELINE] Termine. Aucune publication automatique.")


if __name__ == "__main__":
    main()
