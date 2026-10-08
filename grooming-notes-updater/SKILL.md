---
name: grooming-notes-updater
description: Post one short grooming-notes comment on every Jira ticket discussed on a Cohere Intake squad's (Ibex, Aries, Cabra) latest grooming call in Fellow, saying where the ticket landed, what the call changed, and who owns what's still open. Finds the discussed tickets from the call and from Jira (story points set or status moved during the call), confirms the ticket mapping before posting, and never duplicates a comment. Use when the user says "run grooming notes", "post grooming notes", "update grooming tickets", or "grooming notes for Cabra / Aries / Ibex".
version: 2.0.0
author: Divy Sharma
license: MIT
metadata:
  requires:
    - "~/.config/jira/credentials.env (JIRA_EMAIL, JIRA_API_TOKEN, JIRA_BASE_URL)"
    - "mcp__fellow__search_meetings, get_meeting_summary, get_meeting_transcript, get_meeting_participants"
---

# Grooming Notes Updater

After a squad's grooming call, leave one short 📝 comment on each ticket the call discussed:
where the ticket landed, what the call changed, why the estimate is what it is, and who owns
what's still open. Someone opening the ticket next week should get the call in 15 seconds.

The notes come from two places:
- **Fellow**: the grooming call's summary, plus the transcript around a ticket when needed
- **Jira**: which tickets got pointed or moved during the call, and their committed story points

This skill is self-contained. Nothing else needs to be installed except the Jira credentials.

## How it works

```text
 Fellow call ──► topics + ticket numbers ─┐
                                           ├──► match topic to ticket ──► you confirm ──► one comment each ──► post
 Jira ────────► pointed / moved in call ──┘                               (the gate)     (MOM + SUCCESs pass)
```

| Source | What it gives | How it's read |
|---|---|---|
| Fellow summary | Topics, key points, decisions, action items, recording link | `get_meeting_summary` |
| Fellow transcript | The reasoning behind a decision or estimate | `get_meeting_transcript`, only around one topic |
| Jira changelog | Tickets pointed or moved out of grooming during the call | `scripts/grooming_notes.py agenda` |
| Jira fields | Committed story points, summary, description | Same script |

## When to Use

- right after a squad's grooming call, for every ticket it covered
- a grooming call was missed and the tickets still need notes (name the date)
- a ticket was regroomed and its notes need updating (your own comment only)

## When NOT to Use

| Instead of this skill | Use |
|---|---|
| Daily status on sprint tickets | `eod-context-updater` |
| Full minutes for the whole call | `mom-writer` or `mom-tracker` |
| Writing or refining the ticket itself | `jira-ticket-writer` |
| The call wasn't recorded | Write the note by hand. There's nothing to read. |

## What it needs

| Need | Status | If missing |
|---|---|---|
| `~/.config/jira/credentials.env` | Required | Stop and say so. |
| Fellow MCP | Required | Stop. The call is the whole input. |
| Transcript access | Optional | Write from the summary alone and say "summary only" in the report. |

## Squads

Source of truth is the "Team Intake - Grooming Notes Config" sheet
(`1PWFoEgiVO8pFOIBgMtI653gDqjBnPDuuzeclt-cSlvg`). Re-read it at run time, since it may change.
Ask which squad if the user didn't say. Divy's own squad is **Ibex**.

| Squad | Fellow meeting title | Projects to search | Grooming status (use literally) |
|---|---|---|---|
| Cabra | `IPE - Cabra grooming` | COH | `Ready for / In Grooming` |
| Aries | `IPE - Aries Grooming` | IPS | `Ready for / In Grooming` |
| Ibex | `ICS - Ibex - Grooming` | ICS, IPS | ICS `Ready for Grooming`, IPS `Ready for / In Grooming` |

Three things the original version of this skill got wrong, checked against real calls:
- **Ibex grooms IPS tickets too.** The 2026-10-06 Ibex call covered IPS-2851 and IPS-2854, so
  search both projects.
- **Cabra's grooming status is a parking lot.** About 50 COH tickets sit in it, and the ones
  Cabra actually groomed (COH-8456, COH-8458) were in "To Do". The grooming status is a weak
  signal for Cabra. Story points set during the call are the strong one.
- **Calls say bare numbers.** Fellow writes "Ticket 8456", not "COH-8456". The script adds the
  project prefix.

## Workflow

### 1. Find the call

