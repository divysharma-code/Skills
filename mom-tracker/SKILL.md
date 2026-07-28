---
name: mom-tracker
description: Write a Minutes-of-Meeting (MOM) doc from ONE specific Fellow.app meeting (transcript/summary) that the user has named or pointed to, save it locally, and log it as a row in a "MOM Tracker" Google Sheet. Use when the user says things like "write up this meeting," "log this meeting," "add this to the MOM tracker," "write the MOM for the call with X," "go look at this Fellow recording and write it up," or names a specific meeting/recording/date and asks for minutes/notes. Always operates on exactly one meeting that the user explicitly identifies. Never auto-scans Fellow, never backfills in bulk, and never runs without the user naming the meeting first.
version: 1.0.0
author: Divy Sharma
license: MIT
metadata:
  spreadsheet_id: "<fill in after one-time sheet setup — see Setup below>"
  spreadsheet_url: "<fill in after one-time sheet setup>"
  sheet_tab: "Log"
  local_mom_dir: "<path to your MOM notes folder, e.g. ~/Desktop/MOM/MOM/>"
  requires:
    - "mcp__fellow__search_meetings"
    - "mcp__fellow__get_meeting_summary"
    - "mcp__fellow__get_meeting_transcript"
    - "mcp__fellow__get_meeting_participants"
    - "mcp__google-workspace__read_sheet_values"
    - "mcp__google-workspace__modify_sheet_values"
    - "mcp__google-workspace__manage_doc_tab"
---

# MOM Tracker

Turns one named Fellow.app meeting into a structured MOM markdown file, and
logs it as a single row in a MOM Tracker sheet. See `REFERENCE.md` for the
MOM template variants, the column schema, and the Meeting Type taxonomy.

## Setup (one-time, before first real use)

1. `create_spreadsheet(title="MOM Tracker", sheet_names=["Log"])`
2. Write the header row: `Date | Meeting Type | Attendees | MOM Doc | Topic | Fellow Note ID`
3. Bold the header row, freeze row 1, auto-resize columns.
4. Fill the resulting `spreadsheet_id`/`spreadsheet_url` into this file's
   frontmatter above, and set `local_mom_dir` to wherever you keep meeting
   notes. Never re-run this step or re-search for the sheet afterward — one
   sheet, referenced by ID, forever.

## When to use

Only when the user explicitly names or points to a specific meeting — by
title, date, participant names, or a Fellow link/ID — and asks for it to be
written up, logged, or tracked. Never proactively scan Fellow for new
meetings, never run this on more than one meeting per invocation, never
backfill past meetings unless each one is named individually.

| Instead of mom-tracker | Do this |
|---|---|
| No Fellow recording/notes exist for the meeting | Write the MOM directly from what you're told — nothing to fetch, skip the skill |
| Bulk-processing many past meetings at once | Not supported. Name each meeting individually, one pass per meeting |
| Just want to know what was discussed, no permanent doc needed | Pull `get_meeting_summary`/transcript and answer directly — don't invoke the skill |
| Changing the tracker's columns, taxonomy, or template variants | Edit `REFERENCE.md` directly — that's a one-time config change, not a per-run action |

## Workflow (run in order)

1. **Resolve the meeting.** If a `meeting_id`/`note_id` was given directly,
   use it. Otherwise use `search_meetings` (title/participants/date) to
   confirm the exact meeting meant — if more than one candidate matches,
   ask which one rather than guessing.

2. **Pull context.**
   - Always: `get_meeting_summary` (chapters, action_items, decisions).
   - Only if the summary is thin, cuts off mid-topic, or more depth/direct
     quotes are needed: `get_meeting_transcript` in 300–3600s chunks.
   - `get_meeting_participants` for the attendee list (also feeds Meeting
     Type inference).

3. **Draft the MOM.** Pick the variant from `REFERENCE.md` §1 using its
   "Choosing a variant" heuristic — 1:1 knowledge-share, weekly rollup,
   discussion/brainstorm, or strategy/belief-mapping (decode) — and fill it
   in. For the Questions section specifically, follow `REFERENCE.md` §2 to
   decide between an attribution table and thematic clusters; don't default
   to one without checking which fits the meeting's shape. Follow the house
   style exactly: H1 title with date + duration inline, no YAML frontmatter,
   H2 numbered sections, tables for anything structured (frameworks, action
   items, decisions), closing with a `## Reference` block naming the Fellow
   `note_id` / `meeting_id` / `recording_id` and any follow-up people.

4. **Save locally** to `<local_mom_dir>/<YYYY-MM-DD>-<slug>.md` (match the
   existing filename convention — see `REFERENCE.md` §1 examples).

5. **Build the proposed tracker row**: Date, a *guessed* Meeting Type (see
   `REFERENCE.md` §4 — never commit this silently), Attendees, Topic, the
   Fellow Note ID, and a MOM Doc link (the local file's `file://` path,
   unless a Google Doc mirror already exists — see step 8).

6. **Confirm gate — CONFIRM BEFORE WRITING TO THE SHEET.** Show:
   - the saved MOM's file path and its section headings
   - the exact row about to be appended, with the guessed Meeting Type
     called out explicitly to accept or correct

   Wait for an explicit go-ahead. Only skip this if explicitly told to skip
   it for that run.

7. **Append the row.** Read `Log!A:A` on the tracker sheet (`spreadsheet_id`
   above) to find the last used row, then `modify_sheet_values` on
   `row + 1`, columns A–F. Use `=HYPERLINK("<url_or_file_path>", "<label>")`
   for the MOM Doc cell.

8. **Optional Google Doc mirror** — only if asked. Push the MOM into a
   Google Doc: create or find the target Doc, then `manage_doc_tab` with
   `action: populate_from_markdown` using the saved MOM's markdown. If the
   row was already logged, update that row's MOM Doc cell to the new Doc
   URL instead of adding a new row.

## Notes

- This skill never touches more than one meeting per run. For several
  MOMs, treat each one as a separate pass through steps 1–8 (still one at a
  time, still with its own confirm gate).
- The tracker's `spreadsheet_id` is fixed in this file's frontmatter after
  Setup — don't search for or create a new sheet on every run.
- Permission prompts on first use of any Google Sheets write tool or
  Fellow transcript/participant tool are expected if they aren't already
  allow-listed.
