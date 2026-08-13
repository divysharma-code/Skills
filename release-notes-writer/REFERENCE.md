# Release Notes Writer — Reference

## Format A — config/behavior change

Mirrors the live Confluence page "Letter Formatting: Release Note (Client
Services)." Best fit when the change is a backend/config improvement rather
than something with new UI to walk through.

```
> Purpose. [One line: who this note is for and what it covers. State plainly
> if no action is required and this isn't a workflow change.]

## Release summary

| Update | Type | Availability | Who it affects |
| --- | --- | --- | --- |
| [one-line name] | [Quality/accuracy enhancement, New capability, Fix, etc.] | [rollout timing] | [who] |

## What's changing

* **[Short bold label].** [One line: what changed, in terms the reader manages.]
* ...

## What [reader] will notice

[1-2 sentences: the visible/felt effect.]

## Action required

[None. / Specific action, stated as an imperative.]

## Availability and timing

[Rollout cohorts/dates if phased.]

## Anticipated questions

* **[Question a reader will actually ask].** [Direct answer. If it's genuinely
  open rather than answered, say that instead of guessing.]
* ...

## Contributors

**Delivery team**
* [Name] — [role: Product/Engineering/etc.]

**Also had a hand in this**
* [Name] — [team, if not core delivery] — [what they did: reviewed, flagged
  a scoping call, consulted on precedent, etc.]

## Reference

[Ticket keys, config names — kept out of the prose above.]
```

**Worked example** (Letter Formatting: Release Note, Client Services —
condensed):

> Purpose. This is an informational release note for Client Services to share
> with clients. It summarizes the letter quality and accuracy improvements
> being delivered in Q2 2026. No client action is required.

| Update | Type | Availability | Who it affects |
| --- | --- | --- | --- |
| Letter formatting and accuracy improvements | Quality / accuracy enhancement | Rolling out through Q2 2026, per plan | Clients where Cohere generates the letters |

What's improving: correct units on therapy letters, letters addressed to the
right recipient, consistent formatting, correct template by line of business,
reliable withdrawal/dismissal letters, administrative denial letters that
previously could be missed.

Action required: none — these are quality improvements delivered by Cohere.

It also closes with an internal-only "How to position to clients" section —
talking points for reps, kept separate from the client-facing content above it.
Worth including whenever the note's real audience (Ops/CX) needs to relay this
to someone else (a client) and would benefit from framing guidance.

**Worked example of the two added sections** (from the Census intake channel
note, IPS-2583):

Anticipated questions:
* **Does this apply to any client besides HMSA?** No — it's config-gated, and
  only HMSA has it turned on.
* **Does this change how TAT is calculated?** No — identical to Portal, only
  the channel label differs.
* **Will clients see new letters for Census requests?** No — it inherits
  standard Portal notification config; no channel-specific letters were
  built (that was explicitly out of scope for HMSA).
* **What if another client wants this later?** Open — turning the config on
  for a different plan would still need someone from Review/Letters to
  confirm they don't need channel-specific notification logic the way HMSA
  didn't. Not answered by this ticket.

Contributors:

**Delivery team**
* Paridhi Jain — Product (drove the ticket, flagged the notification-scope
  question to Review)
* Chaitanya Gopireddy — Engineering (schema, backend, and frontend changes)

**Also had a hand in this**
* Carrie Watson — Review team, confirmed HMSA doesn't need channel-specific
  letter logic for Census, which is why notifications stayed out of scope
* Vidhi Kakani — consulted on precedent from the WISeR project's handling of
  a similar channel/TAT question
* Code review across the three linked PRs: Rafael Zanetti, Anthony Vargas,
  Abhinav Dhara, Sai Teja Pulugurtha

## Format B — new feature/UI change

Mirrors the live Confluence page "Release | Expandable Cards for Appeal
Notes." Best fit when there's something new to actually click through.

```
**[Date] – We're excited to announce [feature] in [location]!** [1-2 sentences:
what it lets the reader do that they couldn't before.]

# Release summary

| Status | Feature | Launch date | User group |
| --- | --- | --- | --- |
| ... | ... | ... | ... |

# Release details

## What's new?

[1-2 short paragraphs — not a spec.]

## How do I use it?

| Description | Image |
| --- | --- |
| [Step 1] | [screenshot] |
| [Step 2] | [screenshot] |

## Anticipated questions

* **[Question a reader will actually ask].** [Direct answer, or "open" if
  genuinely unresolved.]

## Contributors

**Delivery team**
* [Name] — [role]

**Also had a hand in this**
* [Name] — [team, if not core delivery] — [what they did]

# Helpful links

* Jira: [link]
* Documentation: [link]
* Feature flag: [if applicable]
```

