# SLIs, SLOs and alerts

Read when defining what "healthy" means for an agent and when an operator is paged. The method is independent evidence (Google SRE Workbook, "Implementing SLOs", https://sre.google/workbook/implementing-slos/); the metric names are ADK 2.8.0 source; the agent-specific SLI lists and Online Monitors are vendor material and are labelled so.

## Method

1. Measure first. Take two to four weeks of the metrics below (or a load test when the agent is new) and write down the observed distribution before choosing a target. A target with no baseline is a guess that pages people.
2. Express each SLI as good events over total events for a stated window. Never set 100 percent; the model, the tools and the network each fail on their own schedule.
3. Alert on error-budget burn (fast burn over a short window plus slow burn over a long window), not on every threshold crossing. Keep raw-threshold alerts for conditions that need an immediate human (telemetry stopped, every tool failing, budget exhausted).
4. Review the SLO when the agent's model, tools or traffic mix changes; adk-model-and-output-contracts and adk-agent-evaluation own the quality measurements that justify a new target.
5. Shape each condition to its data class. Error ratios are sparse, so a Z-score against a near-zero standard deviation is unstable; burn rate is the right form. Dynamic baselines (Z-score, moving average, seasonal offset) adapt to slow drift, so keep a static threshold beside them; a seasonal `offset 1w` comparison fires again a week later when the anomaly becomes the baseline, so track one direction and avoid `abs()`. In Cloud Monitoring, omit `duration` on a PromQL condition whose lookback exceeds 25 h (it is rejected with `INVALID_ARGUMENT`) and use `300s` on shorter ones; keep PromQL on one line without comments; inside Terraform heredocs write `${var.x}`, not `var.x` (Google's `agent-platform-alert-configuration` and `cloud-run-alert-configuration` skills, read 21 October 2026).

## Candidate SLIs for an ADK agent

| SLI | Good / total | ADK signal | Evidence |
| --- | --- | --- | --- |
| Invocation success | `invoke_agent` datapoints without `error.type` / all `invoke_agent` datapoints | `gen_ai.invoke_agent.duration` with `error.type` label | source metric; the ratio is a generic availability SLI (independent) |
| Invocation latency | datapoints under the threshold / all | same histogram; buckets 0.1 to 409.6 s | source; choose the threshold from the baseline percentile |
| Tool reliability by tool | `execute_tool` datapoints without `error.type` / all, per `gen_ai.tool.name` | `gen_ai.execute_tool.duration`; dict-reported errors count when the tool's `_detect_error_in_response` hook reports them (MCP `isError`, REST `error`) | source; "tool-call error rate by tool" appears as an agent SLI in vendor material (Agent Runtime monitoring page, Langfuse and Arize docs) |
| Model call reliability | `generate_content` datapoints without `error.type` / all, per `gen_ai.request.model` | `gen_ai.client.operation.duration` | source; `error.type` is the provider status code for `APIError` |
| Tokens per invocation | distribution of `adk.experimental.invoke_agent.total_tokens` per agent | experimental metric, `ADK_EXPERIMENTAL_TELEMETRY=true` | source; "tokens per successful task" is vendor material; divide by successful invocations yourself |
| Model calls per invocation | `gen_ai.invoke_agent.inference_calls` distribution | source histogram, buckets 0 to 512 | a loop guard belongs to adk-operational-guardrails; the metric shows the loop |
| Task success, trajectory, safety, final response quality | sampled judge scores | Online Monitors (below) or adk-agent-evaluation on exported cases | vendor; judge outputs need calibration before they gate anything |
| Escalation or hand-off rate | invocations ending in a hand-off tool or state flag / all | your own tool name in `gen_ai.tool.name`, or a BigQuery `AGENT_TRANSFER` row | vendor material as an SLI; the measurement is yours |
| Feedback rate | negative feedback records / invocations with feedback | structured feedback logs ([feedback capture](feedback-capture.md)) | your data; low volume, high value |

Write each SLI with its window, its measurement query and the dimension it is sliced by (`gen_ai.agent.name`, `gen_ai.tool.name`, `gen_ai.request.model`). Workflow-grain metrics carry `adk.experimental.root_agent.name` instead of an agent name; exclude `gen_ai.workflow.nested=true` datapoints before summing (documented behaviour, metrics.md 2026-09-18).

### Measurement queries

Invocation success as a Cloud Monitoring burn-rate condition, grouped by agent so one policy covers every agent (Google's `agent-platform-alert-configuration` skill, read 21 October 2026; the metric name is vendor guidance, confirm it in your export per [signals and schema](signals-and-schema.md)):

```promql
sum(rate(workload_googleapis_com:gen_ai_invoke_agent_duration_count{error_type!=""}[1h])) by (gen_ai_agent_name)
/ sum(rate(workload_googleapis_com:gen_ai_invoke_agent_duration_count[1h])) by (gen_ai_agent_name)
> (1 - 0.999) * 14.4
```

The fast-burn policy requires this over 5 m `and` 1 h; the slow-burn policy uses 6 h `and` 3 d with factor 1.0. The host's own availability counters pair with it ([export paths](export-paths.md)).

Tool and model reliability can also be measured from exported spans with a `condition_sql` alerting policy over the Observability Analytics view, where span `status.code = 2` is an error; group by `JSON_VALUE(resource.attributes, '$."cloud.resource_id"')` as well when several agents share the project, keep only failing rows with `HAVING`, and let `row_count_test` fire on any row:

```sql
SELECT JSON_VALUE(attributes, '$."gen_ai.tool.name"') AS tool,
       COUNTIF(status.code = 2) * 100.0 / COUNT(*) AS error_pct
FROM `{project}.{location}._Trace.Spans._AllSpans`
WHERE JSON_VALUE(attributes, '$."gen_ai.operation.name"') = 'execute_tool'
GROUP BY tool HAVING error_pct > 5.0
```

The model variant filters `gen_ai.request.model IS NOT NULL` and groups by model. Prerequisites: the `observability.googleapis.com` API and the `_Trace` bucket, plus a BigQuery dataset linked to that bucket when the query feeds an alert policy or an external tool (https://docs.cloud.google.com/trace/docs/analytics, 2026-10-20); `condition_sql` needs Terraform provider 6.x and takes no manual timestamp filter (Google's `agent-platform-alert-configuration` skill, read 21 October 2026).

## Alerts worth having

| Alert | Condition | Why |
| --- | --- | --- |
| Error budget fast burn | invocation error ratio over 1 h exceeds 14.4 times the budget rate (SRE Workbook multiwindow example) | Pages a human while budget remains |
| Error budget slow burn | ratio over 6 h or 3 d exceeds 1 to 6 times the budget rate | Ticket, not page |
| Telemetry stopped | no `gen_ai.invoke_agent.duration` points for N minutes while request count on the host is above zero (`run.googleapis.com/request_count`, `aiplatform.googleapis.com/reasoning_engine/request_count`) | Export failure looks like success without this |
| Tool failing | `error.type` ratio for one `gen_ai.tool.name` above the baseline for 10 min | Isolates a dependency from the model |
| Model provider errors | `gen_ai.client.operation.duration` points with `error.type` in `429`, `5xx` rising | Quota and provider incidents |
| Loop or runaway | p99 of `gen_ai.invoke_agent.inference_calls` above the configured limit | Pairs with adk-operational-guardrails budgets |
| Spend | sum of `adk.experimental.invoke_agent.total_tokens` per hour above the planned envelope | Metric is experimental; keep the alert tolerant to renames |
| Quality | `aiplatform.googleapis.com/online_evaluator/scores` on resource `aiplatform.googleapis.com/OnlineEvaluator` with `evaluation_metric_name` one of `task_success`, `final_response_quality_v1`, `tool_use_quality_v1`, `hallucination_v1`, below 0.8 (0.9 for hallucination) for 300 to 1800 s (quality-alerts page, 2026-10-20) | Vendor recipe; calibrate the threshold on your judge. Align with `ALIGN_PERCENTILE_50`: the score is a distribution and `ALIGN_MEAN` is defined only for numeric values (Aligner reference, https://docs.cloud.google.com/monitoring/api/ref_v3/rest/v3/projects.alertPolicies, fetched 2026-10-21), although Google's page example still shows `ALIGN_MEAN` |
| Analytics pipeline | `BigQueryAgentAnalyticsPlugin.get_drop_stats()` any reason non-zero, exported by the host | Rows silently missing otherwise ([bigquery analytics](bigquery-analytics.md)) |

Every alert names the dashboard, the trace query and the runbook step ([debugging runbook](debugging-runbook.md)) in its documentation field. An alert nobody receives fails silently: Cloud Monitoring notifies from the service agent `service-{project_number}@gcp-sa-monitoring-notification.iam.gserviceaccount.com`, which needs `roles/pubsub.publisher` on a Pub/Sub channel's topic; a topic with a message storage policy or in-transit enforcement cannot receive notifications; delivery failures appear in Cloud Logging as `resource.type="stackdriver_notification_channel" AND severity>=ERROR` (Google's `cloud-monitoring-notification-channels-configuration` and `cloud-logging-query-generation` skills, read 21 October 2026). Attaching a channel is an approval, never a guess.

When the deliverable is the alerting policy itself (Terraform, Online Monitor provisioning, traffic-pattern classification), consult the installed Google skill `agent-platform-alert-configuration` (from google/skills), which writes Terraform only and proposes a full policy suite by default; for a formal SLO on the host's request metrics, `google-cloud-slo-alert-configuration`; for the channel, `cloud-monitoring-notification-channels-configuration`. If one is not installed, adk-engineer explains how to get it.

## Online Monitors (vendor, Agent Platform)

Agent and Model Evaluations reached GA on 2026-07-31 (Google Developers Blog). Online Monitors grade a sample of production Cloud Trace spans about every 10 minutes with configurable sampling rate, maximum per run and filters, using judge metrics such as Task Success, Tool Use Quality, Safety, Trajectory and Final Response, with any Model Garden model as judge; scores are written to Cloud Monitoring as `aiplatform.googleapis.com/online_evaluator/scores` labelled by `evaluation_metric_name`, and quality alerts create incidents that link to the graded traces (quality-alerts page, 2026-10-01). Requirements and costs: Cloud Trace export enabled, a per-service agent identity that reads traces, judge model calls billed per evaluation plus GCS storage. Monitors are created through the console or the `OnlineEvaluatorServiceClient` (v1beta1) with predefined metric specs and `random_sampling.percentage` (default 10), not through Terraform (Google's `agent-platform-alert-configuration` skill, read 21 October 2026). Restrict creation of monitors to administrators; each monitor is recurring spend. Treat a monitor score as a sampled estimate with judge error; a drop is a reason to pull the sampled traces into [trace to evaluation](trace-to-evaluation.md), not a verdict.

## Dashboards

One page per agent: request rate and error ratio (`invoke_agent`), latency heatmap, tool error ratio by tool, model latency and errors by model, tokens per invocation, inference calls per invocation, and the quality score when a monitor exists. Add a telemetry-health tile (points per minute) so an export failure is visible on the same page. Keep the queries keyed on attributes observed in your export; the span and metric names are in development and change by ADK version ([compatibility](compatibility.md)). When the deliverable is the widget itself, write the query with the installed Google skill `cloud-monitoring-promql-query` or `cloud-monitoring-list-time-series-request`, then consult `cloud-monitoring-chart-generation` (from google/skills); if one is not installed, adk-engineer explains how to get it.

Independent community project; not affiliated with or endorsed by Google.
