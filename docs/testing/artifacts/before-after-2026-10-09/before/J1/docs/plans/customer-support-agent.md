# Implementation plan: Email customer-support agent

Status: draft, ready goals identified (no goal started)
Architecture: [../architecture/customer-support-agent.md](../architecture/customer-support-agent.md)
Continuation source of truth: this plan

## Destination and constraints

**Destination:** a pilot that turns each inbound support email into a cited reply
draft in the helpdesk. Eligible refunds ≤ 200 EUR are executed automatically under
policy, and billing questions are answered through the billing team's agent.
Releases ship weekly behind an evaluation gate. **Non-goals:** see design §1.
**Budget:** 2 weeks, 2 engineers, about €500 model spend. **Authorisation now:**
design only. Each goal's local work is authorised once the user asks for it. Cloud
deploys (G06), live model runs (G01/G02 live tiers) and calls to the payments or
billing staging environments need separate, explicit permission.

Repository state: empty (only `.claude/skills/`). Every module below is a
**proposed** greenfield layout. Pinned versions are not yet chosen: ADK version,
model ID and judge ID come from G00. Any goal that changes them is a release.

Proposed layout: `support_agent/{intake.py, worker.py, router.py, agents/reader.py,
agents/composer.py, prompts/<agent>/instruction.md, refunds/{policy.py, ledger.py,
executor.py, reconciler.py}, billing_peer.py, kb/{ingest.py, search.py},
release_check.py}`, `tests/`, `evals/`, `release/manifest.yaml`.

## Implementation map

| Decision | Component and integration point | GCP responsibility | Primary skill | Verification still needed |
| --- | --- | --- | --- | --- |
| D1 intake/jobs | `intake.py` webhook (HMAC) → `support_jobs` insert → Cloud Tasks enqueue | Cloud Run, Cloud Tasks, Cloud SQL | `deploy-adk-on-google-cloud` | Cloud Tasks named-task dedupe window |
| D2 identity | `worker.resolve_customer(thread)` before any agent call. `customer_id` placed in trusted state | — | `adk-tool-auth-and-secrets` | Helpdesk DMARC field (OD3) |
| D3/D4 refunds | `refunds/policy.py`, `ledger.py` (claim txn, caps, kill switch), `executor.py`, `reconciler.py` | Cloud SQL. Secret Manager for API credential | `safe-api-tool-calls` | Provider idempotency/status (OD1) |
| Reader/composer | `LlmAgent` ×2 run by `Runner` in `worker.py`. `output_schema` on both. `kb_search` FunctionTool on composer | Vertex AI (EU) | `adk-workflow-design` | `output_schema` + tools on chosen ADK version |
| D5 billing | `billing_peer.py` wraps `RemoteA2aAgent(timeout=30)` or REST | Peer's hosting. Worker SA ID token | `adk-agent-interoperability` | Peer card/auth (OD2) |
| D6 KB | `kb/ingest.py` → pgvector `kb_release`. `kb/search.py` bounded results | Cloud SQL pgvector, Vertex embeddings | `adk-memory-architecture` | pgvector on existing DB |
| D9 release | `release/manifest.yaml`, CI gate script, canary runbook | CI runner, Cloud Run traffic tags | `adk-release-engineering` | — |
| Observability | OTel setup in `worker.py`/`intake.py` | Cloud Trace/Logging EU | `adk-agent-observability` | Content-capture env gates on version |

## Goals and dependencies

| ID and goal | Type | Depends on | Primary skill | State / blocker |
| --- | --- | --- | --- | --- |
| G00 Confirm external contracts | discovery | — | `adk-engineer` (routes per question) | ready (needs the owning teams) |
| G01 Dev set and baseline | implementation | — | `adk-agent-evaluation` | ready (needs ticket export) |
| G03 Refund policy and ledger, local | implementation | — | `safe-api-tool-calls` | **ready, next** |
| G02 Reader agent and router | implementation | G01 | `adk-workflow-design` | proposed |
| G04 KB retrieval and composer | implementation | G02 | `adk-memory-architecture` | proposed |
| G05 Billing peer adapter | implementation | G02. OD2 for live | `adk-agent-interoperability` | proposed (fake peer ready) |
| G08 Adversarial suite | implementation | G03, G04, G05 | `adk-agent-security` | proposed |
| G07 Release manifest and gate | implementation | G01, G08 | `adk-release-engineering` | proposed |
| G06 Shadow deploy and telemetry | implementation | G07, G00, cloud authorisation | `deploy-adk-on-google-cloud` | blocked: authorisation |

Two-week schedule (proposed): week 1 covers G00 ∥ G01 ∥ G03, then G02. Week 2 covers
G04, G05, G08 and G07. G06 is shadow-only if authorised. Pilot refunds stay disabled
until OD1 and OD3 are closed.

### G00 — Confirm external contracts (discovery)

- **Question:** OD1 (refund idempotency/status), OD2 (billing A2A card, protocol
  version, auth, input-required use), OD3 (DMARC in helpdesk payload), OD6 (EU model
  ID, retirement date, prices), plus pgvector availability and the ADK version pin.
