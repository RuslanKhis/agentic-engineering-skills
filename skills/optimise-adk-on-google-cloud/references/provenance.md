# Provenance and scope

This skill translates updated Chapter 4 Parts 1, 2 and 3 into conditional engineering
actions. Its editorial sources are
`chapter-04-cloud-optimization/manuscript/CHAPTER-04-PART-1-UPDATED.md`,
`chapter-04-cloud-optimization/manuscript/CHAPTER-04-PART-2-UPDATED.md` and
`chapter-04-cloud-optimization/manuscript/CHAPTER-04-PART-3-UPDATED.md`.
The repository-relative locators below are optional provenance for maintainers;
the portable skill does not require the book repository to be present.
Historical evidence describes the recorded configuration and workload, not a
new execution of this skill.

## Application boundaries

Rules for lazy client creation, small schema lookups, result previews, complete
exports, structured delegation and independent I/O come from the manuscript's
application steps and these implementations:

- `chapter-04-cloud-optimization/application-optimizations/optimized_agent/bigquery_tools.py`
- `chapter-04-cloud-optimization/application-optimizations/optimized_agent/schema.py`
- `chapter-04-cloud-optimization/application-optimizations/optimized_agent/sub_agents.py`
- `chapter-04-cloud-optimization/application-optimizations/optimized_agent/parallel_tools.py`
- `chapter-04-cloud-optimization/application-optimizations/optimized_agent/sql_safety.py`

Default mock BigQuery results and mock download locations establish local
behaviour only. Scripted orchestration and truncation regressions are in
`chapter-04-cloud-optimization/application-optimizations/tests/test_main_offline.py`.
The initial live workflow exposed fabricated currency fallbacks and a truncated
answer; the later repaired campaign verified real currency results, five-row
export and a ten-row preview against fifteen exact exported rows. Preserve that
sequence using `chapter-04-cloud-optimization/FULL-TOOLS-RESULTS-2026-09-14.md`
and `chapter-04-cloud-optimization/CURRENCY-CSV-RESULTS-2026-09-14.md`.

Tenant authorisation, bounded arbitrary queries, strict typed handoffs, durable
authorised downloads, bounded pooled HTTP clients and deterministic execution
branches are production principles retained from the manuscript. The small
companion adapters do not establish those controls.

## Skills and caching

Progressive loading and preservation of application-level cache settings map to
`chapter-04-cloud-optimization/application-optimizations/optimized_agent/skills.py`,
`chapter-04-cloud-optimization/application-optimizations/optimized_agent/agent.py`
and `chapter-04-cloud-optimization/application-optimizations/optimized_agent/main.py`.
Request-level history exclusion is exercised by
`chapter-04-cloud-optimization/application-optimizations/verification/verify_formatter_isolation.py`.

The focused live evidence records actual Skill loading, current formatter state
with old history absent, and two later turns each reporting 5,414 cached input
tokens. It does not establish automatic formatter integration, script sandboxing
or ordinary-request cache hits. The offline counterexample in
`chapter-04-cloud-optimization/manuscript-review/evidence/single_turn_model_calls.py`
shows why `single_turn` is not a one-generation budget.

## Lifecycle and evidence

Persisted reservations, ownership before mutation, uncertain-outcome
reconciliation and cleanup-only recovery draw from
`chapter-04-cloud-optimization/application-optimizations/verification/campaign_budget.py`,
`chapter-04-cloud-optimization/application-optimizations/verification/full_tools_campaign.py`
and their guard tests. The currency/CSV report records a concurrent receipt-writer
failure and repair; its initial metadata counter is not independently exact.

Cloud resource ownership and repeatable cleanup also map to
`chapter-04-cloud-optimization/cloud-run/lifecycle.py`,
`chapter-04-cloud-optimization/cloud-run/native_lifecycle.py`
and `chapter-04-cloud-optimization/cloud-run/tests/test_owned_lifecycle.py`.
`chapter-04-cloud-optimization/CLEANUP-CONFIRMATION-2026-09-15.md`
provides later independent inventory evidence. Logical absence is separate from
provider recovery retention, historical usage and billing. The campaign's fixed
identities, limits and private SDK patches are audit-specific, not portable
production enforcement or permission for another paid run.

## Cloud Run

Serving, authentication, source staging, smoke acceptance and CPU experiments
map to `chapter-04-cloud-optimization/cloud-run/main.py`,
`chapter-04-cloud-optimization/cloud-run/auth.py`,
`chapter-04-cloud-optimization/cloud-run/stage_agent.py`,
`chapter-04-cloud-optimization/cloud-run/smoke.py`
and `chapter-04-cloud-optimization/cloud-run/cpu_experiment.py`.

