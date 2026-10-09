# Implementation plan: salon booking assistant

Status: draft — ready goals identified; scope-gate answers assumed
Architecture: [../architecture/salon-booking-assistant.md](../architecture/salon-booking-assistant.md)
Continuation source of truth: this plan; tickets in
[../tickets/salon-booking-assistant/](../tickets/salon-booking-assistant/) copy its phase 1 goals.

## Destination and constraints

Destination: signed-in customers of the five salons book, move and cancel
their own appointments through a website chat widget, via the existing
booking API, with every change confirmed by the customer and executed once.
Non-goals and accepted stack: see the design (D1–D8). Authorization in this
session: design only. No repository code exists yet (greenfield; only the
skills directory was present when inspected on 2026-10-09). Every module path
below is **proposed**.

Pins the goals inherit (provisional, D6): `google-adk==2.8.0` (version the
sibling skills were checked against), model `gemini-3.8-flash` on Vertex AI
(lifecycle snapshot checked 2026-10-08: stable, no shutdown announced),
prompt in `booking_assistant/prompts/instruction.md` versioned by git SHA. No
judge model in phase 1 (evaluation uses deterministic trajectory and
tool-argument checks). Changing any of these is a release, not a side effect.

Proposed layout:

```
booking_assistant/
  agent.py            # App + LlmAgent factory (G02)
  prompts/instruction.md
  tools/read.py       # list_services, find_availability, list_my_appointments (G02)
  tools/propose.py    # propose_booking/move/cancel (G04, G05)
  booking_client.py   # BookingClient protocol + HTTP client (G01, G02)
  fake_booking.py     # in-memory fake used by tests and evals (G02)
  operations.py       # proposals + booking_operations, confirm executor (G04)
  gateway.py          # FastAPI: auth, sessions, turns, confirm (G03)
widget/               # embeddable chat widget (G06)
evals/                # cases + runner (G07)
deploy/               # Cloud Run, Cloud SQL, secrets notes (G08)
```

Gateway JSON contract (owned by G03, consumed by G06; proposed):
`POST /v1/sessions` → `{session_id}`;
`POST /v1/sessions/{id}/turns {text}` → `{messages:[{id, role, text}], proposals:[{id, kind, summary, expires_at}]}`
(409 while a turn is running);
`POST /v1/proposals/{id}/confirm` → `{status: succeeded|failed|uncertain, reference?, message}`;
`GET /v1/operations/{proposal_id}` → same shape. All routes require the
customer token.

## Delivery profile and capacity

Profile: **MVP or pilot** (design, "Delivery constraints").

| Phase | Delivers | Goals | Human hours, agent-assisted (range) | Capacity and reserve |
| --- | --- | --- | --- | --- |
| 1, ship | Real signed-in customers book, move and cancel at all five salons, safely, with failures and cost visible | G01–G11 | 57–88 | 3 people × 5 focused h/day × 10 days = 150 h; 25% reserve → 112.5 h |
| 2, harden | CI evaluation gate, retention/erasure, adversarial suite, SLOs, cost dashboards, guest booking, production-to-eval loop | G12–G18 | 47–80 | When the team has time after launch |

Estimates are person-hours of human effort with a coding agent (hands-on plus
review and verify), for a team new to ADK: every figure already includes the
×1.5 multiplier from the skill's starting points. Calendar waits are on goals.

| Person | Goals | Hours | Their capacity (after reserve) |
| --- | --- | --- | --- |
| Dev A (agent and writes) | G02, G04, G05 | 17–27 | 37.5 |
| Dev B (contract, widget, evaluation, operations list) | G01, G06, G07, G10 | 21–31 | 37.5 |
| Dev C (identity, cloud, launch) | G03, G08, G09, G11 | 19–30 | 37.5 |

Schedule block (single source of each estimate; tickets copy it):

