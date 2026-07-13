#!/usr/bin/env python3
"""Cohere bug-triage helper for Jira board 1487 (Intake Prod Bugs).

Pure standard library — no pip installs needed (works on system python3 3.9+).

Subcommands
-----------
  fetch    Pull the untriaged queue, classify steps-to-reproduce (YES/THIN/NO),
           extract numbered steps, and emit JSON (or a human table with --table).
  comment  Post the "needs steps to reproduce" comment on the given issue keys.
           Only comments on keys you explicitly pass — it never mass-comments.

Credentials are read from ~/.config/jira/credentials.env:
  JIRA_EMAIL, JIRA_API_TOKEN, JIRA_BASE_URL
"""

import argparse
import base64
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from html.parser import HTMLParser

# ---------------------------------------------------------------------------
# Config — safe to edit
# ---------------------------------------------------------------------------
BOARD_ID = 1487
# Columns "RALF Support" (To Do, Under investigation) + "Product Triage"
# (Scoping, Planning) make up the untriaged queue on board 1487.
UNTRIAGED_STATUSES = ["To Do", "Under investigation", "Scoping", "Planning"]
COMMENT_TEXT = (
    "Triage: this ticket is missing steps to reproduce. Please add clear, "
    "numbered steps so the issue can be validated and worked."
)
# A ticket with a Steps-to-Reproduce heading is treated as THIN (flag, no
# comment) when it has fewer than this many lines or characters of content.
THIN_MIN_LINES = 2
THIN_MIN_CHARS = 40
CREDS_PATH = os.path.expanduser("~/.config/jira/credentials.env")

# Section headings that mark the END of a Steps-to-Reproduce block.
_END_HEADINGS = (
    r"(client severity|payer|phase|auth tracking number|impact|expected result|"
    r"actual result|triage note|triage|problem statement|resolution|"
    r"according to integrations|comment from)"
)


# ---------------------------------------------------------------------------
# Credentials + HTTP (Basic auth, stdlib only)
# ---------------------------------------------------------------------------
def load_creds():
    if not os.path.exists(CREDS_PATH):
        sys.exit(f"ERROR: credentials file not found at {CREDS_PATH}")
    env = {}
    with open(CREDS_PATH) as fh:
        for line in fh:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip()
    for key in ("JIRA_EMAIL", "JIRA_API_TOKEN", "JIRA_BASE_URL"):
        if not env.get(key):
            sys.exit(f"ERROR: {key} missing from {CREDS_PATH}")
    return env


def _auth_header(env):
    raw = f"{env['JIRA_EMAIL']}:{env['JIRA_API_TOKEN']}".encode()
    return "Basic " + base64.b64encode(raw).decode()


def api(env, method, path, params=None, body=None):
    url = env["JIRA_BASE_URL"].rstrip("/") + path
    if params:
        url += "?" + urllib.parse.urlencode(params)
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Authorization", _auth_header(env))
    req.add_header("Accept", "application/json")
    if data is not None:
        req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            payload = resp.read().decode()
            return json.loads(payload) if payload else {}
    except urllib.error.HTTPError as e:
        detail = e.read().decode(errors="replace")[:300]
        sys.exit(f"ERROR: {method} {path} -> HTTP {e.code}: {detail}")
    except urllib.error.URLError as e:
        sys.exit(f"ERROR: network problem reaching Jira: {e.reason}")


