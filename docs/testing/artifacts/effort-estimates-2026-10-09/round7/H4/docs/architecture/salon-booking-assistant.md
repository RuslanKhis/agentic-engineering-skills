# System design: salon booking assistant (ADK)

Status: **draft**. Written in one pass, with nobody available to answer
questions. Every row in *Assumed answers* is provisional, and so is every
decision that depends on one. Decisions and their reasons live here. The plan
([docs/plans/salon-booking-assistant.md](../plans/salon-booking-assistant.md))
holds estimates, owners, capacity and the cut line, and does not repeat them.

## Assumed answers

| # | Question | Assumed answer | Decisions that depend on it |
| --- | --- | --- | --- |
| A1 | When is the first version due, and is it continued? | In 10 working days (two weeks), then continued | Profile, phase split |
| A2 | Hours and familiarity of the three developers | About 5 focused hours a day each. Strong in Python, new to ADK (×1.5 on estimates), have used GCP | Plan capacity |
| A3 | Money for models and cloud | Small: about US$300 a month during the pilot (labelled assumption) | D8, D9 |
| A4 | Who uses it | Salon customers, in English, signed in to the chain's existing booking website | D3, D10 |
| A5 | How a customer is identified | The booking website already has customer login, and the gateway can verify its token (a JWT or an introspection endpoint) | D3; G04 checks it first |
| A6 | What the booking API offers | A staging environment, plus availability, create, reschedule and cancel endpoints. Idempotency-key support and atomic reschedule are **unknown**, and G01 finds out | D4 |
| A7 | Booking policies | Cancel or move only up to 24 h before the appointment, otherwise the customer phones the salon. Book at least 2 h ahead. The salon owner signs off (wait W1) | D5 |
| A8 | Channel | A web chat widget on the existing booking site. No SMS, WhatsApp or voice | D10 |
| A9 | Launch scope | Phase 1 goes live at **one pilot salon**. The other four salons join in phase 2 | D12 |
| A10 | Existing infrastructure | A GCP project with billing exists. There is no Postgres the assistant can reuse | D6, D7 |
| A11 | Retention and privacy | Transcripts kept for 30 days. The privacy notice is updated before launch (W1) | D11 |
| A12 | Payments or deposits | None in the MVP | Scope |
| A13 | Who runs it after launch | The three developers, in business hours | Runbook in G10 |

## Purpose and constraints

**Journey (the running example).** Maya is signed in to the salon website at
21:40 and types "move my Thursday cut with Jo to Saturday morning". At the
moment she can only phone the salon during opening hours, or cancel and rebook
through a form that has no stylist availability view. After this change, the
assistant finds her Thursday appointment and shows Jo's free Saturday-morning
slots. Maya picks one, sees a confirmation card with the exact old and new
details, presses **Confirm**, and gets a confirmation that comes from the
booking API's own record.

**The model decides:** what the customer wants, which of their appointments
they mean, which offered slot they chose, and the wording of replies.
**Code controls:** who the customer is, which appointments they own, policy
windows, whether a slot is still free, the confirmation and every write.

Non-goals for phase 1: payments, waitlists, reminders, other channels,
languages other than English, memory of preferences across sessions, and staff
tools.

## Delivery constraints, depth and deferred controls

**Profile: MVP or pilot.** Real external customers make real appointment
changes that salon staff act on. Personal data is involved (name, contact
details, appointment history). Each effect is reversible but visible to
people outside the team.