```yaml
- goal: G01
  phase: 1
  hands_on: 3-4
  review: 1-2
  total: 4-6
  owner: Dev B
  blocked_by: []
  calendar_waits: staging booking API credentials from its owner
  wait_days: 0-1
- goal: G02
  phase: 1
  hands_on: 3-5
  review: 2-3
  total: 5-8
  owner: Dev A
  blocked_by: []
  calendar_waits: none
  wait_days: 0
- goal: G03
  phase: 1
  hands_on: 4-6
  review: 2-3
  total: 6-9
  owner: Dev C
  blocked_by: [G01]
  calendar_waits: none
  wait_days: 0
- goal: G04
  phase: 1
  hands_on: 4-6
  review: 3-5
  total: 7-11
  owner: Dev A
  blocked_by: [G01, G02]
  calendar_waits: none
  wait_days: 0
- goal: G05
  phase: 1
  hands_on: 3-5
  review: 2-3
  total: 5-8
  owner: Dev A
  blocked_by: [G04]
  calendar_waits: none
  wait_days: 0
- goal: G06
  phase: 1
  hands_on: 5-7
  review: 2-3
  total: 7-10
  owner: Dev B
  blocked_by: []
  calendar_waits: none
  wait_days: 0
- goal: G07
  phase: 1
  hands_on: 5-8
  review: 1-2
  total: 6-10
  owner: Dev B
  blocked_by: [G02]
  calendar_waits: none
  wait_days: 0
- goal: G08
  phase: 1
  hands_on: 3-4
  review: 1-2
  total: 4-6
  owner: Dev C
  blocked_by: []
  calendar_waits: GCP project, billing and Vertex AI access
  wait_days: 0-1
- goal: G09
  phase: 1
  hands_on: 3-5
  review: 2-3
  total: 5-8
  owner: Dev C
  blocked_by: [G03, G08]
  calendar_waits: none
  wait_days: 0
- goal: G10
  phase: 1
  hands_on: 3-4
  review: 1
  total: 4-5
  owner: Dev B
  blocked_by: [G04]
  calendar_waits: salon managers briefed (request the slot on day 1)
  wait_days: 0-1
- goal: G11
  phase: 1
  hands_on: 3-5
  review: 1-2
  total: 4-7
  owner: Dev C
  blocked_by: [G05, G06, G07, G09, G10]
  calendar_waits: none
  wait_days: 0
```

Schedule check, run 2026-10-09 with
`python3.11 .claude/skills/adk-system-designer/scripts/check_schedule.py --plan docs/plans/salon-booking-assistant.md --tickets docs/tickets/salon-booking-assistant/ --days 10 --reserve 0.25 --person "Dev A=5" --person "Dev B=5" --person "Dev C=5"`
(exit status 1):

```text
Phase 1: 11 goals, 57-88 human hours
Capacity after reserve: 112.5 h; fits: yes
  Dev A: 17-27 h of 37.5 h available
  Dev B: 21-31 h of 37.5 h available
  Dev C: 19-30 h of 37.5 h available
Longest dependent chain (low): G02 -> G04 -> G05 -> G11, 5.6 working days
Longest dependent chain (high): G01 -> G04 -> G10 -> G11, 9.73 working days
Finish with these people and dependencies, 25% of each day held in reserve: 6.67-11.13 working days
Calendar: 10 working days; fits: low end only
```

**What this means.** Phase 1 fits the hours (57–88 of 112.5 after reserve;
each person has slack), but the calendar fits **only at the low end**: if
estimates run high, the launch lands on working day 11–12, not 10. The
calendar is set by the chain through the staging-credential wait
(G01 → G04 → G10 → G11, 9.7 working days at the high end) and by Dev C
working G03 → G09 → G11 in order, not by total hours.

What was changed after failing runs, and why (all true of the work):

1. First run (G01–G09, G08 = provisioning and hosted gateway together): high
   end 13.5 days. Split cloud provisioning (new G08, needs no gateway, starts
   day 1) from hosting the gateway (G09), and moved the managers' change list,
   runbook and briefing out of the launch goal into G10 for the person with
   spare hours. Result: 11.9 days.
