# System design: salon booking assistant (MVP)

Status: **draft**. Written in one pass without the user; every row in
[Assumed answers](#assumed-answers) is provisional, and the decisions that
depend on it are marked *provisional* below. Capacity, finish range, owners and
the cut line live in the [plan](../plans/salon-booking.md#summary-for-the-reader)
and are not restated here.

## Assumed answers

No one could be asked, so each question became a labelled assumption. Change
a row and revisit the decisions in its last column.

| # | Question I would have asked | Assumed answer | Decisions that depend on it |
| --- | --- | --- | --- |
| A1 | Where do customers talk to the assistant? | A chat widget embedded in the chain's existing website. No phone, SMS or WhatsApp in the MVP | D5, D10 |
| A2 | Do customers already sign in on the website, and can our backend verify that sign-in? | Yes: the site has customer accounts and issues a session token (JWT or similar) our backend can verify. New customers sign up on the site first. **Checked in G01**; if false, a one-time code through the booking API replaces it (G04 grows by about a day) | D3, I1 |
| A3 | What does the booking API offer for writes: idempotency keys, a reschedule endpoint, availability search, a sandbox, lookup of a customer's appointments? | Availability search, book, cancel, reschedule and list-by-customer exist; a sandbox exists; **no idempotency keys** (we design for the worst case). The team owns the API. **Checked in G01** | D2, D4, I3 |
| A4 | Team hours and familiarity? | Three full-time developers, about 6 focused hours a day each, fluent in Python, comfortable with GCP, **new to ADK** (estimates ×1.5) | Plan only |
| A5 | Money for models and cloud? | About USD 300 a month for the MVP; a Cloud Billing budget alert at 50/90/100% | D8 |
| A6 | Are there deposits, cancellation fees or anything that moves money? | No money moves through this flow. Salon policy: free cancellation or move up to 24 h before; inside 24 h the assistant gives the salon's phone number instead of acting | D2, D7 |
| A7 | Languages, jurisdiction? | English only; UK/EU, so GDPR applies (privacy notice, retention, no content in logs) | D9 |
| A8 | Who signs off going live? | The chain's operations manager approves the privacy notice text, the pilot salon and a 15-minute staff briefing; allow 2–4 working days for the answer (W1 in the plan) | D11, G10 |
| A9 | Expected traffic? | Up to about 300 conversations a day across five salons, peaks on Monday mornings | D5, D8 |
| A10 | Launch everywhere at once, or one salon first? | One pilot salon at the end of phase 1, the other four when the go-live criteria in G10 hold | D11 |
| A11 | Existing GCP project? | Yes, with billing; Vertex AI and Cloud Run may be enabled in it; the booking API is reachable from Cloud Run | D5, D6 |
| A12 | Can customers pick a stylist? | Optional preference passed to availability search | D7 |

## Purpose and constraints

**Journey (running example).** Maya, a signed-in customer, opens the chat on
the website on Sunday evening and types "can I move my Thursday colour
appointment at Camden to Saturday morning?". Today she must phone during
opening hours or find the appointment in a booking page that cannot reschedule,
so salons spend reception time on moves and lose cancelled slots that nobody
refills. Intended outcome: the assistant finds her Thursday appointment, offers
the Saturday morning slots for the same service, shows a card "Move Colour with
Priya, Camden: Thu 16 Oct 14:00 → Sat 18 Oct 10:30 — Confirm / Not now", and
after she presses Confirm the booking API moves it and the card shows the
confirmed time from the API's receipt.

**Fixed constraints:** the existing booking API is the only system of record for
appointments; two weeks to the first real customers; three developers; the
product keeps being improved afterwards, so phase 1 code is kept.

**Non-goals for the MVP:** payments and deposits, marketing messages, staff-side
features, voice, languages other than English, memory of preferences beyond what
the booking API stores.

**What the model decides, what code controls.** The model interprets the
request, asks for missing details, chooses which read tool to call and which
change to propose. Code owns customer identity, the date and time zone, which
appointments belong to the customer, the 24-hour policy, the pending proposal,
the customer's confirmation and every write to the booking API.

**Outcome to improve (hypothesis, unmeasured):** share of moves and
cancellations done without a phone call, and refilled cancelled slots.
Baseline: reception call log for two weeks before the pilot (requested with W1 in the
plan). Guardrail: no rise in no-shows or in "wrong
appointment" complaints.

## Delivery constraints, depth and deferred controls

| Scope-gate answer | Value |
| --- | --- |
| First useful version due, and after | Two weeks (10 working days) from start; continued (A4) |
| People and hours | Three developers, ~6 focused h/day, new to ADK (A4). The team runs it afterwards |
| Money | ~USD 300/month (A5) |
| Users, and what they read | External customers of five salons, using the chat; the operations manager reads the go-live checklist |
| Data and effects | Real personal data (name, contact, appointment history); reversible writes to real appointments that salon staff and customers see; no money (A6) |
| Profile | **MVP or pilot**: first external users, real data, real writes; staged to one salon first (A10) |

| Concern | Depth now (phase 1) | Trigger that raises it |
| --- | --- | --- |
| Core judgment, measured | Build: 30-case labelled evaluation set run locally before go-live (G07) | Eval in CI in phase 2 (G11) |
| Customer identity and scope | Build: verified website sign-in, own appointments only (D3) | — |
| Secrets and credentials | Build: Secret Manager, Cloud Run service account, no keys in code (G08) | Rotation when the team grows or a key leaks |
| External writes | Build: customer-confirmed proposals, durable operation record, reconcile-before-retry (D2, D4) | Reconciliation job in phase 2 (G13) once uncertain outcomes are measured |
| Sensitive data | Build at MVP depth: field minimisation, no content in logs, 30-day session deletion (D9) | Model Armor / SDP screening if free text from staff or a second channel enters the context |
| Prompt injection and agency | Build: trifecta check, no egress, no model-reachable write (D2, security posture) | Adversarial suite in CI with phase 2 eval gate |
| Budgets and loop limits | Build: per-invocation call cap, per-customer daily allowance, kill switch, budget alert (D8) | Shared admission store if replicas > 1 cause oversubscription |
| Memory and retrieval | ADK sessions only; no long-term memory | Customers asking for "my usual" repeatedly → preferences profile (later) |
| Frontend | Build: widget, completed JSON, proposal cards (D10) | Streaming when p50 complete response > 6 s |
| Hosting | One Cloud Run service with rollback to previous revision (D5) | — |
| Observability | Minimal: structured logs, token use and operation outcome per invocation, one log-based dashboard (G08) | Traces and SLO alerts in phase 2 (G12) before all five salons |
| Release engineering | Minimal: pinned model, prompt in git, release manifest, local eval before deploy | Eval gate in CI (G11) |
| Performance and cost tuning | Defer | Measured cost > USD 0.05 per conversation or p50 > 6 s |

**Floor kept:** no secrets in source, prompts or logs; `RunConfig.max_llm_calls`
and a budget alert plus kill switch; no booking change without the customer
pressing Confirm on a card showing the exact details; only the signed-in
customer's data reaches the model; model ID pinned (D6). No accepted risks.

**Who may use phase 1:** signed-in customers of the pilot salon, then all five
salons once G10's go-live criteria hold. **Graduation conditions** before more
salons, a second channel or marketing traffic: evaluation gate in CI (G11),
traces and alerts (G12), uncertain-operation reconciliation (G13).

## Guarantees and acceptance

| ID | Invariant | Enforcing component and authority | Failure outcome | Planned verification |
| --- | --- | --- | --- | --- |
| I1 | A customer sees and changes only their own appointments | Gateway verifies the website token and writes `customer_id` into trusted session state; tools read it from state, never from arguments; the confirm endpoint re-reads the appointment from the booking API and checks its owner | "I can't find that appointment" with no detail; nothing written | Offline: tool called with another customer's appointment ID returns not-found; confirm with another customer's token returns 403 and no API write (G04, G05) |
| I2 | No book, move or cancel without the customer pressing Confirm on a card showing salon, service, stylist, old and new time | The model has no write tool; `propose_*` tools only store a pending proposal; `POST /operations/{id}/confirm` is the only path to a write and takes no model input | Proposal expires after 15 min; nothing written | Offline: scripted model calls every tool and tries "just book it"; booking fake records zero writes until confirm (G05) |
| I3 | One confirmed proposal causes at most one booking-API effect, through double clicks, client retries, timeouts and restarts | Operation record in Postgres with a state machine and a unique proposal ID; reconcile by lookup before any retry (D4) | Card shows "Confirmed" or "We're checking this with the salon" — never a second booking | Offline: double confirm, and a fake that commits then times out, each give exactly one fake booking (G03, G05) |
| I4 | The customer is told an appointment is booked, moved or cancelled only from the booking API's receipt | Card status rendered from the operation record, not model text; instruction forbids claiming completion | Card shows the true state even if the model's text is wrong | Eval cases where the model must not claim success before confirm (G07); widget test (G06) |
| I5 | Spend and abuse are bounded | `max_llm_calls`, per-customer daily turn allowance in Postgres, kill switch, budget alert (D8) | "The assistant is busy, call the salon" | Offline: 41st turn of the day refused without a model call (G08) |
| I6 | No conversation content or contact details in logs | Logging filter on structured fields only; ADK content capture off | — | Log capture test on a full conversation finds no message text or phone/email pattern (G08, G09) |

## Architecture and decisions

```text
Browser widget ──HTTPS──▶ Cloud Run: assistant service (FastAPI)
  (site session token)      ├─ gateway: verify token → customer_id, allowance, kill switch
                            ├─ ADK Runner + one LlmAgent (Vertex AI, pinned model)
                            │     read tools ─────────────────────▶ Booking API (reads)
                            │     propose_* tools ─▶ operations table (status=proposed)
                            ├─ POST /operations/{id}/confirm ─────▶ Booking API (write)
                            │     (no model involved)               ▲ receipt
                            └─ Cloud SQL Postgres: ADK sessions, operations, allowances
```

| ID | Requirement | Design choice | Reason | Tradeoff / alternative | Verification | Status |
| --- | --- | --- | --- | --- | --- | --- |
| D1 | Interpret free-text booking requests over a small set of capabilities | **One `LlmAgent`** with about seven function tools; no sub-agents | One responsibility, one context, one tool set; nothing for a second agent to own | Less modular than a router + specialists, which would add routing errors and evaluation surface for no boundary | Tool count ≤ 8 in a declaration dump; eval selection accuracy (G07) | proposed |
| D2 | I2 and I4: writes to real appointments only with the customer's approval | **Propose → confirm in code.** `propose_booking`, `propose_move`, `propose_cancellation` validate and store a proposal bound to exact details and return its summary; the widget renders a card; the confirm endpoint rechecks owner, 24-hour policy (A6) and slot availability, then writes | Approval is a UI action the model cannot forge, bound to stored details, testable without a model | Needs a card in the widget and a second endpoint. ADK's native tool confirmation was the alternative; rejected for the MVP because we would still need the recheck and binding in our code, and its limitations must be checked against the pin | I2 test; a slot taken between propose and confirm returns "no longer available" and new options (G05) | proposed |
| D3 | I1 | **Trusted customer scope** from the website's verified token, placed in session state by the gateway; session IDs bound to the customer; tools have no `customer_id` parameter | A conversation ID or appointment ID is a locator, not permission | Depends on A2. Fallback: one-time code via booking API, +~1 day in G04 | I1 tests (G04) | **provisional (A2)** |
| D4 | I3 under a booking API without idempotency keys (A3) | **Durable operation record**: `proposed → executing → succeeded / failed / uncertain`, claimed atomically; on timeout or 5xx, look up the customer's appointments for the same salon, service and start time before any retry; move uses the API's reschedule endpoint; if it has none, book the new slot first, then cancel the old one, recording both effects | A retry after a lost reply cannot prove the first call failed; lookup can | Lookup can be ambiguous (two identical bookings) → `uncertain`, shown honestly, staff runbook (G10). If the API has idempotency keys, use the operation ID as the key and keep the lookup as a check | Fake that commits then times out; double confirm; restart between claim and write (G03) | **provisional (A3)** |
| D5 | Host an API, the confirm endpoint and the widget backend for ~300 conversations/day | **One Cloud Run service** (FastAPI around the ADK `Runner`) + **Cloud SQL for PostgreSQL** (small instance) for ADK `DatabaseSessionService`, operations and allowances | The team needs custom endpoints and a gateway anyway; one service and one database is the least to operate | Agent Runtime would manage sessions but still need our gateway and confirm service; Firestore is cheaper at idle but would split stores. Cloud SQL costs a fixed monthly amount | Restart test: a session and a pending proposal survive a revision restart (G08) | proposed |
| D6 | Stable behaviour across the plan's horizon | **`gemini-3.8-flash` on Vertex AI**, pinned, low temperature; no `output_schema` (cards come from tool results, not model JSON). Lifecycle table `model-lifecycle-2026-10-01.json`, checked_on 2026-10-08: stable since 2026-09-02, no shutdown or Vertex retirement listed. Avoid 3.6-flash (Vertex retirement 2026-11-19), 3.7-flash (2027-01-28) and the 2.5 family (2026-10-20) | Newest stable Flash with no retirement inside the plan | Quality for this task is unmeasured until G07; 3.5-flash (Vertex retirement 2027-05-19 or later) is the fallback | Confirm the ID and region against Vertex documentation on the day of G02; eval result (G07) | proposed; ID re-check needed |
| D7 | The model must not invent dates, slots or policy | Today's date and the salon's time zone injected into state per turn; `find_slots` takes an ISO date range, service and optional stylist, returns at most 10 slots with IDs; proposals accept only slot IDs returned in this session, checked in code; 24-hour rule enforced in code (A6, A12) | "Saturday morning" is language; the actual slot is data | The model sometimes asks one more clarifying question | Eval cases on relative dates around midnight and DST (G07); unit test of the 24-hour rule (G05) | proposed |
| D8 | I5 and the spend floor on a public service | `RunConfig.max_llm_calls=8` per turn (provisional), 40 turns per customer per day and at most 2 open proposals, both in Postgres; `ASSISTANT_ENABLED` per salon in config as kill switch; Cloud Billing budget alert at USD 150/270/300 (alerts only, not a cap) | Admission in our code is the only real stop; the alert only observes | A single Postgres counter is fine at one or a few instances; reconsider if replicas grow | I5 test; kill-switch test (G08) | proposed |
| D9 | GDPR and I6 | Tool results carry only first name, salon, service, stylist first name, times; free-text appointment notes dropped; logs carry IDs, tool names, status, tokens; ADK sessions deleted after 30 days by a scheduled job; privacy notice linked in the widget | Minimisation is cheaper than screening | No transcript for debugging beyond 30 days; screening (Model Armor) deferred | I6 test; deletion job test against a dated fixture (G08/G09) | proposed |
| D10 | Customers see clear options and an unambiguous result | Widget calls `POST /chat` and gets completed JSON: assistant text plus zero or more cards (slots, proposal, operation status) built by code from tool results and operation records | Cards come from data, so a wrong sentence cannot change a booking or its displayed status | No streaming; a 3–6 s wait shows a typing indicator | Widget test renders proposal and status from fixtures (G06) | proposed |
| D11 | Limit the blast radius of the first release | Per-salon enable flag; pilot at one salon; go-live criteria in G10 | Problems reach one salon's customers first | The other four wait a few days | G09 checklist | **provisional (A8, A10)** |

**Versions.** No installed ADK exists. Working assumption: **google-adk 2.8.0**
on Python 3.11, the version the specialists were checked against
(`deploy-adk-on-google-cloud/references/compatibility.md`,
`adk-model-and-output-contracts/references/compatibility.md`). Confirming the
pin, `DatabaseSessionService` against Postgres and `RunConfig.max_llm_calls` on
it is an acceptance item of G02. No provider facts were looked up online in this
session; region availability of the model and Cloud SQL prices are unverified.

### Model-facing contracts

| Surface | Contract | Implementing skill and verification |
| --- | --- | --- |
| Instruction | Scope (the five salons, these three actions), ask for missing service/date, never claim a change happened — the card shows it, inside 24 h give the salon number, refuse off-topic briefly. Date, time zone, salon list and customer first name come from state, not prose | `adk-agent-instructions`; rendered-request test (G07) |
| Tools (read) | `list_services(salon_id)`, `find_slots(salon_id, service_id, date_from, date_to, stylist?)`, `list_my_appointments()` | `adk-tool-interface-design`; declaration dump, bounded results (G02) |
| Tools (propose, no effect) | `propose_booking(slot_id)`, `propose_move(appointment_id, slot_id)`, `propose_cancellation(appointment_id)`; return `{status, proposal_id, summary}` or an actionable error | `adk-tool-interface-design`; I2 test (G05) |
| Output | Plain text; no `output_schema` | `adk-model-and-output-contracts` for D6 only |

## Data and authority

| Data / operation | Owner and scope | Writers / readers | Source and freshness | Lifetime / erasure |
| --- | --- | --- | --- | --- |
| Appointments, availability, customer record | Booking API; per customer | Confirm endpoint writes; tools read | Authoritative, read live each time | Booking API's own policy |
| ADK session (conversation) | Assistant; bound to `customer_id` | Runner | Not authoritative for bookings | Deleted 30 days after last activity |
| Operation record | Assistant; per customer | Propose tools, confirm endpoint | Authoritative for "what we asked and what the API said" | 13 months (dispute window, assumption), customer IDs only |
| Daily allowance counters | Assistant | Gateway | — | 7 days |

Three identities: the **customer** (website token, verified in the gateway), the
**Cloud Run service account** (calls Vertex AI and Cloud SQL), and the
**booking API credential** (a service credential in Secret Manager; it can act
for any customer, so I1 rests on our gateway and the confirm endpoint's owner
check — G01 asks whether the API can also take the customer token).

### Security posture

| Agent | Private data | Untrusted content | Write or egress | Resolution |
| --- | --- | --- | --- | --- |
| Booking agent | Yes: the signed-in customer's own appointments | The customer's own messages (the principal); booking-API free text removed (D9) | No model-reachable write or egress; writes happen only after a UI confirm (D2) | Write leg removed from the agent; scope enforced in code (D3) |

Tool tiers: read (three tools), propose (no effect), write (confirm endpoint
only, outside the agent). No code executor. Adversarial cases in G09: "cancel
all appointments for Anna Smith", an appointment ID from another customer, a
slot ID never offered, a message claiming to be salon staff, and a
confirm request replayed after expiry — each asserts no booking-API write.

## Budgets and capacity

Per customer turn: 1–3 model calls expected, at most 8 (D8); 0–3 booking-API
reads; no retries by our code on model calls beyond the SDK default (G02
records what that default is at the pin). Assumed ~300 conversations/day × ~4
turns (A9). Cost is symbolic because prices were not looked up: conversations ×
turns × calls × (input tokens × input price + output tokens × output price) +
Cloud SQL fixed monthly + Cloud Run. G08 measures tokens per conversation in
staging; the plan's G12 turns it into cost per completed booking. Latency
target (assumption): complete reply p50 ≤ 6 s, measured in G10.

## Failure and recovery

| Failure window | What Maya sees | Retained state / possible effects | Safe next action and owner |
| --- | --- | --- | --- |
| Booking API times out after it committed the move | Card: "We're checking this with the salon" | Operation `executing`; the move may exist | Confirm endpoint looks up her appointments; if the new time exists → `succeeded`; if ambiguous → `uncertain`, staff runbook (G10); never a blind retry |
| Slot taken between proposal and Confirm | "That time was just taken" + fresh slots | Proposal `failed`, no write | Customer picks again |
| Move without a reschedule endpoint: new booking succeeds, cancel of old fails | Card: "Booked Sat 10:30; your Thursday appointment is still booked — we've told the salon" | Both effects recorded | Retry cancel once via lookup; else `uncertain` for staff |
| Double click / browser retry on Confirm | One confirmed card | One operation, claimed atomically | — |
| Cloud Run instance replaced mid-confirm | On reload, card shows the operation's current state | `executing` row with no receipt | Next status read triggers lookup-reconcile (G03); scheduled sweep in phase 2 (G13) |
| Customer asks about another person's appointment | "I can only help with your own appointments" | Nothing | — |
| Vertex AI unavailable or call cap hit | "I can't help right now — call Camden on …" | Session kept; no proposal | Retry later; alert in phase 2 |
| Allowance exhausted or kill switch on | Same message, no model call | — | Ops manager / on-call dev flips the flag |
| Release while a proposal is pending | Proposal still confirmable on the new revision | Operations table unchanged; schema migrations additive only in phase 1 | Roll back by routing traffic to the previous revision |
| Token expired mid-conversation | Widget asks her to sign in again | Session retained under her `customer_id` | — |

Not applicable: streaming partial output (D10), long-term memory, A2A/MCP peers,
analytical queries, deferred jobs other than the deletion sweep.

## Verification and handoff

Offline deterministic tests against a booking-API fake carry I1–I6 (G02–G06).
Local integration: a real Postgres in a container for restart and double-confirm
(G03, G05). Bounded live: the booking-API sandbox and Vertex AI in staging
(G08, G10). Release evidence for the pilot: the G10 go-live checklist. Release
manifest (G08): image digest, prompt version, model ID, tool-schema hash,
eval-set hash, secret versions. Rollback unit: the previous Cloud Run revision,
kept ready for the pilot week.

Goals, owners, estimates and run prompts: [plan](../plans/salon-booking.md).

## Open decisions

| Question or assumption | Why it changes the design | Owner / evidence needed | What it blocks |
| --- | --- | --- | --- |
| A2 website sign-in verifiable? | Decides D3 and G04's size | G01 reads the site's auth; tech lead | G04 scope |
| A3 idempotency, reschedule, sandbox | Decides D4's retry path and the move failure row | G01 reads the API; Dev B | G03 route |
| A6 cancellation policy and fees | A fee would make cancellation a money effect | Operations manager | G05 rule |
| A8/A10 pilot salon and sign-off | Go-live date | Operations manager (W1) | G10 |
| D6 model ID in the chosen region | Pinned model | G02 checks Vertex docs | G02 |
