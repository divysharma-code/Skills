---
name: eod-context-updater
description: Post a one-sentence EOD status comment on every ticket in a Cohere Intake squad's (Ibex, Aries, Cabra) active sprint that had real activity on a day, built from Jira comments, the squad's standup and grooming calls in Fellow, and Slack threads. Use when the user says "run EOD", "run EOD with context", "post EOD updates", "EOD from Slack and Fellow", "update every ticket from standup and Slack", or "update tickets for yesterday".
version: 2.0.1
author: Divy Sharma
license: MIT
metadata:
  requires:
    - "~/.config/jira/credentials.env (JIRA_EMAIL, JIRA_API_TOKEN, JIRA_BASE_URL)"
    - "mcp__fellow__search_meetings, get_meeting_summary, get_meeting_transcript (optional)"
    - "mcp__slack-mcp-dev__slack_search_messages, slack_get_thread_replies, slack_get_users (optional)"
---

# EOD Context Updater

Each morning, for one squad, leave a single-sentence 🤖 comment on every sprint ticket that
had real activity the day before: what moved or was decided, why, and what happens next.

Evidence comes from four places, so a ticket that was discussed but never changed status
still gets its update:
- **Jira**: status moves and human comments for the day
- **Fellow**: the squad's standup and grooming (sprint planning) calls
- **Slack**: threads in the squad's channels
- **Confluence**: the release doc, to catch tickets that shipped without a status change

This skill is self-contained. Nothing else needs to be installed except the Jira credentials.

## How it works

```text
 Jira sweep ───┐
 Fellow calls ─┼──► match evidence to tickets ──► one SUCCESs sentence each ──► review table ──► post
 Slack threads ┤        (by ticket key)                                         (you can veto)
 Release doc ──┘
```

| Source | What it gives | How it's read |
|---|---|---|
| Jira | Status moves and comments for the day | `scripts/eod_context.py sweep` |
| Fellow | What was said in standup and grooming | Meeting summary first, transcript only around a ticket |
| Slack | Decisions and blockers in squad threads | Search by ticket key in the squad's channels |
| Confluence | Tickets that shipped to prod that day | Release doc in space `ENG`, plus a confirmed ship |

## When to Use

- the morning EOD run, covering every active ticket, not only the ones that moved
- a ticket was discussed in standup or Slack but its Jira status didn't change
- backfilling a missed day for one squad

## When NOT to Use

| Instead of this skill | Use |
|---|---|
| Drafting a question to someone on Slack | `slack-question-writer` |
| Writing up one full meeting | `mom-writer` or `mom-tracker` |
| A sign-off after manual testing | `dev-signoff-writer` |
| Commenting on sub-tasks or "Ready for Dev" tickets | Don't. This skill never does. |

## What it needs

| Need | Status | If missing |
|---|---|---|
| `~/.config/jira/credentials.env` | Required | Stop and say so. Nothing works without it. |
| Fellow MCP | Optional | Write from Jira alone and report "no standup or grooming context". |
| Slack MCP (`slack-mcp-dev`) | Optional | Report "Slack not checked". On an auth error, the user runs `/mcp`, no reconfigure. |

## Squads

Source of truth is the "Team Intake" sheet (`1PccUHP7x4qpaMdxLJKRWTOYldEyGyDVoENYKDDGT5Wc`).
Ask which squad if the user didn't say. Divy's own squad is **Ibex**.

| Squad | Project / board | Fellow meeting titles | Slack channels (name, ID) |
|---|---|---|---|
| Ibex | ICS / 7962 | `ICS - Ibex - Standup`, `ICS - Ibex - Sprint Planning` | #intake-india-devs C0B5WRT5BUP, #aries-squad C05FXA0LSCD |
| Aries | IPS / 192 | `IPE - Aries standup`, `IPE - Aries - Sprint Planning` | #aries-squad C05FXA0LSCD, #aries-squad-dev-chat C05GKNNQFCN |
| Cabra | COH / 43 | `IPE - Cabra standup`, `COH - Cabra Sprint Planning` | #cabrasquad-dev-chat C05GQ2Q0DAP, #cabra-squad C05FKMPM4NB |

