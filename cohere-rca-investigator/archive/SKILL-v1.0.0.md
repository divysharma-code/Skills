---
name: cohere-rca-investigator
description: "Investigate ONE Cohere ticket (CTS, COH, IPS, ICS, DP) end to end and write the RCA as a clear document. Works in a fixed order: ticket, docs hypothesis, human context (Fellow/Slack), code check, write-up. Every claim is tagged VERIFIED or GUESS, and a guess is replaced as soon as better evidence shows up. Also owns how the RCA doc is written: plain English first, tables over prose, old-guess vs corrected-finding table, a 'still unverified' list. Use when asked to investigate, RCA, root-cause, or 'help me understand' a specific ticket, especially as a newcomer, or to write up an investigation. For the daily board-1487 queue use cohere-bug-triage instead."
version: 1.0.0
author: Divy Sharma
license: MIT
metadata:
  requires: ["Jira creds in ~/.config/jira/credentials.env", "gh CLI authed to CohereHealth"]
  optional: ["Fellow MCP", "Slack MCP", "google-workspace MCP"]
---

# Cohere RCA Investigator

One ticket in, one RCA out. The point is to be right, not fast: the first answer is a
guess, and the job is to replace it with something verified.

## Core rule

Tag every claim **VERIFIED** (saw it in the ticket, code, data or a transcript) or **GUESS**
(inferred). Never state a guess as fact. When better evidence contradicts an earlier guess,
say so openly and show both (see TEMPLATE.md, "What I got wrong").

## Inputs

Ticket key (required). Optional: a Fellow link, a Slack thread, a reporter name. Use plain
English for a newcomer: explain a term the first time it appears.

## Workflow (in order, don't skip ahead)

1. **Ticket.** Pull it from Jira (Basic auth from `~/.config/jira/credentials.env`, include
   comments, linked issues, clones). Split the reporter's claims into separate complaints and
   judge each: true / partly true / not true, with why. Reporters often bundle a real bug
   with a wrong description of it (e.g. "auto-approved" when a human approved after a pend).

2. **Docs hypothesis.** Search RALF (`CohereHealth/ralf`, via `gh`) for the feature area.
   Form a first hypothesis and label it **GUESS**. Name the likely owner (Intake / Clinical
   Intelligence / Integrations / Data platform) and whether it can be reproduced in UAT.
   Ownership map: case/auth statuses = clinical intelligence; auth retriggers = integrations,
   not Intake. RALF miscategorizes ownership, so cross-check it.

3. **Human context.** If given a Fellow link or Slack thread, read the summary and transcript
   (Fellow short links carry no ID: search by topic and date, match the `meeting_link`).
   People in the room usually know what the docs don't. Where it contradicts step 2, replace
   the guess. If the user gave no recording or thread, skip and say the write-up is mostly GUESS.

4. **Code check.** Find the real logic. `core-platform` and `frontend` merge to **`develop`**
   (the API's default branch is stale), so fetch with `?ref=develop`. Run
   `gh search prs "<KEY>" --owner CohereHealth` to find both halves of a FE+BE change.
   Cite `file:line`. **Read what a field does, not what its name says** (`createdByExternal`
   was true only for back-office staff, the opposite of its name). If the config or rule
   lives outside the repo, say so and keep the cause as "likely".

5. **Re-check negative claims.** "No test data", "not reproducible", "no config exists" are
   often stale. Verify before repeating them.

6. **Write-up.** Use [TEMPLATE.md](TEMPLATE.md). Chat first. Only create a Google Doc if
   asked.

## Documentation rules (learned the hard way)

- **Plain English first.** The reader may be new. Analogy and a 3-line short version go
  before anything technical.
- **Tables and bullets over paragraphs**, tiny sections, white space. Dense prose reads as
  unfinished to Divy.
- **Keep ticket keys, config strings and ownership jargon out of the prose.** Put them in
  the Reference footer. The exceptions are the source line and `file:line` citations.
- **Show the correction.** A two-column "my earlier guess | what the evidence showed" table
  builds trust and stops the next person repeating the guess.
- **End with "Still unverified".** Config you couldn't see, scope questions, screenshots you
  couldn't open. Name the person who can answer each. This is honest, not patchy.
- **Run it through the-humanizer** before sharing outside chat: zero em dashes, no
  arrow-chains in prose, no "to be clear" announcements. Divy's tables, bullets and ELI5
  override the humanizer's "prefer prose" default.
- **No PHI.** Tracking IDs are fine. Member IDs, DOBs and names are not.

## Boundaries

- Never post to Jira, Slack or Drive unless asked. The user decides what gets filed.
- Not filing a fix ticket is the default. If asked to draft one, hand the findings to
  `jira-ticket-writer`, and offer `slack-question-writer` for the ask.
- Docs for Google Docs: stage Markdown in `~/.workspace-mcp/attachments/` with real `#`
  headings and a blank line between lines (single newlines merge), and no `<angle>` text.

## If a source is missing

Fellow, Slack or Google not connected: skip that step, label the gap in "Still unverified"
and lower confidence. Don't fill the gap with a guess.
