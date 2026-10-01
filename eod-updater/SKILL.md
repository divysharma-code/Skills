---
name: eod-updater
description: Post a one-sentence automated EOD status comment on every Jira ticket in a Cohere Intake team's (Ibex, Aries, or Cabra) active sprint that changed status on a given day, defaulting to the last working day so it can be run each morning for yesterday. Pulls the day's status changes from Jira, context from that team's Fellow standup and sprint-planning recordings, the Confluence release doc to catch tickets that shipped to prod without a status change, and Slack when a Slack tool is connected (skipped and flagged when it isn't). Use when the user says "run EOD updater", "post EOD updates", "EOD status", or "update tickets for yesterday".
---

# EOD Jira Status Updater

Each morning: for one team, find the tickets whose status changed on the report day
(default: last working day), and leave a single-sentence 🤖 comment on each saying what
moved, why, and what is next.

## What it needs

| Need | Status | If missing |
|---|---|---|
| `~/.config/jira/credentials.env` (JIRA_EMAIL, JIRA_API_TOKEN, JIRA_BASE_URL) | **Required** | Stop and say so. Nothing works without it. |
| Fellow MCP (standup summaries) | Optional | Comment is built from Jira signals alone; say "no standup context" in the report. |
| Slack tool | Optional, **not connected in most sessions** | Skip it, and tell the user Slack was not checked. Never guess at Slack content. |

Everything else (Confluence release docs) reuses the same Jira credentials. No extra install.

## Teams

Source of truth is the "Team Intake" sheet
(`1PccUHP7x4qpaMdxLJKRWTOYldEyGyDVoENYKDDGT5Wc`). Ask which team if the user didn't say;
Divy's own team is **Ibex**.

| Team | Project / board | Fellow meeting titles | Slack channels (name, ID) |
|---|---|---|---|
| Ibex | ICS / 7962 | `ICS - Ibex - Standup`, `ICS - Ibex - Sprint Planning` | #intake-india-devs C0B5WRT5BUP, #aries-squad C05FXA0LSCD, #intake-application-engineering C09U39422AV, #intake-application-pdde-internal C09TQBM0KMY, #intake-application-pdde C02DX2DR324 |
| Aries | IPS / 192 | `IPE - Aries standup`, `IPE - Aries - Sprint Planning` | #aries-squad C05FXA0LSCD, #aries-squad-dev-chat C05GKNNQFCN, plus the three shared channels above |
| Cabra | COH / 43 | `IPE - Cabra standup`, `COH - Cabra Sprint Planning` | #cabrasquad-dev-chat C05GQ2Q0DAP, #cabra-squad C05FKMPM4NB, plus the three shared channels above |

Standups happen Mon, Tue, Wed, Fri. On other days updates are given in sprint planning,
so search both titles. Release docs live in Confluence space `ENG` and are titled like
`Intake Ibex Release YYYY-MM-DD` or `<Team> Release YYYY-MM-DD`.

## Procedure

### 1. Pick the report day

Default is the last working day (yesterday; Friday if today is Monday). The user can
name any date. Use it everywhere below as `DATE`.

### 2. Fetch the tickets

```bash
python3 scripts/eod.py fetch --team Ibex --date 2026-09-30
```

It prints, for each sub-task-free ticket in the team's active sprint(s) that changed status
on `DATE` (excluding "Ready for Dev"): key, summary, assignee, the transitions made that
day with times, the status **as of the end of DATE**, the current status, and any existing
🤖 EOD comment for `DATE`.

Use the status as of end of `DATE`, not the current one. A ticket that moved again the next
morning still gets the sentence that was true at EOD on `DATE`.

### 3. Check for a release that shipped that day

Search Confluence (ENG space) for a release doc dated `DATE` for the team. If the release
party thread or Fellow summary confirms it went to prod that day, every ticket key in the
doc's table is **Shipped to Prod**, even if Jira never left "Ready to Deploy". Add those keys
to the working set (the status-change query misses them). A ticket is Shipped only when it
is in the doc **and** the release is confirmed shipped that day. Do not infer that sub-tasks
shipped from a parent in the doc.

### 4. Gather context per ticket

- **Fellow:** get the meeting summary for `DATE` from the team's standup (then sprint
  planning). Pull only lines that mention the ticket key or its topic.
- **Jira comments** from `DATE` (PRs, Dev sign-offs, PO review results, test plans). This
  is often the richest source.
- **Slack:** only if a Slack tool is available, searched by ticket key in the team channels
  for `DATE`. Otherwise skip it and say so in the report.

### 5. Write one sentence per ticket

Format, exactly:

```
🤖 **EOD Status (YYYY-MM-DD):** <one sentence>
```

- One sentence. No bullets, no second paragraph.
- Say what moved, why, and what happens next (blocker, PR, who is waiting on whom).
- Use real details (test-plan step counts, PR numbers, config names), never invented ones.
- Zero em dashes. Use contractions where a person would. No "leverage", "seamless", "robust".
- Shipped tickets: `Shipped to prod in the <date> release, <owner>'s <what shipped> passed pre- and post-release validation (<one concrete detail>).`
- No standup or Slack context? Write it from the Jira transition and comments alone.

### 6. Show the drafts, then post

Show a table (Ticket | End-of-day status | Comment) and post. Posting is the whole point of
this skill, so do not ask again if the user already said to run it.

```bash
python3 scripts/eod.py post ICS-26 --date 2026-09-30 --text "<the sentence>"
```

The script skips a ticket that already has a 🤖 EOD comment for `DATE`; if one exists
(for example a ticket that then shipped later that day) pass `--update` to edit it in place
instead of adding a second.

### 7. Report back

The table of what was posted, plus one line on what was **not** checked (Slack, Fellow) so
the gap is visible, not silent.

## Rules

- Never post on sub-tasks or "Ready for Dev" tickets.
- Never duplicate an EOD comment for the same date.
- Never claim "shipped" without the release doc **and** a confirmed release.
- Never invent context. A thin sentence from Jira alone beats a confident guess.
