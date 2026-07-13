# Divy's Cohere Master Skills for PMs

A small, growing collection of [Claude Code](https://claude.com/claude-code) **Agent Skills** built for Product work at Cohere Health. Each skill lives in its own folder and can be dropped into `~/.claude/skills/` to use.

> **Internal:** references Cohere systems (Jira, internal sheets, intake architecture). Visible to CohereHealth org members. No credentials or PHI are stored here.

## Skills

| Skill | What it does |
|-------|--------------|
| [`cohere-bug-triage`](./cohere-bug-triage) | Triages Intake production bugs (Jira board 1487): pulls the untriaged queue, classifies steps-to-reproduce, extracts auth-check specifics, matches a UAT test patient, RCAs each bug against the intake architecture to flag whether it's reproducible in UAT, and drafts comments on tickets missing steps — all into a Google Sheet. |

## Using a skill

```bash
cp -R cohere-bug-triage ~/.claude/skills/
```

Then invoke it from Claude Code (see each skill's `README.md` / `SKILL.md` for setup and prerequisites).
