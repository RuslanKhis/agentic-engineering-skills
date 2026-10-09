# Implementation plan: salon booking assistant (MVP)

Status: draft — ready goals identified (G01, G04); product assumptions unconfirmed
Architecture: [docs/architecture/salon-booking-assistant.md](../architecture/salon-booking-assistant.md)
Continuation source of truth: this plan; tickets in
[docs/tickets/salon-booking-assistant/](../tickets/salon-booking-assistant/) copy its goals.

## Destination and constraints

A signed-in customer of any of the five salons books, moves or cancels an
appointment in a web chat, confirms on a card, and the existing booking API
holds the result. Non-goals in phase 1: payments or deposits, voice/SMS/WhatsApp,
languages other than English, staff-facing use, long-term memory. Stack
(proposed, greenfield): Python, FastAPI, `google-adk==2.8.0` (working
assumption, confirmed in G02), `gemini-3.8-flash` on Vertex AI, Cloud Run, Cloud
SQL Postgres, Secret Manager. Inherited pins: model `gemini-3.8-flash`, prompt
version `booking-v1`, no judge model (evaluation assertions are deterministic).
Authorization in this session: design only; nothing provisioned or installed.

Proposed layout (not yet created):

```text
app/
  gateway.py        # FastAPI: JWT verification, session ownership, admission
  agent.py          # LlmAgent factory, instruction booking-v1, RunConfig
  tools/read.py     # list_services, find_slots, list_my_appointments
  tools/propose.py  # propose_booking, propose_move, propose_cancel
  executor.py       # confirm endpoint logic, operation record, reconciliation
  booking_api.py    # typed client + FakeBookingApi for tests
  store.py          # Postgres tables: proposals, allowance
web/widget/         # chat widget + confirmation card
evals/              # 30 cases + runner
tests/
```

## Delivery profile and capacity

Profile: **MVP / pilot** (design, *Delivery constraints*).

| Phase | Delivers | Goals | Human hours, agent-assisted (range) | Capacity and reserve |
| --- | --- | --- | --- | --- |
| 1, ship | Real customers book, move and cancel safely via the beta link; failures and cost visible | G01–G09 | 44.5–74 | 3 people × 10 days × 6 h × 0.6 = 108 h; 25 % reserve → 81 h |
| 2, harden | CI evaluation gate, idempotent writes, SLOs and alerts, streaming, adversarial suite | G10–G14 | 19–36 (coarse) | Weeks 3–4, as time allows |

Estimates are person-hours of human effort with a coding agent (hands-on plus
review and verify) for a team new to ADK: every figure already includes the
×1.5 multiplier. Calendar waits are listed on goals, not added to hours.

| Person | Goals | Hours (from the schedule check) | Their capacity (10 days × 3.6 h) |
| --- | --- | --- | --- |
| Dev A — booking API client, agent and evaluation | G01, G02, G06, G07 | 15.5–26.5 | 36 |
| Dev B — the confirm flow, executor to card | G03, G05 | 13.5–21.5 | 36 |
| Dev C — identity, cloud and launch | G04, G08, G09 | 15.5–26 | 36 |

Who could take which: **Dev A** should be whoever knows the booking API and is
most interested in prompt and model behaviour: the client (G01) feeds the agent
(G02), whose behaviour they then measure (G06) and bound (G07). **Dev B** should
be the most careful reviewer of correctness code: G03 is the one goal where a
bug double-books or loses a customer's appointment, and G05's card shows its
outcome, so one person owns the confirm path end to end. **Dev C** should be
whoever knows the existing site's login and the GCP project: identity (G04),
deployment (G08) and the launch check (G09). This split was chosen by trying
every owner assignment with the schedule helper's own analysis; it gives the
earliest high-end finish (see below). Dev B has the most slack and can pair on
G09 or start phase 2 G11 from about day 7.

