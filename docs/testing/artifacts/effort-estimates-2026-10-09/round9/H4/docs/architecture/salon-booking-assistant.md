# System design: salon booking assistant

Status: **draft**. The team was not available for this session, so every
decision below rests on the assumed answers A1 to A10, and decisions that
depend on them are **provisional** until the team confirms. No decision is
user-accepted yet.

Decisions and their rationale live here. The plan
([docs/plans/salon-booking-assistant.md](../plans/salon-booking-assistant.md))
holds estimates, owners, capacity, finish range and cut line; the tickets hold
each goal's scope and acceptance.

## Assumed answers

| ID | Question I would have asked | Assumed answer | Decisions that depend on it |
| --- | --- | --- | --- |
| A1 | When must the first useful version exist, and what happens after? | 10 working days from start; kept and improved afterwards | Phase 1 code is the kept form (D1–D12) |
| A2 | How many hours each, and how familiar with ADK and GCP? | Three developers, about 5 focused hours a day each on this project; strong in Python and web; new to ADK; some GCP. ×1.5 on every estimate | Plan capacity and estimates |
| A3 | What budget is there for models and cloud? | About USD 300 a month during the MVP | D2, D9 |
| A4 | How do customers sign in today? | The salon website has customer accounts issued by the booking system. Its login yields a signed token (JWT) whose subject is the booking-system customer ID, and our backend can verify it. Fallback if it is not verifiable: a one-time email code, about 6–10 extra hours | D3; blocks G03 |
| A5 | Does booking involve deposits, prepayment or no-show fees? | No. No money moves through the assistant | D4 depth; "Later" list in the plan |
| A6 | What does the booking API offer for writes? | REST with list salons/services/stylists, availability search, create, reschedule, cancel and list-by-customer. An idempotency-key header is **unknown** (G01 finds out). Move is a single reschedule call | D5; shapes G04, G06 |
| A7 | Who enforces the cancellation and late-change policy? | The booking API rejects changes inside the policy window (assumed 24 hours) with a distinct error. Our confirm endpoint rechecks it before dispatch | G05, G06 |
| A8 | Who uses it, and through which channel? | External salon customers, through a chat widget on the existing salon website (web only). Anonymous visitors may browse availability; booking, moving and cancelling need sign-in. The chain owner judges the pilot | D3, D7, D8 |
| A9 | Languages and time zones? | English only. All five salons share one time zone, but the time zone is read per salon from the API anyway | D12 |
| A10 | What data is touched? | Personal data: customer name, contact details on file and appointment history. No health or payment data. Tools expose only what the journey needs | D10 |

## 1. Purpose and constraints

**Journey (running example).** Maya has a Saturday 10:00 cut with Sam at the
Riverside salon and needs to move it to next week. Today she phones the salon,
during opening hours only, and often waits while the receptionist serves a
client. The website can book, but she does not find a way to move an
appointment, so she cancels and rebooks or gives up. With the assistant, she
signs in on the salon site, types "move my Saturday haircut to Thursday
afternoon next week". The assistant shows her Saturday appointment and three
free Thursday slots with Sam. She taps a proposal showing *Riverside · Women's
cut · Sam · Thu 23 Oct 14:30*, presses **Confirm**, and sees the new time taken
from the booking API's receipt.

**Model versus code.** The model interprets the request: which appointment,
which service, which stylist, and what "Thursday afternoon" means. It chooses
read tools and proposes a change. Code owns everything else: who the customer
is, which appointments they may touch, dates resolved to absolute times,
policy checks, the confirmation click, the write to the booking API and the
displayed result.

**Non-goals for the MVP:** payments, SMS or WhatsApp, staff-facing features,
reminders, waitlists, languages beyond English, and remembered preferences.

**Outcome to improve (hypothesis, unmeasured):** the share of book, move and
cancel requests that customers complete without phoning, out of hours
especially. Guardrail: support calls about wrong bookings must not go up.
Baseline: the salons' current phone-change volume, which the salon owner
supplies during G11. G11 measures completion and the plan's phase 2 tracks
it.

**Existing systems (assumed, not inspected):** the booking API and its
database are the authority for appointments and availability. The salon
website and its customer login are assumed as in A4. No application code
exists in this repository yet.

## 2. Delivery constraints, depth and deferred controls

