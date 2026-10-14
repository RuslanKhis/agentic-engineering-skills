# System design: salon booking assistant (MVP)

Status: **draft**. Written in one pass with no access to the user; every
decision marked *provisional* depends on an assumed answer below. Decisions
live here; the [plan](../plans/salon-booking-assistant.md) and
[tickets](../tickets/salon-booking-assistant/) refer to them by ID.
Capacity, finish range and cut line: see the plan's summary.

## Assumed answers

The user was not available. Each row is a question that would have been asked,
the answer assumed, and what depends on it.

| # | Question | Assumed answer | Decisions that depend on it |
| --- | --- | --- | --- |
| A1 | When must the first version exist, and is it continued? | Live for real customers in 10 working days (by 2026-10-28); kept and improved afterwards | Phase 1 cut, kept-code form |
| A2 | Who builds it, hours, familiarity? | Three developers (Dev A, B, C), about 5 focused hours a day each on this; fluent in Python and GCP, new to ADK (1.5× multiplier applied in the plan); the same team runs it | Estimates, owners |
| A3 | Money for models and cloud? | Up to about US$300 a month during the MVP (illustrative) | D6, D9 |
| A4 | Who uses and judges it? | Signed-in customers of the five salons, through a chat widget on the existing booking website; the salon chain's owner judges the MVP | D3, D8, phase 1 "done" |
| A5 | What data, what effects? | Real customer personal data (name, contact, appointment history); reversible writes (book, move, cancel) that make the booking system notify the customer; **no payments, deposits or fees** | Floor, D4, D5 |
| A6 | How do customers sign in today? | The booking website has customer login and issues a session token the backend can verify (JWT with JWKS, or an introspection endpoint) | D3 |
| A7 | What does the booking API offer? | It is ours: server-to-server key; reads for salons, services, stylists, availability, a customer's appointments; create, native reschedule and cancel; it enforces business rules (opening hours, cancellation window); **no idempotency keys** | D4, D5, D7 |
| A8 | Which channels? | Web chat only; English only; all five salons in one time zone | D2, D8 |
| A9 | Scope of a booking? | One service per appointment, for the signed-in customer only (no booking for others) | D2, tool set |
| A10 | Rollout? | Go live at one pilot salon on day 10; enable the other four after five trading days without a write incident (phase 2 G08) | Cut line |
| A11 | Retention and region? | Chat sessions kept 30 days; one GCP region chosen with the salon chain for Cloud Run, Cloud SQL and Vertex AI | D7, D9, open decision O3 |
| A12 | Existing database to reuse for sessions? | None suitable; a new small Cloud SQL for PostgreSQL instance | D7 |

## Purpose and constraints

**Journey.** Maria is signed in on the salon's booking site at 21:40 and wants
to move Thursday's 17:00 colour appointment at the Riverside salon to Saturday
morning with the same stylist. Today she clicks through four screens or waits
for the salon to open and phone. With the assistant she types "can I move my
Thursday colour to Saturday morning with Jo?", sees two offered slots, picks
one, presses **Confirm** on a card that shows the exact old and new times, and
gets the booking system's usual confirmation SMS. The outcome to improve is
self-service changes completed without a phone call; baseline unknown (see
Verification).

**What the model contributes:** understanding the request, choosing which
read tool to call, presenting options, and proposing an exact booking, move or
cancellation. **What code controls:** who the customer is, which appointments
they own, the business rules (the booking API), executing writes after the
customer's confirmation, and the reported status.

Fixed constraints: the existing booking API and website; GCP; ten working
days; three people. Non-goals for phase 1: payments, booking for others,
multi-service bookings, SMS/WhatsApp/voice channels, other languages,
staff-facing features, personalised memory.

## Delivery constraints, depth and deferred controls