2. Reassigned G03 (identity) to Dev C and G06 (widget) to Dev B, so the
   person who hosts the gateway also builds it and the widget goes to the
   person with slack: 11.1 days (the run above).

What-ifs run with the helper (same command, temporary copies of this plan):

| Remedy | Finish, working days | Closes the gap? |
| --- | --- | --- |
| G05 cut to cancel-only, "move" waits for phase 2 (3–5 h) | 6.7–11.1 | No |
| Reduce G10 to runbook + briefing (2–3 h) | 6.1–10.6 | No |
| Drop G10, fold runbook and briefing into G11 | 6.4–10.8 | No |
| Ship booking only (G05 to phase 2) | 6.7–11.1 | No |
| Eval G07 moved to Dev A (tried before the reassignment in step 2) | 7.2–12.2 | No (worse) |
| Same plan, team confirms 6 focused h/day | 5.6–9.4 | **Yes** |
| Same plan, launch date moved to 12 working days | 6.7–11.1 of 12 | **Yes** |

No scope cut tested closes the gap without cutting the floor; only more
focused hours or two more days do. **Assumed choice (the user was not
available, O7):** keep the 10-day target, hold a go/no-go at the end of day 7,
and if G05 or G10 is not done then, move the launch to day 12. Nothing in the
floor moves.

**Cut line.** Phase 1 = G01–G11 ships at all five salons (57–88 h of 112.5 h
after reserve). Phase 2 = G12–G18 (47–80 h) waits. If time runs out early,
each completed goal is still useful in this order: G02 (read-only answers
locally) → G04 (booking end to end locally) → G03 (safe for real customers)
→ G08/G09 (hosted with limits) → G06 (customer-facing widget) → G05 → G10 →
G11. The floor (G03 identity, G04 confirm-and-execute-once, G09 limits) is
never cut.

## Implementation map

| Decision / requirement | Component and integration point (proposed) | GCP responsibility | Primary skill | Verification still needed |
| --- | --- | --- | --- | --- |
| D1, D2 read tools | `LlmAgent` in `agent.py`, tools in `tools/read.py`, `App` + `Runner` used by `gateway.py` | Vertex AI model endpoint | `adk-tool-interface-design` | ADK 2.8.0 constructor names; model ID on Vertex |
| D2, D4, D5 propose and confirm | `tools/propose.py` writes proposals; `operations.py` executes on `POST /v1/proposals/{id}/confirm` | Cloud SQL tables | `safe-api-tool-calls` | Booking API idempotency (O2) |
| D3 identity | `gateway.py` middleware verifies token, sets `customer_id` in session state, checks session owner | — | `adk-tool-auth-and-secrets` | Token format (O1) |
| D7 sessions | `DatabaseSessionService` on Postgres | Cloud SQL Postgres | `adk-memory-architecture` (supporting) | Session schema on 2.8.0 |
| Widget | `widget/` calling the gateway contract above | Static hosting on the existing site | `adk-frontend-integration` | Embedding on the existing site |
| I5 limits, D7 hosting, logs | G08 foundation; G09 `RunConfig(max_llm_calls=8)`, per-customer daily counter table, Cloud Run, structured logs | Cloud Run, Cloud SQL, Secret Manager, Cloud Logging/Trace, billing budget | `deploy-adk-on-google-cloud` | Region, prices |
| I4 recovery | G10 change list and runbook over `booking_operations` | — | `safe-api-tool-calls` | Managers' workflow |
| Quality | `evals/` cases + runner against the fake | — | `adk-agent-evaluation` | Pass-rate baseline |

## Goals and dependencies

