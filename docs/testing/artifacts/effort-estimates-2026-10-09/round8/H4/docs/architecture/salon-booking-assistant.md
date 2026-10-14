# System design: salon booking assistant (MVP)

Status: **draft**. The user was not available, so every scope answer below is
assumed and the decisions that depend on it are provisional. Decisions and
their rationale live here. Estimates, owners, capacity and the cut line live in
the [plan](../plans/salon-booking-assistant.md). Each phase 1 goal's scope and
acceptance live in its [ticket](../tickets/salon-booking-assistant/).

## Assumed answers

| # | Question | Assumed answer | Decisions that depend on it |
| --- | --- | --- | --- |
| A1 | Deadline and afterwards | Given: MVP in two weeks (10 working days), then continued | Phase 1 code is kept, not thrown away |
| A2 | People, hours, familiarity | Given: three developers. Assumed: full time on this, about 6 focused h/day each, new to ADK (×1.5 on estimates), comfortable with GCP basics | Capacity, owners |
| A3 | Money | About $150/month for model and cloud during the pilot; a billing alert only, not a hard cap | D7 |
| A4 | Users and what they see | The salons' own customers, already signed in to our existing booking web app, using a chat panel there. Salon staff are not users in phase 1 | D3, D8 |
| A5 | Data and effects | Real personal data (name, appointments). Reversible writes that real people see: book, move and cancel. No payments or deposits | D2, D4, floor |
| A6 | Booking API | We own it. It accepts the customer's bearer token, lists that customer's appointments, offers availability, create, reschedule and cancel. It enforces the cancellation policy. Idempotency-key support is **unknown** | D3, D4; G01 confirms |
| A7 | Rollout | One pilot salon at the end of phase 1; the other four in phase 2 (G13) | G09, G13 |
| A8 | Language and channel | English, web chat only (no SMS, WhatsApp or voice) | D8, later list |
| A9 | Region and residency | Same region as the booking API, not yet known | D6, G08 |
| A10 | Retention | Conversations kept 30 days | D9, G12 |
| A11 | Human fallback | The assistant gives the salon's phone number; no live handover | D1 |
| A12 | Sign-off | The chain's operations manager approves the policy text, the assistant's wording and the pilot salon; 3–5 working days (W1) | G09 |

## Purpose and journey

**Journey.** Maya, signed in to the chain's booking site, types "can I move my
Thursday cut with Sam to next week, ideally after 5?" Today she has to find the
appointment, cancel it and search the calendar again, or phone a busy salon
during opening hours. With the assistant, it finds her Thursday appointment and
searches Sam's availability next week after 17:00 at that salon. It offers three
slots. When she picks one, a card shows the old time, the new time, the salon,
the service and the stylist. She presses **Confirm**, the booking API
reschedules, and the card shows the receipt.

**Outcome to improve.** Booking changes completed without a phone call. That
benefit is a hypothesis. G09 records a baseline (completed versus abandoned
proposals during the pilot week), and the guardrail is that fewer than 1 in 20
confirmed operations needs a staff correction. That threshold is an assumption.

**Model versus code.** The model interprets the request, chooses read tools,
asks clarifying questions and drafts proposals. Code owns identity, the
customer's scope, today's date and the salon's time zone, slot validity,
confirmation, the write itself and its outcome. Non-goals for phase 1: payments,
staff-facing use, other channels, memory of preferences across conversations,
and marketing.

## Delivery constraints, depth and deferred controls

Profile: **MVP or pilot.** Real customers complete a journey that changes real
appointments, so the team must be able to see failures and cost. It sits below
production because there is one pilot salon and no SLOs yet.

