#!/usr/bin/env python3
"""ACE Publishing Pipeline.

Chaine complete en un seul lancement :
  1. briefing_orchestrator_v0.py  ->  brief DRAFT du jour
  2. telegram_gate.py             ->  envoi X post draft a Asso_CM, attente ok/non
  3. post_to_x.py                 ->  publication + Proof of Agent receipt

Usage:
  python run_pipeline.py                    # pipeline complet
  python run_pipeline.py --skip-brief       # saute l'etape 1 (brief deja genere)
  python run_pipeline.py --dry-run          # gate + dry-run post (aucune publication)
  python run_pipeline.py --post-text "..."  # X post custom, saute les etapes 1 et 2

Doctrine ACE : human bounds before autonomy.
Aucune publication sans confirmation explicite de l'operateur via Telegram.
"""
import argparse
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    from dotenv import load_dotenv
    _env = Path(__file__).parent / ".env"
    if not load_dotenv(_env):
        load_dotenv()  # fallback CWD
except ImportError:
    pass

ROOT    = Path(__file__).parent.resolve()
PUBDIR  = ROOT / "publications"
DRAFTS  = ROOT / "drafts"


def _today() -> str:
    return datetime.now(timezone.utc).date().isoformat()


def _run(cmd: list[str], label: str) -> int:
    print(f"\n[PIPELINE] {label}")
    print(f"[PIPELINE] > {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=ROOT)
    return result.returncode


def step_brief() -> int:
    """Etape 1 : genere le brief du jour via l'orchestrateur."""
    rc = _run([sys.executable, "briefing_orchestrator_v0.py"], "Etape 1 : generation du brief")
    if rc != 0:
        print(f"[PIPELINE] STOP : orchestrateur sorti avec code {rc}.")
    return rc


def step_gate(text: str, dry_run: bool, timeout: int) -> int:
    """Etape 2 : gate Telegram — envoie le draft, attend la validation."""
    draft_path = DRAFTS / f"{_today()}-x.txt"
    DRAFTS.mkdir(exist_ok=True)
    draft_path.write_text(text, encoding="utf-8")

    cmd = [sys.executable, "telegram_gate.py", "--file", str(draft_path), "--channel", "X", "--timeout", str(timeout)]
    rc = _run(cmd, "Etape 2 : gate Telegram (en attente de ta validation)")
    if rc == 0:
        print("[PIPELINE] APPROUVE.")
    elif rc == 1:
        print("[PIPELINE] REFUSE. Pipeline arrete, draft conserve.")
    else:
        print("[PIPELINE] TIMEOUT ou ERREUR. Draft conserve, aucune publication.")
    return rc


def step_post(text: str, dry_run: bool) -> int:
    """Etape 3 : publication X avec receipt."""
    draft_path = DRAFTS / f"{_today()}-x.txt"
    draft_path.write_text(text, encoding="utf-8")

    cmd = [sys.executable, "post_to_x.py", "--file", str(draft_path)]
    if dry_run:
        cmd.append("--dry-run")
    rc = _run(cmd, "Etape 3 : publication X" + (" (DRY RUN)" if dry_run else ""))
    return rc


def _brief_text_for_today() -> str | None:
    """Retourne le contenu du brief du jour si deja genere."""
    path = PUBDIR / f"{_today()}-briefing.md"
    if path.exists():
        return path.read_text(encoding="utf-8")
    return None


# -----------------------------------------------------------------------------
def main() -> None:
    ap = argparse.ArgumentParser(description="ACE Publishing Pipeline")
    ap.add_argument("--skip-brief",  action="store_true",
                    help="Saute l'etape 1 (brief deja genere aujourd'hui)")
    ap.add_argument("--dry-run",     action="store_true",
                    help="Gate actif, mais post en dry-run (aucune publication reelle)")
    ap.add_argument("--post-text",   help="X post custom (saute les etapes 1+2, poste directement)")
    ap.add_argument("--timeout",     type=int, default=1800,
                    help="Timeout gate Telegram en secondes (defaut 1800 = 30 min)")
    args = ap.parse_args()

    print(f"[PIPELINE] ACE Publishing Pipeline — {_today()}")
    print(f"[PIPELINE] dry-run={args.dry_run} | skip-brief={args.skip_brief}")

    # --- Mode post direct (bypass orchestrateur + gate) ---
    if args.post_text:
        print("[PIPELINE] Mode post direct : gate saute, publication immediate.")
        rc = step_post(args.post_text, args.dry_run)
        sys.exit(rc)

    # --- Etape 1 : brief ---
    if not args.skip_brief:
        rc = step_brief()
        if rc not in (0,):
            # L'orchestrateur sort avec des codes non-zero pour ALREADY_GENERATED etc.
            # On continue si le brief existe deja.
            if _brief_text_for_today() is None:
                sys.exit(rc)
            print("[PIPELINE] Brief deja present, on continue.")
    else:
        print("[PIPELINE] Etape 1 sautee (--skip-brief).")

    # --- Recupere le brief pour construire le X post ---
    brief = _brief_text_for_today()
    if brief is None:
        print(f"[PIPELINE] STOP : aucun brief trouve pour {_today()}.")
        sys.exit(1)

    # --- Prepare le X post draft ---
    # Par defaut : affiche le brief et demande a l'operateur de fournir le X post.
    # Dans un pipeline entierement automatise, ici on appellerait un LLM pour
    # generer le post depuis le brief. Pour l'instant : arret propre avec instruction.
    draft_path = DRAFTS / f"{_today()}-x.txt"
    DRAFTS.mkdir(exist_ok=True)

    if draft_path.exists():
        print(f"[PIPELINE] Draft X existant trouve : {draft_path}")
        x_text = draft_path.read_text(encoding="utf-8").strip()
    else:
        print(f"\n[PIPELINE] Aucun draft X pour {_today()}.")
        print(f"[PIPELINE] Crée le fichier : {draft_path}")
        print(f"[PIPELINE] Puis relance avec --skip-brief.")
        print(f"\n--- Brief du jour (source) ---")
        print(brief[:800] + ("..." if len(brief) > 800 else ""))
        sys.exit(0)

    # --- Etape 2 : gate Telegram ---
    rc = step_gate(x_text, args.dry_run, args.timeout)
    if rc != 0:
        sys.exit(rc)

    # --- Etape 3 : post X ---
    rc = step_post(x_text, args.dry_run)
    sys.exit(rc)


if __name__ == "__main__":
    main()
