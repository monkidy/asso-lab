# ACE Operating Doctrine

ACE is an applied operating doctrine for agentic governance: closed by default, evidence first, human bounds, and receipts over claims.

It is designed for AI-agent work that needs to stay bounded, reviewable, and revocable.

Autonomy without governance is not intelligence. It is liability.

ACE does not try to make non-deterministic models inherently trustworthy. It constrains what they are allowed to do, records what happened, and keeps human authority explicit.

## Core principles

### 1. Closed by Default

Nothing is allowed unless it is explicitly admitted by the active boundary.

Unexpected input, missing evidence, schema mismatch, stale state, unclear authority, or unsafe scope should halt the path instead of being guessed through.

### 2. Evidence First

Receipts over claims.

An agent saying "done" is not enough. The system should preserve inspectable evidence of what was proposed, what was checked, what was refused, what changed, and what still requires human review.

### 3. Human Bounds

Human authority remains explicit.

Agents may propose, prepare, summarize, transform, or execute inside a valid envelope. They do not create their own authority, expand their own scope, or treat convenience as permission.

### 4. ACE governs admissibility

ACE defines whether an action is admissible.

Asso, or any agent operating under the doctrine, executes only inside an explicit envelope: mandate, boundary, evidence, stop conditions, handoff, and rollback.

### 5. Receipts are boundaries made visible

A receipt is not marketing proof and not formal verification.

It is a code-generated evidence trail: status, hash, sources, timestamp, signature, or other explicit fields when present. Its role is to make review possible and reduce false readiness claims.

### 6. Fail-Closed by Default

When the system cannot prove that an action is allowed, it should stop, surface the reason, and require review.

Fail-open behavior is treated as a defect.

## Public and private boundary

Public repositories demonstrate the doctrine through bounded documentation, SOPs, receipts, examples, and audit trails.

The full runtime remains private until its governance boundaries, safety envelopes, and operator controls are stable enough to expose without creating false authority claims.

Public artifacts do not grant runtime authority, merge authority, trading authority, publishing authority, or permission-to-act.

## Current public artifacts

- `ai-ops-sop-pack`: public SOPs for bounded handoffs, PR audit discipline, cold recovery, and operator review.
- `asso-lab`: public observer surface showing code-generated receipts and traceable briefs.
- `ace-agent-governance-receipt-standard`: public receipt standard for mandate, proposal, action receipt, and refusal receipt shape.
- `asso-execution-bridge`: private runtime and full operating system, not used as public proof until its boundaries are ready to expose.

## Language discipline

Use concrete failure modes before doctrine.

Use public artifacts before claims.

Translate internal language into externally legible engineering terms: boundary, gate, receipt, handoff, control plane, fail-closed, default-deny, audit trail.

Do not claim production readiness, formal verification, autonomous permission-to-act, client adoption, revenue, live execution, or runtime availability without explicit public evidence.

## Version

Version: 0.2
Date: 2026-06-09
Author: Hichem Benali
Status: PUBLIC_DOCTRINE_ANCHOR_V0
