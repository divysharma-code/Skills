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

## Pick one house format — don't invent a third

Cohere already has two live formats in Confluence. Use whichever fits (both in
full, with worked examples, in `REFERENCE.md`):

- **Format A — config/behavior change**: Purpose line → summary table
  (Update / Type / Availability / Who it affects) → what's changing (bullets)
  → what the reader will notice → action required → timing → reference footer.
- **Format B — new feature/UI change**: one-line narrative opener → summary
  table (Status / Feature / Launch date / User group) → what's new → how to
  use it (numbered steps) → reference footer.

## Workflow

1. **Get the source.** A Jira ticket key/link, a Confluence config-doc page
   (e.g. the "Context → Components → Configuration Example" format), or a
   rough bullet list of what shipped.
   - Jira key/URL given → pull it via the Atlassian MCP (`getJiraIssue`) if
     connected. If not connected, ask Divy to paste the summary/description.
   - Confluence link given → pull it via `getConfluencePage` and translate its
     config-field language into what the reader actually manages — never
     leave a raw field name like `enableManuallyCreatedProviders` in the note.
2. **Pick the format** (A or B) and confirm the register is internal
   (Ops/PlatCon/CX) unless told otherwise.
3. **Draft**, answering the four questions explicitly. Short paragraphs,
   generous line breaks — that's the fix for "don't like scrolling," not
   removing personality.
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

See [REFERENCE.md](REFERENCE.md) for the two full format templates with worked
examples, the real Cohere retro feedback on its release notes channel, and the
existing Jira-driven pipeline (`release notes required?` field + `Planned
Release Date`) that already feeds weekly Intake & Review release notes.
