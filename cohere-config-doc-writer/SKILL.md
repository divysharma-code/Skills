---
name: cohere-config-doc-writer
description: Write Cohere Health engineering-facing feature/config reference documentation in the Confluence "Context → Components → Configuration Example" format (the house style used on pages like "Fax Intake Configuration"). Use whenever Divy asks to document a config block, write up a JSON config schema for a Confluence page, add a new config section to an existing feature-config page, spec out how a config key/feature flag should be set up for a client, or turn a Jira ticket about a new config option into a Confluence entry. This is the OPPOSITE audience from Divy's ELI5 field-guide docs in product-knowledge/intake (those are for Divy himself, learner-facing, analogy-heavy) — this skill is for the engineers/implementation-team readers who actually flip these config keys for a client, so keep it precise and technical, not simplified.
---

# Cohere Config Doc Writer

Cohere's engineering config-reference pages (Confluence, ENG/COH space) follow
a recurring template regardless of feature area. The goal of this skill is
consistency across pages — someone who has read one of these pages should be
able to navigate any other one without re-learning the format. Read
`references/example-fax-intake-configuration.md` once before your first use;
it's the real page this template was extracted from and doubles as a
calibration example — check new output against it if you're unsure whether
something reads "in-house."

## When a page has multiple config blocks

A single Confluence page (e.g. "Fax Intake Configuration") usually documents
*several* related but independently-toggleable config blocks, not one. Each
block gets its own `##` sub-heading and its own full Context → Components →
Configuration Example cycle. Don't merge unrelated config blocks into one
section just because they live under the same parent key — a reader jumping
straight to a heading from a Jira link should get a complete, self-contained
explanation without having to read the sibling sections first.

## Per-block template

Use this structure for every config block, in this order. Skip a piece only
if it genuinely doesn't apply (e.g. no screenshot exists yet) — don't pad.

### 1. Heading
The human name of the feature/config block, not the JSON key
(e.g. "Patient Card Display Fields", not `displayFields`).

### 2. Context
2–5 sentences, prose (no bullets). Cover, in this order:
- **What it enables** — the functional behavior this config controls, stated
  concretely (what a user sees/does differently), not abstractly.
- **Why it exists** — the business or technical rationale, especially if
  there's a non-obvious reason (e.g. "traditionally there has been a single
  fax line across clients which creates a single point of failure").
- **Provenance, if there is one** — if a specific Jira ticket drove this
  config, cite it inline in the exact chip style Confluence renders Jira
  smart-links in: `**TICKET-KEY: Ticket title — Status**` (e.g.
  `**COH-7543: Be able to view "IPA association" info in the patient card —
  Done**`). If it's not yet shipped, use the ticket's actual status instead
  of "Done." Only cite a ticket if you actually have one — never invent a
  ticket key.

Do not add a "Why" paragraph that's just restating the "What" in different
words — if you don't know the real rationale, ask rather than filling the
paragraph with filler ("this improves configurability and flexibility").

### 3. Components
One bullet per top-level JSON key introduced by this block. Nest one level
for child keys inside an object/array-of-objects. For every key, state:
- **What it is** — object/list/boolean/string, and what it controls.
- **What happens if it's absent** — this is the single most load-bearing
  fact in these docs and the source material states it explicitly almost
  every time: "if this config block does not exist, users won't get a list
  to choose from and the default behavior applies" / "if it is missing... the
  fields will not appear even though the frontend code is in prod." Never
  skip this. If you don't know the fallback behavior, say so explicitly
  rather than omitting the point — a missing "what if absent" reads as "this
  is always required," which may be wrong.
- **Constraints, if any** — uniqueness rules ("`speciality` must be unique
  per client"), naming conventions ("`identifier` follows
  ALL_CAPS_WITH_UNDERSCORES"), value resolution rules (lodash-style path
  resolution, `payerCustomFields` matching by `fieldName`), anything a
  config-setter could get subtly wrong.

Format each key name in inline code (`` `keyName` ``), not bold or plain
text — this is what makes the Components list scannable against the JSON
example below it.

