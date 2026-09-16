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

## Part 1 depth review: coverage and additions

Rechecked on 16 September 2026 against the complete updated Part 1 manuscript,
current application/Cloud Run implementation, initial independent audits, failed
campaigns and subsequent live repair/cleanup records. This is a coverage map for
maintainers, not another set of instructions an ordinary invocation must load.
Paths in the source column are relative to `chapter-04-cloud-optimization/`.

| Knowledge carried into the skill | Portable destination and change | Source and evidence boundary |
| --- | --- | --- |
| Lazy clients, narrow schema tools and trusted SQL policy | Retained [application.md](application.md); added job submission/wait/cancellation/retrieval and optional Storage Read distinctions | `application-optimizations/optimized_agent/{bigquery_tools,schema,sql_safety}.py`; manuscript application steps. The fixed-fixture adapter is not an arbitrary-query policy engine. |
| Actual configuration and deployment wiring | New [application-integration.md](application-integration.md) ledger and fresh-process checks | `optimized_agent/{main,agent,campaign_profile,bigquery_tools}.py` under `application-optimizations/`: import-time settings, literal model selection, cached clients and a schema-only profile. Environment presence is not effective configuration. |
| Bounded previews, full export and correct result selection | Retained architecture; new explicit current-result handoff and optional [formatting_contract.py](../assets/formatting_contract.py) | Manuscript bounded `FormattingInput` example and `CURRENCY-CSV-RESULTS-2026-09-14.md`. Asset is a new tested production building block; it does not establish query authorisation, durable storage or formatter integration. |
| Narrow child context and missing coordinator integration | New integration steps and A/B, failed-B-after-A and concurrent-result tests | `optimized_agent/{agent,sub_agents,bigquery_tools}.py`; `verification/verify_formatter_isolation.py`, both under `application-optimizations/`. Focused history exclusion passed; the original imported formatter was not wired to SQL output. |
| Independent async I/O, real/mock separation and honest currency errors | Retained [application.md](application.md); added per-stage failure diagnosis | `optimized_agent/parallel_tools.py`, `tests/test_parallel_tools.py` under `application-optimizations/`; `FULL-TOOLS-RESULTS-2026-09-14.md` and later currency/CSV report. A repaired successful lookup does not make the earlier combined failure a pass. |
| Progressive Skills and explicit cache behaviour | Retained [skills-and-cache.md](skills-and-cache.md); added early eligible cache creation, prefix accounting and independent deletion verification | `optimized_agent/{skills,agent}.py` under `application-optimizations/`; `cloud-run/INDEPENDENT-AUDIT-2026-09-11.md`; focused live cache/loading records. Experimental version-specific behaviour, not guaranteed cache hits or a script sandbox. |
| Complete answers and aggregate root/child work | New [part1-verification.md](part1-verification.md) and two [real-ADK tests](../tests/test_part1_adk_budget.py) | The initial Cloud Run audit records nested call-limit behaviour; this skill independently reproduces it in ADK 2.8.0 with deterministic models. A final-marked, content-free limit error is also reproduced; no provider usage is inferred. |
| Enforceable attempts, bytes, elapsed allowance and recovery | New operation-by-operation verification recipe | `application-optimizations/verification/{campaign_budget,full_tools_campaign}.py` and guard tests; currency/CSV report's concurrent receipt-writer failure. Retain cumulative counters, original start time, atomic unique receipt writes and cleanup-only recovery. Historical private SDK patches are not reusable enforcement. |
| Actual framework versus generous doubles | New acceptance ladder and reproduced-failure test table | `application-optimizations/tests/test_main_offline.py`, initial application audit and setup tests: real State delta, content-free events, partial table loads and create-only probes. Test the actual integration seam, then claim only that boundary. |
| Source staging, installed packages and multi-parser arguments | New [cloud-run-troubleshooting.md](cloud-run-troubleshooting.md) procedures | `cloud-run/{stage_agent,lifecycle}.py`, deployment/ownership tests and `FOLLOWUP-AUDIT-2026-09-13.md`: upload allowlist differs from Docker context, comma-valued settings cross parsers, checkout imports can hide missing package data. |
| Native source deploy failure despite fake CLI tests | New diagnosis and real Cloud SDK transport-boundary test plan | `NATIVE-ADK-RESULTS-2026-09-14.md`, corrected `NATIVE-ADK-LIVE-RESULTS-2026-09-14.md`, `cloud-run/native_lifecycle.py`, `cloud-run/tests/test_native_cloud_sdk.py`. SDK 572.0.0 selected a different path for remote source; literal generation suffix and default staging ownership mattered. The later private schema smoke passed. |
| Verified TLS, writable home, authentication and UI errors | New exact-interpreter troubleshooting with narrow regression conditions | Full-tools and follow-up reports; `cloud-run/{Dockerfile,auth,proxy,main}.py` and tests. CA trust was repaired without disabling verification; non-root HOME, token audience/client and the specific ADK UI SSE error representation needed separate tests. |
| Reconciliation, cleanup and absence evidence | Retained [lifecycle.md](lifecycle.md); added delayed visibility, deleted-service-account 403 and unexpected-content cases | `cloud-run/lifecycle.py` and ownership tests; `CLEANUP-CONFIRMATION-2026-09-15.md`. Retry exact reads, reconcile accepted work, verify terminal jobs and ownership before deletion. Permission failure is not absence. |
| Project access, credentials, APIs and trial billing | Retained the explicit target/preflight procedure in [lifecycle.md](lifecycle.md) | Chapter README and native live preflight records distinguish CLI, ADC, workload identity, quota project and required APIs/billing. Root environment changes do not replace nested keys. Existing-project success does not establish fresh-project onboarding. |
| CPU/startup/concurrency and honest measurement | Retained [cloud-run.md](cloud-run.md); added UI pre-warming and canary-versus-paired-experiment distinctions | `cloud-run/cpu_experiment.py`, follow-up report and manuscript serving guidance. Functional runs and limited timing samples establish no transferable speedup. Production shared sessions, backpressure and multi-instance operation still need target-specific tests. |
| Observable phases without leaking application data | New logging/export checks in [application-integration.md](application-integration.md) | Manuscript production telemetry guidance and `cloud-run/tests/test_telemetry.py`. Inspect the final formatter/exported representation; application spans omit platform queue/startup and do not establish browser token delivery. |

