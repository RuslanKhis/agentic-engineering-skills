# Implementation plan: Card dispute assistant

Status: draft. Ready goals are identified. Every decision is provisional on
the assumed answers.
Architecture: [docs/architecture/card-dispute-agent.md](../architecture/card-dispute-agent.md)
Continuation source of truth: this plan

## Destination and constraints

At GA (about 2027-02-08), authenticated retail customers in the bank's app can
dispute a merchant card transaction through a conversation. The result is
exactly one correctly classified case in core banking, created only after they
confirm a code-rendered summary. Unauthorised claims are routed to the
existing fraud journey. Non-goals are listed in the design. Accepted stack
(proposed): Python, `google-adk==2.8.0` (working pin, confirm in G01), FastAPI
on Cloud Run in an EU region, Cloud SQL Postgres, Vertex AI `gemini-3.8-flash`
(agent and judge, pinned), Sensitive Data Protection.

**Current authorisation:** design only. No goal is yet authorised for cloud
resources, IAM, live model calls or core-banking sandbox access. Each goal's
execution scope names what it needs.

**Inspected:** the repository has no application code. **Proposed layout**
(greenfield, unverified):

```text
dispute_assistant/
  api/            FastAPI app: auth middleware, admission, SDP ingress, output checks, submit, status
  agent/          App/Runner factory, LlmAgent, prompts/ (versioned), callbacks
  tools/          transactions.py, drafts.py, status.py, handoff.py (trusted context only)
  policy/         dispute_policy: categories, eligibility, reason-code map, approved texts
  operations/     dispute_operation store, core client, reconciler job
  integrations/   core_banking client (mTLS), live_chat client, sdp client
tests/            offline (scripted model, fakes), integration (postgres), eval/
release/          manifest, eval gate config
```

## Delivery profile and capacity

Profile: **production service** (see the design, "Delivery constraints").

| Phase | Delivers | Goals | Estimate (focused hours) | Capacity and reserve |
| --- | --- | --- | --- | --- |
| 1, ship (to GA) | Merchant disputes end to end for real customers in staged rollout, with SLOs, release gates and recovery tested | G00 to G13 | 1,440 to 2,180 | 6 × 16 wk × 40 h × 0.65 ≈ 2,500 h; 20% reserve leaves ≈ 2,000 h |
| 2, harden and extend (GA + 3 months) | Evidence reading, second language, Model Armor, fraud path, production-fed evals, tuning | G14 to G20 | 700 to 1,120 | Same team after GA |

**Fit:** phase 1 fits at the low and middle of the range. It does not fit at
the high end (2,180 > 2,000). If the burn-down at week 8 projects above
2,000 h, apply these **contingency cuts** in order:

1. C1: G05 ships the reconciler as a Dispute Ops manual queue with a runbook
   instead of an automated lookup job (saves about 60 h). The `uncertain`
   state and the no-duplicate guarantee stay.
2. C2: G12 replaces automated canary analysis with manual staged traffic
   steps and written thresholds (saves about 50 h).
3. C3: G03 drops `get_dispute_status`; status stays in the app's existing case
   list (saves about 40 h).
4. C4: GA is limited to a 25% cohort, which shrinks the G13 load test to 1×
   peak plus a smaller margin (saves about 40 h).

Beyond C1 to C4 (about 190 h), the GA date or the cohort must move. That is
the user's decision, not a floor cut. **Please confirm or move this cut
line.**

**If time runs out early,** the order that keeps each step useful is G00,
G01, G02, G03, G04, G05 (a working, safe end-to-end flow in staging). Then
G07 and G08 (data and security gates), G10, then G11, G12 and G13.

**Parallel streams** for the six engineers (suggested):

- A: G01, G04, G10 (agent and quality)
- B: G02, G03, G06 (identity, tools, API)
- C: G00, G05 (writes)
- D: G07, G08 (data and security, with the security reviewer)
- E: G11, G12 (platform and release)
- F: G09, G13 (guardrails and readiness)

**Regulatory milestones** (calendar, not engineering hours; owners assumed):

