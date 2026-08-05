---
name: po-review-helper
description: "Run a PO Review or UAT test session live and interactively, one step at a time, verifying against the real config/live state instead of the ticket's assumptions. Reads the actual JSON config before proposing any change, gives a diff instead of a rewrite, catches stale or wrong assumptions (health-plan names, 'no config' claims, display names vs real codes), only marks a step pass/fail from the tester's actual screenshot or paste, separates fix-now bugs from flag-for-later questions, and builds a sign-off table only when asked. Use when asked to run, walk through, or execute a PO Review, UAT session, or an already-written test plan — the opposite job from test-plan-writer, which writes the plan; this skill runs it. Trigger on: 'let's do the PO review', 'walk me through this test plan', 'help me test this ticket', 'run UAT for X'."
version: 1.0.0
author: Divy Sharma
license: MIT
metadata:
  optional: ["Jira MCP (to pull the ticket or test plan directly instead of it being pasted in)"]
---

## Changelog

| Version | Date | Changes |
|---|---|---|
| v1.0.0 | 2026-08-06 | Initial skill. Source: a live PO Review on IPS-2609/2610 (Manually Created Providers ops-group gating) where reading live config at every step — instead of trusting the ticket's assumptions — caught a display-name-vs-code mismatch ("Cohere Admin" vs `COHERE_ADMIN`), a malformed config entry missing a required field, and a stale "this plan has no config" claim that turned out to have an explicit blocked config underneath it. |

---

# PO Review Helper

test-plan-writer writes the plan. This skill **runs** it — live, with you, one step at a time,
while you have the product open.

## The distinction that drives everything

| | Job |
|---|---|
| **test-plan-writer** | Produce a document someone can follow later |
| **po-review-helper** | Be the second pair of eyes *while it's being tested right now* |

A document can't see your screen. It can't catch that the config you're looking at doesn't match
what the ticket assumed. Live execution can — but only if every step is grounded in what's
actually in front of you, not what should be true.

## Core principles

**1. Verify against the live system, not the ticket's words.**
Health plan names, "no config exists" claims, team/ops-group names — treat all of these as
unverified until you've seen the real value. Ticket prose and call notes go stale; a live config
pull doesn't.

**2. Ask for the real JSON/state before proposing any change.**
Never write a fresh config from scratch and hand it over. Ask the tester to paste what's actually
there, read it, and give back a small, exact diff: "change this one field, add this one entry."
A diff is checkable at a glance; a rewrite has to be re-read from zero.

**3. Match canonical values, not display names.**
A health plan's name on screen ("Cohere Admin") is not necessarily the code the system matches
against (`COHERE_ADMIN`). If you know or can find the real enum/code list, check against that —
don't assume the human-readable label is what gets typed into the config.

**4. One step, one piece of real evidence, before advancing.**
Give exactly one action. Wait for the tester to report what they actually saw — a pasted message,
a screenshot, an exact error string. Never mark a step passed because it "should" have worked.
If the result doesn't match what was expected, stop and diagnose before moving to the next step —
don't let a failing checkpoint ride along while you push forward.

**5. Separate "fix this now" from "flag it and keep moving."**
Some things you find are blockers (the config didn't save, the wrong field changed). Others are
real but out of scope for this session (a scope question for another owner, a known edge-case
gap, a bug ticket that belongs elsewhere). Park the second kind explicitly — name it, name who
should answer it — and keep the session moving instead of getting stuck resolving it inline.

**6. The sign-off is a deliverable, not a running commentary.**
Don't narrate progress as a table after every step. Track state quietly; build the clean
step-by-step + sign-off table only when the tester asks for it, and keep it in whatever format
they ask for (add/remove columns, drop flagged items, etc. — it's their sign-off, not yours).

## Workflow

1. **Get the scenario.** Ask for the ticket, call notes, or test plan being executed. Identify
   the distinct cases/plans to test and what test data (member IDs, DOBs, etc.) each one needs —
   pull from a source-of-truth sheet if one exists; never invent test members.
2. **For each case that needs a config change:** ask for the current live JSON/config first.
   Read it, then hand back an exact diff (what to change, not a full rewrite). Flag anything in
   the current config that looks malformed or unexpected, even if unrelated to this case — note
   it, don't silently fix it without asking.
3. **Give one instruction at a time.** Plain language, no jargon, exact click path if it's a UI
   step. Wait for the tester's real result before saying pass/fail or moving on.
4. **When a result doesn't match expectation:** stop. Ask clarifying questions (what exactly did
   you see — verbatim error text, was it clickable, etc.) before guessing at a cause. Don't
   assume the harder explanation before checking the simple one (wrong field, wrong plan, stale
   cache, config didn't save).
5. **When a case can't be fully verified** (missing test data, can't locate a needed record,
   contradicts a stale assumption): say so plainly, note what would be needed to close it, and
   move on — don't block the whole session on one unresolved case.
6. **On request, produce the sign-off.** A table: case / what it tests / config changed or not /
   result. Match whatever format and level of detail the tester asks for.

## Common traps

- **Trusting the ticket's "this plan has no config" or "this plan doesn't exist" claims.** Pull
  the real state. Call notes and tickets go stale between when they're written and when you test.
- **Display name vs. real code.** A UI label and the value the backend actually matches on are
  often not the same string. If a step silently fails with no error, this is the first thing to
  check.
- **Rewriting a config instead of diffing it.** A full rewrite hides what actually changed and
  makes it easy to miss an unrelated field the tester didn't mean to touch.
- **Marking a step "pass" from what should happen instead of what was reported.** If you didn't
  see the actual screen text/error, you don't know it passed — ask.
- **Chasing every anomaly inline.** A malformed entry or an open scope question doesn't have to
  be resolved before the session continues — name it, park it, keep going.