| Concern | Depth now | Trigger that raises it |
| --- | --- | --- |
| Core judgment, measured | Build: a labelled evaluation set of 30 cases (G08, G09) | CI gate in phase 2 (G12) |
| Identity and per-customer scope | Build (G04) | — |
| External writes | Build: confirmation in code, durable operation record, reconciliation of uncertain results (G03) | Automatic reconciliation job (G16) when uncertain results exceed 1 a week |
| Sensitive data | Minimal: no message content in logs or traces, 30-day retention | Phase 2 retention job (G15) |
| Prompt injection and agency | Build structurally: the agent holds no write tool (D2) | Adversarial suite (G14) before all five salons |
| Budgets | Build: `max_llm_calls` and a daily allowance per customer (D9) | Shared budget if traffic grows past the assumed level |
| Frontend | Build: a simple widget (G05) | — |
| Hosting | Cloud Run with staging and prod, and the previous revision kept for rollback | Canary at all-salon launch |
| Observability | Minimal-plus: structured operation logs, token usage, ADK traces with content capture off | SLOs and alerts (G13) |
| Release | Minimal: pinned model and versions, offline tests in CI | Evaluation gate (G12) |
| Memory and retrieval | Out of scope: the journey needs only the current session and booking API data | Customers asking for "my usual" |
| Performance tuning | Defer | Measured p95 above 8 s |

**Floor kept:** no secrets in code, prompts or logs (Secret Manager). A spend
stop: `max_llm_calls`, a daily allowance per customer, a GCP budget alert and a
kill switch. No appointment change happens until the customer presses
Confirm on details rendered from the stored proposal. Personal data stays out
of logs. The model ID is pinned.

**Who may use it:** signed-in customers of the pilot salon. **Graduation
conditions before all five salons:** G12 to G16 complete, a pilot review of
uncertain or failed operations, and the salon owner's agreement.

## Guarantees and acceptance

| Invariant | Enforced by | Failure outcome | Verification |
| --- | --- | --- | --- |
| I1. A customer can read and change only their own appointments | Gateway takes `customer_id` from the verified token into trusted state (D3). Tools filter by it, and the confirm endpoint re-fetches the appointment and checks its owner | Treated as "not found" with no disclosure | Cross-customer tests in G03 and G04 |
| I2. No appointment changes without a customer Confirm on the exact stored details | The model has only `propose_*` tools. The confirm endpoint (code) executes the stored payload (D2) | Proposal expires and nothing changes | Scripted-model test: the model "says" confirmed but no API write occurs (G03, G06) |
| I3. One Confirm produces at most one booking-API change | `operation_id` is unique in the DB. The API call carries the idempotency key if the API supports one, otherwise reconciliation runs before any re-send (D4) | A duplicate click returns the existing result | Double-click and timeout tests (G03) |
| I4. Policy windows hold whatever the model says | Policy is checked in code at proposal and again at confirm (D5) | Refused, with the salon phone number | Policy-edge tests (G03) |
| I5. Spend stays bounded | `max_llm_calls`, the per-customer allowance and the kill switch (D9) | Polite refusal and the phone number | Allowance test (G04) |
| I6. A reported success means the booking API holds the booking | Success text is built from the API response, not by the model | "We're checking" state instead | Lost-response test (G03) |

## Architecture and decisions

```text
Browser widget ──JSON──> Cloud Run: FastAPI gateway ──> ADK Runner ──> LlmAgent (Vertex Gemini)
  (booking site)          │ verify site token → customer_id         │ read tools + propose_* tools
                          │ allowance, kill switch                   │
                          ├── POST /confirm/{operation_id} (code, no model) ──> Booking API (write)
                          └── Cloud SQL Postgres: ADK sessions, operations, allowances
```

