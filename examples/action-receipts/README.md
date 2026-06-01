# ACE Action Receipt Examples

These examples show the difference between a publication receipt and an action receipt.

Asso Lab already demonstrates publication receipts: a brief was produced, sourced, hashed, timestamped, and stored.

Action receipts demonstrate a stricter pattern:

- what the agent requested
- what boundary applied
- what checks ran
- what was allowed or refused
- what still requires human review

These files are static examples.

They do not prove live execution.
They do not grant runtime authority.
They are not compliance certification.
They are not formal verification.

They show the public shape of bounded agent governance.

## Examples

- `bounded_file_read.allowed.json` — an agent requests read-only access inside a bounded scope.
- `forbidden_write.refused.json` — an agent requests a write action outside its boundary and is refused.
- `export.needs_human_review.json` — an agent requests export of data and requires human approval.

## Core idea

A model saying "done" is not evidence.

A receipt should make review possible:

- what was proposed
- what was checked
- what was refused
- what changed
- what still needs human review