# ---------------------------------------------------------------------------
# Description parsing
# ---------------------------------------------------------------------------
class _Strip(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []

    def handle_starttag(self, tag, attrs):
        if tag in ("p", "br", "li", "div", "h1", "h2", "h3", "h4", "tr"):
            self.parts.append("\n")

    def handle_data(self, data):
        self.parts.append(data)

    def text(self):
        return re.sub(r"\n{3,}", "\n\n", "".join(self.parts)).strip()


def html_to_text(html):
    p = _Strip()
    p.feed(html or "")
    return p.text()


def adf_to_text(node):
    """Fallback: flatten Atlassian Document Format JSON to text."""
    if node is None:
        return ""
    if isinstance(node, dict):
        if node.get("type") == "text":
            return node.get("text", "")
        chunks = [adf_to_text(c) for c in node.get("content", [])]
        sep = "\n" if node.get("type") in ("paragraph", "listItem", "heading") else ""
        return sep.join(x for x in chunks if x)
    if isinstance(node, list):
        return "\n".join(adf_to_text(c) for c in node)
    return ""


def parse_field(text, label):
    """Grab a single-line 'Label: value' from the templated description."""
    m = re.search(rf"{label}\s*:\s*(.+)", text, re.I)
    return m.group(1).strip() if m else ""


def extract_steps(text):
    """Return a list of cleaned step strings, or None if no steps section."""
    m = re.search(r"steps to reproduce\s*:?", text, re.I)
    if not m:
        return None
    rest = text[m.end():]
    nxt = re.search(r"(^|\n)\s*[\*_]{0,2}\s*" + _END_HEADINGS + r"[\*_]{0,2}\s*[:\-]",
                    rest, re.I)
    block = rest[: nxt.start()] if nxt else rest
    lines = [re.sub(r"^\s*[\d\.\)\-\*•]+\s*", "", ln).strip() for ln in block.splitlines()]
    return [ln for ln in lines if ln]


_NARR_DROP = re.compile(
    r"^\s*(client severity|payer|phase|auth(?:orization)?\s*tracking\s*number)\s*:", re.I)


def extract_narrative(text):
    """The reporter's problem context (Description/Impact/Problem/Ask) — everything
    before the Steps to Reproduce block, minus the boilerplate header fields. Raw
    material for a plain-English summary; not shown verbatim in the sheet."""
    m = re.search(r"steps to reproduce\s*:?", text, re.I)
    head = text[: m.start()] if m else text
    lines = [ln.strip() for ln in head.splitlines()
             if ln.strip() and not _NARR_DROP.match(ln.strip())]
    return re.sub(r"\s{2,}", " ", " ".join(lines))[:800]


def classify(steps):
    if steps is None:
        return "NO"
    if len(steps) < THIN_MIN_LINES or len(" ".join(steps)) < THIN_MIN_CHARS:
        return "THIN"
    return "YES"


def extract_auth_details(text):
    """Pull the search specifics a tester needs to pull up / validate the auth:
    auth-tracking number, CPT/HCPCS codes, ICD-10 diagnosis, and provider NPIs."""
    parts, ids = [], []
    # Templated "Auth Tracking Number:" value — kept only if it's a single clean
    # token (catches non-standard formats like MCR_NV-F7180V0J), never a section label.
    m = re.search(r"auth(?:orization)?\s*tracking\s*number\s*:\s*(.+)", text, re.I)
    if m:
        v = m.group(1).strip().strip("*").split("\n")[0].strip()
        stop = ("description", "impact", "steps", "triage", "payer", "phase",
                "problem", "ask", "submitter")
        if (v and len(v) <= 32 and re.search(r"\d", v)
                and re.fullmatch(r"[A-Za-z0-9_#/\-. ]+", v)
                and not v.lower().startswith(stop)):
            ids.append(v)
    ids += re.findall(r"\b[A-Z]{4}\d{4}\b", text)              # Cohere tracking tokens
    ids += re.findall(r"authorization\s*#?\s*(\d{6,13})\b", text, re.I)  # numeric auth #
    cleaned = [x.strip().strip(",;") for x in ids if x.strip().strip(",;")]
    seen = []
    for x in cleaned:
        # drop a token that's already contained in another entry (e.g. the bare
        # number when "Authorization # <number>" is also present)
        if any(x != o and x in o for o in cleaned):
            continue
        if x not in seen:
            seen.append(x)
    if seen:
        parts.append("Auth#: " + ", ".join(seen[:6]))
    cpts = re.findall(r"\bCPT\s*(?:code)?\s*[:#\-]?\s*([A-Z]?\d{4,5}[A-Z]?)", text, re.I)
    cpts += re.findall(r"\b([JT]\d{4})\b", text)  # common HCPCS J/T codes
    if cpts:
        parts.append("CPT: " + ", ".join(dict.fromkeys(cpts)))
    dx = re.findall(r"(?:diagnosis|dx)[^\n]*?\b([A-Z]\d{2}\.?\d{0,3})\b", text, re.I)
    if dx:
        parts.append("Dx: " + ", ".join(dict.fromkeys(dx)))
    npis = re.findall(r"NPI[^\d]{0,8}(\d{10})", text, re.I)
    if npis:
        parts.append("NPI: " + ", ".join(dict.fromkeys(npis)))
    return " | ".join(parts)


# ---------------------------------------------------------------------------
# Fetch
# ---------------------------------------------------------------------------
def get_description_text(env, key):
    issue = api(env, "GET", f"/rest/api/3/issue/{key}",
                params={"expand": "renderedFields", "fields": "description"})
    html = (issue.get("renderedFields") or {}).get("description")
    if html:
        return html_to_text(html)
    return adf_to_text((issue.get("fields") or {}).get("description"))


def age_days(created):
    try:
        dt = datetime.strptime(created[:19], "%Y-%m-%dT%H:%M:%S").replace(tzinfo=timezone.utc)
        return (datetime.now(timezone.utc) - dt).days
    except Exception:
        return ""


def fetch(env, statuses, limit):
    jql = "status in ({}) ORDER BY created ASC".format(
        ", ".join(f'"{s}"' for s in statuses))
    records, start = [], 0
    while True:
        page = api(env, "GET", f"/rest/agile/1.0/board/{BOARD_ID}/issue", params={
            "jql": jql, "startAt": start, "maxResults": 50,
            "fields": "summary,status,assignee,priority,created",
        })
        for issue in page.get("issues", []):
            f = issue["fields"]
            desc = get_description_text(env, issue["key"])
            steps = extract_steps(desc)
            records.append({
                "key": issue["key"],
                "summary": f.get("summary", ""),
                "status": (f.get("status") or {}).get("name", ""),
                "assignee": (f.get("assignee") or {}).get("displayName", "Unassigned"),
                "priority": (f.get("priority") or {}).get("name", ""),
                "payer": parse_field(desc, "Payer"),
                "created": (f.get("created") or "")[:10],
                "age_days": age_days(f.get("created", "")),
                "steps_status": classify(steps),
                "steps": steps or [],
                "auth_check": extract_auth_details(desc),
                "narrative": extract_narrative(desc),
                "url": f"{env['JIRA_BASE_URL'].rstrip('/')}/browse/{issue['key']}",
            })
            if limit and len(records) >= limit:
                return records
        start += page.get("maxResults", 50)
        if start >= page.get("total", 0):
            break
    return records


def steps_cell(rec):
    """Numbered multi-line string for the Google Sheet cell."""
    if rec["steps_status"] == "NO":
        return ""
    return "\n".join(f"{i}. {s}" for i, s in enumerate(rec["steps"], 1))


# ---------------------------------------------------------------------------
# Comment
# ---------------------------------------------------------------------------
def post_comment(env, key, message):
    body = {"body": {"type": "doc", "version": 1, "content": [
        {"type": "paragraph", "content": [{"type": "text", "text": message}]}]}}
    api(env, "POST", f"/rest/api/3/issue/{key}/comment", body=body)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser(description="Cohere bug-triage helper (board 1487)")
    sub = ap.add_subparsers(dest="cmd", required=True)

    pf = sub.add_parser("fetch", help="pull + classify the untriaged queue")
    pf.add_argument("--statuses", nargs="+", default=UNTRIAGED_STATUSES,
                    help="workflow statuses to include")
    pf.add_argument("--limit", type=int, default=0, help="cap number of tickets")
    pf.add_argument("--table", action="store_true", help="human table instead of JSON")

    pc = sub.add_parser("comment", help="post the needs-steps comment on given keys")
    pc.add_argument("keys", nargs="+", help="issue keys, e.g. COH-1234 IPS-567")
    pc.add_argument("--message", default=COMMENT_TEXT, help="override comment text")

    args = ap.parse_args()
    env = load_creds()

    if args.cmd == "fetch":
        recs = fetch(env, args.statuses, args.limit)
        for r in recs:
            r["steps_cell"] = steps_cell(r)
        if args.table:
            need = sum(1 for r in recs if r["steps_status"] == "NO")
            print(f"{len(recs)} untriaged bugs | {need} missing steps (would get a comment)\n")
            for r in recs:
                flag = {"YES": "✅", "THIN": "⚠️ ", "NO": "❌"}[r["steps_status"]]
                print(f"{flag} {r['key']:<11} P{r['priority'][-1:]:<2} "
                      f"age {str(r['age_days']):>3}d  {r['summary'][:60]}")
        else:
            print(json.dumps(recs, indent=2, ensure_ascii=False))

    elif args.cmd == "comment":
        for key in args.keys:
            post_comment(env, key, args.message)
            print(f"commented: {key}")


if __name__ == "__main__":
    main()