| Milestone | Target | Owner | Gates |
| --- | --- | --- | --- |
| DPIA approved | 2026-12-04 | DPO | Any real customer data (G13 pilot) |
| Threat model reviewed | 2026-11-20 | Security reviewer | G05, G08 |
| AI Act transparency and model-risk sign-off | 2027-01-08 | Compliance, Model Risk | Customer cohort |
| Penetration test complete and criticals fixed | 2027-01-22 | Security | GA |
| DORA register / outsourcing note updated | 2027-01-22 | Third-party risk | GA |

## Implementation map

| Decision / requirement | ADK or application component and integration point | GCP service/responsibility | Primary skill | Verification still needed |
| --- | --- | --- | --- | --- |
| D1 single agent | `LlmAgent` in an `App`, run by the app-owned `Runner` from `api/` | Vertex AI regional endpoint | `adk-workflow-design` | Constructor names at pin (G01) |
| I1, I2 identity | FastAPI middleware verifies the gateway JWT and sets `customer_id`. Runner `user_id = customer_id`. Tools read it from trusted context | Workload identity; Secret Manager for the mTLS cert | `adk-tool-auth-and-secrets` | Gateway JWT format and JWKS (G02) |
| D8 sessions | `DatabaseSessionService` and a per-session advisory lock | Cloud SQL Postgres (EU, CMEK) | `adk-memory-architecture` | V4 |
| Tool contracts | `FunctionTool`s in `tools/` with a `before_tool_callback` ownership check | — | `adk-tool-interface-design` | Declaration dump |
| D3, D5 policy | `policy/` module; the summary renderer; the authorisation question | — | `adk-agent-instructions` (code vs prompt split) | Dispute Ops sign-off on tables |
| D2, D4 submit | `POST /disputes/{id}/submit`, `dispute_operation` table, core client, reconciler | Cloud Run job + Cloud Scheduler | `safe-api-tool-calls` | V5 (G00) |
| I7 data | SDP inspect/de-identify before the Runner; typed projections; output checker | Sensitive Data Protection (EU) | `protect-adk-sensitive-data` | V6 |
| I9 budgets | `RunConfig.max_llm_calls`, allowance table, semaphore, kill switch | Cloud SQL | `adk-operational-guardrails` | `RunConfig` at pin |
| D11 API | Complete-reply JSON contract for the app team | — | `adk-frontend-integration` | App team review |
| D7 hosting | Container, Cloud Run service and job, VPC egress | Cloud Run, VPC-SC, Interconnect | `deploy-adk-on-google-cloud` | V3 |
| SLOs | OTel to Cloud Trace/Monitoring, content capture off | Cloud Monitoring/Logging | `adk-agent-observability` | Env gates at pin |
| D12 release | Manifest, CI eval gate, traffic split | CI runner, Cloud Run revisions | `adk-release-engineering` | — |

## Goals and dependencies