| Concern | Depth now | Trigger that raises it |
| --- | --- | --- |
| Core judgment, measured | Build: an evaluation set of about 30 cases (G07) | More salons (G13) brings the CI gate (G11) |
| Identity and per-customer scope | Build (D3) | — |
| Secrets | Build: workload identity, no booking-API secret (D3) | — |
| External writes | Build: confirmation, at most one effect per confirmation, uncertain outcomes kept (D2, D4) | First uncertain outcome in production brings G10 forward |
| Sensitive data | Build: tool-result projections and no message text in logs (D9); retention purge deferred | Purge (G12) is due before day 30 after launch |
| Injection and agency | Build structurally: the agent has no write tool (D2); adversarial cases in G07 | Free-text fields or a new channel |
| Budgets | Build: per-turn call cap and per-customer daily allowance (D7) | Abuse, or spend above 50% of A3 |
| Memory | Sessions only (D5) | A repeated "same as last time" request in pilot transcripts |
| Frontend | Build: minimal chat panel with cards (D8) | Slot-picker and streaming in phase 2 (G14) |
| Hosting | Cloud Run with revision rollback (D6) | — |
| Observability | Build: traces, token cost, operation outcome logs (G08) | SLIs and alerts with more salons (G13) |
| Release | Minimal: pinned versions, deterministic CI, manual evaluation run before release (D11) | G11 before the second release that changes the prompt or model |
| Performance tuning | Defer | Median reply above 6 s in pilot traces |

**Floor kept:** no secrets in code, prompts or logs. Spend stops through
`max_llm_calls`, the daily allowance and a billing alert. Nothing changes an
appointment without the customer's own click on a card that shows its details.
Real data is limited to the signed-in customer's own records and kept out of
logs. The model ID is pinned. No risks accepted beyond A3's alert-only budget.

**Who may use it:** signed-in customers of the pilot salon. **Graduation
conditions** before all five salons: G10 to G13 complete; no unreconciled
uncertain operations; pilot correction rate within the guardrail.

## Guarantees

| ID | Invariant | Enforcing component and evidence | Failure outcome | Planned verification |
| --- | --- | --- | --- | --- |
| I1 | A customer reads and changes only their own appointments | The gateway derives `customer_id` from the token the booking API verifies. Tools and the executor call the booking API with that same customer token, and the API authorizes it | 404 or denial; nothing is disclosed | G05 and G03 cross-customer tests; G07 adversarial cases |
| I2 | No booking, move or cancel without the customer's click on a card showing salon, service, stylist and local time (plus the old time for a move) | Executor in the gateway's confirm endpoint (D2); the model has no write tool | Without a click the proposal expires; nothing happens | G03 and G04 tests: the model cannot reach a write; an expired card is refused |
| I3 | One confirmation causes at most one booking-API effect | Atomic claim on the operation row; idempotency key = operation ID (D4) | A double click returns the first outcome | G03 concurrent-confirm test |
| I4 | An uncertain write is never re-sent automatically and is visible | Operation state `uncertain`; staff alert log (D4) | The customer is told it is being checked and not to rebook | G03 timeout test |
| I5 | A proposed time is a real slot from this conversation's search, in the salon's time zone | `propose_*` takes a `slot_id` that code resolves from the session's stored search results | Unknown slot → actionable tool error | G04 test with a made-up time |
| I6 | Spend is bounded | `RunConfig.max_llm_calls=8` per turn; 40 turns per customer per day in Postgres; billing alert | Polite stop message | G05 tests |

## Architecture and decisions

```text
Browser (booking web app, signed in)
  │  token + message                 │ Confirm(operation_id)
  ▼                                  ▼
Cloud Run: gateway (FastAPI) ──────► executor ──► Booking API (customer token)
  │ verifies token → customer_id        ▲  claim/record
  │ per-session lock, allowance         │
  ▼                                     │
ADK Runner → LlmAgent (Vertex, gemini-3.8-flash)
  read tools ─────────────────────────► Booking API (customer token)
  propose_* ──► operations table ───────┘
Cloud SQL Postgres: ADK sessions, operations, daily usage
```

