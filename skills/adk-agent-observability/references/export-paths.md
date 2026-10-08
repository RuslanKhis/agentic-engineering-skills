# Export paths by host

Read when choosing or auditing where telemetry goes. Source statements are google-adk 2.8.0 (`telemetry/setup.py`, `google_cloud.py`, `_agent_engine.py`, `_agent_engine_metric_exporter.py`, `cli/cli_deploy.py`) unless a version is named. Google Cloud statements are vendor guidance with their page dates.

## Rules that hold on every host

- `maybe_set_otel_providers(hooks, resource)` builds a `TracerProvider`, `MeterProvider` (`shutdown_on_exit=False`) and `LoggerProvider` only for signal types that have hooks, appends generic OTLP exporters for every `OTEL_EXPORTER_OTLP_*ENDPOINT` set, and does not override a provider that another component already set globally. One owner per signal; if the application or an instrumentor sets a provider first, ADK's exporters never attach.
- `get_gcp_exporters(enable_cloud_tracing, enable_cloud_metrics, enable_cloud_logging, google_auth)` returns hooks. Traces and metrics go by OTLP HTTP to `https://telemetry.googleapis.com/v1/traces` and `/v1/metrics` (mTLS endpoints when `GOOGLE_API_USE_CLIENT_CERTIFICATE` or `GOOGLE_API_USE_MTLS_ENDPOINT` select them) with an `AuthorizedSession` from Application Default Credentials. Logs in 2.8.0 use `CloudLoggingExporter` (package `opentelemetry-exporter-gcp-logging`) with log name `adk-otel` off Agent Runtime; 2.9.0 moves logs to OTLP at `telemetry.googleapis.com` (CHANGELOG).
- The project is resolved from ADC; with no project the function logs a warning and returns empty hooks, so a misconfigured identity fails silently into "no telemetry". Check the startup log for `Cannot determine GCP Project`.
- `get_gcp_resource` merges `gcp.project_id`, `OTEL_SERVICE_NAME` / `OTEL_RESOURCE_ATTRIBUTES` and, off Agent Runtime, the GCP resource detector (GCE, GKE, Cloud Run attributes; a warning when `opentelemetry-resourcedetector-gcp` is missing). On Agent Runtime it sets `cloud.platform=gcp.agent_engine`, `service.name` to the engine id, `service.version` to the runtime revision and `cloud.resource_id=//aiplatform.googleapis.com/projects/{p}/locations/{l}/reasoningEngines/{id}`.
- Flush deliberately: `BatchSpanProcessor` and `PeriodicExportingMetricReader` export on timers; call `force_flush` on each provider in the shutdown path with its own budget and inspect the boolean result (optimise-adk-on-google-cloud's `gke-serving.md` covers GKE drain budgets).

## APIs, roles and quotas (vendor guidance)

| Need | Guidance | Source and date |
| --- | --- | --- |
| APIs | `telemetry.googleapis.com`, Cloud Logging, Cloud Monitoring, Cloud Trace, Service Usage, and `aiplatform.googleapis.com` on Agent Runtime | Google Cloud "Instrument ADK agents" page, 2026-09-30 |
| Write roles | `roles/telemetry.tracesWriter` (traces only) or `roles/telemetry.writer` (all three), `roles/logging.logWriter`, `roles/monitoring.metricWriter`; a separate quota project needs `roles/serviceusage.serviceUsageConsumer` and the `x-goog-user-project` header | same; the Agent Platform tracing page still lists the legacy `roles/cloudtrace.agent` |
| Read roles | `roles/cloudtrace.user`, `roles/logging.viewer`, `roles/monitoring.viewer` | same |
| Trace limits | 1,024 attributes per span, 64 KiB attribute value, 1,024-byte span name, 256 events, 128 links, 30-day retention | Cloud Trace quotas page, fetched 2026-10-07 |
| Monitoring limits | 10,000 metric descriptors per project, 30 labels, 1,024-char label values, 200 time series per write, one point per 5 s per series, 200,000 active series per monitored resource, 24-month retention | Cloud Monitoring quotas page, fetched 2026-10-07 |
| Billing | OTLP metrics bill as Prometheus samples ingested; traces at Cloud Trace span pricing; Storage Write API for BigQuery rows | respective pricing pages |

Enabling APIs and granting roles are approvals. A service-account key file as ADC has been reported to fail OTLP export with `invalid_scope` (issue #7024, community, status unclear); prefer attached service identities.

## Agent Runtime (Vertex AI Agent Engine)

- Master switch: `GOOGLE_CLOUD_AGENT_ENGINE_ENABLE_TELEMETRY=true` in the deployment's environment (Agent Platform tracing page, 2026-10-01: replaces `enable_tracing`; needs the Telemetry API and Logging API). `adk deploy agent_engine --otel_to_cloud` sets it and, when `.env` lacks `ADK_CAPTURE_MESSAGE_CONTENT_IN_SPANS`, sets that to `false`; when `.env` already carries the switch, the flag turns on automatically (`cli/cli_deploy.py`, 2.8.0).
- Optional: `OTEL_SEMCONV_STABILITY_OPT_IN=gen_ai_latest_experimental` plus `OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT=EVENT_ONLY` adds prompts, responses and `user.id` to log records (vendor; content policy is protect-adk-sensitive-data's).
- Metrics: the runtime throttles CPU when a request ends, so a periodic reader starves. `_get_agent_engine_metrics_setup` (only when `GOOGLE_CLOUD_AGENT_ENGINE_ID` is set and no `MeterProvider` is already installed) builds `_RequestDrivenMetricReader` plus a span processor that collects on `generate_content` span starts, and `maybe_install_request_metrics_middleware(app, otel_to_cloud=True)` drives it from FastAPI request start and end. Constraints in source: collect only while serving; never closer than the floor (5 s default); at least once per period (60 s) under load. Documented residual loss: a request shorter than the floor that is the last before idle loses its points. Installing your own `MeterProvider` first disables this with a warning, and metrics may be dropped between requests.
- Traces and logs are force-flushed per request by the `AdkApp` host (source comment in `_agent_engine.py`), not by this middleware.
- Trace context: the runtime passes `Google-Agent-Engine-Traceparent`; `TopSpanProcessor` stamps a `supportID` attribute on the top span from the incoming `traceparent` baggage.
- Built-in metrics on monitored resource `aiplatform.googleapis.com/ReasoningEngine` (labels `resource_container`, `location`, `reasoning_engine_id`): `aiplatform.googleapis.com/reasoning_engine/request_count`, `request_latencies`, `cpu/allocation_time`, `memory/allocation_time`, with `response_code` and `response_code_class`; ADK 2.6.0 or later with telemetry on adds the GenAI metrics as user-defined metrics; an "Agent Runtime Overview" dashboard shows sessions, turns, invocations, tokens, p50 to p99 latency, errors, topology and MCP metrics (Agent Runtime monitoring page, 2026-10-01). Stdout lands in `reasoning_engine_stdout`, stderr and build logs beside it; child resources (Sessions, Memory Bank, Code Execution) are not logged (Agent Runtime logging page, fetched 2026-10-07).

## Cloud Run

- Run `adk api_server --otel_to_cloud` (the CLI calls `get_gcp_exporters` and `maybe_set_otel_providers`) or call them from the application before constructing the `Runner`. `adk deploy cloud_run --otel_to_cloud` adds the flag to the generated `CMD` (`cli/cli_deploy.py`).
- Set `ADK_CAPTURE_MESSAGE_CONTENT_IN_SPANS=false` explicitly; nothing sets it for you here (adk-docs `integrations/cloud-trace.md`, fetched 2026-10-07).
- Metrics use the periodic reader at `MIN_EXPORT_INTERVAL_MS` (5 s). Cloud Run also throttles CPU outside requests on request-based billing; test a quiet instance for dropped points, and consider always-allocated CPU or a flush in the request path if points go missing (this is an inference from the Agent Runtime design, not documented Cloud Run behaviour).
- Correlate logs: emit structured JSON with `logging.googleapis.com/trace` as `projects/{project}/traces/{trace_id}`, `logging.googleapis.com/spanId` and `logging.googleapis.com/trace_sampled` (Cloud Logging structured logging page). The `CloudLoggingExporter` path writes OTel log records; application `logging` output needs its own correlation fields.

## GKE

- Same programmatic setup as Cloud Run. The GCP resource detector supplies the `k8s_container` resource when the metadata server is reachable.
- Exporter allowlists, custom session spans and drain budgets are optimise-adk-on-google-cloud's (`references/gke-serving.md`, `assets/session_observation.py`); do not duplicate them. This skill owns which ADK signals exist and what they mean.
- A collector sidecar or DaemonSet receiving `OTEL_EXPORTER_OTLP_ENDPOINT` is the usual place for attribute processors; the collector then needs the writer roles above through Workload Identity.

## OTLP third parties

| Destination | Mechanism in adk-docs (fetched 2026-10-07) | Duplicate-span check |
| --- | --- | --- |
| Langfuse, Phoenix, Arize AX | `openinference-instrumentation-google-adk` `GoogleADKInstrumentor().instrument()` | Runs beside ADK's native spans; verify one `invoke_agent` per invocation in the destination. Open report: the instrumentor suppresses `invoke_workflow` and node spans on ADK 2.x (openinference #3844, community); earlier reports of orphan or duplicate spans after a partial patch (Arize community thread 2026-02-20) and an `instrument()` failure on ADK 2.10 fixed 2026-09-29 (#3857) |
| Weave, MLflow Tracing, Grafana Cloud, Datadog, Cloud Trace | OTLP exporter and a global `TracerProvider` set before ADK, or `maybe_set_otel_providers` with hooks | ADK attaches to the existing provider; no second instrumentor |
| Langfuse masking | `mask_otel_spans` applies only to Langfuse's exporter (Langfuse masking page, vendor) | Other exporters in the same process still receive unmasked attributes |

Pin `openinference-instrumentation-google-adk` to a version tested with the pinned ADK; `opentelemetry-instrumentation-google-genai` below `1.0b0` drops `user.id` (issue #6361, community, open). Run the agent with `run_async`; Langfuse documents that synchronous `runner.run()` executes on a thread that loses OTel context (vendor).

## Flush and shutdown checklist

1. Which component owns each provider, and does anything set one earlier?
2. Is `force_flush` called on traces, metrics and logs in the shutdown handler with a budget, and is its result logged?
3. On Agent Runtime, is the metrics middleware installed (`otel_to_cloud=True` path) and is no other `MeterProvider` created?
4. Does the startup log show the project resolved and the exporter packages present (`opentelemetry-exporter-otlp-proto-http`, `opentelemetry-exporter-gcp-logging`, `opentelemetry-resourcedetector-gcp`)?
5. Does one synthetic invocation produce the expected spans in the destination within the batch delay, and one metric point within the export interval?

Independent community project; not affiliated with or endorsed by Google.