`chapter-04-cloud-optimization/FOLLOWUP-AUDIT-2026-09-13.md`
records Docker schema/UI/auth/session behaviour and qualified timing samples.
`chapter-04-cloud-optimization/NATIVE-ADK-LIVE-RESULTS-2026-09-14.md`
records the corrected native source deployment and private schema smoke.
These hosted checks used the bounded `schema-smoke` profile, with explicit
caching disabled. They do not establish hosted full-tool permissions, CSV export,
distributed sessions or cache reuse. The original case-study headlines and
incomplete CPU comparison establish no transferable speedup. Fresh-project
onboarding remains outside the recorded coverage.

## Portable helper origins

`skills/optimise-adk-on-google-cloud/scripts/check_run.py` is a new, deliberately
stricter saved-event consistency verifier inspired by the manuscript's completion
and evidence rules. It is not an exact copy of a campaign verifier. Its explicit
contract requires correlated declared tools, asserted results and one completed
answer; optional cache/partial checks remain saved-record observations. Acceptance
does not authenticate evidence, measure latency, prove cloud permissions or enforce
a live budget. Its scope is covered by
`skills/optimise-adk-on-google-cloud/tests/test_check_run.py`
and `skills/optimise-adk-on-google-cloud/tests/test_adk_contract.py`.

`skills/optimise-adk-on-google-cloud/scripts/inspect_project.py`
and its inspector tests are adapted from the MIT-licensed
`skills/deploy-adk-on-google-cloud/scripts/inspect_project.py`
and `skills/deploy-adk-on-google-cloud/tests/test_inspect_project.py`.
The upstream licence is `skills/deploy-adk-on-google-cloud/LICENSE`;
retain its copyright and permission notice when redistributing the adaptation.
Manifest inspection supplies bounded declaration evidence, not resolved-package
compatibility or proof of application architecture.

## Agent Runtime application and state

`chapter-04-cloud-optimization/agent-runtime/support_agent/agent.py` exports both
the root agent and its App; its default profile includes compaction and a metrics
tool. The routing-only live profile disables both. Its deterministic routing tool
still sits inside model-mediated orchestration, so one agent is not one generation.
`chapter-04-cloud-optimization/agent-runtime/support_agent/requirements.txt`
records the ADK 2.8.0 / AI Platform SDK 1.153.1 / GenAI 2.19.0 combination.
The inspector's additional runtime gate and extra-conflict rule are grounded in
that file and installed 1.153.1 distribution metadata, not a general resolver.

`chapter-04-cloud-optimization/agent-runtime/runner.py` constructs its real local
Runner with only the root agent, losing exported App compaction. The rule to
preserve App settings is also checked independently in this skill's
`tests/test_runtime_contract.py`: real ADK and summariser orchestration, with
deterministic generation boundaries, changes subsequent request context while
retaining stored original events. It contrasts agent-only construction. The
installed 2.8.0 compaction implementation uses observed prompt usage or an
effective-context estimate if metadata is absent; it does not impose a hard
next-request token limit. None of this proves real model summary quality.

`chapter-04-cloud-optimization/agent-runtime/local_compaction_test.py` defaults
to a fixed summary and list replacement. Other independent demonstrations use
mock providers in `chapter-04-cloud-optimization/agent-runtime/examples/`:

- `memory_callbacks.py` selects a fixed event slice and awaits mock ingestion;
  durable cursors, an outbox and nonoverlapping delivery are production additions.
- `workflow_parallelism.py` and `support_context.py` demonstrate scheduling;
  trusted policy, required/optional data and aggregate admission are additional
  application contracts.
- `backpressure.py` bounds queue count but not chunk bytes or the full
  failure-aware shutdown protocol.
- `selective_persistence.py` joins, awaits and clears a shared buffer; the
  completed-batch guidance prevents loss of input arriving during that await.
- `model_retry.py` checks a mock synchronous attempt between deadline checks;
  whole-attempt deadlines and retry ownership require separate enforcement.
- `resource_sizing.py` computes an inverse CPU recommendation. Its arithmetic
  tests do not validate that interpretation; the skill instead uses measured
  container topology, memory and downstream capacity.

`chapter-04-cloud-optimization/agent-runtime/long_running_demo.py` demonstrates
call-ID continuation with a dictionary, daemon thread and default mock runner.
Durable jobs, owner-bound idempotency, terminal failures, restart recovery and
deduplicated continuation are production principles, not properties of that demo.
`chapter-04-cloud-optimization/manuscript-review/evidence/part2/stream_consumer_probe.output.json`
records false-positive acceptance in the original manuscript's stream consumer.
The skill retains strict completion rules and separate delivery evidence instead.

## Agent Runtime lifecycle evidence

`chapter-04-cloud-optimization/agent-runtime/owned_runtime.py`,
`chapter-04-cloud-optimization/agent-runtime/smoke_session.py` and
`chapter-04-cloud-optimization/agent-runtime/tests/test_owned_guards.py`
ground the receipt, source-allowlist, repeat-verification, operation-scope and
cleanup rules. Their private SDK interception and Unix-specific wrappers are not
bundled as portable deployment automation.

