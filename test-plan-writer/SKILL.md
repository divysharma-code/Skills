---
name: test-plan-writer
description: "Write a test plan for a ticket, feature, or change as an end-to-end user journey rather than a checklist of acceptance criteria. Walks the workflow the way a real user would, confirms existing business logic still holds, and puts the effort on the edge cases that survive normal testing — records created before the change, the thing that got removed, missing optional data, stale state after a switch. Generates the questions to ask engineering about which fields and collections a change touches instead of guessing at them. Use when asked to write or review a test plan, a QA plan, UAT steps, a validation plan, or test cases for a ticket; when asked how to test a feature or what could break; or when a test plan reads like restated acceptance criteria and needs rewriting as a journey."
version: 3.3.0
author: Divy Sharma
license: MIT
metadata:
  optional: ["Jira/tracker MCP (to read the ticket and write the plan back)", "an architecture or schema source (to identify affected fields)"]
---

## Changelog

| Version | Date | Changes |
|---|---|---|
| **v3.3.0** | **2026-08-05** | **Test data is a first-class step, not a placeholder.** New Workflow step 7 (*Resolve the test data before writing setup*) and PLAYBOOK §9 *Sourcing test data*: name the tab not just the workbook, look up by keyword with formulas rather than bulk reads (large sheets truncate, and a truncated read looks complete), prefer a pre-bundled identifier column, `COUNTIF` before taking the first match, and match the sub-dimension the gate actually reads. Adds the alias check (verify a tenant name against the sheet's distinct list before writing it into a plan — names from call transcripts are often wrong), the "no test member for X ages badly" rule, the distinction between *no member* and *tenant not configurable in this environment*, five test-data traps, and a clean-up-your-scratch-work rule for shared source-of-truth sheets. Source: three PO-review plans where the call's health plan ("Avira") did not exist in the worksheet at all, a documented "no HMSA test member" blocker turned out to be stale with five members available, and the only listed member for one tenant was the wrong line of business for the rule being tested. |
| **v3.2.0** | **2026-08-04** | **Written for the person clicking, and grounded in the diff.** Two additions. (1) **No coding language in the plan body** — field names, status codes, hook names, repo and PR numbers, and language trivia go in a Reference footer, never in a step. Every step now answers *where to go / what to do / how it should look*, rendered as a table once there's more than one setup phase. (2) **Read the shipped diff before writing steps** — new Workflow step 6 plus PLAYBOOK §7 *Mining the diff*. On the ticket that prompted this, the diff answered five of eight questions that had been queued for humans, and produced the highest-value step in the plan (a bug the devs hit and fixed). Added five edge-case generators (the deleted key, the loading race, the deliberately-unchanged sibling, the pre-validator record, case-insensitive vs typo-tolerant), three assumption traps (ACs contradicting shipped code, a ticket's example values treated as real, a test account that cannot match the gate), and the false-pass check. Source: a group-based access-control plan where the ticket's own acceptance criteria contradicted the merged code, and a draft config carried a one-character typo in exactly the field the feature fails silently on. |
| v3.1.0 | 2026-08-04 | **One default shape, not two.** Collapsed the old 3-section house format (Original Draft / Meeting Notes / Test Plan) and the migration-only variant into a single default template used every time, regardless of ticket count: `Test Plan` / `Assigned to` / `Tickets` / `Problem:` one-liner / `What is [X]?` (or `[X] and [Y]?` for linked tickets) / `Setup:` / `Steps to test tickets` / `Open questions`. If a draft was already given, it's folded silently into "What is X?" and "Steps" — it no longer gets reproduced as its own section. `Before:`/`Now:`/`What changed:`/`Why test:` lines and the arrow-chain ticket linkage are now the default explainer shape for every plan, not an opt-in for migrations only. Source: Divy asking for the same structure on a single-ticket plan that had been used for a 3-ticket migration plan — the two formats were an unrequested distinction the skill invented, not something he asked for. |
| v3.0.0 | 2026-08-04 | **Context-first check + scoring.** Added a context-first pass before building journeys: read full context (not just a summary), name what changed in three lines (before/now/unchanged), state how linked tickets connect, and check the described test approach against real architecture/ownership/flag docs before trusting it. Added a migration/linked-ticket house-format variant (`Before:`/`Now:`/`What changed:`/`Why test:` lines + arrow-chain ticket linkage). Added a scoring pass (Context Clarity, Assumption-Checking, Coverage, Question Sharpness) with the rule that a misapplied catch doesn't count. Added the Common Assumption Traps library + self-update loop to PLAYBOOK.md. Source: an Okta→Cognito notification-migration test plan spanning three linked tickets, where an initial "assumption check" turned out to apply a risk from the wrong user population — caught, corrected, and turned into a reusable trap instead of a one-off fix. |
| v2.0.0 | 2026-08-03 | Default to a compact house-format doc instead of the labeled framework. |
| v1.0.0 | 2026-07-30 | Initial skill. |