- **Bounded investigation:** docs and staging cards from the owning teams. Official
  Vertex/ADK pages, with each URL and access date recorded in the design §9. Stop
  after 2 days, or once each question has an answer or a named owner.
- **Expected output:** design §10 rows closed or re-scoped, plus the dated sources.
  This unblocks enabling auto-refund, G05 live wiring and G06.

### G03 — Refund policy and ledger, local (next ready)

- **Outcome and linked decisions:** given a validated claim and an authoritative
  order, the system makes at most one correct provider refund, or a human proposal.
  Links D3, D4, I1, I2.
- **Scope:** `policy.py` (rules from design §3 Q5, versioned), `ledger.py` (claim
  transaction with unique `(order_id, order_line_id)`, caps reservation, kill
  switch), `executor.py` (re-read before dispatch, provider key `op_id`),
  `reconciler.py`. The provider is a fake that implements both OD1 variants.
  **Excluded:** model calls, helpdesk, live payments API.
- **Prerequisites:** none for local. The live provider waits on OD1.
- **Skills:** primary `safe-api-tool-calls`. Supporting `adk-operational-guardrails`
  (caps, kill switch).
- **Acceptance:** the policy table passes for every rule boundary (199.99 / 200.00 /
  200.01 EUR, day 30/31, already refunded, foreign customer). Concurrent duplicate
  claims → one dispatch. Crash after dispatch → `uncertain` → reconciler resolves
  without a second dispatch. Changed payload for an existing op → rejected. Daily
  cap reached → no dispatch. Kill switch → no dispatch.
- **Verification:** `pytest tests/refunds` against PostgreSQL in a local container.
  These tests need no `google.adk`.
- **Execution scope:** local only.
- **Status and evidence:** planned.

### G01 — Dev set and baseline

- Outcome: about 200 labelled historical tickets (intent × language, 40 refund
  cases with known outcomes, 60 KB questions with gold articles), redacted. The
  frozen eval-set hash and the current first-response baseline are recorded.
  Primary `adk-agent-evaluation`; supporting `protect-adk-sensitive-data` for
  redaction. Acceptance: labels double-checked on a 20 % sample, and the set's hash
  is recorded.

### G02 — Reader agent and router

- Outcome: an email yields validated `TicketClaims`, and code routes each intent.
  Primary `adk-workflow-design`; supporting `adk-model-and-output-contracts` (schema,
  repair, refusal), `adk-agent-instructions` (prompt as versioned code),
  `adk-agent-security` (reader has 0 tools). Acceptance: scripted prose,
  fenced-JSON and valid-but-wrong outputs behave as designed. Live intent accuracy
  on G01 is recorded as the baseline (3 repeats, live run authorised separately).

### G04, G05, G06, G07, G08 — coarse until their prerequisites settle

- **G04:** KB ingest with versioned release, bounded `kb_search`, composer with
  citations and `release_check`. Acceptance: recall@5, citation support, and a
  foreign order ID blocked.
- **G05:** `BillingPeerAdapter` against a fake peer covering normal, timeout, error,
  input-required and injected instructions. Live wiring waits on OD2 and OD4.
- **G08:** adversarial cases from design §6 with call-absence assertions, added to
  the gate.
- **G07:** manifest with no aliases, an exit-code gate, a canary runbook, and the
  weekly billing-peer contract check.
- **G06:** shadow deploy (refunds disabled) in the EU region, OTel with content
  capture off, deploy readback. Needs explicit cloud authorisation.

## What the reviewer reads

| Document | Establishes |
| --- | --- |
| [Design](../architecture/customer-support-agent.md) | Method, decisions, invariants, failure handling, open decisions |
| This plan | Goal order, acceptance, what is deferred or blocked |
| `evals/SUMMARY.md` (created by G01) | Latest eval result per case and gate history |

## Open decisions for further planning

These are the design's OD1–OD6 (design §10); they are not repeated here. All the
product-owner answers in design §3 are assumptions until a real PO confirms them.

## Resume here

- **Next goal:** G03 Refund policy and ledger. It carries the most consequential
  invariant (money, I1/I2), and it is fully local with a fake provider that covers
  both OD1 outcomes.
- **Read first:** design §3 (Q5), §4 (I1, I2), §5 (D3, D4) and §8 refund rows.
- **Next action:** write the policy rule table as parametrised tests, then the
  ledger claim transaction.
- **Continuation prompt:**

```text
Use adk-engineer to continue G03 "Refund policy and ledger, local" from docs/plans/customer-support-agent.md.
Read docs/architecture/customer-support-agent.md and preserve its accepted decisions (D3, D4, invariants I1, I2).
Use safe-api-tool-calls and adk-operational-guardrails.
Work within local code and a local PostgreSQL container only (no payments API, no cloud), verify the G03 acceptance cases, and update
the plan with actual evidence and remaining blockers.
```
