# Implementation plan: Card Dispute Assistant

Status: **draft**. Ready goals are identified, but every decision is still
proposed: the user has not reviewed the design.
Architecture: [docs/architecture/card-dispute-assistant.md](../architecture/card-dispute-assistant.md)
Continuation source of truth: this plan

## Destination and constraints

**Destination:** retail customers of the bank dispute a card transaction
in the banking app's chat. One confirmed draft opens exactly one correctly
categorised dispute case in core banking. Production service, GA ~4 months after
start.

**Non-goals:** eligibility or refund decisions, card blocking, evidence uploads
(phase 2), status queries (later), non-card payments.

**Accepted stack:** none accepted yet. The proposed stack is Python, `google-adk==2.8.0`
(working assumption; confirm against the chosen pin in G02), FastAPI service on
Cloud Run in an EU region, Cloud SQL PostgreSQL, Vertex AI Gemini on an EU
endpoint, the bank's existing gateway, IdP and integration layer.

**Pinned artefacts the goals inherit (design D14):** agent model
`gemini-3.8-flash`, judge `gemini-3.8-flash` (secondary metrics only),
prompt `prompts/dispute_assistant/v1.md`. Any change to these is a release
(G12), not a side effect of another goal. Source: `model-lifecycle-2026-10-01.json`
(checked_on 2026-10-08); re-check before G03 live runs.

**Authorization:** design only. This session authorised no implementation,
cloud provisioning, IAM change, paid test, or access to core banking.

**Repository facts:** empty repository at `1450f0f`. All module paths below
are a **proposed** layout:

```text
app/
  main.py                # FastAPI: /sessions, /turns, /drafts/{id}/confirm, /health
  auth.py                # token verification → customer_id; session ownership
  screening.py           # PAN/IBAN detector; promise check on replies
  agent/agent.py         # LlmAgent factory, App/Runner wiring, RunConfig
  agent/tools.py         # five model-facing tools
  agent/callbacks.py     # before_tool_callback ownership checks
  disputes/rules.py      # categories, required facts, windows, deadlines
  disputes/drafts.py     # canonical payload + hash
  disputes/operations.py # operation state machine, submit, reconcile
  integrations/core_banking.py  # adapter (real + fake)
  budgets.py             # allowances, kill switch
prompts/dispute_assistant/v1.md
evals/                   # dev set, adversarial suite, runner config
release/manifest.json
infra/                   # Terraform modules (platform-team conventions)
tests/
```

## Delivery profile and capacity

Profile: **production service** (design § Delivery constraints).

| Phase | Delivers | Goals | Estimate (focused hours) | Capacity and reserve |
| --- | --- | --- | --- | --- |
| 1, ship | GA: one language, six categories, confirm-and-open with reconciliation, pilots passed, sign-offs recorded | G00–G15 | 1,440–2,180 (mid ≈ 1,810) | 6 × 17 wk × 40 h × 0.6 ≈ 2,450 h; 25% reserve → ≈ 1,840 h for goals |
| 2, harden and extend | Evidence uploads (quarantined reader), second language, status queries | G16–G18 | coarse: 500–800 | After GA, same team |

Estimates assume engineers new to ADK and include setup time. Record the actual
effort in each goal's evidence. If phase 1 runs over, cut in this order: G13
reduced to one soak run, G09 per-customer allowance reduced to a global limit,
G10 dashboards reduced to alerts. Never cut the floor, G05, G07 or G14. If
those don't fit, GA moves.

Calendar (assumed start 2026-10-12): **month 1** G00, G01, G02, G11 start;
**month 2** G03, G04, G05, G06; **month 3** G07, G08, G09, G10, G12, external
pentest booked; **month 4** G13, G14 staff pilot (2 weeks) then customer pilot
(2 weeks), G15 sign-offs, GA ~2027-02-08. External approvals (DPIA, model risk,
pentest) are calendar dependencies outside team hours.

If people become unavailable, goals stay useful in this order: G02 → G03 →
G04 → G05 → G06 → G07 (a safe, measured internal build), then G08 → G11 → G10 →
G12 (shippable), then G09, G13, G14.

