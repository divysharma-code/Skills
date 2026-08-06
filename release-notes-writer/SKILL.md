---
name: release-notes-writer
description: Write Cohere release notes for Ops, PlatCon, and CX/Client Services readers — internal, non-engineering — from a Jira ticket, a Confluence config-doc page, or a rough bullet list of what shipped. Turns a technical config/feature change into a note that answers what changed, why, how it affects the reader's day-to-day, and what they need to do differently; personality/human tone is welcome since the audience is internal, but never at the cost of clarity or burying the actual change. Use when Divy asks to write, draft, or publish release notes, a "what shipped" update, a change announcement for Ops/CX/PlatCon, or wants to turn a ticket or config doc into a release note.
---

# Release Notes Writer

Release notes fail for one of two opposite reasons: they're a dry restatement of
the Jira ticket title ("Config change to manuallyCreatedProviders"), or they're
so busy being clever that the reader can't tell what actually changed. Neither
serves Ops, PlatCon, or CX — the people who'll field a client call about this
change five minutes after it ships. This skill's job is the translation step:
take something written for engineers (a ticket, a config doc) and write it for
someone who has to act on it, not implement it.

## The four questions every note has to answer

1. **What changed** — described in terms of what the reader will see/do
   differently, not the config key name.
2. **Why** — the real reason, not "improves configurability." If the ticket
   doesn't say why, ask rather than inventing a plausible-sounding rationale.
3. **How it affects the reader** — their queue, the config they manage, the
   tickets they'll get from clients.
4. **What they need to do differently** — often "nothing." Say that
   explicitly and put it near the top; don't make the reader infer it from an
   absence of instructions.

Skip any of these and the note reads exactly like the internal feedback Cohere
already has on record about its own release notes: "messy," hard to follow,
people "don't like scrolling." See `REFERENCE.md` for the actual quotes — reread
them before drafting, because they show the real complaint was never "too much
personality," it was length and scannability.

## Two more sections every note carries

Beyond the four questions, every note ends with these two — not optional
extras, part of the default shape:

- **Anticipated questions.** A short Q&A block that gets ahead of what a
  reader will ask five minutes after this ships — client scope ("does this
  apply to us?"), whether it's actually live yet, whether TAT/notifications
  really changed. Pull the questions from what's actually ambiguous in the
  source (a caveat in the config doc, a scoping note in the ticket), not
  generic filler. If something's a genuine open question rather than an
  answer you have, say that — don't invent an answer to look complete.
- **Contributors.** Name everyone who touched the work, not just whoever's
  listed as assignee/PO on the ticket. Pull from the Jira comment trail
  *and* the linked PR(s) — author plus reviewers — and call out anyone
  outside the core delivery pod by name (a reviewer on another team, someone
  from Review/Letters who signed off on a scoping decision, a person
  consulted for precedent from a related project). Don't fold everyone into
  a generic "the team" — that's exactly the credit non-PDDE contributors
  usually don't get. If a name's role or team affiliation isn't clear from
  the source, say so rather than guessing at it.

## Audience — this skill defaults to internal (Ops/PlatCon/CX)

Not client-facing. That means:
- Personality, a human voice, even a little humor is fine — the same retro
  feedback explicitly says "don't want to discourage back and forth... mini
  celebrations are important."
- It is *not* license to obscure the actual change. Every note still needs to
  survive the four questions above.
- If Divy asks for a client-facing version of the same change, that's a
  different, stricter register (plain English, zero jargon, "no action
  required" framing dominant) — write it as a separate note, don't try to
  serve both audiences in one draft.

## Pick one house format — don't invent a fourth

Cohere has three live formats. Use whichever fits (all three in full, with
worked examples, in `REFERENCE.md`):

- **Format A — config/behavior change**: Purpose line → summary table
  (Update / Type / Availability / Who it affects) → what's changing (bullets)
  → what the reader will notice → action required → timing → anticipated
  questions → contributors → reference footer.
- **Format B — new feature/UI change**: one-line narrative opener → summary
  table (Status / Feature / Launch date / User group) → what's new → how to
  use it (numbered steps) → anticipated questions → contributors → reference
  footer.
- **Format C — batch/multi-workstream rollup**: for when several distinct
  things shipped over weeks/months and get bundled into one running update
  (Slack-native, not a Confluence page). Opening hook paragraph with a
  headline metric → one entry per workstream (status emoji + bolded outcome
  headline + short why-it-matters paragraph + inline per-item shoutout) →
  closing capstone stat → separate leadership/design shoutout. Credit lives
  per-item here instead of in one end-of-note Contributors section — see
  REFERENCE.md for why and for the worked example (the Casey AI rollup).

## Workflow

1. **Get the source.** A Jira ticket key/link, a Confluence config-doc page
   (e.g. the "Context → Components → Configuration Example" format), or a
   rough bullet list of what shipped.
   - Jira key/URL given → pull it via the Atlassian MCP (`getJiraIssue`) if
     connected. If not connected, ask Divy to paste the summary/description.
   - Confluence link given → pull it via `getConfluencePage` and translate its
     config-field language into what the reader actually manages — never
     leave a raw field name like `enableManuallyCreatedProviders` in the note.
   - Also pull the linked PR(s) off the ticket (schema/BE/FE, whatever's
     linked) — author and reviewers. This is where non-PDDE contributors
     usually surface that the Jira comment trail alone won't show.
2. **Pick the format** (A, B, or C) and confirm the register is internal
   (Ops/PlatCon/CX) unless told otherwise. Reach for C only when the source
   is genuinely a multi-workstream batch (several separate pieces of work,
   different teams, shipped over a period) — not a fancier way to write a
   single-change note; that's still A or B.
3. **Draft**, answering the four questions explicitly, plus the anticipated
   questions and contributors sections (or, in Format C, the per-item
   shoutouts). Short paragraphs, generous line breaks — that's the fix for
   "don't like scrolling," not removing personality. In Format C especially,
   don't let the punchy one-liner replace the why — a status emoji and a
   bolded headline are not a substitute for the sentence that says what it
   actually means for the reader. Slightly fuller beats too terse here.
4. **Read it back once as a leak check**: would this embarrass anyone if a
   client saw it forwarded? This is where a placeholder or venting line
   ("TBD — a shit tonne of config changes") gets caught before it ships.
5. **Ask before publishing anywhere** — this skill drafts. Whether it lands in
   a Confluence page, gets pasted into Slack, or stays as a doc is Divy's call
   each time, not a default.

## Common mistakes

- Restating the ticket title as the whole note — the ticket says *what*
  changed, the note has to say *why* and *so what*.
- Burying "no action required" instead of leading with it.
- Config-doc language leaking through untranslated.
- One note trying to serve both an internal and a client-facing audience.
- Inventing a "why" when the source doesn't give one — ask instead.
- Crediting only the PO/assignee on the ticket and calling it "the team" —
  check the linked PR(s) for who actually reviewed and shipped it.
- Anticipated questions that restate the summary table instead of surfacing
  the thing a reader would actually push back on.
- Format C used just to look punchier for a single-item note — it's for
  genuine multi-workstream batches, not a style upgrade.
- Per-item shoutouts in Format C that are so terse the "why it matters"
  disappears — a one-line headline plus a name list isn't a release note.

See [REFERENCE.md](REFERENCE.md) for the three full format templates with
worked examples, the real Cohere retro feedback on its release notes channel,
and the existing Jira-driven pipeline (`release notes required?` field +
`Planned Release Date`) that already feeds weekly Intake & Review release
notes.
