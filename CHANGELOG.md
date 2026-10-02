# Asso Lab Changelog

Public, dated build log of Asso Lab. Newest first.
Receipts over claims: every entry is dated, and this repository's git history is
the tamper-evident record. For action-level proof, see `proof-of-agent/`.

## Public-surface realignment (2026-10-02)

- Repositioned Asso Lab as a bounded public proof surface derived from Asso and the wider SYSTASYS work.
- Marked June-era ACE identity, doctrine and visual material as historical provenance rather than current parent identity.
- Removed the obsolete social publishing pipeline, scheduler, operator routines, local draft/log artifacts and stale environment example from the current branch.
- Kept receipts, publications, examples, Proof of Agent material and public-safe doctrine available as inspectable evidence.
- Replaced stale public operator instructions with a current public-repository boundary.
- Updated README, START_HERE, STATUS and CONTRIBUTING so public proof is not confused with current private runtime truth.
- Historical changelog entries below are preserved as dated facts. References to files removed from current `main` describe what existed at that time; the git history remains the provenance record.

## v0.5 (2026-06-09)
- Reader-first public model pass.
- Added `START_HERE.md` plain English guide.
- Added `VISUAL_OVERVIEW.md` with diagrams and one-screen tables.
- Added `STATUS.md` to separate public proof from private runtime claims.
- Added `CONTRIBUTING.md` to preserve bounded, evidence-first contribution rules.
- Added Apache-2.0 `LICENSE`.
- Rewrote `README.md` as a public entry point with clear public/private boundary.
- Clarified `ACE-Operating-Doctrine.md` wording for external readers.

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
Historical entries are not current operating instructions. Current public status lives in `STATUS.md`.
