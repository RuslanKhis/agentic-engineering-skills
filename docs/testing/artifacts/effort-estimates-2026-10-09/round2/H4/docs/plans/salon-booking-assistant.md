# Implementation plan: salon booking assistant

Status: draft; ready goals identified (G01, G02, G04, G06 can start on day 1)
Architecture: [../architecture/salon-booking-assistant.md](../architecture/salon-booking-assistant.md)
Continuation source of truth: this plan; tickets in [../tickets/salon-booking-assistant/](../tickets/salon-booking-assistant/) copy its phase 1 goals

## Destination and constraints

Destination: signed-in customers of five salons book, move and cancel real
appointments through a chat widget on the existing website, each change executed
only after the customer presses Confirm on a card rendered from a stored proposal.
Non-goals for phase 1 are listed in the design.

Accepted stack (proposed, awaiting the team): Python, `google-adk` (working pin
2.8.0, decided in G02), FastAPI gateway, Vertex AI `gemini-3.8-flash` (pinned),
Cloud SQL Postgres, Cloud Run, Secret Manager. The repository is empty apart from
this design; every module path below is **proposed**.

Authorization: design only so far. Each goal authorizes local code and offline
tests; G08 and G09 additionally need the team to name the GCP project and approve
deploys, and G09 needs the salon operations lead's sign-off.

Inherited release artefacts: model `gemini-3.8-flash`; prompt version `v1` from
G02/G03; eval set hash from G06. Changing any of them is a release (see G10).

## Delivery profile and capacity