| ID and goal | Phase | Type | Human hours | Depends on | Primary skill | State |
| --- | --- | --- | --- | --- | --- | --- |
| G01 Booking API contract confirmed | 1 | discovery | 4–6 | — | `safe-api-tool-calls` | ready |
| G02 Read-only assistant runs locally | 1 | implementation | 5–8 | — | `adk-tool-interface-design` | ready |
| G03 Signed-in customers get their own sessions | 1 | implementation | 6–9 | G01 | `adk-tool-auth-and-secrets` | ready after G01 |
| G04 Customer books a slot with one confirm | 1 | implementation | 7–11 | G01, G02 | `safe-api-tool-calls` | ready after G01, G02 |
| G05 Customer moves or cancels their appointment | 1 | implementation | 5–8 | G04 | `safe-api-tool-calls` | blocked by G04 |
| G06 Chat widget with confirmation cards | 1 | implementation | 7–10 | — | `adk-frontend-integration` | ready |
| G07 Evaluation set of 25–30 conversations | 1 | implementation | 6–10 | G02 | `adk-agent-evaluation` | ready after G02 |
| G08 Cloud foundation provisioned | 1 | implementation | 4–6 | — | `deploy-adk-on-google-cloud` | ready (needs authorization to provision) |
| G09 Gateway hosted with limits and logs | 1 | implementation | 5–8 | G03, G08 | `deploy-adk-on-google-cloud` | blocked |
| G10 Managers' change list, runbook and briefing | 1 | implementation | 4–5 | G04 | `safe-api-tool-calls` | blocked |
| G11 Staging rehearsal and launch at the five salons | 1 | implementation | 4–7 | G05, G06, G07, G09, G10 | `deploy-adk-on-google-cloud` | blocked |
| G12–G18 | 2 | implementation | see below | G11 | see below | proposed |

Run prompts below use the plan path; each ticket file carries its own.

### G01 — Booking API contract confirmed

- **Phase and estimate:** 1; hands-on 3–4, review 1–2, total 4–6; calendar wait: staging credentials from the booking API owner, 0–1 day (request on day 1); owner Dev B
- **Outcome and linked decisions:** settles O1, O2, O3 so D3 and D5 stop being provisional.
- **Scope:** read the booking API's docs/code; make bounded calls to **staging only**: availability, create, reschedule, cancel, list-by-customer, a duplicate create with the same key, a request with an invalid customer token. Out: any production call.
- **Depth:** discovery; writes only to staging test salons.
- **Implementation route:** `docs/architecture/booking-api-contract.md` (endpoints, auth, error codes, idempotency, rate limits) and the final `BookingClient` protocol signatures in `booking_client.py` that G02's fake must match.
- **Prerequisites:** staging credentials.
- **Primary skill:** `safe-api-tool-calls`
- **Supporting skills:** `adk-tool-auth-and-secrets` (customer token verification answer for O1)
- **Acceptance:** contract doc answers O1–O3 with evidence (request/response excerpts, no secrets); a decision on D5 (key replay vs lookup-before-retry); stopping condition: 6 hours spent or all three answered.
- **Verification:** authorized live calls against staging only, listed with results.
- **Execution scope:** staging booking API only, once credentials are issued.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G01 from docs/plans/salon-booking-assistant.md. Read docs/architecture/salon-booking-assistant.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G02 — Read-only assistant runs locally

