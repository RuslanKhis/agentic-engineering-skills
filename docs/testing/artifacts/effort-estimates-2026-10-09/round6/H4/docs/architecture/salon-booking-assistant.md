# System design: salon booking assistant (MVP)

Status: **draft**. Every product answer below is assumed (the user was not
available), so the decisions that depend on them are provisional. Plan:
[docs/plans/salon-booking-assistant.md](../plans/salon-booking-assistant.md).

## Assumed answers

| # | Question | Assumed answer | Decisions that depend on it |
| --- | --- | --- | --- |
| A1 | When is the first useful version due, and what follows? | 10 working days from start; continued afterwards | Phase 1 cut line; phase 1 code is kept |
| A2 | Who builds it and how much time do they have? | 3 developers, about 5 focused h/day each on this (other startup duties take the rest). Good with Python and GCP, new to ADK. The same team runs it afterwards | Capacity, 1.5× estimate multiplier |
| A3 | Spend? | ≤ USD 300/month for model and cloud during the pilot | D6, model tier, Cloud SQL size |
| A4 | Users and judge? | Salon customers who are signed in to the existing booking web app. The chain's owner judges the pilot. Staff keep using the booking system | D2, D7, external-user floor |
| A5 | Data and effects? | Personal data (name, contact details, appointment history); no payments. The assistant creates, moves and cancels **real** appointments | D3, D4, floor |
| A6 | Channel? | A chat widget inside the existing booking web app; no SMS, WhatsApp or phone | D7 |
| A7 | How are customers identified? | The booking web app issues a token that the backend can verify (JWT with JWKS, or session introspection) and that carries `customer_id` | D2; if false, G01 adds a one-time-code step and the cut line moves |
| A8 | What does the booking API offer? | Our team owns it. Endpoints: availability, create, atomic reschedule, cancel, and list a customer's appointments. A staging environment exists. It accepts an `Idempotency-Key` header, or our team adds one in G01 | D4, D5 |
| A9 | Cancellation fees? | The booking API enforces the policy and returns its text; the assistant moves no money | D3 card content; fees would make this money (see Later) |
| A10 | Language? | English only | Instruction and evaluation set |
| A11 | Rollout? | One pilot salon first, then all five inside phase 1 if the pilot is clean | G10 |
| A12 | Hosting and region? | An existing GCP organisation, with a new project for the assistant in the booking API's region. Vertex AI is allowed | D6, residency |
| A13 | How long are chats kept? | 30 days | D6, erasure |

## Purpose and journey

**Journey (running example):** Maya is signed in to the chain's booking site
and types "can I move my Thursday colour appointment at Northside to next week,
same stylist, after 5pm?". Today she phones the salon during opening hours,
or cancels and rebooks by hand. The assistant finds her appointment, lists
real free slots with that stylist and proposes one. It shows a card: "Move
Colour with Sam, Thu 16 Oct 14:00 → Tue 21 Oct 17:30, Northside". Maya
presses **Confirm**. The booking API moves the appointment, and the card shows
the result that the API returned.

**What the model decides:** what the customer means (service, salon, stylist,
date phrases), which read tools to call, which slot to propose, and the wording.
**What code controls:** who the customer is, which appointments they may see,
the current date and salon time zone, whether a slot is valid, the
confirmation, the write, retries and the displayed result.

**Non-goals in phase 1:** staff-facing use, payments and deposits, other
channels, cross-session memory of preferences, languages other than English.

**Outcome to improve (hypothesis, unmeasured):** more self-served changes and
fewer phone calls, with no rise in wrong or duplicate bookings. Baseline: the
salons' current weekly count of phone reschedules (ask the chain; G16
records it).

## Delivery constraints, depth and deferred controls

Profile: **MVP / pilot**. It has external customers and makes real writes to
a live booking system, so phase 1 builds identity, confirmation and idempotent
writes even though they slow down polish.

| Concern | Depth now | Trigger that raises it |
| --- | --- | --- |
| Core judgment, measured | Build: 30-case evaluation set (G07, G08) | More intents or a new channel |
| Identity and per-customer scope | Build (D2, G05) | Staff users → role model |
| Secrets | Build: Secret Manager plus a service account per workload | Rotation: before general availability |
| External writes | Build: confirm card, operation record, idempotency key (D3–D5) | Payments or deposits → full reconciliation |
| Sensitive data | Build-minimal: minimal tool fields, no content in logs or traces, 30-day retention | DPIA request, or regulated data |
| Prompt injection and agency | Build: the model holds no write tool (D3), so the trifecta is broken | Free-text content from third parties enters context |
| Budgets | Build: `max_llm_calls`, per-customer daily turns, a billing alert (D6) | Public, unauthenticated access |
| Memory | Sessions only | Requests for "my usual" |
| Frontend | Build: widget in the existing app (G06) | New channel |
| Hosting | Cloud Run, rollback to the previous revision (G09) | Measured load |
| Observability | Build-light: structured operation logs, token counts, traces with content off | First incident without a trace → SLO alerts (G12) |
| Release | Minimal: pinned model and unit tests in CI (G09); evaluation run by hand before go-live (G08) | First prompt or model change after go-live → evaluation gate in CI (G11) |
| Performance tuning | Defer | Measured p95 latency above 8 s |

