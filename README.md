# Asso Lab

![Receipt signed by code, 2026-05-27](assets/screenshots/receipt-2026-05-27.png)

**Bounded public observation surface derived from Asso.**

Asso Lab is not Asso itself, and it is not Asso Capital Engine. It is a small public surface for inspecting one part of the work: bounded briefs, receipts, evidence, refusals and reviewable agent actions.

New here? Start with [`START_HERE.md`](START_HERE.md). It explains Asso Lab in plain English.

Prefer diagrams and tables? Open [`VISUAL_OVERVIEW.md`](VISUAL_OVERVIEW.md).

Current status: [`PUBLIC_OBSERVER_SURFACE_V0`](STATUS.md).

## The simple question

How do we know AI-assisted work stayed inside its limits?

Asso Lab gives a small public answer:

> Publish the brief, publish the receipt, keep the boundary visible.

## What this repo is

Asso Lab is a public proof surface derived from the broader Asso / SYSTASYS work.

It demonstrates:

- bounded briefs;
- code-generated receipts;
- traceable sources, hashes, timestamps, and status fields;
- public doctrine for fail-closed agent governance;
- examples of allowed, refused, and human-review agent actions.

The receipt/admissibility doctrine historically published under ACE remains useful here as a narrow governance layer. It is not the parent identity of Asso, SYSTASYS or Asso Capital Engine.

## Why this matters

AI agents should not only answer.

They should leave evidence.

A claim like "done" is not enough. A reviewer should be able to inspect what happened, what did not happen, and what proof exists.

This is the principle:

> Receipts over claims.

## Proof in 30 seconds

1. Open [`publications/`](publications/) and read a public brief.
2. Open [`receipts/`](receipts/) and find its receipt.
3. Check the receipt fields: status, hash, sources, timestamp, signature.
4. Verify that the artifact is a trace, not a marketing promise.

## Who this is for

- people building AI-agent workflows;
- founders and operators using AI automation;
- compliance, legal, security, and risk reviewers;
- developers who want inspectable handoff and receipt patterns;
- non-technical visitors who need to understand what is public proof and what is not.

## How it works

1. Code reads declared sources.
2. The AI proposes inside a bounded envelope.
3. Code generates a receipt describing what happened.
4. The receipt is stored as an audit trail.
5. The result can be reviewed later.

## Public and private boundary

Public artifacts demonstrate the doctrine through bounded documentation, receipts, examples, and audit trails.

The full private systems remain private until their governance boundaries, safety envelopes, and operator controls are stable enough to expose without creating false authority claims.

This public repo does not grant runtime authority, merge authority, trading authority, publishing authority, wallet authority, deployment authority, or permission-to-act.

## What this repo does not prove

This repo does not prove:

- production readiness;
- formal verification;
- live runtime safety;
- private implementation safety;
- client adoption;
- revenue;
- autonomous permission-to-act.

Those claims require separate evidence.

## Main files and folders

- [`START_HERE.md`](START_HERE.md) - plain English guide.
- [`VISUAL_OVERVIEW.md`](VISUAL_OVERVIEW.md) - diagrams and one-screen tables.
- [`STATUS.md`](STATUS.md) - current maturity and proof status.
- [`ACE-Operating-Doctrine.md`](ACE-Operating-Doctrine.md) - public receipt/admissibility doctrine anchor.
- [`publications/`](publications/) - public briefs.
- [`receipts/`](receipts/) - evidence trails.
- [`examples/action-receipts/`](examples/action-receipts/) - static examples of bounded agent actions.
- [`CONTRIBUTING.md`](CONTRIBUTING.md) - contribution rules for the public surface.
- [`CHANGELOG.md`](CHANGELOG.md) - dated build log.

## Related public repos

- [ACE Agent Governance Receipt Standard](https://github.com/monkidy/ace-agent-governance-receipt-standard): public receipt standard.
- [AI Ops SOP Pack](https://github.com/monkidy/ai-ops-sop-pack): public SOPs for bounded handoffs and PR audit discipline.

## Where this sits

- **Asso**: the longitudinal cognitive continuity system.
- **SYSTASYS**: the wider architecture.
- **Asso Capital Engine**: the operating economic layer.
- **Asso Lab**: this bounded public observation surface.

The deeper public map is at https://hichembenali.com/asso.

## Governance doctrine in one line

Closed by Default. Evidence First. Human Bounds. Receipts over claims.

Knowledge is not authority. Proposed action stays inside explicit permission.

## Action receipt examples

Asso Lab includes static [action receipt examples](examples/action-receipts/) showing bounded agent actions: allowed, refused, or requiring human review.

These examples are not runtime proof. They show the public shape of bounded agent governance.

## License

Apache-2.0.