| ID | Requirement | Design choice | Reason | Tradeoff / alternative | Verification |
| --- | --- | --- | --- | --- | --- |
| D1 | Interpret free-form booking requests | One `LlmAgent` with seven function tools: `list_salons_and_services`, `search_availability`, `list_my_appointments` (reads) and `propose_booking`, `propose_move`, `propose_cancel` (proposals), plus `salon_contact` | One judgment, a small tool set and one context; sub-agents would have no distinct responsibility | A router with per-intent sub-agents adds routing errors for no isolation gain | Selection accuracy on G07 |
| D2 | Writes need the customer's approval (I2) | Proposal tools only write a `proposed` operation row with a canonical payload and a 10-minute expiry, then return a card. The browser's Confirm calls `POST /operations/{id}/confirm`, and code executes | The model cannot reach a write, which removes the write leg of the lethal trifecta and makes approval a deterministic click | More frontend work than ADK's built-in tool confirmation, whose known limitations would need checking against the pin | G03 and G04: no write without the confirm call; the payload executed equals the payload shown |
| D3 | Per-customer scope (I1) without a new secret | Forward the customer's existing booking-app token. The gateway verifies it with the booking API and sets the session `user_id` to `customer_id`. The token stays in request memory only, never in session state, events or logs | The API already authorizes customers, so it becomes a second enforcement point | An expired token ends the turn with "please sign in again"; a service credential would need its own scoping and a secret | G05: forged or other-customer session IDs denied; the token is absent from stored events |
| D4 | At most one effect, honest uncertainty (I3, I4) | `operations` table with states `proposed → executing → succeeded / failed / uncertain / expired`. The claim is `UPDATE … WHERE state='proposed' AND expires_at>now()`. Send `Idempotency-Key: <operation_id>` if the API supports it (A6). A timeout or 5xx after dispatch → `uncertain`, with no retry. Reconciliation is manual in phase 1 (runbook) and automatic in G10 | Keeps the operation identity across retries and double clicks | Manual reconciliation costs staff time until G10 | G03 tests |
| D5 | Conversation state survives restarts and instances | ADK `DatabaseSessionService` on Cloud SQL for PostgreSQL (smallest tier), the same instance as `operations` and usage | One transactional store; no memory service needed | One more managed service versus managed Agent Platform sessions; the cost is checked in G08 | G05 restart test |
| D6 | Host the gateway and Runner | One Cloud Run service, min instances 1 during salon hours, in the booking API's region (A9). Roll back by moving traffic to the previous revision | The gateway is needed anyway for identity and the confirm endpoint; Agent Runtime would add a second hop | Instance cost against cold starts | G08 deploy readback; G09 rollback rehearsal |
| D7 | Model and spend (I6) | Vertex AI `gemini-3.8-flash`: stable, released 2026-09-02, no shutdown or Vertex retirement listed in the lifecycle snapshot checked 2026-10-08. Low thinking level, no `output_schema`. Avoid `gemini-3.6-flash` (Vertex retirement 2026-11-19) and `gemini-3.7-flash` (2027-01-28) | Inside the plan horizon; workload identity, no API key | Regional availability is unverified (G08) | G08 calls the pinned ID in the region |
| D8 | Browser contract | Completed JSON per turn `{messages[], cards[], turn_status}`; a card is `{operation_id, kind, details, expires_at, state}`. No streaming | Replies are short; the cards carry the consequential state | No progressive text; revisit in G14 | G05 and G06 contract tests |
| D9 | Personal data | Tool results are projections: the customer's own appointments only, no contact fields, stylist first names. Telemetry content capture off; logs hold IDs and outcomes, never message text | MVP depth without new services | Harder debugging from logs; traces keep IDs that lead to the session | G08 log sample check |
| D10 | Overlapping turns in one conversation | A Postgres advisory lock per session; an overlapping turn returns 409 "still working" | Prevents interleaved tool calls and duplicate proposals | The user must wait | G05 test |
| D11 | Behavior comparable across releases | `release.json` records image digest, model ID, prompt version, tool-schema hash and ADK version. Deterministic tests run in CI; the evaluation set runs by hand before each release (G09) | MVP depth within capacity | A CI gate waits for G11 | G09 release record |

**Versions.** No ADK is installed here. The working assumption is
`google-adk==2.8.0`, the version the specialist skills were checked against.
G01 confirms it against the chosen pin. ADK interfaces named here (`LlmAgent`,
`Runner`, `RunConfig.max_llm_calls`, `DatabaseSessionService`) need checking
against that pin.