- **Phase and estimate:** 1; hands-on 3–5, review 2–3, total 5–8; no waits; owner Dev A
- **Outcome and linked decisions:** in `adk web`, a customer fixture asks "what's free with Jo on Saturday at Northside?" and gets correct slots from the fake. D1, D2 (read half), D6.
- **Scope:** `agent.py`, `prompts/instruction.md`, `tools/read.py`, `booking_client.py` protocol (assumed shape; G01 adjusts), `fake_booking.py` with five salons. Out: proposals, gateway, hosting.
- **Depth:** pinned model and `max_llm_calls`; tools read `customer_id` from state only.
- **Implementation route:** `LlmAgent` with three function tools in an `App`; scripted-model Runner tests.
- **Prerequisites:** none; Vertex or API-key access for one manual run.
- **Primary skill:** `adk-tool-interface-design`
- **Supporting skills:** `adk-agent-instructions` (instruction and what stays in code), `adk-model-and-output-contracts` (confirm `gemini-3.8-flash` and ADK 2.8.0 pin)
- **Acceptance:** results bounded (≤ 10 slots); a tool error returns `{status: "error", error: ...}` and the agent offers the salon phone; `customer_id` is not a model-visible parameter (declaration dump); pin confirmed or changed with a note.
- **Verification:** offline `pytest` with scripted model; one manual `adk web` run.
- **Execution scope:** local; one small manual model run.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G02 from docs/plans/salon-booking-assistant.md. Read docs/architecture/salon-booking-assistant.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G03 — Signed-in customers get their own sessions

- **Phase and estimate:** 1; hands-on 4–6, review 2–3, total 6–9; no waits; owner Dev C
- **Outcome and linked decisions:** I1, D3, D7, D8.
- **Scope:** `gateway.py` routes in the contract above, token verification per G01, session owner check, `DatabaseSessionService` on local Postgres, 409 on overlapping turns. Out: confirm endpoint logic (G04), hosting (G09).
- **Depth:** build; cross-customer denial tests.
- **Implementation route:** FastAPI middleware → `customer_id` → session state at creation → Runner per turn.
- **Prerequisites:** G01 (token answer).
- **Primary skill:** `adk-tool-auth-and-secrets`
- **Supporting skills:** `adk-memory-architecture` (session service and restart), `adk-frontend-integration` (gateway JSON contract)
- **Acceptance:** customer B with customer A's session ID → 403 and no model call; invalid token → 401; process restart keeps the conversation; second turn while one runs → 409.
- **Verification:** local integration with Postgres in a container and a real restart.
- **Execution scope:** local.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G03 from docs/plans/salon-booking-assistant.md. Read docs/architecture/salon-booking-assistant.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G04 — Customer books a slot with one confirm

