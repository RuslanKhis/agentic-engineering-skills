# System design: salon booking assistant (MVP)

Status: **draft**. Every product answer below was assumed because the requester
could not be asked; decisions that depend on them are marked *provisional*.
Plan: [docs/plans/salon-booking-assistant.md](../plans/salon-booking-assistant.md).
Tickets: [docs/tickets/salon-booking-assistant/](../tickets/salon-booking-assistant/).

## Assumed answers

| # | Question that could not be asked | Assumed answer | Decisions that depend on it |
| --- | --- | --- | --- |
| A1 | Who talks to the assistant: salon customers, or front-desk staff on their behalf? | Salon customers, through a chat widget on the existing booking website | D1, D2, D5, all of the floor |
| A2 | How do customers sign in today? | The existing booking site already has customer login and issues a signed token (JWT with a JWKS endpoint) that our backend can verify; the token carries the booking API's customer ID | D2, G04 |
| A3 | Hours and experience of the three developers | All three work on this full time for 10 working days, about 6 available hours a day at focus 0.6 (3.6 focused h/day each); strong Python, new to ADK (estimates ×1.5), comfortable with GCP; one existing GCP project | Capacity and cut line, plan |
| A4 | Money for models and cloud | About US$300 a month during the MVP, Vertex AI billed to the existing project | D6, model choice |
| A5 | What the booking API offers | The team owns it; it has a staging environment, endpoints for services, free slots, a customer's appointments, create, reschedule and cancel; it enforces business rules (opening hours, cancellation window). **Unknown:** whether create/reschedule/cancel accept an idempotency key and whether a request can be looked up by a client reference | D3, D4, G01 (discovery) |
| A6 | Channels and languages | Web chat only; English only | D5; voice, SMS, WhatsApp and other languages are later items |
| A7 | Payments, deposits, multi-service bookings | None in phase 1: one service per appointment, optional stylist preference, no money moves | Floor depth; a deposit would make the write a payment |
| A8 | Customer notifications | The booking API already emails/SMSes the customer on create, reschedule and cancel; the assistant sends nothing itself | D3 (no egress tool) |
| A9 | Launch audience | Real customers of all five salons, behind a "Book with the assistant (beta)" link; the existing booking form stays available as the fallback | Failure handling, kill switch in G08 |
| A10 | Data location and retention | Personal data (name, contact, appointment history); deploy in the same region as the booking API; conversations kept 30 days | D2, D6, G07 |

## Purpose and constraints

**Journey.** Maya, a signed-in customer of the Riverside salon, types "can I move
my Thursday cut to Saturday morning with Jo?". Today she must find the
appointment in the booking form, cancel and rebook, which customers abandon on
mobile and front desks then handle by phone (no baseline measured; see
*Outcome measurement*). Intended outcome: the assistant finds her Thursday
appointment, shows Jo's Saturday-morning slots, and after she presses
**Confirm** on a card showing old and new times, the appointment is moved in the
booking system and she sees the confirmed result. Fixed constraints: the
existing booking API is the only system of record; ship in two weeks with
three developers; keep improving afterwards.

**Model versus code.** The model interprets the request, asks for missing
details, picks which read tool to call and drafts a proposal. Code owns the
customer's identity, the salon time zone and today's date, the proposal's
exact contents, the confirmation, the write, retries and the outcome shown on
the card.

Observed facts: the repository holds only skill packages (no application code,
manifests or tests yet). Everything else is a proposal or assumption above.

## Delivery constraints, depth and deferred controls

| Scope-gate answer | Value |
| --- | --- |
| First useful version due, and after | 10 working days; continued (phase 1 code is kept) |
| People and hours | Three developers, A3; they run it afterwards |
| Money | A4, Vertex AI; billing budget alert at 50/90/100 % |
| Users and what they read | External customers using the live widget (A1, A9); the team reads traces and outcomes |
| Data and effects | Real personal data; reversible writes visible to customers and stylists (book, move, cancel); no money |
| Delivery profile | **MVP / pilot**: first external users completing the journey safely, with failures and cost visible |

