# ACE Visual Charter V1

Status: REVIEWABLE (V1). Canonical, cross-fleet visual doctrine for ACE / Asso.

This document does not invent a new brand. It consolidates the two visual
identities that already shipped into one dual-mode system, so every repo points
at a single source of truth.

Sources consolidated:
- `asso-lab/brand/BRAND.md` (light "proof layer" identity: ink on paper, monospace, verification seal).
- `asso-execution-bridge/assets/brand/README_ACE_BRAND_V0.md` plus `apps/ace-board-control-room/src/styles.av0.css` (dark "operator surface" identity: obsidian and glacier blue).

## 1. Principle

ACE is an operating system for bounded agent execution. The brand should look
like what it is: verifiable, dated, auditable. Sober, technical, never flashy.
Receipts over claims: no surface states "live" or "production" without a proof
it can point to.

## 2. Two modes, one system

The fleet has two surface families. They share semantics and type. They differ
only in luminance. A surface picks ONE mode and stays in it; do not mix paper
and obsidian on the same screen.

- LIGHT mode: docs, README, public proof, receipts, social. The "ink on paper" proof identity.
- DARK mode: apps, the ACE Control Room, operator runtime surfaces. The "obsidian operator" identity.

## 3. Color tokens

### 3.1 Light mode (proof / docs)
| Token | Hex | Use |
| --- | --- | --- |
| ink | `#111111` | primary text, marks |
| paper | `#FAFAF7` | background |

### 3.2 Dark mode (apps / Control Room)
| Token | Hex | Use |
| --- | --- | --- |
| obsidian | `#0F1115` | background base |
| graphite | `#1A1E26` | background gradient stop |
| ice | `#C8DDF0` | highlight, primary text on dark, wordmark fill |
| ash | `#6E7785` | auxiliary text, outlines, parked / neutral |

Implementation note: the live Control Room CSS currently runs a deeper obsidian
variant (base `#050B0E` to `#0A1620`, glacier `#76D0F2` / `#A0BCFF`). Treat the
values in the table as the canonical spec; surfaces should converge on it. This
is a tracked implementation delta, not a contradiction.

### 3.3 Shared semantic accents (BOTH modes)
These carry meaning. Use them ONLY for their state, never for decoration.

| Token | Hex | The ONLY thing it may signal |
| --- | --- | --- |
| verified-green | `#1FA463` | verified, allowed, pass, live-OK |
| live-blue (glacier) | `#7BA9D9` | info, running, interactive, live link (non-alarm) |
| stop-red | `#DC2626` | STOP, risk, refused, fail-closed, blocked. RESERVED. |

Hard rule (gate doctrine): green means allowed/verified, red means refused/stop.
Red is never used for emphasis or decoration. Blue is the only "live/running"
accent that is not an alarm. Green confirms a proven-good state.

## 4. Status semantics (badges, status cards, dashboards)

One color per state, mirroring the runtime:

- LIVE_OK / VERIFIED / PASS  -> verified-green
- RUNNING / INFO / LIVE (neutral)  -> live-blue
- STOP_ACE / RISK / REFUSED / FAIL_CLOSED  -> stop-red
- PARKED / NEUTRAL / UNKNOWN  -> ash (dark) or 60% ink (light)

Never show a green "live" badge that a receipt cannot back. Unproven status is
neutral, not green.

## 5. Typography

- JetBrains Mono (fallback IBM Plex Mono): marks, wordmark, hashes, receipts, code, status tokens. Mono signals code and proof.
- Inter: body and headlines.
- SVG assets use system-font fallbacks by design (no `@font-face`); outline text to paths for hi-fi print.

## 6. Marks

- Wordmark: `[ ACE ]`, brackets in verified-green, encoding "bounded execution" (`asso-lab/brand/wordmark.svg`).
- Proof seal: stamped double ring with a green check, meaning "Proof of Agent"; use as signature mark and as a watermark on proof screenshots (`asso-lab/brand/proof-seal.svg`).
- App monogram (dark surfaces): the geometric chevron-stack ACE mark (`asso-execution-bridge/assets/brand/ace_logo_mark_v0.svg`).
- ACE expands to "Asso Capital Engine", the operator surface. It is distinct from the AAS trading runtime; the mark is not a fintech or coin mark.

## 7. Tone and claims

- Voice: premium, sober, high-trust. Operating-system calm, not hype, not cyberpunk, not casino.
- No em dashes in prose (house rule). Use commas, colons, parentheses, or short sentences.
- Whitespace is part of the brand. No neon, no flashy effects, no gradients beyond the documented obsidian base.
- Claims discipline: every "live / production / 24-7" statement must link to a proof (receipt, run id, or checkpoint). Absent proof, describe status honestly (v0, prototype, reviewable, bounded).

## 8. Application by surface

| Surface | Mode | Notes |
| --- | --- | --- |
| README / docs (public) | Light | link this charter; sober headers |
| Proof receipts / social | Light | proof-seal watermark |
| ACE Control Room UI | Dark | obsidian base, glacier / green / red status tokens |
| Operator runtime surfaces | Dark | status semantics from section 4 |
| Profile / namesake (monkidy) | Light, text-only | sober tone, no badges needed |
| Markdown packs (ai-ops-sop-pack) | Light, text-only | consistent headers, status vocabulary |

## 9. Provenance

This V1 supersedes nothing destructively. `brand/BRAND.md` (asset specs and SVGs)
and `assets/brand/README_ACE_BRAND_V0.md` (app mark and ICO instructions) remain
the asset companions. This charter is the cross-fleet doctrine they both serve.

Receipts over claims.
