# System design: salon booking assistant (MVP)

Status: **draft**. The user was not available, so every scope answer below is
assumed and every decision is a recommendation (none user-accepted yet).
Plan, capacity, finish range and cut line: [plan](../plans/salon-booking-assistant.md)
(not restated here). Tickets: [docs/tickets/salon-booking-assistant/](../tickets/salon-booking-assistant/).

## Assumed answers

Questions I would have asked, the answer assumed, and what depends on it.
Decisions that depend on an assumed answer are provisional.

| # | Question | Assumed answer | Decisions that depend on it |
| --- | --- | --- | --- |
| Q1 | Which channel do customers use? | A chat widget on the chain's existing website, on pages where the customer is logged in. No SMS/WhatsApp in phase 1. | D3, D8 |
| Q2 | How are customers identified today? | The website already has customer login; our backend can verify its token (OIDC/JWT with a JWKS endpoint) and map the subject to the booking API's `customer_id`. | D3, G03 |
| Q3 | Who builds it, how many focused hours, how familiar? | Three full-time developers (Dev A, B, C), about 6 focused hours a day each; experienced with GCP and with the booking API they built; new to ADK (×1.5 on every estimate). | Plan capacity |
| Q4 | Deadline and afterwards? | 10 working days from start; continued and improved afterwards by the same three people, business-hours support. | Phasing |
| Q5 | Money for models and cloud? | About USD 300 a month for the MVP (model plus new cloud resources); no paid load tests. | D7, D9 |
| Q6 | What does the booking API support? | REST: list locations/services/staff, search availability, list a customer's appointments, create, cancel, probably reschedule. **Idempotency keys, atomic reschedule and slot-hold semantics are unknown**; G01 finds out. A staging environment with test customers exists. | D4, G01, G04 |
| Q7 | Business rules? | Moves and cancellations inside 24 hours of the appointment are refused in chat and sent to the salon phone; no deposits or payments in chat; services that need a consultation are not bookable in chat; booking horizon 60 days. | D5 |
| Q8 | Who uses it and who signs off? | External customers of five salons; the salon chain (our client) signs off policies, wording, privacy notice and the pilot salon (W1). Staff see results in the existing booking system. | Floor, W1 |
| Q9 | Language and time zone? | English only; all five salons in one time zone, taken from the booking API per location. | D5, G05 |
| Q10 | Does the booking system already notify customers? | Yes, it sends its own confirmation/cancellation email or SMS. The assistant sends no messages itself. | D2, failure grid |
| Q11 | Retention and privacy? | Chat transcripts kept 30 days, operation records 13 months; the salon chain updates its privacy notice (part of W1). | D6, G12 |
| Q12 | Existing GCP? | One existing GCP project and region with Cloud SQL for PostgreSQL that can host a new `assistant` database. | D6, D7 |
| Q13 | Traffic? | Up to about 100 conversations a day across five salons, at most 5 concurrent. | D7, D9 |
| Q14 | Who takes which work? | No preference given; split by strength (A: agent and model, B: identity and frontend, C: booking API and writes). | Plan owners |
| Q15 | Does the cut line suit you, and can the date move? | Pilot salon live in phase 1, other four salons first in phase 2; the pilot date may move from 10 to 12 working days rather than dropping a floor item (the reviewed plan fits 10 days only at the low end). | Plan |
| Q16 | Who maintains the chain's website? | Our team maintains the booking pages and can embed the widget on the website's staging and production sites. | G06, G09 |
| Q17 | Who approves using the existing GCP project, and how fast? | The team lead, within 1–3 working days (W0). | G05, G07 |

## Purpose and constraints

**Journey.** Priya, a customer of the Riverside salon, is logged in on the
chain's website on Sunday evening. Today she must open the booking form, page
through each stylist's calendar to move Tuesday's cut to Thursday, or phone
during opening hours. With the assistant she types "move my Tuesday cut to
Thursday afternoon, same stylist", sees two slots, taps **Confirm** on one,
and gets the booking system's confirmation. The appointment moves exactly
once; nobody else's appointments are visible or changeable.

