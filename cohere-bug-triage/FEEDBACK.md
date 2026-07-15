# Feedback & Improvement Backlog — cohere-bug-triage

A case-by-case backlog for improving this skill. Work items one at a time; check a
box when it's shipped. Each case records where the feedback came from, the symptom,
and the proposed fix so future-me (or a reviewer) has the full context.

Not a spec — a living punch list. Add new cases as they surface from real triage runs.

---

## Source: "Sam / Divy Check In" — 2026-07-14 (Samuel Hamway)

Sam reviewed a live run and trained on real tickets. The through-line: **the skill
answers "is this testable in UAT?" but the daily decision is "who owns this and where
does it go?"** Ownership was ~80% of the session.

### Case 1 — No team-ownership or routing logic  ⬜
- **Symptom:** Skill only emits `Testable in UAT?` (✅/🟡/❌) + a layer tag. It never
  says which team owns the ticket or what action to take. That's the missing half of triage.
- **Ownership rules from the session (seed the map):**
  - Case / auth **statuses → clinical intelligence (rules engine)**, NOT intake.
    (The "cases falling into pending" ticket was canceled & redirected.)
  - **Auth retriggers → integrations**, NOT intake. (Example: CoH-8228.)
- **Fix:** Add an **`Owner team`** column backed by a hard-coded ownership map, and a
  **`Routing action`** column: `Test in UAT` / `Reassign to <team>` / `Move to investigation`
  / `Comment: needs steps`. This is the highest-priority case.

### Case 2 — RALF is treated as authoritative, but it miscategorizes  ⬜
- **Symptom:** Step 5 / REFERENCE rubric grounds RCA in RALF. Sam flagged RALF gets it
  wrong on the tickets that matter: tagged a Health Partners **auth retrigger as "UI related"**;
  mis-tagged **CoH-8228 as intake** (it's integrations).
- **Fix:** Demote RALF to a *hint*. Cross-check its call against the Case 1 ownership map;
  when they disagree, mark the row **low-confidence / human review** instead of asserting.

### Case 3 — Low-context tickets get a forced verdict  ⬜
- **Symptom:** `Problem (plain English)` and `RCA` assume the narrative is rich enough to
  classify. Sam confirmed tickets often don't say whether it's business / UI / data, so the
  skill guesses and over-claims certainty ("it's an art, not just science").
- **Fix:** Detect thin context and output **"🟡 needs human judgment / investigation"**
  rather than a false ✅/❌.

### Case 4 — Missing "investigation" pathway + no Pendo capture  ⬜
- **Symptom:** A no-repro-steps ticket with a **Pendo link** was moved to **investigation**
  (an engineer can trace it), not bounced to the reporter. Current flow only has
  `NO steps → comment asking for steps`.
- **Fix:** (a) Extract **Pendo links** into a column; (b) add a branch — no steps *but* has
  Pendo/enough signal → suggest **investigation**, not a "needs steps" comment.

### Case 5 — Extend "draft, don't assert" beyond the comment gate  ⬜
- **What's already right:** the confirm-before-post gate matches Sam's caution — the skill
  never auto-acts on a live board.
- **Fix:** Apply the same posture to the `Owner team` / `Testable` / `Routing` columns —
  present them as drafts for human confirmation, not verdicts.

---

## How to use this file
- Pick one unchecked case, implement it in `scripts/triage.py` + `SKILL.md` + `REFERENCE.md`,
  test on a small `fetch --limit`, then check the box and note the commit.
- Keep the ownership map (Case 1) as the single source of truth once it exists; link RALF
  to it rather than the other way around.
