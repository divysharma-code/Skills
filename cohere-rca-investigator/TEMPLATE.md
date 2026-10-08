# RCA Template

Copy the structure. Delete a section only if it truly doesn't apply. Keep each section tiny.

---

## <Plain-English title: what went wrong, not the ticket key>

> Source: <TICKET-KEY>, <Fellow/Slack source if any>. Investigated <date>.
> Confidence: <High / Medium / Low>, because <one line>.

### The short version (ELI5)

<2 to 3 lines. One concrete analogy. No jargon.>

### What the reporter is saying

| # | Complaint | Is it true? |
|---|---|---|
| 1 | <claim in plain words> | True / Partly / Not true. <why, one line> |

### What actually went wrong

| Layer | What happens |
|---|---|
| <rule / service / screen> | <plain-English behavior> |
| <next layer> | <what it does with the result> |

<Cite code as `path/File.groovy:123` (branch develop). Mark VERIFIED or GUESS per row if mixed.>

### What I got wrong

Include only if evidence overturned an earlier guess.

| Earlier guess | What the evidence showed |
|---|---|
| <old hypothesis> | <corrected finding and where it came from> |

### What to fix, and who owns it

| # | Fix | Owner team |
|---|---|---|
| 1 | <specific change> | Intake / Clinical Intelligence / Integrations / Data platform |

### Still unverified

| Open item | Who can answer |
|---|---|
| <config not visible / scope question / screenshot not opened> | <name or team> |

### Reference

- Tickets: <keys, clones, related>
- Code: <repo, path:line, branch>
- Docs / recordings / threads: <links>
- Config / rule IDs: <ids>

---

## Optional follow-ons (only when asked)

- Draft a fix ticket: `jira-ticket-writer`, then check it against SUCCESs.
- Ask the owning team on Slack: `slack-question-writer`, one clear ask.
- Share outside chat: run the-humanizer first, then import to a Google Doc.