---

# Test Plan Writer

Most bad test plans are acceptance criteria wearing a numbered list. They confirm the new thing
exists, then stop. What they miss is everything that was already working.

A test plan walks the **end-to-end journey** a real user takes, and confirms two things: the new
behaviour works, and **the business logic that was already there did not break**.

Full method: **[PLAYBOOK.md](PLAYBOOK.md)**.

## The distinction that drives everything

| | Answers |
|---|---|
| **Acceptance criteria** | What should this feature do? *(a required field throws a red error)* |
| **Test plan** | Does the whole workflow still hold, end to end, with this change in it? |

If your plan has one section per AC bullet, you have written acceptance criteria in a different
font. Restructure it as journeys.

## Write it for the person clicking

The plan is read by someone with the product open, not by the person who wrote the code. Every
sentence has to survive that reader. **No coding language in the plan body** — that means no
field or column names, no HTTP status codes, no hook, class, repo, branch or PR names, no
language trivia ("empty arrays are falsy"), no file paths.

Those facts still matter — put them in a one-line **Reference** footer at the bottom, where
someone chasing provenance can find them and a tester can ignore them.

| Don't write | Write |
|---|---|
| "`teamOverrides` is a nullable `String`, max 255, no enum" | "you type the team name in by hand, so a typo saves fine and quietly matches nobody" |
| "returns `422 UNPROCESSABLE_ENTITY`" | "red toast: *Couldn't save — these two settings can't both be on*" — quote the text the tester will actually see |
| "evaluated in `useAccessConfigState`" | "on the details step, as the page loads" |
| "backend PR merged to `develop`, frontend still open" | "the config half is already in, the screen half isn't yet" |

Two tests for a finished plan: could a new joiner run it without opening the ticket, and does
every expected result describe something **visible on screen**? If a step's expected result is a
status code or a database state, it is an engineering check — label it as one or cut it.

## Quick start

> Write a test plan for PROJ-1234.

One default shape, every time — a single ticket or several, a plain feature or a migration.
Keep the explainer lines as lines, not prose; this is the one place bullet-dash formatting is
dropped on purpose. It still uses the journey thinking and edge-case generators from PLAYBOOK.md
to decide *what* to test — this just renders the result as a ticket-ready doc:

```
Test Plan
Assigned to - [name, or a visible placeholder if unknown — never invent one]
Tickets - [ticket key(s)]

Problem: (one-line summary of what's being changed)

What is [X]? — or "What is [X] and [Y]?" when two or more tickets are linked

[Ticket A] — [short label; omit the label entirely when there's only one ticket]
Before: what it used to do
Now: what it does instead
What changed: the one thing that's actually different
What didn't change: everything else — say it explicitly
Why test: the reason this needs checking at all

[Ticket B] — [short label] (repeat the five lines above per linked ticket)

How they connect (only when 2+ tickets are linked)
[Ticket A] → [what happened while testing it] → [why Ticket B exists]
So testing A end-to-end also proves B works. One test plan, N tickets.

Setup: config states, health plans, test data, login persona.
Include the click path to anything the tester has to configure, and a paste-ready block for
any config they must apply. If different steps run at different times, say which run now.

Steps to test tickets
Every step answers three things: WHERE to go · WHAT to do · HOW IT SHOULD LOOK.
"Verify it works" is not an expected result. Name what appears on screen, and quote the
message text where there is one.

1. one action, one visible result, per line
...
End with a step that repeats the flow on the opposite/OFF condition, to confirm nothing else changed.

Open questions
1. anything still unresolved after Workflow steps 5–7 — sharp and grounded, one per line.

Reference
ticket keys · config and field names · PRs · docs — one line, at the very bottom.
```

