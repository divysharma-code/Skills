#!/usr/bin/env python3
"""Grooming notes updater, Jira side. Standard library only, no other skill needed.

  agenda  List the tickets a squad's grooming call most likely covered. STRONG = named in the
          call, or story points set / status moved out of grooming during the call. AGENDA ONLY =
          sat in the grooming status that day but nothing changed.
  post    Post one grooming-notes comment, or update your own in place.

Credentials: ~/.config/jira/credentials.env (JIRA_EMAIL, JIRA_API_TOKEN, JIRA_BASE_URL).
Dates are US Eastern.
"""

import argparse
import base64
import datetime as dt
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from zoneinfo import ZoneInfo

ET = ZoneInfo("America/New_York")
JIRA_TS = "%Y-%m-%dT%H:%M:%S.%f%z"
MEMO = "\U0001F4DD"
CAMERA = "\U0001F3A5"
POINTS = "customfield_10024"
MAX_LINE = 280

GROOMING_STATUS = {
    "ICS": "Ready for Grooming",
    "IPS": "Ready for / In Grooming",
    "COH": "Ready for / In Grooming",
}
TEAMS = {"ibex": ["ICS", "IPS"], "aries": ["IPS"], "cabra": ["COH"]}


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


def call(c, method, path, body=None, missing_ok=False):
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
        if missing_ok and e.code == 404:
            return None
        sys.exit(f"Jira {e.code} on {method} {path}: {e.read().decode(errors='replace')}")


def ts(s):
    return dt.datetime.strptime(s, JIRA_TS)


def when(s):
    t = dt.datetime.fromisoformat(s.replace("Z", "+00:00"))
    return t if t.tzinfo else t.replace(tzinfo=ET)


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


def search(c, jql, fields):
    issues, token = [], None
    while True:
        params = {"jql": jql, "fields": fields, "maxResults": 100}
        if token:
            params["nextPageToken"] = token
        r = call(c, "GET", "/rest/api/3/search/jql?" + urllib.parse.urlencode(params))
        issues += r.get("issues", [])
        token = r.get("nextPageToken")
        if not token or r.get("isLast", True):
            return issues


def history(c, key):
    """Status and Story Points changes as (datetime, kind, from, to), oldest first."""
    out, start = [], 0
    while True:
        r = call(c, "GET", f"/rest/api/3/issue/{key}/changelog?startAt={start}&maxResults=100")
        for h in r.get("values", []):
            for it in h["items"]:
                if it["field"] == "status":
                    out.append((ts(h["created"]), "status", it.get("fromString"), it.get("toString")))
                elif it.get("fieldId") == POINTS or it["field"] == "Story Points":
                    out.append((ts(h["created"]), "points", it.get("fromString"), it.get("toString")))
        start += len(r.get("values", []))
        if r.get("isLast", True) or not r.get("values"):
            return sorted(out, key=lambda x: x[0])


def date_tags(d):
    """The ways a grooming date has been written in existing comments (2026-10-06, Oct 6, 2026, Sept 10, 2026)."""
    tags = {d.isoformat(), f"{d:%b} {d.day}, {d.year}", f"{d:%B} {d.day}, {d.year}"}
    if d.month == 9:
        tags.add(f"Sept {d.day}, {d.year}")
    return tags


def grooming_comment(c, key, date):
    """(id, author name, author accountId) of a grooming-notes comment for `date`, if one exists."""
    tags, start = date_tags(date), 0
    while True:
        r = call(c, "GET", f"/rest/api/3/issue/{key}/comment?orderBy=-created&startAt={start}&maxResults=100")
        batch = r.get("comments", [])
        for x in batch:
            body = text(x["body"])
            if MEMO in body and "Grooming notes" in body and any(t in body for t in tags):
                return x["id"], x["author"]["displayName"], x["author"]["accountId"]
        start += len(batch)
        if not batch or start >= r.get("total", 0):
            return None