All three squads also share #intake-application-engineering C09U39422AV,
#intake-application-pdde-internal C09TQBM0KMY and #intake-application-pdde C02DX2DR324.

Standups run Mon, Tue, Wed and Fri. On other days updates are given in sprint planning, so
search both titles. Release docs are in Confluence space `ENG`, titled like
`Intake Ibex Release YYYY-MM-DD` or `<Team> Release YYYY-MM-DD`.

## Workflow

### 1. Pick the squad and the day

The day is the last working day (Friday if today is Monday), or any date the user names.
Use it everywhere below as `DATE`.

Days are counted in **US Eastern time**, matching the team's existing 🤖 comments. A move at
9pm Eastern on the 1st belongs to the 1st, even though it is already the 2nd in India. The
script handles this. Pass `--date` explicitly when running from India before US midnight,
because the default "yesterday" is computed in Eastern time.

Someone else may already run this for the squad. The script skips any ticket that already
has a 🤖 comment for `DATE`, so running it twice never double-comments.

### 2. Sweep Jira

```bash
python3 scripts/eod_context.py sweep --team Ibex --date YYYY-MM-DD
```

It prints two lists for the squad's active sprint. **ACTIVE** tickets moved or got a human
comment that day, with the day's transitions, the status **as of the end of `DATE`**, and the
comments. **QUIET** tickets had no Jira activity, so check Fellow and Slack for them.

Use the end-of-day status, not the current one. A ticket that moved again the next morning
still gets the sentence that was true at EOD on `DATE`.

### 3. Read Fellow

Find the squad's standup and sprint-planning calls for `DATE` with `search_meetings` (title
plus date). Read `get_meeting_summary` first. Pull `get_meeting_transcript` only around a
ticket key or topic, in 5 to 60 minute windows. Check both meeting titles.

### 4. Read Slack

For each ticket key, run `slack_search_messages` in the squad's channels with `after_date` and
`before_date` around `DATE`. Open hits with `slack_get_thread_replies`. Names come back as
user IDs, so resolve them with `slack_get_users`. Squad channels only, never DMs or any other
channel.

### 5. Check for a release

Search Confluence (`ENG`) for a release doc dated `DATE` for the squad. If the release party
thread or the Fellow summary confirms it went to prod that day, every ticket key in the doc's
table is **Shipped to Prod**, even if Jira never left "Ready to Deploy". Add those keys to the
working set, since the sweep misses them.

A ticket is Shipped only when it is in the doc **and** the release is confirmed that day. Never
infer that sub-tasks shipped from a parent in the doc.

### 6. Match evidence to tickets

Match on ticket key first, then on clear topic words. Drop any topic match you're unsure of.
When sources overlap, trust Jira comments first, then Fellow, then Slack. A ticket with no
evidence gets no comment. Never write "no update" filler.

### 7. Write one sentence per ticket

The comment Jira shows is:

```text
🤖 **EOD Status (YYYY-MM-DD):** <one sentence>
```

The script adds the 🤖 and the bold `EOD Status (date):` header itself. Pass `--text` ONLY the
sentence, with no header, no 🤖, and no `**`. Passing the full line posts the header twice, the
second copy as literal asterisks.

- One sentence. No bullets, no second paragraph.
- Say what moved or was decided, why, and what happens next (blocker, PR, who is waiting on whom).
- Use real details (test-plan step counts, PR numbers, config names), never invented ones.
- State the fact, not where it came from. "Per Slack" and "as discussed in standup" are filler.
- Shipped tickets: `Shipped to prod in the <date> release, <owner>'s <what shipped> passed pre- and post-release validation (<one concrete detail>).`
- Thin evidence? Write it from the Jira transition and comments alone. A thin true sentence beats a confident guess.

Run each draft through the SUCCESs pass below, then the language pass.

