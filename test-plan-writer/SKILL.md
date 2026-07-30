---
name: test-plan-writer
description: "Write a test plan for a ticket, feature, or change as an end-to-end user journey rather than a checklist of acceptance criteria. Walks the workflow the way a real user would, confirms existing business logic still holds, and puts the effort on the edge cases that survive normal testing — records created before the change, the thing that got removed, missing optional data, stale state after a switch. Generates the questions to ask engineering about which fields and collections a change touches instead of guessing at them. Use when asked to write or review a test plan, a QA plan, UAT steps, a validation plan, or test cases for a ticket; when asked how to test a feature or what could break; or when a test plan reads like restated acceptance criteria and needs rewriting as a journey."
version: 1.0.0
author: Divy Sharma
license: MIT
metadata:
  optional: ["Jira/tracker MCP (to read the ticket and write the plan back)", "an architecture or schema source (to identify affected fields)"]
---

# Test Plan Writer

Most bad test plans are acceptance criteria wearing a numbered list. They confirm the new
thing exists, then stop. What they miss is everything that was already working.

A test plan walks the **end-to-end journey** a real user takes, and confirms two things: the
new behaviour works, and **the business logic that was already there did not break**.

Full method: **[PLAYBOOK.md](PLAYBOOK.md)**.

## The distinction that drives everything

| | Answers |
|---|---|
| **Acceptance criteria** | What should this feature do? *(a required field throws a red error)* |
| **Test plan** | Does the whole workflow still hold, end to end, with this change in it? |

If your plan has one section per AC bullet, you have written acceptance criteria in a
different font. Restructure it as journeys.

## Workflow

1. **Read the change.** The ticket, plus its parent, its comments, and any grooming notes —
   scope is usually narrowed there, and testing something that got split out is wasted work.

2. **Name what actually changes**, in one sentence, and **who is affected**: which users,
   which clients, which configurations. If a flag or config gates it, then two populations
   exist — the ones who get the change and the ones who must not notice it.

3. **Find the consequence.** What does this data *do* downstream? A field that only renders is
   low stakes. A field that decides money, routing, eligibility, or who gets notified is where
   the real risk lives, and the journey must follow the value that far. Ask this before writing
   a single step.

4. **Build the journeys** (patterns in PLAYBOOK): the new path end to end · the default path
   that must stay untouched · the round-trip through edit and re-open · the regression for
   everyone not receiving the change.

5. **Weight the edge cases.** Features rarely fail on the happy path. Use the edge-case
   generators in PLAYBOOK — pre-existing records, the removed thing, missing optional data,
   stale state after a switch. This is where a plan earns its keep.

6. **Draw the lanes.** State plainly what this plan does *not* cover and why — design QA,
   backend-only assertions, work split into other tickets. An honest exclusion beats a step
   nobody can actually run.

7. **List what you had to ask rather than assume.** Unresolved inputs go at the bottom as
   questions for engineering and questions for product. Do not paper over them.

8. **→ Confirm before writing to the tracker.** Draft-only is the default.

## The lane rule

Test what you are responsible for. Typically:

- **Yours (functional):** the right data is captured, it persists, it flows correctly
  downstream, and nothing that used to work stopped working.
- **Not yours (design QA):** colours, layout, spacing, whether a control looks right.
- **Not clickable (backend):** field writes, payload shape, collection updates. These become
  *questions for engineering*, not fabricated UI steps.

Spending steps outside your lane pads the plan and hides the thin coverage inside it.

## Never

- Never fabricate test data — an account, member, order, or record ID. An invented ID looks
  exactly like a real one and wastes a tester's afternoon. Write a visible placeholder and say
  where the real value comes from.
- Never write a step nobody can execute by clicking. If it needs a DB query or a payload
  inspection, mark it as an engineering check.
- Never test what the ticket explicitly split out. Cite the ticket that owns it instead.
- Never assume which fields or collections a change writes. Ask.

## If information is missing

Ask. A test plan built on an assumed field name, an assumed config scope, or an invented
account sends someone down a path that cannot be run. Name the blank as an open question and
let the person who knows fill it.

And read your own plan before you hand it over: if a stakeholder asks why a step exists, you
need the answer without re-reading it. State the single most likely failure in plain language
at the top so the point survives skimming.
