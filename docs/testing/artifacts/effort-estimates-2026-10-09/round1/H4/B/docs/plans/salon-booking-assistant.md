# Implementation plan: salon booking assistant

Status: draft — ready goals identified (G01, G02 ready now; the rest wait on them)
Architecture: [../architecture/salon-booking-assistant.md](../architecture/salon-booking-assistant.md)
Continuation source of truth: this plan; per-goal tickets in [../tickets/salon-booking-assistant/](../tickets/salon-booking-assistant/)

## Destination and constraints

Signed-in customers of five salons book, move and cancel appointments through a
website chat that calls the existing booking API, with customer confirmation
before every change. Non-goals for phase 1: payments, guests, other channels,
languages, memory across sessions. Accepted stack (assumed): Python, google-adk
**2.8.0** (working assumption, confirm in G02), Vertex AI `gemini-3.8-flash`
(fallback `gemini-3.5-flash`), Cloud Run, existing Cloud SQL Postgres. The
repository is greenfield: every module path below is **proposed**. No cloud
action is authorised by this plan; G03 and G10 need an explicit go-ahead for
staging and production targets.

Proposed layout: `app/agent.py` (agent factory), `app/instruction.md`,
`app/tools/{read,propose}.py`, `app/booking_client.py` (+ `fake_booking_api.py`),
`app/operations.py` (operation record + executor), `app/server.py` (FastAPI
gateway), `web/widget/`, `evals/`, `release/manifest.yaml`, `tests/`.

## Delivery profile and capacity

Profile: **MVP** (see design, delivery constraints).

| Phase | Delivers | Goals | Human hours, agent-assisted | Capacity and reserve |
| --- | --- | --- | --- | --- |
| 1, ship (2 weeks) | Signed-in customers book/move/cancel safely; team sees failures and cost | G01–G10 | 54–86 (58–94 if G04 is needed) | 3 × 10 d × 7 h × 0.6 ≈ 126 h; 25 % reserve → ≈ 95 h |
| 2, harden (weeks 3–6) | Advertised launch, guests, CI gate, alerts | G11–G17 | 38–68 | When the team has time |

Estimates already include ×1.5 for a team new to ADK; they are assumptions.

| Person | Goals | Hours | Capacity after reserve |
| --- | --- | --- | --- |
| Dev A (booking API) | G01, G03, G05 | 17–28 | ≈ 32 |
| Dev B (agent/Python) | G02, G08, G09 (+ G04 if needed) | 15–24 (19–32) | ≈ 32 |
| Dev C (full stack) | G06, G07, G10 | 22–34 | ≈ 32 — over at the high end |

Longest dependent chain: G02 → G05 → final G09 run → final G10 release ≈
19–28 h, about 5–7 working days for one person. G09 case writing and G10's
staging pipeline start early, in parallel, so they are not on the chain.
**Cut line:** if Dev C or the chain runs high by day 8, G10 ends at staging plus
staff/friends accounts; the public flip moves to day 1 of phase 2. If only one
person remains, the useful order is G01 → G02 → G05 → G06 → G07 (a working
confirm-safe assistant), then G08, G09, G10.

## Implementation map

| Decision | Component and integration point (proposed) | GCP | Primary skill | Still to verify |
| --- | --- | --- | --- | --- |
| D1 | `LlmAgent` in `app/agent.py`, run by `Runner` in `app/server.py` with `RunConfig(max_llm_calls=12)` | Vertex AI | adk-tool-interface-design | ADK 2.8.0 constructor names |
| D2, D4, D5 | `propose_*` tools write `operations` rows; `POST /operations/{id}/confirm` executor | Cloud SQL | safe-api-tool-calls | API idempotency + reschedule (G01) |
| D3, D8 | Token verification middleware → `user_id`; `DatabaseSessionService` | Cloud SQL, Secret Manager | adk-tool-auth-and-secrets | Site token format (G01) |
| D6 | JSON chat API + widget card | — | adk-frontend-integration | Website embed method |
| D7 | Model ID in `release/manifest.yaml`, read at startup | Vertex AI | adk-model-and-output-contracts | Region availability (G02) |
| D9 | Cloud Run service + service account | Cloud Run | deploy-adk-on-google-cloud | Project/region, authorisation |

