# System design: salon booking assistant (MVP)

Status: **draft**. Written in one pass without the user; every decision that
rests on an assumed answer below is **provisional** until the team confirms it.
Decisions and rationale live here; estimates, owners, capacity and the finish
range live in the [plan](../plans/salon-booking-assistant.md); goal scope and
acceptance live in the [tickets](../tickets/salon-booking-assistant/).

## Assumed answers

The user was not available. Each row is a question that would have been asked,
the answer assumed, and what depends on it.

| # | Question | Assumed answer | Decisions that depend on it |
| --- | --- | --- | --- |
| Q1 | When must the first useful version exist, and what then? | Given: production MVP within two weeks (10 working days), then continued. Phase 1 code is kept. | Phase split, plan |
| Q2 | How many focused hours per day can each developer give, and how familiar are they with ADK and GCP? | Three developers on this full time, about 5 focused hours a day each (8 h × ~0.6). Experienced in Python and in the booking API; new to ADK (×1.5 on estimates); have used GCP before. | Capacity, every estimate |
| Q3 | What can be spent on models and cloud? | A small startup allowance: about USD 300 a month for MVP traffic, with alerts at 50 % and 100 %. | D8, D10 |
| Q4 | Who uses it? | External customers of all five salons, signed in on the chain's existing website, English only. Salon staff keep using their existing tools. | D3, D9, G06, G10 |
| Q5 | Can our backend verify the website's customer login? | Yes: the website issues a signed token (JWT, JWKS endpoint) whose subject is the booking API's customer ID or maps to it 1:1. | D3, G05. If wrong, a guest/OTP flow (G15) moves into phase 1 and something else moves out |
| Q6 | What does the booking API support today? | REST + JSON, server API key, a staging environment, salon/service/stylist/availability reads, list-by-customer, create, cancel; it rejects double-booking of a slot. **Unknown:** idempotency keys, atomic reschedule, lookup by client reference. We own the API and can add these. | D4, D5, G01, G02 |
| Q7 | Cancellation and change policy (notice period, fees)? | The booking API enforces the policy and returns a rejection with a reason; no fees, deposits or payments in the MVP. | D2, G04 |
| Q8 | Does the booking API already notify customers (email/SMS) on create, move and cancel? | Yes; the assistant sends no messages of its own. | Security posture, D2 |
| Q9 | Region and privacy obligations? | Deploy in the booking API's region, which the team already knows (no outside decision); customer name and appointment history are personal data; the chain's privacy notice needs a line about the assistant, drafted by us and approved in W1. | D6, D7, W1 |
| Q10 | Who on the salon side approves go-live, on what evidence, and how long does it take? | The chain's operations manager, on a one-page description and the privacy wording (a staging demo offered, not required); 3–5 working days after asking (W1, requested day 1). If they require a staging demo first, go-live moves later (plan what-ifs). | G10 |
| Q11 | Who resolves an unknown or partial booking outcome? | A developer on rota during launch week, then the salon front desk using a runbook. | D4, G10 |
| Q12 | Channel? | Web chat only; no phone, SMS or WhatsApp in phase 1. | D9 |
| Q13 | Model provider preference? | Gemini on Vertex AI under the startup's GCP project. | D8 |
| Q14 | Expected traffic? | Up to a few hundred conversations a day across five salons; bursts on Monday mornings. | Budgets, D7 |
| Q15 | Is the two-week date fixed if the high estimate is reached? | Assumed: day 10 is the target and day 14 the latest acceptable go-live. The plan shows the what-ifs and asks. | Plan summary |
| Q16 | Who owns the customer website and its login? | We do (same team): adding our token audience, the same-origin `/assistant` route and the account-area link is our own work in G05 and G06, not an outside wait. | D3, D9, G05, G06 |
| Q17 | Is there a GCP project with billing and Vertex AI we can use? | Yes, the project the booking API runs in, or a sibling; enabling Vertex AI and access for three developers takes up to a day (W3, day 1). | D7, D8, G07, G08 |

## Purpose and constraints

**Journey (running example).** A returning customer of the Northside salon wants
to move their Thursday 17:00 colour appointment to Saturday morning. Today they
phone during opening hours and wait while reception checks the diary; out of
hours they cannot change anything. With the assistant they open chat on the
chain's website (already signed in), say "move my Thursday colour to Saturday
morning", see two Saturday slots with the same stylist as a card, tap
**Confirm** on one, and see the booking API's confirmation; Thursday is
released. Fixed constraints: the existing booking API is the only authority for
appointments; three developers; two weeks to production.

