# System design: salon booking assistant (MVP)

Status: **draft**. Written in one pass without the user available; every
answer in the Assumed answers table is provisional, and so is every decision
that depends on one. No decision below has been accepted by the user yet.

Decisions and their rationale live here. Estimates, owners, dependencies,
capacity, finish range and the cut line live in the
[plan](../plans/salon-booking-assistant.md); each goal's scope and acceptance
live in its [ticket](../tickets/salon-booking-assistant/).

## Purpose and constraints

**Journey (running example).** Priya, an existing customer of the Camden
salon, is signed in on the chain's website on a Tuesday evening. She types "can
I move my Thursday cut to Saturday afternoon, same stylist?". Today she would
phone the salon during opening hours, or work through the booking page's
calendar for the right salon, stylist and service. The assistant finds her
Thursday appointment, finds Saturday slots with that stylist, and offers a
**Move** card: "Thu 22 Oct 10:00 → Sat 24 Oct 14:30, Women's cut with Sam,
45 min, £52". Priya clicks Confirm; the booking API reschedules it; the card
shows the new booking reference. If anything is uncertain she is told so, and
the salon phone number is offered.

**Outcome to improve (hypothesis, unmeasured).** More bookings, moves and
cancellations completed outside opening hours without staff time, with no rise
in wrong or duplicate appointments. Baseline: unknown; the first week's counts are recorded in G14.

**Fixed constraints (from the request).** Three developers; MVP in two weeks,
then continued; ADK; the existing booking API is the only system that books,
moves and cancels; design only in this session.

**What the model decides and what code controls.** The model interprets the
customer's words, picks salon, service, stylist and time from tool results,
and proposes one operation per appointment it would change. Code owns everything else: who the customer is,
which appointments are theirs, the salon notice-window policy, the payload
that is executed, confirmation, idempotency, retries and the result the
customer is shown.

**Non-goals for phase 1.** Guest booking without an account, payments or
deposits, staff-facing features, channels other than the web widget,
languages other than English, cross-session memory ("my usual stylist").

### Assumed answers

The user could not be asked. Each row is the question I would have asked, the
answer assumed, and the decisions that are provisional because of it.

| # | Question | Assumed answer | Provisional decisions |
| --- | --- | --- | --- |
| Q1 | When exactly is "two weeks", and is it continued? | 10 working days, Mon 19 Oct to Fri 30 Oct 2026; continued after launch | Plan dates, phase split |
| Q2 | How many focused hours per day can each developer give, and how familiar are they with ADK and GCP? | ~6 h/day on this project at focus 0.6 (3.6 h/day); new to ADK (estimates ×1.5); have used GCP before (no extra setup day) | All estimates, the cut line |
| Q3 | What spend is available for models and cloud? | Up to about US$300/month during the MVP; a billing alert at that figure | D10 |
| Q4 | Who uses it and who judges it? | Existing customers of the five salons, signed in on the chain's website; judged by the founders and the salon chain's owner | D2, D9 |
| Q5 | What data does it touch and what can it change? | Real personal data (name, contact, appointment history); real bookings, moves and cancellations in the live booking system, visible to customers and staff | Profile, floor, D3, D4 |
| Q6 | Does the existing site have a customer login that issues a verifiable token? | Yes: a signed JWT with a JWKS endpoint | D2, G02 (if no: open decision OD1) |
| Q7 | Do we own the booking API and does it have a staging environment? | Yes, built by this team; staging exists with test data for the five salons | D5, D6, G01, G06 |
| Q8 | Does the API accept an idempotency key, and is reschedule one atomic call? | Unknown; assumed "reschedule is one call", idempotency unknown | D5, D6 (settled by G01) |
| Q9 | Does the booking system message customers on changes? | Yes in production (its own SMS/email); disabled on staging | Floor, G01, G10 |
| Q10 | What are the salons' rules: notice window for moves/cancels, bookable services, deposits? | 24 h notice placeholder, all services bookable, no deposits; real values come from the salon chain (wait W1) | G04/A8, G09 |
| Q11 | Where are the salons and where must data stay? | UK; Vertex AI and Cloud SQL in `europe-west2` (London), subject to model availability there | D7, D8 |
| Q12 | Must new customers without an account be able to book? | Not in phase 1 | Non-goals, phase 2 G17 |
| Q13 | Which languages and channels? | English, web widget only | D9 |
| Q14 | Who are the three developers by strength? | Dev A knows the booking API; Dev B front end and prompting; Dev C backend and GCP | Owners in the plan |
| Q15 | Launch all five salons at once or pilot one? | All five at once, each with its own enable flag as a rollback | G05/A2, G11 |
| Q16 | Who handles uncertain operations after launch? | Dev A checks the operator list daily during phases 1 and 2 | G06/A7 |
| Q17 | Where is the cut line? | Full scope, go-live after 14 working days (Thu 5 Nov); see the plan's summary | Plan, OD3 |

