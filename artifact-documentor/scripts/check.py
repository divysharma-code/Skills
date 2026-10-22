#!/usr/bin/env python3
"""Pre-publish checks for an RCA insight page. Usage: python3 check.py page.html"""
import re
import sys

page = open(sys.argv[1], encoding="utf-8").read()
visible = re.sub(r"<!--.*?-->", "", page, flags=re.S)
problems = []

left = re.findall(r"\{\{[^}]*\}\}", visible)
if left:
    problems.append(f"{len(left)} unfilled placeholder(s), first: {left[0]}")

if "\u2014" in visible:
    problems.append("em dash found; rewrite the sentence")

for section in re.findall(r"<section[^>]*>(.*?)</section>", visible, flags=re.S):
    heading = re.search(r"<h2>(.*?)</h2>", section)
    name = heading.group(1) if heading else "untitled section"
    body = "".join(re.findall(r"<tbody>(.*?)</tbody>", section, flags=re.S))
    for row in re.findall(r"<tr>(.*?)</tr>", body, flags=re.S):
        if 'class="tag' not in row:
            cell = re.sub(r"<[^>]+>", "", row)[:50]
            problems.append(f'untagged row in "{name}": {cell}')

if re.search(r"\b(0[1-9]|1[0-2])/(0[1-9]|[12]\d|3[01])/(19|20)\d{2}\b", visible):
    problems.append("MM/DD/YYYY date found; could be a date of birth (PHI)")

if len(re.findall(r'<li class="turn">', visible)) > 3:
    problems.append('more than 3 timeline "turn" rows')
if len(re.findall(r'<li class="found">', visible)) > 1:
    problems.append('more than 1 timeline "found" row')

for label in re.findall(r'aria-label="([^"]*)"', visible):
    if len(label) < 40:
        problems.append(f"diagram aria-label too thin: {label!r}")

if '<div class="term">' not in visible:
    problems.append("no term cards")

print("\n".join("- " + p for p in problems) if problems else "OK: no problems found")
sys.exit(1 if problems else 0)
