# Bypass CRD Redirect (Include Vendor-Delegated Codes)

_Calibration example for the Feature/Capability Reference template. Source:
Confluence page "Bypass CRD Redirect (Include Vendor-Delegated Codes)",
COH space, child of the "Prior Authorization check" hub page._

## Overview

Bypass CRD Redirect lets authorized internal staff include codes that are
delegated to another vendor in a Cohere authorization, instead of being
redirected away to submit elsewhere. When the PA check determines that a
code is delegated to a different vendor, it normally blocks submission
through Cohere and tells the user to submit through that vendor. This
feature adds a controlled override: a permitted user checks a box, selects
a qualifying reason, and the delegated codes are included on the Cohere
request, which then pends for review.

It reuses the existing Non-PAL reason-modal pattern (reason selection at
intake plus reason visibility for reviewers), with two differences: no
free-text field and no "Learn More" button. It is gated by feature flag,
payer configuration, and user group, and shipped first for Alignment
(ServiceOps General staff).

## Why we built this

Some authorizations contain codes that are delegated to another vendor
alongside codes Cohere handles. Today the CRD redirect blocks those
delegated codes from being submitted through Cohere, so internal staff
working a case have no way to include a delegated code even when there is a
legitimate operational reason to (for example, keeping a request together
or a coverage-documentation need). This forces workarounds and slows down
case handling.

Bypass CRD Redirect gives internal staff a governed path to include those
codes, capturing a structured reason so the decision is auditable and
visible to reviewers, while keeping the behavior off by default and
restricted to specific user groups.

## Some definitions

**CRD (Coverage Requirements Determination)** — The service behind the PA
check that determines whether prior auth is required for each code and who
the auth submission and delegated vendors are.

**Delegated vendor** — The vendor responsible for a given code's
authorization (Cohere or another vendor). When the delegated vendor is not
Cohere, the PA check redirects the user to submit through that vendor.

**CRD redirect** — The PA-check behavior that surfaces vendor-delegated
codes under the "Requires submission through another organization" section
and blocks them from being submitted through Cohere.

**Bypass CRD Redirect** — The controlled override that lets a permitted
user include vendor-delegated codes on a Cohere request by selecting a
qualifying reason. The request pends for review. **This is the scope of
this effort.**

## What we built

At the PA-check results step, when a permitted user has vendor-delegated
codes in the "Requires submission through another organization" section,
they can check a box to include those codes with a qualifying reason.
Selecting a reason includes the codes on the Cohere request, which pends
for review. The bypass is off by default and controlled by a feature flag,
payer configuration, and user group.

### Intake: reason checkbox and modal

- In the "Requires submission through another organization" section,
  permitted users see a checkbox: "I have a qualifying reason to include
  these codes."
- Checking it opens a modal titled "Bypass delegated vendor redirect" with
  the prompt "Select a qualifying reason for including these codes:" and a
  single-select list of configured reasons.
- The primary button, "Include codes (request will pend for review)," is
  disabled until a reason is selected. The secondary button, "Cancel,"
  closes the modal and unchecks the box.
- Attempting to continue without a reason blocks submission and shows
  validation: "Select a reason to continue."
- There is no free-text field and no "Learn More" button (the two
  differences from the Non-PAL flow).
- If the reasons config is missing or invalid, the flow falls back to
  current behavior and the codes remain redirected.
- Clinical service mappings and continuations behave exactly like
  No-PA-Required codes.

### Delegated-vendor recalculation on bypass

Because key configuration (for example, the Service Request Form Field
Configuration) is driven by the delegated vendor, the change must persist
immediately when a user confirms bypass, not only on Continue. On confirm,
a patch request persists the state, the delegated vendor is recalculated,
and the UI rehydrates with the updated configuration (required fields,
visibility, attributes). Unchecking reverses the action and re-renders the
prior configuration; Continue and Save & Exit are disabled while the patch
is in flight.

### CRD check flag

When a delegated redirect is triggered, the CRD evaluates whether the
bypass configuration is enabled for the payer and returns a discrete
boolean (`canBypassCrd`) so the front end routes correctly. This check runs
only when delegated-redirect logic is invoked.

### Persistence

