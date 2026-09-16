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

## Implementation-depth recheck — 16 September 2026

The second review compared the manuscript, serving code, installed SDK adapters,
test doubles, deployment guides and failure/recovery records. It added
[integration recipes](integration-recipes.md), [managed deployment](managed-deployment.md)
and [failure recovery](failure-recovery.md), and expanded the four store guides.
The entrypoint loads these references conditionally. More detail does not change
the source's acceptance boundary or turn recommendations into implemented code.

| Added lesson | Source anchors | Evidence and limit |
| --- | --- | --- |
| App/Runner assembly, metadata-only ownership reads, trusted consent and public event projection | `memory_support_agent/runtime.py`, `api/services.py`, `api/session_access.py`, `api/app.py`, `api/public_projection.py`; `tests/test_public_projection.py`, `tests/test_lifespan.py`, `tests/test_session_access.py` | Implemented interfaces; snippet checks use real ADK types with local doubles. New real-event tests showed `is_final_response()` can accept partial events with summarisation/LRO overrides; the skill adds an explicit partial guard absent from the source. Narrower classification of policy outages and unrelated SDK errors is also an improvement. |
| Successful tool plugins mutate and return `None`; output publication must be complete | `memory_support_agent/sensitive_tool_output_plugin.py`; `tests/test_content_boundary.py`, `tests/test_parallel_tool_screening.py` | Actual PluginManager coverage exists. A downstream analytics-export canary is a stronger proposed test, not established by configuration order. |
| HMAC canonicalisation, retained-key aliases, completed and erased replay | `memory_support_agent/secret_provider.py`, `api/run_coordinator.py`; `tests/test_offline_api_acceptance.py`, `tests/test_secret_provider.py` | HTTP coverage with Secret Manager doubles; distributed key-rollout and all retention scenarios remain separate. |
| Candidate serialisation and one-slot cardinality | `memory_support_agent/tools/preferences.py`, `memory_support_agent/callbacks.py`; `tests/test_vertex_memory_handoff.py` | Real Runner sequential/parallel handoff is tested for one remember tool, not two remember calls sharing the slot. |
| Preserve late handles without regressing status | `memory_support_agent/memory_ledger.py`, `memory_support_agent/managed_memory.py` | New offline reproduction confirms local handle loss after `mark_indeterminate` and a Redis read/modify/write status regression under a controlled interleaving. Neither implementation was fixed in this documentation task. |
| Recall projection, project aliases and actual fact TTL configuration | Installed ADK 2.8.0 `google/adk/memory/memory_entry.py` and `google/adk/memory/vertex_ai_memory_bank_service.py`; `memory_support_agent/managed_memory.py`, `scripts/managed_stack_lib/google_cloud.py`; `tests/test_managed_memory_sdk.py`, `tests/test_memory_recall_project_identity.py`, `tests/test_privacy_project_identity.py` | The entry schema supports metadata but the inspected search adapter drops it. The lab resource body fixes fact TTL at 24 hours; changing `MEMORY_TTL_SECONDS` alone does not update it. Other SDK versions need inspection. |
| Atomic erasure completion and unblock | `memory_support_agent/privacy/ledger.py`, `memory_support_agent/privacy/worker.py`; `tests_live/test_privacy_redis.py` | Implemented claim/owner/status fence, with historical real-Redis coverage. It does not cancel downstream requests; that Redis suite was not rerun in this recheck. |
| Runtime RAG permission, release pinning and discriminating evaluation | `memory_support_agent/release_registry.py`, `scripts/managed_stack_lib/permissions.py`, `scripts/managed_stack_lib/rag_evaluation.py`, `ingestion/evaluate_rag.py`, `ingestion/promote_rag.py`; `tests/test_rag_runtime_permissions.py`, `tests/test_release_registry.py` | Managed evaluation assumes the first document; the generation fake does not enforce generation. Multi-document evaluation, fuller standalone fingerprints and ambiguous promotion reconciliation are extensions, not proven source behaviour. |
| Authorised-view ACLs and lazy BigQuery result fetching | `scripts/managed_stack_lib/configuration.py`, `memory_support_agent/backends/bigquery_tickets.py`; `tests/test_gcp_contracts.py` | Source establishes view authorisation. Its query tests return eager lists; deadline/error handling across lazy pages needs stronger coverage. Stable public pagination is an optional addition. |
| Analytics capture, schema and loss as separate contracts | `memory_support_agent/analytics.py`, `memory_support_agent/config.py`; `tests/test_analytics.py` | Source has opt-in metadata-oriented configuration. Actual exporter-byte canaries and dropped-event metrics require separate verification. |
| Resume only eligible retrieval attempts; preserve completed cases and uncertainty | `scripts/managed_stack_lib/rag_evaluation.py`; `tests/test_rag_setup_recovery.py`; `OFFLINE_RAG_RECOVERY_2026-09-14.md`, `INDEPENDENT_RAG_RECOVERY_LIVE_2026-09-14.md` | Offline interruption/budget tests and a later successful setup retrieval; no permission to repeat imports or claim full hosted acceptance. |
| Bound log pagination, use real token expiry and continue only recognised smoke phases | `scripts/cloud_smoke.py`, `scripts/managed_stack_lib/google_cloud.py`; `tests/test_cloud_probe_log_window.py`, `tests/test_rest_token_expiry.py`; `CLOUD_HOSTING.md`, `INDEPENDENT_HOSTED_FINAL_2026-09-14.md` | Source has these recovery mechanisms. Token tests use doubles; continuation is narrowly guarded, not a universal resume facility. |
| Protect within actual quota and retain evidence before cleanup | `memory_support_agent/content_policy.py`, `memory_support_agent/sensitive_data.py`; `INDEPENDENT_SCREENING_REPLAY_2026-09-14.md`, `INDEPENDENT_DLP_DIAGNOSIS_2026-09-15.md`, `CLEANUP_CONFIRMATION_2026-09-15.md` | Call fan-out follows the implementation. Component replay did not establish the final failure's cause; pacing/batching and a complete hosted continuation remain unverified. |

The ledger reproduction executed only the three ledger class definitions
extracted with Python's AST, with injected standard-library dependencies and an
in-memory storage double. It did not import the application, load credentials
or call Redis/cloud services. The local sequence was `claim → mark_indeterminate
→ attach_operation → iter_unsettled`; the handle remained absent. In the Redis
case, the double changed stored status after returning the pending snapshot;
attachment wrote that stale status back. This demonstrates the transition
defects, not their observed frequency in a deployed system. The possible loss
of discovery-index consistency is a source-code inference, not a live result.

Deployment ordering and identity/configuration lessons also come from
`AUTHENTICATION.md`, `MANAGED_LAB.md`, `CLOUD_HOSTING.md`, `MIGRATION.md` and
`RAG_FOUNDATION.md`. Remote runtime, context compaction, streaming reconnect,
multi-candidate outboxes and guarded cutover recipes are labelled production
additions. Official service references are linked next to the relevant managed
deployment and recovery claims; no current prices or universal location/model
availability are asserted.

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