### Model-facing contracts

| Surface | Contract | Skill and verification |
| --- | --- | --- |
| Instruction | Scope: booking, moving and cancelling at the chain's salons. Always search before proposing. Never claim success until a card shows `succeeded`. Give the salon's number when stuck. Today's date, the customer's first name and the salon time zones come from state templating that code fills | `adk-agent-instructions`; rendered-request test (G02) |
| Tools | Seven declarations, primitive parameters, results capped at 10 slots or appointments, `{status, …, error_hint}`. Tier: read / proposal; no write tier exposed | `adk-tool-interface-design`; declaration dump (G02, G04) |
| Output and model | Plain conversational text; pinned ID per D7 | `adk-model-and-output-contracts`; G01 records the pin |

## Data and authority

| Data | Owner and scope | Writers / readers | Source and freshness | Lifetime |
| --- | --- | --- | --- | --- |
| Appointments, availability | Booking API, per customer | Executor writes; tools read | Live on each call; rechecked at confirm | Booking API's policy |
| Operations | Gateway, per customer | Proposal tools, executor | Authoritative for "what the assistant did" | 1 year (audit; assumption) |
| ADK sessions | Gateway, `user_id = customer_id` | Runner | Per conversation | 30 days (A10; purge in G12) |
| Customer token | Customer | Request memory only | Per request | Never stored |

**Security posture.** For the single agent: private data yes (own appointments),
untrusted content only the customer's own messages (salon and service text comes
from our API), write or egress none (D2). Resolution: write leg removed.
G07 adversarial cases cover other customers' IDs, "skip the confirmation" and
instructions planted in a message.

## Budgets and capacity

Expected per turn: 2–4 model calls (8 maximum) and 1–3 booking-API calls. A
pilot salon handles tens of conversations a day, so concurrency is in single
digits. Cost is symbolic until G08 checks current Vertex and Cloud SQL prices.
The billing alert is set at A3. Exhaustion outcomes: the turn cap gives a polite
stop; the daily allowance points to the booking site and the salon phone.

## Failure and recovery

| Failure | Customer sees | State / possible effect | Next action and owner |
| --- | --- | --- | --- |
| Slot taken between proposal and confirm | Card `failed`: "that time was just taken" and the agent offers to search again | Operation `failed`; no effect | Customer searches again |
| Booking API times out after dispatch | Card `uncertain`: "we're checking, please don't book again; the salon will confirm" | The effect may have happened | Staff runbook (G09) checks the appointment list; G10 automates this |
| Double click or two tabs | Same card outcome twice | One effect (I3) | None |
| Confirm after expiry, or the appointment changed meanwhile | "This proposal expired"; agent searches again | Nothing | Customer |
| Instance restarts while `executing` | Card stays `executing` and is shown as uncertain after 60 s | Possible effect | As for a timeout |
| Model unavailable or call cap reached | "I can't help right now", booking-site link and salon phone | No operation | Customer; alert via G08 logs |
| Token expired mid-conversation | "Please sign in again"; the conversation resumes | Session kept | Customer |
| Another customer's appointment ID, or a forged session ID | Not found | Nothing read or changed | None; logged as a denial |
| Cancellation inside the policy window | Card `failed` with the API's reason | Nothing | Customer phones the salon |
| Rollback | Previous revision serves; open proposals expire | Operations kept | Release owner (G09) |

## Open decisions

| Question | Why it matters | Who settles it | Blocks |
| --- | --- | --- | --- |
| A6: does the booking API accept an idempotency key? | Without one, I3 rests on the claim alone and timeouts become more common | Booking-API owner (G01) | G03 detail only |
| A6: is "move" a reschedule endpoint or cancel plus create? | Cancel plus create can leave the customer with no appointment | G01 | G03 and G04 scope |
| A9: region, and is the model available there? | Hosting and residency | G08 | G09 |
| A2 and A3: hours and money | Every estimate and the cut line | User | Plan |
| A7 and A12: pilot salon and who signs off | Go-live | User / chain | G09 |
