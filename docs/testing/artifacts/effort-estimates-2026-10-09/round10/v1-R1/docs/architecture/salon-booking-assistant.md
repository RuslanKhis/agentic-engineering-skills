# System design: salon booking assistant

Status: **draft**, revision 2 (2026-10-14). The salon owners moved the launch
from 10 to 8 working days with the same three developers; that date is a user
decision. Everything else still rests on the assumed answers A1 to A15, and
decisions that depend on them are **provisional** until the team confirms. No
other decision is user-accepted yet.

Decisions and their rationale live here. The plan
([docs/plans/salon-booking-assistant.md](../plans/salon-booking-assistant.md))
holds estimates, owners, capacity, finish range, cut line and the list of what
this revision removed or weakened; the tickets hold each goal's scope and
acceptance.

## Assumed answers

| ID | Question I would have asked | Assumed answer | Decisions that depend on it |
| --- | --- | --- | --- |
| A1 | When must the first useful version exist, and what happens after? | **User-stated (2026-10-14): 8 working days** (was 10). Assumed: day 1 is the first implementation day, nothing has been built yet, and the launch is the pilot salon going live (G11). Kept and improved afterwards | Phase 1 code is the kept form (D1–D12); the cut package A11–A15 |
| A2 | How many hours each, and how familiar with ADK and GCP? | Three developers, about 5 focused hours a day each on this project; strong in Python and web; new to ADK; some GCP. ×1.5 on every estimate. No overtime to absorb the shorter date | Plan capacity and estimates |
| A3 | What budget is there for models and cloud? | About USD 300 a month during the MVP | D2, D9 |
| A4 | How do customers sign in today? | The salon website has customer accounts issued by the booking system. Its login yields a signed token (JWT) whose subject is the booking-system customer ID, and our backend can verify it. Fallback if it is not verifiable: a one-time email code, about 6–10 extra hours | D3; blocks G03 |
| A5 | Does booking involve deposits, prepayment or no-show fees? | No. No money moves through the assistant | D4 depth; "Later" list in the plan |
| A6 | What does the booking API offer for writes? | REST with list salons/services/stylists, availability search, create, reschedule, cancel and list-by-customer. An idempotency-key header is **unknown** (G01 finds out). Phase 1 uses create and cancel only; reschedule is used by G06 in phase 2 | D5; shapes G04a, G06 |
| A7 | Who enforces the cancellation and late-change policy? | The booking API rejects changes inside the policy window (assumed 24 hours) with a distinct error. Our confirm endpoint rechecks it before dispatch | G05 |
| A8 | Who uses it, and through which channel? | External salon customers, through a chat widget on the existing salon website (web only). In phase 1 every chat turn needs sign-in (A12). The chain owner judges the pilot | D3, D7, D8 |
| A9 | Languages and time zones? | English only. All five salons share one time zone, but the time zone is read per salon from the API anyway | D12 |
| A10 | What data is touched? | Personal data: customer name, contact details on file and appointment history. No health or payment data. Tools expose only what the journey needs | D10 |
| A11 | At launch, may "move my appointment" be two confirmed steps (book the new time, then cancel the old one) instead of one reschedule? | Yes. The single-step reschedule is G06 in phase 2 | D1, D4, §7 two-step row; G05, G08, G11 |
| A12 | May the chat require sign-in at launch, with anonymous availability browsing later? | Yes. Visitors keep browsing availability on the existing website meanwhile | D3, D9; G03, G07; G22 |
| A13 | Is a 20-case pre-launch evaluation (every category kept) enough evidence for the pilot, growing to 30 or more in phase 2? | Yes, with the same launch threshold | §2 core judgment; G08, G11, G14 |
| A14 | May Cloud Trace export wait until after launch, with structured logs (IDs, statuses, token counts) during the first pilot week? | Yes. The pinned ADK 2.8.0 lacks the span-retention fix noted for 2.10.0 anyway | §2 observability, I6; G09, G16 |
| A15 | May the 30-day session deletion job be built after launch? | Yes, provided it runs before the first session is 30 days old (launch day + 30 calendar days) | D10, §5; G21 |

