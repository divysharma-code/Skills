# Playbook

The method behind [SKILL.md](SKILL.md). Read the section you need.

---

## 1. Journey patterns

Four journeys cover most changes. Write them in this order — the first two are mandatory, the
last two apply whenever they exist.

### Journey A — the new path, end to end *(always)*

Start where a real user starts, not where the feature starts. If the change is a field on step
four of a submission flow, the journey begins at step one, because that is how the bug will be
found.

Follow the value **past the save**. A change that captures data is not proven correct until you
have seen where that data lands — the review screen, the summary, the document, the outbound
payload, the notification.

### Journey B — the default path that must stay untouched *(always)*

Run the same flow the way it works today, without invoking the new behaviour. This is the
journey that catches "we added a branch and the main road now has a pothole." It is the single
most-skipped journey and the cheapest one to write.

### Journey C — the round-trip *(whenever the data can be edited)*

Save, leave, come back, edit, save again. Then repeat wherever else the record can be reached:
edit before submit, edit after submit, a follow-on or continuation, a different entry channel,
a read-only view someone else sees.

State-carrying UI — toggles, modes, filters — is where this journey pays. A control that
defaults correctly on create and forgets on edit is a classic.

### Journey D — regression for the unaffected population *(whenever a flag or config gates it)*

If a change is gated, two populations exist. Run a full flow for someone **not** getting the
change and confirm they cannot tell anything happened. Configured versus unconfigured, flag on
versus flag off, client A versus client B.

An ungated change has no Journey D — say so rather than inventing one.

---

## 2. Edge-case generators

Features rarely fail on the happy path. Walk this list and keep what applies; two or three real
ones beat ten generic ones.

| Generator | The question it asks |
|---|---|
| **Pre-existing records** | What about rows created *before* this change shipped? Does the new code read old data correctly? |
| **The removed thing** | Something was deleted — a checkbox, a field, an option. What happens to records that used it? |
| **Missing optional data** | The new path assumes a value exists. What happens when that record does not have it? |
| **Stale state after a switch** | The user changes a mode or filter mid-flow. Does the old selection survive when it should not? |
| **The boundary** | Right at the on/off line: config present vs absent, flag flipped mid-session, a record straddling both. |
| **Downstream assumptions** | Who consumes this data and did they assume the old shape? Rules, routing, documents, integrations. |
| **Permissions** | Does every role that can reach this screen behave correctly? Can a role that should not see it get there? |
| **Empty, loading, error** | No results, slow response, failed save. Easy to forget, cheap to test, common in production. |
| **Duplicate and re-entry** | Submit twice, refresh mid-flow, use the back button. |
| **The deleted key** | Something was *removed* from a config or payload rather than changed. Does the old value survive server-side? Many APIs only bind keys present in the request, so a deleted block silently persists and can trip validation that reads it. |
| **The loading race** | The gate reads identity, permissions, or a remote config. What shows during the window before that resolves? A control that defaults to the wrong state for 200ms and then corrects is a real defect, and it's visible on a hard refresh. |
| **The deliberately-unchanged sibling** | A code comment saying "this must stay independent of X" names a second control on the same screen that must *not* follow the new behaviour. Test that it didn't. |
| **The pre-validator record** | A new constraint blocks bad data from now on. It does nothing about rows saved before it shipped. What does the new code do when it reads one? |
| **Wrong case vs wrong spelling** | If matching is case-insensitive, these are two different tests with two different results. Wrong case should still match; a typo should silently match nothing — and if nothing validates the value, the config saves either way. |

**Pick by consequence, not by count.** If the change decides money, routing, or who gets
notified, spend the edge cases there. Note it explicitly when a generator does not apply — that
is coverage information too.

---

## 3. The three exclusion buckets

State exclusions in the plan. An unrunnable step is worse than an absent one, and silent gaps
read as coverage.

| Bucket | Contains | How to write it |
|---|---|---|
| **Another lane** | Colours, layout, spacing, visual behaviour of a control | Name the role or person who owns it |
| **Not clickable** | Field writes, payload shape, collection updates, job triggers | Move to *questions for engineering* |
| **Out of scope** | Work split into other tickets, or explicitly deferred | Cite the ticket that owns it |

---

## 4. Questions instead of guesses

You will not know which fields and collections a change touches. That knowledge comes from
having done post-release reviews on the same system, and the shortcut is to ask an engineer —
not to infer it from a ticket description.

Ask these, adapted:

1. Which records and fields does this write? Only the obvious one, or does anything else update
   as a side effect?
2. Is the outbound shape identical across the new and old variants, or does a consumer need to
   branch?
3. Does any existing rule, validation, or routing logic assume the value this change makes
   variable?
4. Is there a migration or backfill, and what happens to records that predate it?

Then a short list for product: unresolved scope, unnamed configuration values, disagreements
between the ticket and its grooming notes, missing test data.

**A named blank is a finding.** A guessed field name is a defect you authored.

---

## 5. Shape and register

Write steps a tester can follow without knowing the ticket:

- **Numbered, sequential, executable.** One action and one observation per step.
- **Name the screen, the input, and the expected result.** "Verify it works" is not a step.
- **The system is the subject.** "The request submits and the summary shows X", not "the user
  can see that it worked."
- **Lead with the setup block** — configuration to apply, account or record to use, flag state.
- **Open with the one most likely failure**, in a sentence, before the steps. It is what
  survives skimming.