## Goals and dependencies

| ID and goal | Phase | Type | Hours | Depends on | Primary skill | Owner | State |
| --- | --- | --- | --- | --- | --- | --- | --- |
| G01 Booking API contract and sign-in facts | 1 | discovery | 3–5 | — | safe-api-tool-calls | Dev A | ready |
| G02 Assistant answers availability and lists my appointments (offline) | 1 | impl | 4–7 | — | adk-tool-interface-design | Dev B | ready |
| G03 Real booking API client against staging | 1 | impl | 4–7 | G01 | safe-api-tool-calls | Dev A | blocked by G01 |
| G04 Idempotency keys in the booking API (only if G01 finds none) | 1 | impl, conditional | 4–8 or 0 | G01 | safe-api-tool-calls | Dev B | blocked by G01 |
| G05 Book, move and cancel exactly once after confirmation | 1 | impl | 10–16 | G02; G01 for move path; G03/G04 for live check | safe-api-tool-calls | Dev A | blocked by G02 |
| G06 Signed-in chat API with customer-owned sessions | 1 | impl | 8–12 | G01 (token facts); G02 | adk-tool-auth-and-secrets | Dev C | blocked by G01 |
| G07 Chat widget with confirmation card | 1 | impl | 6–10 | G06 API contract | adk-frontend-integration | Dev C | blocked by G06 contract |
| G08 Spend and abuse limits, content-free telemetry | 1 | impl | 3–5 | G06 | adk-operational-guardrails | Dev B | blocked by G06 |
| G09 Thirty-conversation evaluation set | 1 | impl | 8–12 | G02 (read cases), G05 (write cases) | adk-agent-evaluation | Dev B | blocked by G02 |
| G10 Deploy to staging, soft launch | 1 | impl | 8–12 | G03, G05–G09 | deploy-adk-on-google-cloud | Dev C | blocked |

### G01 — Booking API contract and sign-in facts (discovery)

- **Phase and estimate:** 1; hands-on 2–3, review and verify 1–2, total 3–5; calendar waits none; owner Dev A
- **Outcome and linked decisions:** answers A5, A7 and the baseline; settles D3, D4, D5.
- **Scope:** read the booking API's code/OpenAPI and the website's auth; write `docs/architecture/booking-api-contract.md` with endpoints, auth, error codes, idempotency-key support, atomic reschedule (yes/no), business rules enforced server-side, notifications sent, staging URL (no secrets), the site token format and verification method, and last month's self-service vs front-desk change counts. Stop when every question is answered or named as missing.
- **Depth:** discovery only; no code changes.
- **Implementation route:** existing booking API repo and website repo (not in this repository).
- **Prerequisites:** access to both repos.
- **Primary skill:** safe-api-tool-calls. **Supporting skills:** adk-tool-auth-and-secrets (token verification facts).
- **Acceptance:** the contract file answers the 9 questions above; the fake API in G02/G05 is updated to match; decision recorded: G04 needed yes/no, D5 path atomic/create-then-cancel.
- **Verification:** review by Dev B and Dev C (30 min).
- **Execution scope:** read-only; no calls to production.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G01 from docs/plans/salon-booking-assistant.md. Read docs/architecture/salon-booking-assistant.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G02 — Assistant answers availability and lists my appointments (offline)