```yaml
- goal: G01
  phase: 1
  hands_on: 2.5-4
  review: 1-2
  total: 3.5-6
  owner: Dev A
  blocked_by: []
  calendar_waits: none
  wait_days: 0
- goal: G02
  phase: 1
  hands_on: 2-3.5
  review: 1-1.5
  total: 3-5
  owner: Dev A
  blocked_by: [G01]
  calendar_waits: none
  wait_days: 0
- goal: G03
  phase: 1
  hands_on: 5-8
  review: 3-5
  total: 8-13
  owner: Dev B
  blocked_by: [G01]
  calendar_waits: none
  wait_days: 0
- goal: G04
  phase: 1
  hands_on: 3.5-6
  review: 2.5-4
  total: 6-10
  owner: Dev C
  blocked_by: []
  calendar_waits: none
  wait_days: 0
- goal: G05
  phase: 1
  hands_on: 4-6
  review: 1.5-2.5
  total: 5.5-8.5
  owner: Dev B
  blocked_by: [G04]
  calendar_waits: none
  wait_days: 0
- goal: G06
  phase: 1
  hands_on: 4.5-8
  review: 1.5-2.5
  total: 6-10.5
  owner: Dev A
  blocked_by: [G02]
  calendar_waits: none
  wait_days: 0
- goal: G07
  phase: 1
  hands_on: 2-3.5
  review: 1-1.5
  total: 3-5
  owner: Dev A
  blocked_by: [G04]
  calendar_waits: none
  wait_days: 0
- goal: G08
  phase: 1
  hands_on: 4-6.5
  review: 1.5-2.5
  total: 5.5-9
  owner: Dev C
  blocked_by: [G02, G07]
  calendar_waits: production booking API credential (request day 1)
  wait_days: 0
- goal: G09
  phase: 1
  hands_on: 3-5
  review: 1-2
  total: 4-7
  owner: Dev C
  blocked_by: [G03, G05, G06, G08]
  calendar_waits: salon manager go/no-go (0-1 day)
  wait_days: 0-1
- goal: G10
  phase: 2
  total: 4.5-9
  blocked_by: [G09]
- goal: G11
  phase: 2
  total: 3-6
  blocked_by: [G09]
- goal: G12
  phase: 2
  total: 4.5-9
  blocked_by: [G09]
- goal: G13
  phase: 2
  total: 3-6
  blocked_by: [G09]
- goal: G14
  phase: 2
  total: 4-6
  blocked_by: [G09]
```

Schedule check (run 2026-10-09 with
`python3.11 .claude/skills/adk-system-designer/scripts/check_schedule.py --plan docs/plans/salon-booking-assistant.md --tickets docs/tickets/salon-booking-assistant/ --capacity 81 --days 10 --person "Dev A=3.6" --person "Dev B=3.6" --person "Dev C=3.6"`):

```text
Phase 1: 9 goals, 44.5-74 human hours
Capacity after reserve: 81 h; fits: yes
  Dev A: 15.5-26.5 h of 36 h available
  Dev B: 13.5-21.5 h of 36 h available
  Dev C: 15.5-26 h of 36 h available
Longest dependent chain (low): G04 -> G07 -> G08 -> G09, 5.14 working days
Longest dependent chain (high): G04 -> G07 -> G08 -> G09, 9.61 working days
Finish with these people and dependencies: 5.83-10.58 working days
Calendar: 10 working days; fits: low end only
```

Exit status 1: phase 1 fits the 81 hours at its high end (74 h), but the
calendar fits **at the low end only**: with these three people and the
dependencies, the finish range is 5.83–10.58 working days against 10. The
longest dependent chain is G04 → G07 → G08 → G09 (9.61 days high). No other
owner assignment does better (every assignment was tried with the helper's
`analyse` function; best high-end finish 10.58 days). Two pre-agreed moves bring
the high end inside the calendar, re-checked with the same function: booking
the salon manager's walkthrough in advance (G09 wait 0–0.5 day) **and** cutting
`propose_move` (below) gives 43–71.5 h and a 5.42–9.81-day finish.

**Cut line.** Ships in phase 1: G01–G09, about 44.5–74 of the 81 reserve-adjusted
hours. Waits for phase 2: G10–G14 (19–36 h, coarse). Checkpoint at the end of
day 6: if G03 or G04 is not done, take these cuts in order, each leaving a
working product: (1) `propose_move` leaves G03 and moving becomes "cancel, then
book" with two confirmation cards (saves about 1.5–2.5 h of Dev B's time and
the move-specific reconciliation; returns in phase 2); (2) G09 launches one
salon first and the other four a week later; (3) G06 drops to 15 cases. The
floor (confirmation, identity, allowance, no content in logs) is not cut.
If one person works alone, the order that stays useful is G01 → G02 → G04 →
G03 → G07 → G05 → G08 → G09, with G06 shrinking to a smoke set.
**Please confirm or move this cut line.**

