# Cohere Master Skills for PMs

A mix of skills I actually use — some built specifically for product work at Cohere Health, some general-purpose (writing, research, design, decision-making) — plus plain-English product-knowledge docs. Each skill sits in its own folder — to use one, copy the folder into `~/.claude/skills/` and call it from Claude Code.

The Cohere-specific ones lean on internal systems (Jira, our tracking sheets, the intake architecture) and only really do anything useful inside the org. Nothing sensitive is checked in here, no credentials, no PHI.

## What's in here

**cohere-bug-triage** is the one I reach for when I'm working through Intake production bugs on Jira board 1487. It grabs the untriaged queue, figures out which tickets actually have usable steps to reproduce, pulls the auth-check details out of each one, and matches every bug to a UAT test patient. It also checks each bug against the intake architecture so you know upfront whether it's even reproducible in UAT or needs to go to eng. All of that lands in a Google Sheet, and for the tickets missing steps it'll draft a comment asking for them (you approve before anything gets posted).

**cohere-config-doc-writer** is the opposite-register companion to the product-knowledge docs below: it writes Cohere's engineering-facing config-reference pages (the "Context → Components → Configuration Example" format used on Confluence pages like Fax Intake Configuration), for the audience that actually flips these config keys for a client — precise and technical, not ELI5. Comes with a real calibration example in `references/`.

**council** convenes four voices (in-context Claude, a Skeptic, a Pragmatist, a Critic) for ambiguous decisions and go/no-go calls — structured disagreement before choosing, not code review.

**grill-me** interviews me relentlessly about a project or product, one question at a time, walking down each branch of the decision tree until we reach shared understanding.

**market-research** produces decision-oriented market sizing, competitor comparisons, and industry intelligence with source attribution — research that supports a call, not research theater.

**marketing-psychology** applies psychological principles and mental models (anchoring, social proof, loss aversion, framing) to marketing decisions and copy.

**ram-writing-style** writes in a specific blunt, text-message-like voice for LinkedIn/social posts — short sentences, real proof, no corporate buzzwords.

**the-humanizer** reviews any draft (blog, LinkedIn, email, Slack) for AI-generated patterns, scores it, and rewrites it in an authentic human voice.

**ui-ux** is a design intelligence reference for web/mobile — styles, color palettes, font pairings, UX guidelines, and chart types across common stacks.

**write-a-skill** is the meta-skill: walks through creating a new agent skill with proper structure, progressive disclosure, and bundled resources.

**product-knowledge/** is where I keep plain-English notes on how Cohere product features actually work — the "how does this thing work" knowledge behind scoping, config, and bug investigation. These are feature docs, not skills. First one in there is the fax intake configuration guide (ELI5-first). See [product-knowledge/README.md](product-knowledge/README.md) for the index.

## Using one

```bash
cp -R cohere-bug-triage ~/.claude/skills/
```

Then just ask Claude Code to run it. Setup and prerequisites for each skill are in its own README / SKILL.md.
