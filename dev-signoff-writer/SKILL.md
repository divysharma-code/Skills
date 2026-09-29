---
name: dev-signoff-writer
description: Write a Dev sign-off from raw manual-test notes (steps taken, test data, network calls, a screenshot annotation) and post it as a Jira comment with CC mentions. Finds the one thing worth flagging using the SUCCESs framework (Made to Stick), writes it in plain ELI5 language with every acronym spelled out on first use, tightens it with the-humanizer (zero em dashes, no filler), and renders any step-by-step testing as a flat S.No | Action | Expected Result table (crisp-test-plan-writer's shape). Use when Divy pastes test notes and asks for a "Dev sign-off," a "sign-off comment," or to write up manual testing/validation results for a ticket, especially when a screenshot has a handwritten annotation calling out an edge case the happy-path steps missed.
---

# Dev Sign-Off Writer

Composes three skills Divy already has, in a fixed order, for one recurring output: a
short Jira comment that says "this works, except for this one real case, and here's
the decision someone needs to make." Never write this from scratch — always run the
pipeline below.

## The four steps, in order

### 1. Find the one thing worth flagging (SUCCESs)

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

### 2. Write it ELI5 — ban acronyms and jargon

Every acronym gets spelled out in plain words the first time it appears, in the sentence
itself, not a footnote. `TTL` becomes "the 60-day cool-down" (the actual number, not the
concept-name). `NICU` becomes "any hospital admitting a newborn," not "Neonatal Intensive
Care Unit" — spelling out the acronym is still jargon; say what it means in practice.

Rule of thumb: if a smart friend outside engineering would have to ask what a word
means, replace the word with the thing it refers to.

### 3. Tighten with the-humanizer

Run the drafted text through the-humanizer's universal phrase-level and structural
checks (load that skill directly — don't skip it or approximate its rules from memory).
Non-negotiable for this output:

- **Zero em dashes.** Scan the final text character-by-character for `—` before posting
  — a single read-through misses them (see the em-dash lesson already in
  the-humanizer's own changelog). Confirm the count is 0, don't eyeball it.
- Cut filler openers, hedge phrases, and "it is / does not" contraction-free register —
  write like you'd say it out loud.
- Contractions where a person would use them ("doesn't," "isn't," "won't").
- No stacked fragments, no grandiose closers, no honesty-disclaimer phrases ("stated
  bluntly," "I'll be honest").

Cut words. Don't cut substance — every finding and every open question from step 1
survives, just said in fewer words.

### 4. Render steps as a flat table

If the raw notes include a numbered procedure (click-path + expected result), render it
in crisp-test-plan-writer's fixed shape — a single flat table, no journeys, no named
parts:

```
| S.No | Action | Expected Result |
|---|---|---|
| 1 | ... | ... |
```

Setup/test-data goes in its own small table above the steps table if there's a
health-plan/member-ID/config matrix worth naming — same convention as a crisp test
plan's Setup row, just split out since a sign-off usually has fixed reference data
rather than a single setup step.

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
account IDs by re-deriving the mention structure each time — that's exactly the kind
of deterministic, repeatable operation `write-a-skill` says belongs in a script. Use
`scripts/post_signoff.py`:

```bash
# Resolve names to account IDs first if any are ambiguous or unconfirmed
python3 scripts/post_signoff.py resolve "vidhi" "jeremy" "lakshman"

# Post a new comment (reads the sign-off body from a local markdown file)
python3 scripts/post_signoff.py post ICS-25 signoff.md --cc "Vidhi Kakani,Jeremy Wdowik,lakshmankishore.k"

# Update an existing comment in place instead of posting a new one
python3 scripts/post_signoff.py post ICS-25 signoff.md --cc "..." --comment-id 604812
```

The script:
- Reads `~/.config/jira/credentials.env` for auth (same convention as `cohere-bug-triage`).
- Converts the markdown body (headings, bold, tables, blockquotes) to ADF — including
  real ADF tables, not pipe-text that renders as a wall of text in Jira.
- Resolves each CC name via `user/search`. **If a name search returns more than one
  match** (this happened with "Jeremy" — Jeremy Jones and Jeremy Wdowik both exist),
  the script prints all matches and refuses to guess. Confirm with the user which one,
  then pass the exact `displayName` or `accountId`.
- Emits real Jira `mention` nodes so CC'd people actually get notified — not plain
  `@Name` text, which is inert.

If the Atlassian MCP is connected instead of the `gh`/curl + credentials-file route,
use the MCP's comment tools directly with the same ADF shape this script produces —
don't duplicate the mention-resolution logic by hand in that path either; read
`scripts/post_signoff.py` for the exact node shapes to replicate.

## Never

- Never invent a gap to fill the SUCCESs shape. If everything passed, say so plainly
  and skip straight to "Ask" only if there's a real open question — otherwise the
  sign-off just confirms and stops.
- Never post to Jira with an ambiguous name unresolved. A wrong CC is worse than a
  slower post — ask which person, every time a search returns 2+ matches.
- Never invent test data, member IDs, or error text — pull them from what was actually
  pasted or screenshotted.
- Never skip the em-dash scan. This is the single most-missed step across every prior
  run of this pipeline.
