# System design: salon booking assistant (MVP)

Status: **draft**. Written in one pass without the user; every row of the
Assumed answers table below is unconfirmed, and decisions that depend on one are
marked *provisional*. Nothing here is user-accepted yet.

Decisions and their rationale live here. Estimates, owners, the finish range
and the cut line live in the [plan](../plans/salon-booking-assistant.md);
goal scope and acceptance live in the
[tickets](../tickets/salon-booking-assistant/).

## Assumed answers

| # | Question I would have asked | Assumed answer | Decisions that depend on it |
| --- | --- | --- | --- |
| Q1 | When must the first useful version exist, and is it continued? | 10 working days from 2026-10-15 (live by 2026-10-28); continued afterwards, so phase 1 code is kept | Phase cut, D-all kept form |
| Q2 | Who builds it, hours each, ADK/GCP familiarity? Who runs it? | Three developers, full time on this for the two weeks, about 6 focused hours a day each; comfortable with Python and basic GCP, new to ADK (estimates ×1.5); the same three run it | Plan capacity, owners |
| Q3 | Money for models and cloud? | Small: about A$500 a month for model plus cloud during the pilot, with a budget alert; no committed spend | D8, model tier |
| Q4 | Who uses it and who judges it? | Existing customers of the five salons who already have an account on the chain's booking website; the chain's operations manager judges the pilot | D3, D6, W1 |
| Q5 | What data does it touch, what can it change? | Real personal data (name, phone, email, appointment history); creates, moves and cancels real appointments. No payments or deposits through the API in the MVP | Floor, D4, D5, D9 |
| Q6 | Does the booking API have a staging environment and idempotency keys? | We own it; a staging copy exists. Idempotency-key support is unknown; G01 finds out, and because we own the API we can add it | D5 |
| Q7 | How do customers sign in today? | The website's login issues a token our backend can verify (JWT with a published key set). If not, email one-time codes through the booking API, which moves G03 by about a day | D3 |
| Q8 | Does the API move an appointment atomically? | Unknown. Design covers both: atomic reschedule, or book-new-then-cancel-old | D5, F-row "partial move" |
| Q9 | Which channel? | A chat widget on the existing signed-in website pages. No SMS, WhatsApp or phone | D6 |
| Q10 | Where must data stay? | Australia: Cloud Run and Cloud SQL in `australia-southeast1`; the Vertex AI model location still needs checking (OD2) | D7, D2 |
| Q11 | What is the cancellation and change policy? | Changes and cancellations through chat allowed until 24 hours before the start; inside 24 hours the assistant gives the salon's phone number. Configurable, confirmed in W1 | D5, G05 |
| Q12 | Languages? | English only | D2 instruction |
| Q13 | What happens when the assistant cannot help? | Show the salon's phone number; no live hand-off to staff in the MVP | D6 |
| Q14 | Who signs off the go-live, and the use of customer data with a model provider? | The chain's operations manager; requested on day 1 (W1, 3 to 5 working days) | G09 |

## Purpose and constraints

**Journey (running example).** Maya, a signed-in customer of the Fitzroy salon,
types "can I move my cut with Sam on Thursday to sometime Saturday morning?".
Today she phones the salon during opening hours or rebooks herself in a
multi-step web form; staff spend phone time on routine changes. The assistant
finds her Thursday appointment, shows Saturday-morning slots with Sam, and when
she picks 10:30 shows a card "Move: Cut with Sam, Fitzroy, Thu 22 Oct 14:00 →
Sat 24 Oct 10:30. Confirm?". She taps Confirm; the booking API changes the
appointment once, and the card shows the confirmed result from the API.

**Fixed constraints (observed from the request):** ADK in Python; the existing
booking API is the system of record and the only writer of appointments; five
salons; MVP within two weeks; continued afterwards. The repository is empty
apart from the skills, so every module named below is *proposed*.