`chapter-04-cloud-optimization/AGENT-RUNTIME-LIVE-RESULTS-2026-09-14.md`
is the authoritative dated result for routing-only deployment, remote-client
session continuity and selected negative access tests. Its four submissions
produced seven observed logical generations. Cleanup passed after a regional
DELETE operation parser failure and recovery of already accepted work; no second
DELETE or replacement deployment was needed. A new response-parser branch was
tested offline; live recovery verified regional polling and exact absence.

`chapter-04-cloud-optimization/agent-runtime/chat_client.py` omits the full
deadline, authoritative rendering and cleanup controls; the live harness supplied
its deadline and session cleanup. Neither that live result nor
`chapter-04-cloud-optimization/agent-runtime/tests/test_real_boundaries.py`
establishes the real local managed-session runner, full metrics/compaction, Memory
Bank, browser partial delivery, durable jobs, cross-principal isolation, load
improvements or fresh-project onboarding. Capacity products and stronger
production state designs remain guidance requiring their own evaluation.

## GKE workload and lifecycle

`chapter-04-cloud-optimization/gke/owned_lab.py` owns manifest generation, source
staging, immutable-image recording, dedicated build/node identities, direct KSA
permissions, two-Pod quota, private exposure and repeat verification. Its checked-in
`gke/k8s/` references are not the applied deployment. This grounds inspection of
the real delivery path and the rule to reconcile quota, surge and HPA as one
configuration. Tests in `gke/tests/test_owned_lab.py`,
`gke/tests/test_deploy_preflight.py` and `gke/tests/test_deployment_scripts.py`
exercise ownership, collisions, IAM preservation and uncertain-operation recovery.
The skill carries those invariants, not the lab's project-specific automation.

`chapter-04-cloud-optimization/GKE-RETRY-LIVE-RESULTS-2026-09-14.md` is the final
successful result after the earlier capacity failures. It records the same-region
private workload, actual digest and KSA, real routing/UI, stored-event continuity
through Pod replacement, repeat setup, session cleanup and independent teardown.
The source matched 89 offline tests. Five submissions produced nine logical
generations. Both Ready Pods were on one node. No region/quota/code change during
that successful retry explains the prior provider shortage as an application fix.

`chapter-04-cloud-optimization/CLEANUP-CONFIRMATION-2026-09-15.md` distinguishes
active-resource absence from source-object soft deletion and provider history.
Complete cleanup owns session resources, builds, registry/storage, IAM, identities
and network dependencies as well as the cluster. Production edge/database/pool
additions need separate ownership; the private lab's deletion does not cover them.

## GKE serving and production principles

`chapter-04-cloud-optimization/gke/app.py` wires `SESSION_SERVICE_URI` into ADK's
FastAPI factory and falls back to temporary SQLite; it does not consume
`DATABASE_URL`. `gke/tests/test_managed_sessions.py` checks regional URI handling
independently of global model location. `gke/tests/test_application_http.py`
exercises actual ADK HTTP/session orchestration with model transport doubled;
its user keys and health endpoint do not establish caller identity or live model
readiness. `gke/support_agent/agent.py` classifies support tickets; it does not
submit them to a help desk.

`gke/examples/credential_startup.py`, `client_reuse.py` and
`session_service_lifecycle.py` are illustrative components, not the server's
implemented startup lifecycle. Some use mock services; credential retry counts
alone do not bound a refresh operation. `gke/examples/request_timing.py` emits
raw session identifiers, so its monotonic timing lesson is retained without
copying its payload as a production telemetry policy.

`gke/tests/test_telemetry.py` tests developer-UI consent with telemetry disabled.
The updated manuscript and
`chapter-04-cloud-optimization/manuscript-review/evidence/part3/session_telemetry_smoke_probe.output.json`
support the distinction between capture flags, exception leakage and raw native
conversation identifiers. The optional `assets/session_observation.py` adapts the
manuscript's custom span helper. `tests/test_gke_observation.py` checks actual
in-memory export, exception/cancellation preservation, safe fixed attributes and
unsafe default/parent controls. This is local custom-span evidence, not a complete
ADK/HTTP/exporter privacy filter.

`gke/scripts/validate_smoke.py` and `gke/smoke_test.sh` ground complete routing and
exact-session cleanup. The skill's existing `check_run.py` additionally validates
explicit invocation/call correlation and strict STOP completion. Neither saved
events nor the historical `/run` PASS establish partial delivery through an edge.

HPA/VPA coordination, admitted resource sizing, topology, Gateway/IAP, backend
draining, PostgreSQL pools/migrations, retained clients, export allowlists and
advanced capacity/isolation options are production principles retained from the
updated Part 3 manuscript, with official documentation linked in the GKE
references. They require implementation and target-specific evaluation; they
are not presented as live-tested companion features.
