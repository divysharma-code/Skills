---
name: eod-context-updater
description: Post a one-sentence EOD status comment on every ticket in a Cohere Intake squad's (Ibex, Aries, Cabra) active sprint that had real activity on a day, built from Slack channel threads, the squad's standup and grooming/sprint-planning calls in Fellow, and Jira comments. A wrapper on eod-updater, so it keeps all of that skill's rules, format and duplicate protection, but also covers tickets that were discussed without a status change. Use when the user says "run EOD with context", "update every ticket from standup and Slack", "EOD from Slack and Fellow", or wants the full-context version of the EOD updater.
version: 1.0.0
author: Divy Sharma
license: MIT
metadata:
  requires:
    - "eod-updater skill installed (supplies credentials, team table, posting)"
    - "mcp__fellow__search_meetings, get_meeting_summary, get_meeting_transcript"
    - "mcp__slack-mcp-dev__slack_search_messages, slack_get_thread_replies, slack_get_users"
---

# EOD Context Updater

Wrapper on `eod-updater`. Read that skill's SKILL.md first. Everything in it still applies:
comment format, one sentence, zero em dashes, no sub-tasks or "Ready for Dev", no duplicate
for a date, "Shipped" only with release doc plus confirmed release, never invent context,
US Eastern day, honest report of what wasn't checked. This skill only changes **where the
evidence comes from** and **which tickets qualify**.

## What it needs

| Need | Status | If missing |
|---|---|---|
| `eod-updater` at `~/.claude/skills/eod-updater/` | Required | Stop. Say to install it. |
| Fellow MCP | Optional | Say "no standup/grooming context"; Jira-only sentences. |
| Slack MCP (`slack-mcp-dev`) | Optional | Say "Slack not checked". Auth error: user runs `/mcp`, no reconfigure. |

## Which tickets qualify

`eod-updater` comments only on tickets that changed status. This skill also comments on a
ticket with **no move** if the day has evidence for it: a human Jira comment, a Fellow
mention, or a Slack thread. A ticket with none of these gets nothing. Never write "no
update" filler.

## Procedure

1. **Team and day.** Team from the user, else ask. Day = last working day or the date given
   (pass `--date` explicitly if running from India before US midnight). Team table lives in
   `eod-updater`.
2. **Sweep Jira.** `python3 scripts/sweep.py --team Ibex --date YYYY-MM-DD` lists ACTIVE
   tickets (moved or human-commented that day, with the day's comments) and QUIET tickets.
3. **Read Fellow.** Search the team's standup and sprint-planning/grooming titles for the
   day (`search_meetings` with title and from/to date). Use `get_meeting_summary` first, then
   `get_meeting_transcript` in 300-3600s windows only around a ticket key or topic. Standups
   run Mon, Tue, Wed, Fri, so check both meeting titles.
4. **Read Slack.** For each ticket key, `slack_search_messages` with `in_channel` set to the
   team's channels and `after_date` / `before_date` around the day. Open hits with
   `slack_get_thread_replies`. Names come back as user IDs, resolve with `slack_get_users`.
   Team channels only. Never read DMs or other channels.
5. **Release check.** Same as `eod-updater` step 3: ENG release doc dated that day, plus a
   confirmed ship. Add those keys to the set.
6. **Match evidence to tickets.** Match on ticket key first, then clear topic words. A topic
   match you're unsure of is dropped, not guessed. Prefer Jira comments, then Fellow, then Slack.
7. **Write one line per ticket**, in `eod-updater`'s exact format:
   `🤖 **EOD Status (YYYY-MM-DD):** <one sentence>`. What moved or was decided, why, what's next.
   Real details only (PR numbers, steps, config names). A line from a Slack/Fellow source
   states the fact, not "someone said in Slack". Shape it with the SUCCESs pass in [REFERENCE.md](REFERENCE.md).
8. **Show the table, then post.** Table: Ticket | Evidence used (Jira/Fellow/Slack) | Comment.
   Posting is the point of the skill, so don't re-ask if the user said to run it. If a
   comment relies on a single Slack message or one-line transcript snippet, mark it
   "single source" in the table and let the user veto before posting.
   Post with `python3 ~/.claude/skills/eod-updater/scripts/eod.py post <KEY> --date <DATE> --text "<sentence>"`
   (add `--update` to replace an existing one).
9. **Report.** Counts posted / skipped (already had one) / no evidence, plus one line on
   what wasn't checked (Slack, Fellow, release doc).

## Writing the sentence

Run every draft through the SUCCESs pass and the language pass in
[REFERENCE.md](REFERENCE.md). The line stays one sentence in `eod-updater`'s format.

## Rules specific to this skill

- Slack and Fellow content goes into a **company Jira ticket**: work facts only. No PHI,
  member names, credentials, personal remarks, or anything from a private channel.
- Quote nothing. Paraphrase into one sentence.
- A disagreement between sources (Jira says Done, standup says still testing) is stated as
  the Jira fact, and flagged to the user in the report, not smoothed over.
- Never post a sentence you couldn't point to a source for.