| ID and goal | Phase | Type | Estimate (h) | Depends on | Primary skill | State / blocker |
| --- | --- | --- | --- | --- | --- | --- |
| G00 Core dispute API contract | 1 | discovery | 40–80 | — | `safe-api-tool-calls` | ready (needs integration team and sandbox access) |
| G01 Pinned skeleton with scripted-model tests | 1 | implementation | 50–90 | — | `adk-workflow-design` | **ready** |
| G02 Verified customer identity and session ownership | 1 | implementation | 100–160 | G01 | `adk-tool-auth-and-secrets` | ready after G01 |
| G03 Owner-scoped transaction read tools | 1 | implementation | 100–150 | G02 | `adk-tool-interface-design` | ready after G02 (fake core) |
| G04 Dispute conversation and draft | 1 | implementation | 140–200 | G03 | `adk-agent-instructions` | ready after G03; live part blocked by V1 |
| G05 Confirmed, idempotent case creation | 1 | implementation | 180–260 | G00, G04 | `safe-api-tool-calls` | blocked by G00 |
| G06 App API contract | 1 | implementation | 70–110 | G04 | `adk-frontend-integration` | ready after G04 |
| G07 Sensitive-data boundaries | 1 | implementation | 110–160 | G02 | `protect-adk-sensitive-data` | ready after G02; live part blocked by V6 |
| G08 Threat model and adversarial suite | 1 | implementation | 90–140 | G04 | `adk-agent-security` | ready after G04 |
| G09 Budgets, kill switch and handoff | 1 | implementation | 90–140 | G02 | `adk-operational-guardrails` | ready after G02 |
| G10 Evaluation set and CI gate | 1 | implementation | 110–160 | G04 | `adk-agent-evaluation` | ready after G04 |
| G11 EU deployment | 1 | implementation | 130–190 | G01 | `deploy-adk-on-google-cloud` | blocked by V3 and authorisation |
| G12 Observability and release lifecycle | 1 | implementation | 130–190 | G11 | `adk-agent-observability` | blocked by G11 |
| G13 Pilot and GA readiness | 1 | implementation | 100–150 | all of G00–G12 | `adk-release-engineering` | blocked |
| G14 Evidence reading with a quarantined reader | 2 | implementation | 140–220 | G13 | `adk-agent-security` | proposed |
| G15 Second language | 2 | implementation | 100–160 | G13 | `adk-agent-evaluation` | proposed |
| G16 Model Armor screening layer | 2 | implementation | 60–100 | G13 | `protect-adk-sensitive-data` | proposed |
| G17 Proactive case-status notifications | 2 | implementation | 80–140 | G13 | `safe-api-tool-calls` | proposed |
| G18 Production samples to eval refresh | 2 | implementation | 80–120 | G13 | `adk-agent-observability` | proposed |
| G19 Unauthorised-claim path with fraud API | 2 | implementation | 160–260 | G13, fraud contract | `safe-api-tool-calls` | proposed |
| G20 Measured latency and cost tuning | 2 | implementation | 80–120 | G13 traffic | `optimise-adk-on-google-cloud` | proposed |

Phase 1 total: 1,440 to 2,180 h. Phase 2 total: 700 to 1,120 h.

### G00: Core dispute API contract (discovery)

- **Phase and estimate:** 1; 40–80 h.
- **Outcome and linked decisions:** settles V5 for D4 and I4/I5. The deciding
  questions: does create-case accept an idempotency key (with what scope and
  retention)? Can a case be found by transaction ID? Is customer scope
  enforced server-side? What are the error and timeout semantics? Is there a
  sandbox with fault injection?
- **Scope:** read the API spec and interview the integration team. Run a
  bounded sandbox probe (≤ 50 calls) only if authorised. Excludes building the
  client.
- **Depth:** discovery only; the result is a decision record.
- **Implementation route:** `docs/architecture/decisions/core-dispute-api.md`
  (proposed), recording the chosen replay strategy: key-based, or
  lookup-before-retry with manual reconciliation as last resort.
- **Prerequisites:** a named integration-team contact, spec access.
- **Primary skill:** `safe-api-tool-calls`
- **Supporting skills:** none.
- **Acceptance:** each deciding question answered with a cited source (spec
  section, ticket or sandbox log), or marked unknown with the fallback chosen.
- **Verification:** a document review by the security reviewer and the G05
  owner.
- **Execution scope:** document work is authorised. Sandbox calls need
  explicit approval and credentials from the integration team.
- **Stopping condition:** two weeks elapsed. Then choose lookup-before-retry
  plus the manual queue and proceed.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G00 from docs/plans/card-dispute-agent.md. Read docs/architecture/card-dispute-agent.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G01: Pinned skeleton with scripted-model tests

- **Phase and estimate:** 1; 50–90 h (includes first-ADK setup for the team).
- **Outcome and linked decisions:** D1, D6, D12. A runnable FastAPI service
  owns an ADK `App`/`Runner` with one `LlmAgent` and no real tools yet. A
  scripted fake model drives an offline test, and CI runs it.
- **Scope:** project layout as proposed above; dependency pins and lockfile;
  a `release/manifest` stub with the model ID `gemini-3.8-flash` and the
  prompt version. Excludes auth, tools and the cloud.
