# SPM and Engineer Q&A loop

Two voices argue the ticket into shape while the code is read. The **SPM** (senior product
manager) grills. The **Engineer** answers only from evidence, by reading RALF (Cohere's internal
docs repo) and the code. The human is not asked anything until the loop ends.

This is the `grill-me` method, built in, so no other skill needs to be installed.

## Grill rules (from grill-me)

- One question at a time.
- Walk the decision tree. Settle a question before the ones that depend on it.
- Every question comes with the SPM's own recommended answer.
- If a document or the code can answer it, go read it. Do not ask a person.

## The two voices

| Voice | Who | Job | Must not |
|---|---|---|---|
| SPM | Fresh subagent | Ask the next best question, with a recommended answer and what evidence would settle it. Say DONE when no open branch is left. | Read code. Answer its own question. |
| Engineer | Fresh subagent | Answer from RALF (`main`) and code (`core-platform`, `frontend` on `develop`). Cite `file:line`. Tag VERIFIED, INFERRED or UNVERIFIED. | Guess. Answer from the ticket text alone. |
| You (orchestrator) | Main agent | Pass messages, keep the log, check the answers that change the diagnosis. | Skip the check. |

Give each subagent only its prompt below plus the compact context named there. Never the whole
chat. No member IDs, dates of birth or names in any prompt.

## One round

1. **SPM turn.** Prompt:
   > You are a senior product manager grilling an engineer about ticket `<KEY>`. Brief:
   > `<the step-2 plain-English brief>`. Q&A so far: `<log>`. Open branches: `<list>`.
   > Ask ONE question, the next one that unblocks the most. Return exactly: `Question`,
   > `Why it matters` (one line), `My recommended answer`, `Evidence that would settle it`.
   > If nothing is left, return `DONE` and a one-line reason.
   > Standing question: whenever the last answer was "nothing in code does X", your next
   > question must ask whether config, data or another service could do X.
2. **Engineer turn.** Prompt:
   > You are an engineer answering a PM's question about ticket `<KEY>`. Question: `<Q>`.
   > Read RALF (`CohereHealth/ralf`, branch `main`) and code (`core-platform` and `frontend`,
   > branch `develop`, via `gh`). Return exactly: `Answer` (plain English), `Tag`, `Evidence`
   > (`file:line` or doc path), `Could this live outside the repo?` (config, database, another
   > service), `What I did not check`. If it cannot be answered from code or docs, say
   > UNVERIFIED and name the one check and the person who could settle it. Do not guess.
3. **You.** Log the round. If the answer changes the diagnosis, open the cited file and confirm
   the claim yourself before accepting it. If the Engineer contradicts the SPM's recommended
   answer, mark it "SPM assumption overturned" (it goes in "What I got wrong").

## Stop when

| Condition | Then |
|---|---|
| SPM returns DONE | Move on. |
| 12 rounds reached | Stop and list the open branches. (8 cut off the last branches on COH-8147.) |
| The same branch comes back UNVERIFIED twice | Park it and move to the next branch. |

## What comes out

| Piece | Goes to |
|---|---|
| Round log: SPM asked, Engineer answered, tag, evidence | Template section "How the code answered the PM's questions" |
| Overturned assumptions | "What I got wrong" |
| Parked and UNVERIFIED branches | "Still unverified", then step 11 (the human grill) |

## Search budget

GitHub code search allows 10 queries a minute. Fetch the repo file tree once and filter it
locally, then read files with `gh api .../contents/<path>?ref=develop`. Use code search only for
a name the tree can't find, and space those calls out. If a search is rate-limited, wait for it
instead of reading the empty result as "not found". RALF redirects some Integrations questions
to `integration-ai`, so follow that pointer.

## Why the standing question exists

On COH-8221 the first finding was "Cohere has no QMB block", true only for code. The block
messages live in health-plan configuration, which neither a code search nor RALF can show. A
loop that accepts "nothing in code" as "nothing" repeats that mistake.

## If you cannot spawn subagents

Run both voices inline, in turns, labelled SPM and Engineer, with the same rules. Say once that
they share one context, so the questions are less independent.
