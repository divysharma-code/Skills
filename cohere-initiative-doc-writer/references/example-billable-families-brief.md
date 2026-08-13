# Initiative | Billable Families

_Calibration example for the Initiative Brief template. Source: a pasted
Confluence-style initiative brief for the "Billable Families" initiative._

## Overview

The "Billable Families" initiative aims to address inefficiencies and
inconsistencies in the current authorization workflow, particularly for
diagnostic imaging and other specialties where procedure codes are overly
granular. This initiative will enable grouping related procedure codes into
billable families, ensuring that authorizations account for variations
within these groups while avoiding redundant submissions and reviews. By
implementing this framework, Cohere can streamline the submission and
review processes, improve user experience, and enhance scalability for
future specialties and payers.

## Context

Currently, prior authorization workflows rely on individual procedure codes
to drive submission and review processes. While effective in most cases,
this approach can lead to challenges in situations where procedure codes
are overly specific for the sought care.

For example:

- **Diagnostic Imaging**: Procedure codes like MRI with contrast, MRI
  without contrast, and MRI with and without contrast often fall under the
  same clinical intent and evaluation process. However, minor variations in
  the actual procedure performed may require resubmissions or re-reviews,
  even when the initial authorization was clinically appropriate.
- **Physical Therapy**: During referrals, providers may submit
  authorization requests based on preliminary diagnoses (e.g., ACL tear
  suspected via a knee MRI). The specific imaging technique is determined
  later by the radiologist's evaluation, but any mismatch in submitted CPT
  codes can result in denials or the need for a resubmission (and thus a
  re-review).

These challenges have operational and financial implications:

- **Duplicate submissions and reviews**: 2.69% of submissions of 7055
  family codes involved resubmissions with a different code within the
  same family in the past 90 days (a total volume of 1765 cases). Of these,
  88.15% were autoapproved. Since an approval for one code should be
  sufficient for others within the same family due to clinical equivalence,
  these resubmissions resulted in unnecessary manual review for 213 cases.
  At a cost of $27.00 per manual review, addressing this issue could save
  approximately $5,751 in operational expenses over this 90-day period for
  7055 cases alone (only 8.11% of total DI requests).
- **Member experience issues**: Denials due to minor procedural mismatches
  create friction for providers and patients.
- **Scalability concerns**: As Cohere expands into new specialties and
  payers, managing these inefficiencies becomes increasingly challenging.

## Problem Statements

_What problem(s) is the user experiencing and why are they important to
them?_

**Auth Submitters**

- **Redundant Submissions/Editing**: Currently we require submitters to
  restart the authorization process or edit an existing authorization if a
  procedure code changes within the same family after approval (when
  requests are initially submitted for one procedure but are performed
  under a different procedure within the same family).
- **Overly Granular Care Options (Maybe)**: Some submitters seem to face
  confusion when selecting specific procedure codes (e.g., MRI with
  contrast vs. without contrast), when aiming to submit an authorization
  for a clinical service (like knee MRI).

**Clinical Reviewers**

- **Duplicate Review Workload**: Reviewers are often required to reassess
  edited submissions or resubmissions when the procedure code was changed
  within the same family, consuming time and resources without altering
  the clinical decision.

**Payers**

- **Claims Inconsistencies**: Changes in procedure codes post-authorization
  can result in processing inconsistencies, leading to payment delays or
  denials (particularly for 'no auth, no pay' payers).

## Impact / Why Now

The Billable Families initiative addresses established inefficiencies in
our prior authorization workflow, particularly for diagnostic imaging and
other specialties where minor variations in procedure codes lead to
operational friction. We have established a consistent incoming volume of
resubmissions (over 500 cases per month on average for 7055 family alone),
giving us a measurable opportunity to reduce redundant processes.
Healthpartners, a client particularly heavy on diagnostic imaging, is also
going live; this go-live sets the need for a smoother experience as more
pressing. BCBST & MMO will be going live with HTI as well, further
contributing to volume increases. Additionally, several payers in the
Cohere pipeline have a 'no auth, no pay' policy; for these payers,
mismatches between approved and billed codes within the same family can
result in denied claims, creating payment delays and administrative
burdens.

## Goals / Success Criteria

_Metrics/benchmarks to show that we have solved the Problem Statements
above._

| Goal | Metrics to track |
|---|---|
| Reduce duplicate submissions for codes in the same family | <1% back-to-back resubmission rate within the same billable family (currently ~2.7%). Note: each percentage point reduction translates to significant opex savings, as every resubmission saved reduces the RN review cost of $27.00 per case. For example, reducing resubmissions by 10,500 annually could save approximately $283,500. |
| User satisfaction remains steady | Submitters of codes in relevant billable families (DI, physical therapy, CT, etc.) do not see a drop in satisfaction scores (NPS & CSAT) post deployment |

## Phase I

### Jobs to Be Done

_What are the needs of key users, what are we trying to accomplish, and how
are we trying to accomplish it._