**Render the steps as a table** (`# | Where to go | What to do | How it should look`) once the
plan has more than one setup phase or more than about six steps, and group the rows into named
parts — config side, the allowed path, the blocked path, edge cases, regression. Same three
things either way; the table just stops the "where" and the "should look" from collapsing into
one sentence. A short plan stays a numbered list.

Where a failure would actually belong to a different ticket, say so in the expected result
itself — a tester who files it in the wrong place loses a day to the bounce.

If Divy hands you his own draft first, don't reproduce it as a separate "original draft" section
— fold it straight into "What is X?" and "Steps to test," the same as if you'd derived it
yourself from a ticket or a call. The draft is input, not part of the output shape.

No "Journey A/B/C/D" or "Not Covered" / "Ask Engineering" headers inside the doc itself — those
stay internal to how you picked the steps, and surface only as the plain numbered list and the
Open Questions section above.

### Full framework (opt-in)

Use this labeled shape instead when asked for the fuller breakdown — grooming a large or risky
change, or explicitly asked for "journeys," "edge cases," or "what's not covered":

```
Most likely failure: requests created before the checkbox was removed.

SETUP             flag state · account or record to use (placeholder if unknown)

JOURNEY A         the new path, end to end — start at login, follow the value past the save
JOURNEY B         the default path, untouched — the same flow without the new behaviour
JOURNEY C         the round-trip — save, leave, return, edit, and every other surface
JOURNEY D         regression for the ungated population — only if a flag or config gates it

EDGE CASES        chosen by consequence, not by count
NOT COVERED       design QA · backend assertions · work split to other tickets
ASK ENGINEERING   which fields and collections this actually writes
ASK PRODUCT       unresolved scope, unnamed config values, missing test data
```

Nothing is written back to the tracker until you say so.

## Workflow

1. **Get the full context, not the summary.** Read the ticket, its parent, comments, and
   grooming notes — and if there's a call or thread behind it, read that too, not just a
   recap. Scope is usually narrowed there, and summaries drop the exact words that reveal how
   something actually works.

2. **Name what changed, in three lines**: what it used to do, what it does now, and what stayed
   exactly the same. If you can't fill in all three, you don't understand the change yet — find
   out before writing anything else.

3. **If more than one ticket is linked, say how in 1–2 sentences** before any steps. Don't assume
   the reader already knows why they're connected — "testing A also proves B" is worth stating
   outright, not implying.

4. **Name who is affected**: which users, clients, configurations. If a flag gates it, two
   populations exist — those who get it and those who must not notice.

5. **Check the described test approach against real docs before trusting it** — architecture
   notes, ownership docs, feature-flag references, past design reviews, anything beyond the
   ticket itself. Specifically: is there a flag gating this, and is it on where you're testing?
   Does the owning team match who's assigned? Does the test setup exercise the real mechanism,
   or something that happens to produce the same result? Read PLAYBOOK's *Common Assumption
   Traps* before turning anything you find into a flagged gap — a wrong catch is worse than no
   catch.

6. **Read the code that shipped, not just the ticket.** Find the PR — its description, its
   changed-file list, and the diff of the file holding the new logic. This is the single highest
   return step in the workflow and it belongs *before* you write any step, because the ticket is
   a plan and the diff is what exists. It tells you: which surfaces changed that nobody
   mentioned; what the devs already hit and fixed (their bug is your best test case); how edge
   cases actually resolve; and which branch is still unmerged, so you know what can be tested
   today. Details in PLAYBOOK §7. **Where the acceptance criteria and the merged code disagree,
   the code is what ships** — test the code and raise the AC as a defect in the ticket, don't
   write a step that asserts the AC.

7. **Resolve the test data before writing setup.** Look it up in the authoritative sheet or
   fixture set, name the tab, and match the sub-dimension the feature actually gates on — right
   tenant but wrong line of business is the most common false pass in this whole method. Verify the
   tenant name really exists there before writing it down; names from calls and memory are often
   subtly wrong. If a prior doc says "there is no test member for X", re-check rather than repeat
   it. Method and traps in PLAYBOOK §9.

