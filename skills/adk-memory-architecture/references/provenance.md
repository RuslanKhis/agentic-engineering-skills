# Provenance and evidence limits

This skill adapts the author-owned Chapter 6 implementation and revised
manuscript of *Agentic Engineering*, under the repository's MIT licence. The
included [licence](../LICENSE) preserves that notice. No external source code or
other author's skill is bundled. The source repository has no published book
URL, so no publication link is invented. This package is fully usable alone.

Paths below identify historical evidence relative to the optional source
repository's `chapter-06-memory-and-rag/` directory. They are provenance labels,
not installation dependencies. The revised manuscript is
`CHAPTER_06_UPDATED.md`; the accepted comparison is
`MANUSCRIPT_COMPARISON_2026-09-15.md`.

## Rule-to-evidence map

| Skill behaviour | Implementation and test anchors | Qualification |
| --- | --- | --- |
| Choose stores by authority, lifetime and uncertainty | Manuscript “The different kinds of memory”, “Choose the store from the requirement”; `memory_support_agent/runtime.py` and `memory_support_agent/agent.py` | Architecture principle; four stores are available modes, not mandatory infrastructure |
| Use authenticated subject and owned session access; preserve API startup controls | `api/auth.py`, `api/session_access.py`, `api/services.py`; `tests/test_session_access.py`, `tests/test_api_authz.py`, `tests/test_lifespan.py` | Implemented; a bare Runner/CLI path does not inherit the full HTTP lifecycle |
| State deltas, public projection, completed-response idempotency | `api/public_projection.py`, `api/run_store.py`, `api/run_coordinator.py`; `tests/test_public_projection.py`, `tests/test_run_coordinator.py`, `tests/test_run_store.py` | Buffered JSON and completed replay implemented; renewable session leases and streaming replay are production additions |
| Consent, narrow candidates and asynchronous generation reconciliation | `memory_support_agent/tools/preferences.py`, `memory_support_agent/callbacks.py`, `memory_support_agent/managed_memory.py`, `memory_support_agent/memory_ledger.py`; `tests/test_vertex_memory_handoff.py`, `tests/test_managed_memory_sdk.py`, `tests/test_memory_ledger.py` | Implemented candidate/LRO ledger; durable candidate outbox, scanning and ready receipts are production additions |
| Trusted memory scope, eligibility and expiry | `memory_support_agent/memory_policy.py`, `memory_support_agent/managed_memory.py`, `memory_support_agent/tools/protected_memory.py`; `tests/test_memory_policy.py`, `tests/test_managed_memory_sdk.py`, `tests/test_protected_memory.py` | Local fixtures do not implement semantic retrieval; local and hosted readiness claims differ |
| Coordinate forgetting, late writes and content-free retry tombstones | `memory_support_agent/privacy/gate.py`, `memory_support_agent/privacy/ledger.py`, `memory_support_agent/privacy/service.py`, `memory_support_agent/privacy/sinks.py`, `memory_support_agent/privacy/worker.py`; `tests/test_privacy_workflow.py`, `tests/test_privacy_unsettled.py` | Worker-stage admission block implemented; immediate atomic block at request acceptance is a production addition |
| Bind retrieval to approved source manifest, entitlement and release | `memory_support_agent/backends/vertex_rag.py`, `memory_support_agent/release_registry.py`, `memory_support_agent/tools/policy.py`; `tests/test_rag_retrieval.py`, `tests/test_gcp_contracts.py`, `tests/test_release_registry.py` | Explicit application retrieval implemented; do not infer native model-service retrieval has identical inspection coverage |
| Stage, evaluate and promote with release-bound evidence and CAS | `ingestion/setup_rag.py`, `ingestion/evaluate_rag.py`, `ingestion/promote_rag.py`; `tests/test_rag_ingestion.py`, `tests/test_release_registry.py` | Narrow source inspection and two positive document-ID evaluation cases; broader quarantine/evaluation, citation rendering and byte budgets are additions |
| Parameterised trusted-scope SQL, authorised serving view, dated freshness | `memory_support_agent/backends/bigquery_tickets.py`, `memory_support_agent/tools/tickets.py`, `sql/serving_view.sql`; `tests/test_gcp_contracts.py`, `tests/test_local_backends.py` | Row timestamps are not replica-completeness evidence; durable runtime query reconciliation and total deadlines are additions |
| Protect before persistence/model use; minimise analytics and fail closed | `memory_support_agent/content_policy.py`, `memory_support_agent/sensitive_tool_output_plugin.py`, `memory_support_agent/analytics.py`; `tests/test_content_boundary.py`, `tests/test_parallel_tool_screening.py`, `tests/test_analytics.py` | After-tool rejection cannot undo writes; whole-row/log/trace inspection remains necessary |
| Durable setup state, explicit scope and separate regional teardown | `scripts/managed_stack.py`, `scripts/managed_stack_lib/`, `RAG_FOUNDATION.md`; `tests/test_managed_stack.py` | Lifecycle lessons from bounded campaigns; cleanup visibility and retained storage limit assurances |
| Read-only project inventory and environment mismatch reporting | Bundled `scripts/inspect_project.py` and `tests/test_inspect_project.py` | New helper tested for this skill; static signals do not prove application controls |

Production additions also include context compaction, signed remote end-user
assertions, downstream enforcement of lease loss, complete telemetry/retention
inventories, result byte limits and end-to-end deadlines. They are explicit
design requirements for applications claiming those guarantees, not claims
that the source implemented them. Concrete limits and synthetic topic/schema
names in the source are examples to choose deliberately in a target project.

## Historical acceptance, preserved without upgrading its claims

- The 15 September 2026 snapshot records **888 offline tests passed**, 14
  warnings, no failures or skips, in 159.85 seconds; `pip check` passed. All
  **180** recorded source hashes matched when this skill was created. The
  suite was not rerun in full as part of skill creation.
- The 14 September deployed hosted campaign passed real model/tool calls,
  tickets/RAG, completed-response replay/isolation, profile behaviour, consent
  denial and completed control-user memory. The target consented-memory
  assertion **failed** after DLP de-identification returned
  `ResourceExhausted`. Target completed memory/fresh recall, revision restart
  and separate-worker privacy deletion were **not run**.
- Earlier real managed-backend tests through a local API are a different
  execution boundary. They cannot supply the missing deployed hosted gates.
  Offline SDK doubles and failure injection cannot establish live quota or
  provider behaviour. Earlier quota exhaustion was observed, but timestamps
  did not establish the exact cause of the final hosted failure. Quota
  increases and pacing/batching remain remedies to validate.
- Active-resource cleanup passed for the recorded targets, with a missing
  pre-delete execution inventory preserved as an evidence gap. Regional RAG
  readback later confirmed Unprovisioned state for inspected backends.
  Retention and delayed billing prevent a universal zero-cost assurance.

These results come from `INDEPENDENT_HOSTED_ACCEPTANCE_2026-09-14.md`,
`INDEPENDENT_DLP_DIAGNOSIS_2026-09-15.md`, `CLEANUP_CONFIRMATION_2026-09-15.md`,
`verification/2026-09-15-hosted-acceptance/` and
`verification/2026-09-15-cost-closure/`. Exact source versions are in
[compatibility.md](compatibility.md). Current skill tests are recorded separately
in [skill-validation.md](skill-validation.md).