| Job to be done (JTBD) | User Stories (sub-JTBD) | Notes |
|---|---|---|
| Authorization Submitters | As an authorization submitter, I want to avoid extra steps in the submission process so that I can move on to my next task. As an authorization submitter, I want the approval I receive to still apply even if the patient's needs change slightly, so I don't have to restart or edit the auth. As an authorization submitter, I want a way to request the care my patient needs without having to navigate or select specific procedure codes, since I don't always know which ones are appropriate. | ***Maybe on the last story |
| Clinical Reviewers | As a clinical reviewer, I want to reduce redundancy in the review process so that I can move on to my next task. As a clinical reviewer, I want authorization requests to account for changes within the same billable service, so I can avoid reassessing cases that don't require a new clinical decision. | |

### Launch Timeline

- Scoping with design and eng → week of December 10
- UXR work begins: December 2
- This work was originally intended to be complete by the end of Q1. Due to
  requestTiming issues, and increased scope due to data team involvement,
  this initiative is likely to be complete beginning of Q2
- Review was also unable to take up work until Q2
- Data Team timeline (pre-req for work):
  - Data Contract Finalization – Mid to Late February (Steven/Data Platform
    Team)
  - Ingestion Updates – Begins late March unless Intake can loan a dev or
    take it up
  - Search & API Updates – Timing TBD, dependent on ingestion work
- Key Milestones / Go-live checklist — TBD (a project plan, perhaps)

### Proposed Workflow

From Tony Gallanis: [Billable Families E2E FigJam board]

Designs: [Billable Families Figma file]

### Open Questions

_A live decision log — answers get appended inline as they land, not
deleted once resolved._

- How does this relate to clinical services? Given the clinical service
  refactor, are they 1:1? Do we embed as part of clinical services first or
  no?
  - Short answer seems to be no; we don't seem to get any benefit from
    embedding this in clinical services, and given that there is an
    upcoming revamp there seems to be too many questions here.
- How are families determined and maintained?
  - Continue to follow up on this thread in the new year (Slack link). From
    this thread, when are families determined? Two options: (1) we
    determine the family at the point of searching for the CPT codes
    (showing all those options during the dropdown), or (2) we determine
    the family when the attribute is added determining specific body part.
    We would like to store this in the semantic layer.
- How should users be nudged to select a billable family, or informed that
  other codes in the family are included by default?
- Would PA apply at the family level or the code level? What would this
  look like?
- How are CAQs applied to families?
  - This does not matter — CAQs should just be surfaced for the parent
    code.
- How does autodecisioning handle families?
  - Decisioning should just be executed on the parent code, but this is
    review's work.
- Could some codes in a family be non-PAL exception codes?
  - Still a bit of an open question; need a way to confirm our assumption
    that this is not the case.
- How are families passed down as data? A collection of Px codes?
  - Three pieces of info are passed down: the parent code, the underlying
    codes, and the natural language name of the family.
- Would the review criteria be the same?
  - Should be based on Cherie and Sandy's feedback. At least for DI, there
    is no differentiation between with contrast and without. We are
    getting the list of codes finalized this sprint for commercial,
    delegated DI.
- If a provider submits a CPT code, can we add? If we are passed CPT codes,
  do we need to review each individual CPT code?
  - We are deferring what gets shown on the review side to the clinical
    review team (Nick Berger).
- How do payer platforms handle this?
  - MMO doesn't send CPT codes for PT — Cohere sends "physical therapy."
    Humana does it at CPT code level. MMO might add the others on after
    the submission for DI.
- Are there any issues we'll run into with units (e.g. 1 unit approved, not
  1 unit for each code in the billable family)?
- How does this relate to codes with attributes? They are not specific
  enough, whereas these codes are too specific. Are we expecting any
  billable family codes to have attributes? Yes — see example.
- What about Px code limits? For example, Humana requests can only have 10.
- What is the true situation with PT? Some say you only need one code for
  all, but we need to confirm — this will be out of scope for now.

Questions after the design review: [Billable Families FigJam board, design
review section].

## Resources

### Stakeholders

_Think through all of the stakeholders that need to be involved as early as
possible to make this Initiative successful._

**Squad:**

- **Product**: Connor Feick, Samuel Hamway
- **Design**: Jayna Moloney, Kelsey Guo
- **Engineering**: Mitchell Mellone
- **Analytics**: —
- **UXR**: Jessica Coates Beauchemin
- **Provider Relations**: —
- **Clinical Programs**: —
- **Client/Growth**: —
- **Service Ops**: —
- **Marketing**: —
- **Legal and compliance**: —
- **Privacy/Security**: —

### Links

- Slack: #billable-families
- Research: TBA
- Workflow: user workflow diagram
- Designs: Phase 1 Designs; Ideal State Designs
- Jira: Phase 1 Epic; Phase 2 Epic
- Client decks: TBA
- Related Initiatives: TBA

## Results

_Review the outcome of each phase that we've completed._

| Phase | Goal | Result | Comments |
|---|---|---|---|
| Phase I | (from Goals/Success Criteria above) | _left empty until Phase I ships_ | |
| Phase II | (from Goals/Success Criteria above) | _left empty until Phase II ships_ | |