| Scope-gate answer | Value |
| --- | --- |
| First useful version due | 10 working days (A1); continued |
| People and hours | 3 developers × ~5 focused h/day, new to ADK (A2); the same team runs it afterwards |
| Money | ~USD 300/month for models and cloud (A3) |
| Users and judge | External customers via the web widget; the chain owner judges the pilot (A8) |
| Data and effects | Customer personal data; writes that are reversible but visible to real people (bookings in staff calendars, confirmation messages sent by the booking system); no money (A5, A10) |
| Delivery profile | **MVP or pilot:** first external users, real bookings, the team must see failures and cost |

| Concern | Depth now | Trigger that raises it |
| --- | --- | --- |
| Core judgment, measured | Build: 30-case evaluation set, run locally and before launch (G08, G11) | Phase 2: gate in CI (G14) |
| Identity and per-customer scope | Build: verified login token, own appointments only (G03) | — |
| Secrets | Build: workload identity and Secret Manager (G09) | Rotation when the booking-API key policy requires it |
| External writes | Build: click-confirmed proposals, idempotent dispatch, reconcile-before-retry (G04–G06) | Automated reconciliation (G18) when more than one uncertain operation per week |
| Sensitive data | Build: projected tool results, no message content in logs or traces, 30-day session retention (configured in G09) | Erasure tooling (G17) before the second salon month or the first erasure request |
| Prompt injection and agency | Build at MVP depth: the structure in §5 (model has no executing write tool) | Adversarial suite (G15) in phase 2 |
| Budgets and loops | Build: `max_llm_calls`, per-customer and per-IP turn caps, kill switch (G02, G07, G09) | Shared allowance when traffic exceeds one instance |
| Memory | Conversation sessions only | Repeat customers restating preferences |
| Frontend | Build: plain widget with proposal cards and a Confirm button (G07) | Slot cards (G13) in phase 2 week 1 |
| Hosting | Build: one Cloud Run service with rollback to the previous revision (G09) | — |
| Observability | Build: traces and token cost, content capture off (G09) | SLOs and alerts (G16) |
| Release engineering | Build: pinned versions, release manifest, deterministic tests and scripted evaluation in CI (G09) | Live evaluation gate (G14) |
| Performance tuning | Defer | Measured p95 latency or cost per booking above target |

**Floor kept:** no secrets in code, prompts or logs. Spend stops through
`max_llm_calls`, per-customer caps, an operator kill switch and a billing
budget alert, which alerts only and does not cap. No booking change happens
without the customer's click on an exact proposal. Personal data is limited to
the signed-in customer's own records and stays out of logs. The model ID is
pinned. No accepted risks.

**Who may use it, when:** during G11 only customers of the pilot salon, with
staff informed (W2). **Graduation to all five salons (G12):** at least 3 days
of the pilot with no wrong-booking incident, no uncertain operation left
unresolved, and the G08 evaluation at or above the G11 threshold.

| Deferred control | Why it waits | What would bring it forward |
| --- | --- | --- |
| Live evaluation gate in CI (G14) | Prompt changes are rare in week 2; G11 runs evaluation by hand | First prompt or model change after launch |
| Adversarial suite (G15) | §5 structure blocks the harmful actions in code; the suite adds evidence, not the control | Any new tool, new channel, or a free-text field added to tool results |
| SLOs and alerts (G16) | No baseline until the pilot runs | One week of pilot traffic |
| Erasure tooling (G17) | Retention deletes sessions after 30 days; erasure can be done by hand at pilot scale | First erasure request or second salon month |

Capacity, finish range and cut line: see the plan's summary.

## 3. Guarantees and acceptance

| ID | Invariant | Enforcing component and evidence | Failure outcome | Planned verification |
| --- | --- | --- | --- | --- |
| I1 | A customer reads, moves or cancels only their own appointments | `customer_id` comes from the verified token (G03), is written to session state by the chat API, and is read by tools and by the confirm endpoint. It is never a model argument. Booking API calls filter by it, and the confirm endpoint checks the appointment's owner again | Not-found response, no write | Two fixture customers: B's appointment ID offered by a scripted model is refused at the tool and at confirm (G05, G06, G07) |
| I2 | No booking change happens without the customer clicking Confirm on a proposal showing salon, service, stylist and absolute start time | The model holds only `propose_*` tools, which write a pending proposal. Only `POST /operations/{id}/confirm` dispatches, and it needs the session's verified customer | Proposal stays pending and expires after 10 minutes | A scripted model calls every tool, and the fake booking API records zero writes until confirm (G04) |
| I3 | One confirmed proposal causes at most one booking change | The operation record (unique `operation_id`) moves through a state machine under a row lock; the ID is sent as the idempotency key if the API supports one (G01). An `uncertain` write is reconciled by lookup, never by fresh dispatch | Customer sees "checking with the salon" and later the result | Double click, concurrent confirms, and a lost response after a provider commit all end with one booking (G04) |
| I4 | A shown confirmation reflects the booking API's receipt | The widget renders status from the operation record. Model text never states that a change succeeded | Model text claiming success is not shown as a status card | Model says "booked" while the API fails: the card shows failure (G07) |
| I5 | Spend and work are bounded per turn, per customer and overall | `RunConfig.max_llm_calls=8` (G02); turn caps in chat API middleware (G07); kill switch (G09) | Polite refusal with the salon's phone number | Unit tests at each cap; kill-switch drill in G10 |
| I6 | Message content and contact details do not reach logs or traces | Telemetry content capture is off; logs carry IDs, tool names, statuses and token counts; tool results are projected (D10) | — | Captured log and span export from a test run contain no fixture names or phone numbers (G09) |

