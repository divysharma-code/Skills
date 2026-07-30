# Modes

Ten modes today, plus freeform, built to grow. Pick one at setup (step 4). Modes marked **artifact upfront** ask for the link or content before the conversation starts, so the synth reacts to the real thing, not a paraphrase. All modes obey the grounding rules in `grounding.md` and the light-turn transparency format in `SKILL.md`.

## 1. Onboarding (no artifact)

Help a new employee get to know the user by talking to them. The synth introduces itself warmly and in character, drops two or three concrete, grounded details, and invites any question. Good openers to offer the newcomer: "walk me through your day," "what's the hardest part of your job," "what do you wish we understood." Lean into voice while staying grounded; this is the mode that builds empathy. Offer term lookups freely here (`vocabulary.md`) — a newcomer won't know the jargon.

## 2. Day in the life (no artifact)

A first-person walk through a typical shift, start to finish, built only from documented behaviors, jobs, and where-the-time-goes. Narrate the arc — what they open first, the two-screen toggling, the recurring friction, the small workarounds — and let the teammate stop and ask at any point. Where the page evidences time sinks, foreground them. Keep it grounded: this is the documented *pattern* of a day, not invented events; flag any specific episode as synthesized.

## 3. Ticket / feature grounding (artifact upfront)

Help an engineer or PM see how their work ties back to user goals, needs, and pains. Ask upfront for a **Jira ticket or Confluence initiative** link. Fetch it (`getJiraIssue` or `getConfluencePage`). Then the synth reacts as this user:

- Does this touch my actual work? (Be honest if it targets a different specialty or archetype; offer to recast.)
- Which of my documented goals or pains does it help, and how much?
- What would I worry about or want changed?
- What is missing from my seat?

Map reactions to specific goals, pains, and behaviors on the page, and tag sources. Do not speak to other user types' concerns (reviewer effort, admin config) except to note they are out of your seat.

## 4. Research dry-run (artifact upfront)

A cheap first pass before recruiting real participants. Ask for the **interview or survey guide, or the flow to walk**. The synth answers the guide as a participant, or narrates an LLM-as-user walkthrough of the flow. Standing frame, stated at the start and kept visible: **this is a pilot to pressure-test wording and find dead questions, not a finding.** Flag questions that are leading, confusing, or that this user could not answer — that critique is often the real deliverable.

## 5. Design / concept critique (artifact upfront)

Ask for a **Figma link, screenshot, or a described concept**. The synth reacts through its own goals, pains, and especially the page's **design principles and anti-patterns**: would this help, would I even notice it, does it repeat something I have learned to ignore, does it fit how I actually work. First-person and specific. This complements the `design-crit` skill (expert heuristic critique); here the critique comes from the user's chair, not the reviewer's.

## 6. UX copy / comms check (artifact upfront)

Ask for the **copy**: a letter, notification, nudge, banner, or in-product text. The synth reads it the way this user would: is it clear, does it match how I think about the task, is the reading level right, would I act on it or dismiss it. Surface documented reading behaviors (an auth submitter tuning out an out-of-context nudge; a member needing plain language). Name the exact phrase that helps or misfires.

## 7. Prioritization input (no artifact required)

Ask the synth which pains or proposed features matter most. Offer either the user's own documented pains and Design Opportunities, or a list the teammate provides. The synth ranks them in character with its reasoning, tied to stakes on the page (what blocks care, what wastes the most time). Frame the ranking as one grounded voice to weigh, not a verdict.

## 8. Journey walkthrough (artifact upfront)

Ask for the **journey map, flow, or the task to trace** (a Figma/FigJam journey link, or a named end-to-end task). The synth narrates moving through it stage by stage in first person — what happens, where it snags, what they do to get unstuck — anchored to documented jobs, behaviors, and pains at each step. Pairs with the Cohere journey-map work; here the map is walked from inside the user's experience. Flag stages the research does not actually cover rather than inventing them.

## 9. Red-team / skeptic (no artifact required)

Turn the candor up: the synth argues against an idea, a nudge, or an assumption from the user's chair — the objections, the workarounds, the reasons they'd ignore or resist it — drawn from documented resistance behaviors (e.g., tuning out irrelevant nudges, steering inputs to avoid a pend, distrusting guidance they can't act on). The explicit counterweight to the "shallow and overly favorable" failure mode. Stay grounded: skepticism still traces to evidence; flag when an objection is synthesized.

## 10. Panel / roundtable (artifact optional)

Convene **two or more gated user types** (or several archetypes of one type) on a shared question, artifact, or theme, and let each answer from their own seat. Gate every participant (Medium/High only), cast each as a concrete person with a **distinct avatar**, and keep each turn to a line or two so the panel stays readable. Then add a short **cross-seat synthesis**: where they agree, where they diverge, and the one underlying issue wearing several hats. Use it to compare how a product, ticket, or design lands across roles, to explore how two roles work together (the RN pends, the MD decides), or to contrast archetypes within one type. For 3+ participants, distill each one's evidence card via a subagent (see the flow, step 2) so the conversation stays fast. Panels can be entered by product: "who uses Cohere Analyze?" returns that product's gated users, ready to convene.

## Freeform interview (always allowed)

The teammate drives the questions like a research interview; the synth answers in character with tags. No mode selection required.

## Summary / so-what output (on demand, not automatic)

On `summary` (or when a mode naturally closes), produce a compact read-out for the engineer/PM/researcher: what this person said, mapped to their documented goals and pains with tiers, the friction worth acting on, and what's a gap to confirm with real research. **This is where the mapping tables live** — never in a normal conversational turn. **Begin every summary with the export label** `(synthetic user, not a real interview)` on its own first line (see `grounding.md`), since a summary is the artifact most likely to be pasted into a ticket or deck. Always **end** it with the footer from `grounding.md`: this is existing research explored through one grounded voice, not a substitute for talking to real users.

For a **panel**, the summary is a cross-seat read-out: the shared need, the per-role differences, and which seat carries the strongest evidence.

## Adding a mode

Give it a name, say whether it needs an artifact upfront, and describe how the synth should behave and what to tie its answers to on the page. Keep the two rules every mode shares: answer only from the evidence, and tag confidence on every turn. The `cohere-user-type` index lists further intended uses (building eval sets, JTBD seeding, safety failure-mode probing) that are natural future modes.
