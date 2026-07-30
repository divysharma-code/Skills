# Playbook

Everything the workflow in [SKILL.md](SKILL.md) refers to. Read the section you need.

---

## 1. The panel loop

Four seats. Each is grounded in **one named artifact**, so it argues from something rather than
from vibes. Seats are **role-labeled, not cast as people** — no names, no avatars, no backstory.
(That is deliberate: `meet-a-user` owns the "quoted text is a character's voice" contract, and
this panel is a review board, not a cast.)

| Seat | Grounded in | Its one job |
|---|---|---|
| 📋 **PM** | Initiative Brief — value framing, client(s), the "so that" clause | Name the outcome, and who is hurt if it ships wrong. Guard scope creep. |
| 🎨 **Designer** | Figma links + documented user pains copied into the Brief | Name the surface, and the state everyone forgets: empty / loading / error / permission / no-config. |
| ⚙️ **Engineer** | Architecture Card, especially its **known failure modes** | Name where it lands, what it cannot do, and the nearest failure mode. |
| 🔍 **QA** | The house test-plan genre + the AC produced in round 2 | Ask only click-answerable questions. Owns round 3. |

QA is the strongest seat here, not a formality. Without a dedicated asker, round 3 collapses into
the engineer testing their own design.

### Round 1 — Approach

One to two lines per seat, then a single line naming the chosen approach.

→ becomes the `## Change` or `## Behavior` prose.

### Round 2 — Best case / worst case → **the AC engine**

Each seat names exactly **one best case** and **one worst case** for the chosen approach.
Conversion is mechanical and mandatory — a round cannot produce nothing:

- Every **best case → one AC bullet**, phrased as observable system behaviour with the *system*
  as the subject. "The system displays…", "Requests without X route to…" — never "the user can".
- Every **worst case → either** an AC bullet phrased as a negative guard ("When the configuration
  is absent, current behaviour is preserved") **or** an **open question**, if answering it needs a
  fact that is not on the cards. Never both. Never silence.

For **config stories** the absent-configuration branch is a *pre-loaded, required* worst case. So
the mandatory present/absent pair (§3) falls out of the protocol itself, instead of sitting in a
checklist that a tired drafter skips.

### Round 3 — Q&A challenge → **the test-plan engine**

QA asks, the other seats answer, and every Q&A converts to exactly **one numbered UAT step** that
names a screen, an input, and an expected observation.

- **Q1 is always** "walk me to it from patient search" → yields steps 1–2 (member ID + DOB,
  create the service request).
- Then one question per AC bullet **that is observable in the portal**. Bullets that are not
  observable produce no step and get listed under *not UAT-observable*.

A short honest click-path beats a fabricated complete one.

### Register switch

Tech/defensive stories run **2 rounds**, have **no AC section**, and QA's questions become the
`_Confirm before building:_` italic list instead of numbered steps. One protocol, two outlets.

### Cost guard

3 rounds × 4 seats × 1–2 lines ≈ 30 lines of debate per story. **Hard stop at 3 rounds**; no
free-form continuation. If round 2 yields more than 8 AC bullets, **merge — do not add.**

The transcript is working material, not output. Show it only if asked.

---

## 2. The two registers — pick one FIRST

The register changes the entire skeleton. Decide before drafting a single line.

### Product / config register

Used for feature and configuration work. Exemplars: `COH-8232`, `COH-8135`, `COH-8043`.

```
<prose intro: what changes and for whom. Often opens "Source: <Monday/Confluence link>".>

## Context
<why now, which client asked, what today's behaviour is>

## Change
<the mechanism. For config work, paste the config JSON with the new key in place.>

## Behavior
* **Configured (non-empty `<key>`):** <what happens>
* **Unconfigured / empty (`[]` or absent):** preserve current behaviour. <state the default explicitly>

## Acceptance Criteria
1. <observable system behaviour, independently checkable>
2. ...

## Dependencies
* <blocking work> — [COH-XXXX](link) **(blocks this; must land first)**

## Design
[<name> (Figma)](link)
```

Heading level is `##` at Story, `###` at Epic. The AC heading varies in the wild
(`## Acceptance Criteria`, `## Acceptance criteria`, `## ACs:`, bold `**ACs**`) — prefer
`## Acceptance Criteria`, and match a parent epic's existing style if it has one.

**Config stories must carry all three:** the JSON with the new key in place; the explicit
present-vs-absent pair; and the config's **scope granularity** (client / delegated vendor / LOB /
encounter type — say which levels are supported and which are not).

### Tech / defensive register

Used for guards, hardening, and follow-ups to a bug. Exemplar: `COH-8127`. **No headings at all**
— structure comes from italic inline labels, and there is **no AC section**.