| Scope-gate answer | Value |
| --- | --- |
| First useful version due, and after | 2026-10-28 (10 working days); continued (A1) |
| People and hours | 3 developers × ~5 focused h/day, new to ADK, know GCP (A2) |
| Money | ≤ US$300/month, illustrative (A3) |
| Users or judge | Signed-in salon customers; salon chain owner judges (A4) |
| Data and effects | Real personal data; reversible customer-visible writes; no money (A5) |
| Delivery profile | **MVP / pilot**: first external users completing a real journey with real effects |

Depth per concern:

| Concern | Depth now | Trigger that raises it |
| --- | --- | --- |
| Core judgment, measured | Build: 30-case evaluation set run before launch (G05) | Eval in CI in phase 2 (G09) |
| Identity and per-customer scope | Build (D3) | — |
| Secrets | Build: service account, Secret Manager for the booking API key | Rotation when staff turnover or a leak |
| External writes | Build: customer confirmation in code, one write per confirmation, reconcile by read (D4, D5) | API idempotency keys (G11) when a duplicate is observed or volume grows |
| Sensitive data | Minimal-plus: fields minimised in tool results, no content in logs or traces, 30-day session retention (D9) | Model Armor/SDP screening when free-text notes reach the model or after an incident |
| Prompt injection and agency | Build: one agent, own-data only, writes only through confirm endpoint (D4); adversarial cases in G05 | Threat model refresh when a new tool reads third-party text |
| Budgets and loop limits | Floor: `max_llm_calls`, per-customer daily turn cap, per-IP rate limit, Vertex quota and budget alert (D6) | Per-customer token budget (G10) |
| Memory | Conversation sessions only (D7) | Memory Bank when customers ask for "my usual" |
| Frontend | Build: widget in existing site, completed JSON (D8) | Streaming when measured reply time hurts completion |
| Hosting | Cloud Run, staging + production, previous revision kept for rollback (D7) | Canary when > ~200 conversations/day |
| Observability | Build: traces with token counts, structured logs without content | SLOs and alerts (G12) after two weeks of baseline |
| Release engineering | Minimal: pinned ADK, model and prompt version recorded per release; offline tests in CI | Eval gate in CI (G09) |
| Performance tuning | Defer | Measured p95 reply > 8 s or cost per completed change > budget |

**Floor kept:** no secrets in code, prompts or logs; spend stop (D6); no
booking change without the customer confirming exact details in the UI (D4);
real personal data limited to what the journey needs and kept out of logs
(D9); model pinned (D2).

**Who may use it, on what data:** signed-in customers of the pilot salon in
phase 1, then all five. Graduation conditions before all five salons: five
trading days at the pilot with zero duplicate or wrong-customer writes and the
evaluation pass rate held (G08). Before another channel or anonymous users:
a separate identity design.

## Guarantees and acceptance

| ID | Invariant | Enforcing component and evidence | Failure outcome | Planned verification |
| --- | --- | --- | --- | --- |
| I1 | A customer reads and changes only their own appointments | Gateway verifies the site's session token, derives `customer_id`, writes it to session state; tools read it from state, never from model arguments; the confirm executor re-reads the appointment and compares owner | Refusal message, no API write | Scripted model asks for another customer's appointment ID → tool returns `not_found`; fake API records no write (G02, G03) |
| I2 | No booking change happens without the customer confirming the exact details | Model has only `propose_*` tools; the write runs only from the gateway's confirm endpoint, bound to a stored proposal and its payload hash | Proposal stays pending, expires after 15 min | Scripted model calls every tool; fake API sees zero writes until confirm (G03) |
| I3 | One confirmation causes at most one write | Atomic claim `pending → executing` on the proposal row; no automatic retry of writes; uncertain outcomes reconciled by reading the customer's appointments | Double click shows the same receipt | Two concurrent confirms → one API call; timeout → `uncertain`, reconcile finds/doesn't find the appointment (G03) |
| I4 | "Booked/moved/cancelled" is shown only when the booking API confirmed it | UI renders status from the proposal record's receipt, not model text | "We couldn't confirm this; check My appointments or call the salon" | API error and timeout cases render the right status (G03, G04) |
| I5 | Business rules come from the booking API | Tools pass requests through; API rejection becomes an actionable tool error | Model explains the rule from the error | Late-cancellation case in eval set (G05) |
| I6 | Spend is bounded | D6 limits | Polite "try again later / call the salon" | Unit test for each cap; budget alert configured (G06) |
| I7 | No customer content in logs or traces | Content capture off; log fields are IDs and outcomes | — | Log/trace inspection on staging (G06) |

