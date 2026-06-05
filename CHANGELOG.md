# Asso Lab Changelog

Public, dated build log of Asso Lab and the ACE public surface. Newest first.
Receipts over claims: every entry is dated, and this repository's git history is
the tamper-evident record. For action-level proof, see `proof-of-agent/`.

## v0.4 (2026-06-05)
- Telegram validation gate (`telegram_gate.py`): drafts envoyes a Asso_CM bot, publication bloquee jusqu'a ok/non explicite de l'operateur.
- Pipeline chaine (`run_pipeline.py`): orchestrateur + gate + post_to_x en un seul lancement.
- CLAUDE.md : memoire de session persistante, source de verite pour tout nouveau run Claude Code.
- Google Calendar : event quotidien 13h CET "ACE Brief : verifier + poster" (popup + email).
- Fix dotenv : chargement .env robuste sur Windows (fallback CWD).

## v0.3 (2026-06-05)
- Proof of Agent: public receipt surface live (`proof-of-agent/`), with a dated origination mark.
- Canonical comms format: `docs/comms-field-note-format.md`, single source of truth for X and LinkedIn (ACE Field Note structure, R.O.C, no em dash).
- Intelligence watch routine (private, 3x per weekday): leads, competitors, hot topics, OSS for ACE.

## v0.2 (2026-06-04)
- Daily comms-prep routine (weekdays, 18h Paris): drafts the X post, thread, and LinkedIn version in the ACE Field Note format.
- X presence structured: thesis post pinned, bio cleaned, two private radar lists (Agents & Governance, AI & Society).
- Receipt integrity documented: CRLF-normalized sha256 before comparing to a receipt content_hash.

## v0.1 (2026-05, baseline)
- Asso Lab established as the public observer of ACE: weekday briefings generated with code-signed receipts (briefing orchestrator).

---
This changelog grows as the project advances. One milestone per shipped step, dated, versioned.
