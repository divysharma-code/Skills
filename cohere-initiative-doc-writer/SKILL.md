---
name: cohere-initiative-doc-writer
description: Write Cohere Health Confluence pages for a product initiative, in one of three house styles: a pre-build "Initiative Brief" (problem statement, JTBD, timeline, open questions, stakeholders — used to scope and pitch work, and kept live/updated as phases ship), a post-build "Feature/Capability Reference" (Overview, Why, Definitions, What we built, Example Walkthrough, How it's configured, FAQ — for a shipped feature, mixed PM/eng/ops audience), or a plain-English "Feature Documentation" page in the Fax Intake Close Reason shape (Product Overview, Demo with a Step | Action | Script table, Reporting and Analytics, Release Information, Other Resources with FAQ and stakeholders — for a feature that is built or nearly built, read by CX, Ops and new PMs). Use when Divy asks to write up a new initiative, draft a PRD/brief for an initiative, document a feature that just shipped, write the feature doc or product documentation page for a feature, write a page "like Fax Intake Close Reason", write an "Initiative | <Name>" page, or turn a Jira epic into a Confluence doc. Distinct from cohere-config-doc-writer (that's the narrower engineering-only "Context → Components → Configuration Example" format for a single config block, written for the engineer flipping the key — not the initiative-level narrative this skill covers), jira-ticket-writer (breaks an initiative into Jira stories, not Confluence prose), and release-notes-writer (a short internal "what shipped" announcement for Ops/CX, not the full reference doc).
---

# Cohere Initiative Doc Writer

Cohere documents initiatives in three distinct Confluence house styles. Read
the matching reference file once before your first use of that template — each
is a real page this template was extracted from and doubles as a calibration
example.

## Which template

ALWAYS confirm the shape with Divy before drafting unless he named it or linked
a page to copy. Guessing the wrong shape wastes a whole draft (it happened on
the Temp ID doc: Brief, then Reference, then a rebuild once he linked the page
he wanted). If he links a live Confluence page, fetch it with
`getConfluencePage` and match THAT page's sections, not a saved copy.

- **Still being scoped / not yet built, or written alongside the pitch** →
  Initiative Brief. Title format `Initiative | <Name>`. See
  `references/example-billable-families-brief.md`.
- **Already shipped, and you're documenting what it does / how it's
  configured** → Feature/Capability Reference. See
  `references/example-bypass-crd-redirect-reference.md`.
- **A feature page a CX, Ops or new-PM reader can follow end to end: what it
  is, why, a demo script, where to see it in Kibana, which flag, FAQ, who owns
  it** → Feature Documentation (Fax Intake Close Reason shape). Title is the
  plain feature name. See `references/example-fax-close-reason-feature-doc.md`.
  Pick this when Divy says "feature doc", "product documentation", "like Fax
  Intake Close Reason", or wants a demo script with it. Works while the feature
  is still finishing: mark open items `[GAP]` rather than waiting.