## Architecture and decisions

```text
Browser (booking site, signed in)
   │  session token + message           ┌───────────────── Cloud Run: assistant ────────────────┐
   └──────────────────────────────────▶ │ Gateway (FastAPI)                                      │
                                        │  verify token → customer_id (I1)                       │
                                        │  rate limit / turn cap (D6)                            │
                                        │  POST /chat ──▶ ADK Runner ──▶ LlmAgent ──▶ Vertex AI  │
                                        │                     │ tools (read, propose)             │
                                        │  POST /proposals/{id}/confirm ──▶ Write executor (D4)  │
                                        └────────┬──────────────────────┬─────────────────────────┘
                                                 │                      │ server key (Secret Manager)
                                     Cloud SQL Postgres          Booking API (ours, authoritative)
                                     sessions + proposals         → sends its usual SMS/email
```

| ID | Requirement | Design choice | Reason | Tradeoff / alternative | Verification | Status |
| --- | --- | --- | --- | --- | --- | --- |
| D1 | Interpret free-text requests over a small capability set | One `LlmAgent` with six function tools: `search_availability`, `list_my_appointments`, `get_salon_info`, `propose_booking`, `propose_move`, `propose_cancellation`; salon list and today's date injected via state templating | One judgment, small tool count; function tools give us the exact declarations | Sub-agents per intent rejected: no distinct authority or context | Declaration dump ≤ 6 tools; eval tool-choice accuracy (G05) | proposed |
| D2 | Behaviour stable across days | Pin `gemini-3.8-flash` on Vertex AI (stable, released 2026-09-02, no shutdown announced per `model-lifecycle-2026-10-01.json`, checked_on 2026-10-08); fallback candidate `gemini-3.5-flash` (Vertex retirement 2027-05-19 or later). ADK working assumption `google-adk==2.8.0` | Newest stable flash, cheap, tool use | Avoid 3.6/3.7 flash: Vertex retirements 2026-11-19 and 2027-01-28 fall inside the plan horizon | Regional availability on Vertex verified in G06; pin confirmed in G01 | provisional (O2) |
| D3 | Only the signed-in customer's data (I1) | Gateway verifies the booking site's token (A6) and owns session creation; `customer_id` lives in session state written by code; sessions keyed by customer and checked on every request | Identity from a verified source, outside the model | Asking customers to verify by phone OTP in chat rejected: duplicates the site's login | Cross-customer and forged-session tests (G02) | provisional (A6) |
| D4 | Customer confirms exact details; one write each (I2–I4) | Two-step writes: `propose_*` tools validate against the API (slot exists, appointment owned) and store a proposal row `{id, customer_id, kind, canonical payload, hash, status, expires_at}`; the UI renders a card; the confirm endpoint (plain code) claims the row atomically, re-checks owner and expiry, calls the API once, stores the receipt, and records the outcome in session state for the next turn | The model cannot reach the write; confirmation binds to stored details; double clicks are harmless | More code than ADK's native tool confirmation (rejected: its known limitations would need checking against the pin, and it keeps execution inside the model's tool call) | I2, I3 tests (G03) | proposed |
| D5 | Writes may time out with an unknown result | No automatic retry for writes; on timeout/5xx mark `uncertain`, then reconcile by reading the customer's appointments (book: appointment at that slot exists; move: new time present; cancel: status cancelled) before offering a fresh proposal | Safe without changing the booking API (A7) | A narrow race remains if the API commits after the read; closed by API idempotency keys in G11 | Fake API "commit then timeout" case (G03) | proposed |
| D6 | Spend and abuse bounded on a public endpoint | `RunConfig.max_llm_calls=10` per turn; 40 turns per customer per day and 10 requests/min per IP in the gateway (in-memory per instance in phase 1, accepted); Vertex AI per-minute quota lowered; Cloud Billing budget alert at 50/90/100 % of A3 (alerts only, not a cap) | Floor for a public service | In-memory counters reset on restart and are per-instance; max instances set to 2 to bound it; durable budget in G10 | Unit tests per cap (G06) | proposed |
| D7 | Conversations survive restarts; proposals are durable | Cloud Run (min 0, max 2 instances), `DatabaseSessionService` and a `proposals` table on one Cloud SQL Postgres; booking API remains the only business authority | Small, managed, the team knows GCP | Agent Runtime rejected for now: custom gateway and confirm endpoint are simpler on Cloud Run | Restart mid-conversation keeps history (G06) | provisional (A12) |
| D8 | Customers use it inside the existing site | Custom JSON API: `POST /chat` returns completed text plus any proposal card; `POST /proposals/{id}/confirm` and `/decline`; `GET /session` for reload. No streaming in phase 1 | Fewer failure modes; cards need complete data anyway | Slower perceived reply than streaming | Widget end-to-end on staging (G04, G07) | proposed |
| D9 | Personal data minimised | Tool results return only fields the model needs (no phone, email or payment fields); ADK/OTel content capture off; logs carry IDs and outcomes; sessions deleted after 30 days (job in G13) | Floor for real personal data | Debugging needs session lookups instead of log text | Log inspection (G06) | proposed |