Use `search_meetings` with the squad's title and a 14-day window, and take the latest, or the
date the user names. Results are large, so keep only `meeting_id`, `note_id`, `start_time` and
`end_time`. If no call is found, say so and stop.

The grooming date (`DATE`) is the call's date in **US Eastern time**. A 23:00 India call is
13:30 Eastern the same day.

### 2. Read the summary

Run `get_meeting_summary` and keep:
- `meeting_link`: the recording link for every comment
- `chapters`: one per topic, with `[MM:SS]` key points
- `decisions` and `suggested_action_items` (with assignees)
- every ticket number said in the call

### 3. Build the ticket list

```bash
python3 scripts/grooming_notes.py agenda --team cabra \
  --start <start_time> --end <end_time> --keys 8456,8458
```

Pass the call's `start_time`/`end_time` exactly as Fellow returns them, and every number from
step 2 in `--keys`. The script prints two lists:
- **STRONG**: named in the call, or story points were set, or the ticket moved out of grooming
  during the call (with times, points changes and a description snippet). These are almost
  always the right tickets.
- **AGENDA ONLY**: in the grooming status that day, but nothing changed. Use these only to match
  a topic STRONG doesn't cover, such as a ticket the call deferred.

Any ticket marked **ALREADY POSTED** has a 📝 comment for `DATE` already. Leave it out of the
plan. Another person's comment is never edited.

### 4. Match topics to tickets

For each chapter, match on ticket number first, then on concepts in the summary and description.
Topic titles rarely match ticket summaries word for word. One topic can map to two tickets, such
as a spike and its story. Process chatter (meeting times, who joins the call) maps to no ticket.

### 5. Confirm before posting

Show the plan and wait for an answer. A wrong match puts notes on the wrong ticket.

| Topic (from the call) | Ticket | Points | Confidence | Note |
|---|---|---|---|---|
| Imported requests tab and config | COH-8456 | 3 in Jira, 5 said in call | High | Points mismatch |
| Header read-only expanded view | COH-8458 | 5 | High | |
| Sprint logistics | none | | | Skipped, process only |

Only post to the rows the user confirms. If they already said "post them", still show this
table: the gate is the point of this step.

### 6. Read deeper where needed

The summary gives what was said. The MOM-style notes need why. For a topic with a decision, a
re-estimate or a disagreement, pull `get_meeting_transcript` around its `[MM:SS]` markers, in a 5
to 10 minute window. Skip it for routine topics. Never read the whole call.

### 7. Write the comment

Exact format:

```text
📝 **Grooming notes (YYYY-MM-DD):**
- **Verdict:** <where it landed>, <points> points.
- **Changed in the call:** <what's different from the ticket as written>
- **Why <points>:** <what drives the size or the risk>
- **Open:** <question or action>. Owner: <name>.
🎥 Recording
```

Only the Verdict line is required. Add the others only when the call gave them something real.
A routine ticket gets one line and stops. That's 1 to 5 bullets, each one line, 280 characters
at most.

| Line | What goes in it |
|---|---|
| **Verdict** | Where the ticket landed (ready to build, needs tasking, split, merged into another ticket, blocked on X, deferred) plus the points from the Jira field. |
| **Changed in the call** | Scope cut or added, a decided behavior, an edge case the description misses. The thing an engineer would get wrong from the ticket alone. |
| **Why N** | The reason for the size or the risk, decoded from the discussion. "5 because the card component may need refactoring" beats "pointed at 5". |
| **Open** | An unresolved question or an action, with a named owner. A guess ends in a question mark. |

**Story points.** Use the Jira Story Points field (`customfield_10024`). If the call agreed on a
different number than the field shows, don't post either one: flag it in the step 5 table and
let the user fix the ticket first. If the field is empty, leave the points out.

Run each draft through the two passes below before posting.

#### MOM pass (from mom-writer)

| Rule | For one ticket's notes |
|---|---|
| **Sharpest version** | Write the real decision, not the polite surface. "Frontend only, no API calls until the data team ships domain models" beats "discussed scope". |
| **Decode the why** | When someone argued for a choice, keep the reason: "5, not 3, so the sprint gets pulled down rather than overrun". |
| **Asks have owners** | Every action names an owner. Use `suggested_action_items` assignees, then `get_meeting_participants`. |
| **Omit empty lines** | No line for the sake of the format. |

#### SUCCESs pass (from Made to Stick)

A checklist, not a template. Never pad a note to hit all six.

