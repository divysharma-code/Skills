# Reference source: Fax Intake Configuration (Confluence COH-3502800929)

This is the calibration example the skill is derived from. It shows the house
style used across Cohere's engineering-facing config-reference pages: one
Confluence page per feature area, broken into config-block sub-sections, each
following Context → Components → Configuration Example → (optional) setup
notes.

Preserved close to the original so future config docs can be checked against
real precedent, not a paraphrase.

---

## Fax Intake Case Un-assign sub reason set up

### Context
The fax intake configuration enables Cohere intake staff to create referrals
directly from fax submissions. This configuration also supports attaching fax
documents to the referral and sending fax notices and fax backs for referrals
that come in through the fax workflow. One can have as many sub-reasons in the
drop down as needed.

### Components
- `unassignReasons`: a list of sub-reasons available to users after they
  select "I don't know how to work this case" from the close-reasons option.
  If this config block does not exist, users won't get a list to choose from
  and the default behavior applies.
  - `value`: used for reporting in the backend — any alphanumeric value that
    identifies the selected sub-reason.
  - `shortLabel`: what shows up on the chip ("Unassigned - {shortLabel}") in
    QM after the case has been unassigned.
  - `label`: what is shown to the user in the drop-down when selecting a
    reason for unassigning a fax case.

### Configuration Example
```json
{
  "faxIntakeConfiguration": {
    "unassignReasons": [
      {
        "value": "FAX_FORWARD_VALIDATION_REVIEW",
        "shortLabel": "Forward Validation",
        "label": "Fax Forward Validation Review"
      },
      {
        "value": "VALIDATION_OF_ATTACHMENT",
        "shortLabel": "CSR Attachment",
        "label": "Validation of CSR/Attachment"
      },
      {
        "value": "GENERAL_UNABLE_TO_WORK",
        "shortLabel": "Unable to work",
        "label": "Unable to work"
      }
    ]
  }
}
```

---

## Patient Card Display Fields

### Context
The fax intake configuration drives which member data points appear on the
patient info card across the fax intake and portal UI. Adding a
`displayFields` array surfaces additional coverage or member attributes (for
example, IPA Association for Alignment Health) alongside the core fields
(name, DOB, member ID, health plan). The frontend renders one row per entry
and resolves each value as a lodash-style path against the member/coverage
payload. If `displayFields` is absent, no extra rows render, even when the
underlying data is present in the payload. This is what drives the "IPA
Association" field from **COH-7543: Be able to view "IPA association" info in
the patient card — Done**.