## 1. Purpose and constraints

**Journey (running example).** Maya has a Saturday 10:00 cut with Sam at the
Riverside salon and needs to move it to next week. Today she phones the salon,
during opening hours only, and often waits while the receptionist serves a
client. The website can book, but she does not find a way to move an
appointment, so she cancels and rebooks or gives up. With the assistant, she
signs in on the salon site, types "move my Saturday haircut to Thursday
afternoon next week". The assistant shows her Saturday appointment and three
free Thursday slots with Sam. She taps a proposal showing *Riverside · Women's
cut · Sam · Thu 23 Oct 14:30*, presses **Confirm**, and sees the new booking
taken from the booking API's receipt. The assistant then proposes *Cancel
Riverside · Women's cut · Sam · Sat 18 Oct 10:00*; she presses **Confirm**
again and sees the cancellation receipt. (Phase 1 shape, A11. From G06 in
phase 2 the move is one proposal and one reschedule call.)

**Model versus code.** The model interprets the request: which appointment,
which service, which stylist, and what "Thursday afternoon" means. It chooses
read tools and proposes a change. Code owns everything else: who the customer
is, which appointments they may touch, whether an appointment may still be
changed, dates resolved to absolute times, policy checks, the confirmation
click, the write to the booking API and the displayed result.

**Non-goals for the MVP:** payments, SMS or WhatsApp, staff-facing features,
reminders, waitlists, languages beyond English, and remembered preferences.
Deferred out of phase 1 by the 8-day date: single-step move (G06), anonymous
chat (G22).

**Outcome to improve (hypothesis, unmeasured):** the share of book, move and
cancel requests that customers complete without phoning, out of hours
especially. Guardrail: support calls about wrong bookings must not go up.
Baseline: the salons' current phone-change volume, which the salon owner
supplies during the first pilot week. G20 measures completion and the plan's
phase 2 tracks it.

**Existing systems (assumed, not inspected):** the booking API and its
database are the authority for appointments and availability. The salon
website and its customer login are assumed as in A4. No application code
exists in this repository yet.

## 2. Delivery constraints, depth and deferred controls

| Scope-gate answer | Value |
| --- | --- |
| First useful version due | **8 working days** (A1, user-stated); continued |
| People and hours | 3 developers × ~5 focused h/day, new to ADK (A2); the same team runs it afterwards |
| Money | ~USD 300/month for models and cloud (A3) |
| Users and judge | Signed-in external customers via the web widget; the chain owner judges the pilot (A8, A12) |
| Data and effects | Customer personal data; writes that are reversible but visible to real people (bookings in staff calendars, confirmation messages sent by the booking system); no money (A5, A10) |
| Delivery profile | **MVP or pilot:** first external users, real bookings, the team must see failures and cost |

| Concern | Depth now | Trigger that raises it |
| --- | --- | --- |
| Core judgment, measured | Build: 20-case evaluation set, run locally and before launch (G08, G11) (A13) | Phase 2: 30 or more cases and a gate in CI (G14) |
| Identity and per-customer scope | Build: verified login token on every chat turn, own appointments only (G03) | Anonymous browsing (G22) when visitors ask the assistant before signing in |
| Secrets | Build: workload identity and Secret Manager (G09) | Rotation when the booking-API key policy requires it |
| External writes | Build: click-confirmed proposals, idempotent dispatch, reconcile-before-retry (G04a, G04, G05); a move is two confirmed operations (A11) | Single-step move (G06) in phase 2; automated reconciliation (G18) when more than one uncertain operation per week |
| Sensitive data | Build: projected tool results, no message content in logs. 30-day session deletion job (G21) due before launch day + 30 (A15) | Erasure tooling (G17) before the second salon month or the first erasure request |
| Prompt injection and agency | Build at MVP depth: the structure in §5 (model has no executing write tool) | Adversarial suite (G15) in phase 2 |
| Budgets and loops | Build: `max_llm_calls`, per-customer turn caps, no model call without a verified customer, kill switch (G02, G07, G09), billing budget alert (G10) | Shared allowance when traffic exceeds one instance |
| Memory | Conversation sessions only | Repeat customers restating preferences |
| Frontend | Build: plain widget with proposal cards and a Confirm button (G07) | Slot cards (G13) in phase 2 |
| Hosting | Build: one Cloud Run service per environment with rollback to the previous revision (G09) | — |
| Observability | **Minimal** (A14): structured logs carrying IDs, tool names, statuses and token counts per turn; content capture off (G09) | Cloud Trace export, SLOs and alerts (G16) after one pilot week, or as soon as the ADK pin includes the span-retention fix |
| Release engineering | Build: pinned versions, release manifest, deterministic tests and scripted evaluation in CI (G09) | Live evaluation gate (G14) |
| Performance tuning | Defer | Measured p95 latency or cost per booking above target |

