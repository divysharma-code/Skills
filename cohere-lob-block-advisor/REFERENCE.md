# Findings behind the advisor (dated 2026-10-27)

Read from `core-platform` and `frontend` on `develop` and from the BCBS South Carolina
production referral config. These are starting points. Re-check anything the answer
depends on, because code and config move.

## What exists

| Mechanism | Scope | Hard stop? | What the user sees | Evidence |
|---|---|---|---|---|
| Rules-engine `RedirectAction`, `displayTarget: PATIENT_SELECTION` | One member at patient search; auths and referrals together | Yes when `isOptional` is false: both Start buttons are hidden | `title` and `message`; default "This member cannot be selected. Please contact Cohere for more information" | `core-platform ServiceRequestRuleService.groovy` (`evaluateRulesForPatientSearch`), `PatientController.groovy:160,297`, `Action.groovy:487-498`; frontend `PatientSearchResultCard.tsx:86-155`, `PatientSearchRedirectMessage.tsx:11-18` |
| Rules-engine `RecommendChangeAction` or DisplayMessage at patient selection | Member | No, a warning | `message` | `PatientSearchResultCard.tsx:87-88` |
| `referralManagementConfiguration.referralRequiredCoverageType` | Referrals; matched against `coverage.coverageProductType` (for example HMO) | No. Hides "Start referral" (COH-8541) and, when false, the referral is auto-approved as administrative | None | `PatientService.groovy:544-552`, `ReferralManagementConfigurationService.groovy:22-29`, `ReferralRequestService.groovy:536-548` |
| `fieldConfigurationList[].blockIfOON`, `blockIfUnknown`, `requireReferringProviderIsPCP` | Referral submit; by provider network or PCP status, not LOB | Yes (backend 422) | Backend error message | `ReferralManagementConfiguration.groovy:90-97`, `ReferralRequestService.groovy:466-517` |
| `riskBearingEntity` | Referrals | No match sets `delegated=false`, so the referral is denied at submit | None | `PatientService.groovy:553-559` |
| `submissionConfiguration.hideRecommendedForAutoApprovalForLineOfBusiness` | Auth form, by LOB | No, cosmetic | None | `SubmissionConfiguration.groovy:22-23` |

## What does not exist

- No referral-only LOB block. `DisplayTarget` has no referral value
  (`WithAcceptAction.groovy:50-55`) and the request built for patient search carries no
  request type.
- No `payer-lookup-data-*` collection that maps raw LOB strings to Commercial, Medicaid or
  Medicare Advantage. The only payer-lookup collection in the BCBS SC config is the
  specialty mapping. The mapping CSV looks like a build input (INFERRED).

## Where the member's LOB comes from

Rules read `RulePatient`, built from the primary coverage active today
(`ServiceRequestRuleDataModel.groovy:132-150`):

| Field | Holds |
|---|---|
| `lineOfBusinessType` | The `LineOfBusiness` enum (`LineOfBusiness.groovy:24-41`), matched case-insensitively |
| `lineOfBusinessPayorValue` | The raw payer LOB string |
| `lineOfBusiness` | The LOB description |
| `coverageProductType`, `planType`, `productId`, `groupId`, `policyType` | Other coverage fields a rule can use |

Raw strings in the BCBS mapping file match the enum except `PAI` and
`MEDICARE ADVANTAGE - PDP`. For those two `lineOfBusinessType` is null, so match on
`lineOfBusinessPayorValue`.

## Setup that works today (auths and referrals together)

1. Rules engine: create a service-request rule for the health plan.
2. Condition: `patient.lineOfBusinessType` (or `lineOfBusinessPayorValue`) is one of the
   blocked LOBs. Other options: `patient.coverageProductType`, or `patient.productId`
   (the QMB pattern from STAR-15342).
3. Action: Redirect, patient selection, not optional.
4. Leave `skipPatientSearch` false. It defaults to false.

```json
{ "_class": "RedirectAction",
  "displayTarget": "PATIENT_SELECTION",
  "isOptional": false,
  "title": "Referrals not required",
  "message": "Medicare Advantage members do not need a referral. Please submit an authorization instead." }
```

The action fields are VERIFIED. The `ServiceRequestRule` wrapper and condition JSON were
not read (UNVERIFIED), so build the rule in the rule builder.

## Referral-only block: code change needed

Owner: Intake (`ReferralManagementConfiguration` carries `@EntityMetadata` INTAKE).

- Option C: add a blocked-LOB list to `ReferralManagementConfiguration`, check it in
  `determineReferralEligibility` and in referral submit, and hide or explain "Start
  referral".
- Option D: change the BCBS SC not-required branch so it returns a block instead of
  auto-approving. Smaller, but it affects every unlisted product type.

## Gotchas

- The redirect is enforced in the frontend. No backend re-check of a patient-search
  redirect was found on auth or referral submit (INFERRED). API, fax and internal paths
  may bypass it.
- Rules evaluate the primary coverage as of today, not the service date.
- A vendor-level `referralManagementConfiguration` replaces the health plan's whole object.
  Any new key must be copied into vendor configs.
- BCBS SC prod has no `manualStatusEditRoles`, so void/withdraw is off.
- Rules live in the rules-engine database. Coverage LOB values come from the eligibility
  feed (Data Platform). Neither shows in the repo.

## Tickets

PCR-749 and its duplicate PCR-1170 (the ask), COH-8541 (Start referral UX), PLATCON-4738
(reassigned), STAR-15342 (the QMB block that uses the same redirect pattern), CTS-4433,
CTS-6594.
