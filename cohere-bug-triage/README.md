# Cohere Bug Triage

Turns the daily Intake bug-triage job into one command. It reads the untriaged bugs on the
Jira board (1487, "Intake Prod Bugs"), works out which ones you can actually reproduce,
builds a Google Sheet you can work from, and comments on tickets missing steps — after you
approve.

## What one run gives you

A Google Sheet ("Cohere Bug Triage"), one row per bug, with:

- The steps to reproduce, pulled out as a numbered list.
- A plain-English summary of what the reporter actually means.
- A test patient to use: health plan, member ID, DOB — plus the diagnosis and CPT/auth/NPI
  to search on.
- A **Testable in UAT?** verdict (✅ yes / 🟡 maybe / ❌ no) with a one-line root cause, so you
  skip the bugs that belong to engineering.

Each bug's steps are graded ✅ has steps / 🟡 weak / ❌ none. The ❌ ones get a "needs steps to
reproduce" comment — but only after it shows you the list and you say go.

## Use it

Tell Claude: **"Triage today's Cohere intake bugs."** It runs the whole flow and pauses once,
before commenting.

Quick terminal peek, no sheet:

```bash
python3 ~/.claude/skills/cohere-bug-triage/scripts/triage.py fetch --table
```

## Setup (once)

1. A Jira API token at `~/.config/jira/credentials.env` — your email, the token, and
   `JIRA_BASE_URL=https://coherehealth.atlassian.net`. Get one
   [here](https://id.atlassian.com/manage-profile/security/api-tokens).
2. Google access via the `google-workspace` MCP.

No installs — the script uses only Python's standard library.

## Change the defaults

Edit the top of `scripts/triage.py`:

- Comment wording → `COMMENT_TEXT`
- Statuses that count as "untriaged" → `UNTRIAGED_STATUSES`
- How strict the weak-steps check is → `THIN_MIN_LINES` / `THIN_MIN_CHARS`

## Reproducing a bug

Building the sheet is the easy half; reproducing a bug is hands-on in the UAT portal. The
step-by-step is in [PLAYBOOK.md](PLAYBOOK.md). Detailed mechanics are in
[REFERENCE.md](REFERENCE.md). The instructions Claude follows are in [SKILL.md](SKILL.md).

---

*Original skill by Divy Sharma · MIT License.*
