---
name: dev-signoff-writer
description: Write a Dev sign-off from raw manual-test notes (steps taken, test data, network calls, a screenshot annotation) and post it as a Jira comment with CC mentions. Finds the one thing worth flagging using the SUCCESs framework (Made to Stick), writes it in plain ELI5 language with every acronym spelled out on first use, tightens the language against a built-in AI-pattern checklist (zero em dashes, no filler, real contractions), and renders any step-by-step testing as a flat S.No | Action | Expected Result table. Fully self-contained — no other skill needs to be loaded. Use when Divy pastes test notes and asks for a "Dev sign-off," a "sign-off comment," or to write up manual testing/validation results for a ticket, especially when a screenshot has a handwritten annotation calling out an edge case the happy-path steps missed.
---

# Dev Sign-Off Writer

One recurring output: a short Jira comment that says "this works, except for this one
real case, and here's the decision someone needs to make." Self-contained — every rule
below is the whole pipeline, nothing else needs loading. Run the four steps in order,
never write this from scratch.

## Step 1: Find the one thing worth flagging (SUCCESs)

Made to Stick's framework, applied to a bug-report-length note, not a whole essay:

- **Simple** — one sentence: what breaks, for whom, when.
- **Unexpected** — why does the happy-path testing miss this? (usually: the tested case
  is 1-to-1, the real case is 1-to-many, or vice versa)
- **Concrete** — a real value from the actual test data or screenshot (a member ID, an
  error string, a temp ID), never an invented example.
- **Credible** — cite the exact repro: click path, the request/response, the on-screen
  text.
- **Emotional** — state the real-world consequence in one line (who gets stuck, and
  when it hurts most), not hype. Not "this is critical" — say what actually happens.
- **Story** — walk it as a short before/after: what today's logic assumes, and the
  input that breaks the assumption.

If the raw notes don't contain a genuine gap (all cases pass clean), skip this step
and write a plain pass confirmation. Don't manufacture a "gap" to fill the format.

## Step 2: Write it ELI5 — ban acronyms and jargon

Every acronym gets spelled out in plain words the first time it appears, in the sentence
itself, not a footnote. `TTL` becomes "the 60-day cool-down" (the actual number, not the
concept-name). `NICU` becomes "any hospital admitting a newborn," not "Neonatal Intensive
Care Unit" — spelling out the acronym is still jargon; say what it means in practice.

Rule of thumb: if a smart friend outside engineering would have to ask what a word
means, replace the word with the thing it refers to.

## Step 3: Tighten the language

Scan the drafted text against this checklist before posting. Fix every hit; don't
eyeball it, actually search for each pattern.

**Cut on sight (phrase-level):**

| Pattern | Example | Fix |
|---|---|---|
| Em dash | "the fix — once merged — closes this" | Rewrite with a comma or period. Search-count the `—` character; the answer must be 0. A single read-through misses them — this is the single most-missed step across every prior run of this pipeline. |
| Contraction-free register | "It is not your setup, and the step does not need re-running" | "It isn't your setup, and the step doesn't need re-running." Write "isn't / doesn't / can't / won't" wherever a person would say it that way. Flag any 200+ word stretch with zero contractions. |
| Hollow intensifiers | "crucial", "essential", "significantly" | Say the actual size or consequence instead. |
| AI vocabulary | "leverage", "seamless", "robust", "streamline", "utilize", "comprehensive", "facilitate" | Plain verb: use, works everywhere, solid, simplify, use, full, help. |
| Hedge phrases | "It's important to note that", "One might argue" | Cut the hedge, state the claim. |
| Filler openers | "At the end of the day", "The truth is", "In today's landscape" | Cut; start with the actual point. |
| Honesty-disclaimer phrases | "I'll be honest", "stated bluntly", "put bluntly" | Cut. Just state the claim. |
| Runway sentences | vague hype line before the real detail | Cut the runway, open with the substance. |

**Cut on sight (structural):**

- Opens with a generic claim instead of the specific finding.
- Bullet/fragment stacking used as punchlines ("X. Y. Z." format) — rewrite as one
  real sentence.
- Three-part parallel structure ("It's not about X. It's about Y. It's about Z.") —
  collapse to one direct sentence.
