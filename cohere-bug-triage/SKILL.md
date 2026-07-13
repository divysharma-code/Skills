---
name: cohere-bug-triage
description: "Triage Cohere Intake production bugs (Jira board 1487): pull the untriaged queue, classify steps-to-reproduce (YES/THIN/NO), extract steps + auth-check specifics, write a plain-English problem summary, match a UAT test patient (member ID/DOB/plan) per bug, RCA each bug against the RALF intake architecture to flag whether it's even reproducible in UAT, and comment on tickets missing steps — all into a Google Sheet. Use when the user asks to triage bugs, do bug validation or RCA, check the intake bug queue, find tickets missing steps to reproduce, decide which bugs are testable, or mentions Cohere Intake / board 1487."
version: 1.0.0
author: Divy Sharma
license: MIT
metadata:
  jira_board: 1487
  requires: ["~/.config/jira/credentials.env", "google-workspace MCP"]
---

# Cohere Bug Triage

Automates Divy's daily bug-validation job on the **Intake Prod Bugs** board (Jira 1487).
One run builds a Google Sheet that, per bug, gives: the extracted steps, the auth-check
specifics, a plain-English problem summary, a matched UAT test patient, an RCA + whether
it's even reproducible in UAT — then comments on tickets that are missing steps.

## Quick start

```bash
SKILL=~/.claude/skills/cohere-bug-triage
python3 $SKILL/scripts/triage.py fetch --table    # human preview of today's queue
python3 $SKILL/scripts/triage.py fetch > /tmp/triage.json   # full JSON for the sheet
```

The script reads Jira creds from `~/.config/jira/credentials.env` and uses only the
Python standard library. See [REFERENCE.md](REFERENCE.md) for fields, mappings, and rules.

## Workflow (run in order)

1. **Fetch & classify.** `triage.py fetch` → JSON. Each record: `key, summary, status,
   assignee, priority, payer, created, age_days, steps_status, steps_cell, auth_check,
   narrative, url`. `steps_status` = `YES` / `THIN` (weak) / `NO` (missing → gets a comment).

2. **Create the sheet + base columns** (via `google-workspace` MCP as
   `divy.sharma@coherehealth.com`). Find/`create_spreadsheet` **"Cohere Bug Triage"**; add a
   tab named **today's date** (`YYYY-MM-DD`). Column order (full schema + formulas in
   [REFERENCE.md](REFERENCE.md)):

   `Key · Summary · Status · Assignee · Priority · Payer · Created · Age (days) · Steps? ·
   Steps to Reproduce · Comment posted? · Link · Auth Check Details · Plan Difficulty ·
   Health Plan (for auth) · Test Member ID · Test DOB · Primary Dx · Problem (plain English) ·
   Testable in UAT? · RCA — likely layer & why`

   `steps_cell` → **Steps to Reproduce** (keep line breaks); `auth_check` → **Auth Check
   Details**; **Comment posted?** blank. **Plan Difficulty** = auto ARRAYFORMULA (🟢 Easy
   GHP/Humana · 🔴 Hard Tennessee · 🟡 Medium) — formula in REFERENCE.

3. **Auth-start block** (Health Plan · Test Member ID · Test DOB · Primary Dx). Resolve each
   bug's health plan (payer + summary + steps), match it to a test patient in
   `Test_Patient_Creation_Worksheet`, fill Member ID + DOB. Format **Test DOB** as
   `MM/DD/YYYY`. Primary Dx = first ICD in `auth_check`. Lookup method + plan→member map: REFERENCE.

4. **Problem (plain English).** For each bug, read `narrative` and write ONE jargon-free
   sentence — what the reporter actually means (fall back to summary if narrative is empty).

5. **Testability + RCA.** Classify each bug against the RALF intake architecture
   (`CohereHealth/ralf` → `intake/architecture/overview.md`, read via `gh`): set **Testable
   in UAT?** ✅ Yes / 🟡 Maybe / ❌ No and a one-line **RCA** (layer + why). Rule of thumb:
   ✅ only the frontend auth flow + Clinical Assessment (CAQ); ❌ Integrations/outbound
   (CareAdvance/TMCS/Guiding Care/Rhyme/FHIR), Data platform (Hudi/reporting), Mongo/infra,
   QM/backend. Full rubric in [REFERENCE.md](REFERENCE.md).

6. **Comment gate — CONFIRM BEFORE POSTING.** List every `NO`-steps ticket and get an
   explicit yes (posting writes to a live production board). On approval:
   `python3 $SKILL/scripts/triage.py comment COH-1234 IPS-567 …`, then set **Comment posted?**
   `✓ <date>`. THIN and YES tickets never get a comment.

7. **Summarize.** Counts (total · YES/THIN/NO · commented · ✅/🟡/❌ testable) + sheet link,
   and point the user at the **✅ Testable** rows to work first.

## Reproducing a bug (the manual half)

The steps above prep the queue; actually validating a bug is a UAT portal workflow —
reproduce in **UAT (not DEV)**, pull a test member from the Test Patient Creation sheet, use
**all** the ticket's CPT codes to trigger the right clinical assessment question, then move
it to **Ready for Dev** + `intake-Kanban` label (or `unable to reproduce` → Dev Support after
~30 min). Full step-by-step with tips: **[PLAYBOOK.md](PLAYBOOK.md)**.

## Notes

- To auto-post without the gate (only if the user explicitly asks), skip the approval step.
- Change the comment wording or the "untriaged" statuses at the top of `scripts/triage.py`.
- `fetch --limit N` caps the queue for a quick test; `--statuses "..."` overrides the columns.