**Outcome to improve (hypothesis, unmeasured).** Share of book/move/cancel
journeys completed online without a phone call, with guardrails: wrong-booking
corrections by staff and abandoned chats. No baseline exists; G09 starts
counting completed operations per salon from the operation records.

**What the model decides; what code controls.** The model interprets the
request, picks tools and arguments, and phrases replies. Code owns identity,
which appointments belong to the customer, availability truth, business rules,
the confirmation and every write.

**Non-goals for the MVP:** guest (not logged-in) booking, payments or
deposits, staff-side tools, waitlists, other channels, other languages,
remembering preferences across conversations.

## Delivery constraints, depth and deferred controls

| Scope-gate answer | Value |
| --- | --- |
| First useful version due, and after | 10 working days requested (Q4); the plan fits 12 (Q15); continued |
| People and hours | 3 full-time developers, about 6 focused h/day, new to ADK, experienced on GCP (Q3); same team runs it |
| Money | About USD 300/month (Q5) |
| Users and what they read | External customers using a live service; the salon chain judges the pilot (Q8) |
| Data touched and effects | Real personal data (names, contact details, appointments); reversible writes to real bookings that staff and the customer see; no money (Q7) |
| Delivery profile | **MVP or pilot**: first external users, real data, outside-visible writes; phase 1 ends with one pilot salon live (G09) |

| Concern | Depth now | Trigger that raises it |
| --- | --- | --- |
| Core judgment, measured | Build: 15-case labelled set run before launch (G05) | 30 or more cases on every release in CI (G11) |
| Identity and per-customer scope | Build: verified website login, owned sessions (G03) | Guest booking request (later) |
| Secrets | Build: Secret Manager, workload identity (G07) | Rotation with first credential incident or 90 days |
| External writes | Build: customer confirmation in code, operation record, idempotent or reconciled writes (G04) | Payments or deposits |
| Sensitive data | Build: minimal tool projections, no message content in logs or traces (D10) | Screening (Model Armor) if free-text fields must reach the model |
| Prompt injection and agency | Build: model holds no write tool (D2); adversarial cases in G05/G08 | Expanded suite in phase 2 (G14) |
| Budgets and loop limits | Build: per-turn call cap, per-customer daily allowance, kill switch (D9) | Shared budget store if replicas exceed 1 region or traffic ×10 |
| Memory | Minimal: ADK sessions only, no cross-session memory | Customers ask for "my usual" (later) |
| Frontend | Build: completed-JSON widget (D8) | Measured p90 reply > 6 s → streaming (later) |
| Hosting | Build: one Cloud Run service per environment, previous revision kept for rollback (D7) | Second region or SLA from the client |
| Observability | Build: structured logs without content in the D4 log schema, alert on uncertain/partial operations, ADK traces with content capture off (G07) | SLOs and dashboards in phase 2 (G13) |
| Release engineering | Build: pinned model and ADK, prompt in repo, release manifest, offline tests in CI (G07) | Live eval gate in CI (G11) |
| Performance and cost tuning | Defer | Measured cost per completed operation above assumption, or p90 latency complaint |

**Floor kept:** no secrets in code, prompts, logs or documents; spend stop
(`RunConfig.max_llm_calls` plus per-customer allowance plus kill switch, with a
billing budget alert as notification only); no booking change without the
customer pressing Confirm on a card built by code from the stored proposal;
real personal data only for the logged-in customer's own records, minimised
and kept out of logs; pinned model ID. No risk accepted beyond the floor.

**Who may use it:** logged-in customers of the pilot salon (G09), then all five
salons (G10). **Graduation conditions** before the other four salons: one
pilot day with zero unresolved uncertain or partial operations and no
incident (G10). Before guest users, other channels or payments: the
corresponding later items.

| Deferred control | Why it waits | What would bring it forward |
| --- | --- | --- |
| Full evaluation set (30+) and live gate in CI | Cut from phase 1 to fit the calendar; the 15-case set covers each action and the adversarial cases | Second prompt or model change, or before G10 (G11) |
| Transcript deletion job and erasure requests | 30-day retention not reached during phase 1 | Must ship before day 30 after launch (G12) |
| SLOs, dashboards, production-to-eval loop | No baseline traffic yet | Two weeks of production data (G13) |
| Staff reconciliation screen | Few operations; runbook plus SQL is enough at one salon | More than 2 uncertain/partial ops a week (later) |

