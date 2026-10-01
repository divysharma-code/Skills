#!/usr/bin/env python3
"""EOD updater helper for Cohere Jira. Standard library only.

  fetch  List tickets in a team's active sprint whose status changed on a date,
         with that day's transitions, end-of-day status, and any existing EOD comment.
  post   Post (or update in place) the one-line EOD comment on a ticket.

Credentials: ~/.config/jira/credentials.env (JIRA_EMAIL, JIRA_API_TOKEN, JIRA_BASE_URL).
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


def last_working_day(today=None):
    d = today or dt.date.today()
    d -= dt.timedelta(days=1)
    while d.weekday() >= 5:
        d -= dt.timedelta(days=1)
    return d


def flat(n):
    if isinstance(n, dict):
        if n.get("type") == "text":
            return n.get("text", "")
        return "".join(flat(x) for x in n.get("content", []))
    if isinstance(n, list):
        return "".join(flat(x) for x in n)
    return ""


def eod_comments(c, key, date):
    res = call(c, "GET", f"/rest/api/3/issue/{key}/comment?maxResults=100")
    tag = f"EOD Status ({date})"
    return [x for x in res.get("comments", []) if "🤖" in flat(x["body"]) and tag in flat(x["body"])]


def cmd_fetch(a):
    team = TEAMS.get(a.team.lower())
    if not team:
        sys.exit(f"Unknown team '{a.team}'. Choose from: {', '.join(TEAMS)}")
    c = creds()
    date = dt.date.fromisoformat(a.date) if a.date else last_working_day()
    nxt = date + dt.timedelta(days=1)

    sprints = call(c, "GET", f"/rest/agile/1.0/board/{team['board']}/sprint?state=active")["values"]
    sprints = [s for s in sprints if s.get("originBoardId") == team["board"]]
    if not sprints:
        sys.exit(f"No active sprint found for {a.team} (board {team['board']}).")
    ids = ",".join(str(s["id"]) for s in sprints)
    print(f"Team {a.team} | sprint(s): {', '.join(s['name'] for s in sprints)} | report day {date}")

    jql = (
        f'project = {team["project"]} AND sprint in ({ids}) '
        f'AND status changed DURING ("{date} 00:00","{nxt} 00:00") '
        f'AND status != "Ready for Dev" AND issuetype != Sub-task'
    )
    q = urllib.parse.urlencode({"jql": jql, "fields": "summary,status,assignee,issuetype", "maxResults": 100})
    issues = call(c, "GET", f"/rest/api/3/search/jql?{q}").get("issues", [])
    if not issues:
        print("No tickets changed status that day. (Still check the release doc for shipped tickets.)")
        return

    for i in issues:
        key = i["key"]
        f = i["fields"]
        cl = call(c, "GET", f"/rest/api/3/issue/{key}?expand=changelog&fields=status")["changelog"]["histories"]
        moves = sorted(
            (h["created"], it["fromString"], it["toString"])
            for h in cl for it in h["items"] if it["field"] == "status"
        )
        day = [m for m in moves if m[0].startswith(str(date))]
        eod_status = day[-1][2] if day else f["status"]["name"]
        print(f"\n{key} | {f['issuetype']['name']} | {(f.get('assignee') or {}).get('displayName')} | {f['summary']}")
        print(f"  status at end of {date}: {eod_status} (now: {f['status']['name']})")
        for t, frm, to in day:
            print(f"  {t[11:16]}  {frm} -> {to}")
        existing = eod_comments(c, key, date)
        if existing:
            print(f"  existing EOD comment: id {existing[0]['id']} (use --update to edit)")


def cmd_post(a):
    c = creds()
    date = a.date or str(last_working_day())
    text = a.text.strip()
    if "—" in text:
        sys.exit("Comment contains an em dash. Rewrite it.")
    if "\n" in text:
        sys.exit("EOD comment must be one sentence on one line.")
    body = {
        "type": "doc", "version": 1,
        "content": [{"type": "paragraph", "content": [
            {"type": "text", "text": f"\U0001F916 "},
            {"type": "text", "text": f"EOD Status ({date}):", "marks": [{"type": "strong"}]},
            {"type": "text", "text": f" {text}"},
        ]}],
    }
    existing = eod_comments(c, a.ticket, date)
    if existing and not a.update:
        print(f"{a.ticket}: EOD comment for {date} already exists (id {existing[0]['id']}). Skipped. Pass --update to edit it.")
        return
    if existing and a.update:
        call(c, "PUT", f"/rest/api/3/issue/{a.ticket}/comment/{existing[0]['id']}", {"body": body})
        print(f"{a.ticket}: updated comment {existing[0]['id']}")
        return
    r = call(c, "POST", f"/rest/api/3/issue/{a.ticket}/comment", {"body": body})
    print(f"{a.ticket}: posted comment {r.get('id')}")


def main():
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    s = p.add_subparsers(dest="cmd", required=True)
    f = s.add_parser("fetch")
    f.add_argument("--team", required=True, help="ibex | aries | cabra")
    f.add_argument("--date", help="YYYY-MM-DD (default: last working day)")
    f.set_defaults(fn=cmd_fetch)
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