```
_Parent bug:_ COH-XXXX. _Priority:_ <low (defence in depth) | ...>

_What:_ <the change, naming the real file and the real symbol>

_Why:_ <the gap it closes, and why the obvious fix is not sufficient>

_Confirm before building:_ <the condition under which this ticket becomes unnecessary>

_Related, not in this ticket:_ <the durable fix, if this is the cheap one>

_Depends on:_ <linked work>
```

This register earns its keep by naming real things — source files, line numbers, endpoints. If
the Architecture Card cannot supply them, that is an open question, not a guess.

---

## 3. Field map — what goes where

| Content | Destination |
|---|---|
| Acceptance criteria | **Description body**, under `## Acceptance Criteria` |
| Test plan | **`customfield_10065`** — the live, widely-used field |
| Implementation plan | `customfield_10178` — reproduce the house boilerplate **verbatim** (it is a form, not prose) |
| Authored technical detail | Description: `## Change` / `## Behavior` / `## Engineering plan` |
| Acceptance-criteria custom field `customfield_10720` | **Never.** Effectively unused — writing there is technically valid and socially invisible |
| `components` | **Never.** None defined in the project |

Other fields: Story Points `customfield_10024`, Team `customfield_10001`, Designer
`customfield_10043`. Parent via the real `parent` field, **not** legacy Epic Link
`customfield_10014`. Cross-project parenting to `IPS-` keys is legal (IPS is the predecessor
project).

Issue types: **Story `10001`**, **Epic `10000`**. An `Initiative` type exists but sits at
hierarchy level 0, same as Story — it is **not** a container. Never file there. There is no
`Spike` type; spikes are Stories with "Spike" or "Minispike" in the summary.

Labels: `intake-kanban` is what puts a **parentless** story on the Intake board. Stories under a
well-formed epic usually carry no labels — the parent categorises. Never guess person+client
labels (`YA-ESS`, `VJ-AHP`).

### Test plan genre

A numbered UAT click-path with a real member — **not** a test strategy:

```
1. Navigate to the patient with Member ID <id> and DOB <dob>
2. Create a service request
3. Add procedure code <code> and verify that <specific observable thing> displays correctly
```

For config work, step 1 is the config block to paste, then the verification steps.

If no test patient is known, write `NEEDS_TEST_PATIENT` rather than inventing an ID. The real
lookup (against `Test_Patient_Creation_Worksheet`) is documented in `cohere-bug-triage` — point
there.

Note: the house glossary prefers *member* over *patient*, but this field's own convention says
"Navigate to the patient…". Match the field.

---

## 4. Architecture Card (optional grounding)

Read via `gh` — the repo is not cloned:

```bash
gh api repos/CohereHealth/ralf/contents/<path> -H "Accept: application/vnd.github.raw"
```

**The 3-file spine** (~44 KB — distil it, never hold it raw):

| File | Gives you |
|---|---|
| `intake/architecture/overview.md` | End-to-end flow, 5 entry channels, tech stack, **known architectural failure modes** |
| `intake/source-of-truth/responsibility_complete.md` | Component-level API inventory: real endpoints, services, LOC, method line numbers |
| `intake/architecture/submission_workflow_ownership.md` | The 9-step owner table (§5) |

**Then one topic file, routed by keyword** — do not read them all. In `common/architecture/`:
`auth_vs_sr_data_model.md`, `service_request_lifecycle.md`, `clinical_assessment.md`,
`units_and_approved_units.md`, `domain_boundaries.md`, `delegated_vendor_model.md` (this one
grounds config scope granularity). In `intake/architecture/`: `attachments.md`, `fax_intake.md`,
`referral_management.md`, `advance_notifications.md`, `billable_families.md`.

**Card schema** — one screen, each line carrying its source:

- Components and services this initiative touches (with real names)
- Endpoints and collections involved
- Which of the 9 steps it sits on, and each one's owner
- **Known failure modes** in the neighbourhood (this is what the Engineer seat argues from)
- Config scope levels available, if config work
- Gaps — what the docs do not say

Build it fresh each run. Do not persist it: a stale card that looks authoritative is worse than
no card.

### Traps

- `intake/README.md` advertises five `architecture/*.md` files that actually live in
  `common/architecture/`. Following those links blind returns 404.
- `intake/bug-analysis/` is a single JQL reporting template, **not** architecture.
- CAQ sits mid-flow but is **Clin Intel-owned**, not Intake.

### Precedence and confidence

**ralf > BRD > Jira narrative** for architecture. Jira is authoritative for business intent,
client, and status.

