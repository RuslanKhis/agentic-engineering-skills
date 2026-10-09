# Implementation plan: card-transaction dispute assistant

Status: draft. Ready goals are identified. Nothing has been implemented.
Architecture: [docs/architecture/card-dispute-agent.md](../architecture/card-dispute-agent.md)
Continuation source of truth: this plan.

## Destination and constraints

The destination is GA of the dispute assistant in about 17 weeks. By then an
authenticated customer can identify a card transaction, give the facts the
rules need, confirm with step-up and receive a core banking case reference.
Each confirmation files at most one case. Non-goals are in the design. All
decisions are **proposed**. The assumptions Q1–Q15 and open decisions D-01–D-07
are in the design and are not repeated here.

**Inspected:** the repository contains only `.claude/skills/`. There is no
application code, no manifest and no installed dependencies.

**Inherited pins (proposed):**
- `google-adk==2.8.0`, the version the specialists were checked against.
  Confirming it against the chosen pin is a G01 acceptance item.
- Agent model `gemini-3.8-flash` on Vertex AI in the EU, per the lifecycle
  table checked 2026-10-08.
- Judge `gemini-3.8-flash`, with a separate pinned judge prompt.
- Prompt version `intake-v0`.

Changing any of these is a release (G11), not a side effect.

**Authorization:** this session was design-only. Each goal below authorizes
only local code and offline tests. Cloud provisioning, IAM, live model calls
and calls to the core banking test environment need explicit authorization
naming the target project.

**Proposed module layout (greenfield, unverified):**

```text
dispute_assistant/
  api/            FastAPI app: auth middleware, /sessions, /turns, /drafts/{id}/confirm, /uploads
  agent/          app.py (App/Runner factory), intake_agent.py, prompts/intake-v0.md
  tools/          transactions.py, disputes.py (read + save_dispute_draft), context.py (trusted customer scope)
  eligibility/    rules.py, rule_tables/<version>.yaml
  operations/     model.py (dispute_operation state machine), submit.py, reconcile.py, core_client.py
  screening/      ingress.py (SDP, Model Armor adapters), release_check.py
  guardrails/     budgets.py, killswitch.py, turn_lease.py
  telemetry/      setup.py
tests/            offline/ (fake model, fake core), integration/, eval/
infra/            deployment config, out of scope until G09
```

## Implementation map

| Decision / requirement | ADK or application component and integration point | GCP service/responsibility | Primary skill | Verification still needed |
| --- | --- | --- | --- | --- |
| DD-01 single agent | `LlmAgent` in `agent/intake_agent.py`, served through `App`/`Runner` in `agent/app.py`, called from `api/turns` | Vertex AI (model) | `adk-workflow-design` | Constructor names against the pin |
| DD-04 identity scope (I1, I2) | Middleware verifies the OIDC token → `customer_id` in invocation context. `before_tool_callback` re-asserts it. Tools read the scope from `tools/context.py`, never from arguments | Workload identity, IdP JWKS | `adk-tool-auth-and-secrets` | How trusted context reaches tools in 2.8.0 |
| Tool declarations | `tools/*.py` function tools with bounded, masked results | — | `adk-tool-interface-design` | Declaration size, selection accuracy |
| Instructions | `agent/prompts/intake-v0.md`, versioned. Rendered-request snapshot | — | `adk-agent-instructions` | Templating behavior on the pin |
| Draft output contract | Pydantic model for `save_dispute_draft` args. Repair budget of 2 | Vertex backend | `adk-model-and-output-contracts` | EU availability of the model (D-01) |
| I5 eligibility | `eligibility/rules.py` on versioned tables | — | ordinary code (lead: `adk-model-and-output-contracts` in G02) | Rule content (D-03) |
| DD-02/DD-03 confirm and submit | `api/confirm` → `operations/submit.py` → `core_client.py`. `operations/reconcile.py` job | Cloud SQL, Cloud Scheduler + Cloud Run job, Secret Manager | `safe-api-tool-calls` | Core replay contract (D-02) |
| DD-06 sessions + turn lease | `DatabaseSessionService` (Postgres). `guardrails/turn_lease.py` | Cloud SQL Postgres (EU) | `adk-memory-architecture` | API on the pin. Migration behavior |
| DD-08 screening (I6) | `screening/ingress.py` before session append and the model call. `release_check.py` before response | SDP, Model Armor (EU) | `protect-adk-sensitive-data` | Regional availability (D-01) |
| DD-09 browser contract | JSON turn response `{messages[], draft?, operation?}`. Draft rendered from the stored record | Existing gateway | `adk-frontend-integration` | App shell embedding (D-04) |
| DD-10 budgets | `RunConfig.max_llm_calls` + `guardrails/budgets.py` reservations + kill switch | Cloud SQL control table | `adk-operational-guardrails` | Counter semantics on the pin |
| Security posture | Adversarial suite in `tests/offline/adversarial/` | — | `adk-agent-security` | Reviewer sign-off |
| DD-05 hosting | Container with the actual entrypoint, Direct VPC egress | Cloud Run (EU), Artifact Registry | `deploy-adk-on-google-cloud` | D-01, D-05 |
| SLIs, telemetry | `telemetry/setup.py`, one owner per process, content capture off | Cloud Trace, Monitoring, Logging | `adk-agent-observability` | Exporter test |
| Release manifest and gates | CI pipeline, manifest, traffic split | CI runner, Cloud Run revisions | `adk-release-engineering` | — |

