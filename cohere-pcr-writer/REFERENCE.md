# Reference

## Confluence pages (COH space) — don't rediscover these

| Page ID | Title | Use it for |
|---|---|---|
| `4110516468` | Product Change Requests (fka Product Feedback Process) | The actual field rubric with good/bad examples for Summary, Description, Business Impact. Also defines what a PCR is *not* (pure TS config, clinical content, bugs, IT requests, activation-scoped asks) and the urgent-request bar (contractual commitment, compliance issue, fix for a partially-delivered commitment, egregious missed requirement — and CX/CSP leadership sign-off already in place). |
| `4468604991` | When a PCR ticket needs to to be configured or executed on by another team | Covers the "PM confirms it's available via config → Help Desk creates a follow-up ticket for PlatCon / Clinical Configurations (Letters) / Integrations to execute" flow. This is the applicable process whenever the ask is "please configure/execute what's already validated," not "please build something new." |
| `4331470852` | Configurations Overview | Maps every config surface (Fax Intake, Continuation, Skillsets, Queues, Letters, etc.) to its owning team — almost everything maps to **Technical Services – PlatCon**, a few to **Product** or **IntEng**. Use this to get the SME/owning-team field right instead of guessing. |

Fetch with `mcp__atlassian__getConfluencePage` (cloudId `coherehealth.atlassian.net`,
`contentFormat: "markdown"`).

## Jira precedent-chain shape

When the same kind of ask has been made before, it usually shows up as a chain of linked
tickets across projects, not one ticket:

1. **CTS** project, issue type **Product Change Request** — the ticket filed through the
   Cohere Ticketing System form (what Divy fills out).
2. **STAR** project, same issue type, same title — Help Desk's triage mirror of the CTS
   ticket.
3. An owning-team project (e.g. **PLATCON**, issue type **Change Request**) — the actual
   execution ticket, assigned to the person on that team who'll do the work.

Finding just one of these is enough to infer the others exist — check
`getJiraIssueRemoteIssueLinks` or the issue's linked-issues field to pull the rest of the
chain if you need the execution-ticket assignee or status.

### JQL tool-quirk — avoid blowing the token budget

`searchJiraIssuesUsingJql` via the Atlassian MCP returns full issue descriptions (images,
long tables, everything) regardless of what you pass in `fields` — the `fields` param
does not cap response size the way you'd expect. A broad `text ~ "..."` search across the
whole instance can return 100k+ characters and get rejected before you see anything.

To avoid this:
- Prefer `summary ~ "..."` over `text ~ "..."` for a first pass — summary search is much
  narrower.
- Add `AND project = X` as soon as you have a guess at the right project.
- Keep `maxResults` to 5–10 for exploratory searches; widen only once you've confirmed the
  query is narrow enough not to blow up.
- If a search does exceed the limit, the tool saves the full result to a file — read that
  file in chunks rather than re-running a broader query.

## Standard CTS "Product Change Request" form fields

In order, as the form presents them (confirm against the live form if Divy hasn't pasted
it fresh — fields do get added/renamed):

Summary\*, Feedback Description (What Problem Needs to Be Solved)\*, Business Impact\*,
Impacted User Type\*, Business Critical or Urgent?, Request SME, Client Phase, Customer,
Line of Business, Requested By: Internal Department\*, Product Area, Value Amount (Annual),
Value Type\*, Value Calculation Description, Labels, Email Subject (Customer Success use),
Item Number (Customer Success use), Attachment.

\* = required. "Customer Success use" fields are not Divy's to fill — leave blank.

Fields that live in a dropdown on the real form (Customer, Line of Business, Value Type,
Impacted User Type) can't be verified from outside the form — always tell Divy which of
his filled-in values are a best guess against an unseen dropdown vs. free text he can paste
as-is.

## Worked example

Real PCR drafted this way, for calibration on register/format (not a template to copy
verbatim — the actual content should always come from that ticket's own sources):

> **Summary:** Fax Back Reason Config — Promote to Production for BCBS SC, BCBS TN, Health
> Partners, Avera, Aetna & Humana
>
> **Feedback Description:** Cohere intake staff working the fax-back workflow in Queue
> Management for BCBS SC, BCBS TN, Health Partners, Avera, Aetna, and Humana don't have
> client-specific faxBackReasons configured in Production. Because this config block
> doesn't exist for these clients today, agents fall back to the legacy free-text "Other"
> checkbox instead of the structured, searchable reasons dropdown when sending a fax-back
> notice to a provider — so the language sent to providers isn't standardized, and the
> reason a fax was sent back isn't reportable.
>
> We've built and validated the faxIntakeConfiguration.faxBackReasons JSON for all 6
> clients (categories, reasons, and provider-facing notice text per reason). BCBS SC has
> already been configured and validated end-to-end in Preprod QM by Eden Joy Jimenez
> (Technical Services) — the reasons populate correctly in the dropdown and the right fax
> notice generates. The remaining 5 clients are queued to be configured and validated in
> Preprod next.
>
> Ask: once each client's config is validated in Preprod, have PlatCon (config owner per
> the Configurations Overview page) paste that client's JSON into the Fax Intake feature in
> Production Configuration Management, following the attached step-by-step doc. BCBS SC is
> ready to move now; the other 5 will follow as each clears Preprod validation.
>
> This follows the same pattern as CTS-5346 / PLATCON-5146 (Fax Back Reason Config for
> Medicare - Novitas) — a validated config handoff to PlatCon, not new product work — so
> Triage/PM review shouldn't be needed before PlatCon can action it.
>
> **Business Impact:** Standardizes what's communicated to providers when a fax can't be
> processed, across 6 payers, and gets intake staff off manual free-text entry onto a
> structured dropdown with pre-approved messaging per reason. It also makes "why was this
> fax sent back" reportable at the reason level for these clients for the first time — that
> data is currently unstructured. No contractual deadline attached; this is an
> operational-quality and reporting improvement, not a client commitment.
>
> **Request SME:** Eden Joy Jimenez — configured and validated the BCBS SC config in
> Preprod; can speak to setup/testing.

Note what step 4 (precedent search) surfaced and step 7 (flag unverifiable) caught:
finding CTS-5346/PLATCON-5146 confirmed this exact ask-shape is accepted through the PCR
form even though the general policy text says config changes aren't PCRs — and fields like
Value Type, Customer, and Line of Business were called out as best-guess against dropdowns
the drafting session couldn't see, rather than silently filled with a plausible value.