- **Depth:** production layout kept; no throwaway code.
- **Implementation route:** `agent/factory.py` builds the `App`.
  `api/main.py` holds a module-level Runner with `InMemorySessionService` for
  tests only. A fake `BaseLlm` lives in `tests/`. **Confirm `google-adk==2.8.0`
  (or the chosen newer pin ≥ 2.7.0) against its source and docs for `App`,
  `Runner`, `RunConfig.max_llm_calls`, `DatabaseSessionService` and callback
  signatures. Record the result.**
- **Prerequisites:** a repository and a CI runner; Python version chosen.
- **Primary skill:** `adk-workflow-design`
- **Supporting skills:** `adk-release-engineering` (pins and manifest
  format), `adk-agent-evaluation` (scripted-model test pattern).
- **Acceptance:** `pytest` runs offline with no network and passes. A scripted
  model's reply is returned by the API. The manifest contains no model alias.
  The ADK pin confirmation is recorded.
- **Verification:** offline `pytest tests/offline`.
- **Execution scope:** local files and package install in the dev environment
  (to be authorised by the user at execution time). No cloud.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G01 from docs/plans/card-dispute-agent.md. Read docs/architecture/card-dispute-agent.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G02: Verified customer identity and session ownership

- **Phase and estimate:** 1; 100–160 h.
- **Outcome and linked decisions:** I1, I2, D8. Every request carries a
  verified `customer_id`, and sessions are readable only by their owner.
- **Scope:** JWT verification middleware (JWKS from the gateway);
  `DatabaseSessionService` on local Postgres; owner-keyed session lookup; a
  per-session advisory lock (409 on overlap). Excludes tools.
- **Depth:** build, with cross-customer denial tests.
- **Implementation route:** `api/auth.py` and `api/sessions.py`. The Runner
  call uses `user_id=customer_id`. A `trusted_context` object travels in state
  under a code-owned key that the model cannot write.
- **Prerequisites:** G01; the gateway token format (assume a signed JWT with
  `sub` mapped to `customer_id`).
- **Primary skill:** `adk-tool-auth-and-secrets`
- **Supporting skills:** `adk-memory-architecture` (session backend,
  retention job).
- **Acceptance:** a valid token proceeds. An expired or forged token gets 401.
  User B with user A's session ID gets 404. Two concurrent posts give one run
  and one 409. A Postgres-backed session survives a process restart.
- **Verification:** offline plus local integration (docker Postgres).
- **Execution scope:** local only.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G02 from docs/plans/card-dispute-agent.md. Read docs/architecture/card-dispute-agent.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G03: Owner-scoped transaction read tools

- **Phase and estimate:** 1; 100–150 h.
- **Outcome and linked decisions:** I1. The agent can list and fetch the
  customer's own card transactions and dispute status.
- **Scope:** `list_card_transactions`, `get_transaction` and
  `get_dispute_status` against a fake core client, plus the real mTLS client
  interface. Includes the `before_tool_callback` ownership check on
  `transaction_id`. Excludes drafts.
- **Depth:** build. Results are bounded to ≤ 20 rows and show only masked PAN.
- **Implementation route:** `tools/transactions.py` and `tools/status.py`
  call `integrations/core_banking.py`. No tool parameter is an identity.
- **Prerequisites:** G02.
- **Primary skill:** `adk-tool-interface-design`
- **Supporting skills:** `adk-tool-auth-and-secrets` (trusted scope into
  tools), `safe-api-tool-calls` (read timeouts and retry).
- **Acceptance:** a scripted model asking for a foreign transaction ID gets
  `not_found` and no foreign core read happens. A result over 20 rows is
  truncated with `truncated: true`. A core timeout gives an actionable error.
  The declaration dump is recorded.
- **Verification:** offline.
- **Execution scope:** local only.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G03 from docs/plans/card-dispute-agent.md. Read docs/architecture/card-dispute-agent.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G04: Dispute conversation and draft

- **Phase and estimate:** 1; 140–200 h.
- **Outcome and linked decisions:** D3, D5, D6, I6. The agent gathers facts
  for the five merchant categories and saves a validated draft. Code renders
  the summary and asks the authorisation question.
