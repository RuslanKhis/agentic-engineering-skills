# Signals and schema

Read when adding, naming or auditing telemetry. Every name below was read in google-adk 2.8.0 source (`telemetry/` and `plugins/`) unless a later version is named. The OpenTelemetry GenAI semantic conventions are **Status: Development** and now live in their own repository (github.com/open-telemetry/semantic-conventions-genai, agent-spans document changed 2026-10-05; vendor guidance): pin instrumentation versions, expect renames, and key dashboards on attributes you have observed in the target's own export.

## Environment gates and precedence

`TelemetryConfig` (`telemetry/context.py`) reads every environment fallback once, at construction. Precedence for each knob: admin lock (`ADK_TELEMETRY_IGNORE_RUN_CONFIG` set to `1` or `true`) makes the environment win; otherwise a non-`None` field on `RunConfig(telemetry=TelemetryConfig(...))` wins; otherwise the environment variable; otherwise the default.

| Variable | Accepted values (2.8.0) | Default | Effect |
| --- | --- | --- | --- |
| `ADK_CAPTURE_MESSAGE_CONTENT_IN_SPANS` | off only for `false` or `0` (case-insensitive, stripped) | on | Content on ADK-owned legacy span attributes (`gcp.vertex.agent.llm_request`, `gcp.vertex.agent.llm_response`, tool args and responses). Any other value, including `off` or `no`, leaves it on (source-verified; reported as issue #7311, community) |
| `OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT` | `NO_CONTENT`, `EVENT_ONLY`, `SPAN_ONLY`, `SPAN_AND_EVENT`; `true` or `1` coerce to `EVENT_ONLY`; anything else is `NO_CONTENT` | `NO_CONTENT` | Content on `gen_ai.*.message` / `gen_ai.choice` log bodies (event-bearing modes) and on the experimental inference span (span-bearing modes). A per-request `capture_message_content` also drives the legacy span knob through the span-bearing test |
| `OTEL_SEMCONV_STABILITY_OPT_IN` | CSV containing `gen_ai_latest_experimental` | absent | Experimental GenAI semconv: `gen_ai.client.inference.operation.details` log event with `gen_ai.input.messages`, `gen_ai.output.messages`, `gen_ai.system_instructions`, `gen_ai.tool.definitions`. Google's ADK instrumentation page (2026-09-30, vendor) warns that `true` for the content variable under the latest semconv is an invalid configuration and collects nothing; use `EVENT_ONLY` |
| `ADK_EXPERIMENTAL_TELEMETRY` | `1` or `true` | off | `adk.experimental.*` metrics, token accumulation on `invoke_agent` and `invoke_workflow`, `adk.experimental.context_cache.*` span attributes. 2.10.0 adds per-feature `ADK_EXPERIMENTAL_TELEMETRY_FEATURES` (main source; absent in 2.8.0) |
| `ADK_TELEMETRY_SCHEMA_VERSION_OPT_IN` | `1` or `2` | `2` when `GOOGLE_CLOUD_AGENT_ENGINE_ID` is set, else `1` | v1: top-level `invocation` span. v2: `invoke_workflow {entrypoint}` span plus `gen_ai.invoke_workflow.duration`. The source docstring lists further v2 steps (remove `call_llm`, align `execute_tool` content attributes, flip the default, retire the variable) |
| `ADK_TELEMETRY_IGNORE_RUN_CONFIG` | `1` or `true` | off | Ignore per-request `RunConfig.telemetry`; multi-tenant hosts use it so a caller cannot re-enable content capture |
| `ADK_CAPTURE_MCP_HTTP_BODIES` | boolean | off | MCP HTTP exchange bodies in log records (2.8.0 reports MCP HTTP exchanges as log records, CHANGELOG) |
| `ADK_ROOT_AGENT_NAME` | string | unset | Not read by `telemetry/` in 2.8.0; the metric attribute `adk.experimental.root_agent.name` is filled from the runner's agent |
| `OTEL_EXPORTER_OTLP_ENDPOINT`, `..._TRACES_ENDPOINT`, `..._METRICS_ENDPOINT`, `..._LOGS_ENDPOINT` | URL | unset | `maybe_set_otel_providers` adds a generic OTLP HTTP exporter per signal whose endpoint is set |
| `OTEL_SERVICE_NAME`, `OTEL_RESOURCE_ATTRIBUTES` | OTel standard | unset | Resource attributes through `OTELResourceDetector` |
| `OTEL_METRIC_EXPORT_INTERVAL`, `OTEL_METRIC_EXPORT_TIMEOUT` | ms | 60000, 30000 | Guidepost period and export timeout of the Agent Runtime request-driven reader |
| `GOOGLE_CLOUD_AGENT_ENGINE_METRICS_COLLECTION_INTERVAL_FLOOR_MS` | ms | 5000 (`MIN_EXPORT_INTERVAL_MS`) | Minimum spacing between two metric collects on Agent Runtime |
| `GOOGLE_CLOUD_DEFAULT_LOG_NAME` | string | `adk-otel` | Cloud Logging log name off Agent Runtime |
| `GOOGLE_CLOUD_AGENT_ENGINE_ENABLE_TELEMETRY` | `true` | unset | Read by the Agent Runtime host and by `adk deploy agent_engine`; in ADK 2.8.0 itself it only adds the `Vertex-Agent-Engine/...` User-Agent header to exporters. `--otel_to_cloud` on deploy sets it to `true` and, when `.env` lacks it, sets `ADK_CAPTURE_MESSAGE_CONTENT_IN_SPANS=false` (`cli/cli_deploy.py`) |

Write the effective value of each gate into the review. `OTEL_SDK_DISABLED=true` is an offline convenience, not a review of production exporters (protect-adk-sensitive-data).

## Spans (2.8.0 native instrumentation)

| Span | Attributes set by ADK | Gate or note |
| --- | --- | --- |
| `invocation` (schema v1) or `invoke_workflow {entrypoint}` (schema v2) | v2: `gen_ai.operation.name=invoke_workflow`, `gen_ai.conversation.id`, `gen_ai.workflow.name`, `gen_ai.workflow.nested` only when nested | Entrypoint that is itself a `Workflow` node reuses its own node span |
| `invoke_agent {agent.name}` | `gen_ai.operation.name=invoke_agent`, `gen_ai.agent.name`, `gen_ai.agent.description`, `gen_ai.conversation.id` (session id) | `gen_ai.agent.id`, `gen_ai.data_source.id` and `server.*` deliberately not set; `gen_ai.agent.version` constant exists in `_metrics.py` |
| `execute_tool {tool.name}` | `gen_ai.operation.name=execute_tool`, `gen_ai.tool.name`, `gen_ai.tool.description`, `gen_ai.tool.type` (class name), `gen_ai.agent.name`, `error.type` plus `ERROR` status when the tool raised or returned an error dict detected by the tool's `_detect_error_in_response` hook (`MCP_TOOL_ERROR` for `isError`/`is_error`, `HTTP_ERROR` for a truthy `error` key on REST tools); tool args and response under content gate | 2.10.0 nests tool spans under the agent rather than the model call (CHANGELOG) |
| `generate_content {model}` (native, when `opentelemetry-instrumentation-google-genai` is not wrapping `Models.generate_content` for a Gemini agent) | `gen_ai.operation.name=generate_content`, `gen_ai.agent.name`, `gen_ai.conversation.id`, `gcp.vertex.agent.event_id`, `gcp.vertex.agent.invocation_id`; `user.id` is log-only | With the instrumentor installed ADK only adds extra attributes to the library's span and skips its own client metrics |
| legacy call attributes (`trace_call_llm`) | `gen_ai.system=gcp.vertex.agent`, `gen_ai.request.model`, `gcp.vertex.agent.invocation_id`, `gcp.vertex.agent.session_id`, `gcp.vertex.agent.event_id`, `gen_ai.request.top_p`, `gen_ai.request.max_tokens`, `gen_ai.usage.experimental.reasoning_tokens_limit`, `gen_ai.response.finish_reasons` (lower-cased list), usage attributes below; `gcp.vertex.agent.llm_request` / `llm_response` hold `{}` when content is off | Inline binary parts are summarised, not copied (2.7.0 CHANGELOG) |
| usage attributes (`TokenUsage.to_attributes`) | `gen_ai.usage.input_tokens` (prompt + tool-use prompt), `gen_ai.usage.output_tokens` (candidates + thoughts), `gen_ai.usage.cache_read.input_tokens`, `gen_ai.usage.cache_creation.input_tokens`, `gen_ai.usage.reasoning.output_tokens`, `gen_ai.usage.experimental.system_instruction_tokens` | Names are pinned as strings in `_token_usage.py` pending newer `opentelemetry-semantic-conventions` releases |
| context cache | `adk.experimental.context_cache.hit`, `.fingerprint`, `.contents_count`, `.invocations_used` | `ADK_EXPERIMENTAL_TELEMETRY` only; the fingerprint is a content hash |
| compaction | `gen_ai.compaction.trigger`, `.summarizer_type`, `.event_count`, `.token_threshold`, `.event_retention_size`, `.compaction_interval`, `.overlap_size`, `.result_event_id`, `.start_timestamp`, `.end_timestamp` | Emitted around event compaction |
| skills | `adk.experimental.skill.name`, `.source.type`, `.description`, `.additional_tools`, `.source.uri`, `.resource.path` on `execute_tool` spans | Moved out of experimental in 2.11.0 (CHANGELOG) |

`error.type` on model calls derives from the provider status code (`str(error.code)` for `APIError`, else the exception class name; 2.6.0 CHANGELOG).

The OpenTelemetry GenAI conventions now live in their own repository
(open-telemetry/semantic-conventions-genai, commit 9ffc7e0, 2026-10-21;
Apache-2.0; read 2026-10-22), every agent span and event there still carries
**Development** status, and that repository ships a reference scenario for
google-adk pinned to `google-adk==2.11.0`
(`reference/scenarios/google-adk/`). Its README marks `invoke_agent`
(internal), `invoke_workflow`, `execute_tool`, memory and `SkillToolset`
spans as implemented and inference as correctly delegated to `google-genai`;
its `conformance.yaml` lists the ten violations a conformant run is expected
to show, which is the list to diff against on your own export; this skill
carries them as data in
[assets/semconv-expected-violations.adk-2.11.0.json](../assets/semconv-expected-violations.adk-2.11.0.json)
(exactly five `gcp.vertex.agent.*` keys: `event_id`, `invocation_id`,
`llm_request`, `llm_response`, `session_id`; the tool-argument and
tool-response keys under the same prefix are not in the upstream list, so
they count as drift until the list changes; the removed `gen_ai.system`
attribute, `process.exit.code`, the `execute_tool <gen_ai.tool.name>`
span-name refinement, and histogram unit `1` where the conventions want
`{inference_call}` and `{tool_call}`). Two cautions before using it as a
baseline: the scenario runs the conventions' own reference instrumentation
over ADK and patches ADK's native `trace_tool_call` and
`trace_merged_tool_calls` out (`scenario.py`), so it describes ADK's
operations and attributes, not ADK's native tool spans; and it was checked
against 2.11.0, not 2.12.0. Do not key a dashboard or alert on
`gen_ai.system`; key on `gen_ai.provider.name`, `gen_ai.operation.name` and
`gen_ai.agent.name`, and carry the proprietary `gcp.vertex.agent.*` keys as
ADK-specific joins. A new violation beyond that list on your pinned version
is drift to record, not a dashboard to fix.

## Log records

| Event name | Body | Gate |
| --- | --- | --- |
| `gen_ai.system.message`, `gen_ai.user.message`, `gen_ai.choice` (stable semconv names, `_stable_semconv.py`) | `{"content": ...}`; `gen_ai.choice` adds `index: 0` and `finish_reason` | Content is `<elided>` unless the capturing mode is `EVENT_ONLY` or `SPAN_AND_EVENT`; the ADK Web UI exporter passes `do_not_elide` |
| `gen_ai.client.inference.operation.details` (`_experimental_semconv.py`) | request and response operation details, tool definitions | `OTEL_SEMCONV_STABILITY_OPT_IN=gen_ai_latest_experimental`; content follows the capturing mode |
| `adk.experimental.mcp.http.client.*` | MCP HTTP exchanges | 2.8.0; bodies behind `ADK_CAPTURE_MCP_HTTP_BODIES` |

Logs carry `user.id` as a log-only attribute when the session has a user id; spans do not. On Agent Runtime the OTel event name is dropped (2.9.2 CHANGELOG: only on Agent Engine).

## Metrics (2.8.0, meter `gcp.vertex.agent`)

| Metric | Unit | Attributes | Gate |
| --- | --- | --- | --- |
| `gen_ai.invoke_agent.duration` | s, histogram with explicit buckets 0.1 to 409.6 | `gen_ai.agent.name`, `error.type` | always |
| `gen_ai.invoke_workflow.duration` | s | `gen_ai.operation.name`, `gen_ai.workflow.name`, `gen_ai.workflow.nested` (nested only), `error.type` | schema v2 for the entrypoint row |
| `gen_ai.execute_tool.duration` | s, buckets 0.01 to 81.92 | `gen_ai.agent.name`, `gen_ai.tool.name`, `gen_ai.tool.type`, `error.type` | always |
| `gen_ai.invoke_agent.inference_calls`, `gen_ai.invoke_agent.tool_calls` | count histogram, buckets 0 to 512 | `gen_ai.agent.name` | always |
| `gen_ai.client.operation.duration` | s | `gen_ai.agent.name`, `gen_ai.operation.name`, `gen_ai.provider.name`, `gen_ai.request.model`, `gen_ai.response.model`, `error.type` | native path only |
| `gen_ai.client.token.usage` (created through the installed `opentelemetry-semantic-conventions` helper) | tokens, split by `gen_ai.token.type` = `input` or `output` | as above plus `gen_ai.token.type` | native path only; last chunk's usage; cached tokens are part of input and not recorded separately here |
| `adk.experimental.invoke_agent.{input_tokens,output_tokens,total_tokens,cache_read.input_tokens,reasoning.output_tokens,tool.input_tokens}` | tokens | `gen_ai.agent.name` | `ADK_EXPERIMENTAL_TELEMETRY` |
| `adk.experimental.invoke_workflow.{input_tokens,output_tokens,total_tokens,cache_read.input_tokens,reasoning.output_tokens,tool.input_tokens,inference_calls,tool_calls}` | tokens or count | `adk.experimental.root_agent.name`, `gen_ai.workflow.name`, `gen_ai.workflow.nested` | `ADK_EXPERIMENTAL_TELEMETRY` and schema v2; nested datapoints fold into every enclosing workflow (documented behaviour, metrics.md 2026-09-18) |

ADK's docs call the token histogram `gen_ai.client.token.usage`; the current semconv draft defines `gen_ai.client.inference.usage.input_tokens` and siblings (vendor guidance, 2026-10-05). Observe the name your installed semconv package emits before writing a dashboard.

### Names in Cloud Monitoring (vendor guidance, confirm in your export)

The name a dashboard or alert queries depends on the export path, and no Google page read on 2026-10-21 states it for ADK. Google's own agent alert templates query the histograms as `workload.googleapis.com/gen_ai.invoke_agent.duration` and `workload.googleapis.com/gen_ai.client.token.usage`, in PromQL `workload_googleapis_com:gen_ai_invoke_agent_duration_bucket` or `_count` and `workload_googleapis_com:gen_ai_client_token_usage_bucket`, with attribute dots turned into underscores (`gen_ai_agent_name`, `error_type`, `gen_ai_token_type`) on monitored resource `generic_node`, whose `namespace` label carries the agent key for token usage (Google's `agent-platform-alert-configuration` skill, read 21 October 2026). The OTLP path ADK 2.8.0 uses for Google Cloud (`telemetry.googleapis.com`) is documented as naming metrics with the `prometheus.googleapis.com` prefix plus a point-kind suffix (https://docs.cloud.google.com/stackdriver/docs/otlp/overview, 2026-10-20). List the metric descriptors in the target project before writing a query; when the deliverable is that descriptor lookup or the PromQL itself, consult the installed Google skill `cloud-monitoring-metric-selection` or `cloud-monitoring-promql-query` (from google/skills); if it is not installed, adk-engineer explains how to get it.

## Token arithmetic (`_token_usage.py`)

- A streamed call reports cumulative usage on each chunk. `TokenUsage.from_llm_responses` takes the newest report that has usage, so a trailing chunk without usage does not drop the figure. Summing chunks double counts.
- `input_token_count = prompt_token_count + tool_use_prompt_token_count`; cached tokens are part of the prompt count. `output_token_count = candidates_token_count + thoughts_token_count`. `total_tokens` is derived; the model-reported total is ignored. On `LiteLlm` routes (next bullets) the provider's total is the reliable figure and ADK's derived output is not, which is how this rule and `adk-operational-guardrails`' "prefer provider totals where reliable" fit together. On 2.12.0 both `trace_call_llm` and `trace_generate_content_result` set the usage attributes (`telemetry/tracing.py`, read 2026-10-25), so the `call_llm` and `generate_content` spans repeat one call's usage; sum `generate_content` spans only.
- `InvocationTokenTotals` sums per `invoke_agent` (that agent's own calls) and per `invoke_workflow` (every call inside it). Transport retries by the SDK multiply attempts, not logical calls; adk-agent-evaluation's `execution-evidence.md` states the same counting rule for evaluation runs.
- An `AgentTool` child runs through its own `Runner` with a throwaway in-memory session and a new invocation id, and only its state changes come back (2.12.0 `tools/agent_tool.py`, read 2026-10-25), so a saved parent session omits the child's model calls and their usage; a sub-agent in `sub_agents` with `mode='single_turn'` records them in the parent session. Spans keep the child under the parent's `execute_tool` span, so aggregate cost by trace, not by session export; inherited plugins see the child's calls under the child's invocation and session ids.
- On `LiteLlm`, ADK 2.12.0 stores the provider's `completion_tokens` as candidates and its reasoning tokens as thoughts, and output is candidates plus thoughts (`models/lite_llm.py` and `telemetry/_token_usage.py`, read 2026-10-25); where the provider's completion count already includes reasoning, as on OpenAI-style routes, output tokens and any cost built on them count reasoning twice. Derive output from `completion_tokens` alone on that path, or reconcile against gateway or billing rows; `invocation_summary.py` flags a call whose candidates plus thoughts exceed the reported total minus the prompt (`reasoning_counted_twice_on_N_calls`) and prices that call's output from candidates alone, while its token totals keep ADK's figures so they match dashboards. Key the price table by the session's `model_version`, which on `LiteLlm` is the provider's echo (`o4-mini`), not the span's request name (`openai/o4-mini`), or the call shows as `unpriced_model`. When an `AgentTool` child's model call fails, the parent records the failure as the tool's result text, not as a tool error, and the `execute_tool` span stays unset (observed offline, 2026-10-25), so neither the helper's tool-error count nor a status filter finds it; look for it in the child's own spans. LiteLLM's own captured ADK traces show the same arithmetic (BerriAI/litellm commit 5603724, MIT outside `enterprise/`, `scripts/lens_assets/fixtures/`, read 2026-10-25; fixtures read, not used).
- LiteLLM streaming needs the provider to include usage in the stream; 2.8.0 `lite_llm.py` sets `stream_options={"include_usage": True}` (source), a gap reported earlier as issue #3181 (community).

## What a plugin adds

| Plugin | Emits | Note |
| --- | --- | --- |
| `LoggingPlugin` | console lines with user content, agent flow, LLM request and response summaries, tool args and results | Terminal debugging aid, not a production sink |
| `DebugLoggingPlugin` | a file with whole prompts, responses, tool arguments and session state | Created readable only by its owner; treat as sensitive |
| `AutoTracingPlugin` | spans for in-scope Python functions with argument reprs | 2.7.0 redacts credential values from its attributes (CHANGELOG) |
| `BigQueryAgentAnalyticsPlugin` | rows, not spans (see [bigquery analytics](bigquery-analytics.md)) | Inherits `trace_id` from the ambient span; no duplicate spans |
| `_RequestIntercepterPlugin` (evaluation) | links `LlmRequest` to `LlmResponse.custom_metadata["__llm_request_key__"]` | Internal to the eval system; a pattern for request capture, not a public API |

Independent community project; not affiliated with or endorsed by Google.