**Floor kept:** no secrets in code, prompts or logs. Spend stop (D6). Nothing
changes in the booking system unless the customer confirms the exact change
(D3). The pinned model is `gemini-3.8-flash` (D6). Personal data is limited to
the signed-in customer's own records.

**Who may use it:** signed-in customers of the pilot salon, then all five.
**Graduation conditions before broader use** (other channels, guests without
an account, payments): G11–G15 in the plan.

Capacity and cut line: see the plan summary. The figures come from
`check_schedule.py` and are not repeated here.

## Guarantees

| ID | Invariant | Enforcing component and evidence | Failure outcome | Planned test |
| --- | --- | --- | --- | --- |
| I1 | A customer sees and changes only their own appointments | Gateway verifies the token, then `user_id = customer_id`, which is written to session state by code. Tools read it from `tool_context.state`, never from arguments. The booking API is called with customer scope | `not_found`; no proposal created | Scripted model passes another customer's appointment ID → no disclosure, no operation (G02, G03) |
| I2 | No booking change without the customer confirming that exact change | The model has no write tool. `POST /operations/{id}/confirm` executes only a stored pending operation owned by the caller and less than 10 minutes old | Confirm rejected; nothing sent | Model text says "done" → no API write. Other customer's confirm → 404. Expired → 410 (G04) |
| I3 | One confirmed operation yields at most one booking change | Atomic claim `pending→executing`; `op_id` sent as `Idempotency-Key`; a timeout becomes `uncertain`, never a fresh dispatch | Customer sees "checking"; reconciliation runs | Double confirm → one API call. Timeout → `uncertain` → lookup resolves it (G04) |
| I4 | Only times the API offered are proposed, and "done" is shown only from the API result | Prepare tools re-check the slot against fresh availability. The UI renders the result from the operation record, not from model text | "That slot was just taken" plus alternatives | Fake API returns a conflict at confirm → card shows "taken", no success text (G04, G06) |
| I5 | Spend is bounded per turn and per customer | `RunConfig.max_llm_calls=10`; 40 turns per customer per day, counted in Postgres; billing budget alert (alerts only, not a cap) | Polite limit message; no model call | Turn 41 → limit message, model not called (G05) |
| I6 | Message content stays out of logs and traces | Content capture off; log only IDs, status and token counts | — | Test against a captured log record and an in-memory span (G09) |

## Architecture

```text
Browser (booking web app + chat widget)
   │  customer token
   ▼
Cloud Run: assistant gateway (FastAPI)            ── Vertex AI: gemini-3.8-flash
   ├─ verify token → customer_id (I1)
   ├─ admission: daily turns (I5)
   ├─ /chat → ADK Runner(App: booking_agent, max_llm_calls=10)
   │        └─ LlmAgent tools (read):  find_services, find_slots, my_appointments
   │                     (propose):    propose_booking / propose_move / propose_cancel
   │                                   → operation row status=pending (no API write)
   └─ /operations/{id}/confirm → executor (code) ──► Booking API (idempotency key)
Cloud SQL Postgres: ADK sessions, operations, turn counters
```