## 4. Architecture and decisions

```text
 Browser (salon site)          Cloud Run: booking-assistant (FastAPI)                Booking API (existing)
 ┌─────────────┐  JSON   ┌───────────────────────────────────────────────┐  HTTPS  ┌──────────────┐
 │ chat widget │────────▶│ auth middleware → customer_id (trusted)        │         │ availability │
 │  [Confirm]  │         │ caps + kill switch                             │         │ bookings     │
 └─────┬───────┘         │ Runner ─ LlmAgent (gemini-3.8-flash, Vertex)   │────────▶│ (authority)  │
       │ POST confirm    │   read tools ─────────────────────────────────┼────────▶│              │
       └────────────────▶│   propose_* tools → operations table (pending) │         │              │
                         │ confirm endpoint → dispatcher ─────────────────┼────────▶│ create/move/ │
                         └──────────────┬─────────────────────────────────┘         │ cancel       │
                                        │ Cloud SQL Postgres: ADK sessions,         └──────────────┘
                                        │ operations, turn counters
```

| ID | Requirement | Design choice | Reason | Tradeoff / alternative | Verification | Status |
| --- | --- | --- | --- | --- | --- | --- |
| D1 | Interpret booking requests using a small set of capabilities | One `LlmAgent`, no sub-agents. Read tools: `list_salons_and_services`, `find_free_slots`, `list_my_appointments`. Proposal tools: `propose_booking`, `propose_move`, `propose_cancellation`. That is six function tools | One judgment owner and a small tool set; nothing here needs a separate context or credential | Sub-agents per operation would add routing errors for no gain | Captured request shows 6 declarations; G08 tool-choice accuracy | provisional (A6) |
| D2 | Behaviour stays comparable across releases, within budget | `gemini-3.8-flash` on Vertex AI, pinned. Stable on the Gemini API with no shutdown announced, per the `adk-model-and-output-contracts` lifecycle snapshot (checked 2026-10-08). Low thinking level; temperature left at default | `gemini-3.7-flash` reaches Vertex retirement on 2027-01-28, inside this plan's horizon; 2.5 models retire on 2026-10-20 | Price and quota not looked up (no network); refresh the snapshot before G02 | Release manifest has no alias; G08 baseline recorded against this ID | provisional (A3) |
| D3 | I1 | The chat API verifies the existing login token (signature, issuer, audience, expiry) and maps it to `customer_id`, which it writes to session state. Sessions are created and owned per `customer_id`; an anonymous session gets read tools only, and proposal tools return "sign in to continue" | Authority comes from the verified token, not from the model or a client-supplied ID | Depends on A4; an email one-time code would add 6–10 h | Forged, expired and wrong-issuer tokens are rejected; resuming another customer's session ID is refused | provisional (A4) |
| D4 | I2 | Propose-then-confirm outside the model. A `propose_*` tool validates input, rechecks availability and ownership, and stores a pending operation: canonical payload, `customer_id`, 10-minute expiry. The widget's Confirm calls the confirm endpoint, which rechecks ownership, expiry, slot and policy, then dispatches | The model can never execute a write; the click is bound to the stored payload, not to model text | Native ADK `require_confirmation` was considered and rejected: Google lists `DatabaseSessionService` as unsupported for it ([confirmation known limitations](https://adk.dev/tools-custom/confirmation/#known-limitations), cited via `safe-api-tool-calls` compatibility notes), and a code-owned click is stronger | I2 test; a changed payload under the same operation ID is rejected | proposed |
| D5 | I3 | State machine `pending → confirmed → dispatching → succeeded / failed / uncertain`, with one row per `operation_id`. The confirm handler claims the row atomically. A timeout or connection loss after send means `uncertain`, which is resolved by listing the customer's bookings at that slot, never by fresh dispatch. If the API supports an idempotency key, `operation_id` is sent as that key | A lost response cannot become a duplicate booking | Without an idempotency key, the lookup matches on slot, customer and service; two identical bookings made outside the assistant could confuse it (G01 settles) | Lost-response, double-click and concurrent-confirm tests (G04) | provisional (A6) |
| D6 | Conversations and operations survive restarts and multiple instances | Cloud SQL Postgres, the smallest tier, for ADK `DatabaseSessionService` and the operations and turn-counter tables. SQLite locally | Proposals need a transactional store, and one database serves both | In-memory sessions break on a second instance; Firestore would mean a second store | Restart mid-conversation keeps the session; pinned-ADK check of the session service (G09) | proposed |
| D7 | Serve the widget and the confirm endpoint under our auth | One Cloud Run service running a FastAPI app that owns the `Runner`; previous revision kept for rollback | We need custom endpoints (confirm, auth) anyway; one deployable unit | Agent Runtime would still need a gateway for auth and confirm; GKE is more than the team can run | Deployment readback shows the revision, model ID and prompt version (G09) | proposed |
| D8 | Customers see proposals and real outcomes | Custom JSON contract, non-streaming: `{messages[], proposals[{operation_id, summary fields, expires_at}], operations[{operation_id, status, receipt}]}`. A plain widget in phase 1; slot cards in phase 2 (G13) | Completed replies are simpler to secure and test; status is rendered from records (I4) | No incremental text; replies arrive after 2–6 s (unmeasured) | Contract tests and a manual run in a browser (G07, G11) | proposed |
| D9 | I5 | `max_llm_calls=8` per invocation; 40 turns per customer per day and 20 per anonymous IP per hour in Postgres counters; an env-flag kill switch that answers with the salon phone number; a billing budget alert at 50/90/100 % of A3 | The floor for a public service | Caps may frustrate heavy users; counters cost one query per turn | Cap and kill-switch tests; drill in G10 | provisional (A3) |
| D10 | I6, minimise personal data | Tools return projections: first name, salon, service, stylist first name, start time and appointment ID, without phone, email or staff notes. Content capture is off in telemetry; sessions are deleted after 30 days | Less data reaches the model and storage; staff free-text notes, which are untrusted, never reach the model | The assistant cannot answer "what number do you have for me" | I6 export check (G09) | proposed |
| D11 | Releases can be compared and rolled back | `release.json` records the image, `google-adk==2.8.0` (confirmed in G02), model ID, prompt version and tool-schema hash. CI runs deterministic tests and the scripted-model evaluation. Rollback goes to the previous Cloud Run revision | Model, prompt and tools change together | No canary in phase 1 (Later list) | CI fails on a broken test; rollback rehearsed in G10 | proposed |
| D12 | "Thursday afternoon" resolves correctly | Code injects today's date, the salon's time zone and opening hours into session state for the instruction. `propose_*` takes ISO datetimes, validates them against the salon's hours and echoes the absolute date in the proposal | Date arithmetic is code's job; the customer checks the absolute date before confirming | Model must output ISO datetimes; invalid ones get an actionable error | G08 date cases; daylight-saving boundary case | proposed |

