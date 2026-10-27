# Latency observability for the support agent (Agent Runtime, ADK 2.8.0)

Status: designed offline from the repo and one session export. Nothing was deployed, enabled or queried.
Every metric name, column name and PromQL below is `unverified: confirm against the project's own export`.

## 1. What the one saved session says (offline, hand-computed)

`exports/session-sess-7f31.json`, invocation `inv-91`, event timestamps only (the helper script
`invocation_summary.py` could not run in this session: no shell). Event gaps approximate span durations.

| Step | Seconds | Share of 11.81 s |
| --- | --- | --- |
| model call 1 (to `lookup_order` call) | 1.88 | 16% |
| tool `lookup_order` | 0.31 | 3% |
| model call 2 (to `issue_refund` call) | 1.40 | 12% |
| tool `issue_refund` | 6.79 | 57% |
| model call 3 (final reply) | 1.42 | 12% |
| model total / tools total | 4.71 / 7.10 | 40% / 60% |

- One sample is a lead, not a diagnosis: `issue_refund` (a payments-provider HTTP call, `timeout=10.0` in
  `app/clients/http.py`, no retry visible) dominates here. Confirm across many traces before acting on it.
- Session loading is not observable in the export: the first event is the user message and nothing precedes it.
- Usage: prompt tokens grow 2210 → 2390 → 2510 per call; no streaming partials, so no double-count risk here.
- Gap found: `issue_refund` returns `{"status": "error", ...}`. ADK flags tool errors only for a truthy
  `error`/`isError` key or an exception, so refund failures will look healthy in `error.type`, the tool-error
  alert and the helper. Fix is a product decision (changing the return shape changes what the model sees); until
  then do not rely on the tool-error SLI for these tools.

## 2. Instrumentation

ADK 2.8.0 already emits what is needed, so no application code was added.

| Time to attribute | Signal | How |
| --- | --- | --- |
| Whole invocation | `gen_ai.invoke_agent.duration` | histogram, `gen_ai.agent.name`, `error.type` |
| Model | `generate_content` spans; `gen_ai.client.operation.duration` | per call and per `gen_ai.request.model` |
| Tools | `execute_tool` spans; `gen_ai.execute_tool.duration` | per `gen_ai.tool.name` |
| Host latency | `aiplatform.googleapis.com/reasoning_engine/request_latencies` | built in |
| Session loading and host overhead | residual: host `request_latencies` minus `invoke_agent` duration, plus the gap before the first child span in a trace | inferred, not measured |

Session loading: on Agent Runtime the platform owns the session service and ADK 2.8.0 emits no dedicated span
for it (not confirmed in source this session). The residual is the honest attribution until a measured span
exists. A measured span would need a wrapper around the session service the runtime uses; that is a separate
change and I did not guess at the AdkApp wiring.

Env changes (`deploy/agent_engine.env`):

| Variable | Value | Effective default if absent |
| --- | --- | --- |
| `GOOGLE_CLOUD_AGENT_ENGINE_ENABLE_TELEMETRY` | `true` | unset (no export) |
| `ADK_CAPTURE_MESSAGE_CONTENT_IN_SPANS` | `false` | content captured (on) |
| `OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT` | `NO_CONTENT` | `NO_CONTENT` |
| `ADK_EXPERIMENTAL_TELEMETRY` | `true` | off (no token metrics) |
| `OTEL_SEMCONV_STABILITY_OPT_IN` | not set (keeps the prompt-bearing log event off) | absent |

Schema v2 is the default on Agent Runtime, so the top span is `invoke_workflow {entrypoint}`, not `invocation`.
Key nothing on `gen_ai.system`.

Prompts stay out: span content gate off, message-content mode `NO_CONTENT`, no `LoggingPlugin` or
`DebugLoggingPlugin` in the app (checked `app/agent.py`; deployment is `root_agent` only). Tool arguments and
responses are covered by the same span gate. Also keep `google_adk.*` loggers off DEBUG in production. The
refund `reason` is customer text, so the gate matters. `server.py` (Cloud Run, in-memory sessions) is a
different host from the Agent Runtime deployment and is not instrumented here.