## Implementation map

| Decision / requirement | ADK or application component and integration point | GCP service/responsibility | Primary skill | Verification still needed |
| --- | --- | --- | --- | --- |
| D1 one agent | `LlmAgent` in `app/agent/agent.py`, run by `Runner` from `/turns` handler | Vertex AI EU endpoint | `adk-workflow-design` | ADK 2.8.0 `App`/`Runner` signatures at the chosen pin |
| D2 / I1 scope | `auth.py` middleware → `session.state["customer_id"]` (written by code at session creation); `callbacks.py` `before_tool_callback` ownership check | Gateway/IdP (bank) | `adk-tool-auth-and-secrets` | Token claims (O1) |
| D4 / I5 tools and categories | `agent/tools.py` FunctionTools; `disputes/rules.py` | none | `adk-tool-interface-design` | Declaration rendering in 2.8.0 (Annotated descriptions not sent in 2.8.0, so put them in docstrings) |
| Instruction | `prompts/dispute_assistant/v1.md` with state templating | none | `adk-agent-instructions` | Rendered-request snapshot |
| D14 model and output | `RunConfig`, `GenerateContentConfig`, model pin | Vertex AI | `adk-model-and-output-contracts` | EU availability (G01) |
| D6/D7 / I2, I3, I7 | `disputes/drafts.py`, `disputes/operations.py`, `/drafts/{id}/confirm`, reconciler entrypoint | Cloud SQL; Cloud Run job + Cloud Scheduler | `safe-api-tool-calls` | Core-banking contract (G00) |
| I6 sensitive data | `screening.py` at ingress before `Runner.run_async`; masked tool projections; telemetry env gates | Model Armor / SDP (optional, G01) | `protect-adk-sensitive-data` | Region availability |
| Security posture | callbacks + adversarial suite in `evals/adversarial/` | none | `adk-agent-security` | Security reviewer sign-off |
| D12 budgets | `budgets.py`, `RunConfig.max_llm_calls` | Cloud SQL | `adk-operational-guardrails` | Allowance values (O10) |
| D8/D13 frontend | JSON turn contract; confirmation card; fallback | Bank gateway | `adk-frontend-integration` | App team's chat component |
| D10 hosting | Container, Cloud Run service, VPC egress | Cloud Run, Cloud SQL, Secret Manager, VPC-SC | `deploy-adk-on-google-cloud` | Platform mandate (O4) |
| Observability | ADK OTel setup, structured logs | Cloud Trace/Monitoring/Logging in region | `adk-agent-observability` | Exporter in 2.8.0 |
| Release | `release/manifest.json`, CI gate, revision tags | CI runner, Cloud Run traffic | `adk-release-engineering` | n/a |
| Dev set and eval | `evals/` | Vertex (bounded live runs) | `adk-agent-evaluation` | SME labels |

## Goals and dependencies