### Model-facing contracts

| Surface | Contract | Implementing skill and verification |
| --- | --- | --- |
| Instruction | Prompt version in `prompts/booking_agent/`: role, a booking flow (find, propose, ask the customer to confirm), "never say a change is done; the status card does", policy wording from W2. Identity, dates and caps live in code | `adk-agent-instructions`; rendered-request test |
| Tools | Six function tools (D1), all results bounded dicts `{status, ...}` with actionable errors (`slot_taken`, `outside_policy_window`, `sign_in_required`); tiers: read / propose (write to our store only) — no model-reachable tool writes to the booking API | `adk-tool-interface-design`; declaration dump |
| Output and model | Free text reply; structured data travels through tool results and the operation record, so no `output_schema` in phase 1. Model pinned per D2 | `adk-model-and-output-contracts`; pin check in the release manifest |

## 5. Data, authority and security posture

| Data / operation | Owner and scope | Writers / readers | Source and freshness | Lifetime / erasure |
| --- | --- | --- | --- | --- |
| Appointments, availability | Booking API | Booking API; read by tools; written only by the dispatcher | Authoritative and live; rechecked at propose and at confirm | Booking system's policy |
| Conversation session | Chat API, per `customer_id` (or per anonymous browser) | ADK Runner; read by the owner only | Postgres | 30 days, deleted by a scheduled job (G09); erasure by hand until G17 |
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
around 2,700 model calls a day at roughly 4–6 k input tokens each. Prices were
**not looked up** because this session had no network access. Before G09,
check the current Vertex AI price for the pinned model and for Cloud SQL's
smallest tier, then compare the sum with A3. The billing budget alert only
notifies; it does not cap spend. Enforcement comes from D9. G11 records
measured tokens and cost per completed operation, and those replace these
assumptions. Latency targets are unknown; G11 measures them, and phase 2 sets
them.

