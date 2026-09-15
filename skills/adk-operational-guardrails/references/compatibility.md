# Compatibility and version gates

Read before adopting an ADK-specific API, selecting a dependency version or claiming a tested integration.

## Evidence baselines

| Scope | Exact baseline | What it establishes |
| --- | --- | --- |
| Historical companion offline + local live model/browser verification, 13 September 2026 | Python 3.11.4, macOS arm64; `google-adk==2.8.0`, `google-genai==2.23.0`, `google-cloud-pubsub==2.39.0`, `google-api-python-client==2.197.0` | The bounded local behaviours described in [evidence](evidence.md); not a cloud deployment |
| Skill helper/template and fixture checks | See [validation results](validation-results.md) for commands, date and exact installed versions | Only the checks actually recorded there; no newly executed live campaign |

The companion declares ADK, Pub/Sub and API client pins but does not pin the transitive `google-genai` version. Therefore the same requirements file can resolve a different environment. Do not silently treat historical and current installed versions as equivalent.

The standalone inspector and invocation guard use Python's standard library. Their supported/tested baseline is Python 3.11.4; the guard uses Python 3.11 asynchronous timeout facilities. Other runtimes require validation rather than a claim of automatic compatibility. The core Markdown requires no coding-agent vendor, connector or book checkout. Only environments actually exercised in validation results are claimed as smoke-tested.

Inspector exit codes: **0** means inventory completed within its stated scope, **1** means an incomplete inventory or an explicitly requested ADK mismatch, and **2** means invalid arguments/path. Missing ADK is reported as absent unless `--require-adk` requested a specific version. The bounded scan skips hidden/dependency directories and symlinks, reports selected version constraints and source identifier hints, and inventories lockfile presence without resolving locks. Complex dependency markers/includes, unreadable files or large trees require manual follow-up; a successful exit is never a guardrail verdict.

## Adapt without changing the target's pins

1. Inspect the target's Python constraint, active interpreter, dependency files and lock. Read only relevant version metadata; do not print environment values. The inspector reports installed versions from its own interpreter, which may not be the target environment unless invoked with that interpreter.
2. Preserve the target package manager and dependency declarations. For an absent environment, state missing prerequisites and continue static design/tests that need no external packages. Installation is not an implicit upgrade decision.
3. For ADK 2.8.0, retain the tested boundary contract and use fake-model integration tests. For another version, inspect its installed source and matching official version documentation, adapt narrowly, and prove tool dispatch, model exhaustion, event/usage semantics and iterator cleanup offline. If an API is absent or incompatible, stop that integration with an explicit incompatibility result; provide a version-compatible design rather than silently modifying pins.
4. Recheck current model IDs, lifecycle, location and provider prices before paid tests. The historical models (`gemini-2.5-pro`, `gemini-3.5-flash`) are provenance, not defaults or current recommendations.

Version-sensitive surfaces include `Runner.run_async`, `RunConfig.max_llm_calls`, function-call/response IDs, parallel and partial events, model usage metadata, callback/plugin timing, resumption and session storage. The historical live harness also instruments an ADK-cached model client; this skill does not copy that private coupling into a general-purpose runtime.

Official references, checked 15 September 2026: [ADK 2.8.0 RunConfig](https://raw.githubusercontent.com/google/adk-python/v2.8.0/src/google/adk/agents/run_config.py), [Tool Confirmation](https://adk.dev/tools-custom/confirmation/), [Cloud Billing spend caps](https://docs.cloud.google.com/billing/docs/how-to/budgets-spend-caps). Reopen the relevant official source when an implementation depends on a changing provider feature.
