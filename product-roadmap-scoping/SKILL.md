---
name: product-roadmap-scoping
version: 1.0.0
author: Divy Sharma
license: MIT
description: "Scope a product ask (a client change request, a Monday or Slack item, or meeting notes) into a scoping doc that converts into a Jira Epic plus one discovery ticket. Uses Jobs To Be Done (JTBD) and the reviewing lead's scoping rules: treat the requester's proposed behavior as points to validate, not a spec; decide configuration vs feature flag; leave UX copy and button decisions to the UX owners; keep discovery async before any meeting; and end with next steps for designers, engineers and the PM. Use when asked to scope a request, write a scoping doc or epic description, turn meeting notes or a Monday item into an epic, break a client ask into jobs, decide config vs feature flag, or say what the next steps are for design. Not for writing stories (jira-ticket-writer) or a Confluence initiative brief (cohere-initiative-doc-writer)."
metadata:
  optional: ["Atlassian MCP (to create the Epic and discovery ticket)", "Fellow MCP (to read the source meeting)"]
---

# Product Roadmap Scoping

Turns one raw ask into one scoping doc. The doc is the source for a Jira Epic (JTBD = Jobs To Be Done). It is not a set of engineer-ready tickets. Those come after discovery.

## Core principle

Scoping defines the outcome and the open questions. It does not design the answer.
- The requester's proposed behavior is a hypothesis to test.
- UX (user experience) owners decide how users experience the change.
- Engineers decide how many tickets the work needs.

## Step 1: Size the ask

| Size | Signal | Output |
|---|---|---|
| Small, well understood | One screen, one config value, no UX question | One Jira ticket written directly. No epic. |
| Moderate or unclear | Several user types, copy or button questions, config and tracking questions | This skill: scoping doc, then Epic + discovery ticket |
| Large, new capability | Several phases, new workflow, new client segment | Use cohere-initiative-doc-writer first |

## Step 2: Write the jobs (JTBD)

For each person affected, write one job statement:

> When [situation], I want [motivation], so I can [outcome].

Then list the forces, using only what the source actually says:

| Force | Question it answers | Example |
|---|---|---|
| Push | What hurts today? | Users submit something that gets rejected |
| Pull | What would the new way give them? | Only allowed options are shown |
| Habit | What do they do now, and why does it stick? | Manual workaround |
| Anxiety | What worries them about change? | "Will this look like a bug?" |

Mark anything you infer as `(inferred)`. State the outcome, not the solution. "Users should not think it is a bug" is an outcome. "Show a red banner" is a solution, so it goes under open questions for the UX owners.

## Step 3: Apply the scoping rules

These come from the reviewing lead's guidance. Keep the wording close to the original.

1. **Treat the requester's proposed behavior as points to validate, not a rulebook.** Check each point: Does it make sense? Can we build it? Is it good for user experience? Is it allowed under regulation?
2. **Configuration or feature flag?** Use configuration when clients choose to turn the behavior on or off (for example, a true/false value set per health plan or per delegated vendor). Use a feature flag when every client will eventually get it. Record the choice and the reason.
3. **UX decisions belong to the UX owners.** The PM says that user experience will be affected and critiques the options the owners propose. The PM does not decide copy, whether a button is hidden or disabled, or what a message says. Those become questions for the UX owners.
4. **Tracking is a question, not a build.** Ask whether tracking is useful (for example, how often users try the blocked action). Usually it is not in the first release. Write the question down.
5. **Do not predict the ticket count.** Ask engineers how many tickets the work needs.
6. **Async before meetings.** UX and engineers read the doc and post questions before any call. Post the doc in the team channel ahead of grooming so people can prepare.
7. **Sequence.** If one part is clearer, start there and return to the other part later.
8. **Name the requesting client.** Say whether the ask is one client's rule or a general rule. Name the person who will confirm it.

## Step 4: Write the scoping doc

Plain English first. Short sections, tables and bullets. Every acronym and term gets a glossary entry. Jira keys and config names go only in the Reference section at the bottom.

```
# [Outcome-first title, plain English]

## Summary
Three sentences at most: what changes, for whom, and why now.

## Glossary
| Term | Plain meaning |

## Problem today
One concrete example (for example, one procedure code that maps to two services).

## Who is affected
| Person | Job (JTBD) | Pain today | Forces |

## Desired outcome
Observable behavior only. No UI decisions.

## Requester's points to validate
| # | Point (kept in the requester's words) | Validated? | Notes |

## Guidance received
Quotes from the review, with the role of the speaker. Keep the wording.
| Role | Guidance (verbatim) | Applied as |

## Decisions made
| Decision | Why |

## Open questions for UX owners
- Questions only. No answers written for them.

## Open questions for engineering (discovery)
- What to scope, how many tickets (engineers answer), config location.

## Tracking
In or out of the first release, and why.

## Sequencing
What goes first and why.

## Next steps
### Designers (UX owners)
- Decide the user-facing behavior for each open UX question.
- Bring options. The PM critiques them.
- Deliverables: copy options, button-state options, message options.
### Engineers
- Discovery ticket: scope the change, confirm where config lives, estimate the ticket count.
- Read this doc before the next grooming.
### PM
- Create the Epic and discovery ticket from this doc.
- Post the doc in the team channel before grooming.
- Review the write-up with the reviewing lead in the next 1:1.

## Reference
Source item, meeting ID, Jira keys, config names. Nothing above this section uses Jira keys.
```

## Step 5: Convert to an Epic

- **Epic title:** the doc title.
- **Epic description:** Summary + Problem today + Desired outcome + Decisions made + open questions for each owner. Copy the wording as written. Do not paraphrase the guidance.
- **Attach** the full doc, or link to it.
- **Discovery ticket:** one ticket linked to the Epic, holding the engineering questions and the words "engineers propose the ticket count".
- Create the Epic only after Divy confirms. Nothing goes to Jira without a yes.

## Worked example (from a 30 Oct 2026 review)

Ask: one procedure code can map to two clinical services. Some clients allow both in one request; one client wants only one.

- **Job:** When a code could mean two services, I want the portal to offer only what my health plan allows, so I do not submit something that gets rejected and do not think the system is broken. (Outcome: "they should not think it is a bug".)
- **Decision:** Configuration (true/false per health plan or delegated vendor), not a feature flag. Reason: health plans choose.
- **Point to validate:** The requester's proposed single-selection behavior. Check feasibility, UX and regulation.
- **Tracking:** Question only. Not in the first release.
- **UX owners:** Copy for the restriction, so users do not read it as a bug.
- **Next steps:** Designers bring copy options. Engineers scope in discovery. PM writes the Epic and reviews in the next 1:1.

## Self-check before you hand it back

- Every acronym and term is expanded on first use and in the glossary.
- The requester's points are quoted or kept close to their wording, not rewritten into a spec.
- The PM has not decided UX copy, buttons or messages.
- No ticket count is predicted.
- No Jira keys above the Reference section.
- No em dashes. Tables and bullets, not dense prose.
