---
name: jira-ticket-writer
description: "Write COH Jira Stories from an initiative (Epic, PRD, or pasted brief) by simulating a cross-functional refinement session — PM, designer, engineer, and QA debating approach and best/worst cases until the acceptance criteria and test plan are hardened. Grounds the technical approach against the RALF intake architecture and flags work that is not Intake-owned. Use when asked to write or draft Jira tickets or stories from an initiative or epic, break an initiative into stories, write acceptance criteria or a test plan, refine or groom a ticket, or check whether a piece of work is Intake's to build. Opposite direction from cohere-bug-triage (which triages what already broke) and meet-a-user (which voices the user); this one writes the work."
version: 1.0.0
author: Divy Sharma
license: MIT
metadata:
  jira_project: COH
  optional: ["gh CLI + CohereHealth/ralf access (for architecture grounding)", "Atlassian MCP (to read the epic and create stories)"]
---

# Jira Ticket Writer

A good ticket is not a filled-in template. It is the output of an argument — a PM, a designer,
an engineer, and QA pushing on approach, edge cases, and failure modes until the story, the
technical "how", the acceptance criteria, and the test plan all survive contact. That argument
is the expensive part. This skill runs it and hands you the result.

Full mechanics: **[PLAYBOOK.md](PLAYBOOK.md)**.

## Quick start

> Write the tickets for COH-8248.

Run 1 returns the decomposition map and **stops**:

```
7 candidates → 5 build, 1 context, 1 flagged-foreign

1   Data: add documentType to the attachment model              build
2a  Search FE: require document type on upload                  build
2b  Configuration: per-client document type list                build
—   Route cases by document type                                context → Integrations
—   Split combined attachments into individual documents         flagged-foreign → Data
```

Then: **"draft 1 and 2a"** → each comes back as a full house-format story with acceptance
criteria, a test plan for `customfield_10065`, open questions, and a confidence mark. Nothing
reaches Jira until you say so.

## The one rule

The panel may **voice** freely — it is an instrument, not the product. It may never **source**
evidence. Every fact a seat cites must trace to the Architecture Card, the Initiative Brief, or
the register rules. A seat that needs a fact it does not have raises an **open question**, never
an assertion.

Twenty plausible inventions are worse than one honest gap, because inventions survive review.

## Workflow

1. **Take the initiative.** A COH Epic key, or pasted text. Run the quarter-bucket detector
   (`Q[1-4] \d{4}`, "Fast Follows", "P1s", unrelated children) — on a match, **ask**; never
   silently decompose a quarter bucket as if it were a feature. Epic descriptions are often
   empty; if thin, ask for the Confluence PRD or Monday link, or a paste. Do not infer scope.

2. **Build the Initiative Brief.** Business intent, client(s), value framing, the "so that"
   clause, design links. Jira is authoritative for business intent, client, and status.

3. **Build the Architecture Card — optional.** If `gh` and `CohereHealth/ralf` are reachable,
   read the 3-file spine and distil to one screen (read set + card schema in PLAYBOOK). If not
   reachable, **say so once, plainly**, and mark every technical claim 🔴 for the rest of the
   run. A labelled gap beats a confident guess.

4. **Run the ownership gate.** Which of the 9 submission steps this touches, and who owns each.
   Only **1 of 9 is Intake-owned**, so this fires more often than anyone expects. Three verdicts
   per candidate: `build` / `context` / `flagged-foreign` (see PLAYBOOK). Without the card, state
   that routing is unverified rather than guessing.

5. **Present the decomposition map.** Candidates named `<seq><letter> - <layer>: <imperative>`,
   each with its ownership verdict, register, and dependency order. Show it as an **editable
   table**, then report `N candidates → M build, K context, J flagged-foreign`.
   **→ GATE 1: stop. Ask which stories to draft.** A wrong split otherwise yields beautifully
   written wrong stories, and this is the cheapest moment to fix it.

6. **Draft the chosen stories.** Run the panel loop per story (PLAYBOOK). Each story emits a
   house-format description, a test plan for `customfield_10065`, its open questions, and a
   confidence mark. Pick the register **first** — it changes the whole skeleton.

7. **→ GATE 2: confirm before writing to Jira.** Draft-only is the default. On an explicit yes,
   create as Story (`10001`) parented via the real `parent` field. Never file as `Initiative`.

## Never

- No `As a [role], I want…` on a Story, and no Gherkin. Neither exists in COH Stories.
- Never put acceptance criteria in `customfield_10720` — it is dead. AC go in the description.
- Never emit `components` (none defined project-wide) or guess person+client labels (`YA-ESS`).
- Never fabricate a Member ID or DOB. Emit `NEEDS_TEST_PATIENT` so the gap stays visible; the
  real lookup lives in `cohere-bug-triage`. An invented ID looks exactly like a real one.
- Never auto-fill story points. Offer; do not invent an estimate the panel did not earn.
- Never auto-invoke `meet-a-user` — its *(synthetic user, not a real interview)* label exists to
  stop synthetic voice leaking into artifacts, and a live ticket is that leak. Draft here, then
  run its Panel mode against the finished stories yourself.

## If information is missing

Ask. A wrong config key name, a wrong owning team, or a made-up endpoint is worse than an honest
blank, because someone will build on it. When RALF is unreachable, when the epic is empty, when
the config's scope granularity is unstated — surface it as an open question.
