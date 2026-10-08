# Compatibility and evidence boundaries

Read before relying on any version-dependent name or behaviour in this skill. The pinned reference is google-adk **2.8.0** (tag `v2.8.0`, released 2026-08-25), whose source was read on 2026-10-07. Later behaviour comes from the adk-python main branch at 2.11.0 and its CHANGELOG, labelled by release. Keep the target's pins; a version decision is a separate request.

## Verified in 2.8.0 source

| Surface | Behaviour | File |
| --- | --- | --- |
| `TelemetryConfig` | Reads `OTEL_SEMCONV_STABILITY_OPT_IN`, `OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT` (four modes; `true`/`1` as `EVENT_ONLY`; unknown as `NO_CONTENT`), `ADK_CAPTURE_MESSAGE_CONTENT_IN_SPANS` (default on; off only for `false`/`0`), `ADK_EXPERIMENTAL_TELEMETRY`, `ADK_TELEMETRY_IGNORE_RUN_CONFIG` once at construction; fields `genai_semconv_stability_opt_in`, `capture_message_content`, `adk_experimental_telemetry_opt_in` | `telemetry/context.py` |
| `RunConfig.telemetry` | Optional `TelemetryConfig` honoured at the runner's invocation span (2.8.0 CHANGELOG) | `agents/run_config.py` |
| Schema version | `ADK_TELEMETRY_SCHEMA_VERSION_OPT_IN` `1`/`2`; default `2` only when `GOOGLE_CLOUD_AGENT_ENGINE_ID` is set; v1 emits `invocation`, v2 emits `invoke_workflow {entrypoint}` | `telemetry/_schema_version.py`, `_instrumentation.py` |
| Spans | `invoke_agent {name}`, `execute_tool {name}`, `generate_content {model}` (native) with the attributes listed in [signals and schema](signals-and-schema.md); `error.type` and `ERROR` status on dict-reported tool errors via `_detect_error_in_response` (`MCP_TOOL_ERROR`, `HTTP_ERROR`) | `telemetry/tracing.py`, `_instrumentation.py`, `tools/mcp_tool/mcp_tool.py`, `tools/openapi_tool/.../rest_api_tool.py` |
| Instrumentor hand-off | When `opentelemetry-instrumentation-google-genai` wraps `Models.generate_content` and the agent is Gemini-backed, ADK adds extra attributes to the library's span and skips its own client metrics | `telemetry/tracing.py` |
| Metrics | Names, units, buckets and gates in [signals and schema](signals-and-schema.md); meter `gcp.vertex.agent`; experimental token accumulation only under the opt-in | `telemetry/_metrics.py`, `_instrumentation.py` |
| Token arithmetic | newest cumulative report per call; input = prompt + tool-use prompt; output = candidates + thoughts; total derived | `telemetry/_token_usage.py` |
| Exporters | `maybe_set_otel_providers` never overrides an existing provider; generic OTLP exporters from `OTEL_EXPORTER_OTLP_*ENDPOINT`; GCP traces and metrics by OTLP HTTP to `telemetry.googleapis.com`; logs via `CloudLoggingExporter` (`adk-otel`) | `telemetry/setup.py`, `google_cloud.py` |
| Agent Runtime metrics | `_RequestDrivenMetricReader` with floor 5000 ms, period `OTEL_METRIC_EXPORT_INTERVAL` (60 s), timeout `OTEL_METRIC_EXPORT_TIMEOUT` (30 s); middleware on request start and end; skipped when a `MeterProvider` already exists; documented tail-loss case | `telemetry/_agent_engine_metric_exporter.py`, `_agent_engine.py` |
| Deploy flag | `adk deploy agent_engine --otel_to_cloud` sets `GOOGLE_CLOUD_AGENT_ENGINE_ENABLE_TELEMETRY=true` and, when absent from `.env`, `ADK_CAPTURE_MESSAGE_CONTENT_IN_SPANS=false`; the `.env` switch alone turns the flag on | `cli/cli_deploy.py` |
| BigQuery plugin | Constructor and `BigQueryLoggerConfig` fields in [bigquery analytics](bigquery-analytics.md); `event_id` per row; no OTel spans; table label `adk_schema_version=2` | `plugins/bigquery_agent_analytics_plugin.py` |
| Eval models | `EvalSet`, `EvalCase`, `Invocation`, `IntermediateData`, `SessionInput` fields and the conversation-xor-scenario validator; camelCase aliases with `populate_by_name`; `.evalset.json` files; id pattern `^[a-zA-Z0-9_]+$` | `evaluation/eval_set.py`, `eval_case.py`, `common.py`, `local_eval_sets_manager.py` |
| Events | `Event` extends `LlmResponse`: `partial`, `usage_metadata`, `finish_reason`, `error_code`, `error_message`, `model_version`, `invocation_id`, `author`, `timestamp`; partial events are not saved to the session (`functions.py` comment) | `events/event.py`, `models/llm_response.py`, `flows/llm_flows/functions.py` |
| Absent in 2.8.0 | `ADK_EXPERIMENTAL_TELEMETRY_FEATURES`, OTLP log export to `telemetry.googleapis.com`, `gcp.resource_type` handling, span-retention fix on servers without the debug trace endpoint | main-branch source and CHANGELOG |