- **Phase and estimate:** 1; hands-on 1.5–3, review 2.5–4, total 4–7; waits none; owner Dev B
- **Outcome and linked decisions:** in `adk web`/a test, "What's free Saturday morning with Sam at Elm St?" returns slots from the fake API; "What do I have booked?" lists only the test customer's appointments. D1, D7.
- **Scope:** agent factory, instruction v1 with date/time-zone injected from state, 4 read tools, in-memory fake booking API with fixtures for 5 salons, scripted-model tests. Out: propose tools (G05), HTTP server (G06).
- **Depth:** build; pinned model; `customer_id` from state only.
- **Implementation route:** `LlmAgent` + `Runner`; tools read `tool_context.state["customer_id"]`; results bounded (10 slots, 20 appointments), notes stripped.
- **Prerequisites:** Python env with google-adk pinned (2.8.0 unless the team chooses otherwise).
- **Primary skill:** adk-tool-interface-design. **Supporting skills:** adk-agent-instructions (instruction and date handling), adk-model-and-output-contracts (model pin and Vertex region check).
- **Acceptance:** scripted model calls `search_availability` and gets ≤ 10 slots; `list_my_appointments` returns only customer A's fixtures; no tool declares a `customer_id` parameter; the installed ADK version and `gemini-3.8-flash` region availability (or fallback choice) are recorded.
- **Verification:** `pytest tests/test_read_tools.py tests/test_agent_offline.py` (offline); one bounded live `adk web` session (≤ 10 model calls) if Vertex access exists.
- **Execution scope:** local; the live session needs a Vertex project the team names.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G02 from docs/plans/salon-booking-assistant.md. Read docs/architecture/salon-booking-assistant.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G03 — Real booking API client against staging

- **Phase and estimate:** 1; hands-on 1.5–3, review 2.5–4, total 4–7; waits none; owner Dev A
- **Outcome:** the read tools work against the staging booking API with the same interface as the fake. D4 (transport half).
- **Scope:** `BookingClient` protocol with fake and HTTP implementations; per-call deadline (5 s reads, 10 s writes); retries only on reads and idempotent-keyed writes; error mapping to actionable tool results (`slot_unavailable`, `outside_cancellation_window`, `not_found`, `unavailable`). Out: executor (G05).
- **Depth:** build; credential from Secret Manager/env, never in code.
- **Primary skill:** safe-api-tool-calls. **Supporting skills:** adk-tool-auth-and-secrets (service credential).
- **Acceptance:** contract tests pass against staging for availability, list, and a create/cancel round trip on a test customer; timeout on a write surfaces `uncertain`, never a silent retry without the key; fake and real clients pass the same contract suite.
- **Verification:** `pytest tests/contract -m staging` (authorised live, staging only, test customer).
- **Execution scope:** staging only, after the team names the target.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G03 from docs/plans/salon-booking-assistant.md. Read docs/architecture/salon-booking-assistant.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G04 — Idempotency keys in the booking API (conditional)

