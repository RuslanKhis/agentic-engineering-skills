# System design: salon booking assistant (MVP)

Status: **draft**. The user was not available, so every scope-gate answer below is
assumed (table A). Decisions that depend on an assumption are marked
*provisional*. No decision here has been accepted by the user yet.

Decisions and their rationale live here. Estimates, owners, capacity, finish
range and cut line live in the plan:
[docs/plans/salon-booking-assistant.md](../plans/salon-booking-assistant.md).
Goal scope and acceptance live in the tickets under
[docs/tickets/salon-booking-assistant/](../tickets/salon-booking-assistant/).

## Summary

A web chat assistant on the salon chain's website. It lets customers of five
salons book, move and cancel appointments through the team's existing booking
API. One ADK `LlmAgent` interprets the request and calls narrow function tools
for reads. It never commits a write itself. A write tool only creates a
**pending operation** that is shown to the customer as a confirmation card. The
booking API is called only when the customer clicks Confirm, and that click goes
through an ordinary HTTP route, outside the model, which re-checks ownership and
the slot (D2). Each confirmed operation carries a durable ID that is used as the
idempotency key (D3). Before a move or cancel, code checks that the customer owns
the booking (D4). Hosting is one Cloud Run service with a small Cloud SQL
Postgres database for sessions, operations and allowances (D5, D6).

## Purpose and constraints

**Journey (running example).** On Sunday evening, Maya wants a women's cut at the
Northside salon on Thursday after 17:00. Today she can only phone during opening
hours or fill in a form that staff confirm the next day. With the assistant she
types "cut at Northside Thursday after 5", sees three free slots, picks 17:30,
gives her name and phone, and gets a card saying "Women's cut, Northside, Thu 16
Oct 17:30, with Sam, 45 min. Confirm?" She clicks Confirm and sees the
booking reference. The booking API's existing confirmation SMS or email reaches
her (assumption A10). On Wednesday she returns and writes "move my Thursday
appointment to Friday". She gives her booking reference and phone, picks a new
slot and confirms.

**Friction today:** booking only works by phone during opening hours, or through
a form that staff handle by hand. **Intended outcome:** customers complete
book, move and cancel at any hour without staff, and the front desk sees no more
corrections than before.

| Kind | Facts |
| --- | --- |
| Confirmed by the user | 3 developers; MVP; book, move, cancel through *our existing booking API*; five salons; ship within two weeks, then keep improving; ADK; design only in this session |
| Observed in the repository | Empty repository, so the design is greenfield; no ADK version installed. The specialist skills were checked against `google-adk==2.8.0` (their `references/compatibility.md`) |
| Assumed (table A) | Everything else, including users, channel, API capabilities, hours and money |

