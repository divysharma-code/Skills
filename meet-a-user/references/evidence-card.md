# The evidence card: speed without staleness

User-type pages are large. Re-consulting the full page on every conversational turn is what makes the chat feel slow and stilted. The fix is to read the page **once**, distill it into a compact **evidence card**, and converse from the card — so each turn is a fast lookup, not a re-read.

## The principle (same one the skill already lives by)

`references/user-types.md` is described there as "a convenience cache… confidence is always confirmed live at selection." The evidence card is that same principle one level deeper:

> **The Confluence page is the source of truth. The card is a disposable, derived artifact. Build it live, verify at the moment of use, never treat it as authority.**

## v1: in-session card — fresh by construction, nothing to sync

Build the card at kickoff, from the same `getConfluencePage` read that runs the confidence gate (step 2 of the flow). Then converse from the card.

- **No per-turn reads.** This is the entire speed win — the cost you're removing is re-reading a huge page every turn, not the single setup read.
- **No staleness.** The card is born from the live page each session, so it cannot drift mid-session, and the next session re-reads. There is nothing to keep in sync.
- **Do not modify `cohere-user-type` to push card updates.** Pages are edited directly in Confluence by humans (UXR, authors), not only through that skill — a push model would silently miss every hand-edit and give false confidence. Invalidation must be **pull-based and owned by this skill**, keyed to something that changes on *any* edit.

### What the card holds

A one-screen distillation, each claim carrying its **tier** and **source link** so tags stay instant and honest:

- Identity ranges: role/synonyms, credentials, specialties/settings, plans, tools/EHRs (the casting dice).
- Goals, Jobs to Be Done, Pain Points, Behaviors — each with its tier and source.
- Verbatims (the richest voice cues).
- Archetypes / documented segments (the diversity axes; see `casting.md`).
- Metrics that color sentiment (e.g., a recent CSAT/NPS move).
- The Snapshot confidence and any "Coverage & Gaps" — so the synth can name where its own evidence runs thin.

Keep it tight. If a turn needs a detail the card omitted, that is the rare moment to consult the cited source — not the whole page.

## Keep the turn itself light

Caching is only half the speed story. The other half is the turn format (see `grounding.md`): the **default turn is a short in-character reply plus one compact tag line.** The analytical tables and mapping breakdowns are on demand only (`backstage`, `summary`) — never every turn. A flowing conversation is short answers at real-conversation length; let the reader pull for more.

## Optional phase 2: cross-session persistence

Only if scale justifies it (e.g., a whole cohort onboarding across many sessions on the same handful of types). Then you may persist cards to disk — but the moment you persist, you own invalidation:

- Stamp each card with the source page's `version.number` and `lastModified`.
- At kickoff, do a **cheap version check** against the live page. Match → use the cached card (skip even the setup read). Mismatch → rebuild from the fresh page, then converse.
- Model the refresh on how `term-check` handles its lexicon: a build step plus a version stamp, incremental patch on a small change, full rebuild on a structural one.
- Ownership stays here, in the reader. `cohere-user-type` remains unaware cards exist; its only job is to keep the Confluence page true.

Do not build phase 2 preemptively. v1 (in-session, fresh by construction) delivers the flowing-conversation speed with zero coupling and zero staleness risk.
