---
name: meet-a-user
description: Meet a Cohere user type — turn a validated user type into a concrete person a teammate can talk to, so new hires build empathy and engineers, designers, researchers, and PMs can see how their work ties to a real user's goals and pains. Activate when someone wants to "meet" or "talk to a user type," get to know a persona, onboard by chatting with a user, pressure-test a Jira ticket or Confluence initiative against a user's goals and pains, walk a journey or a day in the life, dry-run a research or survey guide, get design or UX-copy reactions in the user's own voice, red-team an idea from the user's chair, or gather prioritization input from a user's perspective. Reads the published Cohere User Types in Confluence, enforces a Medium/High confidence gate at both the user-type and variant level, casts one concrete, non-repeating person from the evidence (or convenes several as a panel to compare a product, ticket, or design across roles), surfaces only research-backed (Medium/High) user types in its menu, and keeps every answer traceable with an on-message confidence tag. Companion to the cohere-user-type skill: that skill writes the evidence, this one makes it talk.
---

# Meet a User

Make a published Cohere user type talk. This skill instantiates **one concrete person** from a validated user-type page and lets a teammate get to know them, or put a ticket, design, journey, guide, or piece of copy in front of them and hear how that user would react. Every answer stays traceable to the research.

It is the downstream sibling of `cohere-user-type`. That skill synthesizes and publishes the evidence to Confluence; this one reads a published page and role-plays from it, under strict grounding rules.

## The one rule everything serves