**What the model decides and what code controls.** The model interprets the
request, asks for missing details, chooses which read tool to call and drafts a
proposal (salon, service, stylist, start time, or which appointment). Code owns
the customer's identity, today's date and salon time zones, validation of every
argument against the API, the confirmation card's content, the decision to
execute, idempotency, policy (24-hour window) and the wording of results.

**Outcome to improve (hypothesis, unmeasured):** share of booking changes done
without a phone call, without more corrections by staff. Baseline: salon phone
log for one week before launch (G09 records it if the chain can supply it).

## Delivery constraints, depth and deferred controls

Profile: **MVP or pilot**, because real outside customers act on real
appointments; first external users, learning what they need.

| Concern | Depth now | Trigger that raises it |
| --- | --- | --- |
| Core judgment end to end, measured | Build: 20 to 25 labelled conversations run before launch (G07) | Phase 2 puts them in CI (G10) |
| Customer identity and per-customer scope | Build (D3, G03) | Guest browsing (G12) |
| Secrets and credentials | Build: Secret Manager, dedicated service account (G08) | Rotation when staff turnover or an incident occurs |
| External writes | Build: confirmation in code, idempotent create, reconciliation (D4, D5) | Payments or deposits added → full replay review |
| Sensitive data | Build: allow-listed tool fields, no content in logs (D9) | A second channel, analytics export, or a complaint |
| Prompt injection and agency | Build: free-text fields removed from tool results; model cannot execute writes (D4, Security posture) | Adversarial suite in phase 2 (G13) |
| Budgets and loop limits | Build: `max_llm_calls` per turn and a per-customer daily allowance (D8) | Shared budgets if traffic exceeds pilot estimate |
| Memory and retrieval | Minimal: ADK sessions only, no long-term memory | Customers ask for "my usual" (later) |
| Frontend | Build: JSON API and a small widget, no streaming (D6) | Measured time to first answer above 4 s (G14) |
| Hosting | Build: one Cloud Run service, previous revision kept for rollback (D7) | — |
| Observability | Minimal in phase 1: traces and token counts without content, an operations-status log; SLOs in phase 2 (G11) | First week of pilot traffic |
| Release engineering | Minimal: pinned model and ADK versions, unit tests in CI; evaluation in CI in phase 2 (G10) | Second prompt change after launch |
| Performance and cost tuning | Defer | Measured latency or cost above target |

**Floor kept:** no secrets in source, prompts, logs or documents; spend stop
(`RunConfig.max_llm_calls` per turn, per-customer daily allowance, project
budget alert); no appointment is created, moved or cancelled without the
customer pressing Confirm on a card built by code; real personal data limited to
the signed-in customer's own records and kept out of logs; model ID pinned.
Accepted risks: none yet.

**Who may use it:** signed-in customers of the five salons, on their own
appointments. **Graduation conditions** before guest users, another channel or
more salons: evaluation gate in CI (G10), SLOs and alerting on failed or
uncertain operations (G11), adversarial suite passing (G13).

## Guarantees and acceptance

| ID | Invariant | Enforcing component and authoritative evidence | Failure outcome | Planned verification |
| --- | --- | --- | --- | --- |
| I1 | A customer reads and changes only their own appointments | API middleware derives `customer_id` from the verified token (D3); tools and executor take it from trusted state, never from model arguments; the booking API's own customer filter | 403 / "I can't find that appointment"; no read or write | Cross-customer tests in G03 and G05: forged appointment ID and forged session ID both refused |
| I2 | No booking change happens without a confirmation bound to its exact details | Confirm route executes only a stored proposal whose hash matches the card shown; model holds no write tool (D4) | Changed or expired proposal is refused; customer sees "details changed, please check again" | G04: scripted model calls every tool; booking API fake records zero writes until confirm |
| I3 | One confirmation produces at most one appointment change | Operation record keyed by proposal ID; idempotency key sent to the booking API; uncertain outcome reconciled by lookup before any new attempt (D5) | Card shows "checking…" then the reconciled result | G04: double-click, retry after timeout, lost response after commit → one appointment |
| I4 | The confirmed result the customer sees comes from the booking API, not from model text | Card status rendered from the operation record, which holds the API's receipt (D4) | "We could not confirm this change; please call the salon on …" | G04/G06: API returns error after model said "done" → card shows failure |
| I5 | Changes inside 24 hours are refused in code (Q11) | Policy check in the executor before calling the API, with salon time zone | Message with the salon's phone number | G05: 23 h 59 m case refused, 24 h 01 m accepted |
| I6 | Spend per customer and per turn is bounded | `max_llm_calls` on `RunConfig`; daily allowance counter in Cloud SQL checked before each turn (D8) | "You've reached today's limit; call the salon" | G06: allowance exhausted → no model call made |

