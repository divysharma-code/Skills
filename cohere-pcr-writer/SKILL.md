---
name: cohere-pcr-writer
description: Draft Product Change Request (PCR) tickets for the Cohere Ticketing System (CTS) "Internal Other Requests → Product Change Request" form. Grounds every field in a verified source instead of guessing — reads the actual process rubric, finds a precedent ticket making the same kind of ask, and flags live-form fields it can't see (dropdowns) or facts only Divy knows (scope, urgency) instead of fabricating them. Use when Divy asks to write/draft a PCR, a CTS ticket, a "product change request," or needs to ask another team (PlatCon, IntEng, Letters/Clinical Config) to execute something already validated in Preprod.
---

# Cohere PCR Writer

PCR tickets fail review for a predictable reason: they get written from what the
requester remembers rather than what's actually true — vague summaries, no SME named,
a config ask routed like a feature ask, dropdown fields invented to look complete. This
skill's whole job is to make every field trace back to something checked, not assumed.

## Workflow

1. **Read the source, not the retelling.** Open every doc/link/Slack quote the request
   references before drafting anything. Extract: scope (which client(s)/system(s) are
   actually in play), who validated what and where, what's still pending. Don't summarize
   Divy's summary of the source — read the source.

2. **Pull the governing process doc before drafting.** Confluence page **4110516468**
   ("Product Change Requests fka Product Feedback Process") has the real field rubric —
   with good/bad examples — for Summary, Description, and Business Impact. Use it instead
   of freelancing what a "professional-sounding" ticket looks like.

3. **Check whether this is a "config executed by another team" case.** Page **4468604991**
   covers exactly that shape: PM confirms the functionality already exists via config →
   Help Desk creates a follow-up ticket for PlatCon/Letters(Clinical Config)/Integrations
   to actually execute it. If that's what's happening here, that's the applicable process,
   not a feature-build PCR. Page **4331470852** ("Configurations Overview") maps every
   config surface to its owning team — use it to get the SME / owning-team field right;
   never guess a team name.

4. **Search Jira for a precedent ticket that made the same kind of ask.** Even a precedent
   for a different client/feature tells you: the title convention, the phrasing pattern,
   whether this ask-shape is actually *accepted* through this form (precedent overrides
   policy text when the two conflict — say so explicitly if that happens, don't silently
   pick a side), and the linked ticket chain shape (see REFERENCE.md for the chain pattern
   and a JQL tool-quirk to avoid blowing the token budget on this search).

5. **Sanity-check the ticket type fits the ask.** A PCR explicitly excludes: pure TS
   config work (unless a working precedent contradicts the general rule), clinical content
   changes, bugs, IT requests, and activation-scoped asks. If you find a tension between
   the written policy and what you're about to file, tell Divy — don't resolve it silently
   either direction.

6. **Draft every field against the rubric + precedent phrasing**, not generic
   ticket-writing instinct:
   - Summary states the *problem*, not the feature name.
   - Description synthesizes any linked Slack/doc history inline — never just links to it.
   - Business Impact answers "why does solving this matter," concretely, not a restatement
     of the ask.

7. **Separate fact from judgment; ask on judgment, flag on unverifiable.** Things like
   ticket scope (one client vs. several), urgency, or which of several clients to name are
   Divy's calls, not inferences — ask directly rather than picking the "reasonable" default
   and hoping. Live-form dropdowns you can't see the options for (Value Type, Customer,
   Line of Business, etc.) — say plainly these are best-guess or unfillable rather than
   fabricate a plausible-looking value. A confident wrong answer is worse than a flagged gap.

## Output format

Present the ticket field-by-field, in the exact order the CTS form uses (see REFERENCE.md
for the standard PCR field list so Divy doesn't have to repaste the form every time).
Close with two short callouts if applicable: (a) which fields need a manual check against
the live dropdown, and (b) any process-fit caveat surfaced in step 5.

See [REFERENCE.md](REFERENCE.md) for the Confluence page details, the Jira precedent-chain
shape, a tool-quirk note on searching Jira without blowing the token budget, the standard
CTS PCR field list, and a worked example.