- **Scope:** the `policy/` module (categories, eligibility rules, reason-code
  map, approved texts); `save_dispute_draft` and `request_handoff`; versioned
  instruction files; a rendered-request test; the deterministic output checker
  for refund-promise patterns. Excludes submission.
- **Depth:** build. Repair budget 2, then handoff.
- **Implementation route:** `agent/prompts/v1.md`, `tools/drafts.py` and
  `policy/`. Model `gemini-3.8-flash`; record the thinking and sampling
  settings.
- **Prerequisites:** G03. Dispute Ops provides the category and question
  tables. Live model checks need V1 and an authorised non-production project.
- **Primary skill:** `adk-agent-instructions`
- **Supporting skills:** `adk-tool-interface-design` (draft tool schema),
  `adk-model-and-output-contracts` (model pin, invalid-argument handling).
- **Acceptance:** the scripted model's invalid category, overlong narrative
  and prose-instead-of-call each get the designed response. Eligibility tables
  pass unit tests. The captured request shows no identity or policy text in
  the prompt. A "No" to the authorisation question routes to fraud (I8).
- **Verification:** offline; a bounded live smoke test of ≤ 20 calls once
  authorised.
- **Execution scope:** local; the live smoke test needs project and budget
  authorisation.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G04 from docs/plans/card-dispute-agent.md. Read docs/architecture/card-dispute-agent.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G05: Confirmed, idempotent case creation

- **Phase and estimate:** 1; 180–260 h (C1 cuts about 60 h).
- **Outcome and linked decisions:** D2, D4, I3, I4, I5. Submit creates at
  most one case. An uncertain result is shown honestly and reconciled.
- **Scope:** the submit and status endpoints; the `dispute_operation` table
  and state machine; eligibility re-checked at submit; the core create client
  using the G00 strategy; the reconciler Cloud Run job; the manual-queue
  export.
- **Depth:** build: full replay and reconciliation.
- **Implementation route:** `operations/` and `api/submit.py`. A unique
  constraint on `operation_id` and on (customer, transaction, open). A stale
  `draft_version_hash` returns 409.
- **Prerequisites:** G00 decision, G04.
- **Primary skill:** `safe-api-tool-calls`
- **Supporting skills:** `adk-operational-guardrails` (approval binding).
- **Acceptance:** with a fake core, these cases pass: commit-then-timeout
  gives `uncertain`, then the reconciler finds the case and sets `submitted`
  with no second create. A double submit makes one core call. A restart
  mid-call leads to the same outcome. A stale hash makes no core call. The
  agent tool set contains no core write.
- **Verification:** offline with fault injection; local integration with
  Postgres.
- **Execution scope:** local; the sandbox needs G00's approval.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G05 from docs/plans/card-dispute-agent.md. Read docs/architecture/card-dispute-agent.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G06: App API contract

- **Phase and estimate:** 1; 70–110 h.
- **Outcome and linked decisions:** D11, I10. The app team can build the
  screens against a stable, versioned JSON contract.
- **Scope:** OpenAPI for message, history, draft summary, submit, status and
  handoff. Every reply carries `handoff_available`. Includes error shapes and
  a mock server for the app team. Excludes the screens themselves.
- **Depth:** build: complete-reply JSON, no streaming.
- **Implementation route:** `api/schemas.py`, published OpenAPI, contract
  tests.
- **Prerequisites:** G04.
- **Primary skill:** `adk-frontend-integration`
- **Supporting skills:** none.
- **Acceptance:** contract tests pass. Raw ADK events are never forwarded. A
  late execution error does not show as success.
- **Verification:** offline contract tests; review by the app team.
- **Execution scope:** local.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G06 from docs/plans/card-dispute-agent.md. Read docs/architecture/card-dispute-agent.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G07: Sensitive-data boundaries

- **Phase and estimate:** 1; 110–160 h.
- **Outcome and linked decisions:** I7, A12. PAN, CVV and IBAN never reach the
  model, sessions or logs. SDP failure fails closed.
