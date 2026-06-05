#!/usr/bin/env python3
"""
ACE-Receipt v1 -- format de preuve UNIFIE pour asso-lab.
========================================================
Un seul format pour TOUTES les preuves de la chaine editoriale quotidienne :
  - brief publie        (action_class="brief_publish")
  - post X              (action_class="x_post" / "x_reply")
le post X reference le brief dont il derive via links.parent_receipt_id.

Principes (doctrine ACE) :
  - Le receipt est produit par le CODE, jamais par le LLM.
  - confidence n'est jamais auto-declaree par le LLM (calculee ou None).
  - Hard defaults : permission_to_act=False, capital_at_risk="ZERO".
  - RECEIPTS_PROVE_NOT_AUTHORIZE : un receipt prouve, il n'autorise pas.

Module autonome (stdlib only). Aligne sur le standard cross-repo ace_receipt.v1.
Les anciens receipts (legacy) restent immuables ; le crosswalk permet de les LIRE en v1.
"""
from __future__ import annotations
import json
import uuid
from datetime import datetime, timezone
from pathlib import Path

ACE_RECEIPT_VERSION = "ace_receipt.v1"
VALID_STATUS = {"DRAFT", "REVIEWED", "PUBLISHED", "EXECUTED", "SIMULATED",
                "REFUSED", "REJECTED_AT_GATE", "ABORTED", "NO_OP", "CLOSED"}
VALID_SURFACE = {"asso-lab", "asso-execution-bridge", "ACE-LAB-GATEWAY", "unknown"}
DOCTRINE = "RECEIPTS_PROVE_NOT_AUTHORIZE"


def _utc_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def build(action_class, surface="asso-lab", actor="code", operator="hichem",
          status="DRAFT", content_hash=None, sources=None, confidence=None,
          source_schema="asso-lab", receipt_id=None, timestamp_utc=None,
          links=None, stop_ace_present=None) -> dict:
    """Construit un ACE-Receipt v1 (hard defaults de surete appliques)."""
    rid = receipt_id or str(uuid.uuid4())
    return {
        "ace_receipt_version": ACE_RECEIPT_VERSION,
        "receipt_id": rid,
        "timestamp_utc": timestamp_utc or _utc_iso(),
        "surface": surface if surface in VALID_SURFACE else "unknown",
        "actor": actor or "code",
        "operator": operator or "hichem",
        "action_class": action_class or "unknown",
        "status": status if status in VALID_STATUS else "NO_OP",
        "content_hash": content_hash,
        "sources": list(sources) if sources else [],
        "confidence": confidence,
        "safety": {"permission_to_act": False, "capital_at_risk": "ZERO",
                   "stop_ace_present": stop_ace_present},
        "provenance": {"source_schema": source_schema, "source_id": rid,
                       "doctrine_marker": DOCTRINE},
        "links": links or {},
    }


def validate(rec) -> list:
    """Retourne la liste des erreurs (vide = valide)."""
    errs = []
    req = ["ace_receipt_version", "receipt_id", "timestamp_utc", "surface",
           "actor", "operator", "action_class", "status", "safety", "provenance"]
    for k in req:
        if k not in rec or rec[k] in (None, ""):
            errs.append("missing:" + k)
    if rec.get("ace_receipt_version") != ACE_RECEIPT_VERSION:
        errs.append("bad_version")
    if rec.get("status") not in VALID_STATUS:
        errs.append("bad_status:" + str(rec.get("status")))
    s = rec.get("safety", {})
    if not isinstance(s, dict) or "permission_to_act" not in s or "capital_at_risk" not in s:
        errs.append("bad_safety")
    return errs


# --- lecture du parent (le brief du jour) pour lier le post X ---
def read_brief_parent(root: Path, date_str: str):
    """Retourne (receipt_id, timestamp) du brief du jour, v1 OU legacy. (None,None) si absent."""
    p = Path(root) / "receipts" / (date_str + "-receipt.json")
    try:
        r = json.loads(p.read_text(encoding="utf-8"))
        return r.get("receipt_id"), (r.get("timestamp_utc") or r.get("date_utc"))
    except Exception:
        return None, None


# --- crosswalk legacy -> v1 (LECTURE seule ; on ne reecrit jamais les originaux) ---
def from_legacy_brief(r) -> dict:
    return build("brief_publish", surface="asso-lab", actor=r.get("model", "llm"),
                 operator=r.get("operator", "hichem"),
                 status=str(r.get("status", "DRAFT")).upper(),
                 content_hash=r.get("content_hash"), sources=r.get("sources"),
                 confidence=r.get("confidence"), source_schema="ace-receipt-spec(legacy)",
                 receipt_id=r.get("receipt_id"), timestamp_utc=r.get("date_utc"))


def from_legacy_proof_entry(r, parent_id=None, parent_date=None) -> dict:
    links = {}
    if r.get("target"):
        links["target"] = r["target"]
    if r.get("tweet_id"):
        links["tweet_id"] = r["tweet_id"]
    if parent_id:
        links["parent_receipt_id"] = parent_id
        links["parent_date"] = parent_date
    return build(r.get("action", "x_post"), surface="asso-lab",
                 actor=r.get("agent", "claude (ACE CM)"), operator=r.get("operator", "hichem"),
                 status=str(r.get("status", "EXECUTED")).upper(),
                 content_hash=r.get("content_hash"), source_schema="proof-of-agent(legacy)",
                 receipt_id=r.get("receipt_id"), timestamp_utc=r.get("date_utc"), links=links)