## Architecture and decisions

```text
Browser (salon website, signed in)
   │ token
   ▼
Cloud Run: booking-assistant (FastAPI)
   ├─ auth middleware ── verifies token (D3) → customer_id in trusted session state
   ├─ POST /chat ── allowance check (D8) → ADK Runner(App: LlmAgent "booking_assistant")
   │                    tools: list_salons_and_services, find_availability,
   │                           list_my_appointments  (read)
   │                           propose_booking, propose_move, propose_cancel (draft only)
   ├─ POST /proposals/{id}/confirm ── executor (D4, D5) → booking API (write)
   └─ GET  /operations/{id}  ── status from operation record
   │
   ├─ Cloud SQL Postgres: ADK sessions, proposals, operations, allowances
   ├─ Vertex AI: gemini-3.8-flash (pinned)
   └─ Booking API (ours; staging and production)
```

| ID | Requirement | Design choice | Reason | Tradeoff / alternative | Verification |
| --- | --- | --- | --- | --- | --- |
| D1 | Book, move, cancel from free text (confirmed) | **One `LlmAgent`** with six narrow function tools; no sub-agents | One journey, one tool set, one identity; sub-agents would add routing without a distinct responsibility | Less separation if a second domain (product sales) arrives; revisit then | G07 evaluation: tool choice correct on labelled cases |
| D2 | Behaviour stable across days; small budget (Q3) | Model **`gemini-3.8-flash` on Vertex AI**, pinned; latest stable in the lifecycle table (checked 2026-10-08), no shutdown announced. Avoid `gemini-3.6-flash` (Vertex retirement 2026-11-19) and 2.5 models (2026-10-20). *Provisional* on OD2 (location) | Flash tier fits short tool-calling turns and the budget; Vertex keeps data under the GCP project's terms | A pro model may resolve ambiguous dates better; escalate only if G07 shows errors a flash model cannot fix | G01 confirms availability in the chosen location; G07 measures quality |
| D3 | Only the account holder acts on their appointments (I1) | **Reuse the website login** (*provisional*, Q7): middleware verifies the token's signature, issuer, audience and expiry, derives `customer_id`, writes it to session state at session creation and checks session ownership on every request | Enforcement in code before the model runs; the model never chooses whose data to read | Requires a verifiable token from the website; fallback (email codes) costs about a day more | G03 cross-customer and expired-token tests |
| D4 | No change without the customer's approval (I2, I4) | **Propose-then-confirm outside the model.** `propose_*` tools validate against the API (slot still free, appointment belongs to customer) and store a proposal with a content hash; code renders the card from the proposal; the customer's Confirm click calls `/proposals/{id}/confirm`, which re-checks ownership, policy and slot, then executes | The model cannot reach the write path, so injected text or a mistaken turn cannot change a booking; the card shows what will actually be sent | Custom route and card instead of ADK's built-in tool confirmation (which has documented limitations and keeps the write tool in the model's reach) | G04 scripted-model test: zero writes before confirm; changed proposal refused |
| D5 | One confirmation, one change (I3); partial moves visible | **Durable operation record** in Postgres keyed by proposal ID (`pending → sent → confirmed / failed / uncertain`), idempotency key on create/move/cancel calls; on timeout, look up the customer's appointments for that slot before any retry; move uses the API's atomic reschedule if present, else book-new then cancel-old with both steps on the record | Survives retries, double clicks and restarts; a lost response is reconciled, never blindly resent | Needs idempotency support in our API (G01 checks; we can add it) and a reconcile query | G04/G05 fault-injection tests on the booking API fake |
| D6 | Customers use the existing website (Q9) | **JSON request/response API plus a small embeddable widget**, no streaming; confirmation card and operation status are typed JSON, not model prose | Simplest browser contract; cards come from records | No progressive text; acceptable for short turns, revisit on measured latency (G14) | G06 widget test against fakes; G09 end to end on staging |
| D7 | Ship in two weeks with a small team (Q1, Q2) | **One Cloud Run service** (min instances 0, max 5) in `australia-southeast1`; **Cloud SQL Postgres** (smallest shared-core) for ADK `DatabaseSessionService`, proposals, operations and allowances | Sessions and operations survive restarts and multiple instances; one database for everything the app owns | Cloud SQL is a fixed monthly cost and setup time; Agent Runtime would host sessions but the operation record still needs a store | G08 restart test: session and operation survive a new revision |
| D8 | Bounded spend (I6, Q3) | `RunConfig.max_llm_calls = 12` per turn (assumption); **per-customer daily allowance** of 40 turns (assumption) in Postgres, checked before the Runner starts; project budget alert at 50/90/100 % (alert only, not a cap) | Admission in code is the real stop; billing alerts only observe | Legitimate heavy users may hit the limit; tuned after the pilot | G06 allowance test; G08 budget alert exists |
| D9 | Personal data kept to need (Q5) | Tool results are **allow-listed fields** (no free-text notes, no other customers, no staff phone numbers); logs and traces record IDs and statuses, never message text or names; ADK content capture off in telemetry | Minimises what reaches the model, storage and logs | Harder debugging; a session can still be read from Cloud SQL by the team for incidents | G02 result-shape test; G08 log sample check |
| D10 | Interfaces stable while three people work in parallel | **G01 fixes the contracts first**: booking client protocol and fake, proposal and operation models, card JSON schema, module layout | Lets G02, G03, G04 and G08 start the same day | One goal of up-front work before visible progress | G01 acceptance |

