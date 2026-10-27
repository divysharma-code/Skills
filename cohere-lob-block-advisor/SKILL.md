---
name: cohere-lob-block-advisor
description: Answer "can we block this auth or referral for a specific line of business (LOB), plan type, product type or health plan, and how do we set it up?" for Cohere Intake. Checks the three places a block can live (rules-engine redirect, referral management config, hard-coded code), says which one applies to auths versus referrals, gives the setup steps with example JSON, names the owning team, and can draw the flow as a one-page diagram. Use when asked to block, stop, hide, gate, restrict or turn off submission by LOB, line of business, plan type, coverage type, product type or plan name; when a ticket like PCR-749 or PCR-1170 asks for it; or when someone asks "do we support blocking X for client Y".
---

# Cohere LOB Block Advisor

One question in, one answer out: **is a block by LOB (line of business, the kind of
coverage a member has, such as Commercial, Medicare Advantage or Medicaid) possible
today, for auths, for referrals, or neither, and what is the exact setup?**

The answer is never "it depends". It is a verdict per request type, the setup that
works now, and the code change needed if nothing works.

## Core rules

1. Tag every claim **VERIFIED** (read in code, config or a ticket this run), **INFERRED**
   or **UNVERIFIED**. Findings in [REFERENCE.md](REFERENCE.md) are dated. Re-check the
   ones the answer depends on before repeating them.
2. Read what a key does in code, not what its name says. `referralRequiredCoverageType`
   sounds like a block and is not one (see REFERENCE.md).
3. Auths and referrals are separate questions. A block that works for one often does not
   work for the other.
4. Explain every term on first use. The reader is usually a PM, not an engineer.
5. Draft only. Nothing is posted to Jira, Slack or Confluence unless asked.

## Workflow

1. **Pin the ask.** Which client or health plan, which LOBs or plan types, auths,
   referrals or both, and block (stop the user) or hide (remove the button). If the ask
   names only a plan, find out whether plan name or LOB is the real key (see step 4).
2. **Check the three places a block can live, in this order.**

   | Place | How to check | Covers |
   |---|---|---|
   | Rules-engine redirect at patient selection | Read the rule list for the health plan; read `ServiceRequestRuleService.groovy` for what a patient-search rule can see | Auths and referrals together |
   | Referral management config | Fetch the live JSON (portal: My Account, Configuration Management, Feature dropdown, pick the plan) or the pasted config | Referrals only |
   | Hard-coded in code | `gh search prs "<TICKET>" --owner CohereHealth`, then read the diff on `develop` | Whatever the code says |

   `core-platform` and `frontend` merge to `develop`. The API's default branch is stale,
   so always fetch with `?ref=develop`. Fetch the repo tree once and grep locally. Code
   search allows about 10 queries a minute.
3. **Find where the member's LOB comes from.** At patient search, rules read the primary
   coverage that is active today (not the service date). Check which field holds the
   value for this client: the LOB enum, the raw payer string, product type, plan type or
   product ID. Raw strings that are not in the enum come through as null, so match on the
   raw string for those.
4. **Test the key.** Ask whether the proposed key separates the groups. If two LOBs share
   a product type (for example HMO used for both Commercial and Medicare Advantage),
   a product-type list cannot split them. Get one real member from each group through a
   subagent on the test-data sheet and compare the coverage fields. No member IDs or dates
   of birth in tickets or Slack.
5. **Give the verdict.** Fill the verdict table below.
6. **Give the setup.** Steps and example JSON, grounded in the real schema. Mark any part
   of the JSON you did not read as UNVERIFIED and tell the user to build it in the rule
   builder instead.
7. **Name gaps.** Frontend-only enforcement, service date versus today, delegated-vendor
   override (the vendor config replaces the health plan's whole object, one layer deep),
   and what lives outside the repo.
8. **Offer the diagram.** If asked, build a one-page diagram with the `artifact-diagramming`
   and `artifact-design` skills: the member path from patient search to the block or the
   pass-through, the missing check drawn as a dashed box, and a table of options. If the
   Artifact tool is refused, save the HTML locally and say so.
9. **Say who to ask.** Data questions go to Data Platform (the eligibility feed). Rules go
   to the rules owners. Referral config code goes to Intake. Include the exact question for
   each person.

## Verdict table (fill this in every time)

| Request type | Supported today? | Mechanism | Hard stop? | Owner | Evidence |
|---|---|---|---|---|---|
| Auth | Yes / Partly / No | | | | |
| Referral | Yes / Partly / No | | | | |

## Output shape

Plain English first, tiny sections, tables over prose.

1. Short answer: one verdict per request type.
2. A one-line analogy.
3. Verdict table.
4. Setup steps with example JSON.
5. Gaps and what to confirm.
6. Who to ask, with the exact question.
7. Reference footer: ticket keys, config keys, `file:line`.

## Boundaries

- Never edit a live config. Propose a diff and tell the user to create a version first
  ("Create Version" in the config editor).
- Never claim a rule exists without reading the rule list for that plan.
- If a source (Jira, GitHub, the config) is unavailable, say which step was skipped and
  lower the confidence. Do not fill the gap with a guess.
- Not filing a ticket is the default.
