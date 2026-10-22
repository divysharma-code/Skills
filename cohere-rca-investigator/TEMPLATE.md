# RCA Template (v2)

Copy the structure. Delete a section only if it truly doesn't apply. Keep each section tiny.
Plain English first. Tag claims VERIFIED / INFERRED / UNVERIFIED where it matters.

---

## <Plain-English title: what went wrong, not the ticket key>

> Source: <TICKET-KEY>, <Fellow/Slack source if any>. Investigated <date>.
> Environment and login: <DEV/UAT/prod, internal or provider>. This limits the finding if internal.
> Confidence: <High / Medium / Low>, because <one line>.

### The short version (ELI5)

<2 to 3 lines. One concrete analogy. No jargon. Define any domain term first.>

### What the reporter is saying

| # | Complaint | Is it true? |
|---|---|---|
| 1 | <claim in plain words> | True / Partly / Not true. <why, one line> |

### The workflow, screen by screen

Titles are the real on-screen titles, taken from the code. Mark any unconfirmed one.

| # | Screen | Happy path | Bug path | Evidence |
|---|---|---|---|---|
| 1 | <real title> | <what should happen> | <where it diverges> | Verified in code / screenshot N / Unverified |

### What actually went wrong

| Layer | What happens | Tag |
|---|---|---|
| <rule / service / screen> | <plain-English behaviour, `path/File:123`, branch develop> | VERIFIED / INFERRED / UNVERIFIED |

### How the code answered the PM's questions

From the SPM and Engineer loop (QNA-LOOP.md). One row per round, in order.

| # | PM asked | Engineer answered | Tag | Evidence |
|---|---|---|---|---|
| 1 | <question> | <plain-English answer> | VERIFIED / INFERRED / UNVERIFIED | `path/File:123` or doc path |

### What the repro showed

One row per screenshot, in order.

| # | Screen | What it confirms | What it does not prove |
|---|---|---|---|
| 1 | <title> | <fact seen> | <limit> |

### What is proven and what is not

| Link in the chain | Status |
|---|---|
| <form state / saved value / downstream effect> | Confirmed / Reported only / Not shown |

### Business impact

| # | What happens | Who feels it |
|---|---|---|
| 1 | <step in the chain> | <role> |

**What I could not connect:** each gap, with the one check and the person who can settle it.

### What I got wrong

Include only if evidence overturned an earlier guess: mine, a pasted RCA's, or an SPM
assumption the Engineer overturned.

| Earlier guess | What the evidence showed |
|---|---|
| <old hypothesis> | <corrected finding and where it came from> |

### Fix options

Only if there was a real fork. Include the council positions and what the code check said.

| Option | Pros | Hole or risk | Verified in code? |
|---|---|---|---|
| <option> | <one line> | <one line> | Yes / No |

### What to fix, and who owns it

| # | Fix | Owner team |
|---|---|---|
| 1 | <specific change> | Intake / Clinical Intelligence / Integrations / Review / Data platform |

### Questions to groom

| # | Question | Ask | My leaning |
|---|---|---|---|
| Q1 | <question> | <role or person> | <recommended answer> |

### Still unverified

| Open item | Who can answer |
|---|---|
| <config not visible / scope question / check not run> | <name or team> |

### Reference

- Tickets: <keys, clones, related>
- Code: <repo, path:line, branch>
- Docs / recordings / threads: <links>
- Test data: <sheet, tab, row; no member IDs or dates of birth in tickets>
- Config / rule IDs: <ids>

---

## Optional follow-ons (only when asked)

- Google Doc with screenshots: see "Doc mechanics" in SKILL.md.
- Jira description: `jira-ticket-writer`, or the shape used for COH-8363 (actual, expected,
  provisional acceptance criteria, out of scope, grooming questions, test plan, evidence).
- Slack ask to the owning squad: `slack-question-writer`.
- Share outside chat: run the-humanizer first.
