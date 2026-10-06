#!/usr/bin/env python3
"""EOD context updater, Jira side. Standard library only, no other skill needed.

  sweep  List every non-sub-task, non-"Ready for Dev" ticket in a squad's active sprint,
         split into ACTIVE (moved or got a human comment that day) and QUIET (no Jira activity).
  post   Post (or update in place) the one-line EOD comment on a ticket.

Credentials: ~/.config/jira/credentials.env (JIRA_EMAIL, JIRA_API_TOKEN, JIRA_BASE_URL).
Days are counted in US Eastern time (set EOD_TZ to override).
"""

import argparse
import base64
import datetime as dt
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from zoneinfo import ZoneInfo

REPORT_TZ = ZoneInfo(os.environ.get("EOD_TZ", "America/New_York"))
JIRA_TS = "%Y-%m-%dT%H:%M:%S.%f%z"
ROBOT = "\U0001F916"

TEAMS = {
    "ibex": {"project": "ICS", "board": 7962},
    "aries": {"project": "IPS", "board": 192},
    "cabra": {"project": "COH", "board": 43},
}


def creds():
    path = os.path.expanduser("~/.config/jira/credentials.env")
    out = {}
    try:
        for line in open(path):
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, _, v = line.partition("=")
                out[k.strip()] = v.strip().strip("\"'")
    except FileNotFoundError:
        sys.exit(f"Missing {path}. Jira credentials are required.")
    for k in ("JIRA_EMAIL", "JIRA_API_TOKEN", "JIRA_BASE_URL"):
        if k not in out:
            sys.exit(f"{path} is missing {k}")
    return out


def call(c, method, path, body=None):
    auth = base64.b64encode(f"{c['JIRA_EMAIL']}:{c['JIRA_API_TOKEN']}".encode()).decode()
    req = urllib.request.Request(
        c["JIRA_BASE_URL"].rstrip("/") + path,
        data=json.dumps(body).encode() if body is not None else None,
        headers={"Authorization": f"Basic {auth}", "Content-Type": "application/json", "Accept": "application/json"},
        method=method,
    )
    try:
        with urllib.request.urlopen(req) as r:
            raw = r.read()
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as e:
        sys.exit(f"Jira {e.code} on {method} {path}: {e.read().decode(errors='replace')}")


def last_working_day():
    d = dt.datetime.now(REPORT_TZ).date() - dt.timedelta(days=1)
    while d.weekday() >= 5:
        d -= dt.timedelta(days=1)
    return d


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


def status_moves(c, key):
    """All status transitions as (Eastern datetime, from, to), oldest first, fully paginated."""
    out, start = [], 0
    while True:
        r = call(c, "GET", f"/rest/api/3/issue/{key}/changelog?startAt={start}&maxResults=100")
        for h in r.get("values", []):
            when = dt.datetime.strptime(h["created"], JIRA_TS).astimezone(REPORT_TZ)
            for it in h["items"]:
                if it["field"] == "status":
                    out.append((when, it["fromString"], it["toString"]))
        start += len(r.get("values", []))
        if r.get("isLast", True) or not r.get("values"):
            return sorted(out)


def comments_on(c, key, date):
    """Comments created on `date` (Eastern), oldest first. Pages newest-first so long threads are covered."""
    out, start = [], 0
    while True:
        r = call(c, "GET", f"/rest/api/3/issue/{key}/comment?orderBy=-created&startAt={start}&maxResults=100")
        batch = r.get("comments", [])
        for x in batch:
            when = dt.datetime.strptime(x["created"], JIRA_TS).astimezone(REPORT_TZ)
            if when.date() < date:
                return sorted(out, key=lambda o: o[0])
            if when.date() == date:
                out.append((when, x["author"]["displayName"], " ".join(text(x["body"]).split()), x["id"]))
        start += len(batch)
        if not batch or start >= r.get("total", 0):
            return sorted(out, key=lambda o: o[0])


def eod_comment(c, key, date):
    """Id of the 🤖 EOD comment for `date`, if any. Scans all comments: they are posted the next morning."""
    tag = f"EOD Status ({date})"
    start = 0
    while True:
        r = call(c, "GET", f"/rest/api/3/issue/{key}/comment?orderBy=-created&startAt={start}&maxResults=100")
        batch = r.get("comments", [])
        for x in batch:
            body = text(x["body"])
            if ROBOT in body and tag in body:
                return x["id"]
        start += len(batch)
        if not batch or start >= r.get("total", 0):
            return None


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
        r = call(c, "GET", "/rest/api/3/search/jql?" + urllib.parse.urlencode(params))
        issues += r.get("issues", [])
        token = r.get("nextPageToken")
        if not token or r.get("isLast", True):
            return issues