def points(f):
    v = f.get(POINTS)
    return "-" if v is None else f"{v:g}"


def expand(keys, projects):
    out = []
    for k in (x.strip().upper() for x in keys.split(",") if x.strip()):
        out += [f"{p}-{k}" for p in projects] if k.isdigit() else [k]
    return out


def cmd_agenda(a):
    projects = [p.strip().upper() for p in a.projects.split(",")] if a.projects else TEAMS.get(a.team.lower())
    if not projects:
        sys.exit(f"Unknown team '{a.team}'. Choose from: {', '.join(TEAMS)}, or pass --projects")
    c = creds()
    start = when(a.start)
    end = when(a.end) if a.end else start + dt.timedelta(hours=1)
    lo, hi = start - dt.timedelta(minutes=15), end + dt.timedelta(hours=2)
    day = start.astimezone(ET).date()
    fields = f"summary,status,assignee,issuetype,updated,description,{POINTS}"

    found = {}
    for p in projects:
        s = GROOMING_STATUS.get(p)
        if s:
            jql = (f'project = {p} AND issuetype not in (Sub-task, Epic) AND status WAS "{s}" '
                   f'DURING ("{day}", "{day + dt.timedelta(days=1)}")')
            for i in search(c, jql, fields):
                found.setdefault(i["key"], [i, set()])[1].add("grooming status")
    jql = (f'project in ({",".join(projects)}) AND issuetype not in (Sub-task, Epic) '
           f'AND updated >= "{day - dt.timedelta(days=1)}"')
    for i in search(c, jql, fields):
        found.setdefault(i["key"], [i, set()])
    for k in expand(a.keys or "", projects):
        i = call(c, "GET", f"/rest/api/3/issue/{k}?fields={fields}", missing_ok=True)
        if i:
            found.setdefault(k, [i, set()])[1].add("named")

    strong, agenda_only = [], []
    for key, (i, why) in sorted(found.items(), key=lambda kv: (kv[0].split("-")[0], int(kv[0].split("-")[1]))):
        f = i["fields"]
        head = (f"{key} | {f['issuetype']['name']} | {f['status']['name']} | {points(f)} pts | "
                f"{(f.get('assignee') or {}).get('displayName')} | {f['summary']}")
        events, signal = [], "named" in why
        if signal or ts(f["updated"]) >= lo:
            groom = GROOMING_STATUS.get(key.split("-")[0])
            for t, kind, frm, to in history(c, key):
                if not lo <= t <= hi:
                    continue
                events.append(f"  {t.astimezone(ET):%H:%M} {kind}: {frm or '-'} -> {to or '-'}")
                signal = signal or kind == "points" or frm == groom
        if not signal:
            if "grooming status" in why:
                agenda_only.append(head)
            continue
        lines = [head + ("  [named in call]" if "named" in why else "")] + events
        desc = " ".join(text(f.get("description")).split())
        if desc:
            lines.append(f"  description: {desc[:300]}")
        existing = grooming_comment(c, key, day)
        if existing:
            lines.append(f"  ALREADY POSTED for {day} by {existing[1]} (comment {existing[0]})")
        strong.append("\n".join(lines))

    print(f"Projects {', '.join(projects)} | call {start.astimezone(ET):%Y-%m-%d %H:%M}-{end.astimezone(ET):%H:%M} ET "
          f"| change window {lo.astimezone(ET):%H:%M}-{hi.astimezone(ET):%H:%M} ET | DATE {day}")
    print(f"\n== STRONG: named in the call, or points / grooming status changed during it ({len(strong)}) ==")
    print("\n\n".join(strong) or "none")
    print(f"\n== AGENDA ONLY: in the grooming status that day, nothing changed ({len(agenda_only)}) ==")
    print("\n".join(agenda_only) or "none")


def inline(s):
    out = []
    for n, part in enumerate(re.split(r"\*\*(.+?)\*\*", s)):
        if part:
            node = {"type": "text", "text": part}
            if n % 2:
                node["marks"] = [{"type": "strong"}]
            out.append(node)
    return out


