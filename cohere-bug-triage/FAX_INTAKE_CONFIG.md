# Fax Intake Configuration — Field Guide (ELI5)

> Plain-English guide to how Cohere's **fax intake** works and how the configuration
> controls it. Built from Paridhi Jain's KT session (Divy / Paridhi Sync, 2026-07-15)
> plus the fax-intake Confluence + client intake demo.

---

## 🧒 Explain it like I'm 5

> **Cohere runs a giant digital mailroom for health insurance companies.**
>
> Doctors' offices still send paperwork by **fax** (yes, fax — an old machine that mails a
> picture of a page down a phone line) to ask an insurance company "can my patient get this
> treatment?"
>
> The insurance company is busy, so they hire **Cohere** to run the mailroom for them.
>
> 1. The fax first lands at a **post office we rent from a vendor called West Fax**.
> 2. West Fax pings us: *"You've got mail!"* and we grab the fax.
> 3. Every fax comes with a little **sticker of notes** on it — when it arrived, which
>    mailbox (fax line) it came to, which insurance company, and what kind of doctor stuff
>    it's about (its **specialty**).
> 4. We turn each fax into a **ticket** (a "service case") so a worker can pick it up.
> 5. Using the sticker, we drop the ticket into the **right basket (queue)** so the right
>    worker sees it — the "heart doctor" basket, the "mental health" basket, etc.
> 6. A worker grabs the ticket from their basket and handles it.
>
> **The Fax Intake Configuration is the mailroom rulebook.** It says which mailboxes exist,
> what each mailbox is for, which basket each fax goes into, and where to *re-mail* a letter
> that came to us by mistake. Change the rulebook → the mailroom behaves differently.
>
> One thing the rulebook does **not** cover: **automation** (robots that do some sorting by
> themselves). That has its *own* separate rulebook. Ignore it for now.

---

## TL;DR (one level up from ELI5)

