# Compatibility and evidence

## Version handling

Inspect the target's declared Python range, ADK pin, lockfile and selected interpreter before editing. Preserve package manager and versions. A dependency snapshot from another project is evidence, not a lockfile to impose on the target.

The recorded companion environment was Python **3.11.4**, `google-adk` **2.8.0**, `google-genai` **2.23.0**, `google-cloud-bigquery` **3.45.0**, `google-api-core` **2.34.0**, `google-auth` **2.58.0**, `pydantic` **2.13.5**, `sqlglot` **29.0.1**, `pytest` **9.1.1**, `python-dotenv` **1.2.3**, `fastapi` **0.141.1**, `starlette` **1.6.0**, `httpx` **0.28.1**, and `uvicorn` **0.52.4**. ADK was exactly pinned; several other dependencies were declared as ranges. Python 3.12/3.13 support in the companion README was not a completed interpreter test matrix.

Live verification on 13 September 2026 used Gemini `gemini-3.5-flash` through Vertex AI's global endpoint and BigQuery in `US`. Router configuration was MINIMAL thinking/1,000 output tokens; author LOW/8,192. These are historical tested settings, not mandated models, current availability claims or a recommendation to change the target's configuration.

The skill's two read-only helpers are framework-independent standard-library Python. The inspector's no-follow directory scan requires POSIX file-descriptor support; unsupported platforms return a clear error and should use the manual inspection workflow. Their tests do not import ADK or authenticate to Google Cloud. Their exact tested interpreter and agent environment appear in [verification-record.md](verification-record.md). No behavioural portability claim is made for an agent product or OS not tested there.

For another ADK/SDK version, inspect installed callback, workflow, output-schema and event APIs; use official versioned documentation if source is insufficient. Test actual outbound serialisation and READY/refusal round trips. If the needed API is missing or the contract fails, stop that implementation path with the exact mismatch. Preserve the project's pin and offer a compatible adaptation or a separately approved dependency change. Unknown compatibility is not a proven incompatibility, but it is not a pass.

`inspect_project.py --expect-adk 2.8.0` is an optional strict gate for reproducing that baseline. It reports unresolved or conflicting declarations/installed versions rather than claiming the whole environment is compatible. Lockfile presence alone is not a resolved-version check; inspect the actual target lock with its tooling.

Both helpers reject symbolic links in their input path components. Use a canonical real directory/file path when an operating system exposes a location through a symlink. This is an input boundary, not a reason to copy credentials or broaden access. The inspector reads only supported manifests and example variable names; source-file names are inventory leads and source contents still require manual review.

## Provenance map

The source is the MIT-licensed `RuslanKhis/agentic-engineering-adk-gcp` repository, Chapter 10. The implementation was re-opened on 15 September and reviewed again on 16 September 2026 with the updated manuscript and dated audit records. The 15 September check found all 44 source files matching the final 13 September follow-up fingerprints. Source path names below are provenance identifiers, not dependencies or links the installed skill must resolve.

