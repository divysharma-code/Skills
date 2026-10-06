#!/usr/bin/env python3
"""Sweep a team's active sprint for EOD context. Standard library only.

Lists every non-sub-task, non-"Ready for Dev" ticket in the active sprint, split into
ACTIVE (moved or got a human comment on the day) and QUIET (no Jira activity that day).
Reuses eod-updater's eod.py for credentials, API calls, the team table and time zone.
"""

import argparse
import datetime as dt
import importlib.util
import os
import sys
import urllib.parse

EOD_PATH = os.path.expanduser(os.environ.get("EOD_UPDATER_PATH", "~/.claude/skills/eod-updater/scripts/eod.py"))
if not os.path.exists(EOD_PATH):
    sys.exit(f"eod-updater not found at {EOD_PATH}. Install the eod-updater skill first.")
_spec = importlib.util.spec_from_file_location("eod", EOD_PATH)
eod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(eod)

JIRA_TS = "%Y-%m-%dT%H:%M:%S.%f%z"


def text(n):
    if isinstance(n, list):
        return "".join(text(x) for x in n)
    if not isinstance(n, dict):
        return ""
    t = n.get("type")
    if t == "text":
        return n.get("text", "")
    if t == "mention":
        return n.get("attrs", {}).get("text", "@someone")
    if t == "inlineCard":
        return n.get("attrs", {}).get("url", "")
    if t == "hardBreak":
        return " "
    inner = text(n.get("content", []))
    return inner + " " if t in ("paragraph", "listItem", "heading", "tableCell", "tableHeader") else inner


def day_comments(c, key, date, tz):
    """Comments created on `date`, oldest first. Newest-first paging, so long threads are covered."""
    out, start = [], 0
    while True:
        r = eod.call(c, "GET", f"/rest/api/3/issue/{key}/comment?orderBy=-created&startAt={start}&maxResults=100")
        batch = r.get("comments", [])
        for x in batch:
            when = dt.datetime.strptime(x["created"], JIRA_TS).astimezone(tz)
            if when.date() < date:
                return sorted(out)
            if when.date() == date:
                out.append((when, x["author"]["displayName"], " ".join(text(x["body"]).split())))
        start += len(batch)
        if not batch or start >= r.get("total", 0):
            return sorted(out)


def active_sprint_tickets(c, team, ids):
    jql = (
        f'project = {team["project"]} AND sprint in ({ids}) '
        f'AND status != "Ready for Dev" AND issuetype != Sub-task ORDER BY key'
    )
    issues, token = [], None
    while True:
        params = {"jql": jql, "fields": "summary,status,assignee,issuetype,updated", "maxResults": 100}
        if token:
            params["nextPageToken"] = token
        r = eod.call(c, "GET", "/rest/api/3/search/jql?" + urllib.parse.urlencode(params))
        issues += r.get("issues", [])
        token = r.get("nextPageToken")
        if not token or r.get("isLast", True):
            return issues


def main():
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("--team", required=True, help="ibex | aries | cabra")
    p.add_argument("--date", help="YYYY-MM-DD, US Eastern day (default: last working day)")
    a = p.parse_args()

    team = eod.TEAMS.get(a.team.lower())
    if not team:
        sys.exit(f"Unknown team '{a.team}'. Choose from: {', '.join(eod.TEAMS)}")
    c = eod.creds()
    tz = eod.REPORT_TZ
    date = dt.date.fromisoformat(a.date) if a.date else eod.last_working_day()
    day_start = dt.datetime.combine(date, dt.time(0), tz)

    sprints = eod.call(c, "GET", f"/rest/agile/1.0/board/{team['board']}/sprint?state=active")["values"]
    sprints = [s for s in sprints if s.get("originBoardId") == team["board"]]
    if not sprints:
        sys.exit(f"No active sprint found for {a.team} (board {team['board']}).")
    issues = active_sprint_tickets(c, team, ",".join(str(s["id"]) for s in sprints))
    print(f"Team {a.team} | sprint(s): {', '.join(s['name'] for s in sprints)} | report day {date} [times in {tz.key}]")
    print(f"{len(issues)} tickets (sub-tasks and Ready for Dev excluded)")

    active, quiet = [], []
    for i in issues:
        key, f = i["key"], i["fields"]
        head = f"{key} | {f['issuetype']['name']} | {(f.get('assignee') or {}).get('displayName')} | {f['summary']}"
        updated = dt.datetime.strptime(f["updated"], JIRA_TS).astimezone(tz)
        if updated < day_start:
            quiet.append(f"{head} | status: {f['status']['name']}")
            continue
        moves = eod.status_moves(c, key, tz)
        day_moves = [m for m in moves if m[0].date() == date]
        upto = [m for m in moves if m[0].date() <= date]
        eod_status = upto[-1][2] if upto else (moves[0][1] if moves else f["status"]["name"])
        comments = day_comments(c, key, date, tz)
        existing = eod.eod_comments(c, key, date)
        human = [x for x in comments if "\U0001F916" not in x[2]]
        if not day_moves and not human:
            quiet.append(f"{head} | status: {eod_status}" + (" | EOD comment already exists" if existing else ""))
            continue
        lines = [head, f"  status at end of {date}: {eod_status} (now: {f['status']['name']})"]
        lines += [f"  {t:%H:%M}  {frm} -> {to}" for t, frm, to in day_moves]
        lines += [f"  comment {t:%H:%M} {who}: {body[:700]}" for t, who, body in human]
        if existing:
            lines.append("  EOD comment already exists (post with --update to edit)")
        active.append("\n".join(lines))

    print(f"\n== ACTIVE: moved or human-commented on {date} ({len(active)}) ==")
    print("\n\n".join(active) or "none")
    print(f"\n== QUIET: no Jira activity on {date} ({len(quiet)}), check Fellow and Slack for these ==")
    print("\n".join(quiet) or "none")


if __name__ == "__main__":
    main()