## Goals and dependencies

| ID and goal | Type | Depends on | Primary skill | State / blocker |
| --- | --- | --- | --- | --- |
| D-01 Verify EU service availability, quotas, prices; confirm ADK pin | discovery | — | `deploy-adk-on-google-cloud` | ready (needs network and documentation access) |
| D-02 Core banking dispute API contract | discovery | — | `safe-api-tool-calls` | ready (needs the core team) |
| D-03 Rule table, baseline, labelled dev set | discovery | — | `adk-agent-evaluation` | ready (needs disputes ops) |
| G01 Customer finds their own transaction through the agent (walking skeleton) | implementation | — | `adk-workflow-design` | **ready** |
| G02 Validated dispute draft with deterministic eligibility | implementation | G01. D-03 for real rules (a placeholder table is fine) | `adk-model-and-output-contracts` | ready with placeholder rules |
| G03 Evaluation baseline on the labelled dev set | implementation | G02, D-03 | `adk-agent-evaluation` | blocked on D-03 |
| G04 Confirm and submit exactly once, with reconciliation | implementation | G02. D-02 for live | `safe-api-tool-calls` | ready offline. Live blocked on D-02 |
| G05 Sensitive-data boundaries | implementation | G01 | `protect-adk-sensitive-data` | ready offline |
| G06 Threat model and adversarial suite | implementation | G02, G04 | `adk-agent-security` | proposed |
| G07 App and gateway contract with step-up | implementation | G04, D-04 | `adk-frontend-integration` | blocked on D-04 |
| G08 Budgets, turn lease, kill switch | implementation | G01 | `adk-operational-guardrails` | ready offline |
| G09 First shared non-prod deployment (EU) | implementation | G04, G05, G08, D-01, D-05 | `deploy-adk-on-google-cloud` | blocked on D-01, D-05 and authorization |
| G10 SLIs, alerts, runbook | implementation | G09 | `adk-agent-observability` | proposed |
| G11 Release manifest, eval gate, canary, rollback | implementation | G03, G09 | `adk-release-engineering` | proposed |
| G12 Load test and staff + limited-customer pilot | implementation | G06, G07, G10, G11, D-07 | `optimise-adk-on-google-cloud` | proposed (coarse) |
| G13 GA readiness: retention and erasure jobs, DPIA evidence, rollback rehearsal | implementation | G12, D-06 | `adk-memory-architecture` | proposed (coarse) |

**Suggested schedule** (17 weeks, 6 engineers, assumed):

| Weeks | Work |
| --- | --- |
| 1–2 | D-01..D-04 in parallel with G01 |
| 3–6 | G02, G04, G05, G08 in parallel across 4 engineers |
| 5–8 | G03 |
| 7–9 | G06 (security reviewer leads) and G07 |
| 9–11 | G09 and G10 |
| 10–12 | G11 |
| 13–15 | G12 pilot |
| 16–17 | G13 and the GA ramp |

Security reviewer checkpoints are in weeks 2 (threat model on this design), 8
(G06) and 12 (pre-pilot).

### G01: Customer finds their own transaction through the agent

- **Outcome and linked decisions:** an authenticated customer describes a
  charge and the agent returns the matching masked transactions from their own
  cards only. Links: DD-01, DD-04, DD-06, I1, I2.
- **Scope:** API skeleton (`/sessions`, `/turns`), auth middleware with a test
  JWKS, `intake_agent` with `find_card_transactions`, `get_transaction` and
  `list_open_disputes` against a fake core client. Session persistence on local
  Postgres. Excludes drafts, submission, screening and deployment.
- **Implementation route:** `LlmAgent` + `App`/`Runner` in `agent/app.py`.
  Trusted `customer_id` is set by middleware and re-asserted by
  `before_tool_callback`. Opaque per-session `txn_ref` mapping in
  `tools/context.py`. `DatabaseSessionService`. All modules are proposed.
- **Prerequisites:** none. Python 3.11. The ADK is not installed in the
  design environment. Installing it is part of this goal, with authorization.
- **Primary skill:** `adk-workflow-design`
- **Supporting skills:** `adk-tool-auth-and-secrets` (trusted scope, cross-user
  denial), `adk-tool-interface-design` (three read declarations, bounded
  results), `adk-agent-instructions` (intake-v0 prompt and rendered-request test).