## Guarantees and acceptance

| Invariant | Enforcing component and authority | Failure outcome | Planned verification |
| --- | --- | --- | --- |
| I1 A customer sees and changes only their own appointments | Gateway verifies the website token and sets `customer_id` in session state (D3); tools and executor read it from state and the booking API filters by it | 401/404, no model call or provider call | G03/A2, G03/A3, G02/A2, G04/A4 |
| I2 No booking changes without the customer confirming the exact proposal | Model has no write tool (D2); executor runs only from the Confirm endpoint, bound to the stored proposal hash (D4) | Nothing written | G02/A5, G04/A3, G06/A2 |
| I3 One confirmation causes at most one booking change | Operation record keyed by proposal, claimed before dispatch; provider idempotency key or reconcile-before-retry (D4) | Duplicate refused; uncertain outcome held for reconciliation | G04/A2, G04/A5 |
| I4 Business rules hold regardless of what the model says | Rule checks in the executor at execution time (D5) | Refused with phone fallback, no write | G04/A7, G04/A3 |
| I5 The customer is never told a change happened unless the booking API confirmed it | Result shown from the executor's operation status, not model text (D8) | "We're checking" for uncertain; partial explained | G04/A5, G04/A6, G06/A3 |
| I6 Spend per turn and per customer is bounded | `max_llm_calls`, daily allowance, kill switch (D9) | Polite limit message, no model call | G02/A6, G03/A6, G03/A9 |

## Architecture and decisions

```text
Browser widget (logged-in page)
   │  POST /chat {session_id, text}      POST /proposals/{id}/confirm
   ▼
Cloud Run: assistant service  ── verifies website token (JWKS) ─▶ customer_id
   ├─ Gateway (FastAPI): auth, session ownership, allowance, kill switch
   ├─ ADK Runner + LlmAgent "booking_assistant" (gemini via Vertex AI)
   │     tools: list_services, find_slots, list_my_appointments      (read)
   │            propose_booking, propose_move, propose_cancel        (store proposal only)
   └─ Executor (plain code): recheck rules + availability → booking API write
         │                                   │
         ▼                                   ▼
Cloud SQL Postgres "assistant":          Booking API (ours): staging / prod
 ADK sessions, proposals, operations,    authoritative appointments; sends its own
 daily allowance                         confirmation email/SMS
```

Trust boundaries: the browser and model are untrusted for authority; the
gateway and executor are trusted code; the booking API is authoritative for
appointments and availability.