Not this skill: the commercialization business case ("New Product / Feature
Template", ENG space, owned by Commercialization) and the technical-services
config how-to ("[TEMPLATE] Configuration Documentation", Cohere Hub space; use
`cohere-config-doc-writer`). Different owners, different readers.

A hub concept matters for the Reference template only: if this feature
extends an existing durable capability (e.g. "PA Check"), it should nest as a
child page under that hub rather than standing alone — ask whether a hub page
already exists before creating an orphan page.

## Initiative Brief template

Title: `Initiative | <Name>`. Then, in order:

1. **Overview** — 1 paragraph: what this does, what outcome it produces.
2. **Context** — current-state description, 2–3 concrete named examples of
   the breakdown (not abstracted), and quantified pain: real volume/cost
   numbers ("X% of Y over 90 days... at $Z per case, costing $N"). Bullet the
   downstream implications (ops cost, member experience, scalability).
3. **Problem Statements** — grouped by persona/stakeholder (Submitters,
   Reviewers, Payers...). Each: bolded problem name, then 1–2 sentences on
   what they experience and why it matters to them.
4. **Impact / Why Now** — why this is worth doing right now: established
   volume/trend data, upcoming go-lives or dependencies that raise the
   stakes, external forces (payer policy, compliance).
5. **Goals / Success Criteria** — table: Goal | Metric to track. Metrics are
   comparative ("currently X%, target <Y%") and paired with the $ impact of
   moving them.
6. **Phase [N]** — repeat this whole block per phase (Phase I, Phase II...):
   - **Jobs to Be Done** — table: JTBD | User Stories (sub-JTBD) | Notes,
     grouped by persona. Mark speculative stories explicitly (e.g. "***Maybe").
   - **Launch Timeline** — bullets, not a table: scoping/design/eng dates,
     upstream dependencies owned by other teams (named owner + date), key
     milestones/go-live checklist (a placeholder is fine pre-plan).
   - **Proposed Workflow** — link out to the Figma board, attributed to
     whoever proposed it. Don't embed or restate it.
   - **Open Questions** — a LIVE DECISION LOG, not a to-do list. Bulleted,
     can nest sub-questions. As questions get answered, append the answer
     inline under the question rather than deleting it ("Short answer seems
     to be...", "We are deferring this to...", "This does not matter
     because..."). This is what leaves an audit trail of how scope narrowed —
     never delete a resolved question.
7. **Resources**
   - **Stakeholders** — list every functional category even if blank
     (Product, Design, Engineering, Analytics, UXR, Provider Relations,
     Clinical Programs, Client/Growth, Service Ops, Marketing, Legal &
     Compliance, Privacy/Security). This is a checklist so no function gets
     forgotten, not just a contact list — don't drop empty rows.
   - **Links** — Slack channel, Research doc, workflow diagram, Designs (one
     link per named variant, e.g. "Phase 1 Designs" / "Ideal State Designs"),
     Jira (one epic link per phase), client decks, related initiatives.
8. **Results** — table: Goal | Result | Comments, one row set per phase.
   Leave it EMPTY until that phase actually ships — this is what turns the
   brief from a pitch doc into a closed-loop record. Never backfill this
   with a guess.

## Feature/Capability Reference template

Default to this section order (the current, tightest house style — see the
reference file); fall back to a looser structure only if the source material
genuinely doesn't fit it:

1. **Overview** — 2–3 sentences: what this is, what it reuses/differs from
   vs existing patterns.
2. **Why we built this** — the pain, in plain terms, 1–2 short paragraphs.
3. **Some definitions** — only terms this doc introduces or overloads. Bold
   term (+ acronym expansion) — one-line def. Skip anything already defined
   on the hub page.
4. **What we built** — sub-headed by mechanism/component, not by sprint or
   ticket. Spell out any persisted field inline: name, type, nullable/default
   — don't make the reader infer the schema.
5. **Example Walkthrough** — a Step | Action table. Link out to Figma/design
   instead of embedding every screenshot.
6. **[Persona] Side** — repeat per persona if more than one user type is
   affected (e.g. "Review Side" alongside the intake-side walkthrough).
7. **How is this configured?** — where to click in the admin UI, then a
   "Gating flags:" bullet list naming exact flag strings with a one-line
   purpose each, then a literal JSON config block with real key names. State
   scope explicitly — which payers/LOBs this is live for now vs. planned.
8. **FAQs** — numbered, anticipating "what happens if X" edge-case questions.
9. **Other Resources** — links only (Jira epic, Figma, related config page).
   Never duplicate their content here.

## Feature Documentation template (Fax Intake Close Reason shape)

Title: the plain feature name (no `Initiative |` prefix). The headings are
H1 sections, in this order:

1. **Product Overview**
   - **Feature Details** — what it is in plain words, then 2 or 3 bullets of
     what the user sees. Say what changed from the old behavior and what an
     unconfigured client gets (usually "exactly as before").
   - **Why We Built It** — the old pain in 1 short paragraph or 2 bullets.
   - **Known Gaps/Out of Scope** — bullets. Put follow-up tickets and
     unconfirmed assumptions here instead of burying them.
2. **Demo**
   - **Step by Step Walkthrough** — table `Step | Action | Script`. The Script
     column is a first-person line Divy could say out loud to a client, set in
     one concrete scenario (e.g. a newborn in the NICU). Continue rows with a
     blank Step cell.
   - Optional: "NEW Addition!" block for a later change (what is changing,
     impact, config snippet) and a Demo Video link.
3. **Reporting and Analytics** — Kibana link, where the value is recorded
   (field name), what to watch after launch.
4. **Release Information** — feature flag (exact string, `code format`),
   relevant user roles, which payers it is released to. Put the config how-to
   here as a "Configuration" subsection: where to click (My Account >
   Configuration Management > Feature > health plan), a Setting | What it does
   | If left empty table, and a literal config snippet. Verify every field
   name against the config class in core-platform (`?ref=develop`) before
   writing it.
5. **Other Resources**
   - **FAQ** — numbered, bold question then answer. Include "what happens to a
     client I don't configure?" and "what did the old page get wrong".
   - **Documentation / Important Links** — Slack, initiative doc, designs,
     technical docs, Jira epic(s). Ticket keys live HERE and nowhere else.
   - **Key Stakeholders** — PM Owner, Dev Lead, Informed.

Voice rules (Divy corrected these on the Temp ID doc, 2026-10-15):

- Plain English first. Expand every acronym and term on first use.
- No ticket keys, config names or permission names in the body prose. They go
  in the Release Information config table and the Links section only.
- Describe the user's journey in the Demo script, not the engineering story.
- Tables and short bullets over paragraphs. No em dashes.
- Anything unknown is `[GAP]`, never a guess. Do not invent a PM owner: if the
  Jira epic owner is the only evidence, say so and let Divy confirm.
- For Google Docs delivery via import: write real `#` headings, put a blank
  line after every list, and avoid `<angle>` text. Read the doc back after
  import; code blocks and a heading can turn into smart chips.

## Formatting constants (all templates)

- TOC macro is always the first thing on the page (Initiative Brief and
  Feature/Capability Reference only; the Feature Documentation shape has none).
- Bullets and tables over prose; cap paragraphs at ~3 sentences.
- Config/flags are always named exactly as they appear in code/LaunchDarkly,
  in `code formatting` — never paraphrased.
- End sections by linking out, not by restating what the link already says.
- Numbers do the arguing in Context/Impact/Goals — real $ and % figures, not
  "significant savings" or "improved efficiency."

## Sourcing the content

If the Atlassian MCP is connected, use it to pull the driving Jira epic
(status, summary) and check whether a hub page already exists before writing
an orphan Feature Reference page. If it isn't connected, or a ticket doesn't
exist yet, ask Divy to paste the epic key/summary rather than inventing one —
a fabricated ticket key or status is worse than an honest blank.

## If information is missing

Don't invent: stakeholder names, cost/volume figures, metric baselines,
Jira epic keys, or flag names. A wrong number is actively worse than an
honest gap here, because Goals/Impact sections get quoted directly in
prioritization conversations. Ask instead.

## Before publishing

Draft the page content and show it to Divy before writing anything to
Confluence — this is a confirm-before-post skill, same as cohere-bug-triage.
Only call the Confluence write tools after he approves.