## Format C — batch/multi-workstream rollup

For a Slack-native running update that bundles several distinct pieces of
work — different teams, shipped across weeks or months — into one post.
Not a fancier version of Format A/B; use this only when the source really is
a batch, not a single change.

```
[Opening hook — 1 short paragraph. Name the product, credit the teams
broadly, lead with a headline metric or proof point (satisfaction score,
time saved, adoption number). Celebratory tone is fine, but the metric has
to be real, not filler.]

:done: **[Outcome headline, not the internal project name]**
[1-3 sentences: what changed AND why it matters to the reader — don't stop
at the headline.]
Huge S/O: @[everyone who touched this specific workstream]

:work_in_progress: **[Outcome headline]**
[Same shape — what's happening, why it matters, current state.]
Huge S/O: @[names]

:soon: **[Outcome headline], available [date]**
[Same shape, framed as upcoming — give the actual date if you have one.]
Huge S/O: @[names]

[Closing capstone line — one stat that ties the whole batch together, e.g.
zero defects, an aggregate time-savings number.]

Finally, huge shoutout to [leadership/design/technical leads] whose
[design/technical] leadership force-multiplied all of the above.
```

Two things this format does differently from A/B:

- **Status lives per item, not in one table.** `:done:` / `:work_in_progress:`
  / `:soon:` (with a date) replaces the Availability column — appropriate
  when a single post covers items at genuinely different rollout stages.
- **Credit lives per item, not in one end-of-note Contributors section.**
  Each workstream gets its own "Huge S/O" line naming everyone who touched
  *that* piece — including reviewers, ops partners, anyone outside the core
  team. Same non-PDDE-inclusive principle as Format A/B's Contributors
  section, just distributed instead of centralized, because a batch this
  size will have a different contributor list per item.

**Worked example** (a real internal rollup, "Casey" AI assistant — condensed):

> Hi team - we're ready to announce the latest generation of Casey 🤖🤖🤖. Our
> stellar AI teams, in partnership with our amazing operations teams, have
> made huge leaps in Casey over the past couple of months - and the results
> are showing - user satisfaction has grown each survey, now at about 70% for
> internal and external reviewers! We're also seeing time savings and quality
> outcomes for ourselves and our paas clients 🚀

:done: **50% fewer inaccurate answers, rolled out in early May** — Casey's
underlying intelligence got an accuracy upgrade, with no change to response
time. Also just rolled out: better retrieval of information hidden deep
inside tables.
Huge S/O: @Ifeanyi Osuchukwu @Boris Kundu @Will Mau @Hannah Catri @Weiru Chen
@Komal Bodhankar @Leo Mena @Reda Dani @Apurva Tawde @David Coar

:work_in_progress: **Over 100 case-aware review note summary buttons** — case
-specific summary buttons for every delegated clinical area, a dozen already
live, plus a generic review note skill for GHP. Also rearchitected skill
management to make deployment safer.
Huge S/O: @Ciera Von Wolfe @Tomas Rodriguez @Will Mau

:soon: **Claims history as context, available for preprod testing August 14**
— Casey will read a member's claims history when answering questions,
drawing on the Claims History tab going back months.
Huge S/O: @Boris Kundu @Reda Dani @Bri Oribello

Maybe best of all - all of this amazing velocity has come with zero reported
client defects 🚀

Finally huge shoutout to @Melanie Martin, @Laura Wenderoth, @Bri Oribello,
@Betsy Kalven, @J.D. Martindale, @Kenji, @sujata.patil, and @Sridhar Guntoju,
whose design and technical leadership force-multiplied all of the above.

What to notice in this example: the per-item explanation is sometimes *only*
a "what" ("50% fewer inaccurate answers") without a full "why it matters to
you" sentence — that's the one place to go a little more detailed than the
raw source, per item, rather than copying the terseness along with the style.
The status emoji and the S/O line are worth keeping as-is.

## Format D — product narrative (default for Divy)

Not tied to any live Confluence page — this is Divy's own preferred shape,
arrived at after comparing a Format A draft against an ELI5 explainer doc he
judged better-written for the same kind of feature. Best fit for a config or
feature change where the reader benefits from understanding the "why," not
just "what changed."