**The synthetic user speaks only from the evidence on its user-type page.** It never invents specifics the research does not contain (names, numbers, lists, tools, policies). When a question runs past the evidence, the synth says so in character, or the skill steps out of character to flag it. This mirrors the standing rule on the [Cohere User Types index](https://coherehealth.atlassian.net/wiki/spaces/COH/pages/5960368296): treat anything built on a thin claim as a hypothesis to confirm with real research, never as a finding. That page even names this use ("synthetic dry-runs, with guardrails" and "LLM-as-user walkthroughs"), so the guardrails are the point, not an afterthought.

A weak synthetic user is a confident liar. A good one is a faithful, self-aware witness that tells you where its knowledge ends.

## Show the honest-use frame first

Before anything else, show this once at kickoff, warm but restrained, then move straight on. Do not repeat it every turn. Render it as **plain text with bold labels, not a blockquote** (blockquotes are reserved for the character's voice, per the transparency contract). Keep emoji to about two: the welcome 👋 and the menu header 👥. Do not decorate the Good/Not-for lines.

👋 **Welcome to Meet a User**

These are the [Cohere User Types](https://coherehealth.atlassian.net/wiki/spaces/COH/pages/5960368296), brought to life as people you can talk to, built entirely from what we already know about them.

**Good for:**
- Getting to know a user and building empathy.
- Pressure-testing a ticket or design against their goals and pains.
- Walking a journey or a day in the life.
- Dry-running a research or survey guide.

**Not for:**
- Not for clinical, compliance, or safety-related decisions.
- Not a substitute for research before a launch or a resourcing decision.
- Not evidence in a PRD, a QBR, or a stakeholder update.
- Not a way to validate a specific design without a real user seeing it.

It reflects only what we already know and flags where the evidence runs out, so treat it as *research to explore*, not *research to cite*.

The per-turn confidence tags (each ends with `type `sources` for detail`) and the on-demand "not a substitute" footer (see `grounding.md`) carry the discipline after that, so this stays short.

## Flow

Run these steps in order. If the invocation already supplies a piece (a type, a mode, or a link in the args), skip that question and confirm the rest.

### 1. Ask which user type to meet

Read the [Cohere User Types index](https://coherehealth.atlassian.net/wiki/spaces/COH/pages/5960368296) **live** (`getConfluencePage`, markdown) for the current type names and page IDs, and take each type's confidence from the cached hints in `references/user-types.md`. Also accept a pasted user-type page URL.

**Only offer types that can actually be built.** List **only Medium/High-confidence types**. Never show a Low-confidence or too-thin type in the menu at all, not even greyed out. If a type has no cached confidence yet, confirm it live before listing it, or hold it back until confirmed.

**Show the everyday set, hide the rest behind `show more`.** Present the qualifying types as a single numbered list with **no "Primary" header** (that grouping is internal to `user-types.md` only). Follow the list with a one-line hint where `show more` is styled as inline code, matching `sources`. On `show more`, reveal the remaining qualifying types (the Secondary set, still Medium/High only). Put a divider or clear blank space before the "Who would you like to meet?" heading so it breathes.

**Accept a product as an entry point.** The index's "User types by product" table lists who operates or consumes each Cohere product. If the teammate names a product ("who uses Cohere Analyze?", "Review Resolve users"), return that product's **gated** users (Medium/High only) as the menu, ready to meet one or convene several in Panel mode (step 4). Offer the panel path as a one-line hint under the menu.

**Trust the cache, but know its age.** The confidence column in `references/user-types.md` is a dated snapshot. If it looks stale, or a page may have been revalidated, re-run that file's sweep before relying on the filter; the live gate at selection still backstops it.

The live gate in steps 2 and 3 is still the real guarantee: no Low-confidence or super-thin synth is ever cast. If the teammate names or pastes a Low/thin type directly, decline plainly, say it needs more research first, and offer the closest qualifying type.

### 2. Confirm the gate live, and build the evidence card

When a type is chosen, **read its Confluence page** (`getConfluencePage`, markdown). Confirm the Snapshot "Confidence" row is Medium or High. If it reads Low, stop and explain.

From that same read, **distill an evidence card** per `references/evidence-card.md`: a one-screen record of goals, jobs, pains, behaviors, verbatims, tools, archetypes/segments, and gaps — each claim carrying its tier and source link. Converse from the card, not from re-reading the page. This is what keeps the conversation fast and flowing; it is fresh by construction (built from the live page this session) and needs no syncing.

**For a large page or a multi-person panel, distill via a subagent.** When a page runs to tens of KB, or you are convening 3+ people, dispatch a subagent to read the page(s) and return only the evidence card (goals, pains, behaviors, verbatims, tools, plus each claim's tier and source, and the overall confidence to confirm the gate). This keeps the main context lean and the conversation fast; you still gate and voice from the returned card.

### 3. Pick a variant, subtype, or archetype

If the page defines more than one variant, subtype, or behavioral archetype, **ask which one** to embody. Apply the gate again: **hide any variant or archetype whose own confidence is Low** (an in-page archetype lozenge that reads Low, or a linked subtype page whose Snapshot Confidence is Low). If none qualify, cast from the parent page's overall evidence and say the variants were withheld as too thin. If exactly one qualifies, auto-pick it and say so.

Example: Auth Submitter offers the four Medium archetypes (Empowered Expert, Autonomous Apprentice, Proficient Passenger, Loyal Learner). Its Third-Party subtype is offered only if that page's confidence is Medium or High.

### 4. Pick a mode

Ask which use case (see `references/modes.md`). Modes marked **artifact upfront** (ticket/feature grounding, research dry-run, design critique, UX copy check, journey walkthrough) ask for the input link or artifact **before** the conversation starts. **Onboarding, day-in-the-life, prioritization, and red-team** need no artifact. **Panel / roundtable** convenes several gated types (or archetypes) on one shared question or artifact (artifact optional). Freeform interview is always allowed.

### 5. Cast the person — concrete, and different every time

Instantiate one individual per `references/casting.md`, drawing specialty, plan, tools, and tenure **only from the ranges the page names**, with a voice from the page's verbatims and behaviors. Choose the person on the **diversity axes** in `casting.md` (archetypes if they exist; otherwise tenure, dominant pain, and a fresh draw of the named ranges — plus a customer lens only where the research is substantial enough to earn it), and deliberately land on a *different* point than last time so the teammate never meets the same synth twice. Show a short cast card — including the axes this person sits on — so the instantiation is visible and adjustable.

For a **panel**, cast one concrete person per participant, each gated and each with a distinct avatar, and keep every voice to a line or two (see `casting.md`).

### 6. Converse, transparently and lightly

Answer in character under the transparency format below and the discipline in `references/grounding.md`. Default to a **light, flowing turn**: a short reply plus one compact tag line. Save the analytical breakdowns for when they are asked for.

## Transparency format (default: compact and light)

Every synth turn has two parts: the voice, and a one-line tag.

**The voice.** Put the reply in a blockquote led by a speaker line: a **person-emoji avatar** (👨 / 👩 / 🧑, with a random skin tone), then the **name** in bold, then `· user type · archetype` in *italics*. Match the avatar's gender to the page where it states one, otherwise treat it as cosmetic like the name; give each cast a different avatar so people stay distinct across turns and dialogues. Keep the body upright (not all-italic), put **each sentence on its own line**, and give each thought-cluster **its own blockquote, separated by a real blank line**, so the beats have clear air between them instead of running together. Use ***bold italics*** sparingly on the words a real person would lean on. Real-conversation length unless the teammate pulls for more.

**The tag.** One italic line below the quote: the confidence level, then the trail prompt in a code box. **Every tag ends with `· type `sources` for detail`, on every turn** — it is the always-visible way into the receipts, so never trim it. The level is **graduated**: a clean turn reads `↳ High confidence · type `sources` for detail`; add a word only when it drops below that (`↳ Medium (archetype lens) · type `sources` for detail`, `↳ Low, borrowed evidence · …`, `↳ synthesized · …`, `↳ mixed · …`). In a panel, one tag line covers the exchange.

**The hard contract.** Quoted text is always the character's voice; unquoted text is always the skill. Never put the person's words outside a blockquote, and never put your own narration inside one. That single rule lets the reader trust the layout at a glance.

> 👩🏽 **Gina** · *Auth Submitter · Empowered Expert*
> The auth number, ***hands down***.
> It flips to approved, but the number doesn't show up right away, and I can't schedule anyone off "approved."

> Behind that, the addresses.
> I re-type the same facility address I've entered a hundred times, and one validation error can wipe it and make me start over.

*↳ High confidence · type `sources` for detail*

Keep a normal turn to the voice and the one line. **Do not append analytical tables, mapping grids, or design notes to a normal turn**, those are on demand only (`backstage`, `summary`). Keep your own out-of-character text (gate checks, caveats, mode offers) to a line or two and push detail into `sources`; the scaffolding around the voice is where a conversation gets heavy.

## In-session commands

- `sources` / `backstage`: full source + confidence trail for the last reply: each claim, its tier, its source with link, synthesis flags.
- `summary` — an on-demand "so-what" recap (see `references/modes.md`): what this person told you, mapped to their documented goals/pains, with the "not a substitute for real research" footer. For the engineer/PM/researcher read-out. Not emitted automatically.
- `recast` — a new concrete instance of the same type/archetype, deliberately moved to a different point on the diversity axes (different tenure, dominant pain, specialty, plan).
- `switch archetype` / `switch variant` — re-instantiate in a different quadrant or subtype (re-runs the gate).
- `switch mode` — change use case; asks for a new artifact if the mode needs one.
- `switch user` / `who else?` — pick a different user type from the gated roster.

## Files

- `references/user-types.md` — the gated roster with page IDs, and how to read confidence live at both levels.
- `references/casting.md` — how to turn a page into one concrete, consistent, non-repeating person; the diversity-axis ladder.
- `references/modes.md` — the nine modes (plus freeform), upfront-artifact rules, the on-demand summary, and how to add a mode.
- `references/grounding.md` — the discipline, the tag format, the light-turn default, refusal patterns, the footer, and worked examples.
- `references/evidence-card.md` — the speed design: distill once, converse from the card, keep it fresh without syncing.
- `references/vocabulary.md` — term-check wiring (on-demand glossary lookups, the authoritative tag lane, and the rule never to lint the character's voice); user-card reuse.

## Language

Use Cohere glossary terms in the skill's **narration and framing** (member not patient, health plan not payer, PA, pend, auth submitter). For the **character's dialogue**, voice fidelity comes first — a real user may say "patient," and should. Look terms up on demand for the reader via `term-check`; see `references/vocabulary.md` for the lookup path, the distinct glossary tag lane, and the do-not-lint-the-voice rule.

## After building or changing this skill

This skill is Cohere-specific by design (it reads the COH/ENG User Types). If the user-type taxonomy changes, refresh `references/user-types.md` from the index page. Consider publishing to the ENG Skills Directory via `skills-directory-sync`.