Bypass state and reason persist on `serviceRequest.semanticProcedureCode`:

- `isBypassedCrdRedirect` (Boolean, default false)
- `bypassCrdReason` (String, nullable): must equal one of the configured
  reasons when `isBypassedCrdRedirect = true`, and null when false
- `bypassCrdReasonJustification` (String, nullable): supporting field added
  for future justification capture

## Example Walkthrough

| Step | Action |
|---|---|
| PA-check results, delegated codes | Vendor-delegated codes appear under "Requires submission through another organization." A permitted user sees the checkbox "I have a qualifying reason to include these codes." |
| Check the box | The "Bypass delegated vendor redirect" modal opens with a single-select list of qualifying reasons. The "Include codes (request will pend for review)" button is disabled until a reason is selected. |
| Select a reason | The primary button enables. Selecting it includes the delegated codes on the Cohere request; the delegated vendor recalculates and the form rehydrates. Cancel closes the modal and unchecks the box. |
| Continue and submit | The request proceeds with the included codes and pends for review. Bypass state and the selected reason persist on the request. |

Designs: Intake reason modal (Figma link).

## Review Side

On the Clinical Review page, bypassed codes reuse the Non-PAL visual
pattern so reviewers can see what was bypassed and why:

- The PAL column shows the delegated vendor, as it does today.
- Hovering the info icon shows the configured bypass reason chosen at
  submission (no free text).
- A column denotes whether a code is PAL or Non-PAL.

Reviewer visibility is gated by its own flag so it can be enabled
independently of intake. Designs: Non-delegated codes in review (Figma
link).

## How is this configured?

The bypass lives in a dedicated `bypassCRDConfiguration` subsection inside
the existing `nonPalCheckboxConfiguration`, so it does not affect the
current Non-PAL fields. Configure it in Health Plan Configuration
Management, selecting the payer and the `nonPalCheckboxConfiguration`
feature.

**Gating flags:**

- `bypassCrdRedirectFeature` (LaunchDarkly): controls the intake experience.
- `showBypassedCrdStatusToReviewer`: controls the reviewer visibility.

The intake UI shows only when all are true: `bypassCrdRedirectFeature` is
ON, `showBypassCheckbox` is true, and `restrictToUserGroups` is empty or
the current user's group is listed. For Alignment, this is restricted to
ServiceOps General staff; the design is payer- and group-scalable.

```json
{
  "nonPalCheckboxConfiguration": {
    "showContinueWithPriorAuthCheckbox": true,
    "reasonsToIncludeNonPalCodes": [ ... ],
    "enableLearnMoreButton": true,
    "restrictToLineOfBusiness": [],
    "bypassCRDConfiguration": {
      "showBypassCheckbox": true,
      "restrictToUserGroups": ["ServiceOps General User"],
      "bypassCrdNonDelegatedCodesReasons": [
        { "title": "Urgent care / patient safety", "description": "Time-sensitive care scenario" },
        { "title": "Coverage documentation", "description": "Authorization needed for coverage purposes" },
        { "title": "Program exception", "description": "Plan exception or special handling" }
      ]
    }
  }
}
```

## FAQs

1. **Who can bypass the redirect?** Only users in a group listed in
   `restrictToUserGroups` (empty means all groups), while the feature flag
   and `showBypassCheckbox` are on. For the initial launch this is
   Alignment ServiceOps General staff. Providers cannot bypass.
2. **What happens to a bypassed request?** The delegated codes are included
   on the Cohere request and the request pends for review. The delegated
   vendor is recalculated on confirmation so the correct field
   configuration applies.
3. **What if the reasons config is missing or invalid?** The flow falls
   back to current behavior and the codes remain redirected.
4. **How do bypassed codes behave on continuations and clinical service
   mapping?** The same as No-PA-Required codes.
5. **Is a free-text reason captured?** No. Reasons are single-select from
   config. A `bypassCrdReasonJustification` field exists on the model for
   potential future use, but no free text is collected or shown today.

## Other Resources

- Epic: COH-7483 — Bypass CRD Redirect to Allow Non-Delegated Codes
- Figma: Alignment Health Plan Implementation (Bypassing CRD Logic)
- Service Request Form Field Configuration (related config page)