**What the model does and what code does.** The model interprets the request,
asks clarifying questions, calls read tools and *proposes* a booking, move or
cancellation. Code decides who the customer is, which appointments they may
touch, what was proposed (stored record), whether it is still valid, and
performs the write only after the customer presses Confirm. No model output is
ever a write.

**Outcome to improve (hypothesis, not measured).** Bookings and changes made
outside opening hours, and fewer reception phone calls, without more front-desk
corrections. Baseline: the booking API's current count of phone-made changes
per week (to be pulled in G10). Guardrail: operations needing manual
reconciliation and wrong-appointment complaints.

Non-goals for phase 1: payments or deposits, staff-facing assistant, waitlists,
other channels, languages other than English, recommendations.

Observed repository facts: the repository contains only the skills under
`.claude/`; no application code exists yet. All module paths below are
**proposed**.

## Delivery constraints, depth and deferred controls

| Scope-gate answer | Value |
| --- | --- |
| First useful version due, and after | 10 working days to production; continued (Q1) |
| People and hours | 3 developers, ~5 focused h/day, new to ADK (Q2) |
| Money | ~USD 300/month for models and cloud (Q3) |
| Users and what they read | External salon customers, signed in, using the chat on the website (Q4) |
| Data touched and effects allowed | Real personal data (name, appointment history); reversible writes visible to salon staff and the customer (book, move, cancel) |
| Delivery profile | **MVP**: first external users, real data, real writes; phase 1 fits the deadline, phase 2 is written |

Depth per concern:

| Concern | Depth now | Trigger that raises it |
| --- | --- | --- |
| Core judgment, measured | Build: labelled evaluation set run before launch (G07) | CI gate in phase 2 (G12) |
| Identity and per-customer scope | Build: verified website login; tools scoped in code (D3) | Guest booking requested (G15) |
| Secrets | Build: Secret Manager + service account, no keys in code | Rotation in phase 2 when a second key exists |
| External writes | Build: propose-then-confirm, durable operation record, idempotency (D2, D4) | Automatic reconciliation (G16) when unknowns > 1/week |
| Sensitive data | Build (minimal fields): tools return only needed fields; no message text in logs; sessions kept 30 days (D6) | Screening service when free-text notes carry PII (G18) |
| Prompt injection and agency | Build: the agent has no write path (D2); scope in code; 4 adversarial eval cases | Full suite and threat model (G14) |
| Budgets and loop limits | Build: `max_llm_calls`, per-customer daily allowance, kill switch (D10) | Shared budget when traffic > 1,000 conversations/day |
| Memory and retrieval | Sessions only; no long-term memory | "Book my usual" requests in feedback (later list) |
| Frontend | Build: minimal same-origin chat page (D9) | Streaming when median reply > 5 s (later list) |
| Hosting | Build: one Cloud Run service with revision rollback (D7) | — |
| Observability | Build: traces and token cost, content capture off (D11) | SLOs and alerts (G13) |
| Release engineering | Minimal: pinned model, prompt in repo, release record (G08) | Eval gate in CI (G12) |
| Performance and cost tuning | Defer | Measured latency or cost over target |

**Floor kept:** no secrets in code, prompts or logs; spend stop
(`RunConfig.max_llm_calls`, per-customer allowance, kill switch, billing alert);
no booking write without the customer pressing Confirm on the exact stored
proposal; personal data limited to what the journey needs and kept out of logs;
model ID pinned. No accepted risks.

**Who may use phase 1:** signed-in customers of the five salons, on their own
appointments only. Graduation conditions before a wider audience (guest users,
other channels, higher traffic) are the phase 2 goals in the plan.

| Deferred control | Why it waits | What would bring it forward |
| --- | --- | --- |
| Automatic reconciliation job | Unknown outcomes are rare at MVP volume; G04 reconciles on demand | More than one unknown outcome a week |
| Evaluation gate in CI | The set is new; first run sets the baseline | Second prompt or model change |
| SLOs and alerts | No baseline yet | One week of production traffic |
| Adversarial suite beyond 4 cases | The agent cannot write (D2) | Any new tool that reads free text and acts |
| Guest (not signed-in) booking | Needs OTP and abuse controls | Measured drop-off at the sign-in prompt |

Capacity, finish range and cut line: see the plan's summary.

## Guarantees and acceptance

