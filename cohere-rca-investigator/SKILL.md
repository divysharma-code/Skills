---
name: cohere-rca-investigator
description: "Investigate ONE Cohere ticket (CTS, COH, IPS, ICS, DP) end to end, with the user reproducing it live, and produce the RCA plus ready-to-use drafts. Fixed order: ticket, plain-English brief, docs, human context, code, screen-by-screen flow, test data, live repro from screenshots, business impact, fix decision (council), grill, write-up. Every claim is tagged VERIFIED, INFERRED or UNVERIFIED, and a guess is replaced as soon as better evidence shows up. Outputs (draft only): a Google Doc with the screenshots, an impact tab, a Jira description, a Slack message. Use when asked to investigate, RCA, root-cause, reproduce, 'explain the workflow', or 'help me understand' a specific ticket, especially as a newcomer. For the daily board-1487 queue use cohere-bug-triage instead."
version: 2.2.0
author: Divy Sharma
license: MIT
metadata:
  requires: ["Jira creds in ~/.config/jira/credentials.env", "gh CLI authed to CohereHealth"]
  optional: ["Fellow MCP", "Slack MCP", "google-workspace MCP", "council", "jira-ticket-writer", "slack-question-writer", "the-humanizer"]
---

# Cohere RCA Investigator (v2)

One ticket in, one RCA plus drafts out. The point is to be right, not fast. The first answer
is a guess, and the job is to replace it with something verified, with the user's screenshots
as the strongest evidence.

## Changelog

| Version | Date | Change |
|---|---|---|
| 2.2.0 | 2026-10-22 | From a 5-ticket run on board 8105: Q&A cap 8 to 12 rounds, code-search rate-limit guidance, open ticket attachments, analytics-ticket shape, RALF field-name trap. |
| 2.1.0 | 2026-10-22 | SPM and Engineer Q&A loop (grill-me built in, see QNA-LOOP.md) runs during the code step, so the PM's questions are answered from the repo before the human is asked. The human grill now covers only what the loop could not answer. Source: COH-8221, where the grill step was skipped. |
| 2.0.0 | 2026-10-13 | Plain English before anything else. Real screen titles from code. Live screenshot repro loop. Fix-sketch testing. Impact chain with a "could not connect" list. Council at real forks only. One-at-a-time grill. Draft outputs: doc with screenshots, impact tab, Jira description, Slack message. Source: the COH-8363 investigation. |
| 1.0.0 | 2026-09 | Ticket, docs, human context, code, write-up. Archived in `archive/`. |

## Core rules

1. Tag every claim **VERIFIED** (saw it in the ticket, code, data, screenshot or transcript),
   **INFERRED** (follows from verified facts, not seen directly) or **UNVERIFIED** (a guess or
   someone's report). Never state a guess as fact.
2. A pasted RCA, a ticket comment or an old memory is a **hypothesis**. Check it, and show the
   correction (see TEMPLATE.md, "What I got wrong").
3. Explain before you ask. No questions to the user until the plain-English brief is done.
4. Draft only. Nothing is posted to Jira, Slack or Drive until the user says so.

## Workflow (in order, don't skip ahead)

1. **Ticket.** Pull it from Jira (Basic auth from `~/.config/jira/credentials.env`; include
   comments, clones, linked issues, earlier reports of the same bug). Split the reporter's
   claims into separate complaints and judge each: true / partly / not true, with why. Open the
   ticket's screenshots and attachments too; they often show the exact screen or count.
   An analytics or reporting ticket ("X is no longer reportable") is a different shape: first
   find where the number is stamped, then ask whether the traffic moved or the stamp broke.
2. **Plain-English brief.** Five lines: what the problem is, with any domain term defined
   before it is used (e.g. what "Observation" means), plus an ELI5 analogy. Say what you are
   sure of and what you are not. Do this before docs or code.
3. **Docs.** Search RALF (`CohereHealth/ralf`, via `gh`) for intended behaviour and the owning
   team. Label the result as a hypothesis. RALF miscategorizes ownership, so cross-check.
4. **Human context.** If given a Fellow link or Slack thread, read the summary and transcript.
   It often overturns step 3. If none was given, say the write-up leans on guesses.
5. **Code.** `core-platform` and `frontend` merge to **`develop`** (the API's default branch is
   stale), so fetch with `?ref=develop`. `gh search prs "<KEY>" --owner CohereHealth` finds both
   halves of a FE+BE change. Cite `file:line`. **Read what a field does, not what its name
   says.** Check the validator you cite actually belongs to the screen in question. If a rule or
   config lives in a database or outside the repo, say so and keep the cause as "likely".
   **Run the SPM and Engineer Q&A loop alongside this step** ([QNA-LOOP.md](QNA-LOOP.md)): a
   PM subagent asks one question at a time, an Engineer subagent answers from RALF and the
   code, and you log every round. Start it once the step-2 brief exists. It replaces guessing
   what the PM would ask.
6. **Flow map with real screen titles.** Take on-screen titles from the code's label map (for
   the auth builder, the header component), never from memory or your own wording. Mark any
   title you could not confirm. Draw the happy path first, then where the bug path diverges, and
   name the screen where each thing happens.
