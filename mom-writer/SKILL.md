---
name: mom-writer
description: Write a Minutes-of-Meeting (MOM) straight into a NEW Google Doc from one Fellow.app meeting Divy names, extracting exactly three things from the transcript — (1) questions asked and why they came up, (2) the reasoning/mental model of whoever is explaining a concept, and (3) action items with a clear ask and concrete steps. Use when Divy says things like "write the MOM for this as a doc," "turn this meeting into a MOM doc," "pull the questions and action items from this call into a doc," or asks for a quick, direct-to-Google-Doc MOM. Differs from mom-tracker: no local markdown file, no MOM Tracker sheet row — just one Google Doc, one meeting, one pass. Never auto-scans Fellow, never runs without Divy naming the meeting first.
version: 1.0.0
author: Divy Sharma
license: MIT
metadata:
  default_user_google_email: "divy.sharma@coherehealth.com"
  requires:
    - "mcp__fellow__search_meetings"
    - "mcp__fellow__get_meeting_summary"
    - "mcp__fellow__get_meeting_transcript"
    - "mcp__fellow__get_meeting_participants"
    - "mcp__google-workspace__import_to_google_doc"
    - "mcp__google-workspace__get_drive_shareable_link"
---

# MOM Writer

Turns one named Fellow.app meeting into a MOM, written straight into a new
Google Doc. Fixed template, three extraction targets — no variants, no
sheet, no local file.

## When to use

Only when Divy explicitly names or points to a specific meeting — by title,
date, participant names, or a Fellow link/ID — and wants the MOM as a
Google Doc. Never proactively scan Fellow, never run on more than one
meeting per invocation.

| Instead of mom-writer | Do this |
|---|---|
| Divy wants it logged in the MOM Tracker sheet / saved as a local `.md` too | Use `mom-tracker` instead (or in addition) |
| No Fellow recording/notes exist for the meeting | Write the MOM directly from what you're told — nothing to fetch |
| Just wants a quick verbal summary, no doc needed | Pull `get_meeting_summary` and answer directly — don't invoke the skill |
| Bulk-processing many past meetings | Not supported — name each meeting individually, one pass per meeting |

## Workflow (run in order)

1. **Resolve the meeting.** If Divy gave a `meeting_id`/`note_id` directly,
   use it. Otherwise use `search_meetings` (title/participants/date) to
   confirm the exact meeting — if more than one candidate matches, ask
   rather than guessing.

2. **Pull the transcript.** Start with `get_meeting_summary` for a fast
   overview. Then pull `get_meeting_transcript` in 300–3600s chunks for the
   sections that matter — this skill needs actual reasoning and phrasing,
   not just chapter titles, so lean on the transcript more than a
   summary-only pass. `get_meeting_participants` gives the attendee list for
   the Reference section and helps attribute who's speaking.

3. **Extract exactly three things** — don't add other sections, and write
   each row with real depth, not a one-line paraphrase of what was said:
   - **Questions & why**: capture the *sharpest* version of each question,
     not its polite surface wording. If the real question underneath is
     more uncomfortable than how it was phrased out loud (e.g. the actual
     question behind "is our tool credible?" is "why should anyone believe
     our output over a broker or a WhatsApp group?"), write that sharper
     version. When one dominant voice is exploring a problem space with many
     exploratory questions, name the theme each one belongs to in the Why
     column (e.g. "market structure," "trust/credibility," "distribution")
     instead of forcing a flat unrelated list — the theme is often more
     useful than the literal quote.
   - **Perspective & reasoning**: for whoever is explaining a concept or
     their thinking, decode the mental model behind each belief — don't
     transcribe it. Ask what incentive, prior experience, or unstated
     priority makes them frame it this way. Look for a throughline phrase
     they keep returning to (e.g. "math is cheap, trust is expensive") and
     use it as the frame for that row. Each row should read like a decoded
     insight ("they're optimizing for X because Y"), not a restatement of
     their sentence.
   - **Action items**: the concrete ask, who owns it, and the steps to
     execute it — not just a one-line to-do.

   Write plainly throughout — state conclusions bluntly, no
   motivational-poster language, no inflated closers.

4. **Draft the MOM** using the fixed template below. Omit a section
   entirely if that meeting genuinely had nothing for it (e.g. no one was
   explaining a concept) — don't leave an empty table.

   ```
   # <Meeting Title> — MOM (<YYYY-MM-DD>)

   <1-2 sentence overview: who, what kind of meeting, what it covered — if
   one blunt core premise/belief drove the whole conversation, lead with
   that instead of a generic summary>

   ## Perspective & Reasoning
   | Who | Concept / point | Their reasoning (why they frame it this way) |
   |---|---|---|

   ## Questions & Why
   | Question | Asked by | Why it came up |
   |---|---|---|

   ## Action Items
   | Action | Owner | Steps |
   |---|---|---|

   ## Reference
   - Meeting: Fellow note_id `<id>` / meeting_id `<id>`
   - Attendees: <names>
   ```

5. **Create the Google Doc directly** — one call, no separate doc-creation
   step: `import_to_google_doc` with `content` set to the markdown above,
   `file_name` set to `<Meeting Title> — MOM (<YYYY-MM-DD>)`, and
   `user_google_email` = `divy.sharma@coherehealth.com` (see frontmatter)
   unless Divy says otherwise. Drive's markdown conversion preserves the
   headings/tables/bold automatically.

6. **Hand back the link.** Use `get_drive_shareable_link` on the returned
   file ID and give Divy the Doc URL plus a one-line summary of what's in
   it (counts of questions / perspectives / action items found).

## Notes

- One meeting per run. If Divy asks for several, treat each as its own pass
  through steps 1–6.
- This skill never writes to the MOM Tracker sheet or a local file — that's
  `mom-tracker`'s job. If Divy wants both, run `mom-tracker` too.
- Permission prompts on first use of any Fellow transcript tool or the
  `google-workspace` doc-import tool are expected.