| ID | Requirement | Design choice | Reason | Tradeoff / alternative | Verification |
| --- | --- | --- | --- | --- | --- |
| D1 | Interpret free-text requests over a small capability set | One `LlmAgent`, six function tools written by us | One responsibility, one credential, one context; function tools expose exactly what we choose | Sub-agents per intent add routing without a distinct boundary; `OpenAPIToolset` from the booking API would import write endpoints and large descriptions | Declaration dump lists six tools, none writes (G02/A5) |
| D2 | Floor: no outside-visible change without human approval; I2 | Model can only *propose*; proposals are stored and rendered as cards by code; writes run only from the Confirm endpoint | Removes the write leg from the model, so injected or confused text cannot change bookings | One extra click; custom UI instead of ADK's native tool confirmation (whose known limitations would need checking against the pin) | Scripted model "cancels" with no confirm → zero provider writes (G02/A5, G04/A3) |
| D3 | I1 | Gateway verifies the website token, derives `customer_id`, stores it in session state at creation and checks session owner on every request; tools never accept a customer ID argument | Authority comes from verified identity, not from model arguments or session IDs | Depends on Q2; guest booking would need OTP (later) | G03/A1–A4, G02/A2 |
| D4 | I3, I5 | `operations` table: `op_id` (UUID, also the provider idempotency key if supported), `proposal_id` unique, `customer_id`, kind, canonical payload hash, status `claimed → dispatched → succeeded / failed / uncertain / partial / stale`. Claim row before dispatch; if the claim's commit outcome is unknown, re-read by `proposal_id` before dispatch. Log schema (frozen, no personal data): `{event: "operation_status", op_id, status, kind, location_id, ts}`. Retry a write only if G01 proves the key dedupes; otherwise one attempt and reconcile by listing the customer's appointments. Move uses an atomic reschedule endpoint if G01 confirms one, else book-new-then-cancel-old with `partial` on second-step failure | A timeout cannot be treated as "nothing happened"; the record survives restarts | Extra table and states; reconciliation is manual (runbook) in phase 1 | G04/A2, A5, A6, A11, A12 |
| D5 | I4 | Proposal record (fixed contract shared by G02, G04, G06): `{proposal_id, customer_id, kind, location_id, service_id, staff_id?, start_utc, end_utc, appointment_id?, price_display, expires_at (10 min), payload_hash}`. Executor rechecks at execution: owner, expiry, 24 h cutoff, 60-day horizon, chat-bookable service, slot still free / appointment unchanged. Rule values are configuration with these defaults, confirmed in W1; the consultation-only list's source is found in G01 | Rules live in code, not the prompt; the shared schema lets three people build in parallel | Schema change after day 1 costs rework in three goals | G04/A3, A7; G08/A1 integration |
| D6 | Sessions survive restart; records for reconciliation | ADK `DatabaseSessionService` on a new `assistant` database in the existing Cloud SQL Postgres; proposals, operations and allowance in the same database | Reuses an operated store (Q12); one transaction scope for claim | Cloud SQL connection limits shared with the booking API (check in G07) | G03/A5, A8 |
| D7 | Hosting and model within USD 300/month | Cloud Run (staging, prod), min instances 0 staging / 1 prod, dedicated service account; Vertex AI model **`gemini-3.8-flash`** pinned (stable, released 2026-09-02, no shutdown announced in the skill's lifecycle snapshot `model-lifecycle-2026-10-01.json`, checked_on 2026-10-08) | Newest stable flash with no retirement in the plan horizon; avoids `gemini-3.6-flash` (Vertex retirement 2026-11-19) and `gemini-3.7-flash` (2027-01-28) | Newest model has the least field history; fallback candidate `gemini-3.5-flash` (Vertex retirement 2027-05-19 or later). Prices not looked up (no network) | G01/A3 re-checks the lifecycle page; G05/A3 measures quality and tokens |
| D8 | I2, I5; simple UI | Completed-JSON contract: `POST /chat` → `{messages:[{text}], proposals:[proposal card], operation?:{op_id,status,details}}`; `POST /proposals/{id}/confirm` → operation; `GET /operations/{op_id}`; `GET /config` → `{enabled, salons: {location_id: bool}}`; 503 `{error: "assistant_off"}` when a flag is off. The widget sends the website's login token as `Authorization: Bearer`; the gateway allows CORS only from the website's origins. Cards and results rendered from structured fields; model text shown as plain text | Confirmation and outcome never depend on model wording; no streaming state to build | No progressive text; replies arrive whole (expected 2–6 s, unmeasured) | G06/A2, A3, A5, A7; G03/A9 |
| D9 | I6; budget | `RunConfig.max_llm_calls=8` per turn; 40 turns per customer per day and 1,000-character message cap checked in the gateway (Postgres counter); global and per-salon kill switch read per request (G03); Cloud Billing budget alert at USD 300 (notification only) | Bounds work before it is spent; kill switch is the hard stop | A heavy legitimate user hits the cap (polite message, phone fallback) | G02/A6, G03/A6, G03/A9, G07/A6 |
| D10 | Personal data minimised | Tool results projected to whitelisted fields (no staff notes, no other customers, no contact details); telemetry content capture off; logs carry IDs and statuses, never message text | Less to leak via model context, logs or traces | Debugging needs the session store (access restricted to the team) | G02/A5, G07/A4 |
| D11 | Behaviour comparable across releases | Pin `google-adk==2.8.0` now (the version most specialist skills' `compatibility.md` record; no installed version exists to check against; confirmed by G02/A10, the first implementation goal), pin model ID, prompt as versioned code, release manifest (image digest, model ID, prompt hash, tool-schema hash) | Releases roll back as one unit | Planned migration work when the model retires | G07/A3; next lifecycle check on the team calendar |

### Model-facing contracts

| Surface | Contract | Implementing skill and verification |
| --- | --- | --- |
| Instruction | Role, scope (book/move/cancel at five salons), always propose then wait for Confirm, never claim a change happened, phone fallback; current date and salon list come from state templating, not hard-coded | `adk-agent-instructions`; rendered-request test (G05/A1) |
| Tools | 3 read + 3 propose, primitive parameters, IDs not names, results `{status, ...}` bounded to 10 slots / 10 appointments, actionable errors | `adk-tool-interface-design`; declaration dump (G02/A5) |
| Output | Plain text reply; proposals and outcomes travel as structured tool results and gateway fields, so no `output_schema` | `adk-model-and-output-contracts` for model pin (G01/A3) |

## Data and authority

| Data / operation | Owner and scope | Writers / readers | Source and freshness | Lifetime / erasure |
| --- | --- | --- | --- | --- |
| Appointments, availability | Booking API, per customer | Executor writes; read tools read | Authoritative, live; rechecked at execution | Booking system's own policy |
| ADK session events | Customer (owner check, D3) | Runner | Conversation only; not a source of booking truth | 30 days (deletion job G12) |
| Proposals | Customer | Propose tools write; executor, widget read | Snapshot at proposal; expires 10 min | 13 months with operations |
| Operations | Customer; team for reconciliation | Executor | Authoritative for "what the assistant did" | 13 months |
| Daily allowance counters | Customer | Gateway | Per day | 7 days |

Identities: end user = website login subject → `customer_id`; workload =
Cloud Run service account (Vertex AI user, Cloud SQL client, Secret Manager
accessor for the booking-API credential only); booking-API credential = a
service credential scoped to the assistant, held in Secret Manager. No
delegated OAuth.

### Security posture

| Agent | Private data | Untrusted content | Write or egress | Resolution |
| --- | --- | --- | --- | --- |
| booking_assistant | Own appointments only (D3, D10) | Customer's own text; booking-API text fields (projected out, D10) | None: propose tools store a draft only | Write leg removed (D2); writes in code behind Confirm |

Tool tiers: read (3), propose (3, no external effect). Irreversible: none
reachable by the model. No code executor. Adversarial cases: G05/A2 (eval) and
G08/A2 (staging).

## Budgets and capacity

Expected per turn: 1–3 model calls, 0–2 booking-API reads; bounded by
`max_llm_calls=8` and two read attempts per tool. About 100 conversations ×
6 turns × 2 calls ≈ 1,200 model calls/day (assumption). Cost per call not
looked up (no network): G05/A5 measures tokens per conversation and G08
compares with the USD 300 budget. Restart: allowance and operations persist in
Postgres; an in-flight turn is lost and the customer resends. Exhaustion:
limit message with salon phone; operations already confirmed still complete.

## Failure and recovery

Coverage grid (integrations):

| Integration | Unavailable or slow | Rejects the request | Write outcome unknown | Partial multi-step change | Credential expired or revoked | Rate limited or out of quota | Duplicate or concurrent request | Untrusted or malformed content |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Booking API reads | G02/A3 | G02/A4 | n/a: read only calls | n/a: single read calls | G02/A4 | G02/A8 | n/a: reads are idempotent | G02/A5 |
| Booking API writes | G04/A9 | G04/A8 | G04/A5 | G04/A6 | G04/A10 | G04/A9 | G04/A2 | G04/A5 |
| Website login (token, JWKS) | G03/A4 | G03/A2 | n/a: no writes there | n/a: single verification step | G03/A2 | G03/A4 | n/a: stateless token verification | G03/A2 |
| Gemini on Vertex AI | G02/A9 | G02/A9 | n/a: model has no write | n/a: model has no write | G02/A9 | G02/A9 | n/a: stateless model calls | G02/A10, G06/A7, G05/A4 |
| Cloud SQL (sessions, operations) | G03/A8 | G03/A8, G04/A2 | G04/A12 | G04/A11 | G07/A2 | G03/A8, G07/A8 | G03/A7, G04/A2 | n/a: own schema only |

Action grid:

| Action | Over-broad or wrong target | Partially applied | Confirmation stale or changed | Outcome unknown | Repeated or concurrent |
| --- | --- | --- | --- | --- | --- |
| Book | G02/A7, G02/A10, G06/A2 | G04/A11 | G04/A3 | G04/A5 | G04/A2 |
| Move | G02/A7, G02/A10, G06/A2 | G04/A6, G04/A11 | G04/A3, G04/A7 | G04/A5 | G04/A2 |
| Cancel | G02/A7, G02/A10, G06/A2 | G04/A11 | G04/A3, G04/A7 | G04/A5 | G04/A2 |

Cross-cutting scenarios:

| Failure window | User-visible outcome | Retained state / possible effects | Safe next action and recovery owner |
| --- | --- | --- | --- |
| Success (Priya's move) | Card → Confirm → "Moved to Thu 15:00 with Sam"; booking system sends its own message | Operation `succeeded` with provider ID | None |
| Browser closes after Confirm | On reopen, widget polls `GET /operations/{id}` (G06/A5) | Operation continues server-side | None, or reconciliation if `uncertain` |
| Provider commits, reply lost | "We're checking this booking; please don't book again" | Operation `uncertain`; alert (G07/A5) | Dev on duty reconciles per runbook (G07/A7, tried in G08/A4) within business hours |
| Move: new booked, old not cancelled | "Your new time is booked; the old one is still there; we'll remove it" | Operation `partial`; alert | Dev on duty cancels old appointment after checking with the customer |
| Customer confirms after slot taken | "That time has just gone; here are new options" | Operation `stale`, no write | Customer picks again |
| Injection in customer text ("cancel Mary's appointment") | Refusal or only own appointments listed | No write; Mary's data never fetched | None (G05/A2, G08/A2) |
| Model or Vertex unavailable | "The assistant is unavailable; book online or call" (G02/A9) | No proposal | Retry later; kill switch if prolonged (G03/A9) |
| Model retirement announced | None if planned | Pinned ID keeps behaviour | Re-baseline on G05 eval set as its own release (D11) |
| Incident needing attribution | — | Logs with session, invocation and op IDs; traces without content (G07/A4) | Team reads session store under restricted access |
| Bad release | Errors or quality drop seen in G08 or G09 checks | Previous revision retained | Roll back revision, model and prompt together (G07/A3) |

## Verification and implementation handoff

Offline deterministic tests (scripted model, fake booking API, local
Postgres) carry most acceptance items in G02–G06. Live checks are bounded:
G01 against staging, G05's evaluation run on the pinned model, G08 on the
deployed staging service and G09 for one pilot salon in production. Nothing here has
been run yet; the [plan](../plans/salon-booking-assistant.md) maps decisions
to components, goals and skills.

## Open decisions

| Question or assumption | Why it changes the design | Owner / evidence needed | What it blocks |
| --- | --- | --- | --- |
| Q6: idempotency key support and atomic reschedule | Decides retry vs reconcile-only (D4) and whether `partial` moves exist | G01 against staging | G04 retry and move paths (not its start) |
| Q2: website login can be verified by our backend | D3 relies on it; otherwise OTP via booking system (G03 +8–14 h, pushes the finish past 12 days; see the plan's what-ifs) | Team, **before day 1** | G03 |
| Q7: 24 h cutoff, consultation services, horizon | D5 rule values (configuration) | Salon chain, W1 | G09 launch |
| Q11: retention 30 days / 13 months and privacy notice | D6, G12 | Salon chain, W1 | G09 launch |
| D7 model choice | Quality and cost unmeasured | G05/A3, A5 | None (fallback ID named) |
| Q15: cut line and date | Pilot salon in phase 1, four more in phase 2; 12 working days, or name what to drop | User | Plan date |
| Q16, Q17: website ownership, GCP approval speed | G06 embedding; W0 length | Team lead, day 1 | G06, G05, G07 |
