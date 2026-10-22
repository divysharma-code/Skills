---
name: artifact-documentor
description: "The artifact documentor. Turns a finished Cohere RCA (root cause analysis) into a one-page visual walkthrough, published as a private Artifact. The page has a finding-as-headline, a plain-English answer box, term cards, a flow diagram showing where a guard exists and where it is missing, a dated timeline, a diagram of how the answer decides who owns it, a 'why it stayed stuck' table and a 'what is known and what is not' table tagged VERIFIED, INFERRED or UNVERIFIED. Use when asked for the artifact documentor, an insight page, a visual RCA, an explainer page, an artifact for an RCA, 'create a flow diagram and explain what happened', or to share an investigation with a stakeholder or engineers. It does not investigate: run cohere-rca-investigator first, or paste an RCA."
version: 1.1.0
author: Divy Sharma
license: MIT
metadata:
  requires: ["artifact-design skill", "artifact-diagramming skill", "Artifact tool"]
  optional: ["cohere-rca-investigator", "the-humanizer"]
---

# Artifact Documentor

An RCA in, one page out that a stakeholder can read cold in two minutes. The bar is the COH-8221
page ("Two doors into Cohere, and only one has a guard"). [TEMPLATE.html](TEMPLATE.html) is that
page's exact CSS and layout with the content removed.

## Quick start

0. Check you can publish before building: the Artifact tool needs a claude.ai login. If the
   session uses `apiKeyHelper` it refuses every call. Then build the file, save it to the
   Desktop, and tell the user to unset `apiKeyHelper` and run `/login` to get links.
1. Get the RCA: the `cohere-rca-investigator` write-up in this chat, a pasted RCA, or a doc.
2. Load `artifact-design`, then `artifact-diagramming`.
3. Copy TEMPLATE.html to the job's tmp folder as `<key>-insight.html` and fill every `{{...}}`.
4. Run `python3 scripts/check.py <file>`. Fix everything it reports.
5. Publish with the Artifact tool (private). Give the link and say who it was written for.

## The page, top to bottom

| # | Section | What goes in it | Source in the RCA |
|---|---|---|---|
| 1 | Eyebrow | `KEY · Client · Root cause walkthrough` | Header |
| 2 | Headline | The finding as a short sentence, built on an image (doors, guard, tag). Never the ticket title. | ELI5 |
| 3 | Answer box | Lede: what is wanted, where the gap is, what it causes. Muted line: the open question, who asked it, what would answer it, whether anyone has. | ELI5, Still unverified |
| 4 | Terms | One card per term or acronym used anywhere on the page | Glossary, brief |
| 5 | Flow diagram | Happy path and bug path side by side, ending where they meet | Workflow, What went wrong |
| 6 | Timeline | Dated events, one line each | Ticket, comments, calls |
| 7 | Decision diagram | Read X. If A, owner 1. If B, owner 2. | Fix options, owner |
| 8 | Why it stayed stuck | What people tried, why it didn't work, tag | Ticket history, What I got wrong |
| 9 | Known and not | Claim, evidence, tag | Every tagged claim |
| 10 | Reference | Tickets, `file:line` (branch), sources, a no-PHI line | Reference |

Optional, after 9: "Questions the code answered", from the RCA's SPM and Engineer loop (PM
asked, Engineer answered, tag). Add it only when the reader is an engineer.

## Rules

- **Colour carries meaning.** Teal (`--guard`) is a check that exists, or the breakthrough.
  Amber (`--gap`), dashed, is a missing check or a turn in the story. Nothing else gets colour.
- **Every claim in tables 8 and 9 has a tag.** In diagrams, an INFERRED value says "(likely)".
- **A claim says only what its evidence covers.** Code-only evidence means the claim says "in
  code". On COH-8221, "Cohere has no QMB block" was true in code only; the block messages live
  in health-plan config.
- **Define before use.** Any term on the page has a card. Expand every acronym on first use.
- **Timeline classes.** `turn` for an event that changed the story, `found` for the answer.
  At most 3 `turn` rows and 1 `found` row, or the colour stops meaning anything. If the
  ticket ends on an open question, use no `found` row and end on the question, in plain text.
- **Unconfirmed names.** A screen or field name the code did not confirm gets "(unconfirmed)"
  after it, in the diagram and the text.
- **Page variants.** Data fix (a one-time migration): replace flow diagram 1 with a
  before-and-after of the data, and put the risk of running it in the answer box. Analytics
  or reporting gap: the flow diagram shows where the count is stamped, and the ownership
  diagram splits on "did the traffic move, or did the stamp break".
- **Still open.** End with a "Still open" table (open item, who can answer). It is the only
  table that needs no tag.
- **Plain English.** Short sentences, no em dashes, no arrow chains in prose. Ticket keys and
  config strings go in Reference, except in the eyebrow and the code citations.
- **No PHI.** Tracking numbers are fine. Member IDs, dates of birth and member names are not.
- **Diagrams.** Use the two SVG skeletons in the template. Keep `min-width: 760px` so they
  scroll sideways on a phone instead of shrinking. Write a real `aria-label` for each.

## Who it's for

| Reader | Change |
|---|---|
| Stakeholder (CS, client lead) | Default. Drop the optional Q&A section. |
| Engineers | Add the Q&A section and fuller `file:line` in Reference. Keep the answer box. |
| PDF | Publish, then print the page to PDF. Name it `<KEY>-<topic>-for-<reader>.pdf`. |

## If something is missing

- No RCA: stop and offer `cohere-rca-investigator`. Never invent findings to fill the page.
- No dates: drop the timeline and say so under the headline.
- No ownership fork: drop the decision diagram.
- No Artifact tool: save the HTML on the Desktop, open it in a browser, and say it isn't
  published.
- Before sharing outside chat, run `the-humanizer` if installed, but keep tables and cards.

## Checklist before publishing

- [ ] `scripts/check.py` passes
- [ ] The headline states the finding, not the ticket title
- [ ] Every tag matches the RCA's tag for that claim
- [ ] Both themes readable (the template's tokens handle this unless you add colours)