- **Phase and estimate:** 1; hands-on 1.5–3, review 2.5–5, total 4–8 (0 if G01 finds support); waits none; owner Dev B with Dev A reviewing
- **Outcome:** create/reschedule/cancel accept `Idempotency-Key`; a replay with the same key and payload returns the original result; a different payload with the same key is rejected. D4.
- **Scope:** booking API repo: key table with 7-day retention, unique constraint, payload hash. Lookup by key for reconciliation.
- **Primary skill:** safe-api-tool-calls. **Supporting skills:** none.
- **Acceptance:** same key twice → one appointment, same response; changed payload → 409; lookup by key returns the result.
- **Verification:** booking API's own test suite + staging replay test.
- **Execution scope:** booking API repo; its migration needs the team's normal release.
- **Run this goal:** `/adk-engineer Carry out G04 from docs/plans/salon-booking-assistant.md. Read docs/architecture/salon-booking-assistant.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G05 — Book, move and cancel exactly once after confirmation

- **Phase and estimate:** 1; hands-on 4–6, review 6–10, total 10–16; waits none; owner Dev A
- **Outcome:** Maya's journey works end to end in tests: proposal → card data → confirm → one booking-API effect → status from the receipt. D2, D4, D5; invariants I2–I4.
- **Scope:** `propose_booking/move/cancel` (validate ownership and inputs, store canonical payload, 15-min expiry, return summary); `operations` table and migration; executor with atomic `proposed→dispatching` claim, recheck, idempotency key = op ID, status `succeeded/failed/uncertain/partial/expired`; D5 move path per G01; `scripts/reconcile_operations.py` and a one-page runbook. Out: HTTP endpoint wiring (G06 calls the executor), automated reconciliation job (G13).
- **Depth:** build at MVP depth; reconciliation manual.
- **Primary skill:** safe-api-tool-calls. **Supporting skills:** adk-tool-interface-design (propose tool declarations), adk-operational-guardrails (confirmation binding and expiry), adk-agent-security (model cannot reach the write).
- **Acceptance:** confirm executes once under concurrent double-confirm; lost response → `uncertain`, reconcile finds the appointment; slot taken → `failed` with retry path; another customer's appointment ID → `not_found`, no write; model text claiming success without confirm causes no write; move with failing cancel → `partial` with both IDs.
- **Verification:** `pytest tests/test_operations.py tests/test_propose_tools.py` against fake API and local Postgres (offline/local integration); one staging round trip after G03.
- **Execution scope:** local; staging after G03.
- **Run this goal:** `/adk-engineer Carry out G05 from docs/plans/salon-booking-assistant.md. Read docs/architecture/salon-booking-assistant.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G06 — Signed-in chat API with customer-owned sessions

- **Phase and estimate:** 1; hands-on 3–4, review 5–8, total 8–12; waits none; owner Dev C
- **Outcome:** `POST /chat`, `POST /operations/{id}/confirm|decline`, `GET /operations/{id}` serve only the verified customer. D3, D6, D8; I1.
- **Scope:** FastAPI app, token verification middleware, session create/resume with owner check, `DatabaseSessionService` on Postgres, JSON response schema `{reply, pending_operation?, operation_status?}`, 30-day session deletion script. Out: widget (G07), limits (G08).
- **Primary skill:** adk-tool-auth-and-secrets. **Supporting skills:** adk-memory-architecture (session service and retention), adk-frontend-integration (response schema).
- **Acceptance:** customer B cannot read, continue or confirm A's session/operation (403/404, no model call); missing/expired token → 401; restart the process and the conversation continues; response schema validated in tests.
- **Verification:** `pytest tests/test_server.py` with a local Postgres and a test token issuer (local integration).
- **Run this goal:** `/adk-engineer Carry out G06 from docs/plans/salon-booking-assistant.md. Read docs/architecture/salon-booking-assistant.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G07 — Chat widget with confirmation card

- **Phase and estimate:** 1; hands-on 2–4, review 4–6, total 6–10; waits none; owner Dev C
- **Outcome:** on the website, a signed-in customer chats and confirms on a card built from `pending_operation`, then sees the status from `operation_status`. D6; I2, I4.
- **Scope:** embeddable widget, card with old/new details, Confirm/Decline, status states incl. "checking", fallback salon phone, kill-switch flag. Out: streaming.
- **Primary skill:** adk-frontend-integration. **Supporting skills:** none.
- **Acceptance:** card text comes from the operation record (a test where reply text differs from the record shows the record); double tap sends one confirm; `uncertain` never renders "booked"; widget hidden when the flag is off or the user is signed out.
- **Verification:** component tests + a manual browser run against local G06.
- **Run this goal:** `/adk-engineer Carry out G07 from docs/plans/salon-booking-assistant.md. Read docs/architecture/salon-booking-assistant.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G08 — Spend and abuse limits, content-free telemetry