### Model-facing contracts

| Surface | Contract | Implementing skill and verification |
| --- | --- | --- |
| Instructions | One instruction: role, salon list and today's date from state, always offer concrete slots, always use a `propose_*` tool for changes, never claim success (status comes from the card), hand off to the salon phone number when stuck. Identity, rules and limits stay in code | `adk-agent-instructions`; rendered-request test |
| Tool interfaces | Six function tools (D1); primitive parameters; results capped at 10 slots / 10 appointments; `{status, ...}` with actionable errors (`slot_taken`, `outside_cancellation_window`, `not_found`); tiers: read (3), propose (3); no write tool | `adk-tool-interface-design`; declaration dump |
| Output contract and model | Free text; no `output_schema` (structured data travels in proposal records). Model per D2, default sampling, thinking off or low | `adk-model-and-output-contracts`; pin check |

## Data and authority

| Data / operation | Owner and scope | Writers / readers | Source and freshness | Lifetime / erasure |
| --- | --- | --- | --- | --- |
| Appointments, availability, rules | Booking API, per customer | API writes; tools read | Authoritative, read live each turn | Booking system's own policy |
| Conversation session | Assistant, per verified customer | Runner writes; gateway reads after owner check | Cloud SQL | 30 days, then deleted (G13) |
| Proposal record | Assistant, per customer | `propose_*` tools create; confirm endpoint claims and completes | Cloud SQL | 30 days with session |
| Booking API key | Platform | Secret Manager → service account | — | Rotated manually |

Three identities: the customer (site token, verified in gateway), the
assistant workload (Cloud Run service account: Vertex AI user, Cloud SQL
client, the one secret), and the booking API server key (all-customer scope,
so I1 is enforced by our code, not the key).

### Security posture

| Agent | Private data | Untrusted content | Write or egress | Resolution |
| --- | --- | --- | --- | --- |
| Booking assistant | The signed-in customer's own appointments | The customer's own messages; staff-authored salon/service text | Proposals only; writes run in code after the customer confirms | No third-party content and no egress path; scope fixed by I1 and D4. Adversarial cases in G05 assert no write without confirm and no other-customer reads |