- **Scope:** SDP inspect and de-identify before the Runner; typed tool
  projections; telemetry content gates off; session and draft retention jobs;
  a data-flow table for the DPIA.
- **Depth:** build. Model Armor is deferred to G16.
- **Implementation route:** `integrations/sdp.py` and `api/ingress.py`;
  scheduled deletion.
- **Prerequisites:** G02. Live use needs V6.
- **Primary skill:** `protect-adk-sensitive-data`
- **Supporting skills:** `adk-agent-observability` (content-capture gates).
- **Acceptance:** with a fake SDP, a test PAN is stored as `[CARD_NUMBER]`.
  With SDP down, nothing is persisted and the fallback reply is sent. A log
  scan of a test run finds no synthetic PAN.
- **Verification:** offline; a bounded live SDP check with synthetic data
  once authorised.
- **Execution scope:** local; live SDP needs project authorisation.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G07 from docs/plans/card-dispute-agent.md. Read docs/architecture/card-dispute-agent.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G08: Threat model and adversarial suite

- **Phase and estimate:** 1; 90–140 h, plus security reviewer time.
- **Outcome and linked decisions:** the design's security posture table. The
  forbidden actions are proven absent.
- **Scope:** the threat model with OWASP LLM/Agentic IDs; the trifecta check;
  a review of the `before_tool_callback` capability check; adversarial cases
  (injected merchant descriptor, foreign transaction, prompt extraction,
  refund promise, a fake submit tool call) with deterministic assertions.
- **Depth:** build.
- **Implementation route:** `tests/adversarial/` with a scripted model, plus
  live cases in the G10 gate.
- **Prerequisites:** G04.
- **Primary skill:** `adk-agent-security`
- **Supporting skills:** `adk-agent-evaluation` (live adversarial set).
- **Acceptance:** every case asserts no foreign read, no submit and no
  promise text. The security reviewer signs off on the threat model.
- **Verification:** offline; live cases run inside G10.
- **Execution scope:** local.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G08 from docs/plans/card-dispute-agent.md. Read docs/architecture/card-dispute-agent.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G09: Budgets, kill switch and handoff

- **Phase and estimate:** 1; 90–140 h.
- **Outcome and linked decisions:** D9, D10, I9. Work is bounded, and
  operators can stop the agent without a deploy.
- **Scope:** `max_llm_calls=8`; a per-customer daily allowance with an atomic
  increment; an instance semaphore; a kill-switch flag; a live-chat transfer
  with a code-built summary; the fallback-to-form responses.
- **Depth:** build.
- **Implementation route:** `api/admission.py`, `tools/handoff.py`,
  `integrations/live_chat.py`.
- **Prerequisites:** G02. Live-chat API contract (assumed A9).
- **Primary skill:** `adk-operational-guardrails`
- **Supporting skills:** `safe-api-tool-calls` (live-chat transfer call).
- **Acceptance:** a looping scripted model stops at 8 calls. The 41st turn of
  the day is refused. Flipping the kill switch sends the next request to the
  form. The handoff payload contains no transcript content beyond the
  structured fields.
- **Verification:** offline.
- **Execution scope:** local.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G09 from docs/plans/card-dispute-agent.md. Read docs/architecture/card-dispute-agent.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G10: Evaluation set and CI gate

- **Phase and estimate:** 1; 110–160 h.
- **Outcome and linked decisions:** D6, D12. About 150 labelled synthetic
  conversations in the GA language cover the categories, ambiguous
  transactions, fraud signals and adversarial prompts. A pinned judge scores
  the rubric metrics only.
- **Scope:** case authoring with Dispute Ops; metrics (transaction selection,
  category accuracy, required-fact completeness, handoff when due, no promise
  text); thresholds from a measured baseline; a CI gate that fails by exit
  code; a cost ceiling.
- **Depth:** build: gated evaluation.
- **Implementation route:** `tests/eval/` and `release/eval-gate`.
- **Prerequisites:** G04; an authorised non-production Vertex project and
  budget.
