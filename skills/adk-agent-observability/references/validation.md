# Validate the telemetry

Use the target's existing test runner and interpreter. Keep doubles at the model boundary (a scripted `BaseLlm` or a `before_model_callback` that short-circuits) so the real `Runner`, flows and instrumentation run. Fail closed on unexpected network calls (`OTEL_EXPORTER_OTLP_*` unset, no ADC in the test environment).

## Local: in-memory exporter contract

Build a `TracerProvider` with `InMemorySpanExporter` and a `MeterProvider` with `InMemoryMetricReader` before importing the agent, set them as global providers, and run one invocation with a scripted model that calls one tool and then answers.

- Exactly one `invoke_agent {name}` span per agent that ran; `gen_ai.conversation.id` equals the session id; `gen_ai.operation.name` is `invoke_agent`.
- Exactly one `execute_tool {tool}` span per function call; when the scripted tool returns `{"error": "..."}` or `{"isError": True}` (MCP double), the span carries `error.type` and status `ERROR`.
- Exactly one `generate_content {model}` span per logical model call; with a streamed scripted response of three chunks, still one span (2.10.0 and later; on 2.8.0 record what you observe and keep the assertion version-tagged).
- With `ADK_CAPTURE_MESSAGE_CONTENT_IN_SPANS=false` and `OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT=NO_CONTENT` set before `TelemetryConfig` construction, no span attribute contains a synthetic marker placed in the user message, the tool arguments and the tool response; `gcp.vertex.agent.llm_request` is `{}`.
- Repeat with a `RunConfig(telemetry=TelemetryConfig(capture_message_content=ContentCapturingMode.SPAN_AND_EVENT))`: the marker appears; then with `ADK_TELEMETRY_IGNORE_RUN_CONFIG=1` in the environment of a fresh config: it does not. This proves the admin lock, which multi-tenant hosts rely on.
- Metrics: one `gen_ai.invoke_agent.duration` point, one `gen_ai.execute_tool.duration` point, `gen_ai.invoke_agent.inference_calls` equal to the scripted call count; `adk.experimental.invoke_agent.total_tokens` absent without the opt-in and present with it.
- Duplicate-owner regression: install `GoogleADKInstrumentor` (if the project uses it) in the same test and assert the span count does not double; if it does, the project has two owners and must choose.

## Local: saved-session helpers

- `invocation_summary.py` over a fixture with a streamed call (two partial events with cumulative usage, one final event): input and output tokens equal the final chunk's figures; a final event without usage takes the newest partial's figures and sets the `usage_taken_from_newest_partial_on_1_calls` flag. The bundled tests (`tests/test_invocation_summary.py`) cover this; run them from the target's interpreter too.
- `invocation_summary.py --prices` with the project's own price table: `cost_basis.source` is `user_supplied_price_table`; models missing from the table are flagged `unpriced_model`, never guessed.
- `events_to_eval_set.py --select tool_error --dry-run`: `eval_cases` equals the number of invocations with a tool error; `structural_problems` is empty; `redactions` counts are non-zero when the fixture contains an email or URL; the synthetic marker is absent from the output file.

## Mocked: exporter wiring

- Point `OTEL_EXPORTER_OTLP_TRACES_ENDPOINT` at a local HTTP double, call `maybe_set_otel_providers()`, run one invocation and `force_flush`; assert one OTLP request arrived and that the resource carries `service.name`.
- For the GCP path, patch `google.auth.default` to return fake credentials and a project, call `get_gcp_exporters(enable_cloud_tracing=True, enable_cloud_metrics=True)` and assert the hook lists are non-empty; with `GOOGLE_CLOUD_AGENT_ENGINE_ID` set and no prior `MeterProvider`, assert the metric reader is the request-driven one and the span processor list includes the metrics-flushing processor. Assert the warning path when a `MeterProvider` is pre-installed.
- Shutdown: call the application's shutdown handler and assert `force_flush` was invoked on each provider with a budget and its result logged.

## Live (approved project, principal, cost ceiling)

1. One synthetic invocation; within the batch delay, the trace appears in Trace Explorer with the expected spans and `gen_ai.conversation.id`; the log query on `trace=projects/{p}/traces/{id}` returns the application and ADK records.
2. Within the export interval, metric descriptors exist for `gen_ai.invoke_agent.duration` and `gen_ai.execute_tool.duration` on the expected monitored resource; on Agent Runtime, send a second request shortly after the first and confirm both requests' points arrive (the tail-loss case needs a request after the short one).
3. A forced tool failure fires the tool alert within its window; a forced export outage (revoke the writer role on a copy) fires the telemetry-stopped alert.
4. One BigQuery row per expected event type for the invocation; `get_drop_stats()` all zero; the `trace_id` column equals the trace id in Trace Explorer.
5. If an Online Monitor exists, confirm one scored trace and the metric `aiplatform.googleapis.com/online_evaluator/scores` with the expected `evaluation_metric_name`.

A live afternoon establishes only that the path works for that version, project and traffic; it does not establish quota behaviour, retention or cost.

## Completion report

| Evidence | Supports |
| --- | --- |
| Source inspection and the two helpers | Which signals, gates and exporters exist in configuration; no runtime guarantee |
| In-memory exporter tests | Span and metric counts, content gating and the admin lock under the fixture contract |
| Mocked exporter wiring | Provider ownership, request-driven reader selection, flush on shutdown |
| Approved live check | Only the observed project, version, traffic and sample |
| Production principle | A requirement without a test in this change |

List unverified items explicitly: pinned version differing from 2.8.0, the token-usage metric name emitted by the installed semconv package, dashboards keyed on span names across a schema-version change, any content gate whose effective value could not be read from configuration, and Online Monitor or BigQuery behaviour not exercised live. Separate **local**, **mocked**, **live** and **not run**.

Independent community project; not affiliated with or endorsed by Google.
