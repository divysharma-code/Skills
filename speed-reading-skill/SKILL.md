---
name: speed-reading-skill
description: Turn a Jira ticket plus its Confluence config/feature doc into a short, skimmable summary that answers seven fixed questions instead of a generic release note. Use when asked to speed-read a ticket, explain a shipped feature quickly, or turn a ticket + doc into a plain-English explainer.
---

# Speed Reading Skill

Give it a Jira link and the Confluence doc for the same feature. It reads both, then
answers the same seven questions every time. No extra sections, no guessing.

## How to use it

> Speed-read this: [Jira link] and [Confluence link]

## What it does

1. **Reads the two links first.** Jira ticket (summary, description, AC, comments) and
   the linked Confluence doc. These are the only required inputs.
2. **Answers exactly these questions, in this order:**
   - **Overview** — one short paragraph: what shipped, who it's for, is it live.
   - **Why We Built This** — the actual problem, from the ticket. Not "improves
     configurability."
   - **Impact and Outcome** — bullets. What changed and what deliberately didn't
     (things explicitly out of scope count as outcomes too).
   - **Why does it matter?** — the real consequence for the reader, one paragraph.
   - **How does it work?** — one plain sentence walking through the mechanism,
     step by step.
   - **Where can I learn more?** — just the Jira ticket link and the Confluence
     doc link. Nothing else. No PR links, no extra reference material.
   - **Who is the user?** — a two-column table, Role / How they use it. Roles
     only, never names.
3. **Keeps every section short.** If a section runs more than 3-4 sentences, cut it.

## Rules

- Plain English. No config-key names, field names, or internal jargon in the prose.
- No em dashes. No AI-sounding filler ("leverage", "seamless", "robust", etc.).
- Don't add facts that aren't in the ticket or the doc. If something's unclear,
  say it's open rather than guessing.
- Don't editorialize past what's asked. If nobody asked for contributors, code
  links, or a rollout timeline, leave them out.

## Example

**Input:** a Jira ticket + its Confluence config doc for a new intake channel.
**Output:** the seven sections above, each 1-4 sentences or a small table, ready
to paste straight into a doc or a Slack post.