## Implementation map

| Decision / requirement | Component and integration point (proposed) | GCP responsibility | Primary skill | Verification still needed |
| --- | --- | --- | --- | --- |
| D1 one agent | `app/agent.py` factory → `App`/`Runner` in `gateway.py` | Vertex AI model endpoint | `adk-tool-interface-design` | Pin of google-adk and Vertex model availability in region |
| D2 identity | `gateway.py` verifies site JWT, writes `customer_id` to session state at session creation; tools read `tool_context.state` | — | `adk-tool-auth-and-secrets` | Site token claims (A2) |
| D3/D4 propose-confirm-execute | `tools/propose.py` writes proposal; `executor.py` claims, rechecks, writes, reconciles | Cloud SQL | `safe-api-tool-calls` | Booking API idempotency (G01) |
| D5 widget | `web/widget` → `/chat`, `/proposals/{id}`, `/proposals/{id}/confirm` | Cloud Run | `adk-frontend-integration` | Embedding in the existing site |
| D6 hosting/state | `DatabaseSessionService` on Cloud SQL; Cloud Run service account | Cloud Run, Cloud SQL, Secret Manager, Cloud Trace | `deploy-adk-on-google-cloud` | Region, prices |
| I5 budgets | `RunConfig(max_llm_calls=12)`; allowance table in gateway | Billing budget alert | `adk-operational-guardrails` | — |

## Goals and dependencies

| ID and goal | Phase | Type | Human hours | Depends on | Primary skill | State |
| --- | --- | --- | --- | --- | --- | --- |
| G01 Booking API client, fake and contract answers | 1 | discovery + implementation | 3.5–6 | — | `safe-api-tool-calls` | ready |
| G02 Read-only assistant answers availability and "my appointments" locally | 1 | implementation | 3–5 | G01 | `adk-tool-interface-design` | blocked by G01 |
| G03 Propose and confirm book, move, cancel exactly once | 1 | implementation | 8–13 | G01 | `safe-api-tool-calls` | blocked by G01 |
| G04 Signed-in customers only see their own data | 1 | implementation | 6–10 | — | `adk-tool-auth-and-secrets` | ready |
| G05 Chat widget with confirmation card | 1 | implementation | 5.5–8.5 | G04 | `adk-frontend-integration` | blocked by G04 |
| G06 30-case evaluation set and runner | 1 | implementation | 6–10.5 | G02 | `adk-agent-evaluation` | blocked by G02 |
| G07 Spend limits, allowance and PII-safe logging | 1 | implementation | 3–5 | G04 | `adk-operational-guardrails` | blocked by G04 |
| G08 Staging and production on Cloud Run with traces and rollback | 1 | implementation | 5.5–9 | G02, G07 | `deploy-adk-on-google-cloud` | blocked |
| G09 End-to-end launch check and beta release | 1 | verification + release | 4–7 | G03, G05, G06, G08 | `adk-agent-evaluation` | blocked |
| G10 Evaluation gate in CI | 2 | implementation | 4.5–9 | G09 | `adk-release-engineering` | proposed |
| G11 Provider-backed idempotent writes | 2 | implementation | 3–6 | G09 | `safe-api-tool-calls` | proposed |
| G12 SLOs and alerts | 2 | implementation | 4.5–9 | G09 | `adk-agent-observability` | proposed |
| G13 Adversarial suite | 2 | implementation | 3–6 | G09 | `adk-agent-security` | proposed |
| G14 Streaming replies | 2 | implementation | 4–6 | G09 | `adk-frontend-integration` | proposed |

### G01 — Booking API client, fake and contract answers

