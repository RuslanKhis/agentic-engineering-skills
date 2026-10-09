# System design: salon booking assistant (MVP)

Status: **draft**. Written in one pass while the user was unavailable. Every
answer in the table below is assumed, and the decisions that depend on one are
marked *provisional*. Nothing here has been confirmed by the user yet.

Plan: [docs/plans/salon-booking-assistant.md](../plans/salon-booking-assistant.md).
Tickets: [docs/tickets/salon-booking-assistant/](../tickets/salon-booking-assistant/).

## Assumed answers

| # | Question I would have asked | Assumed answer | Decisions that depend on it |
| --- | --- | --- | --- |
| A1 | When does the two weeks start, and what happens afterwards? | Start Mon 2026-10-12, launch Fri 2026-10-23, then keep improving (from the request). Phase 1 code is **kept**. | Plan phases, cut line |
| A2 | How many hours a day can each of the three of you give this, and how well do you know ADK and GCP? | About 7 h/day each, all ten working days. Strong in Python and in your own booking API. New to ADK, some GCP. | Capacity, estimates |
| A3 | How much can you spend on models and cloud? | Up to about US$300 a month during the MVP. | Model tier, D8 |
| A4 | Who uses it? | Salon customers, through a chat widget on the chain's existing website. Staff do not use it in phase 1. | D4, D7, the profile |
| A5 | What data does it touch and what can it change? | Real customer personal data (name, phone, email, appointment history). Real bookings that staff and customers see. **No payments or deposits.** | Floor, D2, D3, D8 |
| A6 | How do customers prove who they are today? | The website already has a customer login, and the backend can verify its session token (by JWT signature or by an introspection call to the booking API). | D4, G03 (provisional) |
| A7 | What does the booking API support? | REST with a staging environment and a service credential. Availability search, create, cancel and list per customer. **Unknown:** whether it has a reschedule endpoint, accepts idempotency keys or has a lookup that can reconcile a lost reply. G00 answers this. | D3, G02 (provisional) |
| A8 | Is there a GCP project, and can it reach the booking API? | Yes to both. The booking API runs outside this design and stays unchanged. | D6, G07 |
| A9 | Which business rules apply, and who enforces them (opening hours, stylist skills, cancellation window)? | The booking API enforces them. The agent shows the API's refusal and never re-implements rules. | D2, failure table |
| A10 | Languages and time zones? | English only. All five salons share one time zone. | Instruction, tool schemas |
| A11 | What happens when a customer needs a person? | Phase 1 shows the salon's phone number. A live staff handoff comes later. | Scope |
| A12 | How long may chat transcripts be kept? | 30 days, then deleted. | D6, phase 2 erasure goal |
| A13 | Who responds when something breaks? | The three developers, in business hours. Salon front desks reconcile bookings flagged as uncertain. | Failure table, runbook |

## Purpose and constraints

**Journey.** Maya sees a free slot on Saturday and wants to move her Thursday
4 pm colour with Sam at the Northside salon to that slot. She has to phone
during opening hours, wait while the front desk searches, and hope the slot is
still free. *Intended outcome:* at 11 pm she types "can I move my Thursday
colour to Saturday morning?" The assistant lists her Thursday booking and
offers Saturday slots with Sam or another colourist. It then shows one
confirmation card: "Move: Colour, Sam, Northside, Thu 4:00 pm → Sat 10:30 am".
She taps **Confirm**. The booking API records the move and the card shows the
booking reference. *Fixed constraints:* the existing booking API is the only
source of truth, the deadline is two weeks, and the team is three developers.

**What the model does and what code does.** The model interprets the request
("Saturday morning", "my colour", "with Sam if possible"), chooses read tools
and writes the reply. Code does everything else: it identifies the customer,
limits reads to that customer, checks availability, builds the confirmation
card from a stored proposal, and runs the write when the customer presses
Confirm. The model never runs a write.