| Skill behaviour | Working source and prior finding | Evidence and limit |
| --- | --- | --- |
| Route complete intents; bind reviewed values | `intelligent_sql_agent/router_agent.py:19`, `query_templates.py:31`, `fast_path.py:31`; `tests/test_query_execution.py` | LIVE reviewed answers 6/6; OFFLINE hostile-value binding. Semantic routing instructions are not a deterministic proof of equivalence. |
| Validate selection; resolve values; retrieve only relevant schemas | `context_agent.py:31`, `schema_tools.py:53`, `value_tools.py`; `tests/test_context_latency.py` | LIVE generated answers used two model calls; OFFLINE dynamic selection, a changed-description sentinel, ambiguous/cross-scope/failing context. No full caller-specific schema policy or tested column-removal/type-drift handling. |
| Tool-free author and wire/runtime schema split | `models.py:63`, `sql_author_agent.py:47`; `tests/test_sql_author_contract.py` | OFFLINE actual SDK serialisation with HTTP double; LIVE no missing-SQL rejection in six generated samples. Not universal SQL correctness. |
| Shared deterministic execution | `query_runner.py:27`, `query_runner.py:148`; `tests/test_query_policy.py`, `tests/test_query_execution.py` | OFFLINE implemented AST/scope/cost/timeout boundaries; LIVE BigQuery results. Limited sandbox, separate call timeouts and row cap only. |
| Grain-aware exact outcome checks | `scripts/smoke_test.py:35`, `tests/test_smoke_answer_aliases.py`; manuscript section 10.5 correction | LIVE exact captured results; OFFLINE replay and alias regressions. Corrected ticket field names and added missing total; repeated-final-renewal invariant remains a production requirement. |
| Public graph and refusal trajectory | `agent.py:64`, `tests/test_workflow.py`, `tests/test_http.py` | LIVE two no-query refusals and browser history after restart; OFFLINE Runner/HTTP tests. Persisted history is not a follow-up resolver. |
| Scope, output and deadline improvements | Manuscript sections 10.7–10.9 and 15 September manuscript comparison | PRODUCTION PRINCIPLE: authenticated scope, exact retrieved-schema binding, full parameter inventory, stricter parser policy, cumulative deadline, response bytes/completeness and true freshness. |
| Idempotent setup, identity readiness and owned cleanup | `scripts/setup_bigquery.py`, `runtime_identity.py`, `cleanup_bigquery.py`; lifecycle/runtime tests | LIVE repeated provisioning/deletion, effective identity, narrowly bounded IAM propagation retry and owned absence. Fresh-project API activation and live timeout recovery NOT RUN. |

`check_results.py` adapts the explicit-alias/exact-decimal lesson from the source smoke checker into a generic local contract; its new input validation is tested locally. `inspect_project.py` is new read-only inspection tooling implementing the prerequisite and version-preservation workflow. Neither helper is copied cloud provisioning code. The included MIT [licence](../LICENSE) preserves the source notice.

## Evidence that must stay separate

- **Recorded live:** 13 September follow-up, six correct browser answers per route and two unsupported no-query refusals. Two raw browser flags and the CLI's original failure remained recorded; exact captured answers passed after justified alias-checker corrections. Generated samples used two model calls each.
- **Recorded failed gate:** that follow-up retained an overall scoped FAIL for first-answer responsiveness. All five warm generated first answers and one of five warm reviewed first answers missed the agreed five-second limit; generated warm final median was 14.1667 seconds. Correctness and call-count improvements did not satisfy that gate. This is historical evidence, not a requirement to optimise every future implementation for that threshold.
- **Recorded offline:** final companion suite, 178 tests passed with 41 warnings. Model/database/HTTP doubles validate their boundaries, not live service operation. The printed corrected chapter SQL separately passed an offline fixture replay on 15 September.
- **Not established:** universal parameterisation of generated SQL (one of six candidates used literal dates), complete SQL sandboxing, latency SLA, live timeout recovery, fresh-project API activation, tenant isolation, semantic follow-ups, repair, caches, managed data-agent/MCP branches or production analytics export.
- **New skill validation:** see [verification-record.md](verification-record.md); no fresh live cloud campaign is implied.

The historical sub-five-second and approximately 80% fast-path anecdotes from another system are excluded from the skill's acceptance claims. No public book URL was available in the source, so no publication link is invented. This community project is independent of Google.

## Depth-review coverage

The 16 September review converted useful reasoning and failure recovery into conditional implementation references. It did not copy every manuscript example or promote advice into tested companion behaviour.

