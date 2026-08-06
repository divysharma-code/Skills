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
