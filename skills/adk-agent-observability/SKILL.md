---
name: adk-agent-observability
description: Instrument, monitor, alert on and debug Python Google ADK agents in production. Covers which spans, metrics and logs ADK emits and which environment gates control them, exporters per host (Cloud Run, GKE, Agent Runtime, OTLP third parties), SLIs, SLOs and alerts including Online Monitors, BigQuery Agent Analytics, feedback capture, turning production traces into evaluation cases, and debugging from a trace to a session. Use for missing or duplicated telemetry, token or cost accounting, alert design, dashboards, or a production incident on an ADK agent. Do not activate for content-redaction policy (protect-adk-sensitive-data), GKE exporter allowlists and custom spans (optimise-adk-on-google-cloud), evaluation design (adk-agent-evaluation), first deployment (deploy-adk-on-google-cloud), or Terraform and CLI scaffolding of telemetry infrastructure (Google's agents-cli skills).
license: MIT
metadata:
  author: Ruslan Khissamiyev
  source-book: Agentic Engineering
  source-chapter: "cross-framework"
  verified-against: "google-adk 2.8.0 source and adk-python main CHANGELOG, 2026-10-07"
---

# ADK agent observability

Decide which signals an ADK agent emits, where they go, what the numbers mean and how an alert leads back to a session and forward to an evaluation case. Deliver the smallest change to an existing agent, or a review with observable findings. Keep one owner per telemetry provider, count usage once per logical model call, read every claim against the pinned ADK version, and leave content policy to protect-adk-sensitive-data.

## Inspect before choosing a mode

1. Record the pinned `google-adk`, `opentelemetry-sdk`, exporter and any `openinference-instrumentation-google-adk` or `opentelemetry-instrumentation-google-genai` versions. Most behaviour below is for **2.8.0**; [compatibility](references/compatibility.md) labels what changed in 2.6 to 2.11 and what later releases fixed. Keep pins unchanged unless a version decision is requested.
2. Identify the host: Agent Runtime (`GOOGLE_CLOUD_AGENT_ENGINE_ID` present at runtime), Cloud Run, GKE or local `adk web` / `adk api_server`. The host decides the exporter, the default telemetry schema version and the metric reader ([export paths](references/export-paths.md)).
3. List every telemetry environment variable in deployment configuration and `.env` files: `GOOGLE_CLOUD_AGENT_ENGINE_ENABLE_TELEMETRY`, `ADK_CAPTURE_MESSAGE_CONTENT_IN_SPANS`, `OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT`, `OTEL_SEMCONV_STABILITY_OPT_IN`, `ADK_EXPERIMENTAL_TELEMETRY`, `ADK_TELEMETRY_SCHEMA_VERSION_OPT_IN`, `ADK_TELEMETRY_IGNORE_RUN_CONFIG`, `OTEL_EXPORTER_OTLP_*`, `OTEL_SERVICE_NAME`, `OTEL_RESOURCE_ATTRIBUTES`. Record the effective value of each with its precedence ([signals and schema](references/signals-and-schema.md)).
4. Find every provider setup: `maybe_set_otel_providers`, `get_gcp_exporters`, `--otel_to_cloud`, `GoogleADKInstrumentor().instrument()`, `TracerProvider(...)` or `set_tracer_provider` in application code, and every plugin on the `App` or `Runner`: `BigQueryAgentAnalyticsPlugin`, `LoggingPlugin`, `DebugLoggingPlugin`, `AutoTracingPlugin`. Note any `RunConfig(telemetry=TelemetryConfig(...))`.
5. Find the logging level in production configuration and whether `google_adk.*` loggers run at `DEBUG` (full prompts in logs, documented behaviour).
6. Inventory existing dashboards, alerting policies, log sinks, BigQuery datasets and where sessions are stored (`SESSION_SERVICE_URI`, Agent Runtime sessions, a database), because debugging ends at a stored session.
7. Run the two helpers on a saved session export with an available Python 3.11+ interpreter after resolving `SKILL_DIR` to this skill's directory. They read the file only; they never import the project or call a provider.

```bash
python "$SKILL_DIR/scripts/invocation_summary.py" --session ./saved_session.json --format json
python "$SKILL_DIR/scripts/invocation_summary.py" --session ./saved_session.json --prices ./prices.json --format csv
python "$SKILL_DIR/scripts/events_to_eval_set.py" --session ./saved_session.json --out ./regressions.evalset.json --select tool_error --dry-run
```

`invocation_summary.py` reports, per invocation, logical model calls, tool calls and tool errors by name (dict responses with a truthy `error`, `isError` or `is_error` key, or an error status), the last authoritative usage per logical call (streaming partials are never summed), finish reasons, model error codes, wall time per step and an optional cost from a price table you supply (`assets/price_table.example.json` is a template with placeholder numbers). `events_to_eval_set.py` converts the same file into the 2.8.0 `EvalSet` shape with a required redaction step ([trace to evaluation](references/trace-to-evaluation.md)). Exit 1 means partial or malformed input; neither helper prints event text.

## Choose the relevant mode

| Mode | Read | Produce |
| --- | --- | --- |
| (a) Instrument | [signals and schema](references/signals-and-schema.md), then [export paths](references/export-paths.md) | One provider owner per process, the exporter for the host, the environment gate matrix with effective values, flush and shutdown on the request path, a check that spans and metrics arrive |
| (b) Define SLIs, SLOs and alerts | [SLO and alerting](references/slo-and-alerting.md) | Good/total ratio SLIs from measured baselines, an error-budget alert, latency and tool-error alerts, Online Monitors with their judge billing approved |
| (c) Debug from a trace | [debugging runbook](references/debugging-runbook.md) | Alert to trace to session to reproduction, with the trace, invocation and session identifiers preserved at every hop |
| (d) Production to evaluation hand-off | [trace to evaluation](references/trace-to-evaluation.md), [feedback capture](references/feedback-capture.md) | Sampling rule, feedback join key, redacted `EvalSet` export reviewed before it becomes a regression case, handed to adk-agent-evaluation |
| (e) Audit telemetry | [signals and schema](references/signals-and-schema.md), [bigquery analytics](references/bigquery-analytics.md), [validation](references/validation.md) | Findings with file and line: duplicate spans or usage, missing correlation, unflushed exporters, content gates left at defaults, version-dependent names |

Modes compose. A new alert that needs a metric the agent does not yet emit is (b) plus (a); an incident review that produces regression cases is (c) plus (d). Structured analytics in BigQuery belong to [bigquery analytics](references/bigquery-analytics.md) and apply to (a), (b) and (d).

## Implement the change

- Keep one owner per signal. `maybe_set_otel_providers` does not replace a provider that is already set; a second owner (an OpenInference instrumentor, an application `TracerProvider`, a `MeterProvider` created before ADK's) produces duplicate or orphan spans and, on Agent Runtime, disables the request-driven metric reader with a warning. Run the agent with `run_async`; a synchronous `Runner.run` executes on a worker thread, which third-party integrations document as breaking context propagation (vendor guidance).
- Set the content gates deliberately and in the same place. In 2.8.0 `ADK_CAPTURE_MESSAGE_CONTENT_IN_SPANS` defaults on and only `false` or `0` turns it off; `OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT` accepts `NO_CONTENT`, `EVENT_ONLY`, `SPAN_ONLY`, `SPAN_AND_EVENT`, treats `true` or `1` as `EVENT_ONLY` and anything else as `NO_CONTENT`. `TelemetryConfig` reads the environment once at construction; a per-request `RunConfig.telemetry` wins over the environment unless `ADK_TELEMETRY_IGNORE_RUN_CONFIG` is set. The policy itself (what may be captured, retention, redaction) is protect-adk-sensitive-data's; apply its baseline from `references/implementation-recipes.md`.
- Choose the schema version on purpose. Schema v2 (`invoke_workflow {entrypoint}` instead of `invocation`) is the default only when `GOOGLE_CLOUD_AGENT_ENGINE_ID` is set; everywhere else v1 applies unless `ADK_TELEMETRY_SCHEMA_VERSION_OPT_IN=2`. Dashboards keyed on span names break at that boundary; the source docstring plans v2 as the global default later.
- Count usage once per logical model call. ADK's `TokenUsage` takes the newest cumulative `usage_metadata` of a streamed call, defines input as prompt plus tool-use prompt tokens and output as candidates plus thoughts tokens, and derives total from those two. Use the same arithmetic in dashboards and in `invocation_summary.py`; summing chunks or adding the model-reported total double counts.
- Gate experimental names. `adk.experimental.*` metrics and context-cache attributes need `ADK_EXPERIMENTAL_TELEMETRY=true` (or the per-request opt-in); the eight `invoke_workflow` token and count metrics also need schema v2, and nested workflow datapoints fold into their parents, so filter `gen_ai.workflow.nested` out before summing.
- Flush on the request path and at shutdown. On Agent Runtime the metric reader collects only while a request is in flight and documents a residual loss for the last short request before idle; everywhere else a `BatchSpanProcessor` and a periodic reader need `force_flush` within the shutdown budget. A missing final flush looks like a silent sampling drop.
- Build SLOs as good/total ratios on measured baselines and alert on error budget burn, never on a 100 percent target. Agent-specific SLIs (task completion, tool-call error rate by tool, tokens per successful task, escalation rate) come from vendor material; treat them as candidates until the target's own baseline exists.
- Prefer metrics for cost and rate questions, traces for one slow or failed turn, BigQuery rows for cohort analysis and joins to feedback, and the stored session for reproduction. Correlate logs with `logging.googleapis.com/trace`, `logging.googleapis.com/spanId` and `logging.googleapis.com/trace_sampled`; a generic `trace_id` field does not correlate.

## Permissions and approvals

Enabling `telemetry.googleapis.com`, Cloud Trace, Cloud Monitoring and Cloud Logging APIs, granting writer roles (`roles/telemetry.tracesWriter` or `roles/telemetry.writer`, `roles/logging.logWriter`, `roles/monitoring.metricWriter`; vendor guidance 2026-09-30), creating BigQuery datasets or tables (Storage Write API is billed), creating log sinks, enabling Online Monitors (each judge call is billed) and turning on content capture are consequential. Present project, host, principal, estimated volume and cost ceiling, obtain approval, and record what was enabled. Reading an existing trace or session with the user's own access is not.

## Validate and finish

Read [validation](references/validation.md). Three checks are observable without a cloud project:

1. An in-memory exporter test that runs the real `Runner` with a scripted model and asserts exactly one `invoke_agent`, one `execute_tool` per tool call and one `generate_content` span per logical model call, with `gen_ai.conversation.id` set and content attributes absent under the chosen gate.
2. `invocation_summary.py` over a saved session with a streamed call, asserting the input and output token totals equal the final chunk, not the sum of chunks.
3. `events_to_eval_set.py --select tool_error --dry-run` over the same session, asserting the case count, the redaction counts and an empty `structural_problems` list.

Live checks (spans in Trace Explorer, metric descriptors in Cloud Monitoring, rows in BigQuery, an alert firing on a synthetic failure) need an approved project and principal. Report what was inspected, which gates were effective, which tests ran and what remains unverified, separating **local**, **mocked**, **live** and **not run**. Record every URL with its page date; semantic convention names and Google Cloud consoles change faster than this skill.

Independent community project; not affiliated with or endorsed by Google.