| Principle | For a grooming note | Check |
|---|---|---|
| **Simple** | The Verdict line alone says where the ticket stands. | Could a reader stop after line one? |
| **Unexpected** | Lead "Changed in the call" with what the ticket text doesn't say. | Is the surprise in there? |
| **Concrete** | Real names: the field, the screen, the config, the dependency. | Could an engineer act without the recording? |
| **Credible** | Every line traces to the summary or a transcript window you read. | Can you point to the timestamp? |
| **Emotional** | Only for a real blocker or go-live date. One plain clause. | Skipped if it's routine? |
| **Story** | Skip. There's no room in a five-line note. | Skipped. |

#### Language pass

Search for each pattern. Don't just eyeball it.

| Cut | Fix |
|---|---|
| Em dash `—` | Comma or period. The count must be 0 (`post` also rejects it). |
| "The team discussed", "It was noted that", "as discussed" | State the decision. |
| A bare transcript line ("Jeremy said this is complex") | Say what's complex and why. |
| leverage, streamline, robust, seamless, utilize, comprehensive | use, simplify, solid, works everywhere, use, full |
| "it is / does not / cannot" | "it's / doesn't / can't" |

### 8. Post

```bash
python3 scripts/grooming_notes.py post COH-8458 --date 2026-10-07 \
  --link https://fellow.link/RB6T7V8ETVEK \
  --line "**Verdict:** Ready to build, 5 points." \
  --line "**Changed in the call:** ..." \
  --line "**Open:** ... Owner: Vidhi."
```

One `--line` per bullet, and `**bold**` works. Add `--dry-run` to check a draft first.
The script builds the Jira comment with real bullets and a clickable Recording link. It skips a
ticket that already has notes for `DATE`, and with `--update` it edits only your own comment.

### 9. Report back

| Ticket | Verdict | Lines | Status |
|---|---|---|---|
| COH-8458 | Ready to build, 5 points | 3 | Posted |
| COH-8456 | | | Held, points mismatch |

Then give counts for posted, skipped (already had notes), held (mismatch or unconfirmed) and
topics with no ticket, plus "summary only" if no transcript was read.

## Rules

- Always confirm the topic-to-ticket mapping before posting.
- Search every project in the squad's row, and expand bare ticket numbers.
- Story points come from the Jira field. If it disagrees with the call, hold and flag.
- One comment per ticket per grooming date. Never edit someone else's.
- 1 to 5 one-line bullets, Verdict first, zero em dashes.
- Every note ends with the recording link, and the script adds it.
- Grooming content ends up in a company Jira ticket, so work facts only. No PHI, member names,
  credentials or personal remarks.
- Paraphrase. Never quote a person.
- Never create a ticket for an unmatched topic. List it in the report.

## Anti-Patterns

- dumping the chapter's key points as bullets (the old, 950-character style)
- posting the points said aloud instead of the Jira field
- trusting the grooming status alone for Cabra
- reading the full transcript of every call
- "The team discussed X" with no outcome
- an action item with no owner
- posting while a points mismatch is unresolved

## Related Skills

- `mom-writer`: where the sharpest-version and decode-the-why rules come from
- `slack-question-writer`: where the SUCCESs framework comes from
- `eod-context-updater`: the daily status sibling, same squads and Jira setup

## Example

Request:

```text
Run grooming notes for Cabra.
```

What happens with the 2026-10-07 Cabra call:
- the summary covers 3 topics and says "8456", "8457" and "8458"
- `agenda` returns those 3 as STRONG, out of 52 tickets in the grooming status
- the plan maps 8456 and 8458, skips sprint logistics, and flags COH-8456: 5 points agreed in the
  call, 3 in Jira
- COH-8458 gets:

```text
📝 Grooming notes (2026-10-07):
- Verdict: Ready to build, 5 points.
- Changed in the call: Imported requests are read-only. Hide integration, clinical review, continuation and letter sections, show only notifications (admins).
- Why 5: Most of the existing card is reused, but it hooks into SR edit config, and all edits must stay off without tangling a future historical-SR config.
- Open: Vidhi to add the historical SR config name to the ticket once it's final, for test planning.
🎥 Recording
```

The value isn't more notes. It's that each note says where the ticket landed and what the
ticket text alone won't tell you.

Credit: based on Paridhi Jain's original grooming-notes-updater (v1.0.0), extended for the Ibex,
Aries and Cabra squads.