- **Acceptance:** a scripted model finds Anna's transaction. A scripted model
  passing customer B's `txn_ref` gets `not_found` and the fake core sees no
  B-scoped call. Session B opened with A's token returns 404. Tool results
  are at most 10 rows with masked PAN. A restart of local Postgres preserves
  the session. **The ADK 2.8.0 pin is confirmed or replaced against the chosen
  version, and the difference is recorded.**
- **Verification:** offline pytest with a fake model and a fake core, plus
  local Postgres integration. No live model calls.
- **Execution scope:** local code and tests in this repository. Package
  installation needs the user's go-ahead. No cloud.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G01 from docs/plans/card-dispute-agent.md. Read docs/architecture/card-dispute-agent.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G02: Validated dispute draft with deterministic eligibility

- **Outcome and linked decisions:** the agent saves a typed draft, and code
  decides eligibility and the missing facts. Links: DD-01, I5, the output
  contract.
- **Scope:** `save_dispute_draft` with a pydantic schema per reason, including
  `unclear`. `eligibility/rules.py` with a versioned placeholder rule table.
  Draft versioning. Repair budget of 2 and the `cannot_complete` path.
  Excludes confirmation and real rule content (D-03).
- **Implementation route:** the function tool validates its args and calls
  eligibility. It returns `{status, missing[], draft_version}`. The draft
  table is in Postgres.
- **Prerequisites:** G01.
- **Primary skill:** `adk-model-and-output-contracts`
- **Supporting skills:** `adk-tool-interface-design` (draft tool declaration and
  actionable errors), `adk-agent-instructions` (ask only for missing facts).
- **Acceptance:** a scripted model emitting prose, invalid args, and valid but
  wrong args each gets the designed outcome. An ineligible transaction (outside
  the window) shows the deterministic reason even when the model argues
  otherwise. The draft stores the rule version.
- **Verification:** offline table-driven tests.
- **Execution scope:** local only.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G02 from docs/plans/card-dispute-agent.md. Read docs/architecture/card-dispute-agent.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G04: Confirm and submit exactly once, with reconciliation

- **Outcome and linked decisions:** one confirmation leads to at most one core
  case, and uncertain outcomes are recovered. Links: DD-02, DD-03, I3, I4.
- **Scope:** `/drafts/{id}/confirm` binding draft version, payload hash and a
  step-up reference (stubbed). `dispute_operation` state machine
  (`CONFIRMED → SUBMITTING → SUBMITTED | FAILED | UNCERTAIN`). Core client with
  `operation_id`. Reconciler job. Manual-reconciliation queue for when lookup
  is unsupported. Live core test only after D-02.
- **Implementation route:** application code, not an ADK tool. The unique
  constraint on `(draft_id, draft_version)` and the atomic claim live in
  Postgres. Core credentials come from Secret Manager in the hosted setting
  and from a local fake here.
- **Prerequisites:** G02. D-02 for live evidence.
- **Primary skill:** `safe-api-tool-calls`
- **Supporting skills:** `adk-operational-guardrails` (approval binding to the
  stored proposal), `adk-tool-auth-and-secrets` (core credential kept outside
  model reach).
- **Acceptance:** each fault (timeout, lost response after commit, worker crash
  mid-request, double confirm, two devices, changed draft, rule change before
  confirm) produces exactly one case at the fake core and the designed
  customer status. No path re-dispatches an `UNCERTAIN` operation without the
  same `operation_id`.
- **Verification:** offline fault-injection tests with a fake core that has
  configurable replay semantics. Live verification is in the core test
  environment after D-02, with authorization.
- **Execution scope:** local only until D-02 and authorization.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G04 from docs/plans/card-dispute-agent.md. Read docs/architecture/card-dispute-agent.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G05: Sensitive-data boundaries

- **Outcome and linked decisions:** PAN, CVV, PIN and OTP never reach the
  model, session store or logs. Links: DD-08, DD-09, I6.
- **Scope:** ingress screening adapter (SDP, Model Armor) behind an interface,
  with a local fake. The adapter fails closed. Output release check. Telemetry
  content-capture settings.
- **Implementation route:** `screening/ingress.py` runs before the session
  append and before the Runner. `release_check.py` runs before the HTTP
  response.
- **Prerequisites:** G01.
- **Primary skill:** `protect-adk-sensitive-data`
- **Supporting skills:** `adk-agent-observability` (content-capture gates).
- **Acceptance:** seeded PAN, CVV and IBAN inputs are blocked or masked, and
  the captured model request and stored events are clean. A screening outage
  produces a refused turn with nothing stored. A seeded PAN in model output is
  replaced.