## Delivery constraints, depth and deferred controls

| Scope-gate answer | Value |
| --- | --- |
| First useful version due, and what happens after it | Fri 30 Oct 2026 (Q1); continued |
| People and hours | Three developers, 3.6 focused h/day each (Q2); new to ADK; the team runs it afterwards |
| Money | About US$300/month (Q3) |
| Users or judge, and what they read | Signed-in salon customers using it; founders and the salon chain judging the running service (Q4) |
| Data touched and effects allowed | Real personal data; real writes to the live booking system (Q5) |
| Delivery profile | **MVP or pilot**: first external users, real writes, team learns from failures and cost |

Depth per concern:

| Concern | Depth now | Trigger that raises it |
| --- | --- | --- |
| Core judgment, measured | Build: 25+ labelled cases run before release (G09) | Live gate in CI in phase 2 (G13) |
| Identity and per-customer scope | Build: verified login token, ownership checked in code (G02, G04) | Guest booking (G17) |
| Secrets | Build: Secret Manager and per-service accounts (G06, G08) | Automated rotation when a second credential appears |
| External writes | Build: confirmation in code, durable operation record, idempotent dispatch, reconciliation (G04, G06) | Payments or deposits (full redesign) |
| Sensitive data | Build, minimal form: fields minimised, no content in logs or traces, 30-day retention (G03, G05, G08) | Free-text notes or health details (allergies) enter chats: Model Armor / SDP |
| Prompt injection and agency | Build: the model holds no write tool; adversarial eval cases (G03, G09) | Phase 2 threat model (G15) |
| Budgets and loop limits | Build: per-turn call cap, per-customer daily allowance, kill switch, budget alert (G03, G05, G08) | Shared budgets if traffic grows past the allowance |
| Memory | Conversation sessions only | Customer feedback asking for preferences (G18) |
| Frontend | Build: minimal widget in the existing site (G07) | Other channels |
| Hosting | Cloud Run staging and production with rollback (G08) | Measured latency or availability need |
| Observability | Build: content-free logs, traces and token counts (G05, G08) | SLOs and alerts in phase 2 (G14) |
| Release engineering | Minimal: pinned image, model and prompt; deterministic tests in CI; live eval run by hand (G09) | First prompt or model change after launch: CI gate (G13) |
| Performance and cost tuning | Defer | Measured p95 or cost per completed operation above target |

**Deviation from the MVP default.** The profile default builds the evaluation
gate into CI in phase 1. Here it is a hand-run release step in G09 and G12 and a
CI gate in G13, because the phase 1 calendar does not fit even without it
(plan summary). Risk while it waits: a prompt change after launch could ship
untested; mitigated by the rule that no prompt or model change ships before
G13.

**Floor kept.** No secrets in code, prompts, logs or documents; a spend stop
(`RunConfig.max_llm_calls`, per-customer allowance, kill switch, budget alert);
every booking, move and cancellation needs the customer's own click on a card
rendered from the stored operation; real personal data limited to what the
journey needs and kept out of logs; the model ID pinned. No accepted risks.

**Who may use it, on what data.** Signed-in existing customers of the five
salons, on their own appointments only. **Graduation conditions** before guest
customers, other channels or payments: G13 (CI gate), G14 (alerts on
uncertain operations), G15 (threat model), and a two-week clean record of
uncertain operations being reconciled within one day.

## Guarantees and acceptance