- **Phase and estimate:** 1; hands-on 2.5–4, review and verify 1–2, total 3.5–6; calendar waits none; owner Dev A
- **Outcome and linked decisions:** a typed client and an in-memory fake that every other goal codes against; written answers to A5 (idempotency key, lookup by client reference, reschedule atomicity, error codes, rate limits, time zone of timestamps). D3, D4.
- **Scope:** `app/booking_api.py` (`BookingApi` protocol, HTTP client, `FakeBookingApi`), a contract note in `docs/architecture/booking-api-contract.md`. Out: tools, executor.
- **Depth:** reads and writes against **staging only**; credential from environment locally, never committed; timeouts set (connect 3 s, read 10 s); no app-level retries on writes (G03 owns them).
- **Implementation route:** `httpx` client with explicit deadline per call; error mapping to `conflict | not_found | rejected | unavailable | uncertain`; fake honours the same contract including a "commit then time out" mode.
- **Prerequisites:** staging base URL and a staging service credential.
- **Primary skill:** `safe-api-tool-calls`
- **Supporting skills:** `adk-tool-auth-and-secrets` (keep the credential out of code and prompts)
- **Acceptance:** contract tests pass against the fake and, once, against staging for a test customer; a write timeout maps to `uncertain`, not `failed`; the contract note answers each A5 question or names who will.
- **Verification:** `pytest tests/test_booking_api.py` offline; `pytest -m staging` local integration, authorized against staging only.
- **Execution scope:** local code and staging calls; no production credential.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G01 from docs/plans/salon-booking-assistant.md. Read docs/architecture/salon-booking-assistant.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G02 — Read-only assistant answers availability and "my appointments" locally

- **Phase and estimate:** 1; hands-on 2–3.5, review and verify 1–1.5, total 3–5; calendar waits none; owner Dev A
- **Outcome and linked decisions:** in `adk web` or a local Runner, "what's free with Jo on Saturday morning at Riverside?" returns at most 10 correct slots in the salon's time zone; "what have I got booked?" lists only the test customer's appointments. D1, D2 (state contract), model-facing contracts.
- **Scope:** `app/agent.py`, `app/tools/read.py`, instruction `booking-v1`. Out: propose tools (G03), gateway (G04).
- **Depth:** pinned `gemini-3.8-flash`; `max_llm_calls=12`; `customer_id`, `today`, `salon_tz` read from state (set by a test fixture until G04).
- **Implementation route:** `LlmAgent` with three `FunctionTool`s returning `{status, ...}`; relative dates resolved by the model against `{today}` and validated in code (no past dates, ≤ 60 days ahead).
- **Prerequisites:** G01 fake.
- **Primary skill:** `adk-tool-interface-design`
- **Supporting skills:** `adk-agent-instructions` (instruction booking-v1 and state templating); `adk-model-and-output-contracts` (confirm model ID against the lifecycle table and Vertex availability in region; record the pin)
- **Acceptance:** scripted-model Runner tests show the right tool and arguments for 5 phrasings; the captured request contains no customer contact fields; a tool argument naming another customer is impossible (no such parameter); google-adk version confirmed and pinned in `pyproject.toml`.
- **Verification:** `pytest tests/test_agent_read.py` offline; one manual `adk web` session against the fake (≤ 20 model calls).
- **Execution scope:** local; Vertex AI calls on the dev project within the A4 allowance.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G02 from docs/plans/salon-booking-assistant.md. Read docs/architecture/salon-booking-assistant.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G03 — Propose and confirm book, move, cancel exactly once

- **Phase and estimate:** 1; hands-on 5–8, review and verify 3–5, total 8–13; calendar waits none; owner Dev B
- **Outcome and linked decisions:** the agent can propose a booking, move or cancel; only the confirm endpoint changes the booking system, once per proposal, and the customer sees the real outcome. D3, D4, I2–I4.
- **Scope:** `app/tools/propose.py`, `app/executor.py`, `app/store.py` (proposals table), confirm and status handlers (plain functions G05 mounts). Out: widget (G05), provider idempotency if missing (G11).
- **Depth:** build for real customers: atomic claim `pending → executing`, recheck slot and ownership before writing, idempotency key = proposal ID when G01 says it is supported, otherwise lookup-before-retry; `executing` older than 60 s treated as `uncertain`; proposal expiry 10 min. No background worker.
- **Implementation route:** propose tools validate with read calls then insert a proposal row with code-rendered summary and return `{status: "proposed", proposal_id, summary}`; executor maps booking-API outcomes to `succeeded | failed:<reason> | uncertain`; reconciliation via `list_my_appointments` match on slot/appointment.
- **Prerequisites:** G01; G02's agent factory to register tools (can merge after G02 lands).
- **Primary skill:** `safe-api-tool-calls`
- **Supporting skills:** `adk-tool-interface-design` (propose tool declarations and errors); `adk-agent-security` (assert the agent holds no write path)
- **Acceptance:** scripted model calling every tool performs zero booking-API writes; confirm twice → one write and the same result; fake "commit then time out" → `uncertain`, then `succeeded` after lookup, never a second create; slot taken before confirm → `failed: conflict`; another customer's proposal ID → 404; restart between claim and write → `uncertain` path.
- **Verification:** `pytest tests/test_executor.py tests/test_propose.py` offline; one staging book→move→cancel run for the test customer.
- **Execution scope:** local and staging only.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G03 from docs/plans/salon-booking-assistant.md. Read docs/architecture/salon-booking-assistant.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G04 — Signed-in customers only see their own data