| Invariant | Enforcing component and authority | Failure outcome | Verification |
| --- | --- | --- | --- |
| I1 A customer reads and changes only their own appointments | Gateway derives customer ID from verified token (D3); tools read it from trusted state; booking API list-by-customer is the authority | 401/404; nothing disclosed | G05/A2, G05/A3, G03/A2, G04/A2 |
| I2 No write without the customer confirming the exact stored proposal | Confirm endpoint in application code (D2); model has no write tool | Rejected confirm; no booking API call | G03/A1, G04/A1, G04/A5 |
| I3 One confirmed proposal causes at most one appointment change | Operation record keyed by proposal ID + booking API idempotency key (D4) | Same receipt returned on repeat | G04/A3, G02/A2 |
| I4 An uncertain write is never shown as success or failure | Operation state `unknown` until lookup by client reference settles it (D4) | "Checking with the salon" | G04/A6, G06/A3 |
| I5 A move never silently leaves two or zero appointments | Atomic reschedule, or book-then-cancel with `partial` state (D5) | Partial shown; runbook | G04/A7, G10/A4 |
| I6 Spend is bounded | `max_llm_calls`, per-customer allowance, kill switch (D10) | Friendly stop, no model call | G03/A4, G05/A4, G08/A4 |
| I7 No secrets or message text in logs | Logging config; Secret Manager | — | G02/A5, G05/A6, G08/A2 |

## Architecture and decisions

```text
Browser (website, signed in)
  │  same-origin chat page (D9)  ── JWT from website session
  ▼
Cloud Run service "booking-assistant" (D7), service account sa-assistant
  ├─ Gateway (FastAPI): verify JWT → customer_id; session ownership; allowance; kill switch (D3, D10)
  ├─ ADK Runner + one LlmAgent "booking_agent" (D1), model gemini-3.5-flash on Vertex AI (D8)
  │     tools: list_salons_and_services, find_availability, list_my_appointments,
  │            propose_booking, propose_move, propose_cancellation   (read or propose only)
  ├─ Confirm endpoint (ordinary code): recheck → execute → record operation (D2, D4)
  └─ BookingPort → HTTP adapter → existing Booking API (authority for appointments)
Cloud SQL PostgreSQL: ADK sessions, proposals, operations, allowances (D6)
Secret Manager: booking API key · Cloud Trace / Logging: spans and metrics, no content (D11)
```

Sequence for the journey: chat message → gateway verifies token, loads or
creates the customer's session, puts `customer_id`, salon timezones and "now
per salon" in session state → agent calls `list_my_appointments`,
`find_availability`, then `propose_move` → the tool stores a proposal (owner,
action, appointment ID, new slot, price, expiry 10 min) and returns it → the
reply carries the proposal card → customer presses Confirm → confirm endpoint
locks the proposal, rechecks owner, expiry and current appointment state,
inserts an operation `executing`, calls the booking API with
`Idempotency-Key = proposal_id` → records `succeeded`, `failed`, `unknown` or
`partial` → returns the receipt and writes it to session state for the next turn.