- **Verification:** offline. Live SDP and Model Armor checks wait for G09.
- **Execution scope:** local only.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G05 from docs/plans/card-dispute-agent.md. Read docs/architecture/card-dispute-agent.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G08: Budgets, turn lease, kill switch

- **Outcome and linked decisions:** work is bounded, and an operator can stop
  new sessions. Links: DD-06, DD-10, I8.
- **Scope:** `max_llm_calls`, turn, session and daily caps, a token
  reservation table, kill switch, and a per-session turn lease (409 on
  overlap).
- **Implementation route:** `guardrails/*` called at admission in `api/turns`.
  `RunConfig` is set in `agent/app.py`.
- **Prerequisites:** G01.
- **Primary skill:** `adk-operational-guardrails`
- **Supporting skills:** none.
- **Acceptance:** exhaustion of each cap returns the fallback message. The kill
  switch blocks new sessions while confirmations and the reconciler continue.
  Two concurrent turns produce one 409. Usage survives a restart.
- **Verification:** offline plus local Postgres.
- **Execution scope:** local only.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G08 from docs/plans/card-dispute-agent.md. Read docs/architecture/card-dispute-agent.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### Discovery goals

- **D-01**
  - Question: are `gemini-3.8-flash` (Vertex), SDP, Model Armor and Cloud SQL
    available in the chosen EU region? What are the quotas and dated prices?
    Is ADK 2.8.0 still the right pin given that 2.11.0 is current?
  - Investigation: official documentation lookup only, with no provisioning.
    Record URL, date and region for each fact. Stop when every row in design
    D-01 has a sourced answer or a confirmed gap.
  - Unblocks: G09 and the cost estimate.
- **D-02**
  - Question: does the core dispute API accept an idempotency key or client
    reference, and for how long? Can a case be looked up by that reference?
    What are its error taxonomy, rate limit and SLA, and is there a test
    environment?
  - Investigation: obtain the written contract and run one replay experiment
    in the test environment, with authorization. Stop when I3's mechanism is
    either supported or replaced by manual reconciliation.
  - Unblocks: G04 live.
- **D-03**
  - Question: what are the reason codes, windows, required facts and
    languages? What is the baseline follow-up rate?
  - Investigation: collect 60–100 anonymised labelled historical cases from
    disputes ops. Stop when the rule table v1 is signed off and the dev set is
    frozen with a hash.
  - Unblocks: G02 real rules and G03.

### Later goals (coarse; scope depends on open decisions)

- G03 eval baseline, primary `adk-agent-evaluation`, supported by
  `adk-agent-instructions`
- G06 threat model and adversarial suite, primary `adk-agent-security`
- G07 app contract, primary `adk-frontend-integration`, supported by
  `adk-tool-auth-and-secrets`
- G09 deploy, primary `deploy-adk-on-google-cloud`, supported by
  `adk-agent-observability` and `adk-release-engineering`
- G10 observability
- G11 release
- G12 pilot, primary `optimise-adk-on-google-cloud`, supported by
  `adk-agent-evaluation`
- G13 GA readiness, primary `adk-memory-architecture`, supported by
  `protect-adk-sensitive-data`

Each gets the full goal block when its blockers clear.

## What the reviewer reads

| Document | Establishes |
| --- | --- |
| docs/architecture/card-dispute-agent.md | Method, invariants and proposed decisions |
| docs/eval/summary.md (created in G03) | Latest result per eval case, linked to the raw runs |
| This plan | Remaining limits, deferred controls and goal evidence |

## Open decisions for further planning

See the design's *Open decisions* (D-01 to D-07). Blocking map:

| Decision | Blocks |
| --- | --- |
| D-01 | G09 |
| D-02 | G04 live |
| D-03 | G03 and the real G02 rules |
| D-04 | G07 |
| D-05 | G09 |
| D-06 | G13 |
| D-07 | G12 |

## Resume here

- **Next goal:** G01, *Customer finds their own transaction through the
  agent*. It is ready because it has no prerequisites, runs fully offline
  with fakes, and establishes the identity-scoping invariant every later goal
  relies on.
- **Read first:** the design, then this plan.
- **Next action:** confirm the ADK pin, then write the fake core client and
  the cross-customer denial test before the agent.
- **Continuation prompt:**

```text
/adk-engineer Carry out G01 (Customer finds their own transaction through the agent) from docs/plans/card-dispute-agent.md.
Read docs/architecture/card-dispute-agent.md and preserve its accepted decisions.
Use adk-workflow-design with adk-tool-auth-and-secrets, adk-tool-interface-design and adk-agent-instructions.
Work within local code and offline tests only, verify the cross-customer denial, masked bounded results and session-restart cases, and update
the plan with actual evidence and remaining blockers.
```

After that goal, the same request without a goal ID continues with the next
ready one: `/adk-engineer Continue the next ready goal in docs/plans/card-dispute-agent.md.`