Versions: ADK working assumption **google-adk 2.8.0** (the version the
specialist skills were checked against); G01 confirms the pin and the
`DatabaseSessionService`, `RunConfig.max_llm_calls` and `App` interfaces
against it. Model lifecycle source: `adk-model-and-output-contracts`
`assets/model-lifecycle-2026-10-01.json`, `checked_on` 2026-10-08. Vertex
retires a stable model about 12 months after release (skill compatibility
note), so expect a `gemini-3.8-flash` migration around September 2027 (later
list).

### Model-facing contracts

| Surface | Contract | Implementing skill and verification |
| --- | --- | --- |
| Instruction | Interprets booking requests for the signed-in customer; asks one clarifying question at a time; always uses tools for times and availability; never claims a change happened (the card says that). Today's date, salon list and time zones are injected from state by code | `adk-agent-instructions`; rendered-request test (G02) |
| Tools (6, all function tools) | Read: `list_salons_and_services`, `find_availability(salon_id, service_id, stylist_id?, date_from, date_to)`, `list_my_appointments(from_date?)`. Draft: `propose_booking`, `propose_move(appointment_id, new_start, stylist_id?)`, `propose_cancel(appointment_id)`. No customer ID parameter anywhere. Results: `{status, ...}` bounded to 20 slots / 10 appointments, actionable errors | `adk-tool-interface-design`; declaration dump and size (G02) |
| Output, model | Plain text replies; no `output_schema` (cards come from code). Pinned `gemini-3.8-flash`, default thinking, temperature left at the model default | `adk-model-and-output-contracts`; G07 |

## Data and authority