**Non-goals for phase 1:** payments, SMS or WhatsApp, staff-facing tools,
languages other than English, remembering preferences between conversations,
marketing messages.

## Delivery constraints, depth and deferred controls

| Scope-gate answer | Value |
| --- | --- |
| First useful version, and afterwards | 2026-10-23, then continued (A1) |
| People and hours | 3 developers × 10 days × ~7 h, new to ADK (A2) |
| Money | ≈ US$300/month for models and cloud (A3) |
| Users, and what they see | External salon customers, in a web chat (A4) |
| Data and effects | Real personal data; real, reversible booking writes; no money (A5) |
| **Profile** | **MVP:** real external users and real writes. The work has to be done safely, and the team has to be able to see failures and cost. |

| Concern | Depth now | Trigger that raises it |
| --- | --- | --- |
| Core judgment, measured | Build: 20 to 25 case eval set run locally before launch (G05) | Eval runs in CI from phase 2 (G08) |
| Identity and per-customer scope | Build (G03) | — |
| Secrets | Build: Secret Manager and a dedicated service account (G07) | Rotation once the API supports it |
| External writes | Build: confirmation in code, idempotent operation record, reconciliation (G02) | Payments or deposits added |
| Sensitive data | Minimal: no message content in logs, 30-day session retention, scoped reads | Phase 2 retention job and review (G10) |
| Prompt injection and agency | Minimal: the model holds no write tool; reads are scoped in code | Staff tools or third-party content (G12) |
| Budgets | Build: per-turn call cap, per-customer daily cap, per-IP rate limit, billing alert (G06) | Abuse seen, or traffic above 10× the assumption |
| Memory | Sessions only, no long-term memory | Customers ask to be remembered |
| Frontend | Build: minimal widget, JSON without streaming (G04) | Measured latency complaints |
| Hosting | One Cloud Run service; the previous revision is the rollback (G07) | — |
| Observability | Minimal now: structured logs, operation outcomes, token count per turn. **Below the MVP default:** traces wait for phase 2 (G09). | First incident that the logs could not explain, or week 3 |
| Release | Minimal: pinned model and ADK, unit tests in CI | Eval gate in CI (G08) before the first prompt change after launch |
| Performance and cost tuning | Defer | Measured p95 above 8 s, or cost above budget |

**Floor kept.** No secrets in code, prompts or logs. Spend stop:
`max_llm_calls`, per-customer caps and a model quota. No booking changes until
the customer presses Confirm on a card rendered from the stored proposal. Real
data is limited to the signed-in customer's own records. The model ID is pinned.

**Graduation conditions** before advertising beyond the salons' own websites or
adding new channels: G08 eval gate in CI, G09 traces and SLIs, G10 retention and
erasure, G12 adversarial suite.

**Capacity and cut line.** 3 × 10 days × 7 h × 0.6 focus ≈ 126 focused hours.
Keeping 30 h (24 %) in reserve leaves 96 h. Phase 1 (G00 to G07) is estimated
at **65 to 94 h**, so it fits even at the high end, with little to spare. If
the work runs high, two things leave phase 1 first: the per-IP limiter in G06
moves to Cloud Armor in phase 2, and G05 shrinks to 12 cases. The floor stays
either way. Phase 2 and the later list are in the plan.

## Guarantees and acceptance

