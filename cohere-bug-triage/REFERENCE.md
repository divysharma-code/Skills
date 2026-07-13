# Reference — cohere-bug-triage

Detailed mechanics behind [SKILL.md](SKILL.md). Read this when tuning behavior.

## Board & queue

- **Board:** 1487 "Intake Prod Bugs" (Kanban), project `COH` — *Digital channel intake
  (Cabra)*. Carries `COH-`, `IPS-`, and `KOZA-` issue keys; the board is 100% Bug type.
- **Untriaged queue** = the two earliest board columns:

  | Board column | Underlying statuses |
  | --- | --- |
  | RALF Support | `To Do`, `Under investigation` |
  | Product Triage | `Scoping`, `Planning` |

  The script fetches these via JQL `status in (...)`. Override with `fetch --statuses`.

## How "steps to reproduce" is detected

Cohere bugs put repro steps in the **description** (the dedicated custom fields —
`customfield_10513/10068/13491/15983` — exist but are left empty on this board). The
description follows a loose template:
`Client Severity → Payer → Phase → Auth Tracking Number → Description → Impact →
Steps to Reproduce → Triage note`.

`extract_steps()` finds the `Steps to Reproduce` heading, grabs everything up to the next
known section heading (Impact, Triage note, etc. — tolerant of leading `*`/bold), strips
list bullets/numbers, and returns clean lines.

### Classification (`steps_status`)

| Value | Meaning | Comment posted? |
| --- | --- | --- |
| `YES` | ≥ 2 lines and ≥ 40 chars of steps | No |
| `THIN` | a steps section exists but is below those thresholds | No — flagged in sheet |
| `NO` | no steps section at all | **Yes** |

Thresholds: `THIN_MIN_LINES`, `THIN_MIN_CHARS` at the top of `scripts/triage.py`.
Only `NO` gets a comment, so we never tell someone "needs steps" on a ticket that has some.

## Sheet schema

One spreadsheet **"Cohere Bug Triage"**, one tab per run named `YYYY-MM-DD`. Columns (A→U):

| Col | Header | Source |
| --- | --- | --- |
| A–H | Key · Summary · Status · Assignee · Priority · Payer · Created · Age (days) | fetch |
| I | Steps? (`YES`/`THIN`/`NO`) | `steps_status` |
| J | Steps to Reproduce | `steps_cell` (numbered, multi-line — wrap the column) |
| K | Comment posted? | filled after the comment step |
| L | Link | Jira browse URL |
| M | Auth Check Details | `auth_check` |
| N | Plan Difficulty | auto formula (below) |
| O | Health Plan (for auth) | resolved from ticket (auth-start block) |
| P | Test Member ID | matched test patient |
| Q | Test DOB | matched test patient, **format `MM/DD/YYYY`** |
| R | Primary Dx | first ICD in `auth_check` |
| S | Problem (plain English) | one-sentence distillation of `narrative` |
| T | Testable in UAT? | ✅ / 🟡 / ❌ (RCA rubric below) |
| U | RCA — likely layer & why | one-line root-cause note |

Header colours as a legend: green = auto/derived data, blue = auth-start inputs, purple =
RCA/analysis. (Earlier versions had an amber manual "worklog" block; it was dropped —
re-add only if the user asks.)

**Plan Difficulty** formula (put in `N2`, fills the column):

```
=ARRAYFORMULA(IF(A2:A="","",IF(REGEXMATCH(LOWER(B2:B&" "&F2:F&" "&J2:J),"ghp|humana|geisinger|oak street"),"🟢 Easy",IF(REGEXMATCH(LOWER(B2:B&" "&F2:F&" "&J2:J),"tennessee|bcbs t\b|bcbst"),"🔴 Hard",IF(F2:F="","—","🟡 Medium")))))
```

## Auth-check details (`auth_check`)

The search specifics a tester needs to pull up the auth and validate the bug in a
non-prod portal, extracted from the description by `extract_auth_details()`:

- **Auth#** — the templated "Auth Tracking Number" value (single clean token, e.g.
  `MCR_NV-F7180V0J`) plus every Cohere tracking token matching `[A-Z]{4}\d{4}` and any
  numeric `Authorization # <digits>`. Substrings already inside another entry are dropped.
- **CPT** — codes after a `CPT` mention, plus common HCPCS `J####` / `T####`.
- **Dx** — ICD-10 codes near "diagnosis"/"dx" (e.g. `M54.16`).
- **NPI** — 10-digit numbers near "NPI".

Rendered as one cell like `Auth#: … | CPT: … | Dx: … | NPI: …`. Pair it with the
`Patient Search — Auth Check` column in the Test_Patient_Creation_Worksheet to pick a
matching test member.

