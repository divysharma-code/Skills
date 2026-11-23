# sprint-health

A Claude Code skill that shows how a squad's sprints are doing, using Kevin Yan's sprint-metrics method
from the **Application Team sprint metrics** Confluence page.

## Install

```bash
git clone https://github.com/divysharma-code/Skills.git ~/code/Skills
cp -r ~/code/Skills/sprint-health ~/.claude/skills/sprint-health
```

You need a Jira API token in `~/.config/jira/credentials.env`:

```
JIRA_EMAIL=you@coherehealth.com
JIRA_API_TOKEN=...
JIRA_BASE_URL=https://coherehealth.atlassian.net
```

## Use

Ask Claude: "how is Ibex doing on sprints", "why did Fireworks score low", "sprint metrics for Cabra".

Or run directly:

```bash
python3 ~/.claude/skills/sprint-health/scripts/sprint_health.py --board 7962 --last 4
```

Python standard library only. Reads Jira only.