The 13 [formatting-contract tests](../tests/test_formatting_contract.py) check the
new asset's exact UTF-8 ceiling, strict cells/shape, nonfinite numbers, safe errors,
input preservation and revalidation after mutation. One authoring failure exposed
Pydantic strict-float acceptance of Decimal; an explicit plain-scalar check repairs
that boundary. Correlation strings remain join keys, not authority. Production
query admission, result ownership, distributed coordination and deployment are
deliberately left to the inspected target rather than supplied as an unverified
copy of the audit harness.

Current provider semantics consulted during this review are linked at their use:
the official BigQuery `Client`/`QueryJob` reference and `gcloud topic escaping`.
These references supplement the recorded implementation; inspect the target's
installed signatures before adapting newer documentation to older pins.

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

## Part 2 depth review: coverage and additions

Rechecked on 16 September 2026 against the full updated Part 2 manuscript, current
runtime application/examples, original comparison probes and retained preparation,
live and recovery results. Repository-relative paths below are optional maintainer
locators under `chapter-04-cloud-optimization/`, not portable dependencies.

| Knowledge carried into the skill | Destination and refinement | Source and evidence boundary |
| --- | --- | --- |
| Remote execution versus local execution with managed sessions | New [runtime-application-integration.md](runtime-application-integration.md) execution/configuration matrix and acceptance sequence | `agent-runtime/{chat_client,runner,local_compaction_test}.py`. The terminal client's hosted continuity passed; agent-only local Runner and mock compaction do not prove hosted App settings. |
| Profile/import/packaging changes can alter real versus mock behaviour | Integration matrix plus [deployment troubleshooting](runtime-deployment-troubleshooting.md) fresh-process recipe | `agent-runtime/support_agent/agent.py:9–46`, `runner.py:38–66`, `tests/test_real_boundaries.py`. Mode is captured at import, absent mocks force real mode, and even a local model-name string can invoke a provider through a real Runner. |
| App propagation and token compaction | Retained App/sliding-window tests; added [token contract tests](../tests/test_runtime_token_compaction.py) | Updated manuscript compaction section, pinned ADK 2.8 implementation and existing `tests/test_runtime_contract.py`. Three new offline tests exercise synthetic observed usage, oversized first input and preserved tool pairs in real outgoing requests. They do not measure real token usage or summary quality. |
| Recent-event retention preserves the tool protocol | Added explicit tail/pair caveat to [agent-runtime.md](agent-runtime.md) and integration recipe | Installed ADK `apps/compaction.py` and `flows/llm_flows/compaction.py`; the new actual-Runner test retains both call and response with nominal retention one. Event count is not an exact raw-history ceiling. |
| Lazy clients and known orchestration | Integration recipe distinguishes imports, construction, cached first use and nested model work | `agent-runtime/examples/{lazy_bigquery_client,cold_start_agent,workflow_parallelism,support_context}.py`. Mock reuse/scheduling does not establish one model generation, shared capacity or implemented refund policy. Concurrent first use follows Python's cache contract. |
| Extending routing to real metrics or compaction | New extension-by-extension acceptance table | `agent-runtime/support_agent/agent.py:88–142`, runtime live report. Triage disabled metrics and compaction; setup supplied no metrics dataset or runtime data grant. The stronger query and history controls remain target integration work. |
| Session continuity, ownership, retention and cleanup | Retained core guidance, added complete App/session/storage/cleanup sequence | `agent-runtime/{chat_client,runner,smoke_session}.py`; runtime live report. The external harness supplied the client's deadline and cleanup. Wrong-user checks under one credential do not prove cross-principal isolation. |
| Trustworthy finite-stream completion | New optional [finite_answer_stream.py](../assets/finite_answer_stream.py) and adversarial tests | `manuscript-review/evidence/part2/stream_consumer_probe.py` and retained JSON reproduced false acceptance of thought/error/truncated text. Updated manuscript supplies the stronger contract; the new component is independently implemented and tested, not a claim that the hosted client uses it. |
| Buffer failure and persistence races | New [runtime-verification.md](runtime-verification.md) controlled-interleaving matrix and failure diagnosis | `agent-runtime/examples/backpressure.py:45–55` swallowed a processor TimeoutError as idle polling; `selective_persistence.py:24–39` cleared newer input after an awaited write. Both defects were reproduced offline during this review; original examples were left unchanged. |
| Memory ingestion at exact acknowledgement boundaries | Retained [state/streams](runtime-state-and-streams.md); added cursor/operation fault sequence | `agent-runtime/examples/memory_callbacks.py:10–30` uses fixed slices and awaited mock writes. Durable outbox, cursor, deduplication and terminal ingestion are production contracts, not hosted evidence. |
| Deferred job acceptance and continuation | Added distinct acceptance/worker/continuation test recipe | `agent-runtime/long_running_demo.py`, updated manuscript job section. Dictionary/thread simulation and done-only polling do not establish durable workers; original call ID/name, authorised job state and complete resumed answer need separate checks. |
| Actual source generation and serialized deployment settings | New archive/spec/effective-state evidence chain | `agent-runtime/owned_runtime.py:155–168,222–258`, `tests/fake_runtime_provider.py`, `tests/test_lifecycle.py:314–395`; preparation report. Retained offline tests ran actual ADK generator and Vertex serializer with transports substituted, including the inline archive. |
| Preflight identity and supported retry scope | Added availability-versus-identity/quota/access distinction and recovery table | `agent-runtime/preflight.sh:41–80`, lifecycle tests, preparation/live reports. ADC token availability is narrower than a verified identity/quota match; API-list failure means unknown. Completed setup verifies rather than silently updating changed source. |
| Accepted operation and cleanup repair | Retained lifecycle rules with concrete state-to-action cases | `AGENT-RUNTIME-PREPARATION-2026-09-14.md`, `AGENT-RUNTIME-LIVE-RESULTS-2026-09-14.md`, `tests/test_owned_guards.py`. The regional DELETE was reconciled without replay; private SDK interception and provider-managed retention are explicit limitations. |
| Runtime sizing, placement, model controls and capacity options | Retained [agent-runtime.md](agent-runtime.md); no fabricated performance numbers or commercial defaults added | Updated manuscript final sections, `examples/{resource_sizing,model_controls,model_retry}.py`. Arithmetic, mock model IDs and synchronous retry demonstrations do not verify capacity, live model availability or in-flight async deadlines. Actual whole-container load and current provider terms remain separate checks. |