A provider faxes a prior-auth request → it hits Cohere's fax vendor (**West Fax**) → we pull
it in → it becomes a **service case** in **Queue Management** → it's filtered by **specialty**
into the right **queue** → a staff member (or a client's own reviewer) works it. The **Fax
Intake Configuration (a JSON)** is the control panel that decides all of this per client:
which fax lines exist, each line's specialty, which queue a fax lands in, who owns the decision
risk, and where to forward misdirected faxes. It controls the whole fax intake product
**except automation** (separate config).

---

## 1. What it is

- The **one-stop configuration** for the fax intake product — from *getting faxes in* to
  *workflow changes and enhancements*.
- **Exception:** **automation** is a separate config. It's integral but optional — fax intake
  works fine without it.
- Live for **~3 years**, used by Cohere staff and by **GHP's own reviewers** (see §5).

## 2. Why fax at all?

Faxes are "a dinosaur, but still a relevant dinosaur" in US healthcare — providers still send
prior-auth requests by fax. So Cohere ingests them and turns them into trackable work.

## 3. The end-to-end journey

```
Provider
   │  sends a fax to a dedicated fax line
   ▼
West Fax (our fax vendor)  ──── two possible paths ─────────────────┐
   │                                                                │
   │ (a) straight to Cohere's vendor fax line       (b) to the health plan's own fax
   │                                                     system → they reroute to us
   │                                                     (automatically or manually)
   ▼                                                                ▼
Cohere application  ◄───────────────────────────────────────────────┘
   │  Either way, we receive it DIRECTLY. We act ON BEHALF OF the health plan —
   │  we do NOT send faxes back out to the health plan.
   ▼
Fax arrives with METADATA (its "sticker"): receipt time, which fax line,
which health plan, specialty, …
   │
   ▼
Queue Management (Cohere's case-management product)
   │  creates a SERVICE CASE = one transaction ID for this one fax
   │  (a service case ≠ a service request)
   ▼
Fax lands in the right QUEUE (filtered by specialty + case type)
   ▼
Staff member (or GHP reviewer) picks it up and works it
```

**Key idea:** the **metadata on each fax** drives the routing, and the routing rules live in
the fax intake config.

## 4. The config (the JSON) — building blocks

Paridhi: "the first thing we get is the **specialty** and the **product ID**." The pieces:

### Product ID
- 🧒 *The address of one mailbox.*
- A **unique ID for each fax line number** (one line = one product ID).
- Wired to the vendor via **webhooks** → when a fax hits that line, we're notified and auto-pull
  the document.
- **Touchless for you:** IT + vendor management set up the line ↔ product ID ↔ webhook. You just
  *receive* the product IDs.

### Specialty
- 🧒 *The label on the basket — "heart stuff," "mental health."*
- A **human-readable tag** you assign to each product ID (e.g. `medical`, `behavioral health`).
- Usually **one specialty per product ID**.
- It's the **main filter for Queue Management** — how a fax gets narrowed from "all cases" down
  to the right client queue.

### Queues & routing
- 🧒 *The baskets the tickets get sorted into.*
- A **queue** shows a team only the cases relevant to them (filtered by specialty + case type).
- **Why multiple lines/queues? Workforce management & separation — NOT faster turnaround (TAT).**
  E.g. behavioral-health worked by specific staff; inpatient vs outpatient split.
- **Why providers have multiple lines:** legacy operations — easier for a provider to "send to
  the behavioral-health line vs the medical line." Payers used to have separate teams per line.
- **Flexible mapping:** you can also merge *many* lines into *one* queue.
  - **GHP → multiple queues.** **Health Partners → 5 fax lines into 1 queue.**
- Queue setup is now owned by **Platcon**, per **Jeremy's "how to launch queues"** walkthrough.

### Risk Bearing Entity (RBE) + delegated vendor
- 🧒 *Who's the grown-up responsible if a decision goes wrong.*
- **RBE = who's on the hook** for a request's decision. **Delegated vendor = who processes it.**
- Matters because clients exist at the **health-plan level** and sometimes the **delegated-vendor
  level**.
- An RBE can be the health plan itself *or* a separate vendor — e.g. **Oak Street Health** is an
  RBE under **both Humana and Aetna**.
- For fax intake it's **less critical** (we already split by specialty). You *can* skip it, but
  **best practice = put some value in both `delegated vendor` and `risk bearing entity`.**

### Manual fax forwarding
- 🧒 *"Return to sender / send to the right address" for a letter that came to us by mistake.*
- Handles **misdirected faxes** meant for a different vendor or the health plan's own line.
- Lets staff **forward the fax to a pre-configured outbound number** with a label/reason.
- You **pre-load the common numbers + labels** so staff pick from a list; **free-text** entry is
  available for one-offs.

## 5. How clients differ (worked examples)

| Client | Setup | Note |
|---|---|---|
| **GHP** | **Multiple queues**; their own reviewers do intake | "Pass-through" deal — GHP staff use our product and process faxes themselves; they don't configure it and don't need Cohere staff to do intake |
| **Health Partners** | **5 fax lines → 1 queue** | Ops team prefers consolidated processing |

Pattern: **the client's operating model decides the queue structure**, and we configure to match.

## 6. Who owns what now

| Area | Owner |
|---|---|
| Fax line ↔ product ID ↔ webhook wiring | **IT + vendor management** (touchless to you) |
| Queue launch/setup | **Platcon** (per Jeremy's walkthrough) |
| Configuration going forward | **Platcon** (Paridhi handed it off) |
| First-line questions, troubleshooting, bug investigation | **You (Divy)** — see Goal |
| Deep product decisions / escalations | Product owners |

## 7. Glossary

- **West Fax** — Cohere's external fax vendor; faxes arrive here first.
- **Service case** — one transaction ID per fax, created in Queue Management. ≠ **service request**.
- **Queue Management** — Cohere's case-management product where cases are worked.
- **Product ID** — unique ID per fax line, webhook-connected to the vendor.
- **Specialty** — human-readable tag per product ID; the main queue filter.
- **RBE (Risk Bearing Entity)** — who bears the decision risk on a request.
- **Delegated vendor** — who processes a request.
- **Pass-through (GHP)** — client uses our product with their own staff; no Cohere intake help.
- **Platcon** — platform/config team that now owns config + queue setup.

---

## 8. Questions discussed in this call

The actual questions raised (mostly Divy → Paridhi), with the short answer each got:

1. **"Walk me through the journey of a fax."**
   → Provider → West Fax → Cohere app → metadata → service case in Queue Management → queue → staff.
2. **"Are there two flows — via health plan to us, and us routing to health plan?"**
   → No. We always receive it **directly** and act **on behalf of** the health plan; we don't
   route faxes back out to them.
3. **"We're talking about the JSON, right?"**
   → Yes — the config is a JSON; first things in it are **specialty** and **product ID**.
4. **"Why do we have multiple fax lines — for categorization/segregation and to improve TAT?"**
   → For **workforce management / operational separation**, **not** TAT. (e.g. behavioral-health
   vs medical staff; inpatient vs outpatient.)
5. **"Why do the clients/providers even have multiple fax lines?"**
   → Legacy operations — providers are used to line-per-specialty; payers historically had
   separate teams. We can keep them split *or* merge into one queue.
6. **"Is there a video on how the different queue types work (client calls, etc.)?"**
   → Yes — **Jeremy's "launch queues" walkthrough**, now owned by **Platcon**; it's in the fax
   intake documentation.
7. **"What is RBE (Risk Bearing Entity) and why is it named that?"**
   → Who's **on the hook** for a request's decision; **delegated vendor** = who processes it.
   Less relevant for fax (we split by specialty), but best practice to fill it. (Do own research
   on Confluence / Koya GPT.)
8. **"What is manual fax forwarding and why do we have it?"**
   → To re-send **misdirected faxes** to the correct vendor/health-plan number, using
   pre-configured numbers + labels (with free-text for one-offs).
9. **"So a wrong fax coming to us gets redirected to a certain number?"** (clarifier)
   → Yes.
10. **"What's your expectation / the next step for me?"**
    → See the **Goal** below (Divy becomes first point of contact + first bug investigator).

**Deep questions parked for time** — Divy had more detailed questions the call couldn't fit;
capture them and bring to the next sync.

---

## 9. Goal — my role on fax intake config

> Framed from Paridhi's handoff at the end of the session.

Now that configuration ownership has moved to **Platcon**, my job is to be the **first point of
contact for fax intake configuration knowledge** — so people don't wait on product owners for
things that are already known. Concretely:

1. **Support Platcon on setup.** They configure independently, but when they get stuck I should
   be **empowered to tell them how to fix it** and unblock the setup.
2. **Advise solution architects scoping new clients.** When an SA asks "can the fax intake
   workflow do X?" (e.g. "can we have a free-text manual-forwarding number?"), I answer
   **yes/no and how** from the docs + this knowledge.
3. **Be the first investigator for fax intake bugs.** Many fax intake bugs exist because the
   **config wasn't set up correctly**. When one comes in, I:
   - check whether the config is set up the right way,
   - **test / experiment** to reproduce it,
   - then hand back to triage: *"here's what went wrong, here's what was needed."*
   Escalate to product owners only when it's genuinely beyond existing knowledge.

**North star:** turn "ask the product owner" into "ask Divy" for anything fax-intake-config
that's already documented — and be the line that separates **config-setup bugs** from **real
product bugs**. This feeds straight into the `cohere-bug-triage` flow (fax intake tickets →
check config first).

---

## 10. Open items / to research

- **Automation config** — separate from this; cover later.
- **Jeremy's "launch queues" walkthrough** — watch it (fax intake docs, now Platcon-owned).
- **RBE / delegated vendor** — Confluence "risk bearing entity" page + Koya/Cohere GPT for depth
  (intake doesn't own most of this side).
- **Parked deep questions** — write them down and raise at the next Paridhi sync.