| Data / operation | Owner and scope | Writers / readers | Source and freshness | Lifetime / erasure |
| --- | --- | --- | --- | --- |
| Appointments, customers, availability | Booking API (system of record) | Writes only via executor (D4); reads via tools, filtered by `customer_id` | Live from API on every tool call; re-checked at confirm | Booking system's retention |
| ADK session and events | Assistant, per customer | Runner; team for incident review | Current conversation | 30 days (assumption), then deleted by a scheduled job (later list) |
| Proposal | Assistant, per customer, per session | `propose_*` tools write; confirm route reads | Expires 10 minutes after creation (assumption) | With session |
| Operation record | Assistant, per customer | Executor; status route; staff reconciliation | Holds the API receipt | 1 year (assumption, audit) |
| Allowance counter | Assistant, per customer per day | Chat route | Daily reset at salon midnight | 7 days |

Identities: **customer** (verified token → `customer_id`), **session** (ADK
session ID, owned by one customer), **business operation** (proposal ID, also
the idempotency key), **workload** (Cloud Run service account with Vertex AI
user, Cloud SQL client and secret accessor for the booking API credential).
The booking API credential is a service credential; the API call carries
`customer_id` from trusted state, and the API must check the appointment
belongs to it (G01 confirms the API does).

### Security posture

| Agent | Private data | Untrusted content | Write or egress | Resolution |
| --- | --- | --- | --- | --- |
| booking_assistant | Own appointments and profile | Customer's own chat text; booking API free-text fields (notes, stylist bios) | Draft proposals only | Free-text API fields removed from results (D9); execution only through the confirm route outside the model (D4); scope from verified token (D3) |

Tool tiers: read (3 tools), draft (3 tools, no external effect), write
(executor, not a tool). Code execution: none. Adversarial cases in G07 (phase 1:
three cases) and the full suite in G13.

## Budgets and capacity

Workload assumption (labelled): five salons, about 50 chat conversations a day
in the pilot, peaks of 5 concurrent. Per turn: 1 to 4 model calls (bounded at
12), 1 to 3 booking API calls; per confirmation: 1 to 3 API calls. Cost is
symbolic until G09 measures tokens per completed booking: about 4k input and
300 output tokens per model call is the planning assumption; no prices were
looked up in this session (no network), so G08 checks current Vertex pricing
for the chosen location. Latency target (provisional): complete reply within
6 s at p90; G14 measures.

## Failure and recovery

| Integration | Unavailable or slow | Rejects the request | Write outcome unknown | Partial multi-step change | Credential expired or revoked | Rate limited or out of quota | Duplicate or concurrent request | Untrusted or malformed content |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Booking API (read) | 5 s timeout, one retry; tool returns `unavailable`, agent says to try later or call (G02) | Tool returns actionable error (G02) | n/a: read only | n/a: single call | Executor and tools fail closed; alert (G08) | Same as unavailable (G02) | n/a: reads are safe | Allow-listed fields; unexpected shape → `unavailable` (G02) |
| Booking API (write) | 10 s deadline; record `uncertain`, reconcile by lookup (G04) | Record `failed` with reason; card shows it (G04) | Reconcile by lookup with idempotency key before any retry (G04, F2) | Move without atomic reschedule: F3 (G05) | Fail closed, `failed`, card says call the salon (G04) | No automatic retry for writes beyond reconcile (G04) | Proposal-ID key; second confirm returns the existing operation (G04) | Receipt validated against proposal; mismatch → `uncertain` (G04) |
| Website login / token keys | Cached key set; if unavailable and cache stale, refuse sign-in (G03) | 401, widget asks to sign in (G03) | n/a: read only | n/a | Expired token → 401 (G03) | n/a: key fetch is cached | n/a | Malformed token → 401 (G03) |
| Vertex AI model | Model timeout → "having trouble, try again or call"; no state change (G06) | Same message; logged (G06) | n/a: model has no write path (D4) | n/a | Service account lacks access → fails at deploy smoke test (G08) | 429 → ADK retry bounded inside `max_llm_calls`, then same message (G06) | Per-session turn lock: second message while one runs is rejected (G06) | Malformed tool call arguments → tool validation error (G02); model text never renders as a card (D6) |
| Cloud SQL | Chat and confirm return 503; no API write without an operation record (G04) | n/a | Record written before API call; restart leaves `sent` → reconcile on read (G04) | Operation and proposal in one transaction (G04) | Fails at startup readiness (G08) | Connection pool bound (G08) | Unique key on proposal ID (G04) | n/a: own schema |