- **Primary skill:** `adk-agent-evaluation`
- **Supporting skills:** `adk-release-engineering` (gate policy).
- **Acceptance:** the baseline run is recorded with the model, judge and
  prompt IDs. The gate fails on a seeded regression. A run that did not happen
  is reported as missing evidence.
- **Verification:** authorised live run, bounded to 150 × 3 repeats.
- **Execution scope:** needs project, model and budget authorisation.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G10 from docs/plans/card-dispute-agent.md. Read docs/architecture/card-dispute-agent.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G11: EU deployment

- **Phase and estimate:** 1; 130–190 h.
- **Outcome and linked decisions:** D7. Staging and production run in the EU
  region inside VPC-SC with CMEK and private egress to the integration
  gateway.
- **Scope:** container; Cloud Run service and reconciler job; Cloud SQL;
  service accounts per workload; Secret Manager; a deploy readback; Cloud SQL
  backup, restore and DR rehearsal; owned-resource cleanup for ephemeral
  environments.
- **Depth:** build, with recovery and cleanup.
- **Implementation route:** the bank's IaC convention (assumed Terraform)
  plus the deploy pipeline.
- **Prerequisites:** G01; V3; platform team approval; IAM change requests.
- **Primary skill:** `deploy-adk-on-google-cloud`
- **Supporting skills:** `adk-tool-auth-and-secrets` (workload identities,
  mTLS secret).
- **Acceptance:** the readback shows the revision, region, service account
  and egress path. A staging request reaches the sandbox core. A DR restore
  drill is recorded.
- **Verification:** authorised staging deployment.
- **Execution scope:** **not authorised yet**. Needs the target project, IAM
  and deployment approval.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G11 from docs/plans/card-dispute-agent.md. Read docs/architecture/card-dispute-agent.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G12: Observability and release lifecycle

- **Phase and estimate:** 1; 130–190 h (C2 cuts about 50 h).
- **Outcome and linked decisions:** D12 and the design's SLIs. Alerts lead to
  a session, and a release is one unit that rolls back together.
- **Scope:** OTel export with content off; SLIs, SLOs and burn-rate alerts;
  the runbook; the release manifest; the CI promotion gate; staged traffic
  steps with thresholds; a rollback rehearsal; a model-retirement calendar
  entry.
- **Depth:** build.
- **Implementation route:** `release/`, CI config, Monitoring dashboards and
  alert policies.
- **Prerequisites:** G11, G10.
- **Primary skill:** `adk-agent-observability`
- **Supporting skills:** `adk-release-engineering` (manifest, canary,
  rollback).
- **Acceptance:** an in-memory exporter test shows one span per agent, tool
  and model call carrying the session ID. A rollback rehearsal restores the
  previous bundle. The manifest has no alias.
- **Verification:** offline exporter test; staging rehearsal.
- **Execution scope:** staging needs G11 authorisation.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G12 from docs/plans/card-dispute-agent.md. Read docs/architecture/card-dispute-agent.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### G13: Pilot and GA readiness

- **Phase and estimate:** 1; 100–150 h (C4 cuts about 40 h).
- **Outcome and linked decisions:** T1, the M1/M2 baselines and the
  regulatory milestones. Staff pilot, then the 1%, 10% and 100% cohorts,
  each with go/no-go evidence.
- **Scope:** a load test at 2× peak; a kill-switch drill; penetration-test
  remediation; the dated cost table; the pilot metrics report; GA go/no-go.
- **Depth:** build.
- **Implementation route:** load scripts; the cohort flag in the app;
  reports.
- **Prerequisites:** G00 to G12; DPIA and compliance sign-offs.
- **Primary skill:** `adk-release-engineering`
- **Supporting skills:** `optimise-adk-on-google-cloud` (load test
  measurement), `adk-agent-observability` (pilot dashboards).
- **Acceptance:** p95 and availability are measured against T1. Zero
  duplicate cases and zero uncertain operations older than 30 min in the
  pilot. Sign-offs are recorded.