**Floor kept (unchanged by revision 2):** no secrets in code, prompts or logs.
Spend stops through `max_llm_calls`, per-customer caps, an operator kill switch
and a billing budget alert, which alerts only and does not cap. No booking
change happens without the customer's click on an exact proposal. Personal
data is limited to the signed-in customer's own records and stays out of logs.
The model ID is pinned. No accepted risks.

**Who may use it, when:** from G11 only signed-in customers of the pilot
salon, with staff informed (W2). **Graduation to all five salons (G12):** at
least 3 days of the pilot with no wrong-booking incident, no uncertain
operation left unresolved, baselines recorded (G20), the deletion job live
(G21), and the G08 evaluation at or above the G11 threshold.

| Deferred control | Why it waits | What would bring it forward |
| --- | --- | --- |
| Live evaluation gate in CI and 30+ cases (G14) | Prompt changes are rare in the pilot week; G11 runs evaluation by hand on 20 cases | First prompt or model change after launch |
| Adversarial suite (G15) | §5 structure blocks the harmful actions in code; the suite adds evidence, not the control | Any new tool, new channel, or a free-text field added to tool results |
| Cloud Trace export, SLOs and alerts (G16) | No baseline until the pilot runs; logs carry the IDs needed to find a session; pinned ADK lacks the span-retention fix | One week of pilot traffic, an incident the logs cannot attribute, or an ADK pin ≥ 2.10.0 |
| Session deletion job (G21) | No session reaches 30 days old before launch day + 30 | **Hard date:** launch day + 30 calendar days; it is a graduation condition |
| Erasure tooling (G17) | Erasure can be done by hand at pilot scale | First erasure request or second salon month |

Capacity, finish range and cut line: see the plan's summary.

## 3. Guarantees and acceptance

| ID | Invariant | Enforcing component and evidence | Failure outcome | Planned verification |
| --- | --- | --- | --- | --- |
| I1 | A customer reads or cancels only their own appointments, and books only for themselves | `customer_id` comes from the verified token (G03), is written to session state by the chat API, and is read by tools and by the confirm endpoint. It is never a model argument. Booking API calls filter by it, and the confirm endpoint checks the appointment's owner again | Not-found response, no write | Two fixture customers: B's appointment ID offered by a scripted model is refused at the tool and at confirm (G04a, G05, G07) |
| I2 | No booking change happens without the customer clicking Confirm on a proposal showing salon, service, stylist and absolute start time | The model holds only `propose_*` tools, which write a pending proposal. Only `POST /operations/{id}/confirm` dispatches, and it needs the session's verified customer. A two-step move is two proposals and two clicks | Proposal stays pending and expires after 10 minutes | A scripted model calls every tool, and the fake booking API records zero writes until confirm (G04a, G04) |
| I3 | One confirmed proposal causes at most one booking change | The operation record (unique `operation_id`) moves through a state machine under a row lock; the ID is sent as the idempotency key if the API supports one (G01). An `uncertain` write is reconciled by lookup, never by fresh dispatch | Customer sees "checking with the salon" and later the result | Double click, concurrent confirms, and a lost response after a provider commit all end with one booking (G04a); forced uncertain booking on staging (G10) |
| I4 | A shown confirmation reflects the booking API's receipt | The widget renders status from the operation record. Model text never states that a change succeeded | Model text claiming success is not shown as a status card | Model says "booked" while the API fails: the card shows failure (G07) |
| I5 | Spend and work are bounded per turn, per customer and overall | `RunConfig.max_llm_calls=8` (G02); a verified customer is required before any model call and turn caps live in chat API middleware (G07); kill switch (G09) | Polite refusal with the salon's phone number; 401 without a valid token | Unit tests at each cap and for the unauthenticated path; kill-switch drill in G10 |
| I6 | Message content and contact details do not reach logs or traces | Telemetry content capture is off; logs carry IDs, tool names, statuses and token counts; tool results are projected (D10). No trace exporter is enabled in phase 1 (A14) | — | Captured log export from a test run contains no fixture names or phone numbers (G09); the span export is checked when G16 enables it |

