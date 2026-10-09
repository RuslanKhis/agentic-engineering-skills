# Implementation plan: salon booking assistant

Status: draft. Ready goals are identified, but they rest on the assumed answers
A1 to A13.
Architecture: [docs/architecture/salon-booking-assistant.md](../architecture/salon-booking-assistant.md)
Continuation source of truth: this plan. The tickets in
`docs/tickets/salon-booking-assistant/` are copies for parallel work, and a
ticket's Evidence section is where its results are recorded.

## Destination and constraints

**Destination.** On 2026-10-23, signed-in customers of the five salons can book,
move and cancel appointments by chatting on the website. Every change goes
through a confirmation card and the existing booking API.

**Non-goals:** payments, SMS or WhatsApp, staff tools, memory of preferences,
other languages.

**Repository facts** (inspected 2026-10-09): there is no application code yet.
The repository holds only `.claude/skills/`. Every module path below is a
**proposed** layout.

**Pins the goals inherit:**
- Model `gemini-3.8-flash` on Vertex AI.
- google-adk 2.8.0 as the working assumption, to be confirmed in G01.
- The prompt is versioned in `app/prompts/booking_assistant.md`.

A goal that changes one of these is a release, not a side effect.

**Authorization.** This session was design only. Running the goals locally is
authorized by running their prompts. Any GCP provisioning, deployment or
booking-API production write in G07 needs the user's explicit go-ahead, with the
project and region named.

Proposed layout:

```text
app/
  agent.py            # LlmAgent factory, App/Runner wiring, RunConfig
  prompts/booking_assistant.md
  tools/booking.py    # 6 function tools (read + propose)
  booking_api/client.py   # HTTP client: timeouts, retries, idempotency
  booking_api/fake.py     # in-memory fake for tests and evals
  operations/ledger.py    # operation records + state machine (Postgres)
  operations/executor.py  # confirm → dispatch → reconcile
  gateway/main.py     # FastAPI: auth, /chat, /operations/{id}/confirm, limits
  web/widget/         # embeddable chat widget
tests/  evals/
```

## Delivery profile and capacity

