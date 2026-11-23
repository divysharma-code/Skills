#!/usr/bin/env python3
"""Sprint health for a Jira scrum board, using the Application Engineering method.

Standard library only. Reads Jira creds from ~/.config/jira/credentials.env.

Usage:
  sprint_health.py --board 7962 [--last 4] [--json]
  sprint_health.py --sprint 19131 [--json]
"""
import argparse
import base64
import json
import os
import sys
import urllib.parse
import urllib.request
from datetime import datetime

SP_FIELD = "customfield_10024"
SPRINT_FIELD = "customfield_10020"
READY_TO_DEPLOY = "ready to deploy"


def load_env(path="~/.config/jira/credentials.env"):
    env = {}
    with open(os.path.expanduser(path)) as fh:
        for line in fh:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                env[k] = v.strip().strip('"').strip("'")
    return env


class Jira:
    def __init__(self):
        env = load_env()
        self.base = env["JIRA_BASE_URL"].rstrip("/")
        token = base64.b64encode(f"{env['JIRA_EMAIL']}:{env['JIRA_API_TOKEN']}".encode()).decode()
        self.auth = f"Basic {token}"

    def get(self, path, params=None):
        url = self.base + path
        if params:
            url += "?" + urllib.parse.urlencode(params)
        req = urllib.request.Request(url, headers={"Authorization": self.auth})
        with urllib.request.urlopen(req) as resp:
            return json.load(resp)

    def paged(self, path, key, params, page=100):
        out, start = [], 0
        while True:
            data = self.get(path, {**params, "startAt": start, "maxResults": page})
            items = data.get(key, data.get("values", []))
            out += items
            start += len(items)
            if not items or data.get("isLast") or start >= data.get("total", start):
                return out


def ts(value):
    return datetime.strptime(value.replace("Z", "+0000"), "%Y-%m-%dT%H:%M:%S.%f%z")


def sprint_members_at(issue, sprint_id, when):
    """True if the issue belonged to the sprint at time `when`, replaying the Sprint field history."""
    fields = issue["fields"]
    if ts(fields["created"]) > when:
        return False
    events = []
    for h in sorted(issue["changelog"]["histories"], key=lambda h: h["created"]):
        for item in h["items"]:
            if item["field"] == "Sprint":
                events.append((ts(h["created"]), item))
    if not events:
        return str(sprint_id) in {str(s["id"]) for s in (fields.get(SPRINT_FIELD) or [])}
    ids = lambda s: {x.strip() for x in (s or "").split(",") if x.strip()}
    current = ids(events[0][1].get("from"))
    for when_changed, item in events:
        if when_changed > when:
            break
        current = (current - (ids(item.get("from")) - ids(item.get("to")))) | ids(item.get("to"))
    return str(sprint_id) in current


def story_points_at(issue, when):
    """Story points in force at `when`: the value as it was just before the first edit after `when`."""
    value = issue["fields"].get(SP_FIELD)
    for h in sorted(issue["changelog"]["histories"], key=lambda h: h["created"], reverse=True):
        if ts(h["created"]) <= when:
            break
        for item in h["items"]:
            if item.get("fieldId") == SP_FIELD:
                try:
                    value = float(item["from"]) if item.get("from") not in (None, "") else None
                except ValueError:
                    value = None
    return value or 0.0


def status_at(issue, when):
    status, first_from = None, None
    for h in sorted(issue["changelog"]["histories"], key=lambda h: h["created"]):
        for item in h["items"]:
            if item["field"] == "status":
                if first_from is None:
                    first_from = item["fromString"]
                if ts(h["created"]) <= when:
                    status = item["toString"]
    if status is not None:
        return status
    return first_from or issue["fields"]["status"]["name"]