def cmd_sweep(a):
    team = TEAMS.get(a.team.lower())
    if not team:
        sys.exit(f"Unknown team '{a.team}'. Choose from: {', '.join(TEAMS)}")
    c = creds()
    date = dt.date.fromisoformat(a.date) if a.date else last_working_day()
    day_start = dt.datetime.combine(date, dt.time(0), REPORT_TZ)

    sprints = call(c, "GET", f"/rest/agile/1.0/board/{team['board']}/sprint?state=active")["values"]
    sprints = [s for s in sprints if s.get("originBoardId") == team["board"]]
    if not sprints:
        sys.exit(f"No active sprint found for {a.team} (board {team['board']}).")
    issues = active_sprint_tickets(c, team, ",".join(str(s["id"]) for s in sprints))
    print(f"Team {a.team} | sprint(s): {', '.join(s['name'] for s in sprints)} | report day {date} [times in {REPORT_TZ.key}]")
    print(f"{len(issues)} tickets (sub-tasks and Ready for Dev excluded)")

    active, quiet = [], []
    for i in issues:
        key, f = i["key"], i["fields"]
        head = f"{key} | {f['issuetype']['name']} | {(f.get('assignee') or {}).get('displayName')} | {f['summary']}"
        if dt.datetime.strptime(f["updated"], JIRA_TS).astimezone(REPORT_TZ) < day_start:
            quiet.append(f"{head} | status: {f['status']['name']}")
            continue
        moves = status_moves(c, key)
        day_moves = [m for m in moves if m[0].date() == date]
        upto = [m for m in moves if m[0].date() <= date]
        eod_status = upto[-1][2] if upto else (moves[0][1] if moves else f["status"]["name"])
        todays = comments_on(c, key, date)
        human = [x for x in todays if ROBOT not in x[2]]
        existing = eod_comment(c, key, date)
        if not day_moves and not human:
            quiet.append(f"{head} | status: {eod_status}" + (" | EOD comment already exists" if existing else ""))
            continue
        lines = [head, f"  status at end of {date}: {eod_status} (now: {f['status']['name']})"]
        lines += [f"  {t:%H:%M}  {frm} -> {to}" for t, frm, to in day_moves]
        lines += [f"  comment {t:%H:%M} {who}: {body[:700]}" for t, who, body, _ in human]
        if existing:
            lines.append(f"  EOD comment already exists (id {existing}); post with --update to edit")
        active.append("\n".join(lines))

    print(f"\n== ACTIVE: moved or human-commented on {date} ({len(active)}) ==")
    print("\n\n".join(active) or "none")
    print(f"\n== QUIET: no Jira activity on {date} ({len(quiet)}), check Fellow and Slack for these ==")
    print("\n".join(quiet) or "none")


def cmd_post(a):
    c = creds()
    date = dt.date.fromisoformat(a.date) if a.date else last_working_day()
    line = a.text.strip()
    if "—" in line:
        sys.exit("Comment contains an em dash. Rewrite it.")
    if "\n" in line:
        sys.exit("EOD comment must be one sentence on one line.")
    body = {
        "type": "doc", "version": 1,
        "content": [{"type": "paragraph", "content": [
            {"type": "text", "text": f"{ROBOT} "},
            {"type": "text", "text": f"EOD Status ({date}):", "marks": [{"type": "strong"}]},
            {"type": "text", "text": f" {line}"},
        ]}],
    }
    existing = eod_comment(c, a.ticket, date)
    if existing and not a.update:
        print(f"{a.ticket}: EOD comment for {date} already exists (id {existing}). Skipped. Pass --update to edit it.")
        return
    if existing:
        call(c, "PUT", f"/rest/api/3/issue/{a.ticket}/comment/{existing}", {"body": body})
        print(f"{a.ticket}: updated comment {existing}")
        return
    r = call(c, "POST", f"/rest/api/3/issue/{a.ticket}/comment", {"body": body})
    print(f"{a.ticket}: posted comment {r.get('id')}")


def main():
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    s = p.add_subparsers(dest="cmd", required=True)
    w = s.add_parser("sweep")
    w.add_argument("--team", required=True, help="ibex | aries | cabra")
    w.add_argument("--date", help="YYYY-MM-DD, US Eastern day (default: last working day)")
    w.set_defaults(fn=cmd_sweep)
    q = s.add_parser("post")
    q.add_argument("ticket")
    q.add_argument("--date", help="YYYY-MM-DD (default: last working day)")
    q.add_argument("--text", required=True)
    q.add_argument("--update", action="store_true")
    q.set_defaults(fn=cmd_post)
    a = p.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
