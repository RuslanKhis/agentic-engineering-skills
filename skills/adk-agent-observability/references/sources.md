# Sources

Every claim in this skill is one of: **source-verified** (read in a local checkout of google/adk-python on 2026-10-07), **documented behaviour** (adk-docs with the page date), **vendor guidance** (Google Cloud or another provider's documentation with the date printed on the page or the fetch date), **independent evidence**, or **community** (issue or forum reports, not reproduced). [Compatibility](compatibility.md) lists what was not verified.

## ADK source and changelog

| Reference | Type | Notes |
| --- | --- | --- |
| google/adk-python tag `v2.8.0` (2026-08-25): `telemetry/context.py`, `_schema_version.py`, `_stable_semconv.py`, `_experimental_semconv.py`, `_metrics.py`, `_token_usage.py`, `_instrumentation.py`, `tracing.py`, `node_tracing.py`, `setup.py`, `google_cloud.py`, `_agent_engine.py`, `_agent_engine_metric_exporter.py`, `_adk_attributes.py`; `plugins/bigquery_agent_analytics_plugin.py`, `logging_plugin.py`, `debug_logging_plugin.py`, `auto_tracing_plugin.py`; `evaluation/eval_set.py`, `eval_case.py`, `common.py`, `local_eval_sets_manager.py`, `request_intercepter_plugin.py`; `events/event.py`, `models/llm_response.py`, `models/lite_llm.py`, `flows/llm_flows/functions.py`, `tools/mcp_tool/mcp_tool.py`, `tools/openapi_tool/openapi_spec_parser/rest_api_tool.py`, `cli/cli_deploy.py`, `agents/run_config.py` | source-verified | Pinned behaviour |
| google/adk-python main at 2.11.0 (2026-10-01): `telemetry/context.py` (`ADK_EXPERIMENTAL_TELEMETRY_FEATURES`), `telemetry/google_cloud.py` (`gcp.resource_type`), `CHANGELOG.md` | source-verified | Later behaviour, labelled by version |
| google/adk-docs: `docs/observability/index.md`, `traces.md` (2026-08-07), `metrics.md` (2026-09-18), `logging.md` (2026-09-21), `docs/integrations/bigquery-agent-analytics.md` (2026-10-05), `cloud-trace.md`, `langfuse.md`, `phoenix.md`, `arize-ax.md`, `weave.md`, `mlflow-tracing.md`, `docs/evaluate/index.md` | documented behaviour, fetched 2026-10-07 | Span and metric tables, export setup, plugin configuration, eval set format |

## Google Cloud and OpenTelemetry

| URL | Date | Used for |
| --- | --- | --- |
| https://github.com/open-telemetry/semantic-conventions-genai (agent spans, metrics, registry) | 2026-10-05 | Development status, span and attribute names, Opt-In content attributes, token usage metric naming |
| https://docs.cloud.google.com/stackdriver/docs/instrumentation/ai-agent-adk | 2026-09-30 | APIs, writer roles, `EVENT_ONLY` guidance, invalid `true` under latest semconv |
| https://docs.cloud.google.com/stackdriver/docs/otlp/overview | fetched 2026-10-07 | Telemetry API OTLP ingestion, quota project header, billing as Prometheus samples |
| https://docs.cloud.google.com/trace/docs/quotas | fetched 2026-10-07 | Span attribute, name, event and retention limits |
| https://docs.cloud.google.com/monitoring/quotas | fetched 2026-10-07 | Custom metric descriptor, label, series and retention limits |
| https://docs.cloud.google.com/trace/docs/troubleshooting | fetched 2026-10-07 | Export troubleshooting (also cited by optimise-adk-on-google-cloud) |
| https://docs.cloud.google.com/logging/docs/structured-logging | fetched 2026-10-07 | `logging.googleapis.com/trace`, `spanId`, `trace_sampled` |
| https://docs.cloud.google.com/agent-builder/agent-engine/manage/tracing | 2026-10-01 | `GOOGLE_CLOUD_AGENT_ENGINE_ENABLE_TELEMETRY`, required APIs, optional semconv and capture settings, legacy `roles/cloudtrace.agent` |
| https://docs.cloud.google.com/gemini-enterprise-agent-platform/scale/runtime/monitoring | 2026-10-01 | `ReasoningEngine` resource, built-in metrics, overview dashboard, ADK metrics as user-defined metrics |
| https://docs.cloud.google.com/agent-builder/agent-engine/manage/logging | fetched 2026-10-07 | `reasoning_engine_stdout`, child resources not logged |
| https://developers.googleblog.com/en/agent-and-model-evaluations-in-gemini-enterprise-agent-platform-are-now-ga/ | 2026-07-31 | Online Monitors GA |
| https://docs.cloud.google.com/gemini-enterprise-agent-platform/optimize/evaluation/quality-alerts | 2026-10-01 | `online_evaluator/scores`, `evaluation_metric_name`, alert example, incidents linking to traces |
| https://cloud.google.com/bigquery/pricing#data-ingestion-pricing | fetched 2026-10-07 | Storage Write API billing |

## Other vendor documentation

| URL | Date | Used for |
| --- | --- | --- |
| https://github.com/google/agents-cli/blob/main/skills/google-agents-cli-observability/SKILL.md (v1.8.0) and `feedback-mechanism.md` | 2026-09-30 | Completion upload path ignoring the content flag, infrastructure command, feedback record and sink pattern |
| https://langfuse.com/docs/evaluation/evaluation-methods/llm-as-a-judge | fetched 2026-10-07 | Judges on sampled traces |
| https://langfuse.com/docs/observability/features/masking | fetched 2026-10-07 | `mask_otel_spans` scope |
| https://www.arize.com/docs/ax/evaluate/run-evals-on-traces.md | fetched 2026-10-07 | Evaluations over traces |

## Independent evidence

| Work | Finding used |
| --- | --- |
| Google SRE Workbook, "Implementing SLOs" (https://sre.google/workbook/implementing-slos/) | SLIs as good/total ratios, targets below 100 percent, multiwindow burn-rate alerting |

## Community reports (not reproduced)

google/adk-python issues #7311 (`AuthCredential` fields in tool-call span attributes; `off` does not disable content), #7162 (REST tool keys in args, fixed), #7112 (MCP `isError` rows as `TOOL_COMPLETED`, open), #7024 (service-account key ADC `invalid_scope` on export), #7017 (view DDL per request, fixed 2.10.0), #6915 and #6692 (span retention growth, fixed 2.10.0), #6465 (duplicate BigQuery rows before `event_id`), #6361 (`user.id` dropped with old genai instrumentor), #6328 (mTLS tracing 401, fixed infrastructure-side), #4829 (thinking tokens absent, fixed), #3845 (camelCase credential keys not redacted), #3181 (LiteLLM streaming usage); Arize-ai/openinference issues #3857, #3844, #3177 and an Arize community thread (2026-02-20) on duplicate or orphan spans beside native ADK spans. They are listed as symptoms to test for on the target.

## Repository references

Sibling skills are cited by name: protect-adk-sensitive-data (content policy and capture baseline in `references/implementation-recipes.md`), optimise-adk-on-google-cloud (`references/gke-serving.md`, `assets/session_observation.py`), adk-agent-evaluation (`references/execution-evidence.md` usage-counting rule, evaluation design), deploy-adk-on-google-cloud (first deployment), adk-operational-guardrails (budgets and loop limits), adk-model-and-output-contracts (finish reasons, failover), adk-frontend-integration and adk-tool-auth-and-secrets (feedback endpoint and identity). Google's `google-agents-cli-observability` skill is an optional composition per `docs/integrations/agents-cli.md`.