| Source topic | Where the skill makes it actionable | Evidence boundary |
| --- | --- | --- |
| Manuscript 10.1–10.2: context growth and two paths | [Implementation](implementation.md), [acceptance](acceptance-and-extensions.md) | Historical two-call generated graph; scaling experiments are proposed tests. |
| 10.3: complete template meaning, routing, typed values | [Implementation](implementation.md), [semantic contracts](semantic-contracts.md) | Reviewed answers and hostile-value regressions verified; stronger periods/ties require explicit metric changes. |
| 10.4: authored semantics, value dictionaries, live schemas | [Semantic contracts](semantic-contracts.md) | Resolver/collector tested; alias-collision detection, nested schema support and access-aware dynamic lookups are extensions. |
| 10.5: denominators, preaggregation, zero-activity entities | [Semantic contracts](semantic-contracts.md), [validation](validation.md) | Exact fixture metrics verified; historical cohort rules, uniqueness and full join-policy enforcement are separate obligations. |
| 10.6: graph, tool ownership, events, trusted state | [ADK runtime](adk-runtime.md), [acceptance](acceptance-and-extensions.md) | Companion graph tested; caller-owned invocation scope and managed branches are extensions. |
| 10.7: parser, parameters, costs, repair and output | [Execution safety](execution-safety.md), [troubleshooting](troubleshooting.md) | Limited executor verified; full sandbox, repair, cumulative budgets and completeness remain extensions. |
| 10.8: follow-ups | [Acceptance and extensions](acceptance-and-extensions.md) | Concrete selection-versus-presentation and pinned-interval tests; semantic follow-up implementation NOT RUN. |
| 10.9: boundary evaluation, telemetry and template promotion | [Acceptance](acceptance-and-extensions.md), [troubleshooting](troubleshooting.md) | Exact-response replay verified; exporter controls and trace-to-template process are production principles. |
| 10.10–10.12: failure modes, actual changes, implementation checklist | [Troubleshooting](troubleshooting.md), the entrypoint and this evidence map | Each recommendation retains its narrower evidence label. |
| 11 September audit: plan caused writes; eager imports; permissive ownership; duplicate loads | [Lifecycle runbook](lifecycle-runbook.md), [ADK runtime](adk-runtime.md) | Public command/import regressions; stable journal and owned operations. No claim that helper-function tests alone prove a safe CLI. |
| 11 September audit: qualified AI/ML functions, whitespace, non-finite numbers, misleading smoke PASS | [Troubleshooting](troubleshooting.md), [acceptance](acceptance-and-extensions.md) | Concrete negative controls; no general-purpose parser copied as a sandbox. |
| 13 September preflight: old project/quota, billing API uncertainty | [Lifecycle runbook](lifecycle-runbook.md) | Actual access/billing/consumer distinction; fresh-project activation NOT RUN. |
| 13 September live campaign: accepted interrupted load, identity, stale deletion visibility | [Lifecycle runbook](lifecycle-runbook.md) | Accepted load was DONE on inspection; pending-load recovery and corrected stale-delete branches have separate offline evidence. |
| 13 September follow-up: wire fields, exact metadata, two calls, IAM propagation, alias adjudication | [ADK runtime](adk-runtime.md), [lifecycle](lifecycle-runbook.md), [validation](validation.md) | Recorded live/offline evidence, failed latency gate and original verdicts preserved. |
| 15 September broader cleanup: authoritative inventory, retained/hidden state, empty RAG backend | [Lifecycle runbook](lifecycle-runbook.md) | Separate historical operation. Routine SQL setup creates no VM, RAG backend or hosted frontend; no universal zero-cost claim. |

One useful limit found during review: the companion's offline demo and independent fixture verifier directly joined two fact aggregates while the authored semantic map listed dimension-to-fact relationships. Matching fixture totals therefore did not demonstrate enforcement of that map's approved joins. The skill requires separate relationship/cardinality assertions; it does not silently modify the source or claim all semantic controls were implemented.

## Portable ADK asset versus historical environment

The optional [offline contract asset](../assets/test_adk_contract.py) is adapted from the companion's real SDK-boundary test pattern. It bundles synthetic fixtures and requires no companion import. Its current execution results and exact environment are recorded separately in [verification-record.md](verification-record.md).

The environment available for the 16 September package work has Python 3.11.4, ADK 2.8.0, GenAI 2.19.0, Pydantic 2.13.4 and google-auth 2.57.0. These differ from the historical live stack above. Running an offline asset there neither reruns the old live campaign nor establishes the whole application on that alternative stack. Dependencies were preserved; do not install these versions merely to satisfy an example.

The asset intentionally uses the version-sensitive private GenAI `client._api_client.async_request` seam to retain real serialisation while replacing external HTTP. Recheck that seam on upgrades. An assertion/import mismatch is a compatibility finding, not a reason to weaken the probe. A synthetic successful response says nothing about live model quality, SQL policy, IAM, model availability or a target's own graph.