| Concern | Depth now | Trigger that raises it |
| --- | --- | --- |
| Core judgment, measured | Build: 30-case evaluation set run before release (G06, G09) | CI gate in phase 2 (G10) |
| Identity and per-customer scope | Build: verified existing-site token, cross-customer denial tests (G04) | — |
| Secrets | Build: workload identity, booking API credential in Secret Manager (G08) | Rotation when the credential is shared beyond the service |
| External writes | Build: customer confirmation in code, durable proposal/operation record, uncertain outcomes reconciled (G03) | Provider idempotency key if G01 finds none: phase 2 G11 |
| Sensitive data | Build at minimal cost: field-minimised tool results, no message content in logs, 30-day retention (G07) | Model Armor / SDP screening when free-text notes or other channels arrive |
| Injection and agency | Build structurally: no write or egress tool on the agent (D3); customer input only affects their own scope | Adversarial suite when a tool reads third-party text (phase 2 G13) |
| Budgets and loop limits | Build: `max_llm_calls` per turn, per-customer daily turn allowance, billing alert (G07) | Shared reservation when traffic exceeds one instance |
| Memory | Sessions only (Postgres); no long-term memory | Customers ask to reuse preferences ("my usual") |
| Frontend | Build: minimal widget with confirmation card, request/response JSON (G05) | Streaming when p95 turn time exceeds ~6 s |
| Hosting | Cloud Run, one service, previous revision kept for rollback (G08) | — |
| Observability | Build: Cloud Trace spans, token usage and operation outcomes in structured logs (G08) | SLOs and alerts in phase 2 (G12) |
| Release engineering | Minimal: pinned model and prompt version in a release manifest, unit tests in CI; eval run by hand before release | Evaluation in CI (G10), before the second prompt change |
| Performance and cost tuning | Defer | Measured p95 latency or cost per completed booking above target |

**Floor kept.** No secrets in code, prompts or logs. Spend stop: `max_llm_calls`
per invocation, a per-customer daily allowance, and a billing budget alert (an
alert, not a cap). No booking change without the customer pressing Confirm on a
card rendered from the stored proposal. Personal data limited to what the
journey needs and kept out of logs. Model ID pinned.

**Graduation conditions** (before more channels, staff use or deposits):
evaluation gate in CI; idempotent writes confirmed with the booking API owner;
SLOs and alerts with an on-call owner; adversarial suite once third-party text
is read.

**Capacity and cut line.** Capacity 3 × 10 days × 3.6 h = 108 focused hours;
25 % reserve leaves 81 h. Phase 1 (G01–G09) and its fit are computed in the
plan's *Delivery profile and capacity* section. Phase 2 and later wait.
*Please confirm or move the cut line.*

## Guarantees and acceptance

| Invariant | Enforcing component and authority | Failure outcome | Planned verification |
| --- | --- | --- | --- |
| I1 A customer reads and changes only their own appointments | Gateway verifies the site token; `customer_id` written to session state by code; tools read it from state, never from model arguments; confirm endpoint checks proposal owner; booking API calls carry that ID | 403 or "not found"; nothing read or written | G04 cross-customer tests: forged session ID, other customer's appointment ID in the message, other customer's proposal ID on confirm |
| I2 No booking change happens without the customer confirming those exact details | Agent has only *propose* tools; only `POST /proposals/{id}/confirm` executes, using the stored proposal | Proposal expires after 10 min; nothing written | G03: scripted model calls every tool; assert zero booking-API writes until confirm; confirm with changed payload is rejected |
| I3 One confirmed proposal causes at most one booking change | Atomic claim on the operation record (`pending → executing`), idempotency key = proposal ID if the API supports it (G01), otherwise lookup-before-retry | Double click returns the same outcome; timeout leaves status `uncertain`, never re-sent blindly | G03: double confirm, timeout after provider commit, restart mid-execution |
| I4 What the customer sees as "confirmed" is what the booking system holds | Card status rendered from the operation record, which is set only from the booking API's response or a reconciliation lookup | "We're checking this booking" for `uncertain` | G03/G05: lost-response case shows `uncertain`, then `succeeded` after lookup |
| I5 A runaway or abusive conversation stops | `RunConfig.max_llm_calls` = 12 per turn; daily allowance of 60 turns per customer (assumed) in Postgres | Polite stop with link to the booking form | G07 tests |

## Architecture and decisions

```text
Browser (existing booking site, signed in)
  │  site JWT
  ▼
Cloud Run: booking-assistant (FastAPI)
  ├─ gateway: verify JWT → customer_id; session ownership; admission (allowance)
  ├─ ADK Runner + LlmAgent "booking_assistant" (gemini-3.8-flash on Vertex AI)
  │     read tools: list_services, find_slots, list_my_appointments
  │     propose tools: propose_booking, propose_move, propose_cancel  → proposal row
  ├─ POST /proposals/{id}/confirm  → executor (code only) → booking API write
  └─ Postgres (Cloud SQL): ADK sessions, proposals/operations, allowance counters
        │
        ▼
Existing booking API (system of record; sends customer notifications)
```

