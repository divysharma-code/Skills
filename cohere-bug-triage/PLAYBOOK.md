# Bug Triage Playbook — UAT reproduction

The human side of triage: how to take a bug from the board's left column and either
**reproduce it → Ready for Dev**, or **give up cleanly → Dev Support**. Distilled from
Samuel Hamway's walkthrough of `COH-8229` (BCBS Tennessee, single-select CAQ showing both
Yes *and* No checked). Pair it with the automation in [SKILL.md](SKILL.md): the triage
sheet tells you *which* bugs have steps and *what* codes to use; this tells you *how* to
drive the portal.

## Golden rules (read first)

- **Reproduce in UAT, never DEV.** DEV holds unreleased features that may not match
  production, so a "bug" there can be misleading. UAT mirrors production functionality with
  stable, fake data — it's the source of truth for reproduction.
- **No steps to reproduce = don't work it.** If the ticket has no clear repro steps and you
  don't understand it, don't burn time. (Samuel would even push back on the ticket's author.)
- **Timebox to ~30 minutes.** Most tickets *can't* be reproduced — that's normal. Don't try
  to force it.
- **No quota.** The point is to learn the portal, not hit a number. Ask for help anytime.

## Step 1 — Pick a ticket

Work the **left column** (RALF Support / untriaged), roughly top-down, but be picky.

- **Tip:** Open the bug and scroll down *first* — look for a real **Steps to Reproduce**
  section. That one check decides whether the ticket is workable.
- **Tip:** Skip "Under investigation" items and things that aren't really bugs — they're not
  good reproduction exercises even if worth reading.
- **Tip:** Prefer a **simple health plan** — **GHP or Humana**. Avoid **Tennessee (BCBS TN)**
  when learning; it has a mountain of custom config ("Byzantine") and extra steps.
- **Shortcut:** In the triage sheet, filter **Steps? = YES** and start there; ignore `NO`.

## Step 2 — Understand the bug + gather inputs

- Read the steps to reproduce and the **root cause area** (for `COH-8229` it was the
  **CAQs** — clinical assessment questions; that's where many portal bugs live).
- Collect from the ticket: **payer/health plan, diagnosis code(s), all CPT codes,** any
  auth/tracking number. (The sheet's **Auth Check Details** column already pulls these.)
- **Get a test patient** from the **Test Patient Creation sheet** (UAT):
  - `Ctrl+F` the payer in **column A `healthPlanName`** (e.g. find *Blue Cross of Tennessee*,
    not South Carolina — match it exactly).
  - Grab that row's **Member ID** and **Date of Birth**. (The `Patient Search — Auth Check`
    column bundles Member ID + DOB + Plan for you.)
  - **Tip:** Match the **line of business** too, not just the payer, when the bug is LOB-specific.

## Step 3 — Create the authorization (the actual repro)

Start a **new** auth (start fresh even if a case already exists for that member).

- Enter the **member** (ID + DOB), then the **primary diagnosis** from the ticket.
- **Include *all* CPT codes the ticket lists.** They're usually there because the specific
  combination is what **triggers the CAQ** where the bug occurs — drop one and you may never
  hit the bug.
- **Dates:** if the ticket doesn't give one, use **any future date**. **Rule of thumb:** if
  the ticket doesn't explicitly say a field matters, it doesn't — don't overthink it.
- **"Select all that apply" / unsure toggles:** select **both/all** — CAQs are driven by the
  clinical service, so you want the fullest path.
- **Provider/facility prompts you can't satisfy:** dismiss and continue; put in something if
  forced. Don't upload the ticket's screenshots/docs unless a step depends on it.
- **Plan-specific extra screens** (Tennessee especially): just keep pressing **Continue**.
- If the flow **splits into multiple requests**, go back and **test only the first one**.

## Step 4 — Validate at the CAQs

- Reach the **clinical assessment questions** and answer per the ticket (exact answer often
  doesn't matter — the bug is in the rendering/logic, not your answer).
- **Confirm the reported behavior.** For `COH-8229`: open **Show clinical assessment** and
  verify **both Yes and No are checked** on a single-select question. Match = reproduced.
- **Tip:** Some views (e.g. the pre-submission summary) aren't retrievable after submit —
  that's often *why* the bug is subtle. Capture it live.

## Step 5 — Reproduced? Document and move it

Do all four, every time:

1. **Move** the ticket to **Ready for Dev**.
2. **Comment:** e.g. *"Yes — able to reproduce in UAT."*
3. **Tracking number:** copy it from the **top of the authorization** and paste it in the
   comment so a developer can open the exact case. (A short recording works too — only if
   repro was quick.)
4. **Screenshot** the bug into the comment.
5. **Add the `intake-Kanban` label.** *Every* reproducible bug gets it, so the Kanban team can
   pick it up as a quick win. (No need to @-tag anyone.)

## Step 6 — Can't reproduce? Exit cleanly

- Hit ~30 minutes, or no clear steps, or you don't understand it →
  **comment `unable to reproduce`** and move it to the **Dev Support** column.
- **Ping Samuel** ("can't do this one") if you're stuck — don't grind.

## Health-plan difficulty cheat sheet

| Easier / learn here | Harder / avoid early |
| --- | --- |
| **GHP**, **Humana** | **BCBS Tennessee** (tons of custom config, extra continue-steps) |

## How this pairs with the skill

The `cohere-bug-triage` automation front-loads Steps 1–2: it pulls the untriaged queue,
flags **Steps? YES/THIN/NO** (skip `NO`), and hands you the **Auth Check Details** (CPT/Dx/
auth #) and a matching test member — so you spend your time on Steps 3–5, the actual portal
reproduction, not on hunting for inputs.
