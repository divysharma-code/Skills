# Test Plan Writer

Most bad test plans are acceptance criteria wearing a numbered list. They confirm the new thing
exists, then stop — and miss everything that was already working.

This writes a test plan as the **end-to-end journey** a real user takes, and checks two things:
the new behaviour works, and the business logic that was already there didn't break.

## What one run gives you

- **Four journeys** instead of a checklist: the new path end to end, the default path that must
  stay untouched, the round-trip through edit and re-open, and a regression pass for whoever
  isn't getting the change.
- **Edge cases chosen by consequence** — records created before the change shipped, whatever got
  removed, missing optional data, stale state after a toggle. The failures that survive normal
  testing rounds.
- **Honest exclusions.** What this plan doesn't cover and why: design QA, backend assertions,
  work split into other tickets. An unrunnable step is worse than an absent one.
- **Questions instead of guesses** — the specific things to ask an engineer about which fields
  and collections a change touches, rather than an invented field name you'd have to defend.

It follows the value past the save. A field that only renders is low stakes; a field that
decides money, routing, or who gets notified is where the journey has to go.

## Use it

Tell Claude: **"Write a test plan for TICKET-1234."** Or paste the change description.

It won't fabricate a test account, and it pauses before writing anything back to your tracker.

## Setup (once)

Nothing required. Optional:

1. **A tracker MCP** (Jira or similar) — to read the ticket and write the plan back. Without it,
   paste the ticket in and copy the plan out.
2. **An architecture or schema source** — to narrow which fields a change touches. Without it,
   those become questions for engineering, which is where they'd end up anyway.

Four things are specific to your team — where test data lives, where architecture is documented,
who owns design QA, and where the plan gets stored. There's a short section at the end of
[PLAYBOOK.md](PLAYBOOK.md) to record them once so each run doesn't rediscover them.

## Where things live

The workflow Claude follows is in [SKILL.md](SKILL.md). The method — journey patterns, edge-case
generators, exclusion buckets, the questions to ask engineering — is in
[PLAYBOOK.md](PLAYBOOK.md).

---

*Original skill by Divy Sharma · MIT License.*