Mark every technical claim: 🟢 verified against ralf · 🟡 owner is in ralf but details are
BRD/config-sourced · 🔴 ungrounded (ralf unreachable). More ink means more risk.

---

## 5. The ownership gate

Of the 9 visible portal submission steps, **only one is Intake-owned**:

| Step | Owner |
|---|---|
| Patient Search · Procedure Code Search | Data Team |
| **Duplicate Check** | **Intake** |
| Service Determination · PA/CRD Check · CAQ · Nudges | Clin Intel |
| Network Check | Integration — *documented as uncertain* |
| Submission | Multi-team (rules = Clin Intel, TAT, SR) |

So a large share of work a PM would naturally ticket is **not Intake's to build**. Run the gate
before writing a technical approach for someone else's component.

### Three verdicts, not two

A binary keep/drop is what turns a gate into theatre.

| Verdict | Meaning | What happens |
|---|---|---|
| `build` | Intake-owned | Gets a full story |
| `context` | Not ours, but our work depends on it | **No story.** Becomes a bullet under `## Out of scope for Intake (context / dependencies)` on the story that depends on it, plus a `## Dependencies` line naming the owning team |
| `flagged-foreign` | Not ours, and substantial enough that someone should ticket it | Named in the run summary as "file with `<team>`". Never drafted as an Intake story |

This has a pre-existing home in the house format: `COH-8248` pairs `## Intake scope (what Cabra
builds)` with `## Out of scope for Intake (context / dependencies)`. The gate fills a section the
best exemplars already have.

### Keeping it honest

1. **Every verdict cites a specific Architecture Card line.** No citation → the verdict is 🟡
   uncertain and goes to Divy. A gate that cannot show its work is a rubber stamp.
2. **Report the counts every run:** `N candidates → M build, K context, J flagged-foreign`. If
   K+J is persistently 0 across real runs, the gate is theatre — say so.
3. **Documented uncertainty stays uncertain.** Network Check is uncertain and Submission is
   multi-team; never launder either into a confident routing.
4. **The gate never deletes information.** Everything gated out reappears — as an out-of-scope
   bullet or a summary line. A gate that makes work vanish gets routed around.

---

## 6. Decomposition

Name candidates the way the house does:

```
<sequence><letter> - <layer>: <imperative behaviour statement>
```

e.g. `2c - Search FE: Select a billable family during auth creation`

Layer ∈ `Data` · `Search FE` · `Configuration` · `Design` · `Letters` · `Scoping`. Supporting
work drops the sequence: `<Feature> - <concern>`, e.g. `Billable Families - Engineering
documentation`, `... - Usage tracking and monitoring`.

Layer order is itself the dependency spine: **Data → Configuration → Search FE → Design →
Letters → Scoping.** State blocking relationships explicitly in each story's `## Dependencies`.

Reference decomposition: `COH-7830` (Therapy Billable Families) has ~20 children following this
convention exactly — the best available yardstick for whether a generated map is plausible.

### The epic-level user story

Exactly one, at Epic level, in the **health plan's voice** — never on a Story:

> As the health plan, I want <capability>, so that <downstream outcome>.

v1 does not edit the Epic. Output the sentence for Divy to paste.

### Thin and mislabelled input

- **Empty epic** (14 of 25 recent epics have no description): ask for the PRD or Monday link, or
  a paste. Do not infer scope from the title.
- **Quarter-bucket epic** (`COH-7956` "Q2 2026 BCBST Gov/Commercial Fast Follows & P1s") holds
  unrelated work and must not be decomposed as a feature. On a match, **ask**.

---

## 7. Exemplars to check against

| Kind | Keys |
|---|---|
| Epic — initiative with scope fencing | `COH-8248` |
| Epic — value-framed with PRD link + real decomposition | `COH-7830` |
| Epic — quarter bucket (do not decompose) | `COH-7956` |
| Story — config | `COH-8232`, `COH-8043` |
| Story — feature FE under an epic | `COH-8135` |
| Story — tech/defensive register | `COH-8127` |
| Story — output/PDF | `COH-8194` |

Spot-check a draft against the matching key before offering to create it. Do not paste exemplar
bodies into this playbook — they go stale the moment someone edits a ticket.

---

## 8. Related skills

- **`cohere-bug-triage`** — triages what already broke; owns UAT test-patient lookup. Opposite
  direction from this skill.
- **`meet-a-user`** — voices the user from research. Deliberately **not** auto-invoked here (its
  synthetic-output label exists to prevent exactly the leak a Jira ticket would create). Natural
  handoff: draft the stories here, then run its Panel mode against them as a separate,
  human-initiated pass.
- **`cohere-config-doc-writer`** — for the engineer-facing Confluence config reference that a
  config story may need alongside it.
