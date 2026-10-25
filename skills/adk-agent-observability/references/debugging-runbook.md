# Debugging from a trace

Read during an incident or when a single bad turn must be explained. The path is alert, then trace, then session, then reproduction, and each hop preserves an identifier. Names are google-adk 2.8.0 source unless labelled.

## 1. From the alert to a trace

- The alert names the metric, the dimension (`gen_ai.agent.name`, `gen_ai.tool.name`, `gen_ai.request.model`, `error.type`) and the window. Open Trace Explorer (or the third-party destination) filtered on the same span attribute and time window. On Agent Runtime the console's Traces tab offers a session view and a span view (vendor, 2026-10-01). Cloud Trace's filter grammar: `+gen_ai.tool.name:get_order` (exact value on any span), `^label:error.type` (key present on the root span), `error:true` (some span failed), `latency:2s` (trace duration at or above, no space before the unit). Predicates match at trace level, not on the same span, so a trace returned for `+gen_ai.tool.name:get_order error:true` may carry the error elsewhere; post-filter on the span you mean (Google's `cloud-trace-querying` skill, read 21 October 2026). For a cohort rather than one trace, the `_AllSpans` SQL in [SLO and alerting](slo-and-alerting.md) gives the error ratio by tool or model. When the deliverable is the live search, the span fetch or the correlated-log pull, consult the installed Google skill `cloud-trace-querying` (from google/skills; `cloud-logging-query-generation` for LQL beyond the `trace=` filter); if it is not installed, adk-engineer explains how to get it.
- Pick a representative trace: a failed one (`error.type` set, span status `ERROR`) and a slow one (long `invoke_agent` or `execute_tool`). Record `trace_id`, `gen_ai.conversation.id` and `gcp.vertex.agent.invocation_id` from the spans.
- If no spans match while the host reports requests, the export is broken: check the startup log for `Cannot determine GCP Project`, missing exporter packages, or a second provider owner ([export paths](export-paths.md)).

## 2. Read the trace

| Symptom in the waterfall | Likely cause | Next check |
| --- | --- | --- |
| `execute_tool` with `error.type` and `ERROR` status, tool did not raise | tool returned an error dict; `MCP_TOOL_ERROR` or `HTTP_ERROR` | tool response in BigQuery `TOOL_ERROR` or `TOOL_COMPLETED` row; the stored event's `function_response` |
| `generate_content` with `error.type` `429` or `5xx` | provider quota or incident | `gen_ai.client.operation.duration` by `gen_ai.request.model`; provider status page; adk-model-and-output-contracts for failover |
| `gen_ai.response.finish_reasons` is `max_tokens`, `safety`, `malformed_function_call` | output limit, safety block, bad function call | `LlmResponse.error_code` on the stored event; adk-model-and-output-contracts |
| many `generate_content` spans under one `invoke_agent` | tool loop or repair loop | `gen_ai.invoke_agent.inference_calls` histogram; adk-operational-guardrails budgets |
| long gap between spans | session load, pool admission, network, compaction | custom session span (optimise-adk-on-google-cloud `assets/session_observation.py`); `gen_ai.compaction.*` span |
| `invoke_agent` present but no `generate_content` | the google-genai instrumentor owns the inference span, or a callback short-circuited the model (2.8.0 records attributes when a plugin short-circuits) | check the instrumentor's spans; `before_model_callback` list |
| two `invoke_agent` spans per invocation, or orphan spans | two tracer owners (OpenInference beside native, or an application provider) | [export paths](export-paths.md) duplicate-span check |
| `invocation` span where dashboards expect `invoke_workflow` (or the reverse) | schema version differs by host | `ADK_TELEMETRY_SCHEMA_VERSION_OPT_IN`, `GOOGLE_CLOUD_AGENT_ENGINE_ID` |
| content attributes hold `{}` | `ADK_CAPTURE_MESSAGE_CONTENT_IN_SPANS=false`; this is the intended production state | read the stored session, not the span |
| spans named `Request Path` or `Response Path` with resource `service.name=modelarmor` in the same trace | Model Armor screened the prompt or the answer; `gcp.modelarmor.violations` lists the policy hits and `gen_ai.security.policy.id` names the template (Google's `agent-platform-alert-configuration` skill, read 21 October 2026) | the template and its policy are protect-adk-sensitive-data's; a rising violation share per agent, joined on `trace_id`, is a safety alert candidate in [SLO and alerting](slo-and-alerting.md) |

Timings on the span are the measurement; `usage` on the `generate_content` span is the last chunk's cumulative figure for that call.

## 3. From the trace to the session

- `gen_ai.conversation.id` is the ADK session id. Fetch the session from the session service the deployment uses (`SESSION_SERVICE_URI`, Agent Runtime sessions API, the database). Agent Runtime does not log Sessions or Memory Bank operations (vendor), so the session service is the only record of the events.
- Export the session to JSON (an object with `events`, or the events array; `session.model_dump_json(exclude_none=True)` gives the first form) and run the helpers. `invocation_summary.py` shows, per invocation, how many logical model calls happened, which tools failed, where the wall time went (`longest_steps`) and whether usage was missing; its `invocation_id` matches the span attribute.
- BigQuery rows for the same `invocation_id` add `ttft_ms`, `finish_reason`, `tool_origin` and the sanitised error text; correlate on `trace_id` when `enable_otel_correlation` or the ambient span was present.
- Logs: query `trace="projects/{project}/traces/{trace_id}"` in Cloud Logging for application and ADK log records; `google_adk.*` logger names identify the module. On Agent Runtime, stdout is in `reasoning_engine_stdout`; on Cloud Run the request record and the container output are separate log ids ([export paths](export-paths.md)).

## 4. Reproduce

1. Convert the session to an eval case with `events_to_eval_set.py --select tool_error` (or `all`) and review the redacted output.
2. Replay deterministically with a scripted model and the real tools' doubles (adk-agent-evaluation's Runner tests), asserting the tool call and the failure. For a tool fault, inject it with Environment Simulation or the backend double; for a model fault, script the response that the trace shows (`finish_reason`, function call arguments).
3. Only then run live, with approval, against an isolated session; compare `invocation_summary.py` on the new session with the production one (model calls, tool errors, usage).
4. Write the fix's test from the reproduction, and keep the eval case in the regression set.

## 5. Close the loop

- Record in the incident note: alert, trace id, invocation id, root cause category (model, tool, dependency, infrastructure, telemetry), fix, and the regression case id.
- When the incident meets an agreed postmortem trigger (user harm, an unapproved outside action, data exposure, a sustained quality drop), extend the note into a blameless review with [operations handover](operations-handover.md#agent-incident-review-blameless-postmortem) and the postmortem template.
- If the alert did not fire or fired late, adjust the SLI or the burn-rate window ([SLO and alerting](slo-and-alerting.md)); if the trace lacked a needed attribute, add it under the experimental gate or as a custom span and note the version dependency ([compatibility](compatibility.md)).
- If the trace contained content it should not have, hand the finding to protect-adk-sensitive-data; set `ADK_CAPTURE_MESSAGE_CONTENT_IN_SPANS=false` and `ADK_TELEMETRY_IGNORE_RUN_CONFIG=1` as the immediate mitigation (issue #7311 describes `AuthCredential` fields in `gcp.vertex.agent.tool_call_args`, community, open at 2026-10-07).

Independent community project; not affiliated with or endorsed by Google.