### Fields required to start an auth (non-prod portal)

**Member ID** + **Date of Birth** (required) and **Health Plan** (optional). These are
member identifiers and come from `Test_Patient_Creation_Worksheet`
(`memberId` col C, `dateOfBirth` col D, `coverage.healthPlanName` col A — all rolled into
its `Patient Search — Auth Check` column). They are **never** on the triage sheet: bug
tickets reference an auth by tracking number and carry codes/NPIs, but not member ID/DOB
(PHI), and in non-prod you use a test member anyway.

**Validation loop:** pick a test member (Patient Search column) → apply the bug's
**Auth Check Details** scenario (auth #, CPT, Dx, NPI) → start/reproduce the auth in the
non-prod portal → record the result on the triage sheet.

## Test-member lookup (auth-start block, cols O–R)

For each bug, detect the **health plan** from `payer + summary + steps` (keywords: humana/
oak street, ghp/geisinger, healthpartners, tennessee, south carolina, avera, mmo/medical
mutual, wiser, aetna, essence…), then pull one representative test patient for that plan.

Reads on `Test_Patient_Creation_Worksheet` truncate at ~50 rows, so **don't** try to read
all ~1,383 rows. Instead build the plan→member map with temporary lookup formulas: insert a
few scratch columns, one row per plan keyword —
`=IFERROR(INDEX($C$2:$C,MATCH("*Humana*",$A$2:$A,0)),"")` (member id, col C) and the same
for DOB (col D) and the matched plan name (col A) — read the small result, then **delete the
scratch columns**. DOBs come back as date serials; convert (base `1899-12-30`) and write as
`MM/DD/YYYY`. WISeR has no test patient; GHP maps to the "Geisinger" plan. Fill Member ID +
DOB only when a plan matches; leave blank otherwise. Line of business may not match — note it.

## Testability & RCA rubric (RALF architecture)

Ground RCA in `CohereHealth/ralf` → `intake/architecture/overview.md` (read via `gh`, decode
base64: `gh api repos/CohereHealth/ralf/contents/<path> --jq .content | base64 -d`). Intake
flow: **Portal / EHR / Fax→QM / Phone→Salesforce → `POST /authorization` → Clinical
Assessment (CAQ) → ServiceRequest → Review Queue + Integrations Platform.**

Only the **frontend auth flow + CAQ** is exercised by creating an auth in UAT, so:

| Testable in UAT? | Layers (RCA tag) |
| --- | --- |
| ✅ **Yes** | `[UI]` frontend (AuthBuilder, ClinicalAssessment, PatientSummary, dashboards, dropdowns, validation, copy) |
| 🟡 **Maybe** | `[UI/Rule]` needs a specific rule/config to fire · `[Rule/Referral]` · `[Access/Perms]` · `[Auth↔SR sync]` race conditions · underspecified tickets (timebox) |
| ❌ **No** | `[Integration]`/outbound (CareAdvance, TMCS, Guiding Care, Rhyme, MCG, FHIR, Salesforce) · `[Data/Analytics]` (Hudi, Tableau, reporting) · `[Infra/DB]` (Mongo schema, OptimisticLocking, guardrails) · `[QM/Backend]` · `[SSO/Config]` · single-record data anomalies |

Known systemic root cause per RALF: **Auth↔ServiceRequest data duplication + non-atomic
writes** (separate Mongo collections, Auth flushes before SR) — behind many status/sync bugs.
`❌`/unclear tickets → `unable to reproduce` comment → Dev Support; RCA is a prioritization
filter, not a code-confirmed verdict.

## Comment

Posted via `POST /rest/api/3/issue/{key}/comment` (Atlassian Document Format). Default text
lives in `COMMENT_TEXT`. The `comment` subcommand only touches keys you pass explicitly.

## Credentials

`~/.config/jira/credentials.env` (chmod 600): `JIRA_EMAIL`, `JIRA_API_TOKEN`,
`JIRA_BASE_URL=https://coherehealth.atlassian.net`. The token inherits the user's Jira
permissions (verified: `BROWSE_PROJECTS` and `ADD_COMMENTS` = true).

## Troubleshooting

- **HTTP 401/403 on fetch** → token expired or lacks access; regenerate at
  <https://id.atlassian.com/manage-profile/security/api-tokens> and update the env file.
- **No steps extracted on a ticket that clearly has them** → the description used an
  unrecognized heading; add it to `_END_HEADINGS` or the `steps to reproduce` regex.
- **Google Sheet step cells look single-line** → enable text wrapping on that column.