- **Phase and estimate:** 1; hands-on 4–6, review 3–5, total 7–11; no waits; owner Dev A
- **Outcome and linked decisions:** I2, I3, I4; D2, D4, D5.
- **Scope:** `propose_booking` tool, `proposals` and `booking_operations` tables, confirm executor with atomic claim, idempotency per G01, uncertain-outcome reconciliation. Out: move/cancel (G05).
- **Depth:** build; the model holds no write tool.
- **Implementation route:** tool stores proposal and returns summary; confirm route (mounted in G03's gateway, testable alone) rechecks owner, expiry and availability, then calls `BookingClient.create`.
- **Prerequisites:** G01 (idempotency), G02 (agent and fake).
- **Primary skill:** `safe-api-tool-calls`
- **Supporting skills:** `adk-tool-interface-design` (propose tool declaration), `adk-operational-guardrails` (confirmation bound to stored details), `adk-agent-security` (no-write-tool check)
- **Acceptance:** confirm → exactly one appointment in the fake and a reference; double confirm → same result, one appointment; fake commits then times out → `uncertain`, then reconciled to one appointment; expired, foreign or unknown proposal → rejected, nothing written; a scripted model calling every tool never mutates the fake.
- **Verification:** offline `pytest` with the fake's fault modes.
- **Execution scope:** local.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G04 from docs/plans/salon-booking-assistant.md. Read docs/architecture/salon-booking-assistant.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G05 — Customer moves or cancels their appointment

- **Phase and estimate:** 1; hands-on 3–5, review 2–3, total 5–8; no waits; owner Dev A
- **Outcome and linked decisions:** Maya's journey end to end locally; I1–I4 for move and cancel.
- **Scope:** `propose_move`, `propose_cancel`, executor branches; cancellation-window errors surfaced from the API. Out: guest flows.
- **Depth:** build, reusing G04's operation record.
- **Implementation route:** as G04, with ownership recheck of `appointment_id` at confirm.
- **Prerequisites:** G04.
- **Primary skill:** `safe-api-tool-calls`
- **Supporting skills:** `adk-tool-interface-design` (two more declarations; tool count stays 6)
- **Acceptance:** move and cancel each change exactly one appointment after confirm; another customer's appointment ID → refused without a call to the write endpoint; slot taken between propose and confirm → `failed`, agent offers alternatives.
- **Verification:** offline `pytest`.
- **Execution scope:** local.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G05 from docs/plans/salon-booking-assistant.md. Read docs/architecture/salon-booking-assistant.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G06 — Chat widget with confirmation cards

- **Phase and estimate:** 1; hands-on 5–7, review 2–3, total 7–10; no waits; owner Dev B
- **Outcome and linked decisions:** the customer-facing part of the journey; I4 display; D8.
- **Scope:** `widget/` embedded on the existing signed-in site; sends the site's token; renders messages and proposal cards; Confirm calls the confirm route; shows `succeeded` / `failed` / `uncertain` from the response only. Built against a stub of the gateway contract, then pointed at G03. Out: streaming, styling beyond the site's existing CSS.
- **Depth:** build; completed JSON per turn.
- **Primary skill:** `adk-frontend-integration`
- **Supporting skills:** none
- **Acceptance:** input disabled while a turn runs; "Moved — reference …" appears only from a `succeeded` response; `uncertain` shows the checking message; an expired proposal's card says so.
- **Verification:** local browser run against the stub, then against G03 locally.
- **Execution scope:** local.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G06 from docs/plans/salon-booking-assistant.md. Read docs/architecture/salon-booking-assistant.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G07 — Evaluation set of 25–30 conversations

- **Phase and estimate:** 1; hands-on 5–8 (mostly writing and labelling cases), review 1–2, total 6–10; no waits; owner Dev B
- **Outcome and linked decisions:** measured D1 quality; settles O6.
- **Scope:** `evals/` cases for book, move, cancel, ambiguous dates, unknown stylist, out-of-hours, cancellation-window refusal, three prompt-injection attempts ("cancel all appointments", "book for customer 123"); runner against the fake asserting tool trajectory and arguments. Write-tool cases use the planned names `propose_*` until G04/G05 land.
- **Depth:** build; run by hand before each deploy (CI gate is G12).
- **Primary skill:** `adk-agent-evaluation`
- **Supporting skills:** `adk-agent-security` (injection cases assert no foreign proposal)
- **Acceptance:** runner reports pass rate per category; injection cases never propose for another customer; baseline recorded with model ID and prompt SHA.
- **Verification:** local runner with the pinned model (bounded live model calls, ≤ 3 repeats).
- **Execution scope:** local; small model spend.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G07 from docs/plans/salon-booking-assistant.md. Read docs/architecture/salon-booking-assistant.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G08 — Cloud foundation provisioned

- **Phase and estimate:** 1; hands-on 3–4, review 1–2, total 4–6; calendar wait: GCP project, billing and Vertex AI access, 0–1 day (request on day 1); owner Dev C
- **Outcome and linked decisions:** D6, D7 infrastructure exists before the gateway is ready.
- **Scope:** staging and production projects or one project with two environments; Cloud SQL Postgres; runtime service account with least privilege (Vertex AI user, Cloud SQL client, Secret Manager accessor); booking API credentials in Secret Manager; billing budget alert at the A3 allowance; Vertex `gemini-3.8-flash` reachable from the service account; monthly cost estimate from current Vertex and Cloud SQL price pages, dated. Out: deploying the gateway (G09).
- **Depth:** build minimal; floor items: no secrets in code, budget alert.
- **Implementation route:** `deploy/` notes and scripts; a placeholder Cloud Run revision proves the service account can reach Vertex and Cloud SQL.
- **Prerequisites:** the team's authorization to provision in their GCP account.
- **Primary skill:** `deploy-adk-on-google-cloud`
- **Supporting skills:** `adk-tool-auth-and-secrets` (service account and secret access)
- **Acceptance:** placeholder revision reads one secret version and makes one model call as the runtime service account; no user-managed key file exists; budget alert configured; cost estimate written with sources and date.
- **Verification:** authorized hosted check in the team's project.
- **Execution scope:** needs explicit authorization to provision.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G08 from docs/plans/salon-booking-assistant.md. Read docs/architecture/salon-booking-assistant.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G09 — Gateway hosted with limits and logs

- **Phase and estimate:** 1; hands-on 3–5, review 2–3, total 5–8; no waits; owner Dev C
- **Outcome and linked decisions:** I5, D7; the G03 gateway runs in staging and production.
- **Scope:** deploy the gateway and agent to Cloud Run on G08's foundation; `RunConfig(max_llm_calls=8)`; 40 turns/customer/day counter in Postgres; IP rate limit; structured logs and traces with session and operation IDs and token counts, no message text, names or phones; release notes recording the bundle (D6); rollback rehearsed once. Out: SLOs, CI gate.
- **Depth:** build minimal for MVP.
- **Prerequisites:** G03, G08.
- **Primary skill:** `deploy-adk-on-google-cloud`
- **Supporting skills:** `adk-operational-guardrails` (limits), `adk-agent-observability` (logs and traces without content), `adk-release-engineering` (release bundle and rollback)
- **Acceptance:** a staging turn works through the hosted gateway; restarting the instance mid-conversation keeps the session; the 41st turn of the day is refused; the 9th model call in a turn is refused; a log sample has no names, phones or message text; traffic moved back to the previous revision once.
- **Verification:** hosted staging checks.
- **Execution scope:** needs the team's authorization to deploy.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G09 from docs/plans/salon-booking-assistant.md. Read docs/architecture/salon-booking-assistant.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G10 — Managers' change list, runbook and briefing

- **Phase and estimate:** 1; hands-on 3–4, review 1, total 4–5; calendar wait: salon managers briefed, 0–1 day (request the slot on day 1); owner Dev B
- **Outcome and linked decisions:** I4 recovery path; D5's manual reconciliation; the benefit measurement (O4).
- **Scope:** a daily list per salon from `booking_operations` (uncertain and failed first, then succeeded); the runbook for an uncertain operation (check the booking system, mark resolved); a 20-minute briefing for managers. Out: dashboards (G13).
- **Depth:** build minimal; read-only over the assistant's own tables.
- **Prerequisites:** G04 (operation table).
- **Primary skill:** `safe-api-tool-calls`
- **Supporting skills:** none
- **Acceptance:** the list shows a seeded uncertain operation first, with no message text; the runbook resolves it in a dry run; managers have seen it.
- **Verification:** local with seeded rows.
- **Execution scope:** local; briefing with the salons.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G10 from docs/plans/salon-booking-assistant.md. Read docs/architecture/salon-booking-assistant.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G11 — Staging rehearsal and launch at the five salons

- **Phase and estimate:** 1; hands-on 3–5 (includes handoff from Dev A and Dev B), review 1–2, total 4–7; no waits; owner Dev C
- **Outcome and linked decisions:** the profile's "done".
- **Scope:** run Maya's journey and the G07 set against the staging booking API through the hosted widget; enable one salon, then the other four after a clean day. Out: phase 2.
- **Prerequisites:** G05, G06, G07, G09, G10.
- **Primary skill:** `deploy-adk-on-google-cloud`
- **Supporting skills:** `adk-agent-evaluation` (pre-launch run against the recorded baseline)
- **Acceptance:** book, move and cancel succeed on staging with references; G07 pass rate not below the recorded baseline; the first production change is confirmed in the booking system by a manager; rollback path known to all three developers.
- **Verification:** authorized live staging and production checks.
- **Execution scope:** needs the team's go-ahead for production.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G11 from docs/plans/salon-booking-assistant.md. Read docs/architecture/salon-booking-assistant.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### Phase 2 goals (coarser; start after G11)

| ID | Goal | Primary skill | Estimate (h) | Acceptance check |
| --- | --- | --- | --- | --- |
| G12 | Evaluation gate in CI with release manifest | `adk-release-engineering` | 5–9 | A PR that breaks a trajectory case fails CI by exit code |
| G13 | Cost per conversation dashboard and per-customer allowance tuning | `adk-operational-guardrails` | 4–8 | Tokens and cost per successful change visible per day |
| G14 | Session retention (30 days) and customer erasure | `protect-adk-sensitive-data` | 6–10 | Sessions older than 30 days absent after the job; an erasure request removes the customer's sessions and proposal details |
| G15 | Threat model and adversarial suite | `adk-agent-security` | 6–10 | 15 adversarial cases; forbidden effects asserted absent |
| G16 | SLIs, SLOs and alerts | `adk-agent-observability` | 6–10 | An alert on uncertain-operation rate or tool-error rate leads to a stored session |
| G17 | Guest booking with phone verification | `adk-tool-auth-and-secrets` | 12–20 | A guest books only after a verified code and cannot see others' appointments |
| G18 | Production samples into the evaluation set | `adk-agent-observability` | 8–13 | 10 redacted production conversations added as cases |

Phase 2 total: 47–80 h. Run prompt for each:
`/adk-engineer Carry out <G1x> from docs/plans/salon-booking-assistant.md.`

## Later

| Item | Trigger that brings it forward | Risk accepted while it waits | Likely primary skill |
| --- | --- | --- | --- |
| SMS/WhatsApp channel | Customers ask for it; web share stays low | Phone-first customers keep calling | `adk-frontend-integration` |
| Other languages | Non-English requests in logs | Some customers get English only | `adk-agent-instructions` |
| Preference memory (favourite stylist) | Repeat customers re-state preferences often | Slightly longer chats | `adk-memory-architecture` |
| Streaming replies | Measured p95 turn latency > 8 s | Waiting spinner | `adk-frontend-integration` |
| Model migration | Retirement announced for `gemini-3.8-flash` | — | `adk-release-engineering` |
| Secret rotation | Security review or staff change | Long-lived booking API key | `adk-tool-auth-and-secrets` |
| Latency and cost tuning | Measured cost above allowance | — | `optimise-adk-on-google-cloud` |

## What the reviewer reads

| Document | Establishes |
| --- | --- |
| [Design](../architecture/salon-booking-assistant.md) | Method and decisions |
| `evals/README.md` (G07) | Latest result per case |
| This plan | Remaining limits and deferred controls |

## Open decisions for further planning

See the design's [open decisions](../architecture/salon-booking-assistant.md#open-decisions)
(O1–O7). O1 and O2 block G03 and G04's final form; G01 answers them. O7
(10 vs 12 working days) is the cut-line decision above.

## Resume here

- **Next goals:** G01, G02 and G08 are ready now and independent; start them on day 1 (Dev B, Dev A, Dev C). On day 1 also request staging credentials (G01), the GCP project (G08) and the managers' briefing slot (G10). Dev B starts G06 against the stubbed gateway contract once G01's calls are done.
- **Read first:** the design, then this plan.
- **Next action:** Dev B requests staging credentials and starts G01; Dev A starts G02; Dev C requests the GCP project and starts G08.
- **Continuation prompt:**

```text
/adk-engineer Carry out G01 from docs/plans/salon-booking-assistant.md.
Read docs/architecture/salon-booking-assistant.md and preserve its accepted decisions.
Use safe-api-tool-calls with adk-tool-auth-and-secrets.
Work within the staging booking API only, verify G01's acceptance cases, and update
the plan with actual evidence and remaining blockers.
```

After that goal, the same request without a goal ID continues with the next
ready one: `/adk-engineer Continue the next ready goal in docs/plans/salon-booking-assistant.md.`