Profile: **MVP** (see the design's delivery section).

| Phase | Delivers | Goals | Estimate (focused h) | Capacity and reserve |
| --- | --- | --- | --- | --- |
| 1, ship | Customers book, move and cancel safely on the live site | G00 to G07 | 65 to 94 | 3 × 10 d × 7 h × 0.6 ≈ 126. Reserve 30 h leaves 96. **Fits at the high end, with little margin.** |
| 2, harden | Graduation conditions: eval gate, traces/SLIs, retention, adversarial suite, handoff to staff | G08 to G12 | 40 to 60 | Weeks 3 to 5, as time allows |

Estimates are assumptions for a team new to ADK. If the work runs high, these
move to phase 2, in this order:
1. The per-IP limiter in G06 (Cloud Armor later).
2. G05 cut to 12 cases.
3. The widget polish in G04 (the plain-HTML card stays).

The floor items in G02, G03 and G06 never move. If the team shrinks, the goals
stay useful in this order: G00 → G01 → G02 → G03 → G06 → G04 → G07 → G05. The
evaluation still runs before launch, at reduced size.

### Who could take which

The people are not named in the request, so the three roles are assumptions.
Match them to whoever fits best.

| Developer | Profile assumed | Goals | Hours (range) |
| --- | --- | --- | --- |
| **Dev A** | Knows the booking API best | G00, G02, G06 | 23 to 31 |
| **Dev B** | Agent and Python | G01, G03, G05 | 22 to 31 |
| **Dev C** | Web and infra | G04, G07 | 22 to 32 |

**Calendar (assumed start Mon 2026-10-12):**

*Days 1 and 2.*
- A runs G00 and starts the fake API.
- B starts G01 against the fake.
- C builds the G04 gateway skeleton and requests the GCP and Secret Manager
  access that G07 needs.

*Days 3 to 6.*
- A builds G02.
- B runs G03 once the A6 answer is in, then G05.
- C works on the G04 widget and card, and stands up G07 staging.

*Days 7 to 8.*
- Integration on staging: G06 and the G05 eval run.

*Day 9.*
- Production deploy, then a test booking at one salon.

*Day 10.*
- Enable the remaining salons (one salon first is recommended; see the open
  decisions), and keep the reserve.

## Implementation map

| Decision | Component and integration point (proposed) | GCP | Primary skill | Verification still needed |
| --- | --- | --- | --- | --- |
| D1 | `app/agent.py` `LlmAgent` + `App`/`Runner` with `RunConfig(max_llm_calls=8)` | Vertex AI | adk-workflow-design | Constructor names against the 2.8.0 pin |
| D2, D3 | `tools/booking.py` propose tools → `operations/ledger.py`. `gateway` confirm route → `executor.py` → `booking_api/client.py`. | Cloud SQL | safe-api-tool-calls | API idempotency and reschedule (G00) |
| D4 | `gateway/main.py` verifies the site session, then `session.state["app:customer_id"]`-style trusted key (final key prefix chosen in G03). Tools read it from `ToolContext.state`. | — | adk-tool-auth-and-secrets | Token verification method (A6) |
| D5 | `tools/booking.py` docstrings and bounded results | — | adk-tool-interface-design | Declaration size |
| D6 | Dockerfile, `DatabaseSessionService` URL, Secret Manager env | Cloud Run, Cloud SQL, Secret Manager, Vertex AI | deploy-adk-on-google-cloud | Region and model availability, price |
| D7 | `gateway` `/chat` JSON + `web/widget` | — | adk-frontend-integration | Browser check |
| D8 | `gateway` counters + RunConfig + quota/alert | Billing budget, Vertex quota | adk-operational-guardrails | Scripted loop test |
| D9 | JSON logger in the gateway and executor | Cloud Logging | adk-agent-observability | No-content log readback |
| D10 | `evals/` set against `booking_api/fake.py` | — | adk-agent-evaluation | Recorded run |

## Goals and dependencies

| ID and goal | Phase | Type | Estimate | Depends on | Primary skill | State |
| --- | --- | --- | --- | --- | --- | --- |
| G00 Booking API contract check | 1 | discovery | 3 to 5 | — | safe-api-tool-calls | ready |
| G01 Agent finds real availability locally | 1 | impl | 8 to 10 | — (uses fake until G00) | adk-workflow-design | ready |
| G02 Confirmed book/move/cancel, exactly once | 1 | impl | 14 to 20 | G00, G01 | safe-api-tool-calls | blocked: G00 |
| G03 Customers see only their own bookings | 1 | impl | 8 to 12 | G01, A6 answer | adk-tool-auth-and-secrets | ready (provisional A6) |
| G04 Chat widget with confirmation card | 1 | impl | 12 to 18 | G01 (API shape), G02 for confirm | adk-frontend-integration | ready (skeleton) |
| G05 Pre-launch eval set | 1 | impl | 6 to 9 | G01, G02 | adk-agent-evaluation | blocked: G02 |
| G06 Spend and abuse limits | 1 | impl | 4 to 6 | G04 | adk-operational-guardrails | blocked: G04 |
| G07 Staging and production on Cloud Run | 1 | impl | 10 to 14 | G02, G03, G04, G06; user go-ahead | deploy-adk-on-google-cloud | blocked: goals + authorization |

### G00 — Booking API contract check

- **Phase and estimate:** 1; 3 to 5 h.
- **Outcome and linked decisions:** answers A6 and A7 so that D3 and D4 can be
  final.
- **Scope:** check, on the staging API:
  - availability search;
  - create, cancel, and reschedule (if it exists);
  - list-by-customer;
  - idempotency-key support and its retention;
  - error codes for a slot conflict and for a rule violation;
  - rate limits and timeouts;
  - how a customer session is verified.

  Count the real daily bookings per salon so the D8 numbers can be replaced.
  No code beyond probe scripts.
- **Depth:** discovery only, on the staging API. No production calls.
- **Implementation route:** `docs/architecture/booking-api-contract.md` (new),
  which records each answer with its evidence (a request or response sample,
  redacted). Update the design's A6, A7 and D3 rows.
- **Prerequisites:** a staging URL and a credential, held in local env and never
  committed.
- **Primary skill:** safe-api-tool-calls.
- **Supporting skills:** adk-tool-auth-and-secrets (session verification method).
- **Acceptance:** each A7 question has a yes/no answer with evidence. The move
  strategy is chosen (reschedule endpoint, or create-then-cancel). The
  reconciliation lookup is identified. Stop after 5 h, and record any remaining
  unknowns as risks.
- **Verification:** the contract note is reviewed by Dev A and Dev B.
- **Execution scope:** staging only.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out docs/tickets/salon-booking-assistant/G00-booking-api-contract.md.`

### G01 — Agent finds real availability locally

- **Phase and estimate:** 1; 8 to 10 h.
- **Outcome:** in `adk web`, "any colour slots at Northside Saturday morning?"
  returns real slots from the fake API, and from the staging API once G00 is done.
- **Scope:**
  - In: `agent.py`; the prompt file; the 3 read tools; `booking_api/client.py`
    (reads only); `booking_api/fake.py`.
  - Out: the propose tools (G02).
- **Depth:**
  - Pinned model.
  - `max_llm_calls=8`.
  - Today's date and the time zone injected by code.
  - Tool results capped at 10 slots.
- **Implementation route:** `LlmAgent` + `App`/`Runner`. The tools use the
  `ToolContext` state. Confirm the ADK 2.8.0 interfaces against the chosen pin.
- **Prerequisites:** none. The fake API is enough to start.
- **Primary skill:** adk-workflow-design.
- **Supporting skills:**
  - adk-tool-interface-design: tool declarations.
  - adk-agent-instructions: prompt and state templating.
  - adk-model-and-output-contracts: model pin and settings.
- **Acceptance:**
  - Scripted-model Runner test: the read tools are called with valid arguments.
  - An ambiguous salon leads to a clarifying question, not a guess.
  - The declaration dump is under 3 KB.
  - The ADK pin is recorded.
- **Verification:** `pytest tests/test_agent_reads.py` (offline). One `adk web`
  session on the pinned model as a bounded live check.
- **Execution scope:** local, plus the model API under the existing allowance.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out docs/tickets/salon-booking-assistant/G01-agent-reads-availability.md.`

### G02 — Confirmed book/move/cancel, exactly once

- **Phase and estimate:** 1; 14 to 20 h.
- **Outcome:** Maya's move happens only after Confirm, and happens once, even
  after a double click or a lost reply (I2, I3, I4; D2, D3).
- **Scope:**
  - In:
    - the three propose tools;
    - the ledger table and state machine;
    - the executor;
    - the write methods of `client.py`;
    - reconciliation by lookup;
    - the partial-move path.
  - Out: the UI (G04).
- **Depth:**
  - Idempotent writes.
  - Bounded retry, only after reconciliation.
  - Proposals expire after 10 min.
  - A front-desk flag, logged, for `uncertain` and partial-move outcomes.
- **Implementation route:**
  - Propose tools validate `slot_id` and `appointment_id` against fresh reads,
    then insert a `proposed` row.
  - `executor.confirm(operation_id, customer_id)` claims the row atomically,
    dispatches it, and records the receipt.
- **Prerequisites:** G00 and G01.
- **Primary skill:** safe-api-tool-calls.
- **Supporting skills:**
  - adk-tool-interface-design: the propose tools.
  - adk-operational-guardrails: binding the confirmation to the stored details.
- **Acceptance:**
  - Against the fake API, a full conversation without a confirm makes zero
    writes.
  - A double confirm leads to 1 create.
  - A timeout on create triggers a lookup, and the result is 1 booking or
    `uncertain`.
  - A 409 conflict leads to `failed:conflict`.
  - Confirming someone else's operation is denied.
  - A partial move leaves both bookings recorded and flagged.
- **Verification:**
  - `pytest tests/test_operations.py` (offline).
  - One book, move and cancel on staging (local integration).
- **Execution scope:** fake API and staging API.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out docs/tickets/salon-booking-assistant/G02-confirmed-writes-exactly-once.md.`

### G03 — Customers see only their own bookings

- **Phase and estimate:** 1; 8 to 12 h.
- **Outcome:** the gateway derives `customer_id` from the verified website
  session and the tools never accept it as an argument (I1, D4).
- **Scope:**
  - In:
    - the auth dependency in `gateway/main.py`;
    - session creation keyed to the customer;
    - a session-ownership check on every `/chat` call;
    - reading `customer_id` from state in the tools.
  - Out: OTP or guest flow (later).
- **Depth:** build. Verified identity with cross-customer denial tests.
- **Implementation route:** FastAPI dependency → `Runner.run_async(user_id=customer_id, session_id=…)`.
  The trusted state key is written only by the gateway.
- **Prerequisites:** G01, and the A6 answer (G00 confirms it).
- **Primary skill:** adk-tool-auth-and-secrets.
- **Supporting skills:** adk-agent-security (scripted-model forbidden-access
  test).
- **Acceptance:**
  - Customer X cannot list or propose on Y's appointment.
  - A session ID belonging to another customer is rejected with 403.
  - An expired token is rejected with 401.
  - No tool declaration has a customer parameter.
- **Verification:** `pytest tests/test_identity.py` (offline).
- **Execution scope:** local.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out docs/tickets/salon-booking-assistant/G03-customer-scope.md.`

### G04 — Chat widget with confirmation card

- **Phase and estimate:** 1; 12 to 18 h.
- **Outcome:** a customer chats in a widget on the website and sees a card,
  rendered from the ledger, with Confirm and Cancel buttons (D7, I4).
- **Scope:**
  - In:
    - `POST /chat` returning `{reply_text, pending_operation?}`;
    - `POST /operations/{id}/confirm`;
    - `GET /operations/{id}`;
    - the widget, with its card states: proposed, succeeded, failed,
      uncertain, expired.
  - Out: streaming and styling beyond the basics.
- **Depth:** build, with no streaming.
- **Implementation route:** FastAPI around the Runner. The card fields come
  only from the ledger row.
- **Prerequisites:** G01. Confirm becomes live with G02.
- **Primary skill:** adk-frontend-integration.
- **Supporting skills:** none.
- **Acceptance:**
  - The card text matches the ledger, not the model's prose.
  - Every card state renders.
  - Refreshing after Confirm shows the same result.
- **Verification:**
  - API tests offline.
  - A browser check against local staging.
- **Execution scope:** local and staging.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out docs/tickets/salon-booking-assistant/G04-chat-widget-and-card.md.`

### G05 — Pre-launch eval set

- **Phase and estimate:** 1; 6 to 9 h.
- **Outcome:** a measured pass rate on 20 to 25 cases before real customers use
  it (D10).
- **Scope:** cases for:
  - booking;
  - moving;
  - cancelling;
  - ambiguous salon, service or time;
  - "next Friday" date reasoning;
  - an unavailable slot;
  - out of scope ("how much is a balayage?");
  - instructions planted in a stylist bio;
  - someone else's booking.

  All against the fake API.
- **Depth:** local run only. The CI gate is G08.
- **Primary skill:** adk-agent-evaluation.
- **Supporting skills:** adk-agent-instructions (fixing the failures).
- **Acceptance:**
  - Recorded results per case.
  - Zero cases where the model claims a booking that the ledger lacks.
  - The tool-choice pass rate is recorded as a baseline (no target is set
    before measuring).
- **Verification:** `pytest evals/` or `adk eval`, on the pinned model with a
  call cap (bounded live).
- **Execution scope:** model API under the allowance.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out docs/tickets/salon-booking-assistant/G05-prelaunch-eval-set.md.`

### G06 — Spend and abuse limits

- **Phase and estimate:** 1; 4 to 6 h.
- **Outcome:** loops, abusive customers and floods stop politely (I5, D8).
- **Scope:**
  - `max_llm_calls`;
  - a per-customer daily turn counter in Postgres;
  - a per-IP limiter;
  - the quota and budget-alert settings, written as a checklist for G07.
- **Depth:** build at the MVP level. Shared budgets come later.
- **Primary skill:** adk-operational-guardrails.
- **Supporting skills:** none.
- **Acceptance:**
  - The scripted looping model stops at the cap with a friendly message.
  - The 41st turn of the day is refused.
  - The counter survives a restart.
- **Verification:** `pytest tests/test_limits.py` (offline).
- **Execution scope:** local.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out docs/tickets/salon-booking-assistant/G06-spend-and-abuse-limits.md.`

### G07 — Staging and production on Cloud Run

- **Phase and estimate:** 1; 10 to 14 h.
- **Outcome:** the assistant serves the five salon pages from Cloud Run, using
  Cloud SQL sessions and the ledger, with rollback by revision (D6, D9).
- **Scope:**
  - Dockerfile;
  - service account;
  - Secret Manager;
  - Cloud SQL;
  - Vertex region check and a dated model price;
  - quota and budget alert;
  - JSON logs with no message content;
  - a release note with the image digest, prompt version, model ID and ADK
    version;
  - a test booking on a test customer;
  - the front-desk runbook for `uncertain` operations.
- **Depth:** minimal observability. Traces are G09.
- **Prerequisites:** G02, G03, G04 and G06, plus **the user's explicit
  authorization** of the project, region and production go-live.
- **Primary skill:** deploy-adk-on-google-cloud.
- **Supporting skills:**
  - adk-agent-observability: the log fields and the content gate.
  - adk-release-engineering: the pinned release note and rollback.
  - protect-adk-sensitive-data: the check that no PII reaches the logs.
- **Acceptance:**
  - The readback shows the revision, model ID and environment.
  - A session survives an instance restart.
  - A log sample contains no customer text.
  - Rolling back to the previous revision works.
  - The production test booking succeeds and is then cancelled.
- **Verification:** hosted checks on staging, then production, within the
  authorization.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out docs/tickets/salon-booking-assistant/G07-cloud-run-staging-and-prod.md.`

## Phase 2 (harden and graduate)

| ID | Goal | Estimate | Primary skill | Acceptance check |
| --- | --- | --- | --- | --- |
| G08 | Eval set grown from production samples, run in CI as a gate that fails by exit code. Monthly check of the model lifecycle. | 8 to 12 | adk-release-engineering | A PR that breaks a case fails CI |
| G09 | Traces (content capture off), token cost per successful booking, SLIs for completed operations and tool errors | 8 to 12 | adk-agent-observability | An exporter test shows one span per agent, tool and model call |
| G10 | 30-day session deletion job, customer erasure request, and PII review of sessions | 6 to 10 | protect-adk-sensitive-data | A deleted session is unreadable, and the ledger keeps no free text |
| G11 | Handoff to staff: "talk to the salon" creates a front-desk task, with an uncertain-operation queue UI | 10 to 16 | adk-frontend-integration | A task appears for the right salon |
| G12 | Adversarial suite: injection through API free-text fields, attempts to reach other customers | 6 to 10 | adk-agent-security | Forbidden calls never run |

## Later

| Item | Trigger | Risk accepted while it waits | Likely primary skill |
| --- | --- | --- | --- |
| Guest booking with OTP | Many customers without logins | Logged-out customers phone instead | adk-tool-auth-and-secrets |
| SMS / WhatsApp channel | Demand after launch | — | adk-frontend-integration |
| Preferred stylist memory | Repeated requests | Customers repeat their preferences | adk-memory-architecture |
| Payments and deposits | Business decision | Not offered | safe-api-tool-calls + adk-operational-guardrails |
| Streaming replies, latency tuning | p95 above 8 s, measured | Slower replies | optimise-adk-on-google-cloud |
| Cloud Armor rate limiting | Abuse seen | Per-instance limiter only | deploy-adk-on-google-cloud |
| Canary releases | Weekly prompt changes | Whole-revision rollouts | adk-release-engineering |

## Open decisions for further planning

See the design's open decisions: A6 login, A7 API features, region,
payments, and launch at one salon or all five.

## Resume here

- **Next goal:** G00, the booking API contract check. It is the only blocker of
  G02 and confirms A6. G01, G03 and the G04 skeleton can start in parallel.
- **Read first:** the design, then this plan.
- **Continuation prompt:**

```text
/adk-engineer Carry out G00 from docs/plans/salon-booking-assistant.md.
```

After that: `/adk-engineer Continue the next ready goal in docs/plans/salon-booking-assistant.md.`
