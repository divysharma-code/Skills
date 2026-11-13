---
name: daily-pm-task-list
description: Build Divy's daily task list for Intake product work, one action-verb line per task, from Jira PO Review queues, squad standup and grooming notes in Fellow, Slack mentions and DMs, Gmail, and Confluence. Use when Divy asks "what are my tasks today", "daily task list", "what's on my plate", "PO list for today", or "what do I need to finish".
---

# Daily PM Task List

Produces one short list of things Divy needs to finish today. Read-only: it never posts to Slack, Jira, Confluence, or email. It drafts; Divy decides what to send.

## Output format (follow exactly)

Group by section, in this order. Skip a section if it is empty.

1. **PO reviews** (PO = product owner review, Divy's approval before a ticket ships), split by squad: Cabra, Aries, Ibex
2. **Docs and release notes**
3. **Sessions** (KT = knowledge transfer, PO = product owner review sessions)
4. **Squad work**: grooming notes, next steps, scoping, due dates
5. **PPP** (Progress, Problems and Plans, Divy's weekly update)
6. **Still open from earlier** (anything from Slack or email not yet in Jira)
7. **Dropped** (asks that are stale, with the reason)

Rules for every line (speed-read style: plain English a newcomer gets on the first read):
- One line. Starts with an action verb: Review, Write, Merge, Add, Set, Scope, Schedule, Plan, Draft, Send, Post, Update, Confirm, Close, Book.
- Says what to finish and, in a few words, why it matters or who is waiting. Good: "Review IPS-2847 and send Paridhi the tiny release note she asked for." Bad: "IPS-2847 is in PO review."
- Ends with a short reference in brackets: ticket key or doc name.
- No em dashes, no filler ("leverage", "seamless"). No jargon without a short expansion on first use.
- Don't add facts that aren't in the sources. If something is unclear, write "confirm X" as the task instead of guessing.
- If a ticket is already Done or has moved past the step, put it under **Dropped** with the new status. Do not list it as a task.
- Max about 25 lines total.

After the list, add a glossary only for terms that appear in it. Expand every acronym once.

## Steps

Run these in parallel where possible.

1. **Jira PO Review queue.** Use the Atlassian MCP (`mcp__atlassian__searchJiraIssuesUsingJql`, `cloudId` = `coherehealth.atlassian.net`).
   - JQL: `project in (COH, IPS, ICS) AND status = "PO Review" ORDER BY project, updated DESC`
   - Squad map: COH = Cabra, IPS = Aries, ICS = Ibex.
   - Fields: summary, assignee, status, updated, duedate.
   - The status is exactly `PO Review`.
2. **Ibex sprint.** JQL: `project = ICS AND sprint in openSprints() AND statusCategory != Done`. Flag Divy's tickets with no due date.
3. **Fellow squad calls, last two working days.** Use `mcp__fellow__search_meetings` with titles "IPE - Cabra standup", "IPE - Cabra grooming", "IPE - Aries standup", "ICS - Ibex - Standup". Read `action_items` and `decisions` from `get_meeting_summary`. Keep items assigned to Divy Sharma and anything he said he would do.
4. **Slack.** Get your own user ID from `mcp__slack-mcp-dev__slack_check_auth`, then run `slack_search_messages` with query `<@YOUR_ID>` and `after_date` = 3d. Also check DMs: `slack_get_channels` with `types=im,mpim`. For each ask to Divy, check the linked Jira ticket status before listing it.
   - Do not use the broad `<@` query. It returns other people's mentions.
   - `mcp__slack-mcp-dev__` is the working server. The prod `slack` server may fail to connect.
5. **Gmail.** Search the last 14 days for asks that mention a ticket key, a client name, or a doc named in Fellow or Slack. Use `mcp__google-workspace__search_gmail_messages` with your own work email as `user_google_email`. Open only the threads that match an ask.
6. **Confluence.** Search by title for any doc named in an ask (`mcp__atlassian__searchConfluenceUsingCql`). Note duplicates, for example two pages on the same feature.
7. **Build the list.** Apply the format rules. Move anything already Done or past its step to **Dropped**.

## Gotchas

- Use the Atlassian MCP for Jira, not curl with the token in `~/.config/jira/credentials.env`. The token can expire and curl then returns an empty result or 401 instead of an error you can see.
- A JQL query that returns zero issues may mean a wrong status name, not an empty queue. Check the project's real status names before reporting "nothing in PO Review".
- Statuses after PO Review (for example Ready to Deploy) mean the PO ask is done. List those under Dropped.
- If a person is named in an ask (a handoff, a doc owner), take the name from the source and don't assume it from an older run.
- If the Slack server fails to connect, say so and build the list from Jira, Fellow and Gmail.

## Example line

`Merge the two Temp ID pages into one so MMO gets a single doc. [Confluence "Temp ID Scalability"]`

## Reference

- Squads and boards: Cabra = COH, Aries = IPS, Ibex = ICS (Jira project keys).
- Fellow meeting titles: "IPE - Cabra standup", "IPE - Cabra grooming", "IPE - Aries standup", "ICS - Ibex - Standup".
- Your own tickets: add `AND assignee = currentUser()` to any JQL.
- The PPP itself is built by the `ppp-updater` skill. This skill only lists the PPP tasks.