| ID | Requirement | Design choice | Reason | Tradeoff / alternative | Verification | Status |
| --- | --- | --- | --- | --- | --- | --- |
| D1 | Interpret free-text requests over a small capability set | One `LlmAgent` with six function tools; no sub-agents | One responsibility, one identity, one tool set; nothing to route | Sub-agents per action add routing errors and evaluation surface for no boundary | G03/A1, G07/A2 | Proposed |
| D2 | No write without the customer's approval of exact details (floor) | Model tools only create stored proposals; the write happens in a confirm endpoint the model cannot call, after a click bound to the proposal ID; recheck before execute | Takes the write leg away from the model; approval binds to stored details, not to chat text | One more endpoint and table; ADK `require_confirmation` was the alternative: shorter, but confirmation is model-mediated, experimental and has documented limitations (adk.dev/tools-custom/confirmation) | G04/A1, G04/A2, G04/A5 | Proposed |
| D3 | Customers see only their own appointments (I1) | Gateway verifies the website JWT (signature, issuer, audience, expiry via cached JWKS) and writes `customer_id` to session state; tools take no identity argument; session IDs checked against owner | Identity comes from code, never from the model or chat | Depends on Q5; asking for phone number in chat is not authentication | G05/A1–A3, G03/A2 | Provisional (Q5) |
| D4 | One confirmation, at most one change; honest uncertain outcomes (I3, I4) | Operation record per proposal (`executing → succeeded / failed / unknown / partial`), booking API `Idempotency-Key = proposal_id`, lookup by client reference to settle `unknown`; blind write retries forbidden | Survives double clicks, restarts and lost responses | Requires adding idempotency and lookup to our booking API if missing (G02) | G04/A3, G04/A6, G02/A2, G02/A3 | Provisional (Q6) |
| D5 | A move leaves exactly one appointment (I5) | Prefer an atomic reschedule endpoint on the booking API (add it in G02 if cheap); otherwise book-new-then-cancel-old with `partial` state and runbook | Atomic is simplest to reason about | Decided in G01 from the API's code | G01/A4, G04/A7 | Open (G01) |
| D6 | Conversations survive restarts and multiple instances; operations are durable | Cloud SQL PostgreSQL (smallest tier) for `DatabaseSessionService` and app tables, reached through the Cloud SQL Python Connector with IAM database authentication (no database password); sessions deleted after 30 days; operations kept 1 year | One managed store for both; transactions for proposal/operation state | A second database to run; Firestore or Vertex AI sessions were alternatives without SQL row locks | G05/A5, G04/A8, G08/A7 | Proposed |
| D7 | A public HTTPS endpoint with custom auth and confirm routes | One Cloud Run service (min 1 instance in business hours, max 3), region = booking API's region; previous revision kept for rollback | Custom routes and JWT verification fit Cloud Run; managed Agent Runtime would still need our gateway for confirm | We own the container and its patching | G08/A1, G08/A5 | Provisional (Q9) |
| D8 | Comparable, affordable model behaviour across the plan's horizon | `gemini-3.5-flash` on Vertex AI, pinned; low thinking; no `output_schema` (proposals are structured by tools, replies are prose) | Stable; Vertex retirement "2027-05-19 or later" per the lifecycle table in `adk-model-and-output-contracts` (checked 2026-10-08), beyond a ~6-month horizon | `gemini-3.8-flash` is newer and stable, but its Vertex retirement date is not in the table; evaluate it in phase 2 as a re-baseline. Re-check by 2027-03 | G03/A4, G07/A4 | Proposed |
| D9 | Customers use it on the website | Minimal same-origin chat page served by the service, request/response JSON (no streaming), proposal cards with Confirm/Decline, text rendered as plain text | Least frontend work; same-origin keeps the website session | No token streaming; AG-UI/CopilotKit deferred | G06/A1–A6 | Proposed |
| D10 | Spend stays bounded (floor) | `RunConfig.max_llm_calls = 10` per turn; 40 turns per customer per day in Postgres; env kill switch returning a "please call the salon" message; Cloud Billing alerts (notification only) | Enforced by the application before model calls | Allowance numbers are assumptions; tune after week 1 | G03/A4, G05/A4, G08/A4 | Proposed |
| D11 | See failures and cost without leaking content | ADK OpenTelemetry to Cloud Trace with message content capture off; structured logs with session, invocation, operation IDs, token counts; no message text | Lets an alert lead to a session without logging personal data | Debugging needs the stored session, not logs | G05/A6, G08/A3 | Proposed |
| D12 | Dates and times are right for each salon | Code puts each salon's timezone and current local date/time in session state; tools take salon ID and local ISO date/time; results carry local time and salon name | What the application knows belongs in code, not the prompt | — | G03/A1, G07/A1 | Proposed |

ADK version assumption: no version is installed; the specialists were checked
against **google-adk 2.8.0** (see `safe-api-tool-calls/references/compatibility.md`).
Confirming constructors against the chosen pin is acceptance item G03/A8.
`DatabaseSessionService`, `RunConfig.max_llm_calls` and OpenTelemetry content
gates must be checked against that pin before relying on them.

### Model-facing contracts

| Surface | Contract | Implementing skill and verification |
| --- | --- | --- |
| Instruction | One instruction file `prompts/booking_agent/instruction.md`: role, ask before guessing salon/service/stylist, always propose and never claim a change happened until the confirm result arrives in state, one proposal per appointment, policy rejections relayed. Identity, dates, limits and policy stay in code. | `adk-agent-instructions`; rendered-request test G03/A8 |
| Tools | Six function tools; reads return at most 10 items and truncate free text to 200 chars inside a `data` field; propose tools return a proposal object; every result has `status` and actionable errors; no identity parameters; tiers: read (4), propose (2, no effect); no write tier exposed | `adk-tool-interface-design`; G03/A2, G03/A5, G03/A7 |
| Output and model | Prose replies; proposals reach the UI from tool results, not model text; model `gemini-3.5-flash` pinned (D8) | `adk-model-and-output-contracts`; G03/A4 |