## 7. Failure and recovery

| Failure window | User-visible outcome | Retained state / possible effects | Safe next action and recovery owner |
| --- | --- | --- | --- |
| Success (Maya's move) | Status card "Moved to Thu 23 Oct 14:30" from the receipt | Operation `succeeded` with receipt | — |
| Token or ID for another customer | "I can't find that appointment" | No read of B's data, no proposal | — (I1 tests) |
| Model unavailable or 8-call cap hit | "Sorry, I can't help right now — call Riverside on …" | Session kept; no proposal | Customer retries later; spike shows in traces |
| Slot taken between propose and confirm | "That time was just taken" plus fresh slots | Operation `failed: slot_taken`; no write | Customer picks again |
| Proposal expired or payload changed | "Please confirm the new details" | Old operation `expired`; nothing sent | Customer reconfirms |
| Inside cancellation window (A7) | Policy text from W2 and the salon phone number | `failed: outside_policy_window` | Salon staff handle the request by phone |
| Booking API timeout after send | "Checking with the salon…" then the actual result | Operation `uncertain`; booking may exist | The dispatcher reconciles by lookup on the next status poll. If that is still unresolved, it goes on the on-call list in the G10 runbook (owner: Dev A in phase 1; automated in G18) |
| Double click / two tabs | One status card | One operation, one write | — (D5 claim) |
| Two tabs send chat messages to one session at once | The second message waits; after 10 s it gets "please resend" | The chat API serialises turns per session (Postgres advisory lock), so one turn writes events at a time; a rejected message runs no model call | Customer resends (G07) |
| Process restart mid-dispatch | Status shows "checking" | Operation `dispatching`; it becomes `uncertain` after a 60 s lease | Same reconciliation as above |
| Kill switch on / budget exhausted | Refusal with the salon phone number | No model calls | Operator turns it off (G10 runbook) |
| Rollback | Previous revision serves | Sessions and operations stay compatible because there is no schema change in phase 1 | Dev C per G10 runbook |

Not applicable in phase 1: remote peers (none), memory erasure races (no
long-term memory), screening service outage (none used), model retirement
(none announced for D2 within the horizon).

## 8. Verification and handoff

The ladder runs in four steps. **Offline:** tool, policy, state-machine and
Runner tests with a scripted model and the fake booking API (G01–G07), plus
the evaluation runner on the fake (G08). **Local integration:** a restart
during dispatch, and a browser run of the widget. **Bounded live:** book, move
and cancel against the staging booking API with the pinned model, at most 50
model calls (G06, G11). **Release:** staging rehearsal, kill-switch and
rollback drill (G10), then the pilot (G11).

ADK interfaces were read against the specialists' `google-adk 2.8.0` baseline.
G02 confirms that pin, and G09 checks the observability notes' span-retention
fix for 2.10.0 or later before enabling traces. Goals, owners and the next
prompt are in the plan.

## 9. Open decisions

| Question or assumption | Why it changes the design | Owner / evidence needed | What it blocks |
| --- | --- | --- | --- |
| A4 customer login verifiable by our backend? | Without it, D3 needs an email one-time code (+6–10 h, which crosses the cut line) | Dev C in G03: JWKS/issuer or session introspection | G03, then G05–G07 |
| A6 idempotency key, reschedule endpoint | Sets D5's dedupe strength; no reschedule endpoint means a move becomes cancel plus rebook (two operations) | Dev A in G01 | G04, G06 |
| A7 who enforces the policy window | If the API does not, our confirm endpoint must hold the rule per salon | Dev A in G01; salon owner via W2 | G05, G06 |
| A3 budget and the price lookup | Model tier and caps | Team; price check before G09 | G09 sizing |
| Cut line (one salon, plain widget) versus one extra day | Scope of the two weeks | The team | G07, G11 scope |