### Components
- `displayFields`: a list of objects, one per extra field to show on the
  patient card. Each entry includes:
  - `label`: the display label shown to the user on the card (e.g. "IPA
    Association").
  - `value`: the path to the data point in the member/coverage payload,
    resolved lodash-style (e.g. `coverage.payerCustomFields.ipaDesc`). For
    `payerCustomFields`, the resolver matches the entry whose `fieldName`
    equals the last path segment and displays its `valueString`. If the
    value is missing, the card shows "N/A".

### Configuration Example
```json
{
  "faxIntakeConfiguration": {
    "displayFields": [
      {
        "label": "IPA Association",
        "value": "coverage.payerCustomFields.ipaDesc"
      }
    ]
  }
}
```

### Setting this up for a client
This block is required per client. It is not enabled by a feature flag. If
it is missing from a client's fax intake config, the fields will not appear
even though the frontend code is in prod and the data is in the payload.

---

## Fax outbound number configuration

### Context
The fax intake configuration also allows users to set up an outbound number
used for fax notices and updates, so there is a single fax line per payer.
Traditionally there has been a single fax line across clients, which creates
a single point of failure. To ensure continuity of business and de-risk this,
we allow health plans to configure an outbound fax number. **NEW: going live
with Essence in Q3 — IPS-2232: Fax - Make Cohere's Outbound Fax Number Payer
Configurable — Done**.

### Components
- `outboundFaxConfiguration`: parent config that encompasses the product ID
  and the fax line used for outbound comms.
  - `outboundFaxNumber`: the number (e.g. `"2222222222"`) displayed on the
    outbound fax document.
  - `outboundFaxProductId`: the product ID of the fax line used for outbound
    communication — ideally one of the sister fax lines for a health plan
    (see Westfax inbound fax config).

### Configuration Example
```json
{
  "faxIntakeConfiguration": {
    "outboundFaxConfiguration": {
      "outboundFaxNumber": "2222222222",
      "outboundFaxProductId": "6edd69db-26b8-406e-a364-17046204a34d"
    }
  }
}
```

---

## Fax Intake for Referrals

### Context
The fax intake configuration enables Cohere intake staff to create referrals
directly from fax submissions. This configuration also supports attaching fax
documents to the referral and sending fax notices and fax backs for referrals
that come in through the fax workflow.

### Components
- `referralsCreationFromFaxEnabled`: boolean flag that determines whether the
  referral-via-fax workflow is enabled. If `true`, fax intake users can
  initiate a referral from the fax QM via a "Create a new referral" button.

### Configuration Example
```json
{
  "faxIntakeConfiguration": {
    "referralsCreationFromFaxEnabled": true
  }
}
```

---

## Fax Intake for Forwarding — Manual Fax Forwarding

### Context
The manual fax forwarding configuration enables Cohere intake staff to
manually forward out-of-scope or misrouted faxes. The structure below
configures the reasons available for manual forwarding and the fax numbers
faxes can be forwarded to.

### Components
- `manualFaxForwardingEnabled`: boolean flag that determines whether manual
  fax forwarding is enabled. If `true`, users can manually forward faxes.
- `manualFaxForwardingCloseOptions`: list of reasons users can select when
  forwarding a fax. Each option has a `label` (shown to the user) and an
  `identifier` (used for internal reporting). Customizable per payer.
- `manualFaxForwardingNumbers`: list of fax numbers faxes can be forwarded
  to. Each entry has a `value` (the fax number) and a `label` (display name
  for the recipient). Client sign-off on numbers/labels is critical to
  prevent PHI leaks — Cohere has no control over what happens after
  forwarding.
  - `userInput`: when `true` instead of a fixed `value`, renders a free-text
    "Other" option so users can type in a fax number manually — see
    **COH-7359: Allow users to enter fax forwarding number manually — Done**.

### Configuration Example
```json
{
  "manualFaxForwardingEnabled": true,
  "manualFaxForwardingCloseOptions": [
    { "label": "Forward this", "identifier": "FORWARD_THIS" },
    { "label": "Out of Cohere Scope", "identifier": "OOCS_TEST" }
  ],
  "manualFaxForwardingNumbers": [
    { "value": "888-417-2760", "label": "Healthy Blue Medical" },
    { "value": "5702143108", "label": "Unhealthy GHP" },
    { "value": "5702408817", "label": "Test if this goes to Avera" },
    { "userInput": true, "label": "Other" }
  ]
}
```

### Verification note
"Go to QM and forward a fax, check this new entry is available." — the
source page includes a manual UI-verification step alongside the config
example. Include one when the config change is easy to eyeball in the UI.

---

## Extensions

### Context
Extensions provide additional configuration blocks that allow routing of
faxes to various Queue Management queues and other custom functionality.

### Components
- `extensions`: list of objects — a list of configurations allowing routing
  of faxes to various QM queues.
  - `extension.name`
  - `caseBuildPercentage`
  - `randomField`
  - `cutOverRate`

(Source page left several of these as bare field names without further
description — acceptable placeholder state while the config is still being
finalized; flag these explicitly as "not yet documented" rather than
inventing a definition.)

---

## Closing structural notes from the source page

- `faxCloseOptions` / `faxChannels` pattern: each `faxCloseOptions` entry
  needs a unique `label` and `identifier`, with `identifier` following
  `ALL_CAPS_WITH_UNDERSCORES`. Each `faxChannels` entry configures a
  specialty + Westfax product ID per intake queue; `speciality` must be
  unique per client — you cannot have two queues for the same payer with the
  same specialty.
- "Further Information" footer: pointers to related design docs (e.g. the
  Westfax multi-payor support doc) and related how-to docs (e.g. the case
  build conversion-percentage guide).
- Page-level footer: **Owning Product Team** — e.g. "PDDE team: Intake".