| ID and goal | Phase | Type | Estimate (h) | Depends on | Primary skill | State / blocker |
| --- | --- | --- | --- | --- | --- | --- |
| G00 Core-banking dispute contract | 1 | discovery | 24–40 | — | `safe-api-tool-calls` | ready (needs core-banking team time) |
| G01 EU model, residency and quota facts | 1 | discovery | 16–24 | — | `adk-model-and-output-contracts` | ready (needs platform team) |
| G02 Walking skeleton: scoped transaction lookup | 1 | implementation | 80–120 | — | `adk-tool-auth-and-secrets` | **ready** |
| G03 Dispute intake judgment, measured | 1 | implementation | 160–240 | G02 | `adk-agent-evaluation` | proposed (live runs need G01) |
| G04 Draft and code-bound confirmation | 1 | implementation | 80–120 | G02 | `safe-api-tool-calls` | proposed |
| G05 Exactly-once case submission and reconciliation | 1 | implementation | 160–240 | G04; G00 for live adapter | `safe-api-tool-calls` | proposed (fake adapter first) |
| G06 Sensitive-data boundaries | 1 | implementation | 100–160 | G02 | `protect-adk-sensitive-data` | proposed |
| G07 Threat model and adversarial suite | 1 | implementation | 100–150 | G03, G04 | `adk-agent-security` | proposed |
| G08 App chat panel integration | 1 | implementation | 160–240 | G04 | `adk-frontend-integration` | proposed |
| G09 Budgets, kill switch, fallback | 1 | implementation | 60–90 | G02 | `adk-operational-guardrails` | proposed |
| G10 Observability, SLIs and runbook | 1 | implementation | 80–120 | G02, G11 | `adk-agent-observability` | proposed |
| G11 Environments and deployment | 1 | implementation | 160–240 | G02; O4 | `deploy-adk-on-google-cloud` | proposed |
| G12 Release manifest, CI gate, canary, rollback | 1 | implementation | 80–120 | G03, G11 | `adk-release-engineering` | proposed |
| G13 Load and resilience test | 1 | implementation | 60–100 | G05, G11 | `optimise-adk-on-google-cloud` | proposed |
| G14 Staff pilot then customer pilot | 1 | implementation (operational) | 80–120 | G05–G13 | `adk-agent-observability` | proposed |
| G15 Compliance evidence pack | 1 | discovery/evidence | 40–60 | G06, G07 | `adk-agent-security` | proposed |
| G16 Evidence uploads with quarantined reader | 2 | implementation | coarse 250–400 | GA | `adk-agent-security` | proposed |
| G17 Second language | 2 | implementation | coarse 120–200 | GA | `adk-agent-evaluation` | proposed |
| G18 Dispute status queries | 2 | implementation | coarse 130–200 | GA | `adk-tool-interface-design` | proposed |

Every goal records its depth: production profile, the floor in the design,
and only its own specialist controls.

### G00: Core-banking dispute contract (discovery)

- **Phase and estimate:** 1; 24–40 h.
- **Outcome and linked decisions:** settles O2 and selects the D7 branch for I2.
- **Scope:** questions: does "create dispute case" accept a client reference, is it unique,
  for how long; is there lookup by reference or by `(account, transaction)`;
  timeouts and error codes; test environment and data; who handles manual
  reconciliation. Excluded: building the adapter.
- **Depth:** evidence only; no production access.
- **Implementation route:** interview the core-banking team, read the API spec, run a bounded
  test-environment experiment (same reference twice, then lookup) if access is granted.
- **Prerequisites:** core-banking team contact; test-environment access (external).
- **Primary skill:** `safe-api-tool-calls`.
- **Supporting skills:** none.
- **Acceptance:** `docs/decisions/core-banking-dispute-contract.md` records the replay contract with its source and date,
  the chosen D7 branch, and a fake-server spec for G05.
- **Verification:** document review by the core-banking owner; test-environment transcript if run.
- **Execution scope:** the test-environment experiment needs explicit authorization naming the environment.
- **Stopping condition:** a written answer to each question, or "unknown" with the
  manual-queue branch selected.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G00 from docs/plans/card-dispute-assistant.md. Read docs/architecture/card-dispute-assistant.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G01: EU model, residency and quota facts (discovery)

- **Phase and estimate:** 1; 16–24 h.
- **Outcome and linked decisions:** settles O3 for D3/D14 and the screening layer in I6.
- **Scope:** confirm that `gemini-3.8-flash` is served on Vertex in the chosen EU region, with
  quotas (RPM/TPM) for T2 load, data-retention and abuse-logging terms, Model
  Armor and SDP region availability, and dated prices for the cost formula. Refresh
  the model lifecycle table. Excluded: provisioning.
- **Depth:** official sources cited with URL and access date.
- **Implementation route:** official docs and the bank's Google account team; record facts in
  `docs/decisions/model-and-region.md`.
- **Prerequisites:** none for documentation; quota readback needs project access.
- **Primary skill:** `adk-model-and-output-contracts`.
- **Supporting skills:** `protect-adk-sensitive-data` (screening availability).
- **Acceptance:** each fact has a source and date, or is marked unresolved with
  the decision it keeps provisional. A replacement model is chosen if
  `gemini-3.8-flash` is not available in region.