Cross-cutting scenarios:

| ID | Failure window | User-visible outcome | Retained state / possible effects | Safe next action and recovery owner |
| --- | --- | --- | --- | --- |
| F1 | Model says "booked!" but no confirm happened | No card status "confirmed", so nothing claims success; instruction forbids the claim | Proposal only | Customer confirms or abandons; G07 case checks the wording |
| F2 | API commits, response lost, customer clicks again | "Checking…", then confirmed once | Operation `uncertain` → lookup finds appointment → `confirmed` | Executor reconciles on next status read; if lookup is unavailable, stays `uncertain` and appears in the staff list (G09 runbook) |
| F3 | Move by book-then-cancel: new booked, cancel of old fails | "Your new time is booked; we could not cancel the old one. The salon will sort it out" | Both appointments exist; operation `partial` | Staff reconciliation from the operations list (G09 runbook); never auto-cancel the new one |
| F4 | Slot taken between proposal and confirm | "That time was just taken; here are nearby times" | Proposal `stale`, no write | Customer picks again |
| F5 | Customer edits session ID or appointment ID in requests | 403 / not found | Nothing | None (I1) |
| F6 | Injected text in a stylist bio asks the model to cancel everything | Field never reaches the model; even if it did, no write without Confirm | Nothing | G07 adversarial case |
| F7 | Rollback to the previous revision | Chats continue; schema changes are additive only in phase 1 | Sessions and operations intact | Release owner (G09 runbook) |
| F8 | Allowance exhausted or spend alert fires | "Daily limit reached; call the salon"; operator can set allowance to 0 to stop all model calls | Counters | Operator stop is a config value outside the agent (G06) |

## Verification and implementation handoff

Offline deterministic checks (G02 to G06) run against the booking API fake and a
scripted model; local integration (G08) against a real Postgres and a restart;
bounded live checks (G09) on staging, then one real test appointment per salon
on a designated test stylist, created and cancelled with the operations
manager's consent. Evaluation (G07) runs the labelled conversations against the
pinned model before launch. Release unit in phase 1: image digest, prompt file
hash, model ID, ADK version, recorded in a release note per deploy (G08).
Observability in phase 1: OpenTelemetry traces and token counts without content
to Cloud Trace, structured logs of operation status changes (G08).

Implementation routes, owners, estimates and the cut line are in the
[plan](../plans/salon-booking-assistant.md).

## Open decisions

| ID | Question or assumption | Why it changes the design | Owner / evidence needed | What it blocks |
| --- | --- | --- | --- | --- |
| OD1 | Does the website login give us a verifiable token (Q7)? | Decides D3 and G03's size | Team, in G01 | G03 |
| OD2 | Is `gemini-3.8-flash` served from an Australian Vertex location, and is the chain fine with model processing outside Australia if not? | Data residency and D2 | G01 lookup; operations manager in W1 | G08 production config |
| OD3 | Idempotency keys and atomic reschedule in the booking API (Q6, Q8) | D5 complexity; G04/G05 size | Team, in G01 | G04, G05 |
| OD4 | 24-hour policy, test stylist for live checks, go-live date (Q11, Q14) | I5 and G09 | Operations manager, W1 | G09 |
| OD5 | Allowance and call-limit numbers (D8), session retention (30 days) | Cost and privacy | Team after G07 token measurements | None in phase 1 |