def sprint_report(jira, sprint):
    sid = sprint["id"]
    start = ts(sprint["startDate"])
    close = ts(sprint.get("completeDate") or sprint["endDate"])
    issues = jira.paged(
        f"/rest/agile/1.0/sprint/{sid}/issue",
        "issues",
        {"expand": "changelog", "fields": f"summary,issuetype,assignee,resolutiondate,created,status,{SP_FIELD},{SPRINT_FIELD}"},
    )
    committed = added = completed_all = completed_committed = ready = 0.0
    rolled = []
    for issue in issues:
        f = issue["fields"]
        if f["issuetype"].get("subtask") or ts(f["created"]) > close:
            continue
        if not sprint_members_at(issue, sid, close):
            continue
        points = story_points_at(issue, close)
        in_at_start = sprint_members_at(issue, sid, start)
        resolved = bool(f.get("resolutiondate")) and ts(f["resolutiondate"]) <= close
        status = status_at(issue, close)
        if in_at_start:
            committed += points
        else:
            added += points
        if resolved:
            completed_all += points
            if in_at_start:
                completed_committed += points
        elif in_at_start:
            rolled.append({
                "key": issue["key"],
                "points": points,
                "assignee": (f.get("assignee") or {}).get("displayName", "-"),
                "status_at_close": status,
                "ready_to_deploy_at_close": status.lower() == READY_TO_DEPLOY,
                "summary": f["summary"],
            })
        if not resolved and status.lower() == READY_TO_DEPLOY:
            ready += points

    def pct(n, d):
        return round(100 * n / d, 1) if d else None

    total = committed + added
    return {
        "sprint": sprint["name"],
        "sprint_id": sid,
        "start": sprint["startDate"][:10],
        "close": (sprint.get("completeDate") or sprint["endDate"])[:10],
        "committed_sp": committed,
        "added_sp": added,
        "total_sp": total,
        "completed_sp": completed_all,
        "committed_completion_pct": pct(completed_committed, committed),
        "delivery_efficiency_pct": pct(completed_all, committed),
        "final_delivery_pct": pct(completed_all, total),
        "ready_to_deploy_at_close_sp": ready,
        "rolled_over_sp": sum(r["points"] for r in rolled),
        "rolled_over": rolled,
    }


def closed_sprints_for_board(jira, board_id, last):
    sprints = jira.paged(f"/rest/agile/1.0/board/{board_id}/sprint", "values", {"state": "closed"})
    # Boards that share issues list each other's sprints; keep only the sprints this board owns.
    sprints = [s for s in sprints if s.get("originBoardId") in (None, board_id)]
    sprints.sort(key=lambda s: s.get("completeDate") or s.get("endDate") or "")
    return sprints[-last:]


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--board", type=int, help="Jira board id, e.g. 7962 for Ibex")
    g.add_argument("--sprint", type=int, help="single sprint id")
    p.add_argument("--last", type=int, default=4, help="closed sprints to report with --board (default 4)")
    p.add_argument("--json", action="store_true", help="print JSON instead of a table")
    args = p.parse_args()

    jira = Jira()
    if args.sprint:
        sprints = [jira.get(f"/rest/agile/1.0/sprint/{args.sprint}")]
    else:
        sprints = closed_sprints_for_board(jira, args.board, args.last)
    reports = [sprint_report(jira, s) for s in sprints]

    if args.json:
        json.dump(reports, sys.stdout, indent=2)
        print()
        return

    def f(x):
        return "-" if x is None else f"{x:.1f}%"

    print(f"{'Sprint':<28}{'Start':<12}{'Close':<12}{'Commit':>7}{'Added':>7}{'Done':>7}{'Committed%':>12}{'DelivEff%':>11}{'Final%':>9}{'RTD':>6}{'Rolled':>8}")
    for r in reports:
        print(f"{r['sprint'][:27]:<28}{r['start']:<12}{r['close']:<12}"
              f"{r['committed_sp']:>7g}{r['added_sp']:>7g}{r['completed_sp']:>7g}"
              f"{f(r['committed_completion_pct']):>12}{f(r['delivery_efficiency_pct']):>11}{f(r['final_delivery_pct']):>9}"
              f"{r['ready_to_deploy_at_close_sp']:>6g}{r['rolled_over_sp']:>8g}")


if __name__ == "__main__":
    main()
