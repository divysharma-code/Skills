---
name: framework-writer
description: Write a detailed, teachable framework document on any topic — a skill, habit, concept, or decision — structured as root-cause diagnosis, an ordered set of layers to build, a decision/mode table where the topic genuinely branches, a time-boxed adoption plan, calibrated targets, and a myths-to-avoid closer. Use when asked to write a framework, a detailed guide, a "for dummies"-style breakdown, a learning plan, or a structured how-to on any subject; or when a draft reads like a flat listicle ("10 tips for X") and needs restructuring into something ordered and buildable.
version: 1.0.0
author: Divy Sharma
license: MIT
---

# Framework Writer

A listicle and a framework can cover the same facts and still be useless in different ways.

| | Reads like | Actually gives the reader |
|---|---|---|
| **Listicle** | "10 tips for public speaking" | A flat bag of advice, no order, no sense of what to do first |
| **Framework** | "Layer 1 → Layer 2 → Layer 3" | An ordered build: each step depends on the last, so doing them in order is itself the instruction |

This skill writes the second kind, for any topic — a skill to acquire, a habit to build, a concept to understand, or a decision to make well.

## Quick start

> Write a framework for negotiating a raise.
> Write me a detailed guide to public speaking, for dummies.
> Turn this into a framework instead of a listicle.

Works the same way regardless of topic. The six-part shape below is the default; **Adapting by topic type** explains which parts bend or drop out depending on what kind of topic it is.

## The shape

```
## Why People Struggle (root causes, not symptoms)
2-4 structural reasons the topic is hard — mechanisms, not "you need more practice."

## The Framework: N Layers, Build in Order
Layer 1 — [foundation]
  - what it is, why it comes first, concrete actions
Layer 2 — [depends on Layer 1]
  - ...
Layer N — [most advanced / hardest to sustain]

## [Decision/Mode table] — only if the topic genuinely branches
| Mode/Approach | When to use it |
|---|---|
Pick this over that, depending on context — not "here are some other tips."

## Adoption Plan (time-boxed)
Week 1 / Week 2 / ... or Day 1-7 / First month — turns the layers into a schedule.

## Realistic Targets
A number, range, or benchmark, so the reader knows what "good" looks like without
over- or under-shooting. State it on its own line, not buried in a paragraph.

## Myths to Avoid
3-5 myth → reality pairs, specific to THIS topic. Each myth must be one a real
person would actually believe, and the reality must say what they'd get wrong
because of it.
```

Format every section with headers, tables, and bullets over paragraphs. Cap prose at 2-3 sentences per block — a framework that has to be read start-to-end defeats its own purpose.

## Adapting by topic type

Not every topic has a real "layer 3" or a real "mode table." Decide the archetype first, then bend the shape to fit it — don't force all six sections onto a topic that doesn't have them.

| Archetype | Example | Layers become | Decision table becomes | Adoption plan becomes |
|---|---|---|---|---|
| **Skill/habit** | speed reading, public speaking | drills to practice, in order of difficulty | when to use technique A vs B | a practice schedule with reps |
| **Concept/knowledge** | how blockchain works, how compilers work | building blocks of understanding, each assuming the last | comparison of related concepts people conflate | a study sequence (what to read/learn first) |
| **Decision/judgment** | negotiating a raise, choosing a database | considerations to work through, in the order they should be resolved | often the centerpiece — this IS the framework | a decision checklist instead of a calendar |
| **Process/system** | running a retro, onboarding a new hire | stages of the process, in execution order | branches for different situations (remote vs in-person) | a rollout timeline |

If a section genuinely doesn't apply (a pure-judgment topic has no "drills"; a one-path skill has no real "modes"), cut it rather than padding it with filler. A five-part framework that's honest beats a six-part one with a hollow section.

## Workflow

1. **Diagnose the real mechanism before writing anything.** Don't invent plausible-sounding root causes, layers, or a "4-week plan" for a topic you don't actually understand well — a confident, well-formatted framework built on fabricated mechanics is worse than a shorter, honest one. If you're genuinely unsure why something is hard or how it actually works, say so and either research it or ask, rather than pattern-matching to what a framework "should" contain.
2. **Pick the topic archetype** (skill/habit, concept, decision, process) using the table above. This decides which sections bend or drop.
3. **Order the layers by real dependency, not by importance.** Layer 2 must actually require Layer 1 to make sense — if the layers could run in any order, they're a list, not a framework, and should be presented as one.
4. **Build the decision/mode table only if the topic genuinely branches.** If the whole framework is one path with no real alternative approaches, don't force a table into existence — cut this section.
5. **Calibrate realistic targets.** Give a concrete number, range, or benchmark. If the field is prone to inflated claims (e.g. "read 1000 wpm with full retention"), name that specific claim as a myth rather than silently avoiding the topic.
6. **Close with myths that are specific to this topic.** Generic filler ("it takes practice," "there's no magic bullet") doesn't count — each myth must be something a real person would believe, and the reality must say exactly what they'd get wrong as a result.
7. **Format for skimming, not linear reading.** Tables and bullets over paragraphs, bold callouts on the load-bearing sentence, headers a reader can navigate without reading start to end.

## Never

- Never fabricate a root cause, statistic, or "layer" for a topic you don't actually know — flag the uncertainty instead of papering over it with confident structure.
- Never force all six sections onto a topic that doesn't have them. A missing section is honest; a padded one is not.
- Never write a myth that's generic enough to apply to any topic. If it doesn't name something specific someone would get wrong, cut it.
- Never bury the realistic-target number inside a paragraph — it needs to be scannable on its own line or in a table.
- Never write a framework as a wall of prose. If a section runs more than 3 sentences without a break, restructure it as a table or bullets.

## If information is missing

Ask who the framework is for (complete beginner vs someone who wants depth) and what archetype the topic is, rather than guessing — a beginner-pitched framework handed to an expert reads as padding, and an expert-pitched one handed to a beginner skips the parts that actually mattered.

## Reference

A full worked example — a skill/habit-type framework (speed reading) built with this exact shape — is in [`references/example-speed-reading-framework.md`](references/example-speed-reading-framework.md). Read it once before your first use to calibrate tone, density, and how the sections render in practice.