| Invariant | Enforced by, with authoritative evidence | Failure outcome | Planned verification |
| --- | --- | --- | --- |
| I1 A customer reads and changes only their own appointments | Gateway puts the verified `customer_id` in trusted session state. Tools read it from state, never from model arguments, and the API adapter re-checks ownership before any write. | "I can't find that booking" with nothing leaked | Offline: the scripted model passes another customer's appointment ID and gets a denial with no API write (G03) |
| I2 No booking change without an explicit Confirm on the exact details | The proposal record stores the canonical payload. `POST /operations/{id}/confirm` is reachable only from the UI button, and the model has no tool that can call it. | Proposal expires after 10 min, and nothing is written | Offline: Runner test asserts zero write calls across a whole conversation without a confirm (G02) |
| I3 One Confirm leads to at most one booking change | Operation ledger: `operation_id` unique, state machine `proposed→confirmed→dispatched→succeeded/failed/uncertain`. Before any retry, a reconciliation lookup checks for a matching booking. | A double click or retry returns the same result | Offline: a double confirm and a timeout-then-retry against the fake API each produce exactly one create (G02) |
| I4 The confirmation card and the final status reflect the booking API's answer, not the model's text | Card and status are rendered from the ledger record and the API reply | "We're checking this booking; the salon will confirm" | Offline: the fake API returns 409 or 500 and the card shows the true state (G02, G04) |
| I5 Spend is bounded | `RunConfig.max_llm_calls=8` per turn, 40 turns per customer per day, 30 requests per IP per minute, Vertex quota and budget alert | Polite limit message, nothing written | Offline: the cap is reached with a scripted looping model (G06) |

## Architecture and decisions

```text
Browser widget ──HTTPS + site session──▶ Cloud Run: gateway (FastAPI) ──▶ ADK Runner ──▶ Vertex AI gemini-3.8-flash
   │  confirm button                        │ verify customer (A6)          │ LlmAgent "booking_assistant"
   └────────POST /operations/{id}/confirm──▶│ budgets, rate limit           │ read tools + propose tools
                                            │ operation executor ──────────▶ Booking API (authoritative)
                                            └─ Cloud SQL Postgres: ADK sessions + operation ledger
```

Trust boundaries: browser (untrusted) | gateway and executor (trusted code,
service account) | model (untrusted proposer) | booking API (authority).