## 4. Architecture and decisions

```text
 Browser (salon site)          Cloud Run: booking-assistant (FastAPI)                Booking API (existing)
 ┌─────────────┐  JSON   ┌───────────────────────────────────────────────┐  HTTPS  ┌──────────────┐
 │ chat widget │────────▶│ auth middleware → customer_id (trusted; 401   │         │ availability │
 │  [Confirm]  │         │   without a valid token)                       │         │ bookings     │
 └─────┬───────┘         │ caps + kill switch                             │         │ (authority)  │
       │                 │ Runner ─ LlmAgent (gemini-3.8-flash, Vertex)   │────────▶│              │
       │                 │   read tools ─────────────────────────────────┼────────▶│              │
       │ POST confirm    │   propose_* tools → operations table (pending) │         │              │
       └────────────────▶│ confirm endpoint → dispatcher ─────────────────┼────────▶│ create /     │
                         └──────────────┬─────────────────────────────────┘         │ cancel       │
                                        │ Cloud SQL Postgres: ADK sessions,         └──────────────┘
                                        │ operations, turn counters
```

| ID | Requirement | Design choice | Reason | Tradeoff / alternative | Verification | Status |
| --- | --- | --- | --- | --- | --- | --- |
| D1 | Interpret booking requests using a small set of capabilities | One `LlmAgent`, no sub-agents. Read tools: `list_salons_and_services`, `find_free_slots`, `list_my_appointments` (each appointment carries a code-computed `changeable` flag from the A7 policy). Proposal tools in phase 1: `propose_booking`, `propose_cancellation`. Five function tools. A move is `propose_booking` for the new slot, then `propose_cancellation` for the old one, offered only for a `changeable` appointment (A11). `propose_move` arrives with G06 | One judgment owner and a small tool set; nothing here needs a separate context or credential. Reusing two tools removes a goal from the 8-day path | Sub-agents per operation would add routing errors for no gain. Two-step move: the customer clicks twice, and the order (book first) is an instruction contract measured by G08, not a code guarantee; see §7 | Captured request shows 5 declarations; G08 tool-choice and move-order cases | provisional (A6, A11) |
| D2 | Behaviour stays comparable across releases, within budget | `gemini-3.8-flash` on Vertex AI, pinned. Stable on the Gemini API with no shutdown announced, per the `adk-model-and-output-contracts` lifecycle snapshot (checked 2026-10-08). Low thinking level; temperature left at default | `gemini-3.7-flash` reaches Vertex retirement on 2027-01-28, inside this plan's horizon; 2.5 models retire on 2026-10-20 | Price and quota not looked up (no network); refresh the snapshot before G02 | Release manifest has no alias; G08 baseline recorded against this ID | provisional (A3) |
| D3 | I1 | The chat API verifies the existing login token (signature, issuer, audience, expiry) and maps it to `customer_id`, which it writes to session state. Sessions are created and owned per `customer_id`. In phase 1 a request without a valid token gets 401 and creates no session and no model call (A12) | Authority comes from the verified token, not from the model or a client-supplied ID. Requiring sign-in removes the anonymous session path and its per-IP cap from the 8-day work and closes unauthenticated model spend | Depends on A4; an email one-time code would add 6–10 h. Visitors cannot ask availability questions before signing in until G22 | Forged, expired, wrong-issuer and missing tokens are rejected; resuming another customer's session ID is refused | provisional (A4, A12) |
| D4 | I2 | Propose-then-confirm outside the model. A `propose_*` tool validates input, rechecks availability, ownership and `changeable`, and stores a pending operation: canonical payload, `customer_id`, 10-minute expiry. The widget's Confirm calls the confirm endpoint, which rechecks ownership, expiry, slot and policy, then dispatches | The model can never execute a write; the click is bound to the stored payload, not to model text | Native ADK `require_confirmation` was considered and rejected: Google lists `DatabaseSessionService` as unsupported for it ([confirmation known limitations](https://adk.dev/tools-custom/confirmation/#known-limitations), cited via `safe-api-tool-calls` compatibility notes), and a code-owned click is stronger | I2 test; a changed payload under the same operation ID is rejected | proposed |
| D5 | I3 | State machine `pending → confirmed → dispatching → succeeded / failed / uncertain`, with one row per `operation_id`. The confirm handler claims the row atomically. A timeout or connection loss after send means `uncertain`, which is resolved by listing the customer's bookings at that slot, never by fresh dispatch. If the API supports an idempotency key, `operation_id` is sent as that key. Built once in G04a and reused by every operation kind | A lost response cannot become a duplicate booking | Without an idempotency key, the lookup matches on slot, customer and service; two identical bookings made outside the assistant could confuse it (G01 settles) | Lost-response, double-click and concurrent-confirm tests (G04a) | provisional (A6) |
| D6 | Conversations and operations survive restarts and multiple instances | Cloud SQL Postgres, the smallest tier, for ADK `DatabaseSessionService` and the operations and turn-counter tables. SQLite locally | Proposals need a transactional store, and one database serves both | In-memory sessions break on a second instance; Firestore would mean a second store | Restart mid-conversation keeps the session; pinned-ADK check of the session service (G09) | proposed |
| D7 | Serve the widget and the confirm endpoint under our auth | One Cloud Run service per environment running a FastAPI app that owns the `Runner`; previous revision kept for rollback | We need custom endpoints (confirm, auth) anyway; one deployable unit | Agent Runtime would still need a gateway for auth and confirm; GKE is more than the team can run | Deployment readback shows the revision, model ID and prompt version (G09) | proposed |
| D8 | Customers see proposals and real outcomes | Custom JSON contract, non-streaming: `{messages[], proposals[{operation_id, summary fields, expires_at}], operations[{operation_id, status, receipt}]}`. A plain widget in phase 1; slot cards in phase 2 (G13). A two-step move shows two proposal cards in turn | Completed replies are simpler to secure and test; status is rendered from records (I4) | No incremental text; replies arrive after 2–6 s (unmeasured) | Contract tests and a manual run in a browser (G07, G11) | proposed |
| D9 | I5 | `max_llm_calls=8` per invocation; 40 turns per customer per day in Postgres counters; no model call without a verified customer (D3); an env-flag kill switch that answers with the salon phone number (G09); a billing budget alert at 50/90/100 % of A3 (G10) | The floor for a public service | Caps may frustrate heavy users; counters cost one query per turn | Cap, unauthenticated-request and kill-switch tests; drill in G10 | provisional (A3) |
| D10 | I6, minimise personal data | Tools return projections: first name, salon, service, stylist first name, start time, appointment ID and `changeable`, without phone, email or staff notes. Content capture is off in telemetry; sessions are deleted after 30 days by the G21 job, live before launch day + 30 (A15) | Less data reaches the model and storage; staff free-text notes, which are untrusted, never reach the model | The assistant cannot answer "what number do you have for me" | I6 log check (G09); deletion check (G21) | proposed |
| D11 | Releases can be compared and rolled back | `release.json` records the image, `google-adk==2.8.0` (confirmed in G02), model ID, prompt version and tool-schema hash. CI runs deterministic tests and the scripted-model evaluation. Rollback goes to the previous Cloud Run revision | Model, prompt and tools change together | No canary in phase 1 (Later list) | CI fails on a broken test; rollback rehearsed in G10 | proposed |
| D12 | "Thursday afternoon" resolves correctly | Code injects today's date, the salon's time zone and opening hours into session state for the instruction. `propose_*` takes ISO datetimes, validates them against the salon's hours and echoes the absolute date in the proposal | Date arithmetic is code's job; the customer checks the absolute date before confirming | Model must output ISO datetimes; invalid ones get an actionable error | G08 date cases; daylight-saving boundary case | proposed |

