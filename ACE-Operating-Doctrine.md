# ACE Operating Doctrine

ACE is a doctrine for governing agentic execution. It is not a product, not a
service, and not a runtime you can buy or invoke. This document states what ACE
publicly claims — and, just as clearly, what it does not.

## Doctrine, not product

ACE is a set of operating principles. The artifacts in this repository document
those principles and show traces of them being applied. They do not package,
sell, or expose a system. Where a runtime exists, it is private (see below).

## Principles

- **Closed by Default** — capabilities are denied unless explicitly opened.
  Nothing is permitted because it was not forbidden.
- **Evidence First** — a claim without a trace is treated as unproven. The
  burden is on the system to show what it did, not on the reader to trust it.
- **Human Bounds** — agents operate inside limits set by a responsible human.
  The human defines the envelope; the agent does not widen it.
- **Receipts over Claims** — the code emits receipts describing what was done.
  The model does not certify its own output.
- **Fail-Closed by Default** — on doubt, error, or missing precondition, the
  system stops rather than proceeds. The safe state is "do nothing."
- **ACE governs admissibility; Asso executes only inside an explicit envelope.**
  ACE decides what is allowed to happen. Asso carries out only the actions that
  fall inside a declared, bounded envelope — never beyond it.

## Public artifacts vs private runtime

Public repositories demonstrate the doctrine through bounded documentation,
receipts, and audit trails. They are evidence that the principles are being
practiced, not a window into the engine.

The full runtime remains private until governance boundaries, safety envelopes,
and operator controls are stable enough to expose without creating false
authority claims. Exposing it earlier would risk implying authority the system
has not earned.

Public artifacts do not grant runtime authority, merge authority, trading
authority, publishing authority, or permission-to-act. They are documentation
and evidence — nothing in them authorizes anyone or anything to act on your
behalf.

## Receipts vs verification

Current public receipts are evidence trails, not formal verification or
production certification. A receipt records that an action happened, with its
sources, hash, timestamp, and status. It does not constitute formal
verification, and it is not a guarantee of correctness or of production
readiness.

## What this doctrine does not claim

- It does not claim to be production-ready.
- It does not claim to be fully autonomous; execution is bounded and
  human-governed.
- It does not claim that receipts are verified proofs; they are audit trails.
- It does not claim any guaranteed outcome.
- It does not claim formal verification of the system or its outputs.
- It does not expose a live runtime; the runtime is private and non-public.
- It does not grant any permission-to-act, in public or in private.