| ID | Requirement | Choice | Reason | Tradeoff | Verification |
| --- | --- | --- | --- | --- | --- |
| D1 | Interpret free-text booking requests | One `LlmAgent` with about 6 function tools. No sub-agents | One responsibility and one tool set, so there is no reason to split | A single prompt carries all three intents | Tool selection on the G06 set |
| D2 | No change without explicit consent (floor, I2) | The model calls `propose_booking/move/cancel`, which validate and store a pending operation and return a summary. The widget renders a card from the **stored** payload, and the click calls `/confirm`, which is ordinary code | Removes the agent's write leg and binds consent to the exact payload | More frontend work than ADK's native tool confirmation. The [confirmation limitations](https://adk.dev/tools-custom/confirmation/#known-limitations) made a code path the safer choice | I2 test |
| D3 | Per-customer scope (I1) | Gateway verifies the booking-site token and writes `customer_id` and `salon_id` into session state that the client cannot set. Tools never accept a customer ID | Identity comes from trusted code, not the model | Depends on A5 | Cross-customer denial (G04) |
| D4 | At most one effect per Confirm (I3) | A `operations` row (`operation_id`, `customer_id`, canonical payload, status `pending → dispatching → done / failed / uncertain`, expiry 10 min). A claim moves it `pending → dispatching` atomically. Status `uncertain` is reconciled by an idempotency lookup or by listing the customer's appointments, and is **never re-sent blind** | A retry, a double click or a restart refer to the same operation | Needs a DB, and A6 is open | G03 tests. G01 decides the replay contract |
| D5 | Salon policy (I4) | `policy.yaml` per salon (windows, bookable services, lead time, phone number), checked in tools and at confirm. The prompt only explains it | What the application knows belongs in code | Policy changes need a deploy (acceptable for 5 salons) | Edge tests at 23 h 59 min and 24 h 01 min |
| D6 | Sessions and operations survive restarts and several instances | `DatabaseSessionService` and the app tables on one small Cloud SQL Postgres (provisional, A10) | One store, supported by ADK | About US$10–30 a month fixed (unverified, check the pricing calculator). Firestore was the alternative | Restart test in G07 |
| D7 | Hosting a small public API | One Cloud Run service per environment (staging, prod) with its own service account. Booking API credential in Secret Manager | Smallest operational load for 3 devs | Cold starts. min-instances=1 in prod is a cost choice | G07 deploy readback |
| D8 | Stable model behaviour across the plan | `gemini-3.8-flash` on Vertex AI, pinned. Lifecycle table `model-lifecycle-2026-10-01.json` (checked 2026-10-08) lists it stable with no shutdown or Vertex retirement date. Avoid 3.6 and 3.7 flash, which retire on Vertex 2026-11-19 and 2027-01-28. Fallback candidate: `gemini-3.5-flash` (Vertex retirement 2027-05-19 or later) | Newest stable, and no migration falls inside the horizon | Not yet measured on our cases | G09 compares both before freezing |
| D9 | Spend stays safe (I5) | `RunConfig.max_llm_calls=12` per turn. 30 turns a customer a day, counted in Postgres. A `ASSISTANT_ENABLED` kill switch. A GCP budget alert at the A3 figure (an alert, not a cap) | Covers a runaway turn and a heavy user | A legitimate heavy user gets the phone number | G04 test |
| D10 | Customers use it on the existing site | Custom JSON API (`POST /chat`, `POST /confirm/{id}`, `GET /operations/{id}`). No streaming in phase 1 | Fewest moving parts. The card comes from data, not from model text | No token streaming (replies take a few seconds) | G05 manual journey |
| D11 | Personal data minimised | Logs hold IDs, status and token counts only. ADK and OpenTelemetry content capture off. Sessions deleted after 30 days (manual in phase 1, a job in G15) | Floor | Harder debugging without transcripts | Log inspection in G11 |
| D12 | Learn safely before scaling | Go live at one salon behind the per-salon flag | Limits the blast radius | Slower rollout | G11 go/no-go |

**Versions.** No ADK is installed here. The working assumption is
`google-adk==2.8.0`, the version the specialists' `compatibility.md` files were
checked against. Confirming against the chosen pin is an acceptance item of G02.

### Model-facing contracts

| Surface | Contract | Skill and verification |
| --- | --- | --- |
| Instruction | Intent understanding, clarifying ambiguous dates or appointments, and choosing only offered slots. Today's date, the salon timezone and the salon name are injected from state, not guessed | `adk-agent-instructions`; rendered-request test |
| Tools (about 6) | `list_services`, `find_slots`, `list_my_appointments`, `propose_booking`, `propose_move`, `propose_cancel`. Inputs are primitives. Results are bounded dicts with `status` and actionable errors. Slot and appointment IDs come only from earlier tool results | `adk-tool-interface-design`; declaration dump |
| Output | Plain text reply. No `output_schema`, because the card is built from the operation record | `adk-model-and-output-contracts`; pin check |

## Data and authority

| Data / operation | Owner and scope | Writers / readers | Source and freshness | Lifetime |
| --- | --- | --- | --- | --- |
| Appointments, availability | Booking API (authoritative) | Confirm endpoint writes; tools read | Live at every call; rechecked at confirm | Booking API's own |
| Pending operation | Customer, by `customer_id` | Propose tools create; confirm endpoint transitions | Expires 10 min after creation | 90 days for audit |
| ADK session | Customer + session ID; ownership checked at the gateway | Runner | — | 30 days |
| Daily allowance | Customer | Gateway | Resets daily, salon timezone | 7 days |

### Security posture

| Agent | Private data | Untrusted content | Write or egress | Resolution |
| --- | --- | --- | --- | --- |
| booking_assistant | Own appointments | The customer's own text; salon-authored service text from the API | **None.** It only creates proposals | The write leg is removed (D2). Notes are capped at 200 characters of plain text |

## Budgets and capacity

The assumed load is at most about 200 conversations a day across five salons,
with about 4 model calls per turn and about 6 turns per conversation. Cost is
symbolic until G09 measures tokens per completed booking, and the figure goes
into the plan. Concurrency is low enough that one Cloud Run instance with
default concurrency covers it. Latency target (provisional): a complete reply
within 8 s at p95.

## Failure and recovery

| Failure window | Customer sees | Retained state / possible effect | Next action and owner |
| --- | --- | --- | --- |
| Another customer's appointment ID guessed | "I can't find that appointment" | Nothing | — |
| Slot taken between proposal and Confirm | "That slot was just taken", plus new slots | Operation `failed` | The customer chooses again |
| Double click or retry on Confirm | The same result | One operation, one API call | — |
| Booking API timeout or 5xx after dispatch | "We're confirming with the salon", then the result from status polling | Operation `uncertain`; the booking may exist | Reconciliation in `/operations/{id}` by lookup. Unresolved after 15 min goes to the dev on duty (runbook, G10) |
| Instance restart while `dispatching` | As above | Same | Same |
| Model unavailable, malformed reply, or call cap hit | "Sorry, please try again or call {phone}" | Session events up to the failure | None. The proposal is not acted on |
| Proposal expired | "Let's check that slot again" | Operation `expired` | Propose again |
| Kill switch or allowance exhausted | Phone number message | — | Ops |
| Customer says "cancel all my bookings" | One proposal per appointment, each confirmed separately | — | — |
| Model retirement | None (pinned) | — | G12 manifest records the date |
| Bad release | — | — | Route traffic back to the previous Cloud Run revision (G07) |

## Verification and implementation handoff

Planned checks only. Nothing has run. The checks fall into three tiers:

- **Offline:** Runner tests with a fake booking API and a scripted model
  (G02, G03, G04, G06).
- **Live:** the evaluation set on the live model against the fake API (G08, G09),
  and a staging journey against the staging booking API (G11).
- **Measured in the pilot:** the benefit hypothesis is that out-of-hours
  changes move from phone to self-service. The measure is the share of
  bookings and changes made through the assistant, with guardrails on
  "uncertain" operations and on salon complaints. The salon has no baseline;
  G01 asks for one month of phone-change counts.

Goals, owners, estimates and the cut line are in
[the plan](../plans/salon-booking-assistant.md).

## Open decisions

| Question | Why it matters | Owner / evidence | Blocks |
| --- | --- | --- | --- |
| A5 token verification | D3 and the whole gateway | First step of G04, against the booking site auth | Rest of G04 |
| A6 idempotency and reschedule atomicity | D4 replay contract. A non-atomic move is two effects | G01 against API docs and staging | G03 |
| A7 policy windows; A11 privacy notice | Policy config and go-live | Salon owner (W1) | G11 (G08 policy cases read `policy.yaml`, so they follow the sign-off) |
| A3 budget figure | Model choice and min-instances | Founders | G07 |
| A9 pilot salon choice | Launch | Salon owner | G11 |