No code executor.

## Budgets and capacity

Assumed load: five salons, at most a few hundred conversations a day, about
4 turns each, about 2–3 model calls per turn (tool call plus answer), each
under ~6k input tokens. Cost per conversation is a symbolic estimate pending
G06 measurement: `turns × calls × (input tokens × input price + output tokens
× output price)`; prices to be read from the Vertex AI pricing page on the
day G06 runs. A3's allowance is the budget alert threshold, not a cap. Cloud
SQL smallest shared-core instance is the main fixed cost.

## Failure and recovery

| Failure window | User-visible outcome | Retained state / possible effects | Safe next action and recovery owner |
| --- | --- | --- | --- |
| Customer asks about another customer's booking | "I can only see your appointments" | Nothing | None |
| Model or Vertex unavailable / call cap reached | "I can't help right now — call the salon on …" | Session up to last event | Customer retries later |
| Slot taken between proposal and confirm | Card shows "That time was just taken" and the agent offers others | Proposal `failed`, no effect | New proposal |
| Booking API times out or 5xx on confirm | Card: "Checking…" then confirmed or "not made" | Proposal `uncertain`; effect possible | Executor reconciles by read (D5); unresolved after 3 reads → staff log entry, salon calls customer (owner: on-call dev) |
| Double click / two tabs confirm | One receipt shown in both | One write (I3) | None |
| Proposal older than 15 min | "This offer expired" | No effect | New proposal |
| Instance restart mid-conversation | History intact | Sessions and proposals in Cloud SQL | Continue |
| Customer's appointment changed by staff after proposal | Confirm re-reads; mismatch → "This appointment changed; let's look again" | No effect | New proposal |
| Model retirement announced | None | — | Planned re-baseline on the eval set (later list) |
| Bad release | Errors or quality drop | — | Roll Cloud Run traffic back to previous revision (G07 rehearses) |

## Verification and implementation handoff

Offline: fake booking API with scripted model for I1–I5 (G01–G03). Local
integration: gateway + widget + Postgres with a restart (G04, G06). Bounded
live: staging booking API and Vertex, the evaluation set (G05, G07). Release:
rollback rehearsal and pilot sign-off (G07).

Product outcome (hypothesis): share of booking changes at the pilot salon
completed through the assistant, with no rise in front-desk calls about
wrong bookings. Baseline: the salon's current weekly count of phone changes,
to be requested in W1.

Release bundle recorded per deploy (G06): image digest, ADK version, model ID,
prompt version, tool-schema hash, secret version. Rollback unit: the Cloud
Run revision; previous revision kept.

The implementation route for each decision, goals and owners are in the
[plan](../plans/salon-booking-assistant.md).

## Open decisions

| ID | Question or assumption | Why it changes the design | Owner / evidence needed | What it blocks |
| --- | --- | --- | --- | --- |
| O1 | Can the backend verify the booking site's customer token (A6)? | If not, D3 needs a different login (OTP or a signed link) | Team lead, from the website auth code | G02 |
| O2 | ADK pin (2.8.0 checked by the skills; observability skill recommends ≥ 2.10 for new production) and `gemini-3.8-flash` regional availability | Changes API names and the model pin | Dev A in G01; Dev B in G06 | G01, G06 |
| O3 | GCP region and data-processing terms acceptable to the salon chain | Residency of inference, sessions and logs | Salon chain owner (W1) | G06, G07 |
| O4 | Does the booking API reschedule natively, and are there cancellation fees? (A5, A7) | Without reschedule, a move is book-then-cancel with a partial-failure path; fees would be money and need stricter confirmation | Team, from API code | G03 |
| O5 | Pilot at one salon first (A10)? | Changes launch scope and G08 | Salon chain owner | G07 |
