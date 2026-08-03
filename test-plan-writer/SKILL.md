---
name: test-plan-writer
description: "Write a test plan for a ticket, feature, or change as an end-to-end user journey rather than a checklist of acceptance criteria. Walks the workflow the way a real user would, confirms existing business logic still holds, and puts the effort on the edge cases that survive normal testing — records created before the change, the thing that got removed, missing optional data, stale state after a switch. Generates the questions to ask engineering about which fields and collections a change touches instead of guessing at them. Use when asked to write or review a test plan, a QA plan, UAT steps, a validation plan, or test cases for a ticket; when asked how to test a feature or what could break; or when a test plan reads like restated acceptance criteria and needs rewriting as a journey."
version: 2.0.0
author: Divy Sharma
license: MIT
metadata:
  optional: ["Jira/tracker MCP (to read the ticket and write the plan back)", "an architecture or schema source (to identify affected fields)"]
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

## Quick start

> Write a test plan for PROJ-1234.

Default output is the **house format** — a compact three-section doc, not the labeled framework
below. It still uses the journey thinking and edge-case generators from PLAYBOOK.md to decide
*what* to test; it just renders the result as a ticket-ready doc instead of a labeled block.

**1. Original Test Plan (Draft)** — only if one was already given; otherwise skip straight to
section 3 and fold this into it. One scope line, then the flow as an arrow click-path:

```
[Entry point] ----> [Step] ----> [Step] ----> "New field/dropdown will come" which contains ---> [Options]
```

Add one line of history if relevant ("existed before, got removed, bringing it back").

**2. Meeting Notes**
- *Context* — 3–5 short factual bullets: what the ticket does, what existed before, what changed.
- *Questions asked in this meeting* — the literal questions raised, as a bullet list, including
  any confusion/self-correction moments. Capture them; don't answer them here.

**3. Test Plan**
Repeat the scope line + arrow click-path + history note from section 1, verbatim. One `Setup:`
line — config states, health plans, test data, login persona. A short numbered list (4–6 steps):
one action, one expected result, per line. End with a step that repeats the flow on the
opposite/OFF condition, to confirm nothing else changed.

Plain, casual sentences, numbered lists — not prose. No "Journey A/B/C/D" or "Not Covered" /
"Ask Engineering" headers inside the doc itself; those stay internal to how you picked the steps.

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

1. **Read the change** — the ticket, its parent, comments, and grooming notes. Scope is usually
   narrowed there, and testing something that got split out is wasted work.

2. **Name what changes**, in one sentence, and **who is affected**: which users, clients,
   configurations. If a flag gates it, two populations exist — those who get it and those who
   must not notice.

3. **Find the consequence.** What does this data *do* downstream? A field that only renders is
   low stakes. A field that decides money, routing, eligibility, or who gets notified is where
   the risk lives, and the journey must follow the value that far. Ask before writing a step.

4. **Build the journeys** — patterns in PLAYBOOK. A and B always; C and D when they apply.

5. **Weight the edge cases.** Features rarely fail on the happy path. Use the generators in
   PLAYBOOK. This is where a plan earns its keep.

6. **Draw the lanes.** Test what you are responsible for — the right data is captured, persists,
   flows downstream, and broke nothing. Not colours, not layout. State what the plan does *not*
   cover and why (buckets in PLAYBOOK); an honest exclusion beats a step nobody can run. Render
   the result in the **house format** by default — the full framework only when asked for it.

7. **List what you had to ask** rather than assume — questions for engineering, questions for
   product, at the bottom.

8. **→ Confirm before writing to the tracker.** Draft-only is the default.

## Never

- Never fabricate test data — an account, member, order, or record ID. An invented ID looks
  exactly like a real one and wastes a tester's afternoon. Use a visible placeholder and say
  where the real value comes from.
- Never write a step nobody can execute by clicking. If it needs a DB query or payload
  inspection, mark it an engineering check.
- Never test what the ticket explicitly split out. Cite the ticket that owns it.
- Never assume which fields or collections a change writes. Ask.

## If information is missing

Ask. A plan built on an assumed field name, an assumed config scope, or an invented account
sends someone down a path that cannot be run. Name the blank as an open question.

And read your own plan before handing it over: if someone asks why a step exists, you need the
answer without re-reading it. State the single most likely failure in plain language at the top,
so the point survives skimming.