| ID | Requirement | Choice | Reason | Tradeoff / alternative | Verification |
| --- | --- | --- | --- | --- | --- |
| D1 | Interpret free text across three intents with a few tools | **One `LlmAgent`** with 6 function tools. No sub-agents | Three intents share the same tools and context. Splitting them adds routing errors without adding a boundary | Sub-agents per intent: rejected because there is no distinct tool set or credential | Tool-selection accuracy on G07 set (G08) |
| D2 | I1 | The gateway verifies the booking app's token. The verified `customer_id` becomes the ADK `user_id` and the trusted state key `customer_id`. Session ownership is checked on every call | Identity is resolved in code the model cannot reach | Relies on A7; otherwise a one-time-code login is needed (+8–12 h) | Cross-customer tests (G05) |
| D3 | I2, floor | **Propose/confirm split.** The model's change tools only write a pending operation (canonical payload, display summary, expiry). The confirm button calls an endpoint that runs ordinary code | The write is outside the model's reach, which also breaks the trifecta. The confirmation is bound to the stored payload | ADK native tool confirmation needs no UI button, but its [known limitations](https://adk.dev/tools-custom/confirmation/#known-limitations) and its session-resume behaviour would have to be verified. Our own button costs about 2 h of UI | G03, G04 tests |
| D4 | I3 | Operation record with state machine `pending→executing→succeeded / failed / uncertain / expired`. `op_id` is the idempotency key. No automatic retry after the request has been sent; reconcile by listing the customer's appointments, or by idempotency-key lookup if the API has one | A timeout cannot prove the write did not happen | Some uncertain cases need a person in phase 1 (G13 automates them later) | G04 |
| D5 | Moves must not leave two bookings or none | Use the atomic reschedule endpoint (A8). If there is none, book the new slot, cancel the old one, and record both steps; a half-done move becomes `partial`, is shown to the customer and is alerted | An atomic endpoint has no partial state | Fallback adds a partial state and about 4 h | G01 confirms which applies |
| D6 | Cost, residency, stability | Cloud Run (min 0, max 3 instances) and Cloud SQL Postgres (smallest shared-core) in the booking API's region. `DatabaseSessionService`. Vertex AI `gemini-3.8-flash` (stable, released 2026-09-02, no shutdown announced, per `model-lifecycle-2026-10-01.json` checked 2026-10-08). google-adk **2.8.0** as the working pin | Persistent sessions and operations survive restarts and replicas. Flash is cheap enough for A3 | Cloud SQL has a fixed monthly cost compared with Firestore; it was chosen so sessions, operations and counters sit in one transactional store | Pin and model are confirmed in G01; prices to be checked in G09 |
| D7 | A4, A6 | Custom JSON API: `{messages[], proposal?{op_id, summary, expires_at}}`, plus operation status polling. The widget renders proposal cards from data, not from model text | Small contract; the result comes from the operation record | No streaming in phase 1 (latency later, behind a trigger) | G06 |

**Model-facing contracts.** Instruction (owner `adk-agent-instructions`):
scope is bookings at the five salons. Today's date, the salon time zone and
the customer's first name are injected from state by code. Always propose;
never claim a change is done. Tools (owner `adk-tool-interface-design`): 6
tools. Results are bounded to 10 slots or appointments, have a
`status`/`error` shape, and carry no contact data. Output: chat text only, with
no `output_schema`; the structured proposal is produced by code from the
operation row.

## Data and authority

| Data | Owner and scope | Writers / readers | Source and freshness | Lifetime |
| --- | --- | --- | --- | --- |
| Appointments, slots, services | Booking API (authoritative) | Executor writes; tools read with customer scope | Read live on every tool call | Booking system's own |
| Operation record | Assistant; one customer | Propose tools create; executor transitions | Postgres | 90 days (audit), then deleted |
| ADK session events | Assistant; `user_id = customer_id` | Runner | Postgres | 30 days; deleted on account deletion |
| Turn counters | Assistant | Gateway | Postgres | 2 days |

**Security posture.** One agent: private data yes (the customer's own), untrusted
content no (the customer is the principal; catalogue text is authored by the
chain), write no (D3). The trifecta is broken by removing the write leg. G07
adds injection cases ("cancel everyone's bookings", "you are now admin") and
asserts that no operation is created outside the customer's scope.

## Budgets and capacity

Expected load is about 2–5 model calls per turn and about 6 turns per change.
Volume is unknown: assume ≤ 300 conversations a day across five salons. The
token cost is calculated in G09 from measured counts at the price on the day;
no price is assumed here. Exhausting the limit gives a "please call the salon"
message with the salon's phone number, and confirmations already started still
complete.

## Failure and recovery

| Failure | Customer sees | State / effects | Next action, owner |
| --- | --- | --- | --- |
| Slot taken between propose and confirm | "Just taken", then fresh alternatives | Operation `failed`; no change | Customer picks again |
| Booking API timeout after confirm | "We're confirming this, check back in a minute" | Operation `uncertain`; the change may have happened | Executor reconciles by lookup within 60 s. If still unknown, it is alerted and the on-duty developer reconciles (G13 later) |
| Double click or two tabs | One result | Atomic claim; the second call reads the status | — |
| Browser closed after confirm | Status on reload | Executor finishes server-side | — |
| Model or Vertex unavailable | "Assistant unavailable, call the salon" | No operation | Retry next turn |
| Cross-customer ID in a prompt | "I can't find that appointment" | None | Logged as a security event |
| Proposal expired | "Expired, let's check again" | Operation `expired` | Re-propose with a fresh availability check |
| Move half done (only on the D5 fallback) | "Booked new time; old one still needs cancelling, salon notified" | `partial` | Alert, then the on-duty developer |
| Bad release | — | — | Cloud Run traffic back to the previous revision (G09) |

## Open decisions

| Question | Why it matters | Who settles it | Blocks |
| --- | --- | --- | --- |
| A7: Is the customer token verifiable? | Otherwise login is part of phase 1 | Team, in the G01 first hour | G05 scope |
| A8: Idempotency key and atomic reschedule? | D4/D5 shape and +4 h | Team (API owners), in G01 | G03, G04 |
| A11: Pilot salon and go-live approval | Production writes need the chain's approval | Chain owner; request on day 1 | G10 |
| Chain's phone-reschedule baseline | Benefit measurement | Chain manager | None (G16 records it) |