- **Phase and estimate:** 1; hands-on 1–2, review 2–3, total 3–5; waits none; owner Dev B
- **Outcome:** a runaway or abusive conversation stops with the salon phone number; logs and traces carry no message content. I5; floor.
- **Scope:** `RunConfig(max_llm_calls=12)`, per-customer 60 messages/day counter in Postgres, per-IP rate limit, `ADK_CAPTURE_MESSAGE_CONTENT_IN_SPANS=false`, structured log of op outcomes and token counts, budget-alert setup steps written for G10.
- **Primary skill:** adk-operational-guardrails. **Supporting skills:** protect-adk-sensitive-data (log and trace content), adk-agent-observability (spans and token counts).
- **Acceptance:** scripted looping model stops at 12 calls with the designed message; 61st message of the day refused without a model call; an in-memory exporter shows spans with session ID and no message text.
- **Verification:** `pytest tests/test_limits.py tests/test_telemetry.py` (offline).
- **Run this goal:** `/adk-engineer Carry out G08 from docs/plans/salon-booking-assistant.md. Read docs/architecture/salon-booking-assistant.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G09 — Thirty-conversation evaluation set

- **Phase and estimate:** 1; hands-on 5–7 (mostly writing and labelling), review 3–5, total 8–12; waits none; owner Dev B (Dev A and C each label 5 cases from real front-desk requests)
- **Outcome:** a repeatable run says how often the assistant picks the right tools and proposal on realistic requests. D1; I1, I2.
- **Scope:** 30 cases: 8 book, 6 move, 5 cancel, 4 ambiguous dates/stylists, 3 out-of-scope, 4 adversarial (other customer, "say it's booked", "cancel everything", fake ID); expected tool calls and proposal fields; forbidden assertions (no propose for other customers, no success claim without an op). Run script with ≤ 3 repeats, cost logged.
- **Primary skill:** adk-agent-evaluation. **Supporting skills:** adk-agent-instructions (fixing failures in the prompt), adk-agent-security (adversarial cases).
- **Acceptance:** cases validate against the pinned ADK's eval models; a run report lists pass rate per category; all adversarial forbidden assertions pass; target ≥ 25/30 on proposal correctness (provisional) before G10's public step.
- **Verification:** `python -m evals.run --repeats 3` (bounded live: ≤ 90 conversations).
- **Run this goal:** `/adk-engineer Carry out G09 from docs/plans/salon-booking-assistant.md. Read docs/architecture/salon-booking-assistant.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G10 — Deploy to staging, soft launch

