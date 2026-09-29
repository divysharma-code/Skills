---
name: slack-question-writer
description: Turn a rough question or request into a short, paste-ready Slack message that gets answered fast, using the SUCCESs framework from Made to Stick (Simple, Unexpected, Concrete, Credible, Emotional, Story). Checks what's already documented before asking, leads with the ask, tells the reader exactly what shape of answer to send back, phrases every guess as a question, keeps sensitive data out, and strips AI-sounding filler (zero em dashes). Works for a DM, an @mention in a channel, a thread reply, or an open question to a group. Use when the user wants to ask someone something on Slack, draft a Slack question or request, ask a channel for help, request data, access, or a doc from a colleague, chase an answer, or says "write it for Slack", "help me ask X", or "use the SUCCESs framework".
---

# Slack Question Writer

One output: a Slack message a busy person can read in 15 seconds and answer without
asking a follow-up. Self-contained. Run the five steps in order.

## Step 1: Pin down the ask

Pull these from the user's note. If something's missing and a reasonable guess exists,
make the guess and flag it in the output. Only ask the user when guessing wrong would
waste the recipient's time.

| Need | Why it matters |
|---|---|
| Who's being asked (person, channel, thread) | Sets tone and whether to @mention |
| Each question, split one per ask | Two asks in one sentence get half an answer |
| What the answer unblocks | Feeds the Emotional line |
| What the user already knows or checked | Feeds the Credible line |
| The shape of answer they want back | Feeds the Concrete line |

## Step 2: Do the homework (if tools allow)

Spend one quick pass on whatever sources you can reach (docs, wiki, ticket tracker,
repo search) for the thing being asked about. Both outcomes help:

- **Found it:** the user may not need to ask. Say so, or narrow the question to the real gap.
- **Didn't find it:** that becomes the hook. "I couldn't find X in Y or Z."

No tools or no time? Ask the user what they already checked. Never claim a search
that didn't happen.

## Step 3: Shape it with SUCCESs

A checklist, not a template. A one-line DM might only need Simple and Concrete.
Never pad a message to hit all six.

| Principle | For a Slack question | Example |
|---|---|---|
| **Simple** | Each ask gets a bold one-line headline. Number them if there's more than one. The first line alone should say what you want. | `*1. What's Census, and how does it work?*` |
| **Unexpected** | One line that gives them a reason to answer now, usually the gap or a contradiction. | "Couldn't find it anywhere as an intake channel." |
| **Concrete** | Spell out the answer shape: columns, time window, format, yes/no, a link. Offer a best guess to correct, because correcting is faster than explaining from scratch. | "`Client \| Channel \| # of auths \| Period`, last 3 to 6 months" / "Is it the daily inpatient list?" |
| **Credible** | Name what you already checked, in a few words. | "Checked the docs wiki and Jira." |
| **Emotional** | One plain line on what the answer unblocks. No hype, no flattery. | "So I know where to focus my testing." |
| **Story** | Usually skip. Use only when the question doesn't make sense without a 1 to 2 sentence before/after. | "Tested with X, got Y, expected Z." |

## Step 4: Apply the Slack rules

- **Lead with the ask.** Context goes after it, never before.
- **Greeting:** one short line or none. No "Hope you're doing well."
- **Length:** 3 to 6 short lines per ask. Longer than that means a doc, or a thread with a TL;DR on top.
- **Easy out:** end with "or point me to where I can pull it myself" or "or tell me who owns this."
- **Guesses are questions.** Any assumption in the message ends in a question mark, never stated as fact.
- **Sensitive data:** never put PHI, PII, credentials, or customer records in the message. When asking for data, say "counts only" or "de-identified" explicitly.
- **Slack markup, not Markdown:** `*bold*` (single asterisks), `_italic_`, `` `code` ``, plain `1.` lists. Double-asterisk bold may not render.
- **Emoji:** one at most.

## Step 5: Language pass

Search for each pattern below. Don't just eyeball it.

| Cut | Fix |
|---|---|
| Em dash `—` | Comma or period. Count the character; the answer must be 0. |
| "Just wanted to flag / reach out / circle back", "Looping in X for visibility" | Say what you need. |
| "Sorry to bother you", "Not sure if this is the right channel, but", "I might be wrong, but" | Cut. Just ask. |
| "At your earliest convenience", "Please be advised" | Too formal for Slack. Cut, or give a real date if timing matters. |
| leverage, streamline, robust, seamless, utilize, comprehensive, facilitate | use, simplify, solid, works everywhere, use, full, help |
| "it is / does not / cannot" where a person would contract | "it's / doesn't / can't" |

## Output

1. **The message** in a blockquote, ready to paste.
2. **How it uses SUCCESs:** a small table mapping each principle to where it shows up, with skipped ones marked. Leave it out if the user only wants the message.
3. **Check before sending:** every guess or assumption in the message, plus anything the user should swap for their own words. Leave it out if there's nothing to check.

## Worked example

Rough input: *"ask Alex what Census is, and for intake stats per client by channel, non-PHI"*

> Hey @Alex, two quick asks while I ramp up on Intake:
>
> *1. What's Census, and how does it work?*
> I've got Portal, Fax and Phone mapped, but couldn't find Census as an intake channel in our docs or Jira. Is it the daily inpatient list facilities send us? Who sends it, how often, and does it create new auths or update existing ones?
>
> *2. Intake volume by channel, per client*
> Could you share a sheet with counts only, no PHI? Something like `Client | Channel | # of auths | Time period`, last 3 to 6 months. It'll tell me which channels matter most per client, so I know where to focus.
>
> If there's a dashboard I can pull this from myself, just point me to it. Thanks!

Check before sending: the "daily inpatient list" line is a guess for Alex to correct.

## Never

- Never invent a search result, number, or fact to sound credible.
- Never state a guess as a fact.
- Never put PHI, PII, or secrets in the draft.
- Never send it yourself. Draft only. If a Slack tool is connected, still show the draft and get an explicit OK before sending.