### Model-facing contracts

| Surface | Contract | Implementing skill and verification |
| --- | --- | --- |
| Instruction | Prompt version in `prompts/booking_agent/`: role, a booking flow (find, propose, ask the customer to confirm), the move flow (only for a `changeable` appointment: propose the new booking first, and propose the cancellation only after the booking's status card shows success), "never say a change is done; the status card does", policy wording from W2. Identity, dates, the `changeable` rule and caps live in code | `adk-agent-instructions`; rendered-request test; G08 move-order cases |
| Tools | Five function tools (D1), all results bounded dicts `{status, ...}` with actionable errors (`slot_taken`, `outside_policy_window`, `not_changeable`, `sign_in_required`); tiers: read / propose (write to our store only) — no model-reachable tool writes to the booking API | `adk-tool-interface-design`; declaration dump |
| Output and model | Free text reply; structured data travels through tool results and the operation record, so no `output_schema` in phase 1. Model pinned per D2 | `adk-model-and-output-contracts`; pin check in the release manifest |

## 5. Data, authority and security posture

| Data / operation | Owner and scope | Writers / readers | Source and freshness | Lifetime / erasure |
| --- | --- | --- | --- | --- |
| Appointments, availability | Booking API | Booking API; read by tools; written only by the dispatcher | Authoritative and live; rechecked at propose and at confirm | Booking system's policy |
| Conversation session | Chat API, per `customer_id` | ADK Runner; read by the owner only | Postgres | 30 days, deleted by a scheduled job (G21, live before launch day + 30); erasure by hand until G17 |
| Operation record | Chat API, per `customer_id` | Propose tools, confirm endpoint, dispatcher | Postgres; receipt from the booking API | 90 days for reconciliation and support |
| Turn counters | Chat API | Middleware | Postgres | 2 days |

There are three identities. The **customer** is verified from the login
token. The **workload** is the Cloud Run service account, which reads the
booking-API key from Secret Manager. The booking API trusts the workload key
for all customers, so our code enforces I1 at every tool and at confirm. There
is no delegated OAuth.

| Agent | Private data | Untrusted content | Write or egress | Resolution |
| --- | --- | --- | --- | --- |
| booking agent | the signed-in customer's own appointments | The customer's own messages; free-text fields from the API (staff notes, service descriptions) | Propose only; no booking-API write and no outbound messages | Remove the write leg: dispatch happens only on the customer's click. Free-text staff notes are projected out (D10); service descriptions are staff-authored and kept. G15 adds the adversarial suite |

## 6. Budgets and capacity

The workload is assumed and illustrative: 5 salons × about 30 conversations a
day, 6 turns each, and about 3 model calls per turn under the cap of 8, so
around 2,700 model calls a day at roughly 4–6 k input tokens each once all
salons are live; the pilot salon alone is about a fifth of that. Prices were
**not looked up** because this session had no network access. Before G09,
check the current Vertex AI price for the pinned model and for Cloud SQL's
smallest tier, then compare the sum with A3. The billing budget alert only
notifies; it does not cap spend. Enforcement comes from D9. G20 records
measured tokens (from the per-turn log fields) and cost per completed
operation, and those replace these assumptions. Latency targets are unknown;
G20 measures them, and phase 2 sets them.

## 7. Failure and recovery

Coverage grid (every external system × every failure type; tests are planned,
not run):

| Integration | Unavailable or slow | Rejects the request | Write outcome unknown | Partial multi-step change | Credential expired or revoked | Rate limited or out of quota | Duplicate or concurrent request | Untrusted or malformed content |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Booking API, reads | Timeout retried at most twice, then "I can't check right now" with the salon phone (G01) | Actionable tool error such as `not_found` (G02) | n/a: read only | n/a: read only | Workload key refused → tool error and an error log line; runbook step (G10) | Treated as transient: at most two retries, then refusal (G01) | n/a: reads are safe to repeat | Staff notes projected out; unexpected payload raises a client error class, not a tool result (G01, D10) |
| Booking API, writes (dispatcher) | Failure before send → `failed`, nothing sent (G04a) | `slot_taken` → fresh slots; `outside_policy_window` → policy text (G04a, G05) | Timeout after send → `uncertain`, reconciled by lookup (G04a; staging drill G10) | Across operations: two-step move row below (G05, G08). Within one operation: n/a, one API call | Key refused → `failed`, no retry; runbook (G10) | Write never retried automatically → `failed`, customer may confirm a fresh proposal (G01, D5) | Row claim and idempotency key → one booking (G04a) | Receipt fields validated; an unreadable receipt → `uncertain`, then lookup (G04a) |
| Customer login keys (token issuer) | Key fetch fails → cached keys until they expire, then 401 "please sign in again" (G03) | Invalid token → 401, no session (G03) | n/a: no writes | n/a | Expired token → 401, widget asks the customer to sign in (G03) | n/a: keys are cached | n/a | Forged or tampered token → 401 (G03) |
| Vertex AI model | "Sorry, I can't help right now — call …"; session kept (row below) | Same refusal; logged with the status (G02) | n/a: the model holds no executing write (I2) | n/a | Workload identity failure → refusal; visible in deploy readback (G09) | Quota error → refusal, no retry loop; `max_llm_calls` bounds a turn (G02) | Turns serialised per session (G07) | Invalid ISO date or argument → actionable tool error (D12, G02); model text never rendered as a status (I4, G07) |
| Cloud SQL Postgres | Chat returns 503 with the salon phone and makes no model call, because the cap check fails closed (G07) | Constraint violation → 500, no dispatch (G04a) | Commit lost after dispatch → lease expiry → `uncertain` → lookup (restart row) | n/a: one transaction per state change | IAM or connection credential failure → 503; deploy readback (G09) | Connection limit → 503 (n/a at pilot traffic) | Row claim (G04a); advisory lock per session (G07) | n/a: our own data |
| Customer browser (widget requests) | n/a: the server owns state | Malformed body → 422 (G07) | Confirm response lost → widget polls `GET /operations/{id}` (G07) | n/a | Missing token → 401 (G07) | Turn cap → refusal with the phone (G07) | Double click or two tabs → one operation (G04a) | Another customer's `session_id` or `operation_id` → refused (G03, G04a) |

| Failure window | User-visible outcome | Retained state / possible effects | Safe next action and recovery owner |
| --- | --- | --- | --- |
| Success (Maya's move, phase 1) | Status card "Booked Thu 23 Oct 14:30", then "Cancelled Sat 18 Oct 10:00", both from receipts | Two operations `succeeded` with receipts | — |
| Two-step move: new booking succeeded, cancellation refused or failed | Second card shows the failure; the assistant says the Saturday appointment is still booked and gives the salon phone | Booking operation `succeeded`; cancellation `failed` (for example `outside_policy_window`) or `uncertain`; the customer holds two appointments | Customer retries the cancellation or phones; staff see both in the calendar. Residual risk until G06: if the model proposed the cancellation first and the slot was then taken, the customer would lose the old slot by their own explicit click; G08 asserts book-first order and `changeable` prevents the late-window case |
| No valid token | 401; widget asks the customer to sign in | No session, no model call | Customer signs in (G03, G07) |
| Token or ID for another customer | "I can't find that appointment" | No read of B's data, no proposal | — (I1 tests) |
| Model unavailable or 8-call cap hit | "Sorry, I can't help right now — call Riverside on …" | Session kept; no proposal | Customer retries later; the spike shows in logs |
| Slot taken between propose and confirm | "That time was just taken" plus fresh slots | Operation `failed: slot_taken`; no write | Customer picks again |
| Proposal expired or payload changed | "Please confirm the new details" | Old operation `expired`; nothing sent | Customer reconfirms |
| Inside cancellation window (A7) | Policy text from W2 and the salon phone number | `not_changeable` at propose, or `failed: outside_policy_window` at confirm | Salon staff handle the request by phone |
| Booking API timeout after send | "Checking with the salon…" then the actual result | Operation `uncertain`; booking may exist | The dispatcher reconciles by lookup on the next status poll. If that is still unresolved, it goes on the on-call list in the G10 runbook (owner: Dev A in phase 1; automated in G18) |
| Double click / two tabs | One status card | One operation, one write | — (D5 claim) |
| Two tabs send chat messages to one session at once | The second message waits; after 10 s it gets "please resend" | The chat API serialises turns per session (Postgres advisory lock), so one turn writes events at a time; a rejected message runs no model call | Customer resends (G07) |
| Process restart mid-dispatch | Status shows "checking" | Operation `dispatching`; it becomes `uncertain` after a 60 s lease | Same reconciliation as above |
| Kill switch on / budget exhausted | Refusal with the salon phone number | No model calls | Operator turns it off (G10 runbook) |
| Rollback | Previous revision serves | Sessions and operations stay compatible because there is no schema change in phase 1 | On-call person per the G10 runbook |

Not applicable in phase 1: remote peers (none), memory erasure races (no
long-term memory), screening service outage (none used), trace exporter
outage (no exporter until G16), model retirement (none announced for D2
within the horizon).

## 8. Verification and handoff

The ladder runs in four steps. **Offline:** tool, policy, state-machine and
Runner tests with a scripted model and the fake booking API (G01–G07,
including G04a), plus the evaluation runner on the fake (G08). **Local
integration:** a restart during dispatch, and a browser run of the widget.
**Bounded live:** book and cancel through the dispatcher against the staging
booking API plus a forced timeout (G10's drill), then the agent's journey,
including Maya's two-step move, with the pinned model, at most 50 model calls
(G11). **Release:** staging rehearsal, kill-switch and rollback drill (G10),
then the pilot (G11).

ADK interfaces were read against the specialists' `google-adk 2.8.0` baseline.
G02 confirms that pin, and G16 checks the observability notes' span-retention
fix for 2.10.0 or later before enabling trace export. Goals, owners and the
next prompt are in the plan.

## 9. Open decisions

| Question or assumption | Why it changes the design | Owner / evidence needed | What it blocks |
| --- | --- | --- | --- |
| A4 customer login verifiable by our backend? | Without it, D3 needs an email one-time code (+6–10 h). The 8-day plan has no room for it; see the plan's what-ifs | Dev C in G03: JWKS/issuer or session introspection | G03, then G05 and G07 |
| A6 idempotency key, reschedule endpoint | Sets D5's dedupe strength; the reschedule endpoint now only shapes G06 (phase 2) | Dev A in G01 | G04a; G06 |
| A7 who enforces the policy window | If the API does not, our confirm endpoint and the `changeable` flag must hold the rule per salon | Dev A in G01; salon owner via W2 | G05 |
| A3 budget and the price lookup | Model tier and caps | Team; price check before G09 | G09 sizing |
| Cut package A11–A15 versus a later date | The 8-day plan fits only with all five; the plan lists what each costs and the date that would restore it | The salon owners and the team | G05, G07, G08, G09, G11 scope |