### Public JSON contract (for G06)

- `POST /api/chat {session_id?, message}` → `{session_id, reply_text, proposals: [{proposal_id, action, salon, service, stylist, start_local, end_local, price, expires_at, replaces?}], operations: [{operation_id, proposal_id, status, receipt?, reason?}]}`
- `POST /api/proposals/{id}/confirm` → `{operation_id, status: succeeded|failed|unknown|partial, receipt?, reason?}`
- `POST /api/proposals/{id}/decline` → `{status: declined}`
- `GET /api/operations/{id}` → current operation state (owner only)

## Data and authority

| Data / operation | Owner and scope | Writers / readers | Source and freshness | Lifetime / erasure |
| --- | --- | --- | --- | --- |
| Appointments, availability | Booking API | Booking API; assistant reads per customer | Authority; read live each turn | Booking API's policy |
| Customer identity | Website login | Website issues; gateway verifies | Token per request; JWKS cached ≤ 1 h | Not stored beyond session state |
| ADK sessions | Customer (by `customer_id`) | Runner writes; owner reads | Conversation only, never authority | 30 days, daily delete job (G05/A5) |
| Proposals | Customer | Propose tools write; confirm endpoint reads/updates | Snapshot at proposal time; rechecked at confirm | Expire after 10 min; kept with operations |
| Operations | Customer; developers/front desk for reconciliation | Confirm endpoint | Receipts from the booking API | 1 year |
| Allowance counters | Customer | Gateway | Per day | 7 days |

Identities: end customer (website JWT); workload `sa-assistant` (Vertex AI user,
Cloud SQL client, secret accessor for the booking API key only); booking API
credential is a server API key held in Secret Manager. The service account's
access to the booking API does not establish the customer's authority; I1 is
enforced in our code before every call.

### Security posture

| Agent | Private data | Untrusted content | Write or egress | Resolution |
| --- | --- | --- | --- | --- |
| `booking_agent` | The signed-in customer's own appointments | The customer's messages (the principal) and free-text fields from the booking API (stylist bios, appointment notes) | None: propose tools have no effect; replies go only to the same customer | Write leg removed (D2); scope in code (D3); free text truncated and placed in data fields (G03/A5); 4 adversarial eval cases (G07/A1) |

No code executor. No MCP or remote agents.

## Budgets and capacity

Per customer turn: expected 2–4 model calls, bounded at 10 (`max_llm_calls`);
2–3 booking API reads; at most one write, only from the confirm endpoint.
Assumed load (Q14): a few hundred conversations a day, ~4 turns each, i.e.
roughly 2,000–5,000 model calls a day at peak. Cost is symbolic until G07
measures tokens per turn: (calls/day × tokens/call × price) + Cloud SQL
smallest tier + Cloud Run min instance. Check against Q3 after G07 and again
after week 1. Billing alerts notify; the kill switch and allowance enforce.
Exhaustion: allowance → friendly 429 with salon phone number; kill switch →
same message, no model calls; confirm endpoint stays available so already
proposed changes can complete.

## Failure and recovery

Coverage grid, one row per external system:

| Integration | Unavailable or slow | Rejects the request | Write outcome unknown | Partial multi-step change | Credential expired or revoked | Rate limited or out of quota | Duplicate or concurrent request | Untrusted or malformed content |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Booking API | G03/A6, G04/A6 | G04/A4 | G04/A6 | G04/A7 | G02/A4, G04/A4 | G02/A4, G03/A6, G04/A4 | G04/A3, G02/A6 | G03/A5, G01/A3 |
| Website login (JWKS) | G05/A7 | G05/A2 | n/a: login is read only | n/a: no multi-step change | G05/A2, G05/A7 | G05/A7 | n/a: token checks are stateless | G05/A2 |
| Cloud SQL (sessions, proposals, operations) | G05/A9, G04/A10 | G04/A11 | G04/A6 | G04/A9 | G08/A7 | G05/A9 | G04/A3, G05/A10 | G03/A5, G07/A1 |
| Vertex AI model | G05/A8 | G05/A8 | n/a: model calls have no effects | G04/A5 | n/a: workload identity, no stored key | G05/A8 | G05/A10 | G03/A7, G07/A1 |

Action grid:

| Action | Over-broad or wrong target | Partially applied | Confirmation stale or changed | Outcome unknown | Repeated or concurrent |
| --- | --- | --- | --- | --- | --- |
| Book | G03/A7 | n/a: single booking API call | G04/A4 | G04/A6 | G04/A3 |
| Move | G03/A3 | G04/A7 | G04/A5 | G04/A6 | G04/A3 |
| Cancel | G03/A3 | n/a: single booking API call | G04/A5 | G04/A6 | G04/A3, G02/A2 |

Cross-cutting scenarios:

| Failure window | User-visible outcome | Retained state / possible effects | Safe next action and recovery owner |
| --- | --- | --- | --- |
| Booking API commits a move, response lost | "We're checking with the salon"; then the result | Operation `unknown`; appointment may have moved | Lookup by client reference (`proposal_id`); never a new key. Owner: confirm endpoint, then on-call dev (G04/A6) |
| Book-then-cancel move: new booked, cancel fails | "Your new time is booked; the old one is still held, the salon will release it" | Two appointments; operation `partial` | Front desk cancels the old one from the reconciliation list (G04/A7, G10/A4) |
| Customer double-clicks Confirm or opens two tabs | One receipt shown in both | One operation | Row lock on proposal (G04/A3, G06/A2) |
| Slot taken between proposal and confirm | "That time has just gone; here are others" | Proposal `failed`; no appointment | Agent re-searches (G04/A4) |
| Process restart mid-confirm | Status poll shows final or unknown | Operation `executing` treated as unknown | Reconcile by lookup (G04/A6, G04/A8) |
| Model unavailable or loops | "Temporarily unavailable, call the salon" | No proposal or a harmless expired one | Retry later; SDK retries only (G05/A8, G03/A4) |
| Spend or abuse | Allowance / kill-switch message | Nothing | Operator flips switch (G05/A4, G08/A4) |
| Rollback | Previous revision serves | Sessions and operations unchanged (schema changes additive only) | Traffic shift to previous revision (G08/A5) |

## Verification and implementation handoff

- **Offline deterministic:** scripted-model Runner tests and the in-memory
  booking fake (G01–G05): ownership, proposal-only tools, idempotency, lost
  response, partial move, restart, allowance, log content.
- **Local integration:** local PostgreSQL restart tests (G04/A8, G05/A5);
  HTTP adapter against a local or staging booking API (G02); real agent,
  confirm service and adapter wired into the gateway (G09).
- **Bounded live:** evaluation set against the pinned model with the fake API
  and a cost limit (G07); staging end-to-end with the real staging booking API
  (G10/A1).
- **Release/operation:** staging deploy, rollback and kill-switch checks (G08);
  integrated staging build (G09); go-live (G10); first-week review of every
  operation (G11).

Benefit measurement (hypothesis): out-of-hours changes and phone calls per
week before and after launch, with manual reconciliations as the guardrail
(G10/A5).

Observability and release at MVP depth: SLIs proposed for phase 2 (G13):
confirmed operations succeeded / confirmed, unknown outcomes per week, tool
error rate by tool, tokens per completed booking. One telemetry owner (the
service), content capture off (D11). Release record per deploy: image digest,
prompt file hash, model ID, ADK version, tool schema hash (G08/A6). Rollback
unit: the Cloud Run revision; previous revision kept.

Implementation routes, goals, owners and acceptance: see the
[plan](../plans/salon-booking-assistant.md) and
[tickets](../tickets/salon-booking-assistant/).

## Open decisions

| Question or assumption | Why it changes the design | Owner / evidence needed | What it blocks |
| --- | --- | --- | --- |
| Q5 website token verifiable by our backend | Without it, I1 needs a new login flow (G15) in phase 1 | Website owner; a sample token and JWKS URL | G05 |
| Q6 booking API idempotency, reschedule, lookup by reference | Decides how much of G02 is API work and D5 | G01 reads the API code | G02, G04 move branch |
| Q15 is day 10 fixed? | High-end estimate finishes after day 10 | User | Cut line in the plan |
| Q2 focused hours and ADK familiarity | Every estimate and the finish range | User | Plan |
| Privacy notice wording (Q9) and sign-off evidence (Q10) | Go-live date | Chain operations manager (W1) | G10 |
| Q16, Q17 website ownership and GCP project | If wrong, outside waits appear before G05, G06, G07, G08 | User | G05–G08 |
| Model choice D8 vs gemini-3.8-flash | Quality vs documented lifecycle | G07 results; phase 2 comparison | None in phase 1 |
