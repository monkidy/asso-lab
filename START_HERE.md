# Start here: plain English guide

This page explains Asso Lab without assuming you know ACE, AI governance, or the private runtime.

## The simple idea

AI agents should not only produce answers.

They should leave evidence.

Asso Lab is a public observer surface for ACE. It shows how AI-assisted work can be bounded, reviewed, and recorded through receipts.

## What problem does this solve?

AI systems often say things like:

> Done.

But a human reviewer still needs to know:

- What was done?
- What was not done?
- Which sources were used?
- Was there a receipt?
- Was anything sent, published, deployed, traded, or executed?
- Can the result be reviewed later?

Asso Lab exists to make those questions easier to answer.

## What is a receipt?

A receipt is a small evidence record.

It can contain fields such as:

- status;
- timestamp;
- sources;
- hash;
- signature;
- what happened;
- what did not happen.

A receipt is not a marketing claim. It is something a reviewer can inspect.

## Everyday analogy

Imagine someone says:

> I prepared the report.

A receipt is the trace that lets you check:

- which report;
- when;
- from which sources;
- whether it was only drafted or actually sent;
- who still needs to review it.

That is the difference between a claim and evidence.

## What Asso Lab shows publicly

This repository shows:

- public briefings;
- receipts attached to those briefings;
- code paths that generate or support those records;
- doctrine explaining why AI agents should stay bounded;
- examples of action receipts, including refused actions.

## What Asso Lab does not show

This repository does not expose the full private runtime.

It does not grant agents permission to act.

It does not prove production readiness.

It does not prove that any private system is safe.

It is a public proof surface: a small, inspectable window into the doctrine.

## Who should read this?

### Non-technical visitor

Start here, then open `VISUAL_OVERVIEW.md`.

### Founder or operator

Read the README and the latest receipts to understand the operating discipline.

### Developer

Inspect the scripts, receipt examples, and generated records.

### Compliance, legal, or security reviewer

Focus on the public/private boundary, receipt fields, and claims the repo explicitly refuses to make.

## What to open next

1. `VISUAL_OVERVIEW.md`
2. `README.md`
3. `ACE-Operating-Doctrine.md`
4. `publications/`
5. `receipts/`
6. `examples/action-receipts/`

## One sentence summary

Asso Lab shows how AI-agent work can be made reviewable through bounded briefs, receipts, and evidence trails.
