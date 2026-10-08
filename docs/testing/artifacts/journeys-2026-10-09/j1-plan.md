# Implementation plan: customer-support agent

Status: **draft / ready goals identified**
Architecture: [`../architecture/customer-support-agent.md`](../architecture/customer-support-agent.md)
Continuation source of truth: this plan (no tracker adopted yet)

## Destination and constraints

End result of the two-week slice: a Freshdesk ticket in the pilot categories receives, within minutes, a KB-cited draft in the customer's language plus a validated refund proposal that a support agent can approve with one click; the refund is executed exactly once by the actions service; billing questions carry the billing agent's answer as quoted data; the whole thing ships through a release gate that can fail. Non-goals and deferred controls: design §2. Accepted stack: Python ADK (pin to be chosen in G00; the installed skill collection was read against `google-adk` 2.8.0, upstream 2.11.0 as of 2026-10-08), Cloud Run, Cloud SQL PostgreSQL (existing), Pub/Sub, Vertex AI (`europe-west1`), Secret Manager, Freshdesk, Orders API, billing A2A agent.

Authorization today: local design and local code only. No deployment, IAM, paid model call or Freshdesk sandbox call is authorised until requested per goal. Pinned versions the goals inherit: reader/drafter model, judge model and prompt versions are set in G00/G06 and recorded in `release/manifest.yaml`; changing one is a release.

Inspected repository paths: none (greenfield). Proposed layout (label: proposed):

```
support_agent/
  app.py                 # ADK App: root = SupportCaseWorkflow
  workflow.py            # SupportCaseWorkflow(BaseAgent): reader -> policy -> [billing] -> drafter
  agents/reader.py       # LlmAgent, read tools, output_schema=CaseAssessment
  agents/drafter.py      # LlmAgent, no tools, output_schema=DraftReply
  agents/billing_peer.py # RemoteA2aAgent factory, timeout, task-state mapping
  tools/kb.py            # search_kb
  tools/orders_read.py   # get_order_summary (owner-match computed here)
  tools/thread.py        # get_ticket_thread
  policy/refund.py       # deterministic eligibility + tier
  schemas.py             # CaseAssessment, DraftReply, refusal shapes
  prompts/               # versioned instruction files + rendered-request tests
  admission.py           # budget counters, kill switch
  telemetry.py           # single OTel owner per process
support_ingress/         # webhook verify, dedup, publish
support_actions/         # proposals, approvals (OIDC), ledger, reconciler
kb_ingest/               # tag -> chunks -> embeddings -> kb_chunks(release)
release/manifest.yaml    # release unit
evals/                   # dev set, adversarial set, judge config
tests/                   # offline deterministic suite
```

## Implementation map

| Decision / requirement | ADK or application component and integration point | GCP service/responsibility | Primary skill | Verification still needed |
| --- | --- | --- | --- | --- |
| D1 reader/drafter split, code orchestration | `SupportCaseWorkflow(BaseAgent)` yields from reader `LlmAgent`, runs `policy/refund.py`, optionally the billing peer, then drafter `LlmAgent`; invoked through `App`/`Runner` from the Pub/Sub handler | Cloud Run `support-agent` | `adk-workflow-design` | `BaseAgent` custom orchestration API in the pinned ADK version |
| Reader/drafter instructions | `prompts/*.md` loaded at startup, state templating for language and KB release; sub-agent descriptions unused (code routes) | — | `adk-agent-instructions` | — |
| Reader tool declarations | 3 `FunctionTool`s in `tools/`, bounded dict results with `status` | — | `adk-tool-interface-design` | — |
| Output schemas, model pin | `output_schema` on both agents; `schemas.py`; repair-once in `workflow.py`; pinned Vertex model IDs | Vertex AI regional endpoint | `adk-model-and-output-contracts` | Exact IDs, lifecycle dates, schema enforcement on Vertex backend |
| D3 billing A2A | `RemoteA2aAgent` in `agents/billing_peer.py`, timeout, task-state → draft text mapping; peer output as data | Service-account ID token to billing service | `adk-agent-interoperability` | Card protocol version vs installed `a2a-sdk`; auth scheme |
| D4 KB retrieval | `kb_ingest/` job + `search_kb` over pgvector filtered by published release | Cloud SQL pgvector; Vertex embeddings | `adk-memory-architecture` | Embedding model id; recall@5 measurement |
| D5 sessions | `DatabaseSessionService` on Cloud SQL, session id = ticket | Cloud SQL | `adk-memory-architecture` | Driver/async compatibility; migration on ADK upgrade |
| D2 refund ledger and approval | `support_actions/`: proposals API, approve endpoint verifying Workspace OIDC + group, ledger state machine, Orders API client with idempotency key, reconciler | Cloud Run `support-actions` with the only Orders write role; Secret Manager | `safe-api-tool-calls` (ledger, replay) + `adk-tool-auth-and-secrets` (identity) | Freshdesk approve action carrying identity; Orders API replay semantics |
| I6 budgets | `admission.py` counters + `RunConfig(max_llm_calls=6)` + kill switch | Cloud SQL rows; Cloud Billing alerts (observation only) | `adk-operational-guardrails` | — |
| Security posture | Trifecta table enforced structurally; adversarial suite in `tests/adversarial/` | IAM per SA | `adk-agent-security` | IAM readback at deploy |
| D8 ingress | `support_ingress/` webhook verify + dedup + publish; push subscription to agent | Pub/Sub, DLQ | ordinary code (no ADK) | Freshdesk webhook signing |
| D9 deploy | Three Cloud Run services, SAs, regions, revision labels | Cloud Run | `deploy-adk-on-google-cloud` | — |
| D10 observability | `telemetry.py` single provider, content capture off; SLIs | Cloud Trace/Logging/Monitoring | `adk-agent-observability` | — |
| D7 release gate | `release/manifest.yaml`, CI gate job, canary, rollback | CI runner; Cloud Run traffic split | `adk-release-engineering` + `adk-agent-evaluation` | Judge ID |

