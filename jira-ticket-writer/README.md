# Jira Ticket Writer

Turns an initiative into refinement-ready COH Stories. A good ticket isn't a filled-in template —
it's the output of an argument between a PM, a designer, an engineer, and QA about approach, edge
cases, and what could go wrong. That argument is the part nobody has time to schedule. This runs
it and hands you the result.

## What one run gives you

First, a **decomposition map** — the candidate stories named the way the house does
(`2c - Search FE: Select a billable family…`), each tagged with who actually owns it. It stops
there and asks which ones you want, because a wrong split turns into twenty beautifully written
wrong stories.

Then, for each story you pick:

- A description in the real COH format — prose intro, `## Change` / `## Behavior`, dependencies,
  design link. No "As a user, I want…", because no COH story reads that way.
- **Acceptance criteria** built from a best-case / worst-case round, phrased as observable system
  behaviour.
- A **test plan** for the Test Plan field — a numbered UAT click-path, not a test strategy.
- Open questions for anything the evidence didn't cover, instead of a confident guess.
- A confidence mark: 🟢 verified against ralf · 🟡 details are BRD-sourced · 🔴 ungrounded.

It also tells you when work **isn't Intake's to build** — only 1 of the 9 visible submission steps
is, so this comes up more than you'd think.

## Use it

Tell Claude: **"Write the tickets for COH-8248."** Or paste an initiative brief if the epic is
empty (many are).

It pauses twice — once at the decomposition map, once before anything is written to Jira.
Draft-only is the default.

## Setup (once)

Nothing required. Both dependencies are optional and it degrades honestly without them:

1. **Atlassian MCP** — to read the epic and create the stories. Without it, paste the initiative
   in and copy the output out.
2. **`gh` CLI with `CohereHealth/ralf` access** — grounds the technical approach and the ownership
   routing in the real intake architecture. Without it, technical claims get marked 🔴 ungrounded
   rather than invented.

## Where things live

The workflow Claude follows is in [SKILL.md](SKILL.md). The substance — the panel rounds, the two
story registers, the field map, the ralf read set, the ownership gate — is in
[PLAYBOOK.md](PLAYBOOK.md).

Sits alongside two siblings pointing the other way: `cohere-bug-triage` triages what already
broke, and `meet-a-user` voices the user. This one writes the work.

---

*Original skill by Divy Sharma · MIT License.*
