---
name: adhoc-grooming-notes-writer
description: Write and post grooming notes plus next steps from ONE ad hoc grooming call (a one-off call that is not a squad's regular grooming ceremony, for example a session where a dev lead walks the team through new tickets and points them live). Reads the call's Fellow recording, matches what was discussed to Jira tickets by topic (ad hoc calls rarely say ticket numbers), checks story points against the Jira field, shows a confirm-before-post table, posts one short 📝 comment per ticket, and lists the call-level next steps with owners. Use when Divy says "ad hoc grooming notes", "adhoc grooming call", "post notes from the call with <person>", "did we post notes from that grooming call", or points at a Fellow recording of a one-off grooming session.
version: 1.0.0
author: Divy Sharma
license: MIT
metadata:
  requires:
    - "grooming-notes-updater skill installed (this skill reuses its scripts/grooming_notes.py for the Jira search and the comment post)"
    - "~/.config/jira/credentials.env (JIRA_EMAIL, JIRA_API_TOKEN, JIRA_BASE_URL)"
    - "mcp__fellow__search_meetings, get_meeting_summary, get_meeting_transcript"
---

# Ad Hoc Grooming Notes Writer

After a one-off grooming call, leave one short 📝 comment on each ticket it covered (where the
ticket landed, what the call changed, what is still open) and hand back the call's next steps.

## Why this is a separate skill

`grooming-notes-updater` is built for a squad's **regular** grooming ceremony. An ad hoc call
breaks three of its assumptions:

| Regular grooming call | Ad hoc grooming call |
|---|---|
| Fixed Fellow title per squad, so the call is found by title | Any title, so the user names it or you search by date and participants |
| Tickets are said out loud ("ticket 8456") and sit in a grooming status | Tickets are shown on screen and talked about by topic, so numbers are rarely said |
| Summary chapters are reliable enough to work from | Short, mixed-purpose call (process chat, KT asks, side tickets), so the transcript is the source |
| Notes only | Notes **plus next steps** that belong to the call, not to one ticket |

## How it works

```text
 Fellow call ──► read summary + FULL transcript ──┐
                                                   ├──► match topic to ticket ──► you confirm ──► one comment each
 Jira (changes in the call window, points) ──────┘                               (the gate)       + call-level next steps
```

## What it needs

| Need | Status | If missing |
|---|---|---|
| `grooming-notes-updater` skill (its script) | Required | Stop and say to install it. This skill does not copy the script. |
| `~/.config/jira/credentials.env` | Required | Stop and say so. |
| Fellow MCP (Model Context Protocol, the connector that lets Claude read Fellow) | Required | Stop. The call is the whole input. |

Script path used below: `~/.claude/skills/grooming-notes-updater/scripts/grooming_notes.py`
(called `S` from here on).

## Workflow

### 1. Find the call

- User named it, or pasted a link: use that.
- Otherwise `search_meetings` over the last 7 days with `title` containing "grooming", plus a
  second search with no title if nothing fits (ad hoc calls are often titled "Adhoc grooming and
  check-in" or just the organizer's name). Keep only `meeting_id`, `note_id`, `title`,
  `start_time`, `end_time`, `meeting_link`.
- More than one candidate: list them and ask which one. Never guess.
- `DATE` = the call's date in **US Eastern time** (a 17:00 India call is 06:30 Eastern the same day).

### 2. Read the whole call

Ad hoc calls are short (20 to 45 minutes), so read all of it:

1. `get_meeting_summary` for the recording link, decisions and suggested action items.
2. `get_meeting_transcript` in 30-minute windows until the call is covered. The summary alone
   misses the details that matter (who reviews what, which testing trick, why a number).

Treat the summary as a map and the transcript as the source. Speech-to-text mangles names and
terms ("Octa" for Okta, "Century" for Sentry), so match names against Jira before trusting them.

### 3. List what the call covered

Make a short inventory from the transcript, one row per topic:

| Topic | Ticket shown on screen? | Pointed in the call? | Number said aloud |
|---|---|---|---|

Process chatter (sprint logistics, holidays, board closures) is **not** a ticket. It goes to
the call-level next steps in step 7.

### 4. Find the tickets in Jira

```bash
python3 $S agenda --projects <KEYS> --start <start_time> --end <end_time>
```

- `--projects`: the squad's project keys (Ibex = `ICS,IPS`, Aries = `IPS`, Cabra = `COH`). There
  is no `--team` here, since the call has no squad title.
- Add `--keys` only for numbers actually **said in the call**. The script labels anything passed
  in `--keys` as "named in call", so passing a guess makes a wrong ticket look confirmed.
- Read the output as evidence, by strength:

| Signal | Meaning |
|---|---|
| Points set or status moved to Ready for Dev **during** the call window | Strongest. The ticket was pointed live. |
| Matches a topic in your step 3 list by description | Strong. Say which words matched. |
| Moved or pointed **after** the call ended | Not this call. Leave it out. |
| Only passed in via `--keys` | No evidence. Don't count it. |

A ticket the call pointed but that Jira shows **no points** on (cleared, or never saved) is a
points mismatch. Hold it (step 5).

### 5. Confirm before posting

Show this table and wait. A wrong match puts notes on the wrong ticket, so the gate stays even if
the user already said "post them".

| Topic (from the call) | Ticket | Points (Jira field) | Matched by | Confidence | Note |
|---|---|---|---|---|---|
| Missing React keys cleanup | ICS-140 | 3 | Points set in call window, description match | High | |
| Provider facility required error | ICS-139 | empty | Topic only | Medium | Held, points missing |
| Sprint logistics | none | | | | Next step, not a ticket |

Rules for the Points column:
- Use the Jira **Story Points** field (`customfield_10024`).
- The call agreed a number but the field is empty or different: do not post either. Flag it and
  let the user fix the ticket, or tell you the number to use in the note.
- Field empty and the call gave no number: leave the points out of the Verdict line.

### 6. Write each ticket's comment

Exact format (the script adds the header and the Recording link):

```text
📝 Grooming notes (YYYY-MM-DD):
- Verdict: <where it landed>, <points> points.
- Changed in the call: <what the ticket text alone doesn't say>
- Why <points>: <what drives the size or the risk>
- Open: <question or action>. Owner: <name>.
🎥 Recording
```

Only Verdict is required. Add other lines only when the call gave something real. Max 5 bullets,
each one line, 280 characters.

Ad hoc-specific rules:

| Rule | Why |
|---|---|
| **Name an owner only if the call named one.** Otherwise write "whoever picks it up". | Tickets groomed ad hoc are often unassigned. A guessed owner is worse than none. |
| **Read the ticket's existing comments first.** If a call decision is already written there, link to it, don't repeat it. | Dev leads often leave the same instruction as a comment before the call. |
| **Carry testing guidance and review routing into the note.** | "Verify by watching the console" or "PO review goes to X, not the usual PO" is what a tester needs and the ticket rarely says. |
| **Say where the ticket will sit next** (sprint, backlog) only if the call decided it. | Backlog vs sprint is a decision, not a default. |
| Paraphrase, zero em dashes, real contractions, no PHI (protected health information), member names or personal remarks. | The comment lands in a company Jira ticket. |

Run the language pass from `grooming-notes-updater` (cut "the team discussed", em dashes, filler
words) before posting.

### 7. Next steps

Next steps come in two kinds:

| Kind | Where it goes |
|---|---|
| **Ticket-specific** (a question, a follow-up task, a review owner) | The ticket's `Open:` line, with its owner. |
| **Call-level** (send tickets to the lead, run a knowledge-transfer session, request tool access, board changes, "review my PR today") | A table in your report, not on any ticket. |

Call-level table, one row per action, each with the owner the call named and a source timestamp:

| Next step | Owner | Source |
|---|---|---|
| Share the recording with the delivery lead so they can pull groomed tickets in by capacity | Divy | [13:53] |

Post a call-level next step to Jira only if the user names the ticket (for example a parent
epic) to carry it. Never create a ticket for one.

### 8. Post

```bash
python3 $S post ICS-140 --date 2026-11-20 --link <meeting_link> --dry-run \
  --line "**Verdict:** Ready for Dev, 3 points." \
  --line "**Changed in the call:** ..."
```

Run with `--dry-run` first, show the output, then run without it for the confirmed rows. The
script skips a ticket that already has notes for `DATE`, and `--update` edits only your own
comment. If a regular grooming call the same day already put notes on the ticket, the script will
skip it: tell the user and offer `--update`.

### 9. Report back

| Ticket | Verdict | Status |
|---|---|---|
| ICS-140 | Ready for Dev, 3 points | Posted |
| ICS-139 | In Progress | Held, points missing |

Then: counts for posted, held, skipped (already had notes) and topics with no ticket, the
call-level next-steps table, and one line on anything unverified (for example "transcript read
0:00 to 27:00, full call").

## Rules

- Always confirm the topic-to-ticket mapping before posting.
- Read the full transcript. Never post from the summary alone.
- Never post points that disagree with the Jira field. Hold and flag.
- Never invent an owner. Use only people the call named.
- A ticket moved or pointed after the call's end time belongs to another event.
- One comment per ticket per date. Never edit someone else's.
- Never create tickets. List unmatched topics in the report.
- No PHI, member names, credentials or personal remarks in any comment.

## Anti-Patterns

- passing guessed ticket numbers in `--keys` so they show up as "named in call"
- trusting the summary's chapters and skipping the transcript
- assigning "Owner: <lead>" because they chaired the call
- putting call-level chores (KT sessions, access requests) on a random ticket
- re-stating a decision that is already in the ticket's own comments
- posting a points number the Jira field doesn't show

## Related Skills

- `grooming-notes-updater`: the regular-ceremony version, and the source of the script this skill calls
- `eod-context-updater`: daily status comments on the same squads' sprint tickets
- `mom-writer`: full minutes of a meeting when you want the whole call, not per-ticket notes