| ID | Requirement | Design choice | Reason | Tradeoff / alternative | Verification |
| --- | --- | --- | --- | --- | --- |
| D1 | Understand free-text requests over a small capability set | **One `LlmAgent`** with about 6 function tools and no sub-agents | The journey is one conversation with one owner. Splitting it would add routing failures without separating any credentials. | A planner/booker split brings no security gain, because writes already sit outside the model | Tool-selection accuracy on the G05 set |
| D2 | Writes need the customer's consent (I2) | **The model proposes, the customer confirms in the UI, code executes.** `propose_booking/move/cancel` validate the request against live availability and store a proposal. The UI renders the card from that record, and the button calls the executor. | Consent is bound to stored details in code the model cannot reach. This avoids depending on ADK's tool-confirmation flow and [its documented limitations](https://adk.dev/tools-custom/confirmation/#known-limitations). | Adds a UI element and an endpoint. ADK's native confirmation would be less code but a weaker binding. | I2 test |
| D3 | A lost reply must not double-book (I3) | **Operation ledger** in Postgres plus the API's idempotency key if G00 finds one. Otherwise, look up the customer's bookings for the same salon, service and start time before re-sending. Move uses the API's reschedule endpoint if it has one, else create-new-then-cancel-old as two ledger steps. *Provisional on A7.* | Retries and double clicks refer to one business operation | The ledger adds a table and a state machine. Create-then-cancel can leave two bookings, so a partial result is flagged to the front desk. | I3 tests, and the partial-move row in the failure table |
| D4 | Customer scope (I1) | Gateway verifies the website session (A6) and writes `customer_id` to session state under a key the model cannot set. Tools do not take customer arguments. *Provisional on A6.* | Identity comes from verified code. An appointment ID the customer types is a locator, not a permission. | Customers without a login can't use it. Guest booking with an OTP is in the later list. | I1 test |
| D5 | The model must see a small, clear interface | **Hand-written function tools** wrapping one API client. No `OpenAPIToolset`. | Gives a small declaration surface, bounded results and actionable errors | More hand code than importing the spec | Declaration dump under 3 KB, and selection accuracy |
| D6 | Hosting, sessions and model on a small team | **Cloud Run** (one service, min instances 0 to 1) + **Cloud SQL Postgres** (`DatabaseSessionService` and ledger) + **Secret Manager** + **Vertex AI** in the business's region | Few moving parts, with rollback by revision. Vertex keeps personal data under the project's terms and region. | Agent Runtime would manage sessions for us, but we need our own gateway for D2 and D4 anyway | G07 readback: revision, env and session persistence across restart |
| D7 | Customers chat on the existing site | Custom JSON API, one completed reply per turn, no streaming. Widget embedded in the logged-in area. | The simplest contract that can carry the confirmation card | No token streaming, so a reply waits for the whole turn (assumed ≤ 8 s) | G04 browser check |
| D8 | Bounded spend on a public surface (I5) | Per-turn `max_llm_calls`, a per-customer daily turn counter in Postgres, a per-IP in-process limiter, a Vertex quota and a billing **alert** (alerts do not cap) | Covers loops, abusive customers and anonymous floods | An in-process limiter is per instance. Cloud Armor in phase 2. | G06 tests |
| D9 | The team can see failures and cost | Structured JSON logs: `session_id`, `invocation_id`, `operation_id`, tool name, outcome and token counts. **No message text.** | Cheapest form that explains an operation failure | Traces deferred (below the MVP default; see the depth table) | G07 log readback shows no customer text |
| D10 | Quality evidence before real customers | A fake booking API and a 20 to 25 case eval set, run locally before launch | Measures tool choice, proposal correctness and refusals | Not yet a CI gate | G05 recorded run |

Decision status: all **proposed** by the designer. None has been accepted by the
user yet.

### Model-facing contracts

| Surface | Contract | Skill and verification |
| --- | --- | --- |
| Instruction | Role and the book/move/cancel scope. Always propose rather than claim a booking is done. Ask when the salon, service or time is ambiguous. Show the salon phone number for anything out of scope. Today's date, the time zone and the salon list are injected from state by code. Kept as a versioned file. | `adk-agent-instructions`; rendered-request test |
| Tools (6) | Read: `list_services_and_salons`, `find_availability(salon_id, service_id, date_from, date_to, stylist_id?)` (at most 10 slots returned), `list_my_appointments()`. Propose: `propose_booking(slot_id)`, `propose_move(appointment_id, slot_id)`, `propose_cancel(appointment_id)`. Each returns `{status, ...}` with actionable errors. Tiers: read, plus propose (no effect). Writes live only in the executor. | `adk-tool-interface-design`; declaration dump |
| Model and output | `gemini-3.8-flash` (stable, released 2026-09-02, no shutdown announced, per `adk-model-and-output-contracts/assets/model-lifecycle-2026-10-01.json`, checked_on 2026-10-08). Avoid `gemini-3.6-flash` (Vertex retirement 2026-11-19) and 2.5 models (2026-10-20), because both dates fall inside the plan. Free-text replies, no `output_schema`, because the card comes from the ledger, not the model. Region availability not yet verified (G07). | `adk-model-and-output-contracts` |

ADK version: none installed. Working assumption: **google-adk 2.8.0**, the
reference that `adk-model-and-output-contracts/references/compatibility.md` was
read against. G01's acceptance includes confirming the interfaces against the
chosen pin.

## Data and authority

| Data / operation | Owner and scope | Writers / readers | Source and freshness | Lifetime / erasure |
| --- | --- | --- | --- | --- |
| Appointments, availability, customers | Booking API | Executor writes. Tools read for the verified customer. | Live on every call, never cached. A slot from a proposal is re-checked by the API at create time. | The booking API's policy |
| ADK session (chat events, state) | Per customer and conversation | Runner | Postgres | 30 days, then a deletion job (G10). Phase 1 deletes by hand on request. |
| Operation ledger | Per customer | Propose tools insert. Executor transitions. | Postgres, unique `operation_id` | 90 days for reconciliation |
| Booking API credential | Service | Secret Manager → executor and tools | — | Rotated per the API's policy |

### Security posture

| Agent | Private data | Untrusted content | Write or egress | Resolution |
| --- | --- | --- | --- | --- |
| booking_assistant | The signed-in customer's own appointments | The customer's messages, and free text in API fields (stylist bios, notes) | **None.** Propose tools store a record and have no effect. | Write leg removed from the model. The confirm endpoint checks the session owner. The worst case is a misleading reply about the customer's own data. |

## Budgets and capacity

Assumption (labelled; G00 replaces it with the salons' real numbers): 5 salons ×
30 chats a day = 150 chats a day. Each chat is about 4 turns × 2 to 3 model
calls ≈ 10 calls, with about 6k input and 300 output tokens per call. That is
about 1,500 calls a day and a peak below 2 concurrent turns. At current Flash
pricing this is a small fraction of A3, **but no price has been looked up in
this session**: G07 records the dated price and source. Cloud SQL's smallest
tier is likely the largest fixed cost. Budget alert at 50 %, 90 % and 100 % of
A3. A Vertex requests-per-minute quota is the hard stop.

## Failure and recovery

| Failure window | Customer sees | Retained state / possible effects | Next action and owner |
| --- | --- | --- | --- |
| Success (Maya's move) | Card shows "Moved, ref ABC123" | Ledger `succeeded` with API receipt | — |
| Slot taken between proposal and Confirm | "That slot was just taken". Fresh slots offered. | Ledger `failed:conflict`, no booking | Customer picks again |
| Create times out or the reply is lost | "We're confirming this with the salon". No success claimed. | Ledger `uncertain`. The booking may exist. | Executor reconciles by lookup (D3). If still unknown after 2 tries, the front desk queue resolves it. |
| Double click / page refresh on Confirm | Same card, same result | One operation | Ledger unique key |
| Move: new booking created, cancelling the old one fails (no reschedule endpoint) | "Your new time is booked. We couldn't release the old one; the salon will." | Both bookings exist | Front desk queue entry, raised as a log alert |
| Another customer's appointment ID in a message | "I can't find that booking" | Nothing | — (I1) |
| Model unavailable, or call cap hit | "I'm having trouble; call Northside on …" | Session kept, no proposal | Customer retries later |
| API refuses on a business rule (late cancel) | The API's reason in plain words | Ledger `failed:rule` | — |
| Model invents a time that isn't in the slots | The propose tool rejects an unknown `slot_id`, and the model must re-search | Nothing | — |
| Model retirement | — | — | Pinned ID; check the lifecycle file monthly (phase 2 G08) |
| Rollback | Previous revision serves. Sessions and ledger stay compatible. | Ledger migrations must be additive in phase 1 | Developer on duty |

## Verification and handoff

Offline: tool, ledger and executor tests against a fake booking API, with
scripted-model Runner tests for I1 to I5. Local integration: the staging
booking API and a Postgres restart. Bounded live: the G05 eval run on the
pinned model, under a spend limit. Hosted: the G07 readback and one test
booking on a test customer at one salon. All of these are **planned**, and none
has been run.

The product hypothesis, not yet measured, is that customers make bookings
outside opening hours and the front desk gets fewer calls. Measure the share of
bookings made through the chat outside opening hours, against a guardrail: the
number of "uncertain" or front-desk reconciliations per week.

Goals, estimates, owners and run prompts are in the
[plan](../plans/salon-booking-assistant.md).

## Open decisions

| Question | Why it matters | Owner / evidence | Blocks |
| --- | --- | --- | --- |
| Customer login verifiable server-side? (A6) | Without it, D4 needs OTP or guest booking | User + G00 | G03 |
| Reschedule endpoint, idempotency keys, lookup filter? (A7) | Shape of D3 and the move flow | G00 | G02 final form |
| Vertex region and `gemini-3.8-flash` availability there | Residency of personal data | G07 lookup | G07 |
| Payments or cancellation fees ever charged by chat? | Would add money-moving controls | User | Later list |
| Ship to all five salons at once, or one first? | Launch risk | User. Recommended: one salon for 2 days. | Launch day |