| ID | Requirement | Design choice | Reason | Tradeoff / alternative | Verification |
| --- | --- | --- | --- | --- | --- |
| D1 *(provisional, A1)* | Interpret free-text requests over a handful of capabilities | One `LlmAgent` with six narrow function tools; no sub-agents | The journey is one conversation over one API; more agents add routing without a distinct boundary | One prompt must cover book, move and cancel; split only if evaluation shows confusion | G06 tool-selection accuracy on 30 cases |
| D2 *(provisional, A2)* | I1 | Identity from the existing site's token, verified in the gateway; `customer_id`, `salon_tz`, `today` placed in session state by code | Reuses the login customers already have; the model cannot select identity | Depends on the site token format; a standalone widget would need its own login (magic link) | G04 tests |
| D3 | I2, I3, A8 | Model *proposes*, code *executes*: propose tools validate against the booking API and store a proposal; the browser's Confirm calls the executor; the agent holds no write or egress tool | Confirmation is bound to stored details and outside the model's reach; an injected instruction cannot write | Two-step UX and a proposal table, compared with ADK's built-in tool confirmation, which would keep the write inside the agent's tool path ([known limitations](https://adk.dev/tools-custom/confirmation/#known-limitations)) | G03 forbidden-write test |
| D4 *(provisional, A5)* | I3, I4 | Durable operation record per proposal in Postgres; idempotency key = proposal ID if supported; else before any retry, look up the customer's appointments for the slot/appointment and reconcile | A timeout can hide a committed write; the proposal ID survives retries and restarts | A table and reconciliation code; no background worker in phase 1 (reconcile on status poll and by operator query) | G03 lost-response and restart cases |
| D5 *(provisional, A6, A9)* | Customers finish the journey on mobile web | Small widget calling a JSON API (`/chat`, `/proposals/{id}`, `/proposals/{id}/confirm`); confirmation card rendered from the proposal row, not model text | Smallest frontend that can show an authoritative card | No streaming in phase 1; AG-UI/CopilotKit not needed for one card type | G05 browser check |
| D6 *(provisional, A4, A10)* | Kept, recoverable state on a multi-instance host | Cloud Run + Cloud SQL Postgres (smallest tier) for ADK `DatabaseSessionService`, proposals and allowance counters; Vertex AI for the model in the booking API's region | One managed store for three small needs; Cloud Run fits a stateless FastAPI app the team can operate | Cloud SQL has a fixed monthly cost; Agent Runtime would host the agent but not the confirm endpoint and gateway | G08 restart keeps session and proposal |

**Versions.** No ADK version is installed. Working assumption: `google-adk==2.8.0`,
the version the specialists' compatibility notes were checked against
(`adk-agent-observability/references/compatibility.md`,
`adk-operational-guardrails/references/compatibility.md`); confirming the pin is
an acceptance item of G02. Model: `gemini-3.8-flash` (stable, released
2026-09-02, no retirement announced) from
`adk-model-and-output-contracts/assets/model-lifecycle-2026-10-01.json`
(checked_on 2026-10-08). Not `gemini-3.6-flash` (Vertex retirement 2026-11-19)
or `gemini-3.7-flash` (2027-01-28), which retire inside the plan's horizon.
Vertex availability in the chosen region, and prices, are unverified (no
network access in this session): G02 verifies them before relying on them.

### Model-facing contracts

| Surface | Contract | Implementing skill and verification |
| --- | --- | --- |
| Instruction | Booking assistant for the five named salons; always resolve relative dates against `{today}` and `{salon_tz}` from state; ask when salon, service or time is ambiguous; never claim a change happened, the card shows it; refuse unrelated requests. Identity, date, salon list and policies come from state or tools, not prose | `adk-agent-instructions`; rendered-request test (G02) |
| Tools | `list_services(salon_id)`, `find_slots(salon_id, service_id, date_from, date_to, stylist_id?)`, `list_my_appointments()`, `propose_booking(...)`, `propose_move(appointment_id, new_start, stylist_id?)`, `propose_cancel(appointment_id)`. All return `{status, ...}` with actionable errors, at most 10 slots per result; no customer contact fields | `adk-tool-interface-design`; declaration dump and size (G02, G03) |
| Output and model | Plain text replies; the proposal's structure lives in the tool result, not an `output_schema`. Pinned `gemini-3.8-flash`, low temperature; no failover model in phase 1 | `adk-model-and-output-contracts`; pin recorded in release manifest (G08) |

## Data and authority

| Data / operation | Owner and scope | Writers / readers | Source and freshness | Lifetime / erasure |
| --- | --- | --- | --- | --- |
| Appointments, services, slots | Booking API, per customer / per salon | Booking API / tools | Authoritative; re-read before every execution | Booking system's policy |
| Conversation session | Customer (`customer_id` owner column) | Runner / gateway | ADK session in Postgres | 30 days, nightly delete (G07) |
| Proposal / operation | Customer | Propose tools, executor | Snapshot of details at proposal time; rechecked at confirm | 90 days for support, then delete (assumed) |
| Allowance counter | Customer, per day | Gateway | Postgres | 7 days |

Identities: end customer (site JWT); Cloud Run service account (Vertex AI user,
Cloud SQL client, secret accessor); booking API service credential in Secret
Manager. No delegated OAuth.

### Security posture

| Agent | Private data | Untrusted content | Write or egress | Resolution |
| --- | --- | --- | --- | --- |
| booking_assistant | The signed-in customer's appointments | The customer's own messages; staff-written service names | None: proposals only; execution is outside the agent | Trifecta broken by removing the write leg (D3); customer text can only affect that customer's own proposals, which they confirm |

Tool tiers: read (three tools), propose (three tools, write only a proposal row
scoped to the caller), execute (not a tool). Phase 2 G13 adds an adversarial
suite if any tool starts returning free text from third parties (for example
stylist notes).

## Budgets and capacity

Assumed workload: five salons, up to ~300 assistant conversations a day,
~6 turns each, ~2.5 model calls per turn (one tool round trip) → ~4,500 model
calls a day, ~3k input / 200 output tokens per call. Cost is symbolic until G02
reads current Vertex prices; the A4 allowance must cover model calls plus Cloud
SQL's fixed tier. Enforcement: `max_llm_calls`=12 per invocation; 60 turns per
customer per day (gateway admission); billing alert. Concurrency at this volume
fits one Cloud Run instance with `min-instances=0`; turn latency target
≤ 6 s p95 (assumption, measured in G09).

## Failure and recovery

| Failure window | Customer sees | Retained state / possible effect | Safe next action and owner |
| --- | --- | --- | --- |
| Success (Maya's move) | Card: "Moved to Sat 10:00 with Jo" | Operation `succeeded` with booking reference; booking API notifies her | — |
| Another customer's appointment ID in the message | "I can't find that appointment" | Nothing | — (I1 tests) |
| Slot taken between proposal and confirm | "That time was just taken"; agent offers new slots | Operation `failed: conflict` | Customer picks again |
| Double click / two tabs confirm | Same card result twice | One write (atomic claim) | — |
| Booking API timeout after it committed | "We're checking this booking" | Operation `uncertain` | Status poll runs lookup; if still unknown after 3 polls, card says "please check your confirmation email"; operator query lists `uncertain` rows daily (Dev B, owner of the confirm flow) |
| Instance restarts mid-execution | Status poll shows `uncertain` | Row stuck `executing` > 60 s is treated as `uncertain` | Same lookup path |
| Model / Vertex unavailable or malformed reply | "Assistant unavailable, use the booking form" with link | Session kept, no proposal | Bounded SDK retries only; no app retry loop |
| Proposal older than 10 min | Confirm disabled, "please ask again" | Proposal `expired` | — |
| Allowance exhausted | Polite stop + booking-form link | Counter | Resets next day |
| Bad release | Widget beta link hidden by flag | Sessions retained | Roll back to previous Cloud Run revision (G08) |

## Verification and implementation handoff

Offline: tools and executor against a fake booking API; Runner tests with a
scripted model (I1–I5). Local integration: booking API **staging** with a test
customer; process restart for persistence. Bounded live: G06's 30-case run on
the pinned model (≤ 200 model calls). Hosted: G09 end-to-end on Cloud Run staging,
then the beta link. **Outcome measurement** (hypothesis, not yet a baseline):
share of assistant conversations ending in a succeeded operation, and front-desk
reschedule calls per week before and after; guardrail: `uncertain` and
`failed` operation rate.

Observability and release (G08): ADK OpenTelemetry to Cloud Trace with
prompt/response content capture **off**; structured logs with session ID,
proposal ID, operation status, token counts; release manifest = image digest,
prompt version, model ID, tool schema hash, secret version. Rollback = previous
Cloud Run revision plus flag. SLOs wait for phase 2 (G12).

Goals, owners and estimates: [plan](../plans/salon-booking-assistant.md).

## Open decisions

| Question or assumption | Why it changes the design | Owner / evidence needed | What it blocks |
| --- | --- | --- | --- |
| A2 site token format and claims | D2 depends on verifying it | Dev C reads the site's auth code (G04 first hour) | G04; fallback magic-link login would add ~1 day |
| A5 idempotency key / client-reference lookup | Decides D4's mechanism | Dev A, G01 | G03's retry path |
| A1, A9 customers vs staff; all salons vs one | Changes identity and launch scope | Product owner | G09 launch scope |
| Retention periods (A10) | Legal basis for personal data | Product owner / whoever handles GDPR | G07 deletion job values |
| Cut line | Phase 1 scope | The three developers | — |