- Contrast-negation ("This isn't about X. It's about Y.") — rewrite as a positive
  declarative statement.
- Credential-stacking or multi-clause throat-clearing before the actual point.
- Grandiose-importance closer ("Everything here is a footnote to that sentence.",
  "It all comes down to this.") — cut, or replace with the concrete next action.
- Punchy orphan mic-drop closer as a standalone fragment — fold into a real final
  paragraph or drop it.
- Every list item opening with the same word (a repeated pseudo-label verb) — vary
  the openers or drop the verb and name the thing directly.

Cut words, don't cut substance. Every finding and every open question from Step 1
survives — just said in fewer words, in the reader's own idiom.

## Step 4: Render steps as a flat table

If the raw notes include a numbered procedure (click-path + expected result), render it
as a single flat table — no journeys, no named parts, no edge-case sweep:

```
| S.No | Action | Expected Result |
|---|---|---|
| 1 | ... | ... |
```

Setup/test-data goes in its own small table above the steps table if there's a
health-plan/member-ID/config matrix worth naming, rather than folded into row 1 —
a sign-off usually has fixed reference data rather than a single setup action.

Never invent test data, member IDs, or error text to fill a row. Pull every value from
what was actually pasted or screenshotted; if a value is missing, leave the cell as an
open question instead of guessing.

## Output shape

```
Dev Sign-Off: <short title>

<one-line bottom line: what was validated, what passed, what didn't>

<Setup / test data table, if any>

<Steps tested, as the S.No | Action | Expected Result table, if any>

<the one gap, if any — SUCCESs-shaped, plain language, 3-5 short paragraphs max>

Ask: <the specific decision someone needs to make, one sentence>

CC: <names>
```

Keep the whole thing short. A sign-off is not a test plan — no journeys, no edge-case
generator sweep, no scoring pass. One gap, well told, beats five gaps skimmed.

## Posting to Jira

Never hand-write the Atlassian Document Format (ADF) JSON or resolve names to Jira
account IDs by re-deriving the mention structure each time — it's a deterministic,
repeatable operation, so it lives in `scripts/post_signoff.py` instead of being
regenerated by hand on every run:

```bash
# Resolve names to account IDs first if any are ambiguous or unconfirmed
python3 scripts/post_signoff.py resolve "vidhi" "jeremy" "lakshman"

# Post a new comment (reads the sign-off body from a local markdown file)
python3 scripts/post_signoff.py post ICS-25 signoff.md --cc "Vidhi Kakani,Jeremy Wdowik,lakshmankishore.k"

# Update an existing comment in place instead of posting a new one
python3 scripts/post_signoff.py post ICS-25 signoff.md --cc "..." --comment-id 604812
```

The script:
- Reads `~/.config/jira/credentials.env` for auth.
- Converts the markdown body (headings, bold, tables, blockquotes) to ADF — including
  real ADF tables, not pipe-text that renders as a wall of text in Jira.
- Resolves each CC name via `user/search`, preferring an exact `displayName` match over
  Jira's fuzzy token match. **If a name still returns more than one match** (this
  happened with "Jeremy" — Jeremy Jones, Jeremy Wdowik, and Jeremy.Rizalte all exist),
  the script prints every match and refuses to guess. Confirm with the user which one,
  then pass the exact `displayName` or `accountId`.
- Emits real Jira `mention` nodes so CC'd people actually get notified — not plain
  `@Name` text, which is inert.

If the Atlassian MCP is connected instead of the `gh`/curl + credentials-file route,
use the MCP's comment tools directly with the same ADF shape this script produces —
read `scripts/post_signoff.py` for the exact node shapes to replicate rather than
re-deriving them.

## Never

- Never invent a gap to fill the SUCCESs shape. If everything passed, say so plainly
  and skip straight to "Ask" only if there's a real open question — otherwise the
  sign-off just confirms and stops.
- Never post to Jira with an ambiguous name unresolved. A wrong CC is worse than a
  slower post — ask which person, every time a search returns 2+ matches.
- Never invent test data, member IDs, or error text — pull them from what was actually
  pasted or screenshotted.
- Never skip the em-dash scan, and never eyeball it — count the character.