- **Verification:** reviewer reads the decision record.
- **Execution scope:** web lookup and read-only console readback, if authorised.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G01 from docs/plans/card-dispute-assistant.md. Read docs/architecture/card-dispute-assistant.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G02: Walking skeleton with scoped transaction lookup

- **Phase and estimate:** 1; 80–120 h (includes ADK and local setup for a team new to it).
- **Outcome and linked decisions:** a signed-in test customer asks "show my card payments
  last week" and sees only their own transactions. Implements D1, D2 and I1.
- **Scope:** in: proposed repo layout, `pyproject.toml` with `google-adk` pinned
  (2.8.0 unless the team chooses otherwise), FastAPI `/sessions` and `/turns`,
  token verification against a local test issuer, session ownership check,
  `DatabaseSessionService` on local Postgres, one `LlmAgent` with
  `list_recent_card_transactions` and `get_transaction_detail` against a fake
  core-banking adapter, `before_tool_callback` ownership check,
  `RunConfig.max_llm_calls=10`, and model ID from config (pinned). Out: drafts,
  submission, UI, cloud.
- **Depth:** production for identity and scope; synthetic data only.
- **Implementation route:** `app/auth.py`, `app/agent/agent.py`, `app/agent/tools.py`,
  `app/agent/callbacks.py`, `app/integrations/core_banking.py` (fake). Customer ID only from
  `tool_context.state`.
- **Prerequisites:** none (local).
- **Primary skill:** `adk-tool-auth-and-secrets`.
- **Supporting skills:** `adk-workflow-design` (App/Runner wiring), `adk-tool-interface-design` (first two tool declarations).
- **Acceptance:** (1) the ADK version is confirmed against the chosen pin and the
  interfaces used are recorded; (2) customer A sees only A's transactions;
  (3) a session ID belonging to A, used with B's token, gets 403; (4) a scripted model
  passing B's transaction ref gets `not_found` and the adapter records no read for B;
  (5) restarting the process keeps the session; (6) the declaration dump has 2 tools,
  each ≤ the agreed byte size.
- **Verification:** offline pytest with a scripted model and fake adapter; local
  integration restart test with Postgres in a container. No live model is required.
- **Execution scope:** local only; package install authorised by the user in that session.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G02 from docs/plans/card-dispute-assistant.md. Read docs/architecture/card-dispute-assistant.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G03: Dispute intake judgment, measured