- **Verification:** production pilot under approved change control.
- **Execution scope:** needs production change approval.
- **Status and evidence:** planned.
- **Run this goal:** `/adk-engineer Carry out G13 from docs/plans/card-dispute-agent.md. Read docs/architecture/card-dispute-agent.md, use the goal's primary and supporting skills, verify its acceptance cases locally and record evidence here.`

### Phase 2 goals (coarser; refine after the GA results)

- **G14 Evidence reading, quarantined reader** (140–220 h; `adk-agent-security`;
  supporting `protect-adk-sensitive-data`, `adk-workflow-design`). A reader
  agent with no tools turns uploads into validated structured facts.
  Acceptance: an injected receipt changes no draft field outside its schema
  and triggers no tool call.
- **G15 Second language** (100–160 h; `adk-agent-evaluation`; supporting
  `adk-agent-instructions`). Acceptance: the eval set in the new language meets
  the GA thresholds.
- **G16 Model Armor layer** (60–100 h; `protect-adk-sensitive-data`).
  Acceptance: the adversarial suite still passes; added latency is measured;
  fail-closed behaviour is defined.
- **G17 Case-status notifications** (80–140 h; `safe-api-tool-calls`).
  Acceptance: an uncertain-to-submitted transition notifies once.
- **G18 Production samples to eval** (80–120 h; `adk-agent-observability`;
  supporting `adk-release-engineering`). Acceptance: a redacted sampled
  session becomes a gate case.
- **G19 Unauthorised-claim path** (160–260 h; `safe-api-tool-calls`;
  supporting `adk-agent-security`). Acceptance: a fraud claim creates one
  fraud case via the fraud API and offers a card block through the existing
  control, within PSD2 handling agreed with Fraud.
- **G20 Measured tuning** (80–120 h; `optimise-adk-on-google-cloud`).
  Acceptance: p95 or cost per submitted dispute improves with quality
  unchanged on the gate.

## Later

| Item | Trigger that brings it forward | Risk accepted while it waits | Likely primary skill |
| --- | --- | --- | --- |
| Model migration off `gemini-3.8-flash` | Vertex retirement date announced | None while the calendar is watched | `adk-release-engineering` |
| Policy Q&A with governed RAG | Customers ask policy questions that the templates do not cover | Those questions get a handoff | `adk-memory-architecture` |
| Voice channel | Contact-centre strategy | — | `adk-frontend-integration` |
| A2A link to a contact-centre agent | The contact-centre platform exposes an agent | Transfer via the API only | `adk-agent-interoperability` |
| Multi-region active-active | Availability target above 99.5% | Regional outage sends customers to the form | `deploy-adk-on-google-cloud` |
| Cross-session memory | Repeat-dispute research shows value; consent design | Customers repeat context | `adk-memory-architecture` |

## What the reviewer reads

| Document | Establishes |
| --- | --- |
| docs/architecture/card-dispute-agent.md | Method, assumed answers, decisions, invariants |
| tests/eval report (from G10, later) | Latest quality result per case |
| This plan | Remaining limits, deferred controls, status |

## Open decisions for further planning

See the design's "Open decisions". The ones that block goals are the core API
contract (G05), V1 and V3 (live checks, G11), the cut line (phase 1), and the
AI Act classification (GA date).

## Resume here

- **Next goal:** G01, the pinned skeleton with scripted-model tests. It has no
  blocking dependency. G00 can run in parallel with the integration team.
- **Read first:** docs/architecture/card-dispute-agent.md, then this plan.
- **Next action:** confirm the ADK pin against its source, create the
  proposed layout, and write the scripted-model offline test.
- **Continuation prompt:**

```text
/adk-engineer Carry out G01 (Pinned skeleton with scripted-model tests) from docs/plans/card-dispute-agent.md.
Read docs/architecture/card-dispute-agent.md and preserve its accepted decisions.
Use adk-workflow-design with adk-release-engineering and adk-agent-evaluation.
Work within local files only, verify the offline scripted-model test and the recorded ADK pin confirmation, and update
the plan with actual evidence and remaining blockers.
```

After that goal, the same request without a goal ID continues with the next
ready one: `/adk-engineer Continue the next ready goal in docs/plans/card-dispute-agent.md.`