- **Phase and estimate:** 1; hands-on 3.5–6, review and verify 2.5–4, total 6–10; calendar waits none; owner Dev C
- **Outcome and linked decisions:** the gateway accepts only a valid site token, binds each session to its customer, and puts `customer_id`, `salon_tz`, `today` into state. D2, I1.
- **Scope:** `app/gateway.py` (FastAPI app, `/chat` endpoint around the Runner, session create/resume with owner check). Out: allowance (G07), widget (G05).
- **Depth:** build: JWKS verification with issuer, audience and expiry; session owner column; caller-supplied session ID never grants access; no fallback login.
- **Implementation route:** FastAPI dependency verifies JWT → `customer_id`; `DatabaseSessionService` (SQLite locally, Postgres in G08) with session created by the gateway; state keys written by code only.
- **Prerequisites:** the existing site's token format (A2) — read in the first hour; if it cannot be verified server-side, stop and raise the magic-link alternative.
- **Primary skill:** `adk-tool-auth-and-secrets`
- **Supporting skills:** `adk-frontend-integration` (session ownership in the browser API contract)
- **Acceptance:** missing/expired/wrong-audience token → 401; customer B resuming customer A's session ID → 403 with no events returned; a message naming A's appointment ID while signed in as B reads nothing of A's; state keys cannot be set from the request body.
- **Verification:** `pytest tests/test_gateway_auth.py` offline with locally signed test tokens and a scripted model.
- **Execution scope:** local.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G04 from docs/plans/salon-booking-assistant.md. Read docs/architecture/salon-booking-assistant.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G05 — Chat widget with confirmation card

- **Phase and estimate:** 1; hands-on 4–6, review and verify 1.5–2.5, total 5.5–8.5; calendar waits none; owner Dev B
- **Outcome and linked decisions:** on the booking site, a signed-in customer chats, sees a card with the proposed change, presses Confirm and sees the status from the operation record. D5, I4.
- **Scope:** `web/widget`, JSON contract `/chat` → `{messages[], proposal?}`, `GET /proposals/{id}`, `POST /proposals/{id}/confirm`; embedding snippet for the existing site. Out: streaming (G14).
- **Depth:** card text comes from the proposal row, never from model text; Confirm disabled after expiry; failure states shown with the booking-form link.
- **Implementation route:** plain JS/TS widget; handlers from G03 mounted in `gateway.py`; until G03 merges, a stub proposal endpoint with the same schema.
- **Prerequisites:** G04; proposal schema from the design (D3).
- **Primary skill:** `adk-frontend-integration`
- **Supporting skills:** none
- **Acceptance:** mobile browser: chat → card → Confirm → `succeeded` shown; `uncertain` shows "We're checking this booking"; expired card cannot confirm; model failure shows the fallback link.
- **Verification:** local browser run against stubbed and, after G03, real handlers with the fake booking API.
- **Execution scope:** local.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G05 from docs/plans/salon-booking-assistant.md. Read docs/architecture/salon-booking-assistant.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G06 — 30-case evaluation set and runner

- **Phase and estimate:** 1; hands-on 4.5–8, review and verify 1.5–2.5, total 6–10.5; calendar waits none; owner Dev A
- **Outcome and linked decisions:** a labelled set the team runs before every release: 10 book, 6 move, 5 cancel, 5 ambiguous/clarify, 4 refuse/out-of-scope (including asking about another customer). Assertions on tool calls and proposal fields, no judge model. D1.
- **Scope:** `evals/cases.jsonl`, `evals/run.py` (Runner + fake booking API + real model), results table. Out: CI gate (G10).
- **Depth:** run by hand before release; ≤ 200 model calls per run.
- **Implementation route:** ADK evaluation or a small Runner loop with a scripted user; pass = right tool sequence and proposal fields; write cases need G03's propose tools (rerun in G09).
- **Prerequisites:** G02.
- **Primary skill:** `adk-agent-evaluation`
- **Supporting skills:** `adk-agent-instructions` (fix instruction failures found by the run)
- **Acceptance:** read and clarify cases run and report a pass rate per category; failed and errored cases are listed separately; the run records model ID, prompt version and date.
- **Verification:** `python evals/run.py` bounded live against Vertex AI.
- **Execution scope:** dev project, within A4.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G06 from docs/plans/salon-booking-assistant.md. Read docs/architecture/salon-booking-assistant.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G07 — Spend limits, allowance and PII-safe logging