### 4. Configuration Example
A single fenced ```json block. Rules:
- Must be syntactically valid JSON — balanced braces, no trailing commas,
  no `...` unless it's clearly a comment about surrounding context (and even
  then prefer a complete, minimal example over an elided one).
- Use realistic values, not placeholders: real-looking health plan names
  ("Healthy Blue Medical"), plausible fax numbers, GUID-shaped product IDs —
  not `"foo"` / `"XXXXXXX"` / `"<value>"`. Precedent from the source material
  literally includes joke placeholder values ("Unhealthy GHP", "Test if this
  goes to Avera") — deadpan realistic beats sterile-placeholder for this
  audience.
- Show the example nested under its real parent key
  (`faxIntakeConfiguration`, or whatever the actual parent config object is)
  so a reader can see exactly where it slots into the full client config,
  not in isolation.

### 5. Optional: screenshot pointer
If a screenshot exists showing where the field/value renders in-product, add
a one-line caption ("Example of places you would see this value (please view
the ticket for all visual areas)") followed by the image. If no screenshot
exists, skip this — don't describe a screenshot that isn't there.

### 6. Optional: "Setting this up for a client" note
Add this whenever the answer to "is this on by default?" is genuinely
worth calling out — i.e. almost always, because the default answer in this
system is usually "no, and there's no error, it just silently doesn't show
up." State plainly:
- Is this block required per-client, or does it apply globally once merged?
- Is it gated behind a feature flag, or does the config block's mere
  presence turn it on?
- What's the failure mode if a client's config is missing this block —
  usually silent (feature just doesn't appear), which is exactly the kind of
  thing that causes "why doesn't this work for Client X" tickets later, so
  it's worth stating even though it feels obvious while you're writing it.

### 7. Optional: verification step
If there's an easy manual UI check for the change, state it as a plain
imperative sentence ("Go to QM and forward a fax, check this new entry is
available") rather than a full test plan — this is a one-liner sanity check
for whoever implements the config, not a QA script.

## Page-level footer (once per page, not per block)

- **Further Information**: links to related design docs or how-to guides,
  if any exist and are genuinely useful — don't pad with a links section
  that has nothing in it.
- **Owning Product Team**: which team owns this config surface (e.g. "PDDE
  team: Intake"). Ask if you don't know — don't guess a team name.

## Tone and register — read this even if you skip everything else above

This is the opposite register from Divy's product-knowledge field guides:

- No analogies, no ELI5 framing, no emoji section markers, no "Questions for
  you" grill section, no glossary. The reader is the person setting up this
  config for a client, not someone building a mental model from scratch.
- Prefer precise declarative sentences over narrative ("The frontend renders
  one row per entry and resolves each value as a lodash-style path against
  the member/coverage payload" — not "basically, think of it like...").
- Still explain *why*, not just *what* — the source material consistently
  states the rationale (single point of failure, PHI leak risk, cross-client
  reporting) even in an otherwise terse register. Terse and unmotivated are
  not the same thing; keep the motivation, drop the hand-holding.
- It's fine, even expected, for Components bullets to get technical
  (lodash paths, fieldName matching, GUID product IDs) — this audience wants
  that, unlike the field-guide audience who explicitly pushed back on that
  kind of density.

## Terminology consistency

Check role/actor vocabulary against the reference doc before using it — not
just the field-level facts. The source material never says "agent"; it says
"users" or "Cohere intake staff." A generic role word that feels natural to
write (agent, rep, operator) can be flatly wrong for this org, and it's easy
to miss on review because the sentence still reads fine — it doesn't look
like an error the way a broken JSON brace does.

Before naming who does an action, anywhere in Context or Components:
- Check `references/example-fax-intake-configuration.md` (or whatever page
  you're extending) for the term it already uses for that role, and match
  it exactly.
- If no reference material covers that role, ask which term is correct
  rather than defaulting to a plausible-sounding one. "Agent" specifically
  is a bad default here — it's ambiguous with insurance agents, AI agents,
  and call-center agents, none of which is what these docs mean.
- Apply this to every noun describing a person or system doing something —
  the person working the fax queue, the person setting up the client
  config, the system component sending the notice — not just the first one
  you write.

## If information is missing

If you don't have enough context to fill in Context, a Components entry's
"what if absent" behavior, the owning team, or a driving ticket — ask rather
than inventing plausible-sounding filler. A wrong "if absent" behavior is
actively worse than an honest gap, because a config-setter will act on it.
