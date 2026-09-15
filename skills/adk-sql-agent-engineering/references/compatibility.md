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

The source is the MIT-licensed `RuslanKhis/agentic-engineering-adk-gcp` repository, Chapter 10. The implementation files were re-opened on 15 September 2026; all 44 files matched the final 13 September follow-up fingerprints. Source path names below are provenance identifiers, not dependencies or links the installed skill must resolve.

| Skill behaviour | Working source and prior finding | Evidence and limit |
| --- | --- | --- |
| Route complete intents; bind reviewed values | `intelligent_sql_agent/router_agent.py:19`, `query_templates.py:31`, `fast_path.py:31`; `tests/test_query_execution.py` | LIVE reviewed answers 6/6; OFFLINE hostile-value binding. Semantic routing instructions are not a deterministic proof of equivalence. |
| Validate selection; resolve values; retrieve only relevant schemas | `context_agent.py:31`, `schema_tools.py:53`, `value_tools.py`; `tests/test_context_latency.py` | LIVE generated answers used two model calls; OFFLINE dynamic selection, metadata change, ambiguous/cross-scope/failing context. No full caller-specific schema policy. |
| Tool-free author and wire/runtime schema split | `models.py:63`, `sql_author_agent.py:47`; `tests/test_sql_author_contract.py` | OFFLINE actual SDK serialisation with HTTP double; LIVE no missing-SQL rejection in six generated samples. Not universal SQL correctness. |
| Shared deterministic execution | `query_runner.py:27`, `query_runner.py:148`; `tests/test_query_policy.py`, `tests/test_query_execution.py` | OFFLINE implemented AST/scope/cost/timeout boundaries; LIVE BigQuery results. Limited sandbox, separate call timeouts and row cap only. |
| Grain-aware exact outcome checks | `scripts/smoke_test.py:35`, `tests/test_smoke_answer_aliases.py`; manuscript section 10.5 correction | LIVE exact captured results; OFFLINE replay and alias regressions. Corrected ticket field names and added missing total; repeated-final-renewal invariant remains a production requirement. |
| Public graph and refusal trajectory | `agent.py:64`, `tests/test_workflow.py`, `tests/test_http.py` | LIVE two no-query refusals and browser history after restart; OFFLINE Runner/HTTP tests. Persisted history is not a follow-up resolver. |
| Scope, output and deadline improvements | Manuscript sections 10.7–10.9 and 15 September manuscript comparison | PRODUCTION PRINCIPLE: authenticated scope, exact retrieved-schema binding, full parameter inventory, stricter parser policy, cumulative deadline, response bytes/completeness and true freshness. |
| Idempotent setup, identity readiness and owned cleanup | `scripts/setup_bigquery.py`, `runtime_identity.py`, `cleanup_bigquery.py`; lifecycle/runtime tests | LIVE repeated provisioning/deletion, effective identity, narrowly bounded IAM propagation retry and owned absence. Fresh-project API activation and live timeout recovery NOT RUN. |

`check_results.py` adapts the explicit-alias/exact-decimal lesson from the source smoke checker into a generic local contract; its new input validation is tested locally. `inspect_project.py` is new read-only inspection tooling implementing the prerequisite and version-preservation workflow. Neither helper is copied cloud provisioning code. The included MIT [licence](../LICENSE) preserves the source notice.

## Evidence that must stay separate

- **Recorded live:** 13 September follow-up, six correct browser answers per route and two unsupported no-query refusals. Two raw browser flags and the CLI's original failure remained recorded; exact captured answers passed after justified alias-checker corrections. Generated samples used two model calls each.
- **Recorded offline:** final companion suite, 178 tests passed with 41 warnings. Model/database/HTTP doubles validate their boundaries, not live service operation. The printed corrected chapter SQL separately passed an offline fixture replay on 15 September.
- **Not established:** universal parameterisation of generated SQL (one of six candidates used literal dates), complete SQL sandboxing, latency SLA, live timeout recovery, fresh-project API activation, tenant isolation, semantic follow-ups, repair, caches, managed data-agent/MCP branches or production analytics export.
- **New skill validation:** see [verification-record.md](verification-record.md); no fresh live cloud campaign is implied.

The historical sub-five-second and approximately 80% fast-path anecdotes from another system are excluded from the skill's acceptance claims. No public book URL was available in the source, so no publication link is invented. This community project is independent of Google.