8. **Find the consequence.** What does this data *do* downstream? A field that only renders is
   low stakes. A field that decides money, routing, eligibility, or who gets notified is where
   the risk lives, and the journey must follow the value that far. Ask before writing a step.

9. **Build the journeys** — patterns in PLAYBOOK. A and B always; C and D when they apply.

10. **Weight the edge cases.** Features rarely fail on the happy path. Use the generators in
   PLAYBOOK. This is where a plan earns its keep.

11. **Ask whether the plan can pass for the wrong reason.** If the tester's account, client, or
    config can't actually match the thing being gated, the "on" and "off" paths look identical
    and a dead feature reads as a pass. Name that risk in one line at the top of the plan and
    put confirming it in the setup, ahead of step one. Then search the tracker for open bugs on
    the same screen — an in-flight bug that breaks the expected result of your negative test
    will be filed against your ticket unless the plan says whose it is.

12. **Draw the lanes.** Test what you are responsible for — the right data is captured, persists,
   flows downstream, and broke nothing. Not colours, not layout. State what the plan does *not*
   cover and why (buckets in PLAYBOOK); an honest exclusion beats a step nobody can run. Render
   the result in the **house format** by default — the full framework only when asked for it.

13. **List what you had to ask** rather than assume — questions for engineering, questions for
    product, at the bottom. Anything still unresolved after steps 5–7 belongs here as a direct
    question, not a guess folded quietly into a step. Address each one to a **named person**, and
    delete the ones the diff already answered rather than asking a human to re-confirm code.

14. **Score the plan before handing it over** — for yourself, in the chat. The score is working
    output, not part of the document; never paste it into the plan the tester reads. Four
    dimensions, 1–10 each, one line of reasoning:
    - *Context Clarity* — could someone who missed the background follow the top section in one read?
    - *Assumption-Checking* — did you verify the approach against real docs, or just restate what you were told?
    - *Coverage* — does it include the real untested combination, or just the happy path someone already ran?
    - *Question Sharpness* — is every open question grounded in something specific you found, or a hedge dressed as diligence?

    A question that targets the wrong population, the wrong ticket, or an outdated doc does not
    count as a real catch under Assumption-Checking — say so instead of keeping the score.

15. **→ Confirm before writing to the tracker.** Draft-only is the default. If the plan is going
    into a Google Doc, markdown must be uploaded as markdown for the tables to convert — a
    plain-text insert turns every table into pipe soup. That replaces the file's contents, so
    fold anything worth keeping from the old version into the upload and say what you did.

## Never

- Never fabricate test data — an account, member, order, or record ID. An invented ID looks
  exactly like a real one and wastes a tester's afternoon. Use a visible placeholder and say
  where the real value comes from.
- **Never write a tenant or plan name into a plan without checking it exists in the test-data
  source.** A name carried over from a call, a thread, or memory is often subtly wrong, and the
  tester discovers it only after the lookup returns nothing. Search the distinct list first, and if
  the name is absent, say what you searched and what the real list holds rather than silently
  substituting the nearest match.
- **Never repeat a "there is no test data for X" claim without re-checking it.** Sheets get
  backfilled; stale blockers keep people stuck. If it now exists, say so explicitly.
- Never write a step nobody can execute by clicking. If it needs a DB query or payload
  inspection, mark it an engineering check.
- Never test what the ticket explicitly split out. Cite the ticket that owns it.
- Never assume which fields or collections a change writes. Read the diff, then ask.
- **Never treat a ticket's example values as real values.** Config samples in a ticket are
  illustrative and are often subtly wrong — a missing underscore, a made-up group name. Find the
  real list in a docs repo or from the person who owns provisioning, and say which source it came
  from. Copying an example value into a setup block invents test data just as surely as inventing
  an account ID.
- **Never ask a human a question the diff already answers.** Every open question you can close by
  reading code is one you're asking someone to re-confirm from memory, and it dilutes the ones
  that genuinely need them.
- Never put a field name, status code, or class name inside a step. Reference footer.

## If information is missing

Ask. A plan built on an assumed field name, an assumed config scope, or an invented account
sends someone down a path that cannot be run. Name the blank as an open question.

And read your own plan before handing it over: if someone asks why a step exists, you need the
answer without re-reading it. State the single most likely failure in plain language at the top,
so the point survives skimming.
