---
name: sprint-health
description: "Show how a Cohere Intake squad's sprints are doing, using Kevin Yan's Application Engineering sprint-metrics method: committed vs added story points (SP), completed SP, Committed Completion, Delivery Efficiency and Final Delivery per sprint, plus what rolled over, where it was stuck at close (Ready to Deploy, In Progress, Blocked), and how much of the miss is release timing. Use when asked how a sprint or squad (Ibex, Aries, Cabra) is doing, to calculate or explain sprint velocity or sprint metrics, why a sprint scored low, what rolled over, or to prepare sprint numbers for a team review."
version: 1.0.0
author: Divy Sharma
license: MIT
metadata:
  method_source: "Kevin Yan, 'Application Team sprint metrics' (Confluence ENG space)"
  requires: ["~/.config/jira/credentials.env"]
---

# Sprint Health

Answers "how is our sprint doing?" with the same math Kevin Yan (Engineering Lead) publishes on the
**Application Team sprint metrics** Confluence page, so the squad's numbers match what leadership sees.
One script, Python standard library only, Jira as the only source.

## Quick start

```bash
SKILL=~/.claude/skills/sprint-health
python3 $SKILL/scripts/sprint_health.py --board 7962 --last 4     # Ibex, last 4 closed sprints
python3 $SKILL/scripts/sprint_health.py --sprint 19131 --json     # one sprint, with rolled-over tickets
```

Creds come from `~/.config/jira/credentials.env` (`JIRA_EMAIL`, `JIRA_API_TOKEN`, `JIRA_BASE_URL`).

| Squad | Board id | Jira project |
|---|---|---|
| Ibex (India) | 7962 | ICS |
| Aries | 192 | IPS |
| Cabra | 43 | COH |

Boards list each other's sprints when they share issues. The script keeps only sprints the board owns
(`originBoardId`). Confirm board ids against the "Team Intake" sheet if a squad changes.

## Kevin's rules (what every number means)

| Metric | Plain English | Formula |
|---|---|---|
| **Committed SP** | Points in the sprint when it started and still in it at close | sum of SP of those tickets |
| **Added SP** | Points that joined after the sprint started (created or moved in later) | sum of SP of those tickets |
| **Total scope** | Committed plus added | |
| **Completed SP** | Points of tickets **resolved** (Done in Jira) on or before the moment someone clicks Close Sprint | |
| **Committed Completion** | How well the squad kept its starting promise | completed committed SP / committed SP |
| **Delivery Efficiency** | Output compared to the starting plan (over 100% means more than planned) | completed SP / committed SP |
| **Final Delivery** | Completion against the final scope | completed SP / total scope |

Details that change the numbers:
- Story points are the estimate in force **at sprint close**. Sub-tasks are excluded.
- Sprint start and close are Jira's timestamps, not the dates written in the sprint name.
- "Completed" means resolved, so **built but not released (Ready to Deploy) counts as zero**.
- A sprint closed late gets extra days to resolve tickets, because the cutoff is the click on Close, not the planned end date.
- Canceled tickets that Jira marks resolved count as completed; tickets resolved before the sprint started still count.

Status bands on Kevin's page: **On track** is 80% or more Committed Completion; **Watch** is below 80%.

## Workflow

1. **Run the script** for the squad and number of sprints the user wants (default last 4 closed).
2. **Show the table** with start and close dates. Always include Jira's actual close date.
3. **Explain every sprint under 80%.** Use the `rolled_over` list: for each ticket give dev, points, status at close
   and how much was `ready_to_deploy_at_close` (finished, awaiting release). Say "release timing" only when that column is non-zero.
4. **Show the release-timing view** when Ready to Deploy points are material: report the sprint with those points counted as done,
   labelled as a looser, non-Kevin view next to his official number. Never replace his number.
5. **Check late closes.** If the close date is days after the planned end, say so, since the extra days flatter the score.
6. **Rolled-over tickets that finished later:** look up each ticket's resolution date. Match it to the squad's
   "Release Captain" tickets (weekly or ad-hoc) only as an inference, and label it as inferred. Jira fix versions are usually empty.

## Caveats to state every time

- Matches Kevin's published Ibex and Cabra pages exactly. Aries can differ by a few SP of added scope on some sprints
  (tickets estimated near the close time), so confirm Aries against his page before presenting.
- Point estimates are read from change history; a ticket re-estimated after close counts at its close-time value.
- Kevin's pages cover sprints that closed in each reporting window; the newest sprint may not be on his page yet.
- Active sprints are not scored. The script reports closed sprints only.

## Common mistakes

- Treating a low score as "work not done". Check status at close first; much of it is built but unreleased.
- Using the sprint name's dates as the work window. Use Jira's start and close.
- Counting sprints from a shared board without the owner filter: you will score another squad's sprint.
- Mixing the looser Ready to Deploy view into Kevin's table without a label.

## Output shape for a team review

1. One-line headline per squad (latest sprint score and trend).
2. The dated table.
3. A short "why" for each sprint under 80%, with the rolled-over table.
4. One sentence on release timing, labelled inferred.

By Divy Sharma, method by Kevin Yan.