| Invariant | Enforcing component and authority | Failure outcome | Verification |
| --- | --- | --- | --- |
| I1 A customer sees and changes only their own appointments | Chat API derives `customer_id` from the verified token (G02); tools read it from trusted state; the operations service checks ownership against the booking API at propose and at confirm (G04) | 404 / refusal, no write | G02/A3, G03/A5, G04/A3 |
| I2 No booking, move or cancel happens without the customer's click on a card showing the material details | Model tools only create pending proposals; only `POST /operations/{id}/confirm` dispatches, executing the stored payload (G04) | Proposal expires unconfirmed | G03/A7, G04/A6, G07/A2 |
| I3 One confirmed operation produces at most one change in the booking system | Operation record claimed atomically before dispatch; `operation_id` sent as idempotency key or reconciled by lookup (G04, G06; D6) | Later confirms return the stored result | G04/A5, G06/A2 |
| I4 The customer is never told "done" unless the booking API confirmed it | Card status comes from the operation record, not model text (G04, G07) | "We're checking" for uncertain outcomes | G04/A4, G07/A3 |
| I5 Spend per turn and per customer is bounded, and an operator can stop it | `max_llm_calls=8` (G03); 30 turns/customer/day and kill switch (G05); budget alert (G08) | Friendly refusal, no model call | G03/A8, G05/A1, G05/A2, G06/A6 |
| I6 No conversation content or contact details in logs or traces | Structured logging and trace content capture off (G05, G08) | — | G05/A4, G08/A6 |

## Architecture and decisions

```text
Browser (existing site, signed in)
  │  customer token (existing login)
  ▼
Chat widget (G07) ──JSON──▶ Chat API on Cloud Run (G02, G05)
                             │ verify token → customer_id (trusted state)
                             │ admission: allowance, kill switch, one turn per session
                             ├──▶ ADK Runner → LlmAgent "booking_assistant" (G03)
                             │        │ model: Vertex AI gemini-3.5-flash (pinned)
                             │        └─ tools: read tools ──▶ Booking API (reads)
                             │                  propose_* ──▶ Operations service (pending only)
                             ├──▶ POST /operations/{id}/confirm ─▶ Operations service (G04)
                             │        claim → recheck → dispatch ──▶ Booking API (writes, G06)
                             └──▶ Cloud SQL Postgres: ADK sessions, operations, allowance
Secret Manager: booking API service credential.  Cloud Logging / Trace: content-free.
```

Trust boundaries: the browser and everything the customer types are untrusted;
the chat API is the only component that turns a token into a customer ID; the
model can read and propose but cannot write; the operations service is the only
caller of booking API write endpoints.