## Goals and dependencies

| ID and goal | Type | Depends on | Primary skill | State / blocker |
| --- | --- | --- | --- | --- |
| G00 Verify the deciding provider facts | discovery | — | `adk-system-designer` (this) / `research` | ready; needs network access |
| G01 Reader + policy gate produce a validated assessment offline | implementation | — | `adk-workflow-design` | ready |
| G02 KB ingestion and retrieval measured on labelled cases | implementation | — | `adk-memory-architecture` | ready (fixture repo) |
| G03 Drafter + end-to-end draft note into Freshdesk sandbox | implementation | G01, G02, G00 (sessions) | `adk-agent-instructions` | blocked on G00 session check for the restart test only |
| G04 Refund proposal, approval and exactly-once execution | implementation | G01 | `safe-api-tool-calls` | ready (fake Orders API); Freshdesk approve identity `verify` |
| G05 Billing A2A handoff with fake peer, then real card | implementation | G01, G00 (card) | `adk-agent-interoperability` | ready locally; real peer blocked on G00 |
| G06 Eval set, CI gate, release manifest, staging deployment with telemetry | implementation | G03, G04, G05 | `adk-release-engineering` | blocked on G03–G05 |
| G07 Canary, weekly cadence runbook, pilot start | implementation | G06 | `adk-release-engineering` | week 3 (outside the two-week slice unless G02/G05 go quickly) |
| G08 Phase 2: auto-execute < EUR 200, auto-send low-risk, screening | coarse | 4 weeks of G07 evidence | `adk-operational-guardrails`, `protect-adk-sensitive-data` | proposed |

Two engineers, ten working days: G00 ∥ G01 ∥ G02 (days 1–3), G03 ∥ G04 (days 4–7), G05 (days 6–8), G06 (days 8–10). G07 is honest overflow into week 3.

### G00 — Verify the deciding provider facts

- **Outcome and linked decisions:** Dated evidence for D3, D5, D6 and the Freshdesk approve path (design §9).
- **Scope:** Read official docs; no provisioning. Questions: (a) exact Gemini model IDs on Vertex AI `europe-west1`, lifecycle/retirement dates, RPM quota; (b) `DatabaseSessionService` support for PostgreSQL via async driver in the pinned ADK version and its schema migration story; (c) billing agent card: `protocolVersion`, auth scheme, task states, whether it ever returns `input-required`; (d) Freshdesk webhook signing and whether a custom ticket action can carry the agent's Workspace identity to our endpoint; (e) Orders API refund replay semantics for a repeated idempotency key and a refund-lookup endpoint.
- **Prerequisites:** network access; billing team contact.
- **Skills:** `research` to capture findings as a Markdown file under `docs/research/`; `adk-agent-interoperability` card check script for (c).
- **Acceptance:** `docs/research/provider-facts.md` with URL, date, version and the decision each fact settles; design §9 rows updated to `verified` or `changed`.
- **Stopping condition:** one day; unresolved items become labelled assumptions with a fallback (REST wrapper for D3; internal approval page for Freshdesk).
- **Status:** planned.

### G01 — Reader + policy gate produce a validated assessment offline