#### SUCCESs pass (from Made to Stick)

A checklist, not a template. Never pad a line to hit all six, and never break the one-sentence
format to fit one.

| Principle | For one EOD sentence | Check |
|---|---|---|
| **Simple** | Open with what changed or was decided. The first few words alone should tell a reader the outcome. | Does it start with the outcome, not background? |
| **Unexpected** | If there's a blocker, surprise, or reversal, say it plainly. Quiet days don't need one. | Is the one thing that isn't routine in there? |
| **Concrete** | Name the real detail: PR number, step count, config key, who is waiting on whom. | Could a reader act on it without opening the ticket? |
| **Credible** | Every fact traces to a Jira comment, Fellow call or Slack thread you read. | Can you point to the source for each claim? |
| **Emotional** | Say what it unblocks or who is waiting. One plain clause, no hype. | Does the reader know why it matters? |
| **Story** | Skip. One sentence has no room for a before and after. | Skipped. |

#### Language pass

Search for each pattern. Don't just eyeball it.

| Cut | Fix |
|---|---|
| Em dash `—` | Comma or period. The count must be 0 (`post` also rejects it). |
| "Just wanted to flag", "FYI", "as discussed" | State the fact. |
| leverage, streamline, robust, seamless, utilize, comprehensive | use, simplify, solid, works everywhere, use, full |
| "it is / does not / cannot" | "it's / doesn't / can't" |

### 8. Show the table, then post

| Ticket | End-of-day status | Evidence | Comment |
|---|---|---|---|
| ICS-26 | Ready to Deploy | Jira, Fellow | 🤖 **EOD Status (...):** ... |

Mark any comment that rests on one Slack message or one transcript line as **single source**,
so the user can veto it. Posting is the point of this skill, so don't ask again if the user
already said to run it. Then post each one:

```bash
python3 scripts/eod_context.py post <KEY> --date <DATE> --text "<sentence>"
```

If a comment for `DATE` already exists (for example a ticket that then shipped later that day),
pass `--update` to edit it in place instead of adding a second.

### 9. Report back

Give counts for posted, skipped (already had one) and no evidence, plus one line on what
wasn't checked (Slack, Fellow or the release doc), so a gap is visible, not silent.

## Rules

- One sentence, zero em dashes, real contractions. No sub-tasks or "Ready for Dev" tickets.
- Never duplicate an EOD comment for the same date.
- Never claim "shipped" without the release doc **and** a confirmed release.
- Never invent context, and never post a sentence you can't point to a source for.
- Slack and Fellow content ends up in a company Jira ticket, so work facts only. No PHI,
  member names, credentials or personal remarks, and nothing from a private channel.
- Paraphrase. Never quote a person.
- If sources disagree (Jira says Done, standup says still testing), state the Jira fact and
  flag the conflict in the report.

## Anti-Patterns

- posting "no update today" on a quiet ticket
- guessing which ticket a vague Slack message was about
- reading the full transcript of every call instead of the parts about a ticket
- writing "per Slack" or "as discussed in standup" instead of the fact
- using the current status instead of the end-of-day status for `DATE`
- skipping the report line on what wasn't checked

## Related Skills

- `slack-question-writer`: where the SUCCESs framework comes from
- `mom-writer`: full minutes from one Fellow meeting
- `dev-signoff-writer`: a sign-off comment after manual testing

## Example

Request:

```text
Run EOD with context for Ibex for 2026-09-30.
```

Likely shape:
- the sweep finds 7 ACTIVE tickets (2 moved, 5 only had comments) and 4 QUIET ones
- Fellow and Slack add context to a few of the quiet ones, and the rest get nothing
- each comment is one sentence, for example ICS-26: "Moved to Ready to Deploy after PO
  review, with all 18 test-plan steps passing on frontend PR #21874; it now waits for the
  next release."

The value isn't more comments. It's that every comment is the one sentence a reader needs.

Credit: based on Paridhi Jain's original EOD updater, extended for the Ibex, Aries and Cabra squads.