7. **Test data.** Use the user's test-data sheet through a **subagent** so a big read stays out
   of the main chat; it returns a filtered table only. Check the tab and its size, not memory.
   Verify the plan name exists (call transcripts mishear them). Match the line of business the
   gate reads, not just the plan. Re-check any "no test data for X" claim. Keep member IDs and
   dates of birth out of tickets and Slack; link the sheet row instead.
8. **Live repro, one screen at a time.** The user sends a screenshot. For each one, say:
   what it **confirms**, what to **look for next**, and what it **does not prove**. Check it
   against the code before you answer. Notice who is logged in (internal staff screens, such as
   an "Unnamed Requestor" banner or a status-change dialog, mean it is not a provider login) and
   say whether that limits the finding. Warn before any click that changes auth state.
   - **Test the user's fix idea** by tracing it through the code. Look for the hole (what a user
     can still do that gets the same bad result) and show the code that proves it.
9. **Business impact.** Connect the bug to what it costs (for example a missed turnaround
   deadline) using the docs. Build a chain table: step, what happens, who feels it. End with
   **"What I could not connect"**, each gap paired with the one check, and the person, that
   would settle it. Never claim a queue, rule or deadline behaves a certain way when it lives in
   data you could not read.
10. **Fix decision.** Only at a real fork, run the council: four voices (Architect, Skeptic,
    Pragmatist, Critic). The three outside voices are **fresh subagents given only the question
    and compact context**, never the whole chat. Use the `council` skill if installed, otherwise
    run the same shape inline. Then **verify the council's load-bearing claim against the code**
    before accepting it, and say if a voice changed your mind.
11. **Grill the human.** Only on what the Q&A loop left open: its UNVERIFIED and parked
    branches. One question at a time, each with your recommended answer and who could answer it.
    Start only after steps 2 to 9 are done. If the loop was skipped, say so in "Still
    unverified". If asked for "all questions", list them ordered by dependency, with the
    options and the catch for each.
12. **Write-up and drafts.** Follow [TEMPLATE.md](TEMPLATE.md) and the output rules below.

## Outputs (all draft only)

| Output | How |
|---|---|
| RCA in chat | TEMPLATE.md. Always first. |
| Google Doc | Tab 1: notes plus every screenshot in order. Tab 2: the impact explainer. Only on request. |
| Jira description | Actual vs expected, provisional acceptance criteria, out of scope, grooming questions, test plan, evidence. Hand to `jira-ticket-writer` if installed. |
| Slack message | Paste-ready, no PHI, ask first. Use `slack-question-writer` if installed. |

**Doc mechanics (learned the hard way):**
- Google Docs only embeds images that are publicly accessible. Do not make screenshots public.
  Build a `.docx` with the images embedded (`uv run --with python-docx`) and import it as a Doc.
- Stage files in `~/.workspace-mcp/attachments/`. Screenshots from the session live in the
  session's image folder; copy them there first.
- A second tab filled from Markdown arrives with tables as raw `| a | b |` text. Create real
  tables with the table tool, bottom-up so positions stay valid, then read the tab back.
- Always read the finished doc back (text and table counts) before saying it is done.
- List what you left behind (extra docs, folders, local files). You cannot delete Drive files.

## Documentation rules

- **Plain English first**, analogy and a 3-line short version before anything technical.
- **Tables and bullets**, tiny sections, white space. Dense prose reads as unfinished.
- **Ticket keys, config strings and ownership jargon go in the Reference footer**, except the
  source line and `file:line` citations.
- **Show the correction** and **end with "Still unverified"**, naming who can answer each item.
- No em dashes, no arrow chains in prose, no "to be clear" announcements. Run the-humanizer
  before sharing outside chat, but keep tables, bullets and ELI5.

## Mistakes to avoid (all made once)

| Mistake | Rule |
|---|---|
| Drew a flow using a screen name I guessed | Real titles come from the code's label map |
| Wrote a repro step ("start as Outpatient") before reading the code | Read the code that sets the value first |
| Cited a validator from a different form | Confirm it is wired to this screen |
| Asked the first grill question before explaining the problem | Brief first, always |
| Predicted what the next screen would be | Say what to look for, not what it will be |
| Read a RALF field by its name (`groupId` there means procedure codes, not a member's group) | Read what the field holds in code |
| Treated "reproduced" as "proven" | Separate the form state, the saved value, and the downstream effect |

## Boundaries

- Never post to Jira, Slack or Drive unless asked. Never change sharing or permissions on
  files without being asked.
- Never send PHI anywhere. Tracking IDs are fine. Member IDs, dates of birth and names are not.
- Not filing a fix ticket is the default.

## If a source is missing

Fellow, Slack, Google or a sibling skill not available: skip that step, label the gap in
"Still unverified", lower confidence, and say so once. Don't fill the gap with a guess.
