# User types: roster and the confidence gate

## Source of truth

The [Cohere User Types index](https://coherehealth.atlassian.net/wiki/spaces/COH/pages/5960368296) (Confluence, cloudId `4b6d47e4-f971-4687-a643-0543ee48f255`) is authoritative. The roster below is a convenience cache so the menu can be built without reading twenty pages. **Confidence is always confirmed live at selection** (step 2 of the flow), never trusted from this table alone.

To read any page: `getConfluencePage` with the cloudId above, the page ID, `contentFormat: markdown`.

## Freshness: what stays current on its own, what does not

**Always live, never stale** (read from Confluence every session):
- The synth's actual knowledge: goals, pains, behaviors, verbatims, metrics, archetype descriptions. Edit a page and the next session reflects it.
- The confidence gate at both levels (steps 2 and 3). A validation that flips a page or a variant up or down changes what gets cast, immediately.
- Discovery itself, when the step-1 index read succeeds: new, renamed, and re-nested types appear without any manual update. Confluence page IDs are durable across renames and moves, so links keep resolving.

**Cached here, can drift** until refreshed:
- The confidence hints in the roster table. These only pre-filter the menu; the live gate is the real guarantee, so at worst a stale hint means a type is offered and then declined at selection, or a freshly validated type is not surfaced in the menu until a refresh.
- The "variants to expect" column, a hint only; actual variants are detected live from the page.

Net: the words a synth says and the gate that admits it are always current. The only thing that can lag is menu pre-filtering, and the live gate backstops it.

## The gate, in two levels

**Level 1, the user type.** Read the chosen page. Find the Snapshot table's **Confidence** row (a status lozenge plus a sentence, e.g. "Medium overall"). Medium or High passes. Low is declined: say it needs more research before it can be simulated, and offer the closest qualifying type. If a page has no clear Snapshot Confidence, scan for an overall confidence statement; if still unclear, treat as ineligible and say why.

Withhold on more than the lozenge: a page that reads Medium but is **super thin** — a stub, mostly placeholder, almost no observed evidence or verbatims — should also be declined or cast only with a loud "this is barely evidenced, treat everything as hypothesis" caveat. The scope is validated user types with enough real research to stand up a person; low-confidence and skeletal pages are out.

**Level 2, the variant / archetype.** After the type passes, look for:
- **In-page behavioral archetypes** (a section like "Behavioral Archetypes"), each with its own confidence lozenge.
- **Linked subtypes / variants** (separate pages, nested under this type in the index or cross-referenced in the overview), each gated by its own Snapshot Confidence.

**Hide every variant or archetype whose confidence is Low.** Offer only the Medium/High ones. If none qualify, cast from the parent page's overall evidence and note the variants were withheld as too thin. If one qualifies, auto-pick and say so.

## Roster (confidence cached; drives the opening menu)

**Confidence swept 2026-07-29.** The opening menu (step 1) shows only rows marked **Yes** in "Menu": every Medium/High type. Low rows are **hidden entirely**, never shown or greyed. A borderline "Low→Medium" shows but is cast with a loud n=1 caveat. Always re-confirm live at selection (step 2); if a page's confidence has moved, fix its row here.

### Primary users

| User type | Page ID | Confidence | Menu | Variants / archetypes |
| --- | --- | --- | --- | --- |
| Auth Submitter (in-house provider-office) | 5996642442 | Medium | Yes | 4 archetypes: Empowered Expert, Autonomous Apprentice, Proficient Passenger, Loyal Learner (each Medium) |
| Third-Party / outsourced submitter (subtype of Auth Submitter) | 6000705633 | Medium | No | hidden by preference: subtype of Auth Submitter, thin sample; still reachable under the Auth Submitter parent or by URL |
| Claims Auditor | 5997068362 | Medium | Yes | subtypes: Code Validator, Clinical Validator |
| Intake Supervisor | 6008275008 | Medium | Yes | under Clinical Operational Leadership |
| Clinical Operations Supervisor | 6014926874 | Medium | Yes | under Clinical Operational Leadership |
| Clinical Operational Leadership (parent) | 6007521353 | Low / hybrid | No | placeholder parent; page archived, titled "Clinical Operations Manager" |
| Clinical Reviewer - MD, Outpatient | 5961383955 | Medium | Yes | |
| Clinical Reviewer - MD, Inpatient | 5967741071 | Low | No | MD inpatient voice absent; external inferred |
| Clinical Reviewer - RN, Outpatient | 5961056349 | Medium (High in places) | Yes | strongest reviewer page |
| Clinical Reviewer - RN, Inpatient | 5961908227 | Medium (internal Low, external Medium) | Yes | |
| Letter Writer (DNW) | 6027444337 | Medium | Yes | internal + external teams |
| Healthcare Analytics Analyst | 5975015735 | High | Yes | |
| HEDIS Abstractor / Auditor | 5967708321 | Low | No | no direct abstractor research yet; top research need |
| Clinical Content Policy Manager | 5979602963 | Medium | Yes | |

### Secondary users (revealed on "show more")

| User type | Page ID | Confidence | Menu | Note |
| --- | --- | --- | --- | --- |
| Client Administrator | 5978030113 | Medium | Yes | ENG space |
| Clinical Portfolio VP | 6019285116 | High | Yes | all 4 incumbents interviewed |
| Customer Success Specialist | 5967872172 | Medium | Yes | |
| Delegation Oversight Manager | 5971837031 | Medium | Yes | |
| Director, HEDIS Operations | 5964202136 | Low→Medium | Yes (caveat) | one direct session, n=1 |
| Director, Utilization Management | 5969412262 | Low | No | no observed research with an external UM director |
| Provider Network Manager | 5972262945 | Low | No | no direct UXR; secondhand only |
| Review Quality Auditor | 5975670797 | High | Yes | dedicated 2025 UXR study |

## Pasted URL

Accept any Confluence user-type page URL. Extract the numeric page ID from the path (`.../pages/<ID>/...`), read it, and run both gate levels. If the URL is not a user-type page, say so.

## Refresh routine

Discovery reads the index live, so this file rarely needs hand-editing. Refresh it when a page's confidence may have moved, or after a batch of new types lands:

1. Read the index (page 5960368296) for the current type list and page IDs.
2. For each type, read its page and note the overall Snapshot Confidence and its Medium/High variants or archetypes.
3. Update the **Confidence** and **Menu** columns and the swept date. Keep Low types listed with **Menu: No** (so the file documents the exclusion) but never let them into the opening menu.

Run it on demand, or schedule it as a periodic sync (the way term-check rebuilds its lexicon). Confirm with the user before automating it.
