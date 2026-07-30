# Vocabulary: sounding on-domain without breaking character

Two jobs here, and they must not be confused:

1. **Help the reader understand the jargon** the synth uses (a new hire won't know `CAQ`, `pend`, `PTA`, `peer-to-peer`, `backOffice`). This is where `term-check` earns its place.
2. **Keep the skill's own narration on-vocabulary** (member not patient, health plan not payer, PA, pend, auth submitter).

What these jobs are **not**: a license to rewrite the character's speech to match Cohere's internal style guide. See "Never lint the character's voice" below — this is the trap.

## Wire in term-check, on demand

`term-check` is the fast, local, read-only glossary counterpart (it never writes Confluence). It lives at `~/.claude/skills/term-check/` with:

- `scripts/lexicon_lookup.py` — look up a term and get its authoritative gloss.
- `scripts/term_check.py` — lint a block of text against the lexicon (used for **narration only**, not the character; see below).

**Depend on it; do not copy its lexicon in.** term-check owns its own freshness (`build_lexicon.py`, `patch_lexicon.py`). Copying its export into this skill would create a stale duplicate — the exact drift problem the evidence card is designed to avoid (see `evidence-card.md`). Call its script at the moment of need instead.

Escalate to the heavy `cohere-glossary` skill only on a miss, exactly as term-check itself does.

### When to look a term up

- **Onboarding / day-in-the-life:** when the reader asks "what's a CAQ?" / "what does *pend* mean?", run `lexicon_lookup.py` and answer authoritatively. Optionally, the first time the synth uses a heavy term in a turn, offer a one-line gloss ("— a CAQ is the clinical assessment question set —") so a newcomer isn't lost. Keep it light; don't gloss every term every turn.
- **Any mode:** if the reader is clearly unfamiliar, a quick lookup beats guessing.

### The distinct tag lane

A glossary definition is a **different kind of fact** than user-type evidence. "Auto-approval means X" is an authoritative system definition; it is **not** evidence that this person behaves a certain way. Tag it in its own lane so the two never blur:

```
↳ glossary definition (authoritative) — not user-research evidence about this person
```

Never let a glossary gloss inflate the confidence of a behavioral claim. The person's behavior still traces only to their user-type page and its tiers.

## Never lint the character's voice

The glossary's preferred/non-preferred guidance ("member not patient") is **Cohere's internal writing standard** — how *we* write, not how a provider-office medical assistant actually talks. Real submitters say "patient." Forcing the character onto glossary-preferred terms makes them *less* authentic to satisfy a style guide they don't work under. That is the opposite of grounding.

The rule:

- **Glossary vocabulary governs the skill's narration and framing** (the parts spoken as the tool, not as the person). `term_check.py` may lint *that* text.
- **The character's dialogue is left alone.** If the cast person would say "patient," they say "patient." Voice fidelity outranks the style guide inside the quotation marks.

## User cards (reuse from cohere-user-type)

Each published user type also has a Figma/FigJam **user card** (built by `cohere-user-type`, Step 9 / `user-card.md`; cards live in section `142:766` of Figma file `odiG9VvpoEjZKkTqRlQBnF`). When a teammate wants a visual companion to the person they're meeting — especially in onboarding — point them to the card, or offer to surface it. It's the same evidence in a glanceable form; it does not change what the synth may assert.