- **Phase and estimate:** 1; 160–240 h (≈ 40 h of SME labelling time is outside the team's hours).
- **Outcome and linked decisions:** the assistant identifies the transaction, asks the
  category's required facts and records a correct draft. Implements D4, I4, I5 and the instruction contract.
- **Scope:** in: `prompts/dispute_assistant/v1.md`, tools
  `check_existing_disputes`, `get_dispute_requirements` and `record_dispute_draft` (draft
  tool writes to the table from G04, or to an in-memory stub until then), `disputes/rules.py`,
  a labelled dev set of ~150 synthetic conversations in L1 (6 categories plus
  ambiguous and "needs human" cases) built with dispute-ops SMEs, a simulated-
  customer harness, metrics (category exact match, required-fact completeness,
  forbidden promise = 0, handoff correctness), thinking/temperature chosen
  from measurement. Out: second language.
- **Depth:** production: gated evaluation; pinned model and judge.
- **Implementation route:** the agent factory from G02; eval runner under `evals/`.
- **Prerequisites:** G02; G01 for live runs on Vertex EU (local scripted tests proceed before it); O7 thresholds (provisional thresholds proposed by the team until set).
- **Primary skill:** `adk-agent-evaluation`.
- **Supporting skills:** `adk-agent-instructions` (prompt), `adk-tool-interface-design` (three new tools), `adk-model-and-output-contracts` (repair budget, model settings).
- **Acceptance:** dev-set report with per-category accuracy and completeness,
  zero forbidden promises, repeat runs with variance reported; invalid draft args
  twice → handoff (scripted test); rendered-request snapshot test passes.
- **Verification:** offline scripted tests; bounded live eval on Vertex staging with a declared request and cost cap.
- **Execution scope:** live runs need an authorised project and budget.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G03 from docs/plans/card-dispute-assistant.md. Read docs/architecture/card-dispute-assistant.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G04: Draft and code-bound confirmation

- **Phase and estimate:** 1; 80–120 h.
- **Outcome and linked decisions:** the customer sees a code-rendered confirmation card and
  confirms it; nothing else can confirm. Implements D6 (draft half) and I3.
- **Scope:** `drafts` table, canonical payload + SHA-256, 30-min confirm window,
  `/drafts/{id}/confirm` with hash check and rechecks (owner, window, no existing
  case, card/account status), card JSON in the turn response. Submission is
  stubbed (G05).
- **Depth:** production.
- **Implementation route:** `app/disputes/drafts.py`, `app/main.py`.
- **Prerequisites:** G02.
- **Primary skill:** `safe-api-tool-calls`.
- **Supporting skills:** `adk-operational-guardrails` (approval binding).
- **Acceptance:** model text "submit it" creates no operation; stale or modified hash →
  409; another customer's draft → 403; expired draft → re-render.
- **Verification:** offline pytest.
- **Execution scope:** local.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G04 from docs/plans/card-dispute-assistant.md. Read docs/architecture/card-dispute-assistant.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G05: Exactly-once case submission and reconciliation

- **Phase and estimate:** 1; 160–240 h.
- **Outcome and linked decisions:** a confirmed draft yields one case and a reference, or an
  honest "pending" that the system resolves. Implements D6, D7, I2 and I7.
- **Scope:** `dispute_operations` with unique constraints and state machine,
  core-banking adapter (fake per G00 spec, then real), deadline 8 s,
  classification (invalid / transient-safe / uncertain), reconciler as a Cloud Run
  job entrypoint (runnable locally), manual queue table and alert hook.
- **Depth:** production: full replay and reconciliation.
- **Implementation route:** `app/disputes/operations.py`, `app/integrations/core_banking.py`.
- **Prerequisites:** G04; G00 for the real adapter.
- **Primary skill:** `safe-api-tool-calls`.
- **Supporting skills:** none.
- **Acceptance:** double confirm → one create call; lost response → `uncertain`,
  reconciler finds the case by reference (or manual queue per D7) with no second
  create; crash between INSERT and send → reconciler lookup first; permanent
  rejection → `failed_permanent` and template; restart preserves all states.
- **Verification:** offline with a fake adapter and fault injection; local integration
  with a real process kill; live in the core-banking test environment once authorised.
- **Execution scope:** local; the test environment needs authorization (G00).
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G05 from docs/plans/card-dispute-assistant.md. Read docs/architecture/card-dispute-assistant.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G06: Sensitive-data boundaries

- **Phase and estimate:** 1; 100–160 h.
- **Outcome and linked decisions:** PANs and credentials never reach the model, storage or
  telemetry. Implements I6, D11 and the promise check for I4.
- **Scope:** PAN/IBAN detector (pattern + Luhn) before `Runner`, masked tool projections,
  reply check (promise phrases, PAN) before release, telemetry content gates,
  log field allowlist, purge jobs (sessions 90 d, drafts 30 d), optional Model
  Armor/SDP layer if G01 confirms.
- **Depth:** production.
- **Implementation route:** `app/screening.py`; env gates in deployment config.
- **Prerequisites:** G02; O5, O6 for values and fail mode.
- **Primary skill:** `protect-adk-sensitive-data`.
- **Supporting skills:** `adk-agent-observability` (content-capture gates).
- **Acceptance:** PAN in input is absent from the captured model request, stored
  events, in-memory exported spans and logs; promise phrase → safe template;
  purge removes expired rows only.
- **Verification:** offline pytest with an in-memory span exporter.
- **Execution scope:** local.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G06 from docs/plans/card-dispute-assistant.md. Read docs/architecture/card-dispute-assistant.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G07: Threat model and adversarial suite

- **Phase and estimate:** 1; 100–150 h, plus security reviewer time.
- **Outcome and linked decisions:** the security posture in the design is proven by tests and
  signed off by the reviewer.
- **Scope:** threat model doc (OWASP LLM/Agentic IDs), enforcement-point map,
  adversarial suite (cases listed in design § Security posture) with
  deterministic forbidden-action assertions, run in CI.
- **Depth:** production: threat model + adversarial suite.
- **Implementation route:** `evals/adversarial/`, `docs/security/threat-model.md`.
- **Prerequisites:** G03, G04.
- **Primary skill:** `adk-agent-security`.
- **Supporting skills:** `adk-agent-evaluation` (suite harness).
- **Acceptance:** each case asserts the absence of the forbidden effect; reviewer
  sign-off recorded; findings tracked.
- **Verification:** offline scripted-model suite; live subset on staging.
- **Execution scope:** local; live subset needs staging.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G07 from docs/plans/card-dispute-assistant.md. Read docs/architecture/card-dispute-assistant.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G08: App chat panel integration

- **Phase and estimate:** 1; 160–240 h.
- **Outcome and linked decisions:** customers use the assistant in the app. Covers D8, D13 and I8.
- **Scope:** JSON turn contract `{reply, card?, status}`, confirmation card, AI
  disclosure banner, "Talk to a person", static-form fallback, error and pending
  states, 409 "still answering", deep link to freeze card.
- **Depth:** production; accessibility per the bank's standard.
- **Implementation route:** the bank app's chat component (inspect it first) via the gateway.
- **Prerequisites:** G04; app team.
- **Primary skill:** `adk-frontend-integration`.
- **Supporting skills:** none.
- **Acceptance:** browser/app tests for the happy path, fallback, pending reference,
  handoff and disclosure; another user's session is not reachable via the API.
- **Verification:** local integration against the service; staging device tests.
- **Execution scope:** app repository access needed.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G08 from docs/plans/card-dispute-assistant.md. Read docs/architecture/card-dispute-assistant.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G09: Budgets, kill switch, fallback

- **Phase and estimate:** 1; 60–90 h.
- **Outcome and linked decisions:** spend and abuse are bounded by the application. Implements D12 and D8.
- **Scope:** per-customer daily allowance (atomic), global admission limit,
  operator kill switch, fallback responses, reconciler exempt from admission.
- **Depth:** production.
- **Implementation route:** `app/budgets.py`, middleware.
- **Prerequisites:** G02; O10 for values.
- **Primary skill:** `adk-operational-guardrails`.
- **Supporting skills:** none.
- **Acceptance:** exhaustion → message + handoff; kill switch → fallback, reconciler
  still runs; concurrent increments don't oversubscribe.
- **Verification:** offline pytest including a concurrency test.
- **Execution scope:** local.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G09 from docs/plans/card-dispute-assistant.md. Read docs/architecture/card-dispute-assistant.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G10: Observability, SLIs and runbook

- **Phase and estimate:** 1; 80–120 h.
- **Outcome and linked decisions:** on-call can see T1–T3 and get from an alert to a session.
- **Scope:** OTel setup with one owner per process, content capture off, structured
  logs with session/invocation/operation IDs, SLIs and burn alerts, runbook for
  uncertain operations, model outage and kill switch.
- **Depth:** production: SLOs and alerts.
- **Implementation route:** `app/telemetry.py` (proposed); Cloud Monitoring config via `infra/`.
- **Prerequisites:** G02, G11.
- **Primary skill:** `adk-agent-observability`.
- **Supporting skills:** `protect-adk-sensitive-data` (content gates).
- **Acceptance:** in-memory exporter shows one span per agent, tool and model call
  with session ID and no content; a staging alert links to a stored session.
- **Verification:** offline exporter test; staging alert drill.
- **Execution scope:** staging needs G11.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G10 from docs/plans/card-dispute-assistant.md. Read docs/architecture/card-dispute-assistant.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G11: Environments and deployment

- **Phase and estimate:** 1; 160–240 h (includes platform-team coordination).
- **Outcome and linked decisions:** dev, staging and prod in the EU region inside VPC-SC. Implements D3 and D10.
- **Scope:** container, Cloud Run service (min 2, multi-zone), reconciler job +
  Scheduler, Cloud SQL private IP, workload identity per component, Secret
  Manager for the integration client cert, Direct VPC egress to Interconnect,
  deploy readback.
- **Depth:** production: recovery and cleanup documented.
- **Implementation route:** `infra/` following platform-team Terraform conventions.
- **Prerequisites:** G02; O4; platform-team project access.
- **Primary skill:** `deploy-adk-on-google-cloud`.
- **Supporting skills:** `adk-tool-auth-and-secrets` (workload identities, secrets).
- **Acceptance:** the staging revision serves the expected image digest and config; no
  key files; the service account has only listed roles; DB backup restore rehearsed.
- **Verification:** authorised staging deploy and readback.
- **Execution scope:** **needs explicit authorization** for project, region and IAM changes.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G11 from docs/plans/card-dispute-assistant.md. Read docs/architecture/card-dispute-assistant.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G12: Release manifest, CI gate, canary, rollback

- **Phase and estimate:** 1; 80–120 h.
- **Outcome and linked decisions:** releases are comparable and reversible. Implements D14.
- **Scope:** `release/manifest.json`, CI gate failing by exit code (deterministic +
  adversarial + dev-set eval with repeat and cost policy; a missing run = fail),
  revision tags and canary thresholds, joint rollback, forward-compatible
  migrations, model/judge retirement calendar.
- **Depth:** production.
- **Implementation route:** CI config (bank's CI), `release/`.
- **Prerequisites:** G03, G11; O9.
- **Primary skill:** `adk-release-engineering`.
- **Supporting skills:** `adk-agent-evaluation` (gate set).
- **Acceptance:** a seeded regression fails the gate; rollback restores the previous
  image, prompt and model pin together; the old revision reads new rows.
- **Verification:** CI run; staging rollback rehearsal.
- **Execution scope:** staging.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G12 from docs/plans/card-dispute-assistant.md. Read docs/architecture/card-dispute-assistant.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G13: Load and resilience test

- **Phase and estimate:** 1; 60–100 h.
- **Outcome and linked decisions:** evidence for T1 and T2 at 2× the A8 peak.
- **Scope:** bounded load against staging with a fake or test core banking; fault
  injection (model 429, core-banking timeout); latency, error rate and cost per case.
- **Depth:** production, measured only.
- **Prerequisites:** G05, G11.
- **Primary skill:** `optimise-adk-on-google-cloud`.
- **Supporting skills:** none.
- **Acceptance:** report with cold/warm runs, failed observations kept, T2 met or
  a tuning item raised.
- **Verification:** authorised staging load with declared request and cost limits.
- **Execution scope:** needs authorization and budget.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G13 from docs/plans/card-dispute-assistant.md. Read docs/architecture/card-dispute-assistant.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G14: Staff pilot, then customer pilot

- **Phase and estimate:** 1; 80–120 h of engineering support.
- **Outcome and linked decisions:** graduation evidence for GA.
- **Scope:** 2-week staff pilot on real accounts, then 2-week customer pilot (~5%
  cohort), daily review of handoffs, manual-queue items and flagged replies;
  redacted samples become eval cases.
- **Depth:** production.
- **Prerequisites:** G05–G13, G15 sign-offs for customer exposure.
- **Primary skill:** `adk-agent-observability`.
- **Supporting skills:** `adk-release-engineering` (cohort traffic), `adk-agent-evaluation` (sample → case).
- **Acceptance:** SLOs met for two consecutive weeks; zero duplicate cases; zero
  cross-customer incidents; product owner GA decision recorded.
- **Verification:** production SLIs and pilot report.
- **Execution scope:** production exposure **requires bank change approval**.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G14 from docs/plans/card-dispute-assistant.md. Read docs/architecture/card-dispute-assistant.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G15: Compliance evidence pack

- **Phase and estimate:** 1; 40–60 h.
- **Outcome and linked decisions:** inputs for DPIA, model-risk review, AI Act Art. 50
  transparency and the DORA register. Settles O5 and O9.
- **Scope:** data-flow map from design § Data and authority; model card (pinned IDs,
  eval results, limits); transparency text; retention values.
- **Depth:** evidence for the bank's own processes; not legal advice.
- **Prerequisites:** G06, G07; DPO and model-risk contacts.
- **Primary skill:** `adk-agent-security`.
- **Supporting skills:** `protect-adk-sensitive-data` (data-flow map).
- **Acceptance:** DPO and model-risk acknowledge receipt; open findings tracked.
- **Verification:** reviewer sign-off records.
- **Execution scope:** documents only.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G15 from docs/plans/card-dispute-assistant.md. Read docs/architecture/card-dispute-assistant.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### Phase 2 (coarse; refine after GA data)

- **G16 Evidence uploads with quarantined reader.** A separate reader agent with no
  tools extracts typed fields from receipts. Malware scan and size limits. The main
  agent gets only validated fields. Primary `adk-agent-security`; supporting
  `protect-adk-sensitive-data`, `adk-workflow-design`. Trigger: rework rate.
- **G17 Second language.** Labelled set in L2, instruction variants, gate per
  language. Primary `adk-agent-evaluation`; supporting `adk-agent-instructions`.
- **G18 Dispute status queries.** Read tool over case management, scoped by
  customer. Primary `adk-tool-interface-design`; supporting `adk-tool-auth-and-secrets`.

## Later

| Item | Trigger that brings it forward | Risk accepted while it waits | Likely primary skill |
| --- | --- | --- | --- |
| Model failover | ADK pin with `FallbackModel` + outage data | Model outage → static form | `adk-model-and-output-contracts` |
| Streaming replies | p95 latency above T2 in pilot | Slower perceived response | `adk-frontend-integration` |
| BigQuery agent analytics | Product analytics needs | Dashboards only | `adk-agent-observability` |
| Governed RAG for help content | Instruction exceeds size budget | Help text in prompt | `adk-memory-architecture` |
| Contact-centre / voice channel | Product decision | n/a | `adk-system-designer` (new design) |
| Judge migration to a different family | O9 decision or judge retirement | Same-family judge bias on secondary metrics | `adk-release-engineering` |
| Cost tuning (context caching, history trimming) | Cost per case above ceiling | Higher cost | `optimise-adk-on-google-cloud` |

## What the reviewer reads

| Document | Establishes |
| --- | --- |
| [Architecture](../architecture/card-dispute-assistant.md) | Method, decisions, invariants, open decisions |
| `evals/README.md` (created in G03) | Latest result per case, linked to run records |
| This plan | Remaining limits, deferred controls, next goal |

## Open decisions for further planning

The canonical list is design § Open decisions (O1–O10). Blocking map:
O1 → G02 live wiring; O2 → G05 real adapter; O3 → G03 live runs, G06 screening;
O4 → G11; O5/O6 → G06; O7 → G03 gate, G10 alerts; O8 → G03 scope; O9 → G12;
O10 → G09 values.

## Resume here

- **Next goal:** G02, the walking skeleton with scoped transaction lookup. It is ready because
  it is local and uses a fake core banking and a test token issuer, so it needs
  no open decision. G00 and G01 can run in parallel with people from outside the team.
- **Read first:** `docs/architecture/card-dispute-assistant.md` (Assumed answers,
  D1, D2, I1), this plan.
- **Next action:** confirm the ADK pin, then scaffold the proposed layout and
  write the cross-customer denial tests before the tools.
- **Continuation prompt:**

```text
/adk-engineer Carry out G02 (walking skeleton with scoped transaction lookup) from docs/plans/card-dispute-assistant.md.
Read docs/architecture/card-dispute-assistant.md and preserve its accepted decisions.
Use adk-tool-auth-and-secrets with adk-workflow-design and adk-tool-interface-design.
Work locally with a fake core-banking adapter and a test token issuer, verify the
cross-customer denial, session-ownership and restart acceptance cases, and update
the plan with actual evidence and remaining blockers.
```

After that goal, the same request without a goal ID continues with the next
ready one: `/adk-engineer Continue the next ready goal in docs/plans/card-dispute-assistant.md.`
