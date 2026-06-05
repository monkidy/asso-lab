#!/usr/bin/env python3
"""Proof of Agent — X publisher.

Reads X API credentials from .env.x (local, gitignored, never committed).
Posts a tweet via OAuth 1.0a user context and appends a Proof of Agent receipt.

Usage:
  python post_to_x.py --verify              # read-only: confirm creds + account (no post)
  python post_to_x.py --text "..." --dry-run  # show what would post, no API call
  python post_to_x.py --text "..."          # post + receipt
  python post_to_x.py --file path.txt       # post text from a file + receipt

The agent acts; the receipt proves it. Human bounds before autonomy.
"""
import argparse
import hashlib
import json
import os
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).parent.resolve()

from dotenv import load_dotenv
load_dotenv(ROOT / ".env.x")

REQUIRED = ["X_API_KEY", "X_API_SECRET", "X_ACCESS_TOKEN", "X_ACCESS_TOKEN_SECRET"]
# Long-dash characters Hichem bans (AI tell). Posting is refused if present.
BANNED_DASHES = ["—", "―"]  # em dash, horizontal bar


def _creds() -> dict:
    missing = [k for k in REQUIRED if not os.environ.get(k)]
    if missing:
        sys.stderr.write("ERROR: missing in .env.x: " + ", ".join(missing) + "\n")
        sys.exit(1)
    return {k: os.environ[k] for k in REQUIRED}


def _client():
    try:
        import tweepy
    except ImportError:
        sys.stderr.write("ERROR: tweepy not installed. Run: python -m pip install tweepy\n")
        sys.exit(1)
    c = _creds()
    return tweepy.Client(
        consumer_key=c["X_API_KEY"],
        consumer_secret=c["X_API_SECRET"],
        access_token=c["X_ACCESS_TOKEN"],
        access_token_secret=c["X_ACCESS_TOKEN_SECRET"],
    )


def _sha_lf(text: str) -> str:
    return hashlib.sha256(text.replace("\r\n", "\n").encode("utf-8")).hexdigest()


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _append_receipt(action: str, target: str, content: str, extra: dict = None) -> dict:
    date = datetime.now(timezone.utc).date().isoformat()
    rec_dir = ROOT / "proof-of-agent" / "receipts"
    rec_dir.mkdir(parents=True, exist_ok=True)
    path = rec_dir / f"{date}.json"
    if path.exists():
        doc = json.loads(path.read_text(encoding="utf-8"))
    else:
        doc = {
            "surface": "Proof of Agent",
            "account": "@dismerciatonton",
            "date": date,
            "doctrine": "receipts over claims; fail-closed by default; human bounds before autonomy",
            "agent": "claude (ACE CM)",
            "operator": "hichem",
            "receipts": [],
        }
    rec = {
        "receipt_id": str(uuid.uuid4()),
        "date_utc": _utc_now_iso(),
        "action": action,
        "target": target,
        "content_hash": _sha_lf(content),
        "agent": "claude (ACE CM) via post_to_x.py",
        "operator": "hichem",
        "status": "EXECUTED",
    }
    if extra:
        rec.update(extra)
    doc.setdefault("receipts", []).append(rec)
    path.write_text(json.dumps(doc, indent=2, ensure_ascii=False), encoding="utf-8")
    return rec


def main() -> None:
    ap = argparse.ArgumentParser(description="Proof of Agent X publisher")
    ap.add_argument("--text", help="tweet text")
    ap.add_argument("--file", help="read tweet text from a file")
    ap.add_argument("--verify", action="store_true", help="read-only auth check, no post")
    ap.add_argument("--dry-run", action="store_true", help="show what would post, no API call")
    args = ap.parse_args()

    if args.verify:
        try:
            me = _client().get_me()
            u = me.data
            print(f"AUTH OK as @{u.username} (id {u.id}). Credentials valid, read confirmed.")
            print("Write permission is confirmed only on the first real post.")
        except Exception as e:
            sys.stderr.write(f"AUTH FAILED: {e}\n")
            sys.exit(1)
        return

    text = args.text
    if args.file:
        text = Path(args.file).read_text(encoding="utf-8")
    if not text or not text.strip():
        sys.stderr.write("ERROR: provide --text or --file\n")
        sys.exit(1)
    text = text.rstrip("\n")

    for d in BANNED_DASHES:
        if d in text:
            sys.stderr.write("REFUSED: text contains a long dash. Hichem's rule: never. Fix before posting.\n")
            sys.exit(2)

    if len(text) > 280:
        sys.stderr.write(f"WARNING: text is {len(text)} chars (>280). X may reject without a long-post entitlement.\n")

    if args.dry_run:
        print("DRY RUN. Would post:\n---\n" + text + "\n---")
        print("len:", len(text), "| content_hash:", _sha_lf(text))
        return

    client = _client()
    try:
        resp = client.create_tweet(text=text)
    except Exception as e:
        sys.stderr.write(f"POST FAILED: {e}\n")
        sys.exit(1)
    tid = resp.data["id"]
    url = f"https://x.com/dismerciatonton/status/{tid}"
    rec = _append_receipt("x_post", url, text, extra={"tweet_id": str(tid)})
    print("POSTED:", url)
    print("RECEIPT:", rec["receipt_id"], "| content_hash:", rec["content_hash"])


if __name__ == "__main__":
    main()