def adf(date, lines, link):
    return {
        "type": "doc", "version": 1,
        "content": [
            {"type": "paragraph", "content": [
                {"type": "text", "text": f"{MEMO} "},
                {"type": "text", "text": f"Grooming notes ({date}):", "marks": [{"type": "strong"}]},
            ]},
            {"type": "bulletList", "content": [
                {"type": "listItem", "content": [{"type": "paragraph", "content": inline(l)}]} for l in lines
            ]},
            {"type": "paragraph", "content": [
                {"type": "text", "text": f"{CAMERA} "},
                {"type": "text", "text": "Recording", "marks": [{"type": "link", "attrs": {"href": link}}]},
            ]},
        ],
    }


def cmd_post(a):
    lines = [l.strip() for l in a.line]
    if not 1 <= len(lines) <= 5:
        sys.exit("Pass 1 to 5 --line values, one per bullet.")
    for l in lines:
        if "—" in l:
            sys.exit(f"Em dash in: {l!r}. Rewrite it.")
        if "\n" in l:
            sys.exit(f"Each bullet must be one line: {l!r}")
        if len(l) > MAX_LINE:
            sys.exit(f"Bullet is {len(l)} characters (max {MAX_LINE}). Cut it: {l[:80]!r}...")
    if not a.link.startswith("https://"):
        sys.exit("--link must be the Fellow recording URL (https://...).")
    date = dt.date.fromisoformat(a.date)
    body = adf(date, lines, a.link)
    c = creds()
    existing = grooming_comment(c, a.ticket, date)
    me = call(c, "GET", "/rest/api/3/myself")["accountId"]
    if existing and (not a.update or existing[2] != me):
        why = "it's someone else's, never edited" if existing[2] != me else "pass --update to edit it"
        print(f"{a.ticket}: grooming notes for {date} already posted by {existing[1]} (comment {existing[0]}). "
              f"Skipped, {why}.")
        return
    if a.dry_run:
        print(f"{a.ticket}: would {'update comment ' + existing[0] if existing else 'post a new comment'}:")
        print(f"{MEMO} Grooming notes ({date}):")
        print("\n".join(f"- {l}" for l in lines))
        print(f"{CAMERA} Recording -> {a.link}")
        return
    if existing:
        call(c, "PUT", f"/rest/api/3/issue/{a.ticket}/comment/{existing[0]}", {"body": body})
        print(f"{a.ticket}: updated comment {existing[0]}")
        return
    r = call(c, "POST", f"/rest/api/3/issue/{a.ticket}/comment", {"body": body})
    print(f"{a.ticket}: posted comment {r.get('id')}")


def main():
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    s = p.add_subparsers(dest="cmd", required=True)
    g = s.add_parser("agenda")
    g.add_argument("--team", default="", help="ibex | aries | cabra")
    g.add_argument("--projects", help="override the team's project keys, e.g. ICS,IPS")
    g.add_argument("--start", required=True, help="call start_time from Fellow, e.g. 2026-10-07T23:00:00+05:30")
    g.add_argument("--end", help="call end_time from Fellow (default: start + 1 hour)")
    g.add_argument("--keys", help="tickets named in the call, bare numbers OK: 8456,8458,ICS-32")
    g.set_defaults(fn=cmd_agenda)
    q = s.add_parser("post")
    q.add_argument("ticket")
    q.add_argument("--date", required=True, help="grooming date, YYYY-MM-DD")
    q.add_argument("--link", required=True, help="Fellow meeting_link")
    q.add_argument("--line", action="append", default=[], help="one bullet; repeat 1 to 5 times; **bold** works")
    q.add_argument("--update", action="store_true", help="edit your own existing comment for this date")
    q.add_argument("--dry-run", action="store_true", help="check and print, don't post")
    q.set_defaults(fn=cmd_post)
    a = p.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
