#!/usr/bin/env python3
"""Dev sign-off poster for Cohere Jira.

Pure standard library — no pip installs needed (works on system python3 3.9+).

Subcommands
-----------
  resolve  Look up one or more names against Jira's user search and print every
           match. Use this first for any name that might be ambiguous — e.g.
           "jeremy" resolves to two different people at Cohere.
  post     Convert a markdown sign-off body to Atlassian Document Format (ADF)
           and post it as a new Jira comment, or update an existing one with
           --comment-id. Resolves --cc names to real Jira mentions so people
           actually get notified (not inert "@Name" text).

Markdown-to-ADF support is deliberately narrow — just what a sign-off needs:
  - A leading "# Title" or "**Title**" line -> bold paragraph
  - "**bold**", `inline code`, and > blockquote lines
  - GitHub-style pipe tables (header row + --- separator row)
  - Plain paragraphs, separated by blank lines
  - "@[Name]" anywhere in the body -> a real Jira mention inline (not just in
    --cc), e.g. "Sai Teja clarified: @[saiteja.pulugurtha] confirmed the API
    already supports this." Resolved the same way as --cc names: refuses to
    post if the name is ambiguous.

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


# ---------------------------------------------------------------------------
# Credentials
# ---------------------------------------------------------------------------

def load_credentials():
    path = os.path.expanduser("~/.config/jira/credentials.env")
    creds = {}
    try:
        with open(path) as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, _, value = line.partition("=")
                creds[key.strip()] = value.strip().strip('"').strip("'")
    except FileNotFoundError:
        sys.exit(f"Missing credentials file: {path}")
    for required in ("JIRA_EMAIL", "JIRA_API_TOKEN", "JIRA_BASE_URL"):
        if required not in creds:
            sys.exit(f"{path} is missing {required}")
    return creds


def jira_request(creds, method, path, body=None):
    url = creds["JIRA_BASE_URL"].rstrip("/") + path
    auth = base64.b64encode(
        f"{creds['JIRA_EMAIL']}:{creds['JIRA_API_TOKEN']}".encode()
    ).decode()
    headers = {
        "Authorization": f"Basic {auth}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            raw = resp.read()
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as e:
        detail = e.read().decode(errors="replace")
        sys.exit(f"Jira API error {e.code} on {method} {path}: {detail}")


# ---------------------------------------------------------------------------
# Name resolution
# ---------------------------------------------------------------------------

def search_users(creds, query):
    encoded = urllib.parse.quote(query)
    return jira_request(creds, "GET", f"/rest/api/3/user/search?query={encoded}")


def resolve_names(creds, names):
    """Return {name: [matches]}. Caller must check for len(matches) != 1.

    Jira's user/search does fuzzy token matching — searching "Jeremy Wdowik" can
    still return every "Jeremy" in the org, not just the exact one. If the query
    exactly matches one candidate's displayName (case-insensitive), narrow to
    that single match instead of surfacing the whole fuzzy set as ambiguous.
    """
    results = {}
    for name in names:
        raw_matches = search_users(creds, name)
        candidates = [
            {
                "accountId": m["accountId"],
                "displayName": m["displayName"],
                "email": m.get("emailAddress", ""),
            }
            for m in raw_matches
        ]
        exact = [c for c in candidates if c["displayName"].lower() == name.strip().lower()]
        results[name] = exact if len(exact) == 1 else candidates
    return results


# ---------------------------------------------------------------------------
# Markdown -> ADF (narrow, sign-off-shaped)
# ---------------------------------------------------------------------------

INLINE_MENTION_PATTERN = re.compile(r"@\[([^\]]+)\]")


def find_inline_mention_names(md_text):
    """Every distinct name inside an @[Name] token in the body."""
    seen = []
    for name in INLINE_MENTION_PATTERN.findall(md_text):
        if name not in seen:
            seen.append(name)
    return seen


def text_node(t, marks=None):
    node = {"type": "text", "text": t}
    if marks:
        node["marks"] = marks
    return node


def parse_inline(line, mention_lookup=None):
    """Split a line into ADF text nodes: **bold**, `code`, and @[Name] mentions."""
    mention_lookup = mention_lookup or {}
    nodes = []
    pattern = re.compile(r"(\*\*[^*]+\*\*|`[^`]+`|@\[[^\]]+\])")
    parts = pattern.split(line)
    for part in parts:
        if not part:
            continue
        if part.startswith("**") and part.endswith("**"):
            nodes.append(text_node(part[2:-2], [{"type": "strong"}]))
        elif part.startswith("`") and part.endswith("`"):
            nodes.append(text_node(part[1:-1], [{"type": "code"}]))
        elif part.startswith("@[") and part.endswith("]"):
            name = part[2:-1]
            m = mention_lookup.get(name)
            if m:
                nodes.append({"type": "mention", "attrs": {"id": m["accountId"], "text": "@" + m["displayName"]}})
            else:
                # Resolution failed upstream in cmd_post's fail-fast check; this
                # branch should be unreachable in practice, but fall back to
                # plain text rather than crashing if it's ever hit.
                nodes.append(text_node(part))
        else:
            nodes.append(text_node(part))
    return nodes or [text_node("")]


def table_cell(line, header=False, mention_lookup=None):
    ptype = "tableHeader" if header else "tableCell"
    return {"type": ptype, "content": [{"type": "paragraph", "content": parse_inline(line.strip(), mention_lookup)}]}


def table_row(cells, header=False, mention_lookup=None):
    return {"type": "tableRow", "content": [table_cell(c, header=header, mention_lookup=mention_lookup) for c in cells]}


def is_table_separator(line):
    return bool(re.match(r"^\|?\s*:?-{2,}:?\s*(\|\s*:?-{2,}:?\s*)+\|?\s*$", line.strip()))


def split_pipe_row(line):
    line = line.strip()
    if line.startswith("|"):
        line = line[1:]
    if line.endswith("|"):
        line = line[:-1]
    return [c.strip() for c in line.split("|")]


def markdown_to_adf(md_text, cc_mentions=None, inline_mention_lookup=None):
    lines = md_text.strip().split("\n")
    content = []
    i = 0
    n = len(lines)

    while i < n:
        line = lines[i]
        stripped = line.strip()

        if not stripped:
            i += 1
            continue

        # Table: a pipe row followed by a separator row
        if stripped.startswith("|") and i + 1 < n and is_table_separator(lines[i + 1]):
            header_cells = split_pipe_row(stripped)
            rows = [table_row(header_cells, header=True, mention_lookup=inline_mention_lookup)]
            i += 2
            while i < n and lines[i].strip().startswith("|"):
                rows.append(table_row(split_pipe_row(lines[i]), header=False, mention_lookup=inline_mention_lookup))
                i += 1
            content.append({
                "type": "table",
                "attrs": {"isNumberColumnEnabled": False, "layout": "default"},
                "content": rows,
            })
            continue

        # Blockquote
        if stripped.startswith(">"):
            quote_text = stripped.lstrip(">").strip()
            content.append({
                "type": "blockquote",
                "content": [{"type": "paragraph", "content": parse_inline(quote_text, inline_mention_lookup)}],
            })
            i += 1
            continue

        # Heading treated as a bold paragraph
        if stripped.startswith("#"):
            heading_text = stripped.lstrip("#").strip()
            content.append({
                "type": "paragraph",
                "content": [text_node(heading_text, [{"type": "strong"}])],
            })
            i += 1
            continue

        # Plain paragraph
        content.append({"type": "paragraph", "content": parse_inline(stripped, inline_mention_lookup)})
        i += 1

    if cc_mentions:
        cc_content = [text_node("CC: ")]
        for m in cc_mentions:
            cc_content.append({"type": "mention", "attrs": {"id": m["accountId"], "text": "@" + m["displayName"]}})
            cc_content.append(text_node(" "))
        content.append({"type": "paragraph", "content": cc_content})

    return {"type": "doc", "version": 1, "content": content}


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def cmd_resolve(args):
    creds = load_credentials()
    results = resolve_names(creds, args.names)
    exit_code = 0
    for name, matches in results.items():
        if len(matches) == 0:
            print(f"{name}: NO MATCH")
            exit_code = 1
        elif len(matches) == 1:
            m = matches[0]
            print(f"{name}: {m['displayName']} <{m['email']}> ({m['accountId']})")
        else:
            print(f"{name}: {len(matches)} matches — pick one explicitly, do not guess:")
            for m in matches:
                print(f"    {m['displayName']} <{m['email']}> ({m['accountId']})")
            exit_code = 1
    sys.exit(exit_code)


def resolve_or_exit(creds, names, label):
    """Resolve a list of names, exiting with every ambiguous match printed if
    any name doesn't resolve to exactly one person. Shared by --cc and the
    @[Name] inline-mention path so both fail the same way."""
    resolved = {}
    resolved_raw = resolve_names(creds, names)
    for name, matches in resolved_raw.items():
        if len(matches) != 1:
            print(f"Cannot resolve {label} name '{name}': {len(matches)} matches found.")
            for m in matches:
                print(f"    {m['displayName']} <{m['email']}> ({m['accountId']})")
            sys.exit(
                f"Refusing to post with an ambiguous {label} name ('{name}'). "
                "Pass the exact displayName from the list above, or use 'resolve' first."
            )
        resolved[name] = matches[0]
    return resolved


def cmd_post(args):
    creds = load_credentials()

    with open(args.body_file) as f:
        md_text = f.read()

    cc_mentions = []
    if args.cc:
        names = [n.strip() for n in args.cc.split(",") if n.strip()]
        resolved = resolve_or_exit(creds, names, "CC")
        cc_mentions = list(resolved.values())

    inline_names = find_inline_mention_names(md_text)
    inline_mention_lookup = resolve_or_exit(creds, inline_names, "@[...]") if inline_names else {}

    adf = markdown_to_adf(md_text, cc_mentions=cc_mentions, inline_mention_lookup=inline_mention_lookup)
    payload = {"body": adf}

    if args.comment_id:
        result = jira_request(
            creds, "PUT", f"/rest/api/3/issue/{args.ticket}/comment/{args.comment_id}", payload
        )
        print(f"Updated comment {args.comment_id} on {args.ticket}")
    else:
        result = jira_request(
            creds, "POST", f"/rest/api/3/issue/{args.ticket}/comment", payload
        )
        print(f"Posted comment {result.get('id')} on {args.ticket}")


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = parser.add_subparsers(dest="command", required=True)

    p_resolve = sub.add_parser("resolve", help="Look up names against Jira user search")
    p_resolve.add_argument("names", nargs="+", help="Names to search, e.g. vidhi jeremy lakshman")
    p_resolve.set_defaults(func=cmd_resolve)

    p_post = sub.add_parser("post", help="Post or update a sign-off comment")
    p_post.add_argument("ticket", help="Jira ticket key, e.g. ICS-25")
    p_post.add_argument("body_file", help="Path to a markdown file with the sign-off body")
    p_post.add_argument("--cc", default="", help="Comma-separated names to @mention, e.g. 'Vidhi Kakani,Jeremy Wdowik'")
    p_post.add_argument("--comment-id", default=None, help="Update this existing comment instead of posting new")
    p_post.set_defaults(func=cmd_post)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