Profile: MVP ([design: delivery constraints](../architecture/salon-booking-assistant.md#delivery-constraints-depth-and-deferred-controls)).

| Phase | Delivers | Goals | Human hours, agent-assisted (range) | Capacity and reserve |
| --- | --- | --- | --- | --- |
| 1, ship | Real customers complete book/move/cancel safely; team sees failures and cost | G01–G09 | 48–79.5 | 3 × 60 h × 0.6 = 108 focused; 25% reserve → 81 |
| 2, harden | Eval gate, traces/SLOs, adversarial suite, retention/erasure, staff hand-off, rollback | G10–G16 | 33–66 | When the team has time after launch |

Estimates are person-hours of human effort with a coding agent (hands-on plus
review and verify), already multiplied by **1.5 for a team new to ADK** (assumption
A2). No new-GCP day is added, because the team already runs the booking API on GCP.
Calendar waits are listed on their goals, not added to hours.

| Person (suggested) | Goals | Hours | Their capacity (focused / after reserve) |
| --- | --- | --- | --- |
| Dev A — backend, knows the booking API | G01, G03, G08 | 18–28.5 | 36 / 27 |
| Dev B — agent and quality | G02, G06, G09 | 13.5–22.5 | 36 / 27 |
| Dev C — web and auth | G04, G05, G07 | 16.5–28.5 | 36 / 27 |

At the high end Dev A and Dev C each use 1.5 h of their own reserve; Dev B has
about 4.5 h of slack and should take the second review of G03 (security-critical)
and help C with G05's restart test. Each goal's review hours are best spent by a
developer other than the owner for G03 and G04.

Longest dependent chain: G01 (6) → G03 (12) → G09 (7.5) = 25.5 h high, about 7
working days at ~3.6 focused hours a day. The busiest person (A or C, 28.5 h high)
needs about 8 of the 10 days, so the **busiest person** is the binding constraint
and phase 1 fits the calendar with roughly 2 days to spare at the high end.

**Cut line.** Fits now: G01–G09, 48–79.5 of 81 hours. If work runs high, cut in
this order (none touches the floor): shrink G06 to 10 cases (saves ~2–3 h); launch
G09 at one salon only and roll out the other four in phase 2 (saves ~2 h); defer
G08's token dashboard to G11 and keep raw token log lines (saves ~1.5 h). If a
single developer is left, the goals stay useful in this order: G01 → G02 → G03 →
G04 → G05 → G07 → G08 → G09, with G06 shrunk.

## Implementation map

| Decision / requirement | ADK or application component and integration point (proposed) | GCP service/responsibility | Primary skill | Verification still needed |
| --- | --- | --- | --- | --- |
| D1 one agent, six tools | `app/agent.py` `LlmAgent` factory; `app/tools/read.py`, `app/tools/propose.py` | Vertex AI model endpoint | `adk-workflow-design` | Confirm `LlmAgent` and `RunConfig` names against the chosen pin |
| D2, D4, D5 propose/confirm/reconcile | `app/proposals.py` (store + claim), `app/executor.py` (confirm, recheck, dispatch, reconcile), `POST /proposals/{id}/confirm` in `app/main.py` | Cloud SQL | `safe-api-tool-calls` | G01's idempotency answer |
| D3 identity | `app/auth.py` middleware → `customer_id` into session state at session creation; tools read `tool_context.state` | — | `adk-tool-auth-and-secrets` | Website token format (A7) |
| D6 sessions, allowance | `DatabaseSessionService` URL from Secret Manager; `app/admission.py` | Cloud SQL Postgres | `adk-memory-architecture` | Session schema creation on the pinned version |
| D7 budgets | `RunConfig(max_llm_calls=8)` in the gateway's `run_async` call; allowance table | Billing budget alert | `adk-operational-guardrails` | Stop exception name on the pin |
| D8 widget contract | `/chat` returns `{reply_text, proposals[], session_id}`; widget in the existing site | — | `adk-frontend-integration` | Site framework and embedding method |
| D9 hosting, release | `Dockerfile`, `release.json`, Cloud Run staging/prod | Cloud Run, Artifact Registry, Secret Manager | `deploy-adk-on-google-cloud` | Project, region, service accounts |

## Goals and dependencies

| ID and goal | Phase | Type | Human hours | Depends on | Primary skill | State / blocker |
| --- | --- | --- | --- | --- | --- | --- |
| G01 Booking API contract and fake | 1 | discovery + implementation | 4.5–6 | — | `safe-api-tool-calls` | ready |
| G02 Read-only assistant answers availability and "my appointments" | 1 | implementation | 4.5–7.5 | G01 fake (start against the design sketch) | `adk-workflow-design` | ready |
| G03 Propose and confirm book/move/cancel exactly once | 1 | implementation | 7.5–12 | G01 | `safe-api-tool-calls` | ready after G01 |
| G04 Signed-in customer sees only their own appointments | 1 | implementation | 6–12 | A7 answered in G01 | `adk-tool-auth-and-secrets` | ready (token format from website code) |
| G05 Conversations survive restarts; per-customer turn allowance | 1 | implementation | 4.5–7.5 | G02 | `adk-memory-architecture` | ready after G02 |
| G06 20-case evaluation set and runner | 1 | implementation | 4.5–7.5 | G02 to run; labelling from day 1 | `adk-agent-evaluation` | ready |
| G07 Chat widget with proposal cards | 1 | implementation | 6–9 | G04; G03 endpoint contract (stub until done) | `adk-frontend-integration` | ready against stub |
| G08 Staging and prod on Cloud Run with logs, cost and rollback | 1 | implementation | 6–10.5 | G04, G05 | `deploy-adk-on-google-cloud` | needs GCP project named |
| G09 Staging acceptance and soft launch | 1 | implementation | 4.5–7.5 | G01–G08 | `adk-agent-evaluation` | waits on salon sign-off |
| G10 Evaluation gate in CI | 2 | implementation | 4.5–9 | G06, G08 | `adk-release-engineering` | proposed |
| G11 Traces, SLOs and alerts | 2 | implementation | 4.5–9 | G08 | `adk-agent-observability` | proposed |
| G12 Adversarial suite and security review | 2 | implementation | 4.5–9 | G03, G06 | `adk-agent-security` | proposed |
| G13 Retention, erasure and log redaction | 2 | implementation | 4.5–9 | G05 | `protect-adk-sensitive-data` | proposed |
| G14 Hand-off to the salon ("talk to a person") | 2 | implementation | 6–12 | G09 | `adk-workflow-design` | proposed; needs salon process |
| G15 Remember a customer's usual stylist and service | 2 | implementation | 4.5–9 | G05 | `adk-memory-architecture` | proposed |
| G16 Canary releases and joint rollback | 2 | implementation | 4.5–9 | G10 | `adk-release-engineering` | proposed |

Phase 1 total: 48–79.5 h. Phase 2 total: 33–66 h for G10–G16 (coarse; phase 1
results may change them).

### G01 — Booking API contract and fake

- **Phase and estimate:** 1; hands-on 3–4, review and verify 1.5–2, total 4.5–6;
  calendar waits none; owner Dev A
- **Outcome and linked decisions:** the team knows exactly how the assistant reads
  and writes appointments, and everyone tests against the same fake. Settles A6, A7; feeds D3, D4, D5.
- **Scope:** read the booking API code/docs; write `docs/booking-api-contract.md`
  (endpoints for salons, services, slots, customer appointments, create, move,
  cancel; auth; error codes; slot uniqueness; idempotency key or status lookup
  support; timezone handling; staging URL); write `app/booking_client.py`
  interface and `tests/fakes/booking_api.py` with scriptable outcomes (success,
  conflict, timeout-after-commit, 5xx). Record how the website's customer token
  can be verified (A7). Out: any change to the booking API itself (if idempotency
  keys are missing, record it as a phase 2 item; D4's reconciliation still works).
- **Depth:** MVP; no real customer data in fixtures.
- **Implementation route:** plain Python client with per-call deadline; no ADK.
- **Prerequisites:** read access to the booking API repository.
- **Primary skill:** `safe-api-tool-calls`
- **Supporting skills:** `adk-tool-auth-and-secrets` (record how the service credential and customer token work)
- **Acceptance:** contract doc answers each open question in the design's Open
  decisions rows A6/A7 with a file:line pointer into the API code; the fake reproduces
  commit-then-timeout; client tests pass offline.
- **Verification:** `pytest tests/test_booking_client.py` offline; no network.
- **Execution scope:** local code only.
- **Status and evidence:** planned
- **Run this goal:** `/adk-engineer Carry out G01 from docs/plans/salon-booking-assistant.md. Read docs/architecture/salon-booking-assistant.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G02 — Read-only assistant answers availability and "my appointments"

- **Phase and estimate:** 1; hands-on 2.5–4, review and verify 2–3.5, total 4.5–7.5; calendar waits none; owner Dev B
- **Outcome and linked decisions:** in a local run, Priya asks "what's free Saturday morning at Northside for a cut?" and "when is my next appointment?" and gets correct answers from the fake API. D1, D7, D8, I4.
- **Scope:** `app/agent.py` (`LlmAgent`, instruction v1 with today's date and salon list injected from state by code), the three read tools, a minimal FastAPI `/chat` around the Runner with `RunConfig(max_llm_calls=8)`, in-memory sessions for now. Choose and record the `google-adk` pin (2.8.0 assumed; consider ≥2.10.0 for production). Out: proposals (G03), auth (G04), persistence (G05).
- **Depth:** MVP; pinned model ID; bounded tool results (≤10 items, no notes fields).
- **Implementation route:** `LlmAgent` + `FunctionTool`s; tools read `customer_id` from `tool_context.state` (G04 sets it; tests set it directly).
- **Prerequisites:** G01's fake (or a temporary one from the design's tool list).
- **Primary skill:** `adk-workflow-design`
- **Supporting skills:** `adk-tool-interface-design` (tool declarations, result bounds, errors); `adk-agent-instructions` (instruction v1, date/timezone templating); `adk-model-and-output-contracts` (pin `gemini-3.8-flash`, sampling, thinking setting)
- **Acceptance:** scripted-model Runner test calls each read tool with valid args; ambiguous "Saturday" across a DST change resolves to salon-local time; a 9th model call in one turn stops with the designed message; declaration dump shows no customer-ID parameter; pinned ADK and model IDs recorded.
- **Verification:** offline `pytest` with a scripted model; a live smoke run against the fake API is optional and needs a Vertex AI project.
- **Execution scope:** local code; live model calls only if the team supplies a project.
- **Status and evidence:** planned
- **Run this goal:** `/adk-engineer Carry out G02 from docs/plans/salon-booking-assistant.md. Read docs/architecture/salon-booking-assistant.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G03 — Propose and confirm book/move/cancel exactly once

- **Phase and estimate:** 1; hands-on 3–5, review and verify 4.5–7, total 7.5–12; calendar waits none; owner Dev A (second review by Dev B)
- **Outcome and linked decisions:** Priya sees a card with the exact change and the booking changes once when she presses Confirm, never otherwise. D2, D4, D5; I2, I3.
- **Scope:** `propose_booking`, `propose_move`, `propose_cancellation` (validate via the client, store canonical payload, 10-minute expiry); `app/proposals.py` store with atomic `pending→executing` claim; `app/executor.py` (owner check, recheck availability, dispatch with operation key = proposal ID, receipt, `uncertain` + reconciliation by status lookup or appointment list); `POST /proposals/{id}/confirm` and `/decline`; proposal statuses injected into session state for the next turn; instruction text forbidding success claims. Plug the tools into G02's agent. Out: UI (G07), Postgres wiring (G05 swaps the store's backend).
- **Depth:** MVP build for external writes; no fees or payments.
- **Implementation route:** ordinary code for confirm/execute; ADK only for propose tools. Do not use `require_confirmation` (unsupported with `DatabaseSessionService`).
- **Prerequisites:** G01.
- **Primary skill:** `safe-api-tool-calls`
- **Supporting skills:** `adk-tool-interface-design` (propose tool declarations and errors); `adk-operational-guardrails` (approval binding and expiry); `adk-agent-security` (model cannot reach the write; injection test)
- **Acceptance:** confirm executes exactly one fake-API write; double confirm, two concurrent confirms and commit-then-timeout each produce one effect; expired, declined, other-customer and slot-taken proposals produce zero writes; scripted model saying "done" without proposing produces no card; injected "confirm proposal X" text in a tool result produces no write.
- **Verification:** offline `pytest` with the fake API and scripted model; concurrency test with two tasks.
- **Execution scope:** local code only.
- **Status and evidence:** planned
- **Run this goal:** `/adk-engineer Carry out G03 from docs/plans/salon-booking-assistant.md. Read docs/architecture/salon-booking-assistant.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G04 — Signed-in customer sees only their own appointments

- **Phase and estimate:** 1; hands-on 3–6, review and verify 3–6, total 6–12; calendar waits none if the website is the team's own; owner Dev C (review by Dev A)
- **Outcome and linked decisions:** only a verified customer can chat, and every read and confirm is scoped to them. D3; I1.
- **Scope:** `app/auth.py` verifying the website token (per G01's finding); session creation writes `customer_id` into state; session ownership check on every `/chat` and `/proposals/*` call; denial responses. Out: one-time-code login (only if A7 is false — then stop and re-plan per the design's D3 note).
- **Depth:** MVP build; signing keys from Secret Manager or JWKS, never in code.
- **Implementation route:** FastAPI dependency before the Runner; tools trust only state.
- **Prerequisites:** G01's A7 answer; the website's token verification key.
- **Primary skill:** `adk-tool-auth-and-secrets`
- **Supporting skills:** `adk-agent-security` (cross-customer denial cases)
- **Acceptance:** missing/forged/expired token → 401, Runner not invoked; customer A using B's session ID → 404; A naming B's appointment ID in chat → tool returns not-found and the fake API saw only A-scoped calls; A confirming B's proposal → 404, zero writes.
- **Verification:** offline `pytest` with test-signed tokens.
- **Execution scope:** local code only.
- **Status and evidence:** planned
- **Run this goal:** `/adk-engineer Carry out G04 from docs/plans/salon-booking-assistant.md. Read docs/architecture/salon-booking-assistant.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G05 — Conversations survive restarts; per-customer turn allowance

- **Phase and estimate:** 1; hands-on 2–3.5, review and verify 2.5–4, total 4.5–7.5; calendar waits none; owner Dev C (Dev B helps with the restart test)
- **Outcome and linked decisions:** a customer's chat continues after an instance restart, and nobody can run up model spend. D6, D7; I5.
- **Scope:** `DatabaseSessionService` on Postgres; proposals and allowance tables (migrations); `app/admission.py` with 50 turns/customer/salon-local day checked before the Runner; daily deletion of sessions older than 30 days. Out: erasure on request (G13).
- **Depth:** MVP; DB URL from environment/Secret Manager.
- **Implementation route:** local Postgres container for tests; Cloud SQL in G08.
- **Prerequisites:** G02.
- **Primary skill:** `adk-memory-architecture`
- **Supporting skills:** `adk-operational-guardrails` (allowance admission and exhaustion message)
- **Acceptance:** restart the gateway process mid-conversation → next turn keeps context; 51st turn rejected with zero model calls; two concurrent turns do not exceed the allowance; proposals survive restart and remain confirmable.
- **Verification:** local integration with a Postgres container (Docker needed); offline unit tests for admission.
- **Execution scope:** local only.
- **Status and evidence:** planned
- **Run this goal:** `/adk-engineer Carry out G05 from docs/plans/salon-booking-assistant.md. Read docs/architecture/salon-booking-assistant.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G06 — 20-case evaluation set and runner

- **Phase and estimate:** 1; hands-on 3.5–5.5 (mostly writing and labelling cases), review and verify 1–2, total 4.5–7.5; calendar waits none; owner Dev B
- **Outcome and linked decisions:** the team can say how often the assistant picks the right action before launch. I2, I4.
- **Scope:** 20 multi-turn cases on synthetic customers: 5 book, 5 move, 4 cancel, 2 ambiguous date/salon needing clarification, 2 out of scope (prices dispute, complaints), 1 other customer's appointment, 1 injected instruction in a service description. Expected tool calls and proposal payloads; a runner that reports per-case pass/fail and model calls. Out: CI gate (G10), judge-model scoring.
- **Depth:** MVP; deterministic checks on proposals and tool calls, no LLM judge.
- **Implementation route:** ADK evaluation against the fake API; live model runs capped at 200 model calls per run.
- **Prerequisites:** G02 to run; G03 for propose cases.
- **Primary skill:** `adk-agent-evaluation`
- **Supporting skills:** none
- **Acceptance:** runner reports all 20 cases with pass/fail and call counts; the two security cases assert zero proposals for the forbidden action; a baseline result is recorded with model and prompt version.
- **Verification:** offline runner structure test; live run needs a Vertex AI project (bounded, authorized by the team).
- **Execution scope:** local; live run only with a named project.
- **Status and evidence:** planned
- **Run this goal:** `/adk-engineer Carry out G06 from docs/plans/salon-booking-assistant.md. Read docs/architecture/salon-booking-assistant.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G07 — Chat widget with proposal cards

- **Phase and estimate:** 1; hands-on 3–4.5, review and verify 3–4.5, total 6–9; calendar waits none; owner Dev C
- **Outcome and linked decisions:** Priya chats on the existing site and confirms or declines changes on cards. D8; I2.
- **Scope:** widget in the existing site (signed-in pages only, behind a per-salon feature flag); renders reply as plain text (no links, images or HTML); renders cards only from `/chat` `proposals[]`; Confirm/Keep buttons call the endpoints; shows `done`, `rejected_stale`, `uncertain` ("checking…") states from responses. Out: streaming, other languages.
- **Depth:** MVP build.
- **Implementation route:** existing site framework (unknown; inspect); talks to the gateway with the site token.
- **Prerequisites:** G04; G03 endpoint contract (stub until merged).
- **Primary skill:** `adk-frontend-integration`
- **Supporting skills:** none
- **Acceptance:** a reply containing `<img src=…>` or a link renders as text; a card is never shown from reply text alone; Confirm twice shows one receipt; flag off → widget absent.
- **Verification:** component tests plus a local run against the gateway with the fake API.
- **Execution scope:** local; no deploy of the website.
- **Status and evidence:** planned
- **Run this goal:** `/adk-engineer Carry out G07 from docs/plans/salon-booking-assistant.md. Read docs/architecture/salon-booking-assistant.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G08 — Staging and prod on Cloud Run with logs, cost and rollback

- **Phase and estimate:** 1; hands-on 4–7, review and verify 2–3.5, total 6–10.5; calendar waits: budget alert may need the billing admin (hours to a day); owner Dev A
- **Outcome and linked decisions:** the assistant runs in staging and prod, the team can see errors, token use and write outcomes per session, and can roll back in minutes. D7, D9.
- **Scope:** Dockerfile, Cloud Run service per environment with its own service account (Vertex AI user, Cloud SQL client, secret accessor for the booking-API credential only); Cloud SQL database; `release.json` (image digest, prompt version, model ID, tool-schema hash, eval-set hash, secret versions); structured JSON logs with session/invocation/proposal IDs, token counts and write outcomes, no message text; billing budget alert at 50/90/100% of A3; rollback rehearsal to the previous revision. Out: traces and SLOs (G11), CI gate (G10).
- **Depth:** MVP; minimal observability per the design table.
- **Implementation route:** Cloud Run, Artifact Registry, Secret Manager, Cloud SQL connector.
- **Prerequisites:** G04, G05; the team names the GCP project and region and authorizes deploys.
- **Primary skill:** `deploy-adk-on-google-cloud`
- **Supporting skills:** `adk-release-engineering` (release manifest, rollback unit); `adk-agent-observability` (log fields, token accounting, content capture off)
- **Acceptance:** staging readback shows the expected image digest and model ID; a test conversation's log lines carry IDs and token counts but no message text; traffic switched to the previous revision and back; the service account cannot read other secrets.
- **Verification:** authorized hosted checks in staging; prod deploy only after G09's staging pass.
- **Execution scope:** needs explicit authorization for the named project; nothing deployed by design work.
- **Status and evidence:** planned
- **Run this goal:** `/adk-engineer Carry out G08 from docs/plans/salon-booking-assistant.md. Read docs/architecture/salon-booking-assistant.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G09 — Staging acceptance and soft launch

- **Phase and estimate:** 1; hands-on 3–5, review and verify 1.5–2.5, total 4.5–7.5; calendar waits: salon operations sign-off on wording and cancellation policy (1–3 days; request it on day 1); owner Dev B with all three for the launch hour
- **Outcome and linked decisions:** real customers at one salon, then all five, use the assistant; the team has a baseline. Design "Outcome to improve".
- **Scope:** G06 live run against staging (≤200 model calls); end-to-end book/move/cancel by each developer on staging; record the salon's current phone volume for these requests as the baseline; enable the flag for one salon, watch logs for 2 days, then the other four; written runbook (disable flag, roll back, reconcile an `uncertain` proposal).
- **Depth:** MVP; launch decision is the team's.
- **Implementation route:** feature flag, Cloud Run prod.
- **Prerequisites:** G01–G08; salon sign-off.
- **Primary skill:** `adk-agent-evaluation`
- **Supporting skills:** `adk-agent-observability` (what to watch during the soft launch)
- **Acceptance:** eval pass rate recorded and agreed by the team (assumed bar: ≥18/20 with both security cases passing); three staging journeys complete with correct receipts; runbook tried once; flag on for one salon.
- **Verification:** authorized live and hosted checks only.
- **Execution scope:** needs the team's go decision; changes real appointments only for consenting test customers until the flag is on.
- **Status and evidence:** planned
- **Run this goal:** `/adk-engineer Carry out G09 from docs/plans/salon-booking-assistant.md. Read docs/architecture/salon-booking-assistant.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### Phase 2 goals (coarse)

- **G10 Evaluation gate in CI** — 4.5–9 h; primary `adk-release-engineering`, supporting `adk-agent-evaluation`. Acceptance: a prompt change that breaks a G06 case fails CI by exit code; model and judge IDs read from `release.json`.
- **G11 Traces, SLOs and alerts** — 4.5–9 h; primary `adk-agent-observability`. Acceptance: one span per agent, tool and model call with session ID; SLI "confirmed proposals reaching `done` / confirmed" with an alert on a measured baseline.
- **G12 Adversarial suite and security review** — 4.5–9 h; primary `adk-agent-security`. Acceptance: 15+ injection and cross-customer cases, each asserting zero forbidden proposals or writes; findings mapped to OWASP IDs.
- **G13 Retention, erasure and log redaction** — 4.5–9 h; primary `protect-adk-sensitive-data`, supporting `adk-memory-architecture`. Acceptance: an erasure request deletes the customer's sessions and proposals and leaves no message content in logs.
- **G14 Hand-off to the salon** — 6–12 h; primary `adk-workflow-design`. Acceptance: "I want to talk to someone" creates one salon task with the conversation summary, visible to the customer as pending.
- **G15 Remember usual stylist and service** — 4.5–9 h; primary `adk-memory-architecture`. Acceptance: owner-scoped profile used in a new session; customer can clear it; cross-customer denial.
- **G16 Canary and joint rollback** — 4.5–9 h; primary `adk-release-engineering`. Acceptance: 10% traffic to a new revision with prompt and model rolled back together on failure.

## Later

| Item | Trigger that brings it forward | Risk accepted while it waits | Likely primary skill |
| --- | --- | --- | --- |
| Streaming replies | Measured p90 turn latency above 8 s | Slower perceived replies | `adk-frontend-integration` |
| SMS/WhatsApp channel | Customer demand or salon request | Web-only reach | `adk-agent-interoperability` |
| Second language | A salon serving another-language clientele | — | `adk-agent-instructions` |
| Deposits, cancellation fees | Business decides to charge | None now (no money in scope) | `safe-api-tool-calls` |
| Idempotency key in the booking API | G01 finds none and reconciliation shows ambiguity | Rare `uncertain` cards resolved by listing | `safe-api-tool-calls` |
| Cost and latency tuning | Spend above 50% of budget or latency trigger | Paying list price | `optimise-adk-on-google-cloud` |
| Model migration | Lifecycle table shows a retirement date for `gemini-3.8-flash` | — | `adk-model-and-output-contracts` |
| Staff-facing use | Salons ask to book for walk-ins | Staff use the existing system | `adk-tool-auth-and-secrets` |

## What the reviewer reads

| Document | Establishes |
| --- | --- |
| [Design](../architecture/salon-booking-assistant.md) | Method, decisions, assumptions |
| `docs/eval/summary.md` (created by G06) | Latest result per case |
| This plan | Remaining limits and deferred controls |

## Open decisions for further planning

See the design's [Open decisions](../architecture/salon-booking-assistant.md#open-decisions); A6 and A7 are settled by G01.

## Resume here

- **Next goal:** G01 Booking API contract and fake — it has no prerequisites and settles the two assumptions that most change G03 and G04. G02, G04 and G06's labelling can start the same day.
- **Read first:** the design, this plan, the booking API repository.
- **Next action:** read the booking API's create/move/cancel handlers and its auth.
- **Continuation prompt:**

```text
/adk-engineer Carry out G01 Booking API contract and fake from docs/plans/salon-booking-assistant.md.
Read docs/architecture/salon-booking-assistant.md and preserve its accepted decisions.
Use safe-api-tool-calls with adk-tool-auth-and-secrets.
Work within local code and offline tests, verify the fake reproduces commit-then-timeout
and the contract answers A6 and A7, and update the plan with actual evidence and remaining blockers.
```

After that goal, `/adk-engineer Continue the next ready goal in docs/plans/salon-booking-assistant.md.`
