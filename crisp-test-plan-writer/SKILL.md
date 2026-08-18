---
name: crisp-test-plan-writer
description: "Turn a Jira ticket (or linked pair/set of tickets) into a test plan fast: read the ticket + parent + full comment history, find the PRs that actually shipped it and read their diffs (not just descriptions), resolve test data live against the source-of-truth sheet, and render steps as one flat S.No | Action | Expected Result table. Use when asked for a quick test plan, PO-review steps, or UAT steps for a specific ticket and there isn't time for the full journey/edge-case/scoring workflow — the diff-mining and live data lookup are what make this fast without making it wrong. For deeper coverage (journeys, edge-case generators, adversarial scoring, migrations), use test-plan-writer instead."
version: 1.0.0
author: Divy Sharma
license: MIT
metadata:
  requires: ["Atlassian/Jira MCP", "gh CLI authenticated to the CohereHealth GitHub org", "Google Workspace MCP (test-data worksheet + Sheets)"]
---

# Crisp Test Plan Writer

The fast path from "here's a ticket" to a test plan someone can run today. Four steps, in order.
Skipping the order is how you end up writing acceptance criteria in a different font, or inventing
test data that looks real and isn't.

**Not the deep-coverage tool.** No journeys, no edge-case generator library, no scoring pass —
that's `test-plan-writer`. This skill exists because most PO-review requests don't need that;
they need the real behavior confirmed against real data, fast.

## The four steps

### 1. Get the real context, not the ticket alone

Pull the ticket **and its parent epic and every comment**, not just the description —
`getJiraIssue` with `fields: [..., "comment"]`, and follow the `parent` link if one exists.

Comments are where the scope actually narrows (a field standardizes on one name over another),
where blockers and bounces show up (Design QA rejected it once, here's why), and where EOD-status
notes tell you what's *actually* shipped vs. still moving — which is not always what the ticket's
`status` field says days later.

If two or more tickets are linked, say in one sentence how — which one's data feeds the other's
UI. State it before any step, don't leave the reader to infer it.

### 2. Mine the diff, not the description

```bash
gh search prs "<TICKET-KEY>" --owner CohereHealth --json number,title,repository,state,url
gh pr diff <number> --repo CohereHealth/<repo>
```

Search every repo that plausibly touched this (frontend *and* core-platform, at minimum), and read
the actual diff of the file holding the new logic — not just the PR description, which is a plan,
not what shipped. This is the highest-return step in the whole recipe. It gets you three things a
ticket alone won't:

- **Bugs already caught and fixed.** A "bandaid fix" or "changing apply location" follow-up PR is
  the dev's own regression test — turn it into your step. If it fixed a value getting lost across a
  reload, your plan needs an explicit save-then-reopen step; don't assume it, go read why the fix
  was needed.
- **Scope past the ticket's stated surfaces.** If the diff touches five files the AC never
  mentioned (a Referral flow, a second card component), that's real, shipped scope — note it as an
  open question about whether it's in scope for *this* release, don't silently add or drop it.
- **The tie-break when the ticket contradicts itself.** Ticket text quoting two different render
  orders for the same field is common when grooming notes and the final AC drift apart — the diff
  is what's live; test that, and flag the ticket text as stale.

### 3. Resolve test data live — never carry it over

Same rule as `test-plan-writer` §9, applied every time, including when the user asks for test data
as a separate follow-up message after the plan is already written:

- Look it up in the real worksheet with a **targeted formula** (`COUNTIF` for a sanity count, then
  `SEARCH`/`MATCH` for the row), not a bulk read of the whole tab — big sheets truncate, and a
  truncated read looks complete.
- Do this in a scratch tab if the sheet is too wide for a plain formula to fit next to the data;
  **clear the scratch tab's contents when you're done** and say so, rather than leaving formulas
  sitting in a shared source-of-truth sheet. Deleting the tab itself is the user's call.
- Confirm the plan/tenant name you were given actually exists in the sheet before writing it down —
  names from tickets, calls, or your own memory of a past session are often subtly wrong.
- If a follow-up asks for *more* test data (a second tenant for a regression check, a different
  segment), re-run the lookup live rather than reusing what a past session cached — the sheet moves.
- If a specific piece genuinely isn't in the sheet (e.g. a null/negative-case value that only lives
  in the application's own config or database), say plainly that it's out of reach from here and
  name who to ask. Don't approximate it.

### 4. Render the fixed shape

```
Test Plan
Assigned to - [name, or a visible placeholder if unknown]
Tickets - [ticket key(s)]

Problem: (one-line summary)

What is [X]? — or "What is [X] and [Y]?" for two or more linked tickets
[Ticket A] — [label]
Before: ...
Now: ...
What changed: ...
What didn't change: ...
Why test: ...
[repeat per linked ticket]

How they connect (2+ tickets only)
[A] → [what happened testing it] → [why B exists]

Setup: config/flag state, health plan, test member + provider data (from step 3), fax/edge
routing notes. Say which pieces run today vs. need eng/PO help to unblock.

Most likely failure: (one line, plain language — the thing most likely to actually break)

Steps to test tickets

S.No | Action | Expected Result
Setup | [confirm config/flag/data are in place] | [what breaks if this isn't true, and which
     later steps that invalidates]
1 | [one action] | [one visible result — quote the on-screen text if there is any]
2 | ...
...
[end with a step that repeats the flow on the opposite/OFF condition]

Open questions
1. [grounded in something specific you found — not a hedge — addressed to a named person]

Reference
[ticket keys · PR numbers · flag/config/field names · docs — one line, at the bottom, never above]
```

Same non-negotiables as `test-plan-writer`: **zero coding language above the Reference line** —
no field, config, status, class, PR, or branch names in the table body, ever; every expected
result names something visible on screen, quoting the actual message text where one exists; a
step nobody can execute by clicking is an engineering check, not a step.

## Never

- Never fabricate test data, or approximate a real ID/member/NPI you couldn't find.
- Never write a plan/tenant name you haven't confirmed exists in the sheet.
- Never skip the diff and write steps from the ticket's ACs alone — the diff is what ships.
- Never ask a question the diff already answered.
- Never put a field name, PR number, or status code inside a step — Reference footer only.
- Never leave scratch formulas live in a shared source-of-truth sheet after you've read the result.