**What the model contributes:** it reads free text ("after 5", "my usual
stylist", "move it to Friday"), chooses which tool to call, picks out the
arguments and writes the reply. **What code controls:** salon and service IDs
come from the API catalogue; code converts time zones, checks ownership and
availability, decides confirmation and commits, allocates idempotency keys,
enforces budgets and filters what is logged.

**Non-goals for the MVP:** answering general FAQs (prices beyond the catalogue,
parking and similar), payments or deposits, staff-side use, remembering
customer preferences across visits, channels other than the website,
languages other than the salons' primary language.

## Assumed answers

The user could not answer questions. Each row would have been asked, and the
decisions in the last column are provisional until it is confirmed.

| # | Question | Assumed answer | Decisions that depend on it |
| --- | --- | --- | --- |
| A1 | Hours each developer gives, and familiarity with ADK and GCP | All three full time on this. About 5 focused hours a day, because a startup interrupts. New to ADK, so a ×1.5 multiplier applies. Has used GCP before (the booking API is assumed to run there), so no extra setup day | Plan capacity, every estimate |
| A2 | Model and cloud budget | Small: about USD 150 a month for the pilot, with a billing alert at 50/90/100 % | D7, D8 |
| A3 | Who uses it and through what channel | The salons' own customers (external people), through a chat widget embedded in the chain's existing website. Salon owners judge the pilot | D5, profile |
| A4 | Data touched and effects | Customer name, phone, email and appointment details (personal data). The effects are creating, moving and cancelling real appointments that staff and customers rely on (reversible, but visible to outside people) | Floor, D2, D4, D9 |
| A5 | Does the booking API accept an idempotency key or client operation ID on writes, and can a booking be looked up by it? | Unknown. Assumed that the team owns the API and can add an `Idempotency-Key` header with a lookup in G01 if it is missing (≤ 1 day) | D3, I3 |
| A6 | Is there a staging instance of the booking API with test salons? | Yes | G01, G06, G09 |
| A7 | How does the website identify customers? Is there a customer login? | No login. Customers are known by phone and email in the booking API. Bookings have a reference that the confirmation message carries | D4 |
| A8 | Business rules (cancellation window, minimum notice, double-booking) | The booking API enforces them and returns a rejection code. The assistant passes the reason on and does not reimplement it | D2, failure grid |
| A9 | Time zones | All five salons are in one time zone. Each salon record still carries its zone | Tool contract |
| A10 | Does the booking API already notify customers about bookings, moves and cancellations? | Yes, by SMS or email. The assistant sends no messages itself | D2, floor |
| A11 | Privacy notice and data retention expected by the salon owner | The website privacy notice gains a paragraph about the assistant. Conversations are kept 30 days. The salon owner approves this before go-live | D9, wait W1 |
| A12 | Where it may run | GCP: a new project for the assistant, Vertex AI in a region near the salons | D6, D7 |

## Delivery constraints, depth and deferred controls

| Scope-gate answer | Value |
| --- | --- |
| First useful version due, and after it | Within 10 working days of the start; continued afterwards (user) |
| People and hours | 3 developers (user). Hours and familiarity are assumed in A1. The same team runs it afterwards |
| Money | A2 (assumed) |
| Users or judge, and what they read | External salon customers using the running service. Salon owners judge the pilot (A3) |
| Data touched and effects allowed | Personal data. Real appointment writes, each confirmed by the customer it belongs to (A4) |
| Delivery profile | **MVP or pilot.** First external users make real, reversible writes. Phase 1 code is kept and extended, not thrown away |

| Concern | Depth now (phase 1) | Trigger that raises it |
| --- | --- | --- |
| Core judgment, measured | Build: 25 labelled conversations run with a live model before launch (G08, G09) | CI gate in phase 2 (G14) |
| User identity and per-user scope | Build: verified booking ownership for move and cancel (D4), in G10 and G11, the first phase 2 goals, because move and cancel sit past the phase 1 cut line (see the plan) | A booking taken over by someone else, or a pilot complaint, brings forward OTP (G13) |
| Secrets and credentials | Build: workload identity; Secret Manager for the booking API key; nothing in code or prompts | Rotation in phase 2 |
| External writes | Build: customer confirmation, durable operation, idempotent commit, uncertain-outcome reconciliation (D2, D3) | — |
| Sensitive data | Build, minimal form: field minimisation, no content or phone numbers in logs, 30-day retention (D9) | Model Armor or SDP screening when free-text notes are written to the API, or real abuse is seen |
| Prompt injection and agency | Build: the agent cannot commit, and ownership is checked in code (D2, D4) | Adversarial suite in phase 2 (G16) |
| Budgets and loop limits | Build: per-invocation, per-session and per-IP limits, an instance cap and a kill switch (D8) | Shared budget reservations when traffic exceeds the pilot |
| Memory and retrieval | Sessions only. No long-term memory and no RAG. The catalogue comes from the API | Customers ask for "my usual stylist" in > 10 % of conversations |
| Frontend | Build: a small embeddable widget with completed JSON replies (D5) | Streaming if measured time to reply exceeds 6 s at p75 |
| Hosting | Build: Cloud Run, staging and production revisions, rollback to the previous revision | — |
| Observability | **Below the MVP default (minimal now):** structured logs with session and operation IDs, tool status, token counts per turn, and an alert on uncertain operations. Cloud Trace waits for phase 2 (G15) because of the two-week date | First incident that logs cannot attribute, or the move to all five salons, whichever comes first |
| Release engineering | Minimal: pinned model, prompt in git, unit tests in CI, a manual evaluation run before launch | CI evaluation gate (G14) before the second prompt or model change after launch |
| Performance and cost tuning | Defer | Measured p75 turn time > 6 s or cost per completed booking > USD 0.05 |

**Floor kept:** no secrets in source, prompts or logs. A spend stop:
`RunConfig.max_llm_calls`, because the application owns the Runner, plus the
budget alert from A2 and a kill switch. Nothing reaches the booking API unless
the customer whose appointment it is confirms the exact details (I1). Personal
data is limited to what the journey needs and kept out of logs (I7). The model
ID is pinned (D7).

**Accepted risks:** none accepted by the user yet. Proposed for acceptance:
**R1**, that ownership checked by reference plus phone (D4) is weaker than a
one-time code. Owner: Dev A. It ends when G13 ships, or at the first report of
misuse.

**Who may use it, on what data:** customers of one pilot salon after launch (G09),
then all five salons (G12). Real customer data. Before
it reaches more users (paid ads, other channels, more chains), these
graduation conditions must hold: G13 (OTP), G14 (CI evaluation gate), G15
(traces and SLO alerts), G16 (adversarial suite).

## Guarantees and acceptance

| ID | Invariant | Enforcing component and authoritative evidence | Failure outcome | Planned verification |
| --- | --- | --- | --- | --- |
| I1 | No booking API write happens without a Confirm click on that exact pending operation, before it expires (10 min) | `POST /operations/{op_id}/confirm` in the chat API. The operation row's payload hash and expiry are checked. The model has no commit tool | The customer sees "expired, please ask again"; no write | Offline: a scripted model calls every write tool repeatedly and the fake API records 0 writes. A confirm with an altered payload or after expiry is refused (G03, G04) |
| I2 | Move and cancel act only on a booking verified in this session | The verification function records verified references in `session.state["app:verified_refs"]`, and only that code path writes this key. The operation service re-checks it at confirm time | The agent asks for the reference and phone again; no write | Offline: a request to cancel an unverified reference is refused at proposal and at confirm. The model trying to set the state key directly has no effect (G10, G11) |
| I3 | One confirmed operation produces at most one booking API effect | `op_id` (UUIDv4, allocated at proposal) is sent as `Idempotency-Key`. The unique row in `operations` is claimed atomically with `pending→committing` | A duplicate click returns the first result | Offline: a double confirm and a concurrent confirm give 1 fake API call. A retry after a lost response gives 1 effect (G03). The provider replay contract is confirmed in G01 (A5) |
| I4 | A write whose outcome is uncertain is never shown as done or as failed | The operation service sets `uncertain`, then looks the operation up by `op_id`. If that lookup fails it raises an alert, and the front desk reconciles | The customer sees "we're checking this; you'll get the usual SMS if it went through, or call the salon" | Offline: a fake timeout after commit gives `uncertain` and a lookup resolves it. A failing lookup triggers the alert log (G07) |
| I5 | A customer sees booking details only for verified references | Read tools for existing bookings take a reference only from `app:verified_refs` | Refusal with a prompt to verify | Offline: an attempt to read an unverified reference is refused (G10) |
| I6 | Spend per conversation and in total is bounded | `RunConfig.max_llm_calls`, per-session turn cap and per-IP session cap in Postgres, Cloud Run max instances, a kill switch, and a billing alert (notification only) | The widget shows "please call the salon" with the number | Offline: limits refuse with the designed message. Staging: the kill switch flips within 1 minute (G05, G06) |
| I7 | No message text, phone or email in logs; conversations deleted after 30 days | A log filter in the chat API. A Cloud Scheduler job deletes sessions and operations older than 30 days | — | Offline: a log-capture test with a known phone number finds none. Staging: the deletion job removes a backdated session (G05, G06) |

**Benefit hypothesis (unmeasured):** share of booking intents completed by the
assistant without staff. Guardrails: the front-desk correction rate and the
no-show rate for assistant bookings compared with phone bookings. The baseline
is unknown, so the pilot week records it (G09). Plain text: this is a
hypothesis, not a promise.

## Architecture and decisions

```text
Browser widget ──HTTPS JSON──▶ Chat API (FastAPI on Cloud Run, owns ADK Runner)
                                 │  session cookie → ADK session (DatabaseSessionService)
                                 │  admission: per-IP / per-session limits, kill switch
                                 ├─▶ LlmAgent "booking_assistant" ──▶ Vertex AI Gemini (pinned)
                                 │      tools: list_salons_and_services, find_slots,
                                 │             verify_booking, get_my_booking,
                                 │             propose_booking / propose_move / propose_cancel
                                 │                  └─ create pending operation (no API write)
                                 ├─ POST /operations/{op_id}/confirm  (not reachable by the model)
                                 │      OperationService: check owner + payload hash + expiry
                                 │      → BookingClient.write(Idempotency-Key = op_id)
                                 ▼
                      Cloud SQL Postgres: adk sessions · operations · allowances
                                 │
                      Existing booking API (staging / production) — authoritative for
                      salons, services, staff, slots, bookings and customer notifications
```

Trust boundaries: the browser and everything the model writes are untrusted.
The chat API, the operation service and the booking client are trusted code.
Identities: an anonymous browser session (server-generated ID in a signed,
HttpOnly cookie), a verified booking reference (D4), the Cloud Run service
account (talks to Vertex AI, Cloud SQL and Secret Manager), and the booking API
key for the assistant's own client.

| ID | Requirement | Design choice | Reason | Tradeoff / alternative | Verification | Status |
| --- | --- | --- | --- | --- | --- | --- |
| D1 | Understand free-text booking requests and call a few capabilities | **One `LlmAgent`** with 7 function tools that we write ourselves, and no sub-agents | No distinct responsibility, credentials or context would justify more agents. Function tools give exactly the interface we write | Rejected: one agent per intent, which adds routing errors without a boundary. Rejected: an OpenAPI toolset over the booking API, which would expose every endpoint and the API's own descriptions to the model | The captured model request shows 7 declarations under a byte budget. Tool selection on the evaluation set (G08) | proposed |
| D2 | A real appointment changes only with the customer's explicit consent to the exact details | Write tools return a **pending operation** (op_id, a confirmation card in a fixed schema, expiry). The commit happens in `POST /operations/{op_id}/confirm` from the widget button, which re-checks ownership, the slot and the payload hash | The model's proposal, the customer's confirmation and backend authorisation are three separate steps, and the model cannot reach the commit | Rejected: ADK native tool confirmation (`require_confirmation`). It keeps approval inside the model loop, and its [known limitations](https://adk.dev/tools-custom/confirmation/#known-limitations) must be checked against the chosen session service. Our route costs one table and one endpoint | I1 tests | proposed |
| D3 | A double click, a retry or a lost response must not double-book | **Durable operation row** (`op_id`, kind, canonical payload, payload hash, owner session, status `pending/committing/done/rejected/uncertain/expired`, API result). `op_id` is the API idempotency key. Reconciliation looks the operation up by `op_id` | Retries and duplicates refer to the same business operation | Needs idempotency support in the booking API (A5, checked in G01). Without it the fallback is a lookup by customer, slot and time window before any retry, which is weaker | I3, I4 tests | provisional (A5) |
| D4 | Only the booking's owner can view, move or cancel it | `verify_booking(reference, phone)`: code calls the API and compares the normalised phone with the one on file. On a match it adds the reference to `app:verified_refs`. 5 failures per session and 10 per reference per day lock it out | Works without customer login (A7). The model passes claimed values and code decides | Weaker than a one-time code: anyone who has both the reference and the phone number can act (R1). OTP is G13. New bookings need no verification. Fake bookings are limited by I6 and by the API's existing confirmation SMS | I2, I5 tests | provisional (A7, R1) |
| D5 | Customers chat from the website; the confirmation must be trustworthy | **FastAPI chat API** owns the Runner. `POST /chat` returns completed JSON `{messages[], card?, status}`. The card is rendered from the tool result, never from model text. The widget is one script tag. Turns overlapping in one session get 409 | Owning the Runner makes `RunConfig` limits apply. Completed JSON is enough for 1–3 s replies and avoids streaming failure modes | No streaming yet (Later). Rejected: `adk web` / `adk api_server`, which give no control over admission, cookies or the confirm route | Offline API tests: card fields equal the stored operation; an overlapping turn gets 409 | proposed |
| D6 | Conversations survive a restart and multiple instances; operations are durable | **Cloud SQL for PostgreSQL** (smallest shared-core tier) holds `DatabaseSessionService` tables, `operations` and `allowances`. Local runs use SQLite | One transactional store gives an atomic claim on operations and shared counters | Rejected: in-memory sessions, which break when Cloud Run uses several instances. Rejected: Agent Platform sessions plus Firestore, which mean two stores and no shared transaction. Cloud SQL costs a fixed monthly fee (price to be checked in G06) | Staging: restart the service mid-conversation and the conversation continues | provisional (A12) |
| D7 | Predictable behaviour at small cost | A Gemini **Flash-tier model on Vertex AI**, with the ID pinned from the dated lifecycle table in `adk-model-and-output-contracts` (`assets/model-lifecycle-*.json`) in G02. Low temperature. No failover in the MVP | Short tool-calling turns don't need a larger tier. Vertex keeps data in a GCP project | The ID is not chosen here because the lifecycle table was not available in this session. A model retiring within 6 months is designed in as a migration (Later) | The release manifest records the ID, with no alias | **open** (model ID) |
| D8 | Bounded spend and an operator stop | `max_llm_calls=8` per invocation, 30 turns per session, 20 new sessions per IP per day, Cloud Run `max-instances=3`, kill switch (`ASSISTANT_ENABLED` config, read every request), and a billing budget alert at A2 | Admission is enforced by the application; a billing alert only notifies | The numbers are provisional, set before any measurement. Real users who hit a limit are sent to the phone | I6 tests | provisional (A2) |
| D9 | Personal data is minimised and not leaked | Tools return only the fields the reply needs: a customer's name and phone only from their own verified booking. A log filter drops message bodies and phone and email patterns. 30-day deletion. Vertex AI used under the project's data terms | Cheapest controls that keep the floor (A4) | No content screening (Model Armor or SDP) in the MVP, see the depth table. Phone numbers do enter model context because the customer types them | I7 tests | provisional (A11) |
| D10 | Launch safely within two weeks | Staging against the booking API's staging instance → pilot at one salon (G09) → all five (G12). Rollback means routing traffic to the previous Cloud Run revision plus the kill switch | Limits the blast radius to one salon while the baseline is measured | Slower roll-out to all five salons | Staging checklist in G09 | proposed |

### Model-facing contracts

| Surface | Contract | Implementing skill and verification |
| --- | --- | --- |
| Instruction | Scope: book, move and cancel at the five salons. Always choose slots from `find_slots`. Never claim a booking is done; say "please confirm on the card". Out-of-scope questions get the salon's phone number. The date, salon list and customer verification state are injected from code, not invented | `adk-agent-instructions`: a rendered-request test (G02, G04) |
| Tools (7) | `list_salons_and_services()`, `find_slots(salon_id, service_id, date_from, date_to, time_after?, time_before?, staff_id?)` returning ≤ 10 slots, `verify_booking(reference, phone)`, `get_my_booking(reference)`, `propose_booking(slot_id, name, phone, email?)`, `propose_move(reference, new_slot_id)`, `propose_cancel(reference)`. Each returns `{status: ok/needs_input/not_allowed/unavailable/error, ...}` with actionable messages. Tiers: read for the first four. The `propose_*` tools are writes to our own store only. The booking API write is reached only through the confirm route | `adk-tool-interface-design`: a declaration dump and its byte size (G02, G04, G07) |
| Output | Free-text reply. The confirmation card comes from the tool result, so there is no `output_schema` | `adk-model-and-output-contracts`: pins the model ID only (G02) |

## Data and authority

| Data / operation | Owner and scope | Writers / readers | Source and freshness | Lifetime / erasure |
| --- | --- | --- | --- | --- |
| Salons, services, staff, slots | Booking API (authoritative) | API / tools | Read live on each call. Salon and service lists cached for 10 min | Not stored |
| Bookings | Booking API (authoritative) | Confirm route via `BookingClient` / verified tools | Live | Booking API's own retention |
| ADK session (events, state) | Anonymous browser session (cookie) | Runner / Runner | — | 30 days, then deleted |
| `app:verified_refs` | That session | `verify_booking` code only / tools, operation service | Re-checked at confirm | With the session |
| Operations | That session; the business operation | Propose tools, confirm route / confirm route, reconciler, front-desk runbook | Status from API receipts | 30 days |
| Allowances | Per session, per IP | Admission middleware | — | 2 days |

**Security posture.** The agent holds private data (verified bookings),
reads content from the customer, who acts for themselves, and from the booking
API (staff-written free text such as service descriptions), and it can create
pending operations. The structure breaks the dangerous path: the agent has
no booking API write and no egress beyond our own API, commits need a human
click (D2), and ownership is checked in code (D4). An injected instruction in
a service description can at most make the agent *propose* something, which
the customer sees and must confirm. Phase 1 has no code execution. Free-text
notes to the API are not supported, so the agent writes no text that staff read.

## Budgets and capacity

The workload is unknown. Assumed for the pilot: ≤ 200 conversations a day across
five salons, about 6 turns each, and 1–3 model calls per turn (capped at 8). The
cost per conversation is symbolic: ≈ 6 turns × 2 calls × (≈ 4k input + 0.3k
output tokens) × the pinned model's prices. Those prices are checked in G02
and recorded with the date. No price is asserted here. Fixed cost: the smallest
Cloud SQL instance plus Cloud Run at minimum 0 instances. Latency target
(provisional): a complete reply within 6 s at p75, measured in G09. Same
conversation: one turn at a time (409 on overlap).

## Failure and recovery

| Integration | Unavailable or slow | Rejects the request | Write outcome unknown | Partial multi-step change | Credential expired or revoked | Rate limited or out of quota | Duplicate or concurrent request | Untrusted or malformed content |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Booking API, reads | 5 s timeout, 1 retry; the tool returns `unavailable` and the agent offers the phone number (G01) | `not_allowed` or `needs_input` with the API reason (G01) | n/a: read only | n/a: single call | Alert. The tool returns `unavailable` (G01, G06) | Same as unavailable; no retry storm (G01) | n/a: idempotent reads | The client validates the schema; unknown fields are dropped; staff text is treated as data (G01) |
| Booking API, writes | Commit 10 s deadline, no blind retry. → `uncertain`, then lookup (G03) | `rejected` with the reason (slot taken, policy window); the card offers alternatives (G03, G04) | `uncertain` → lookup by `op_id` → resolve, or alert plus front-desk runbook (G07, G09) | A move is a single API update. If the API only offers cancel plus book, it becomes a two-step operation with saga rows (open decision O3) | As unavailable. Alert (G06) | As unavailable. The operation stays `pending` until expiry, so the customer may retry the same op (G03) | The atomic claim on `op_id` means one call (G03) | The response is validated. An unexpected payload → `uncertain` (G03) |
| Vertex AI Gemini | ADK retry default, plus the turn deadline (20 s) → "please try again or call" (G02, G05) | A safety block or 4xx → a generic apology and the phone number (G02) | n/a: no external effect | n/a | Workload identity. On failure → alert (G06) | Quota → the same message. `max_llm_calls` caps fan-out (G02, G05) | The 409 overlap rule (G05) | Prose only. The model cannot commit. A proposal with invalid arguments is rejected by tool validation (G04, G07) |
| Cloud SQL | Health check fails → 503 "please call" and no model call (G05, G06) | n/a | The operation claim is transactional. A commit to the API before the DB records the result → `committing` rows older than 1 min are reconciled by `op_id` (G07) | n/a | Workload identity (G06) | The connection pool is bounded (G06) | Unique `op_id` and row lock (G03) | n/a: our own schema |
| Browser / widget | n/a | Bad JSON gets 400 (G05) | A confirm click whose response is lost: the widget polls `GET /operations/{op_id}` (G05) | n/a | A cookie that expired or was tampered with starts a new session; old operations are not reachable (G05) | Per-IP limit (G05) | Double click → the same `op_id` result (G03, G05) | All input is length-capped. Card fields come from the server, never from model text (G05) |

| Failure window | User-visible outcome | Retained state / possible effects | Safe next action and recovery owner |
| --- | --- | --- | --- |
| The slot is taken between the proposal and the confirm | "That time was just taken", with 3 new slots | Operation `rejected`; no effect | The customer chooses again. Recovery is automatic |
| The API commits but the reply is lost | "We're checking…", then done or "call the salon" | Operation `uncertain`; the booking may exist | The reconciler looks it up by `op_id`. Otherwise the front desk follows the runbook (G07). The customer is told not to book again |
| The customer confirms after the move proposal, but the original booking was cancelled by staff meanwhile | "That appointment has changed. Please call" | `rejected`; no effect | The confirm route re-checks the original booking |
| Kill switch on during an active conversation | The next turn shows the phone number. Pending operations can still be confirmed or looked up | Pending operations expire | Operator (on call: Dev C) |
| A service description contains "cancel all bookings" | Nothing beyond a possible odd proposal, which the customer must confirm | None | The adversarial suite in G16 asserts it |
| Model retirement announced | No change for users | — | Planned migration (Later), re-baselined on the G08 evaluation set |
| Rollback | The previous revision serves traffic. Pending operations survive in the DB | The operations schema must stay backwards compatible within phase 1 | Dev C. Additive migrations only |

## Verification and implementation handoff

- **Offline (every goal):** pytest against the in-memory fake booking API, with
  a scripted model where the decision is not under test. Asserts on fake API
  call counts are the evidence for I1 to I5.
- **Local integration:** a real Postgres in Docker for claim and concurrency
  tests (G03). A process restart during a conversation (G05).
- **Bounded live:** the evaluation run with the pinned model, ≤ 25
  conversations × 3 repeats, capped at USD 5 (G08, G09). Contract tests against
  booking API staging (G01).
- **Hosted:** a staging checklist and a pilot at one salon (G09).
- **Observability (minimal, phase 1):** structured logs with `session_id`,
  `invocation_id`, `op_id`, tool name and status, model tokens per turn. Log
  alerts on `operation.uncertain` and on tool error rate. Traces wait for G15.
- **Release bundle (minimal):** Cloud Run revision, git SHA (prompt in git),
  model ID, booking API base URL and secret version, recorded in
  `release.json` at deploy time (G06).

Plan and goals: [docs/plans/salon-booking-assistant.md](../plans/salon-booking-assistant.md).
Proposed module layout (greenfield, not yet verified against ADK 2.8.0):
`app/agent.py` (agent factory), `app/tools/*.py`, `app/booking_client.py`
(+ `fake_booking_api.py`), `app/operations.py`, `app/api.py` (FastAPI),
`web/widget.js`, `tests/`, `evals/`.

## Open decisions

| ID | Question or assumption | Why it changes the design | Owner / evidence needed | What it blocks |
| --- | --- | --- | --- | --- |
| O1 | Booking API idempotency and lookup by operation ID (A5) | Without them, I3 rests on a weaker lookup by slot | Dev A reads the API code in G01 | G03 detail, not its start |
| O2 | Pinned Gemini model ID and its retirement date (D7) | Cost, behaviour and the migration date | G02, from the lifecycle table in `adk-model-and-output-contracts` | Nothing before G02 |
| O3 | Does the API have an atomic "move" (update), or only cancel plus book? | A two-step move needs saga handling and a partial-failure row | G01 | G11 scope |
| O4 | Is ownership by reference plus phone acceptable for the pilot (R1)? | Otherwise OTP (G13) moves into phase 1 and something else moves out | User / salon owner | G10, G11 |
| O5 | Assumed answers A1 to A12 | Hours, budget and channel resize the plan | User | Plan dates |