| ID | Requirement | Design choice | Reason | Tradeoff / alternative | Verification | Status |
| --- | --- | --- | --- | --- | --- | --- |
| D1 | Interpret free text into one booking operation | One `LlmAgent` with six function tools; no sub-agents | One judgment (what does the customer want), small tool set; sub-agents add routing without a distinct responsibility | Less separation than a reader/writer split, which D3 already provides structurally | Declaration dump shows six tools (G03/A5) | Proposed |
| D2 | Customers act only on their own appointments (I1) | Verify the existing login's JWT in the chat API; put `customer_id` in session state each turn; no tool takes a customer ID | Identity from a verified token, never from model arguments | Depends on Q6; magic-link login would replace it (OD1) | G02/A2, G02/A3, G03/A5 | Proposed, depends on Q6 |
| D3 | No write without the customer's approval (I2) | Model calls `propose_booking/move/cancel`, which only store a pending operation; the widget renders the stored operation as a card; the click calls a confirm endpoint in code | The model never holds a write tool, so injected or mistaken text cannot change a booking; confirmation binds to the stored payload | Not ADK's native tool confirmation: we own an extra endpoint and card, but avoid depending on its resume behaviour and its documented known limitations (not re-checked in this session) | G04/A6, G07/A2 | Proposed |
| D4 | One click, one change, even with retries, double clicks and restarts (I3, I4) | Postgres `operations` table: `operation_id`, owner, kind, canonical payload, status (`pending → dispatching → succeeded / rejected / changed / expired / uncertain / failed`), booking reference; conditional update claims before dispatch; reconcile before any re-dispatch | A durable record survives the lost reply; status lookup prevents a duplicate | A table and an operator script to maintain | G04/A4, G04/A5 | Proposed |
| D5 | Move must not leave the customer with two or zero appointments | Move is one reschedule call on the existing appointment | Atomic at the provider: the old slot is kept if the new one fails | If G01 finds no atomic reschedule, either add one to our API or accept book-then-cancel with a `partially_applied` status (OD2) | G04/A11 | Proposed, settled by G01 |
| D6 | Replay contract for writes | Send `operation_id` as the API's idempotency key if supported; otherwise reconcile by listing the customer's appointments and matching salon, start time and service before any retry | We own the API, so a key is cheap to add later | Lookup-based reconciliation can be ambiguous for two identical bookings; then the status stays `uncertain` for the operator | G06/A2 | Proposed, settled by G01 |
| D7 | Host the chat API and keep state across instances | Cloud Run (staging and production services, separate service accounts and databases); Cloud SQL for PostgreSQL for ADK `DatabaseSessionService`, operations and allowance; Secret Manager | Cloud Run hosts our own FastAPI routes (confirm, operator) next to the Runner; one Postgres gives transactions for the operation claim | Managed Agent Runtime would manage sessions but we would still need a service for confirm and admission; GKE is more to run than three people need | G08/A1, G08/A5 | Proposed |
| D8 | Model behaves the same tomorrow and stays available through the plan | Pin `gemini-3.5-flash` on Vertex AI | Stable; Vertex retirement "2027-05-19 or later" and ADK 2.8.0's default, per the lifecycle snapshot checked 2026-10-08 (`adk-model-and-output-contracts/assets/model-lifecycle-2026-10-01.json`); `gemini-3.8-flash` is newer but its Vertex retirement date is not in the snapshot | A newer model may be better; compared on the eval set in G13 | G03/A8; region availability checked in G08/A3 | Proposed |
| D9 | Customers use it where they already sign in | Non-streaming JSON API (`/chat`, `/operations/{id}/confirm`, `GET /operations/{id}`) and a small widget in the existing site | Completed JSON per turn is enough for short replies; streaming adds failure handling with little benefit here | No token-by-token display | G07/A1 | Proposed |
| D10 | Bounded spend and abuse (I5) | `RunConfig.max_llm_calls=8` per turn; 30 turns per customer per rolling 24 h in Postgres; global and per-salon kill switch; Cloud Billing budget alert at Q3's figure | Admission in code is the stop; a budget alert only notifies | A legitimate heavy user can hit the daily limit | G03/A8, G05/A1, G05/A2, G08/A4 | Proposed, figures depend on Q3 |
| D11 | Personal data limited and out of logs (I6) | Tool results carry only the fields the conversation needs; logs carry IDs, counts and statuses; trace content capture off; sessions and operation payloads purged after 30 days | Cheapest form of the sensitive-data floor for an MVP | No content-level screening (Model Armor/SDP) yet | G03/A6, G05/A4, G05/A5, G06/A8, G08/A6 | Proposed |
| D12 | Tool results do not flood or steer the model | Results capped (≤ 10 slots, ≤ 2 KB), free-text API fields truncated and returned as data fields | Bounded context and less injected text | Long service descriptions are cut | G03/A6 | Proposed |

**Versions.** No code exists yet. Working assumption: `google-adk==2.8.0`,
the version the specialist skills were checked against (each specialist's
`references/compatibility.md`); confirming the chosen pin and the APIs used is
G03/A10. Model and region availability are G08/A3. Prices were not looked up
(no network in this session); see Budgets.

### Model-facing contracts

| Surface | Contract | Implementing skill and verification |
| --- | --- | --- |
| Instruction | Owns: understanding the request, asking one clarifying question when salon, service or time is ambiguous, proposing one operation per appointment (never a bulk operation), never claiming an operation is done (the card shows the result). Code owns: customer identity, today's date and salon opening hours (injected from config into state), notice-window policy, payload, execution | `adk-agent-instructions`; rendered-request test in G03 |
| Tools (six) | Read: `list_salons_and_services()`, `find_available_slots(salon_id, service_id, date_from, date_to, stylist_id=None)`, `list_my_appointments()`. Propose (write-intent, no effect): `propose_booking(slot_id)`, `propose_move(appointment_id, new_slot_id)`, `propose_cancel(appointment_id)`. Each returns `{status, ...}` with actionable errors; no customer parameter; results bounded (D12) | `adk-tool-interface-design`; declaration dump in G03/A5 |
| Output and model | Plain text replies; no `output_schema` (proposals travel through the operations store, not model output). Pinned `gemini-3.5-flash`, Vertex AI backend, default thinking; no failover in phase 1 (model outage → fallback message, G03/A11) | `adk-model-and-output-contracts`; G03/A8, G03/A9 |

### Chat API contract (shared by G02, G04, G07)

Proposed, labelled unverified until G02 and G04 implement it:

```text
POST /chat                      {session_id?, message}
  → 200 {session_id, reply_text, proposals: [{operation_id, kind, details, expires_at}]}
    proposals = pending operations created in this invocation, read from the store
  → 401 sign in · 404 unknown session · 409 turn in progress · 429 daily limit · 503 unavailable
POST /operations/{id}/confirm   {}           (body ignored)
  → 200 {operation_id, status, booking_reference?, reason?, next_step?}
GET  /operations/{id}           → same shape, owner only
```

`details` for a move holds both the old and the new appointment. Statuses as in D4.

## Data and authority

| Data / operation | Owner and authorized scope | Writers / readers | Source and freshness | Lifetime / erasure |
| --- | --- | --- | --- | --- |
| Customer identity | Existing login | Chat API reads token each request | Token expiry | Not stored beyond the session's `user_id` |
| Appointments, slots, services | Booking API (authoritative) | Operations service writes; read tools read | Live per call; re-read at confirm | Booking system's own policy |
| Conversation session | Chat API, per verified customer | ADK Runner | — | 30 days, purged (G05/A5) |
| Operation records | Operations service, per customer | Operations service; operator script | Status from booking API responses and reconciliation | Payload details 30 days; ID, status and reference kept for audit |
| Allowance counters | Chat API | Admission | Rolling 24 h | 48 h |
| Booking API service credential | Secret Manager | Operations service and read adapter | Secret version | Rotated by new version |
| Salon policies and opening hours | Salon chain (W1), stored as config | Read by code, injected into state | Per release | — |

The booking API service credential can act for any customer, so ownership is
enforced in our code (I1), not by the credential.

### Security posture

| Agent | Private data | Untrusted content | Write or egress | Resolution |
| --- | --- | --- | --- | --- |
| booking_assistant | The signed-in customer's appointments | Customer messages; free-text fields from the booking API (service descriptions, stylist bios) | None directly: `propose_*` creates pending records only; replies go only to the same customer | Write leg removed from the model (D3); ownership and payload checked in code (G04); adversarial eval cases (G09/A4) |

Tool tiers: read (three read tools), write-intent (three propose tools, no
effect), write (confirm endpoint, code only, customer click). No code
execution. Model text is rendered as escaped plain text in the widget (G07/A5).

## Budgets and capacity

Workload assumption (labelled, unmeasured): five salons, about 15 assistant
conversations per salon per day, about 6 turns each, about 2 model calls per
turn → roughly 900 model calls per day. Bounded per turn by
`max_llm_calls=8`; per customer by 30 turns/day. Read tool calls: at most 2
attempts each; confirm: at most 3 attempts in a 10 s deadline (G04/A9).
Cost per conversation = calls × (input tokens × input price + output tokens ×
output price); prices were not looked up in this session, so the monthly
figure is unverified. G14 measures tokens per turn in production; G08/A4
sets the budget alert. Cloud Run scales to zero with `max-instances=3`; one
small Cloud SQL instance is the fixed cost. Latency target (provisional): a
reply within 8 s for 95 % of turns, measured in G14.

## Failure and recovery

Coverage grid, one row per external system:

| Integration | Unavailable or slow | Rejects the request | Write outcome unknown | Partial multi-step change | Credential expired or revoked | Rate limited or out of quota | Duplicate or concurrent request | Untrusted or malformed content |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Booking API, reads | G03/A2 | G03/A3 | n/a: reads change nothing | n/a: single read calls | G03/A3 | G03/A4 | n/a: reads are safe to repeat | G03/A6, G06/A5 |
| Booking API, writes | G04/A9, G04/A4 | G04/A9, G04/A2 | G04/A4, G06/A2 | G04/A11, G01/A2, G06/A1 | G04/A10 | G04/A9 | G04/A5, G06/A2 | G06/A5 |
| Vertex AI model | G03/A11 | G03/A11 | n/a: model calls change nothing | n/a: each proposal is its own record | G03/A11 | G03/A11, G08/A4 | G05/A3 | G03/A9, G09/A4 |
| Customer login (token, JWKS) | G02/A4 | G02/A2 | n/a: verification is read only | n/a: no multi-step change | G02/A7, G02/A8 | G02/A4 | n/a: verification is stateless | G02/A2 |
| Cloud SQL (sessions, operations, allowance) | G05/A6, G04/A12 | G04/A14 | G04/A14 | G04/A13 | G05/A6 | G05/A6 | G04/A5, G05/A3 | G03/A7, G09/A4 |

Action grid:

| Action | Over-broad or wrong target | Partially applied | Confirmation stale or changed | Outcome unknown | Repeated or concurrent |
| --- | --- | --- | --- | --- | --- |
| Book | G07/A2, G04/A6 | n/a: one booking API call | G04/A2 | G04/A4 | G04/A5 |
| Move | G04/A3, G07/A2 | G04/A11, G01/A2, G06/A1 | G04/A2 | G04/A4 | G04/A5 |
| Cancel | G04/A7, G04/A3 | n/a: one cancel call per appointment | G04/A2 | G04/A4 | G04/A5 |

Cross-cutting scenarios:

| Failure window | User-visible outcome | Retained state / possible effects | Safe next action and recovery owner |
| --- | --- | --- | --- |
| Priya clicks Confirm, the booking API reschedules, the reply is lost | Card: "We're confirming this; check My bookings" | Operation `uncertain`; the move may have happened | Reconcile by lookup before any retry (G04/A4); operator script for leftovers (G06/A7), Dev A daily |
| Browser closes or times out during confirm | On reopen, the card shows the stored status | Operation record | Widget re-posts confirm, which returns the stored result (G07/A4, G04/A5) |
| Process restart between claim and dispatch | Same as lost reply | `dispatching` record | Treated as `uncertain`, reconciled (G04/A5) |
| Salon changes its notice window while a proposal is pending | Confirm refused with the reason | Pending proposal | Policy rechecked at confirm (G04/A8) |
| Text in a message or service description tells the model to cancel everything | At most one card per appointment, each needing a click | Pending proposals only | Structural (D3); tested in G03/A7, G09/A4 |
| Spend or abuse spike | Daily-limit message; or "assistant unavailable, call the salon" | None | Allowance (G05/A1); kill switch (G05/A2) by any developer |
| A bad release | Errors or wrong proposals | Sessions and operations survive | Roll back image, prompt and model together (G08/A5) |
| `gemini-3.5-flash` approaches Vertex retirement (2027-05-19 or later) | None if planned | — | Planned migration with re-baseline (plan, Later) |
| An incident needs attribution | — | Logs and traces by session and operation ID | G05/A4, G08/A6 |

## Verification and implementation handoff

- **Offline deterministic:** fake booking API, scripted model, local Postgres:
  G02–G05 acceptance, run in CI (G09/A3).
- **Local integration:** process restart for sessions and operations (G02/A6,
  G04/A5).
- **Bounded live:** staging booking API (G01/A2, G06), live model eval with a
  cost cap (G09/A2), staging journey and drills (G10, G12).
- **Release:** production smoke and first-day watch (G11).

The evaluator reads the running service and the eval summary recorded in the
plan. Implementation goals, owners and the next prompt: see the
[plan](../plans/salon-booking-assistant.md). Proposed module layout (greenfield,
unverified):

```text
salon_assistant/agent.py            LlmAgent factory and instruction (G03)
salon_assistant/tools/read.py       read tools (G03)
salon_assistant/tools/proposals.py  propose_* tools → operations interface (G03)
salon_assistant/booking_api/        read adapter (G03), write adapter (G06)
salon_assistant/operations/         store, service, confirm router (G04)
salon_assistant/api/                app, auth, admission, logging (G02, G05)
salon_assistant/ops_cli.py          operator list / resolve (G05)
evals/                              cases and runner (G09)
widget/ (in the existing site's repository)  chat widget (G07)
```

## Open decisions

| Question or assumption | Why it changes the design | Owner / evidence needed | What it blocks |
| --- | --- | --- | --- |
| OD1 Does the existing login issue a verifiable token (Q6)? | If not, phase 1 needs magic-link or one-time-code sign-in: +8–14 h and possibly an SMS provider wait | User; first step of G02 | G02 scope |
| OD2 Is reschedule atomic, and is there an idempotency key (Q8)? | Decides D5 and D6; without an atomic reschedule a move can leave two appointments or none | G01 | G04/A11, G06 |
| OD3 Cut line: go live after 14 working days (Thu 5 Nov), or 11 days with each developer giving 4.8 focused h/day (plan summary)? | Phase 1 fits the hours, but not the 10-day calendar at the high end, and no scope cut tested fixes that | User | Go-live date |
| OD4 Salon policies and wording (Q10) | Notice window and refusal wording feed G04/A8 and the eval labels | Salon chain (W1) | G09 |
| OD5 Monthly spend figure (Q3) | Budget alert and daily allowance | User | G08/A4 |
| OD6 Region (Q11) | Model availability and data residency | User; G08/A3 | G08 |