- **Phase and estimate:** 1; hands-on 2–3.5, review and verify 1–1.5, total 3–5; calendar waits none; owner Dev A
- **Outcome and linked decisions:** a conversation cannot loop or run up cost, and logs hold no message content. I5, A10.
- **Scope:** `RunConfig(max_llm_calls=12)` in the gateway; allowance table and admission check (60 turns/customer/day); structured logger with an allow-list of fields; nightly session deletion query (30 days). Out: Model Armor/SDP (later).
- **Depth:** floor plus MVP per-user allowance; billing budget alert configured in G08.
- **Implementation route:** gateway dependency increments and checks the counter atomically (`INSERT ... ON CONFLICT ... RETURNING`); logging filter drops `text`/`content` fields.
- **Prerequisites:** G04.
- **Primary skill:** `adk-operational-guardrails`
- **Supporting skills:** `protect-adk-sensitive-data` (which fields may reach logs and traces)
- **Acceptance:** scripted model that calls tools forever stops at 12 calls with the fallback message; 61st turn of the day refused; log capture of a full conversation contains no message text, phone or email.
- **Verification:** `pytest tests/test_guardrails.py` offline.
- **Execution scope:** local.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G07 from docs/plans/salon-booking-assistant.md. Read docs/architecture/salon-booking-assistant.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G08 — Staging and production on Cloud Run with traces and rollback

- **Phase and estimate:** 1; hands-on 4–6.5, review and verify 1.5–2.5, total 5.5–9; calendar waits: production booking API credential (request day 1); owner Dev C
- **Outcome and linked decisions:** the service runs in staging and production with its own service account, Cloud SQL, secrets, traces without content, a release manifest and a one-command rollback. D6.
- **Scope:** Dockerfile, deploy script, Cloud SQL instance and schema, Secret Manager entry, billing budget alert, feature flag for the beta link. Out: SLOs (G12), CI gate (G10).
- **Depth:** MVP: previous revision kept; content capture off; release manifest = image digest, prompt version, model ID, tool schema hash, secret version.
- **Implementation route:** Cloud Run service with `--service-account`, Cloud SQL connector, ADK OTel export to Cloud Trace.
- **Prerequisites:** G02, G07 (G04 through G07); the widget from G05 is a static asset added to the image in G09; GCP project access; authorization to create these resources (not given in this session).
- **Primary skill:** `deploy-adk-on-google-cloud`
- **Supporting skills:** `adk-agent-observability` (trace export, content gates, token counts); `adk-release-engineering` (manifest and rollback)
- **Acceptance:** staging restart keeps a session and a proposal; a trace shows one span per agent, tool and model call with session ID and no message text; rolling back to the previous revision works; budget alert exists.
- **Verification:** hosted checks on staging, recorded with revision IDs.
- **Execution scope:** needs explicit authorization for the GCP project and region.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G08 from docs/plans/salon-booking-assistant.md. Read docs/architecture/salon-booking-assistant.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G09 — End-to-end launch check and beta release

- **Phase and estimate:** 1; hands-on 3–5, review and verify 1–2, total 4–7; calendar waits: salon manager go/no-go (0–1 day); owner Dev C
- **Outcome and linked decisions:** the full journey works on staging against the staging booking API; the 30-case run passes the agreed bar; the beta link goes live. All invariants.
- **Scope:** redeploy with G03's handlers and G05's widget; G06 rerun including write cases; staging walkthrough of book/move/cancel with a salon manager; p95 turn latency measured on 20 turns; go-live checklist and flag flip. Out: CI gate.
- **Depth:** release bar (assumed): ≥ 90 % overall, 100 % on refuse-other-customer and no-write-without-confirm cases.
- **Implementation route:** run `evals/run.py` against staging config; checklist in `docs/runbooks/launch.md`.
- **Prerequisites:** G03, G05, G06, G08.
- **Primary skill:** `adk-agent-evaluation`
- **Supporting skills:** `adk-release-engineering` (release manifest recorded with the run)
- **Acceptance:** eval bar met; Maya's journey completes on staging; an `uncertain` row can be found with the operator query; rollback rehearsed once.
- **Verification:** hosted staging evidence, then production flag flip with authorization.
- **Execution scope:** production release needs the team's go decision.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G09 from docs/plans/salon-booking-assistant.md. Read docs/architecture/salon-booking-assistant.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### Phase 2 (coarse; refine after phase 1 results)