## Version table from the CHANGELOG (2.6.0 to 2.11.0)

| Version | Date | Change relevant to this skill |
| --- | --- | --- |
| 2.6.0 | 2026-07-29 | Request-driven metric export for Agent Engine; `error.type` derived from provider status code; credentials in `config.http_options` no longer traced; malformed `traceparent` tolerated |
| 2.7.0 | 2026-08-13 | Feature gate for experimental telemetry (`ADK_EXPERIMENTAL_TELEMETRY`); BigQuery plugin delivery and termination observability (`event_id`, drop stats, `finish_reason`, `AGENT_ERROR`, `INVOCATION_ERROR`); auto-tracing redacts credential values; failed tool spans marked as errors; inline binary data summarised on spans |
| 2.8.0 | 2026-08-25 | Per-invocation token metrics for `invoke_agent`; per-workflow token and call-count metrics; context cache state on the model span; `RunConfig.telemetry` honoured at the invocation span; MCP HTTP exchanges as log records; inference span ended when inference ends; attributes recorded when a plugin short-circuits the model |
| 2.9.0 | 2026-09-10 | Logs exported over OTLP to `telemetry.googleapis.com`; inference span ends at the finish reason rather than the first chunk; thought signatures kept out of span attributes; skill-load and script-execution instrumentation |
| 2.9.2 | 2026-09-18 | OTel event name dropped only on Agent Engine |
| 2.10.0 | 2026-09-24 | Per-feature experimental telemetry (`ADK_EXPERIMENTAL_TELEMETRY_FEATURES`); tool calls traced under the agent instead of the model call; a streamed model call traced once instead of per chunk; spans no longer retained on servers without a debug trace endpoint (issue #6915, the `InMemoryExporter` growth reported as #6692, community); `Runner.run` keeps the caller's trace in sync; workflow span marked failed when a node fails; `google.adk.telemetry.tracing` importable on OpenTelemetry 1.39 |
| 2.11.0 | 2026-10-01 | Skill telemetry attributes moved out of experimental; spans mark responses that came from a callback; evaluation gains duration, token and call-count efficiency metrics |

Trace shape therefore differs by version: a 2.8.0 export shows tool spans under the model-call span and one span per streamed chunk in some paths; 2.10.0 and later show tool spans under the agent and one span per call. Dashboards and the duplicate-span check in [validation](validation.md) must be read against the deployed version.

## Version floor recommendation

For a new production deployment prefer google-adk 2.10.0 or later (span-retention fix, OTLP logs, one span per streamed call); 2.9.0 is the floor for OTLP log export. This is a recommendation derived from the CHANGELOG, not a statement that 2.8.0 is unsafe; keep an existing pin unless the fixes above address an observed problem.

## Vendor and community material used, with dates

| Item | Date | Type |
| --- | --- | --- |
| adk-docs `observability/traces.md`, `metrics.md`, `logging.md`, `integrations/bigquery-agent-analytics.md`, `integrations/cloud-trace.md`, `integrations/langfuse.md`, `phoenix.md`, `arize-ax.md`, `weave.md`, `mlflow-tracing.md`, `evaluate/index.md` | fetched 2026-10-07 (metrics.md dated 2026-09-18, traces.md 2026-08-07, logging.md 2026-09-21, bigquery 2026-10-05) | documented behaviour |
| OpenTelemetry GenAI semantic conventions, agent spans (semantic-conventions-genai repository) | 2026-10-05 | vendor guidance; Status: Development |
| Google Cloud "Instrument ADK agents" (`stackdriver/docs/instrumentation/ai-agent-adk`), OTLP overview, Trace and Monitoring quotas | 2026-09-30; quotas fetched 2026-10-07 | vendor guidance |
| Agent Platform tracing, monitoring, logging, quality alerts pages | 2026-10-01 | vendor guidance |
| Google Developers Blog, Agent and Model Evaluations GA | 2026-07-31 | vendor guidance |
| agents-cli `google-agents-cli-observability` skill v1.8.0 and `feedback-mechanism.md` | 2026-09-30 | vendor guidance; optional composition |
| Langfuse evaluation and masking pages; Arize run-evals-on-traces | fetched 2026-10-07 | vendor guidance |
| Google SRE Workbook, Implementing SLOs | fetched 2026-10-07 | independent evidence |
| google/adk-python issues #7311, #7162, #7112, #7024, #7017, #6915, #6692, #6465, #6361, #6328, #4829, #3845, #3181; openinference #3857, #3844, #3177; Arize community thread 2026-02-20 | status as of 2026-10-07 | community; symptoms to test for, not facts about the target |

## Not verified here

- Live export to any Google Cloud project, Online Monitors, BigQuery row landing, alert firing, or third-party ingestion. Nothing in this skill ran a cloud call.
- The exact metric name the target's installed `opentelemetry-semantic-conventions` emits for client token usage, and whether its backend renames it.
- Behaviour of `vertexai.agent_engines.AdkApp` per-request flushing beyond the source comment in `_agent_engine.py`.
- Cloud Run CPU throttling effects on the periodic metric reader; stated as an inference to test.
- Community issue reports cited by number; they identify symptoms, and the fix versions come from the issue trackers and CHANGELOG, not from reproducing them.
- The agents-cli infrastructure and feedback pipeline; described from its documentation and not executed.
