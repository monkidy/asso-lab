# ACE Field Note: R.O.C Comms Format

Canonical comms format for Asso Lab public communication on X and LinkedIn.
This file is the single source of truth. The comms routine and any operator read
it instead of carrying the format inside a prompt. Update the format here, not in
a routine prompt.

North star: **Receipts over claims (R.O.C).** One owned phrase. Everything ladders
back to it.

---

## Hard rules (non-negotiable)

1. **No em-dash, ever.** Never use the long dash character in any content written
   for Hichem. It reads as machine-written and disrespects the reader. Use a
   comma, a colon, a period, or parentheses instead. This rule applies to posts,
   replies, the bio, threads, LinkedIn, and everything else.
2. **No links in the post body.** X throttles reach on posts with external links.
   All links go in the reply to the last tweet of a thread, never in the body.
3. **Proof over summary.** A screenshot of a real receipt or terminal beats
   abstract text and is not penalized like a link. Show the work, not the
   conclusion. This is the unfair advantage: the product is literally the proof.
4. **Language discipline.** X output is English. LinkedIn output is French. Never
   mix two languages in one piece. It confuses the topic model and the reader.
5. **Receipt integrity check before claiming PUBLISHED.** Normalize CRLF to LF
   before computing sha256. On Windows with core.autocrlf=true, git stores LF but
   checks out CRLF, so a raw sha256 of the working-tree file will not match the
   receipt content_hash. Normalize line endings first, then compare.

---

## The post: ACE Field Note structure

1. Line 1: a contrarian hook that stops the scroll.
2. Two to three lines: the insight, seen through the R.O.C lens.
3. Proof when possible (a number, a fact, or a receipt screenshot).
4. Final line: a principle, usually a variant of "Receipts over claims."

Constraints: zero links in body, zero em-dash, single clean post under 280
characters when posted solo.

Posting default for a small account: post the solo first. A thread splits
attention when initial engagement is near zero. Release the thread only once a
post starts to gain traction.

---

## The thread: 6 to 8 tweets

1. Hook (works as a standalone banger if the thread is cut).
2. Reframe the question the field is actually asking now.
3. The shape of the answer (the control layer, the gate, R.O.C).
4. The trade: cost versus payoff, stated plainly.
5. A concrete failure mode the reader has not considered.
6. The through-line: autonomy is not the hard problem, traceability is.
7. The thesis, with a receipt screenshot attached here.
8. CTA: follow plus repost the top post. Sources go in the reply below.

Reply to tweet 8 (and only here): the sources and the brief link.

---

## LinkedIn: French structure

1. Hook on line 1, same contrarian energy, in French.
2. Short paragraphs, one idea each, generous white space.
3. The R.O.C angle stated as a point of view, not a summary.
4. Proof or concrete example.
5. Close on the principle.
6. No links in the body. Put the link in the first comment.

---

## Series identity

Every brief is published as **ACE Field Note #N**. The consistent prefix lets the
algorithm and the audience recognize the series. Number increments per published
brief.

---

## Reply game: the real lever

Spend most X time replying, not posting. A sharp early reply (ten to thirty
minutes after a bigger account posts) places the account in front of that
audience. Add value, never dunk. Aim to be the smartest voice in the thread.

Reusable R.O.C reply angles:

- Enforcement versus audit are different layers. The gate denies, the receipt
  proves the gate held. Collapsing them is security theater.
- An agent saying "done" is not evidence. Preserve what was proposed, checked,
  refused, and changed.
- Permission surface beats capability surface. Deny the call before it exists,
  do not just cap it at runtime.
- Fail-closed is a feature, not a limitation. When the system cannot prove an
  action is allowed, stopping is the correct behavior.

---

## Target roster: seed for the X List "agents / governance"

Curated names for the reply game and the List. Verify the live handle before
adding anyone to the List. Do not assert a handle from memory.

- Simon Willison (LLM tooling, daily field notes).
- swyx (AI engineering, learn in public).
- Charity Majors (observability, "test in prod").
- Hamel Husain (applied LLM evaluation).
- @killix (Issam Hakimi): pointed, technical interlocutor already engaging on
  ACE architecture. Cultivate this one.

Caution: some accounts leave highly calibrated, perfectly on-thesis comments on a
low-view account. Enjoy the validation and engage the ideas in public, but do not
click profile links, be wary of DMs, and verify before following. @BbSrl24 was
flagged on profile signals: engage the idea, do not follow or click.

---

## Repurpose one into four

One brief produces: one X post, one thread, one LinkedIn post (French), one
newsletter snippet. Create once, distribute everywhere. The routine produces all
four in a single run.

---

## Metrics that matter

Watch impressions, then profile visits, then follows. Likes are vanity. Find the
posts that produce follows and make more of those. Stop guessing from likes.