## 3. SLO (provisional)

No baseline numbers were provided, only "p95 doubled". A target without a baseline is a guess, so:

- SLI: share of `invoke_agent` invocations that finish within T seconds, over a 28-day window.
- Provisional objective: 95% within T = 12.8 s (a histogram bucket edge, so the ratio is exact; the one sample
  took 11.8 s). Replace T with the pre-regression p95 plus headroom once two to four weeks of data exist
  (or a pre-regression window is found). Bucket edges: 6.4, 12.8, 25.6.
- Companion SLI: invocation success (`error.type` empty), objective chosen from baseline.
- Budget is 5%, so the SRE 14.4x fast-burn factor (72% bad) is unreachable in practice; use 6x (30% bad) fast
  and 1x (5% bad) slow.

## 4. Alerts (drafts, nothing created)

```promql
# Latency SLI, fast burn: page. Both windows must exceed.
(1 - sum(rate(workload_googleapis_com:gen_ai_invoke_agent_duration_bucket{le="12.8"}[1h])) / sum(rate(workload_googleapis_com:gen_ai_invoke_agent_duration_count[1h]))) > 0.05 * 6
# repeat with [5m]; slow burn: 0.05 * 1 over [6h] and [3d] -> ticket
```

| Alert | Condition | Route |
| --- | --- | --- |
| Latency fast burn | above, 1 h and 5 m | page (channel not chosen) |
| Latency slow burn | 6 h and 3 d | ticket |
| Telemetry stopped | no `invoke_agent` points while `reasoning_engine/request_count` > 0 | page |
| Tool slow | p95 of `gen_ai.execute_tool.duration` per `gen_ai.tool.name` above its baseline, 10 min | ticket |
| Model slow or erroring | `gen_ai.client.operation.duration` p95 and `error.type` 429/5xx | ticket |

Each alert's documentation field must name this file, the trace query below and the runbook step.

Attribution query for Trace Analytics (columns unverified; needs the `_Trace` bucket linked to BigQuery):
group spans by trace, summing duration where `gen_ai.operation.name` is `generate_content` (model) and
`execute_tool` (tools, by `gen_ai.tool.name`) against the root span's duration; the remainder is session load and
overhead.

## 5. Approvals needed before any of this works (not done)

1. Enable `telemetry.googleapis.com` (Cloud Trace is on, the Telemetry API is not; without it exports fail
   quietly). Also check Cloud Logging and Cloud Monitoring.
2. Grant the Agent Runtime service identity `roles/telemetry.writer` (or `tracesWriter` plus `metricWriter`) and
   `roles/logging.logWriter`.
3. Redeploy with `deploy/deploy_agent_engine.sh` (project and region to be named by the owner; region default
   in the script is `europe-west1`).
4. Create alert policies and choose notification channels (Terraform or console).
5. Then verify: one synthetic invocation shows spans in Trace Explorer with no `gcp.vertex.agent.llm_request`
   content, and metric descriptors list; confirm the real metric names and fix the PromQL.

## 6. Questions I could not ask, and the assumptions I used

- What was p95 before and after, and when did it change? Assumed unknown; T is a placeholder.
- Which host serves production, Agent Runtime or the Cloud Run `server.py`? README says Cloud Run; the request
  says Agent Runtime. Assumed Agent Runtime.
- Who receives pages? Assumed undecided; no channel referenced.
- Did anything change at the time of the regression (model, payments provider, prompt, session length)? Unknown;
  prompt tokens grow by ~100-180 per call, so check context growth too.

## 7. Evidence

| Check | Tier / outcome |
| --- | --- |
| Session timings above | offline (hand-computed), pass, one session |
| `invocation_summary.py`, `events_to_eval_set.py` | not run: no shell available |
| In-memory exporter test with real `Runner` | not run: no SDK, not installed per instructions |
| Spans, metrics, alerts live | blocked: Telemetry API disabled, approvals pending |
| Repo unit tests | not run: no shell |