- **G10 Evaluation gate in CI** — `adk-release-engineering` (supporting `adk-agent-evaluation`); 4.5–9 h. Acceptance: a prompt change that drops the refuse-other-customer category fails CI by exit code.
- **G11 Provider-backed idempotent writes** — `safe-api-tool-calls`; 3–6 h; only if G01 found no idempotency key. Acceptance: the booking API rejects a replay of the same proposal ID with the original result.
- **G12 SLOs and alerts** — `adk-agent-observability`; 4.5–9 h. Acceptance: alert on `uncertain` operations > 0 for 15 min and on succeeded-operation ratio below baseline, routed to an on-call owner.
- **G13 Adversarial suite** — `adk-agent-security`; 3–6 h. Acceptance: 15 injection and cross-customer prompts; no forbidden tool call or disclosure.
- **G14 Streaming replies** — `adk-frontend-integration`; 4–6 h; trigger p95 > 6 s measured in G09. Acceptance: first text within 1.5 s; card still rendered from the stored proposal.

## Later

| Item | Trigger that brings it forward | Risk accepted while it waits | Likely primary skill |
| --- | --- | --- | --- |
| SMS / WhatsApp channel | Customers ask for it; widget usage plateaus | Web-only reach | `adk-frontend-integration` |
| Staff-facing mode (front desk books for walk-ins) | Front desk requests it | Staff use the existing tool | `adk-tool-auth-and-secrets` |
| Deposits / payments | Salons require deposits | No money moves now | `safe-api-tool-calls` |
| Long-term preferences ("my usual") | Repeat customers ask | Customers restate preferences | `adk-memory-architecture` |
| Model Armor / SDP screening | Free-text notes or third-party content enter tools | Field minimisation only | `protect-adk-sensitive-data` |
| Background reconciliation worker | `uncertain` operations > a few a week | Daily operator query | `safe-api-tool-calls` |
| Model migration | Next retirement notice for `gemini-3.8-flash` | Pinned model | `adk-release-engineering` |
| Cost and latency tuning | Cost per completed booking or p95 above target | Unoptimised calls | `optimise-adk-on-google-cloud` |

## What the reviewer reads

| Document | Establishes |
| --- | --- |
| [Design](../architecture/salon-booking-assistant.md) | Method, assumed answers and decisions |
| `evals/results/latest.md` (created in G06) | Latest result per case |
| This plan | Remaining limits and deferred controls |

## Open decisions for further planning

| Decision / question | Known facts and alternatives | Evidence or user decision needed | Blocks which goals? |
| --- | --- | --- | --- |
| Site token verifiable server-side (A2) | Alternative: magic-link login, ~+1 day | Dev C reads site auth | G04 |
| Booking API idempotency (A5) | Alternative: lookup-before-retry (designed) | G01 contract note | G03 retry path, G11 |
| Customers vs staff, launch audience (A1, A9) | Design assumes customers, all five salons, beta link | Product owner | G09 scope |
| Retention periods (A10) | 30 days sessions, 90 days proposals assumed | Product owner / data protection | G07 values |
| Cut line | G01–G09 in phase 1 | The three developers | — |

## Resume here

- **Next goals:** G01 (Dev A) and G04 (Dev C) are ready now and independent; Dev B starts G03 once G01's fake exists (about day 2) and can draft the proposal table and card mock-up before that.
- **Read first:** the design, this plan, the ticket.
- **Next action:** Dev A confirms staging access and answers the A5 questions; Dev C reads the existing site's token format and books the salon manager's staging walkthrough for day 9; Dev C also requests the production booking API credential.
- **Continuation prompt:**

```text
/adk-engineer Carry out G01 from docs/plans/salon-booking-assistant.md.
```

After that goal, the same request without a goal ID continues with the next
ready one: `/adk-engineer Continue the next ready goal in docs/plans/salon-booking-assistant.md.`