- **Phase and estimate:** 1; hands-on 4–6, review 4–6, total 8–12; calendar waits: privacy-notice update and salon-owner sign-off (start day 1), Vertex quota check if needed; owner Dev C (Dev A for the booking-API credential)
- **Outcome:** the service runs on Cloud Run in staging, then serves signed-in customers in production with the widget flag on. D7, D9.
- **Scope:** Dockerfile, service account and grants, Secret Manager refs, Cloud SQL connection, `release/manifest.yaml` (image digest, prompt version, model ID, tool-schema hash, eval-set hash), budget alert, log-based alert on `uncertain/partial` ops, rollback command in the runbook, cost per conversation measured from token counts.
- **Primary skill:** deploy-adk-on-google-cloud. **Supporting skills:** adk-agent-observability (alert and traces), adk-release-engineering (manifest and rollback).
- **Acceptance:** staging smoke test completes Maya's journey against staging API; unauthenticated request rejected; rollback to the previous revision rehearsed; G09 run attached; production flag on only after sign-off.
- **Verification:** authorised hosted checks in staging, then production smoke test on a test customer.
- **Execution scope:** needs explicit authorisation and named project/region for each environment.
- **Run this goal:** `/adk-engineer Carry out G10 from docs/plans/salon-booking-assistant.md. Read docs/architecture/salon-booking-assistant.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

## Phase 2 — harden and graduate (weeks 3–6)

| ID | Goal | Hours | Primary skill | Acceptance |
| --- | --- | --- | --- | --- |
| G11 | Guest booking and change via SMS one-time code | 10–16 + SMS provider setup | adk-tool-auth-and-secrets | Unverified phone cannot see or change appointments; code expiry and attempt limit tested |
| G12 | Evaluation gate in CI with release manifest check | 4–8 | adk-release-engineering | PR that drops proposal correctness below threshold fails by exit code |
| G13 | Automated reconciliation of `uncertain/dispatching` operations | 4–8 | safe-api-tool-calls | Op stuck > 2 min reconciled by key lookup; no re-dispatch with a new key |
| G14 | SLIs and alerts: completed-operation ratio, tool error rate, tokens per booking | 4–8 | adk-agent-observability | Alert fires in staging on injected API errors and links to the session |
| G15 | Production samples → redacted eval cases (monthly) | 4–6 | adk-agent-observability | 10 new cases added from real sessions, no personal data |
| G16 | Adversarial suite expansion and security review | 6–10 | adk-agent-security | Findings mapped to OWASP IDs; forbidden-action tests in CI |
| G17 | Advertise launch: privacy notice live, salon staff briefing, measure the outcome hypothesis | 6–12 | adk-agent-observability | Weekly report: completed bookings via chat, front-desk corrections |

## Later

| Item | Trigger | Risk accepted while it waits | Likely primary skill |
| --- | --- | --- | --- |
| Streaming replies | Measured p50 reply > 4 s | Slower perceived replies | adk-frontend-integration |
| WhatsApp/SMS channel | Customers ask for it / web usage low | Website-only reach | adk-agent-interoperability |
| Model Armor / SDP screening | Free-text notes or a new channel enter the context | Customer can paste personal data into the chat (their own) | protect-adk-sensitive-data |
| Reminders and waitlist | Phase 2 outcome measured | — | adk-workflow-design |
| Model migration off `gemini-3.8-flash` | Retirement date announced (check lifecycle table monthly) | — | adk-release-engineering |
| Canary releases | > 1 release/week or > 500 conversations/day | Full-traffic releases with fast rollback | adk-release-engineering |
| Cost and latency tuning | Cost > USD 1 per completed booking | — | optimise-adk-on-google-cloud |
| Second language | Salon demand | English only | adk-agent-instructions |

## What the reviewer reads

| Document | Establishes |
| --- | --- |
| [Design](../architecture/salon-booking-assistant.md) | Method, assumed answers and decisions |
| `evals/REPORT.md` (G09) | Latest pass rate per category, linked to raw runs |
| This plan | Remaining limits and deferred controls |

## Open decisions for further planning

| Decision / question | Known facts and alternatives | Evidence needed | Blocks |
| --- | --- | --- | --- |
| Idempotency keys and atomic reschedule in the booking API | We own the API; add keys if missing (G04) | G01 | G04, G05 move path |
| Site token verifiable by our backend? | Else OTP in phase 1 (+10–16 h, cut line moves) | G01 | G06 |
| `gemini-3.8-flash` on Vertex in region | Fallback `gemini-3.5-flash` | G02 | G10 |
| Privacy notice and owner sign-off | Calendar wait | Founders | G10 public step |

## Resume here

- **Next goal:** G01 (Dev A) and G02 (Dev B) in parallel; both have no prerequisites. Dev C starts G06 against a stub agent once G01's token answer is in (day 1–2).
- **Read first:** the design, this plan, the ticket.
- **Next action:** Dev A opens the booking API repo and answers the G01 questions.
- **Continuation prompt:**

```text
/adk-engineer Carry out G01 Booking API contract and sign-in facts from docs/plans/salon-booking-assistant.md.
Read docs/architecture/salon-booking-assistant.md and preserve its accepted decisions.
Use safe-api-tool-calls with adk-tool-auth-and-secrets.
Work read-only on the booking API and website repositories, verify the nine contract questions are answered,
and update the plan with actual evidence and remaining blockers.
```

After that goal: `/adk-engineer Continue the next ready goal in docs/plans/salon-booking-assistant.md.`
