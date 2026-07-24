# Cohere Master Skills for PMs

A few Claude Code Agent Skills I've built for product work at Cohere Health, plus plain-English product-knowledge docs. Each skill sits in its own folder — to use one, copy the folder into `~/.claude/skills/` and call it from Claude Code.

These lean on internal Cohere systems (Jira, our tracking sheets, the intake architecture), so they'll only really do anything useful inside the org. Nothing sensitive is checked in here, no credentials, no PHI.

## What's in here

**cohere-bug-triage** is the one I reach for when I'm working through Intake production bugs on Jira board 1487. It grabs the untriaged queue, figures out which tickets actually have usable steps to reproduce, pulls the auth-check details out of each one, and matches every bug to a UAT test patient. It also checks each bug against the intake architecture so you know upfront whether it's even reproducible in UAT or needs to go to eng. All of that lands in a Google Sheet, and for the tickets missing steps it'll draft a comment asking for them (you approve before anything gets posted).

**cohere-config-doc-writer** is the opposite-register companion to the product-knowledge docs below: it writes Cohere's engineering-facing config-reference pages (the "Context → Components → Configuration Example" format used on Confluence pages like Fax Intake Configuration), for the audience that actually flips these config keys for a client — precise and technical, not ELI5. Comes with a real calibration example in `references/`.

**product-knowledge/** is where I keep plain-English notes on how Cohere product features actually work — the "how does this thing work" knowledge behind scoping, config, and bug investigation. These are feature docs, not skills. First one in there is the fax intake configuration guide (ELI5-first). See [product-knowledge/README.md](product-knowledge/README.md) for the index.

## Using one

```bash
cp -R cohere-bug-triage ~/.claude/skills/
```

Then just ask Claude Code to run it. Setup and prerequisites for each skill are in its own README / SKILL.md.