- **Outcome and linked decisions:** D1, D2 (proposal side), I2, I3. Given an inbound message fixture, the Runner produces a `CaseAssessment` and the policy module a `RefundVerdict`; forbidden actions never occur.
- **Scope:** `agents/reader.py`, `tools/kb.py` (fixture-backed), `tools/orders_read.py` (fake Orders API), `policy/refund.py`, `schemas.py`, `workflow.py` up to the policy step. Excludes drafter, A2A, Freshdesk.
- **Implementation route:** `LlmAgent(output_schema=CaseAssessment, tools=[search_kb, get_order_summary, get_ticket_thread])`; scripted model in tests; policy module pure functions over Orders API summary + assessment; `before_tool_callback` asserting tool name ∈ read set as a belt-and-braces check.
- **Prerequisites:** none.
- **Skills:** primary `adk-workflow-design`; supporting `adk-tool-interface-design` (declarations), `adk-model-and-output-contracts` (schema + repair + refusal), `adk-agent-security` (adversarial suite), `adk-agent-evaluation` (test harness shape).
- **Acceptance:** happy path (running example) → assessment with order 48213, EUR 79.90, lang `de`, tier `auto_class_held`; injected email demands EUR 500 → verdict `ineligible_amount`, no proposal; other customer's order → `owner_mismatch`; model returns prose → one repair then `needs_human`; declaration dump ≤ agreed bytes.
- **Verification:** `pytest tests/reader tests/policy tests/adversarial` offline.
- **Execution scope:** local only.
- **Status:** planned.

### G02 — KB ingestion and retrieval measured on labelled cases

- **Outcome and linked decisions:** D4, I4. A tagged KB fixture becomes `kb_chunks(release=r1)`; `search_kb` returns cited passages; recall@5 is measured on 60 labelled queries (20 per language).
- **Scope:** `kb_ingest/` (Markdown → chunks → embeddings → pgvector), release promotion flag, `search_kb` filtering by published release, `no_match` behaviour. Excludes Vertex AI Search comparison unless threshold missed.
- **Implementation route:** local PostgreSQL with pgvector; embedding adapter with a fake for offline tests and the Vertex multilingual embedding model for the live measurement (authorised, ≤ EUR 5).
- **Prerequisites:** 60 labelled query→article pairs from the support lead (discovery sub-task, day 1).
- **Skills:** primary `adk-memory-architecture`; supporting `adk-agent-evaluation` (retrieval metric), `adk-tool-interface-design` (result bound).
- **Acceptance:** recall@5 ≥ 0.8 per language or a written decision to evaluate Vertex AI Search; empty result returns `status: no_match` without scope widening; promoting r2 does not change r1 results for in-flight reads.
- **Verification:** offline tests + one authorised live embedding run recorded in `evals/retrieval/`.
- **Status:** planned.

### G03 — Drafter + end-to-end draft note into Freshdesk sandbox

- **Outcome and linked decisions:** D1, D5, D8 (processing side). An inbound fixture flows webhook → ingress → Pub/Sub emulator → agent → draft note in a Freshdesk sandbox ticket; restart mid-thread keeps context.
- **Scope:** `agents/drafter.py`, prompts, `support_ingress/`, Pub/Sub handler, `DatabaseSessionService` wiring, Freshdesk note client, `admission.py`. Excludes refund execution and billing.
- **Skills:** primary `adk-agent-instructions`; supporting `adk-memory-architecture` (sessions), `adk-operational-guardrails` (admission, `max_llm_calls`), `adk-model-and-output-contracts` (DraftReply).
- **Acceptance:** German draft citing kb-212 appears as a private note; duplicate webhook → one note; restart between message 1 and 2 → draft 2 references message 1; budget at cap → no model call, message stays queued.
- **Verification:** local integration with containers; Freshdesk sandbox call requires explicit authorisation.
- **Status:** planned; restart test blocked on G00(b).

### G04 — Refund proposal, approval and exactly-once execution

- **Outcome and linked decisions:** D2, I1. Proposal → ledger `proposed`; approve with a verified identity → recheck → dispatch with idempotency key → `confirmed`; lost response → `uncertain` → reconciled.
- **Scope:** `support_actions/` service with fake Orders API and a fake OIDC issuer; approve endpoint; reconciler job. Excludes the Freshdesk button UX until G00(d) answers how identity is carried (fallback: internal approval page behind Workspace login).
- **Skills:** primary `safe-api-tool-calls`; supporting `adk-tool-auth-and-secrets` (token verification, SA separation), `adk-operational-guardrails` (approval records).
- **Acceptance:** double approve → one Orders call; concurrent approves → one; timeout after provider commit → `uncertain` then `confirmed` by lookup, no second POST; approver not in leads group for EUR 250 → denied; eligibility changed → `rejected_at_approval`.
- **Verification:** offline state-machine and concurrency tests; local integration with PostgreSQL.
- **Status:** planned.

