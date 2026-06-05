#!/usr/bin/env python3
"""ACE Telegram Validation Gate.

Envoie un draft au bot Asso_CM, attend la reponse de l'operateur,
et retourne un exit code exploitable par le pipeline.

Usage:
  python telegram_gate.py --text "post text" --channel X
  python telegram_gate.py --file draft.txt --channel LinkedIn
  python telegram_gate.py --file draft.txt --timeout 3600

Exit codes:
  0 = APPROVED  (operateur a repondu ok / oui / valide / go / 1)
  1 = REFUSED   (operateur a repondu non / refuse / stop / 0)
  2 = TIMEOUT ou ERREUR (pas de reponse dans le delai, draft reste en attente)

Doctrine ACE : human bounds before autonomy.
Aucune publication sans confirmation explicite de l'operateur.
"""
import argparse
import os
import sys
import time
from pathlib import Path

try:
    from dotenv import load_dotenv
    _env = Path(__file__).parent / ".env"
    if not load_dotenv(_env):       # essaie le chemin absolu du script
        load_dotenv()               # fallback: CWD (utile si lance depuis ailleurs)
except ImportError:
    pass  # env vars peuvent venir d'ailleurs (session cloud, $env: PowerShell)

APPROVE = {"ok", "oui", "valide", "go", "yes", "1", "approve", "post"}
REFUSE  = {"non", "no", "refuse", "annule", "stop", "0", "cancel", "nope"}

POLL_TIMEOUT  = 30   # secondes par requete long-poll
POLL_INTERVAL = 2    # pause entre deux polls apres erreur reseau


# -----------------------------------------------------------------------------
def _creds() -> tuple[str, str]:
    token   = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
    chat_id = os.environ.get("TELEGRAM_CHAT_ID", "").strip()
    if not token or not chat_id:
        sys.stderr.write(
            "ERROR: TELEGRAM_BOT_TOKEN ou TELEGRAM_CHAT_ID absent.\n"
            "Ajoute-les dans .env ou comme variables de session.\n"
        )
        sys.exit(2)
    return token, chat_id


def _post(token: str, endpoint: str, **kwargs) -> dict:
    import requests
    r = requests.post(
        f"https://api.telegram.org/bot{token}/{endpoint}",
        timeout=15, **kwargs
    )
    r.raise_for_status()
    return r.json()


def _get_updates(token: str, offset: int | None, timeout: int) -> list:
    import requests
    params = {"timeout": timeout, "allowed_updates": ["message"]}
    if offset is not None:
        params["offset"] = offset
    r = requests.get(
        f"https://api.telegram.org/bot{token}/getUpdates",
        params=params,
        timeout=timeout + 5,
    )
    r.raise_for_status()
    return r.json().get("result", [])


def send(token: str, chat_id: str, text: str) -> int:
    """Envoie un message, retourne le message_id."""
    resp = _post(token, "sendMessage", json={"chat_id": chat_id, "text": text})
    return resp["result"]["message_id"]


def wait_for_reply(token: str, chat_id: str, max_wait: int) -> str:
    """Attend une reponse de l'operateur. Retourne 'approved', 'refused' ou 'timeout'."""
    # Purge les updates en attente pour ne pas confondre avec une ancienne reponse
    offset = None
    try:
        stale = _get_updates(token, offset=None, timeout=1)
        if stale:
            offset = stale[-1]["update_id"] + 1
    except Exception:
        pass

    deadline = time.time() + max_wait
    while time.time() < deadline:
        remaining  = deadline - time.time()
        poll_t     = int(min(POLL_TIMEOUT, max(1, remaining)))
        try:
            updates = _get_updates(token, offset=offset, timeout=poll_t)
        except Exception as e:
            sys.stderr.write(f"[GATE] poll error (non-fatal): {e}\n")
            time.sleep(POLL_INTERVAL)
            continue

        for upd in updates:
            offset = upd["update_id"] + 1
            msg    = upd.get("message", {})
            if str(msg.get("chat", {}).get("id", "")) == str(chat_id):
                reply = msg.get("text", "").strip().lower()
                if reply in APPROVE:
                    return "approved"
                if reply in REFUSE:
                    return "refused"
                # Mot cle non reconnu : rappel
                try:
                    send(token, chat_id,
                         f'Reponse non reconnue : "{reply}"\n'
                         'Reponds "ok" pour approuver ou "non" pour refuser.')
                except Exception:
                    pass

    return "timeout"


# -----------------------------------------------------------------------------
def main() -> None:
    ap = argparse.ArgumentParser(description="ACE Telegram Validation Gate")
    ap.add_argument("--text",    help="texte du draft inline")
    ap.add_argument("--file",    help="texte du draft depuis un fichier")
    ap.add_argument("--channel", default="X",
                    help="label du canal de publication (X, LinkedIn...)")
    ap.add_argument("--timeout", type=int, default=1800,
                    help="delai d'attente max en secondes (defaut 1800 = 30 min)")
    args = ap.parse_args()

    text = args.text
    if args.file:
        text = Path(args.file).read_text(encoding="utf-8")
    if not text or not text.strip():
        sys.stderr.write("ERROR: fournis --text ou --file\n")
        sys.exit(2)
    text = text.strip()

    token, chat_id = _creds()

    preview = (
        f"DRAFT {args.channel} — validation requise.\n"
        f"{'—' * 30}\n"
        f"{text}\n"
        f"{'—' * 30}\n"
        f"Longueur : {len(text)} caracteres\n\n"
        f'Reponds "ok" pour approuver ou "non" pour refuser.\n'
        f"(timeout : {args.timeout // 60} min)"
    )

    try:
        msg_id = send(token, chat_id, preview)
    except Exception as e:
        sys.stderr.write(f"ERROR: envoi Telegram echoue : {e}\n")
        sys.exit(2)

    sys.stderr.write(
        f"[GATE] Draft envoye sur Telegram (msg_id {msg_id}, canal {args.channel}).\n"
        f"[GATE] En attente de ta validation (timeout {args.timeout}s)...\n"
    )

    result = wait_for_reply(token, chat_id, args.timeout)

    if result == "approved":
        try:
            send(token, chat_id, f"APPROUVE. Publication {args.channel} en cours.")
        except Exception:
            pass
        print("APPROVED")
        sys.exit(0)

    elif result == "refused":
        try:
            send(token, chat_id, "REFUSE. Draft conserve, aucune publication.")
        except Exception:
            pass
        print("REFUSED")
        sys.exit(1)

    else:
        try:
            send(token, chat_id,
                 f"TIMEOUT ({args.timeout // 60} min). Draft conserve, aucune publication.")
        except Exception:
            pass
        print("TIMEOUT")
        sys.exit(2)


if __name__ == "__main__":
    main()
