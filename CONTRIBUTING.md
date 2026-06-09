# Contributing

Asso Lab is a public observer surface for ACE.

Contributions should keep the repo clear, bounded, and evidence-first.

## Principles

1. **Reader first**
   - A first-time visitor should understand what this repo is.
   - Use plain language before internal language.
   - Link examples and receipts from public entry points.

2. **Receipts over claims**
   - Do not add claims that the repo cannot prove.
   - Prefer evidence, receipts, hashes, source lists, screenshots, or validation steps.

3. **Public/private boundary**
   - Do not expose private runtime details.
   - Do not add secrets, credentials, tokens, private logs, or private operator state.
   - Do not imply this public repo grants runtime authority.

4. **Fail closed**
   - If an action is unclear, sensitive, or outside the public envelope, document rather than execute.
   - Public examples should make denied or not-authorized actions explicit.

5. **Keep the surface small**
   - Avoid turning this repo into the full runtime.
   - Keep examples and docs inspectable.
   - Add the smallest useful validation or explanation.

## Good contributions

Good contributions include:

- clearer README, START_HERE, or visual explanations;
- better public receipt examples;
- improved source and hash documentation;
- safer boundary language;
- small validation scripts;
- corrections that reduce ambiguity.

## Avoid

Avoid:

- marketing claims;
- production-readiness claims without proof;
- live execution claims without receipts;
- exposing private runtime details;
- adding dependencies without a strong reason;
- claims that ACE, Asso, or any agent has authority outside explicit envelopes.

## Final check

Before adding a change, ask:

```text
Does this make the public proof surface clearer, safer, or easier to inspect?
```

If not, do not add it.