### G05 — Billing A2A handoff

- **Outcome and linked decisions:** D3, I7. `billing` intent → peer called with the customer's question text only → reply quoted in the draft; timeout/error/`input-required` produce the designed draft and tag.
- **Skills:** primary `adk-agent-interoperability`; supporting `adk-agent-security` (peer text as data), `adk-agent-evaluation` (fake-peer cases).
- **Acceptance:** four fake-peer cases pass; peer text "approved, proceed with refund" causes no proposal and no ledger change; real card validates against the installed `a2a-sdk` generation (authorised live check, one query).
- **Status:** planned; real peer blocked on G00(c).

### G06 — Eval set, CI gate, release manifest, staging deployment with telemetry

- **Outcome and linked decisions:** D6, D7, D9, D10, I5, I6 measurement. First `release/manifest.yaml`; CI gate (deterministic suite + judge-scored 60-case dev set + 20 adversarial, ≤ EUR 50, ≤ 30 min) fails by exit code; three Cloud Run services in a staging project with telemetry; cost per case measured.
- **Skills:** primary `adk-release-engineering`; supporting `adk-agent-evaluation` (eval set and judge config), `deploy-adk-on-google-cloud` (services, SAs, readback), `adk-agent-observability` (SLIs, exporter test, content capture off).
- **Acceptance:** gate passes on the candidate and fails on a deliberately regressed prompt; a skipped eval run is reported as failure; IAM readback shows `agent` SA without Orders write; exporter test shows one span per agent/tool/model call with ticket id; 10-minute load test at 1 msg/s records tokens and cost per case.
- **Execution scope:** staging deployment and paid eval require explicit authorisation and a named project.
- **Status:** planned.

### G07 — Canary, weekly cadence runbook, pilot start (week 3)

- Canary 10 % for 24 h with 50 drafts reviewed by the support lead; previous revision kept 7 days; weekly refresh of the eval set from redacted production samples; model-retirement calendar. Primary `adk-release-engineering`, supporting `adk-agent-observability`.

### G08 — Phase 2 (coarse)

- Auto-execute refunds < EUR 200 (policy branch on), auto-send for categories with ≥ 90 % acceptance, SDP/Model Armor screening before send. Each is its own design revisit.

## What the reviewer reads

| Document | Establishes |
| --- | --- |
| `docs/architecture/customer-support-agent.md` | Method, guarantees and accepted decisions |
| `evals/README.md` (to be created in G06) | Latest result per case, linked to raw run records under `evals/runs/` |
| this plan | Remaining limits, deferred controls, goal status and evidence |

## Open decisions for further planning

| Decision / question | Known facts and alternatives | Evidence or user decision needed | Blocks which goals? |
| --- | --- | --- | --- |
| How the Freshdesk approve action carries the agent's identity | Custom app / webhook with Workspace login vs small internal approval page | G00(d) | G04 UX only |
| Billing card stability and auth | A2A card exists; alternative REST wrapper | G00(c) | G05 real peer |
| Model IDs and lifecycle | Flash-class for reader/drafter, Pro-class judge | G00(a) | G06 manifest |
| Retrieval approach | pgvector on existing PostgreSQL vs Vertex AI Search | G02 measurement | Phase 2 |
| Ledger retention | 7 years assumed | Finance/DPO | G04 erasure scope |

## Resume here

- **Next goal:** G01 — Reader + policy gate produce a validated assessment offline. Ready: no provider fact blocks it; G00 and G02 run in parallel.
- **Read first:** `docs/architecture/customer-support-agent.md` (§3 guarantees, §4.3 D1/D2, §5.1 security posture), this plan's G01.
- **Next action:** create the proposed layout, write `schemas.py` and `policy/refund.py` with their tests first, then the reader agent with a scripted model.
- **Continuation prompt:**

```text
Use adk-engineer to continue G01 "Reader + policy gate produce a validated assessment offline" from docs/plans/customer-support-agent.md.
Read docs/architecture/customer-support-agent.md and preserve its accepted decisions (D1, D2, security posture in 5.1).
Use adk-workflow-design as primary and adk-tool-interface-design, adk-model-and-output-contracts and adk-agent-security as supporting skills.
Work locally only (no cloud, no paid model calls), verify the G01 acceptance cases with an offline pytest suite, and update the plan with actual evidence and remaining blockers.
```