The stream asset is a new optional implementation of decoded single-invocation
answer acceptance. It has no transport, credentials, model invocation, tool-result
semantic validator or durable job/store. Its strict STOP policy and teaching limits
must match the target adapter. It never makes previews authoritative or proves
browser delivery. Tests include real ADK event JSON shapes alongside synthetic
error, timeout, cancellation and cleanup cases. The token tests use real SDK
orchestration with deterministic models and synthetic usage only.

Official references consulted for this refinement were ADK context compaction,
the Agent Runtime deployment guide, Python 3.11 cache semantics and asyncio
exceptions. They support the linked contract explanations; pinned implementation
tests and retained campaign records determine the historical claims. No new
cloud or model campaign was run.

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

## Part 3 depth review: coverage and additions

Rechecked on 16 September 2026 against the updated Part 3 manuscript, its original
comparison, the current GKE implementation/examples/tests, every provisioning
attempt and final cleanup records. Paths below are maintainer locators beneath
`chapter-04-cloud-optimization/`, not dependencies of the installed skill.

| Knowledge carried into the skill | Destination and refinement | Source and evidence boundary |
| --- | --- | --- |
| Actual release versus reference YAML | Retained GKE modes; added [deployment troubleshooting](gke-deployment-troubleshooting.md) and [verification](gke-verification.md) | `gke/owned_lab.py:119–129,412–454`, Dockerfile, renderer tests and updated manuscript §§0–4. Source staging and Docker copy are two separate inclusion boundaries; no HPA/PDB/edge was added to the verified lab. |
| Server configuration and service reuse | New [application integration](gke-application-integration.md) | `gke/app.py:24–34`, `tests/test_managed_sessions.py:20–41`, `examples/{client_reuse,session_service_lifecycle}.py`. Import-time settings and actual request dependencies matter; helper caching alone does not prove server reuse. |
| Factory configuration and lifecycle composition | New real-factory test and qualified PostgreSQL guidance | Installed ADK 2.8 `cli/fast_api.py` and `cli/api_server.py`; `tests/test_gke_http_contract.py`. The factory supports `session_db_kwargs`; its supplied lifespan exits before cached Runner closure. A second service is not automatically wired, and early service disposal can precede a later flush. |
| Session storage work versus returned history | New [session contracts](../tests/test_gke_session_contract.py) and serving caveat | Updated manuscript history section; actual ADK database/Vertex adapters. SQLite applies SQL LIMIT; the managed adapter consumes its doubled API iterator before a positive slice. Zero skips event retrieval. Full storage and state remain intact. The raw slice can split a tool pair; downstream model repair is not tested. |
| Runner flush versus engine disposal | Real SDK/SQLite observation and explicit lifecycle ownership | Updated manuscript lifecycle component; actual `Runner.close` and `DatabaseSessionService.close`. Separate calls cause flush then engine disposal; no PostgreSQL pool, migration, network timeout or production drain claim. |
| API creation, app/author identities and streaming | New [HTTP contracts](../tests/test_gke_http_contract.py) | `gke/tests/test_application_http.py:50–76`; actual ADK factory with a deterministic model. Explicit-ID and collection payloads differ; missing/false streaming gives no partials, true reaches the stream boundary, and an error can follow HTTP 200. TestClient is not browser/network timing evidence. |
| Credential startup and readiness | Retained probe/resource guidance; added actual-client integration sequence | `examples/credential_startup.py:11–36`, runtime-example tests, optional metadata patch. Demonstration retries and a separate init token wait do not prepare ADK's own client or bound a stalled network refresh. No startup asset or new remote warm-up was imposed. |
| Native and custom trace privacy | New actual-native in-memory-export negative control | `gke/tests/test_telemetry.py`, `examples/request_timing.py`, original Part 3 telemetry probe, new session contract. UI consent with telemetry disabled is separate; flags still permit `gen_ai.conversation.id`. Existing custom-span safety does not sanitise native/parent spans or logs. |
| Complete output versus narration | Strengthened shared [saved-run checker](../scripts/check_run.py) and three regressions | `gke/scripts/validate_smoke.py` accepts a synthetic mismatched call/result plus partial-only text. The skill checker initially also accepted text with a code-execution result; repaired to reject unsupported non-null Part protocols, including late activity. Independent review also exposed nested function-response media and continuation fields; these and partial/scheduled protocols now fail explicitly. Actual SDK serialisation covers code-result and nested-response counterexamples. Original companion unchanged. |
| Provider contract failures before capacity | Deployment symptom/recovery table and precise chronology | `GKE-PREPARATION-2026-09-14.md`, `GKE-LIVE-RESULTS-2026-09-14.md`, `GKE-REPAIR-LIVE-RESULTS-2026-09-14.md`, owned-lab tests. The first failure was a Storage collection path; the next exposed Cluster-versus-Operation response handling before an accepted create later failed for capacity. |
| Exact grants and independent identities | Scoped six-grant diagnostic table | `GKE-RETRY-CAMPAIGN-2026-09-14.md:44`, `gke/owned_lab.py:315`, final live report. Build, node and direct KSA identities differ; conditional grants and changed etags need correct interpretation. Lab roles are historical evidence, not a universal production policy. |
| Completed setup verifies; it does not update | Added source/spec/UID/grant contract and failure recipes | `gke/owned_lab.py:425`, `tests/test_owned_lab.py:85–129`. Interrupted setup and changed source are distinct from a matching completed repeat. No claim of automatic repair or resumable release updates. |
| Accepted-operation and partial-cleanup recovery | Added receipt fields and observed wire-shape lessons | `gke/owned_lab.py:208`, owned-lab tests 132–249, repair and cleanup reports. Strict operation attribution, definite rejection versus uncertainty, deleted-account inventory fallback and network-delete reconciliation preserve owned state without replay. |
| Final retry, continuity and cleanup scope | Retained functional PASS with exact production exclusions | `GKE-RETRY-LIVE-RESULTS-2026-09-14.md`, `CLEANUP-CONFIRMATION-2026-09-15.md`. Five submissions/nine generations, same-region successful provisioning, events retained through replacement UID, all owned cleanup. Two Ready Pods on one node are not node/zone resilience; soft deletion/provider history can remain. |
| Resources, HPA/VPA, public edge, drain and advanced options | Retained conditional designs; added implementation-to-evidence matrix | Updated manuscript sizing, autoscaling, Gateway/IAP, shutdown, advanced-feature and rollback sections. These remain target production choices, not mandatory additions or newly verified live capabilities. |

The manuscript's statement that earlier attempts failed for capacity reasons is
an incomplete description of the first Storage failure and subsequent response
parser defect. The new deployment reference preserves the full sequence; the
manuscript itself was not edited. The companion smoke-validator counterexample is
also documented as a separate limitation, not a retraction of the recorded
successful live answers.

No new asset was needed: existing observation and finite-answer components remain
conditional options. The new package tests retain actual SDK/SQL/HTTP behaviour
while replacing external effects. Current primary documentation was consulted
for Deployment termination overlap, Workload Identity principal composition,
Storage bucket insertion and session concepts; exact SDK observations remain
versioned local evidence. No cloud account or model API was accessed.
