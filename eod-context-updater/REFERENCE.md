# Reference: writing the EOD sentence

Used by step 7 of `SKILL.md`. Every comment is still one sentence in `eod-updater`'s format.

## SUCCESs pass (from Made to Stick)

A checklist, not a template. Run it on every draft. Never pad a line to hit all six, and
never break `eod-updater`'s format to fit one.

| Principle | For one EOD sentence | Check |
|---|---|---|
| **Simple** | Open with what changed or was decided. The first few words alone should tell a reader the outcome. | Does it start with the outcome, not background? |
| **Unexpected** | If there's a blocker, surprise, or reversal, say it plainly. Quiet days don't need one. | Is the one thing that isn't routine in there? |
| **Concrete** | Name the real detail: PR number, step count, config key, who is waiting on whom. | Could a reader act on it without opening the ticket? |
| **Credible** | Every fact traces to a Jira comment, Fellow call or Slack thread you read. Thin evidence gets a thin sentence. | Can you point to the source for each claim? |
| **Emotional** | Say what it unblocks or who is waiting. One plain clause, no hype. | Does the reader know why it matters? |
| **Story** | Skip. One sentence has no room for a before and after. | Skipped. |

## Example shape

Illustrative, from ICS-26:

`🤖 **EOD Status (2026-09-30):** Moved to Ready to Deploy after PO review, with all 18 test-plan steps passing on frontend PR #21874; it now waits for the next release.`

## Language pass

Search for each pattern. Don't just eyeball it.

| Cut | Fix |
|---|---|
| Em dash `—` | Comma or period. The count must be 0 (`eod.py post` also rejects it). |
| "Just wanted to flag", "FYI", "as discussed" | State the fact. |
| leverage, streamline, robust, seamless, utilize, comprehensive | use, simplify, solid, works everywhere, use, full |
| "it is / does not / cannot" | "it's / doesn't / can't" |