```
# [Feature name]

## Overview
[1-3 sentences: what this is and what changed, in plain terms a first-time
reader can follow without already knowing the feature.]

## Why We Built This
[The real constraint or scaling problem that made the old approach stop
working — not "improves configurability." If the source doesn't say why,
ask rather than inventing a plausible-sounding rationale, same as Format A.]

## Impact and Outcome
* [Concrete, sourced outcome.]
* [Concrete, sourced outcome.]
* [Concrete, sourced outcome.]
[If a real rollout number or adoption metric isn't in the source, say so as
a footnote instead of inventing one — an honest gap beats a fabricated stat.]

## Why does it matter?
[1-3 sentences of connected prose, one clause per affected group. Do NOT
write this as a label-colon list ("For agents: ... For providers: ...") —
that's a flagged AI pattern (see the-humanizer). Weave it into a real
paragraph instead.]

## How does it work?
[A Piece | What it does table, or short bullets, naming the actual
mechanism — config fields, categories, fallback behavior. Keep field names
here, not in the prose above.]

## Where can I learn more?
[Source doc/page, config path. If the source doesn't cite a ticket or PR,
say so as a quiet footnote rather than guessing at timing or credit.]

## Who is the user?
| Role | How they use it |
|---|---|
[one row per persona]
```

**Worked example** (Faxback Reasons, condensed — the draft that established
this format, 2026-08-13):

> ## Overview
> Faxback Reasons replaces free-text faxback handling with a categorized,
> searchable dropdown. When a fax intake agent needs to send a fax back to a
> provider, usually because something's missing or the case is out of scope,
> they now pick a preset reason instead of typing one from scratch.
>
> ## Why We Built This
> Before this, every payer either shared one hardcoded list of fax reasons or
> had custom logic hand-coded per payer by engineering. As more payers joined
> the Cohere environment, each needing its own specific set of reasons, that
> stopped scaling: a new client with different reasons meant another
> engineering ticket.

Full draft (all seven sections, with the how-it-works table and who's-the-user
table) lives in the chat history that produced it — this excerpt is here to
show register and section length, not to be copied verbatim.

Two things this format does differently from A/B:

- **No headline Availability/Timing or Contributors sections.** When the
  source doc doesn't cite a shipping ticket or PR (common — check whether
  neighboring sections on the same config page cite one before assuming this
  one should), that information drops to a one-line italic footnote under
  "Where can I learn more?" instead of an empty or "TBD" section header. A
  missing section reads as unfinished; a quiet footnote doesn't.
- **"Why does it matter?" is prose, not a table or a label-colon list.** The
  temptation is to write "For agents: X. For providers: Y. For health plans:
  Z." — resist it. That's a flagged AI pattern (label-colon framework). Weave
  the same three points into one real paragraph instead.

## Real feedback on record — read this before drafting

From the Confluence page "2025 Release Notes - ARCHIVE," a retro on Cohere's
own release notes channel. This is the actual bar, not a guess about tone:

- "The current release notes channel is messy. Users have trouble following
  updates and 'don't like scrolling.'"
- "Can't keep track isn't because of emojis — [it's] busy[ness] and time to
  digest paragraphs of text — maybe some things need to be special for ops."
- "Don't want to discourage back and forth, and want to encourage
  relationships. Mini celebrations are important."
- "Is read-only gonna do more harm than good?"

Takeaway: the complaint was never "too much personality." It was length,
scannability, and treating every audience the same. Ops specifically was
flagged as needing different handling than clients get — which is exactly why
this skill defaults to the internal register rather than the strict
client-facing one.

## The existing pipeline this skill slots into

Cohere already runs a lightweight release-notes pipeline for Intake & Review,
started as a pilot in March 2025 (Confluence COH space, "'25 Intake & Review
Product Release Notes Pilot (Week of X)" pages, weekly):

- A Jira custom field, `release notes required? [dropdown]`, flags tickets
  that should surface in that week's note.
- A JQL query filters those tickets by `Planned Release Date` within the week
  and orders them by a custom field — this is a mechanical ticket list, not a
  written note.
- Purpose stated on the pilot page: "keep Customer Success & Client Support
  informed of that week's changes" — the same Ops/CX-adjacent audience this
  skill targets.
- Open ask, unresolved as of Dec 2025 (Jira **RLQ-359**, "Break out the
  release notes by team"): split that script's output by team using a
  Jira-project → team mapping (Intake = COH, KOZA, IPS projects).
- Details on which Jira fields drive this:
  https://docs.google.com/document/d/1USB_lEpchrQV-Mux9JG10f6rlct91KDyPTipl3g0M_c/edit?tab=t.0

In practice: that pipeline produces the raw ticket list (the "source" in this
skill's workflow step 1). This skill's job is turning that list — or a single
ticket, or a config doc — into an actual note in Format A or B.
