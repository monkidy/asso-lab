#!/usr/bin/env python3
"""
verify_chain -- controle la chaine editoriale d'un jour au format ACE-Receipt v1.
================================================================================
Charge le brief (parent) + les posts X (enfants), valide tout en v1, et verifie
que chaque post pointe vers le brief via links.parent_receipt_id.

Les receipts v1 sont lus nativement ; les receipts legacy sont PROJETES en v1 via
le crosswalk (lecture seule -- les fichiers originaux ne sont jamais reecrits).

Usage:
  python verify_chain.py              # aujourd'hui (UTC)
  python verify_chain.py 2026-06-04   # un jour precis
"""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import ace_receipt as arc

ROOT = Path(__file__).parent.resolve()


def _load(p):
    try:
        return json.loads(Path(p).read_text(encoding="utf-8"))
    except Exception:
        return None


def _brief_as_v1(r):
    if r is None:
        return None
    if r.get("ace_receipt_version") == arc.ACE_RECEIPT_VERSION:
        return r
    return arc.from_legacy_brief(r)


def verify(date_str: str) -> dict:
    brief = _brief_as_v1(_load(ROOT / "receipts" / (date_str + "-receipt.json")))
    bid = brief.get("receipt_id") if brief else None
    bts = brief.get("timestamp_utc") if brief else None

    proof = _load(ROOT / "proof-of-agent" / "receipts" / (date_str + ".json"))
    posts = []
    for e in (proof.get("receipts", []) if proof else []):
        if e.get("ace_receipt_version") == arc.ACE_RECEIPT_VERSION:
            posts.append(e)
        else:
            posts.append(arc.from_legacy_proof_entry(e, bid, bts))  # projection liee

    rep = {"date": date_str, "brief_present": brief is not None,
           "brief_valid": (arc.validate(brief) == []) if brief else False,
           "brief_receipt_id": bid, "posts": len(posts),
           "posts_valid": 0, "posts_linked": 0, "errors": []}
    for p in posts:
        errs = arc.validate(p)
        if not errs:
            rep["posts_valid"] += 1
        else:
            rep["errors"].append({"post": p.get("receipt_id"), "errs": errs})
        if bid and p.get("links", {}).get("parent_receipt_id") == bid:
            rep["posts_linked"] += 1
    rep["chain_ok"] = bool(brief and rep["brief_valid"]
                           and rep["posts_valid"] == len(posts)
                           and rep["posts_linked"] == len(posts))
    return rep


if __name__ == "__main__":
    d = sys.argv[1] if len(sys.argv) > 1 else datetime.now(timezone.utc).date().isoformat()
    print(json.dumps(verify(d), indent=2, ensure_ascii=False))