Match the house format wherever the plan will live. If the tracker has a convention — a
numbered click-path, a Given/When/Then, a table — follow it rather than importing a template.
Read two or three recent well-regarded plans on the same team and mirror them.

---

## 6. Common assumption traps

Step 5 of the Workflow asks you to check the described test approach against real docs before
trusting it. This is where that checking itself goes wrong. Read this list before you turn a
finding into a flagged gap — a wrong catch sends someone chasing a question that doesn't apply,
which is worse than not raising it at all.

| Trap | What it looks like | Fix |
|---|---|---|
| **Wrong population** | A risk documented for one group (e.g. non-portal users with no account) gets applied to a different group (e.g. SSO users) because the two sit in the same doc or the same initiative. | Check exactly who the original risk was written about before reusing it for someone else. |
| **Stale doc, current ticket** | An old planning or review doc scored a *broader* initiative as risky or unready; the ticket in front of you may be a narrower, already-resolved slice of it. | Confirm the ticket's actual scope before importing an old doc's verdict wholesale. |
| **Proxy field, not the real gate** | A manual test edits a field that happens to change the outcome, but isn't the field the code actually branches on. | Ask which field or flag the code checks — don't infer it from what worked once. |
| **Confident tone, no source** | A question sounds sharp because it's specific, not because it's grounded in something real. | Every open question should point at a doc, a flag, or a line someone actually said — not a hunch dressed up as diligence. |
| **AC as truth** | The acceptance criteria describe behaviour the merged code doesn't implement — often because someone edited one AC inline and left the bullets beneath it contradicting the edit. Writing a step that asserts the AC produces a "failure" that is really a doc bug. | The shipped code wins. Test what's built, and raise the AC mismatch as a defect on the ticket. |
| **Example values as real values** | A config sample in a ticket gets copied into the setup block. The names look plausible and one of them is subtly wrong — a missing underscore, an invented group. | Find the real list in a docs repo or from whoever provisions it. Cite the source. Treat an unverified value as a placeholder. |
| **The test that can't fail** | The account, client, or config used for testing can't match the thing being gated, so the on and off paths render identically and a dead feature reads as a pass. | Before step one, confirm the tester's identity actually falls inside the gate. Ask what a false pass would look like — if you can't tell it apart from a real one, the setup is wrong. |

### Self-update

After using this skill, if you (or the person you handed the plan to) catch a trap that isn't
listed above, add a row here — pattern, what it looked like, the fix — instead of only noting it
somewhere private. The next ticket benefits, not just this one.

---

## 7. Mining the diff

The ticket is what someone intended. The diff is what exists. Read it before writing steps —
it converts questions you were about to ask a human into facts, and it is usually the difference
between a plan that restates the ticket and one that finds something.

Find the PR from the ticket key. Read four things, in this order:

| Read | What it gives you |
|---|---|
| **PR description** | The author's own before/after in prose, usually clearer than the ticket. Often states the resolution order and what was deliberately left alone. |
| **Changed-file list** | Surfaces nobody mentioned. Two files where you expected one means two screens to test. Test files named after a component tell you what the author thought was risky. |
| **The diff of the main logic file** | How edge cases actually resolve — the null branch, the fallback order, the guard clauses. |
| **Code comments inside the diff** | The highest-value lines in the whole exercise. Authors explain the non-obvious right where they handled it. |

What to extract:

- **Bugs the devs already hit.** A defensive fix with a comment explaining why ("the backend only
  binds keys present in the request, so a removed key leaves a stale value") is a defect that
  reached someone's machine. It becomes a top-priority step, phrased as the user action that
  triggered it — not as the code that fixes it.
- **Which half is merged.** Backend and frontend often live in different repos on different
  branches. If one is merged and one is open, the plan has two phases and must say which steps
  run today. Check the merge target, not just the merged flag — a PR merged to `develop` won't
  appear on `main`.
- **Guard clauses that name a state you hadn't considered.** `if (user === undefined) return` is a
  loading race. A normalising function is a case-sensitivity test. An early return is a fall-through
  path that needs its own step.
- **"Must stay independent of" comments.** These name a control that must *not* change. Test it.
- **Real values.** An `example =` annotation or a test fixture carries values closer to reality
  than a ticket's illustration — though still confirm the authoritative list elsewhere.
- **How errors surface.** Whether a rejection lands as a red toast, an inline field error, or a
  silent no-op is the expected result of your negative test. Quote the string the user sees, not
  the status code.

If there's no PR yet, say so — that's a finding, and it means the plan is written against intent
and will need a pass once code exists.

## 8. Adapting this to your organisation

The method is portable; four inputs are local. Answer these once and reuse them.

| Input | Question | Where it usually lives |
|---|---|---|
| **Test data** | Where do valid test accounts or records come from? | A shared sheet, a seeding script, a fixtures repo. **Never invent one.** |
| **Architecture** | Where can you look up which services and collections a change touches? | An architecture repo or docs site, a schema reference, or an engineer |
| **Lane boundary** | Who owns design QA, and what is functional validation's share? | Team convention — confirm it, do not assume it |
| **Destination** | Where does the plan live, and in what format? | A tracker field, a test-management tool, or the ticket body |

Record the answers at the top of this file for your own setup, so the next run does not
rediscover them.

### Sibling skills

If a sibling skill already owns one of these inputs, call it rather than duplicating it — test
data lookup, ticket authoring, and architecture grounding are commonly owned elsewhere.
