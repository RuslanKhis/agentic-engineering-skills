# SLIs, SLOs and alerts

Read when defining what "healthy" means for an agent and when an operator is paged. The method is independent evidence (Google SRE Workbook, "Implementing SLOs", https://sre.google/workbook/implementing-slos/); the metric names are ADK 2.8.0 source; the agent-specific SLI lists and Online Monitors are vendor material and are labelled so.

## Method

1. Measure first. Take two to four weeks of the metrics below (or a load test when the agent is new) and write down the observed distribution before choosing a target. A target with no baseline is a guess that pages people.
2. Express each SLI as good events over total events for a stated window. Never set 100 percent; the model, the tools and the network each fail on their own schedule.
3. Alert on error-budget burn (fast burn over a short window plus slow burn over a long window), not on every threshold crossing. Keep raw-threshold alerts for conditions that need an immediate human (telemetry stopped, every tool failing, budget exhausted).
4. Review the SLO when the agent's model, tools or traffic mix changes; adk-model-and-output-contracts and adk-agent-evaluation own the quality measurements that justify a new target.

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
| Quality | `aiplatform.googleapis.com/online_evaluator/scores` for `evaluation_metric_name=task_success` below 0.8 for 1800 s with 60 s mean alignment (Google's example) | Vendor recipe; calibrate the threshold on your judge |
| Analytics pipeline | `BigQueryAgentAnalyticsPlugin.get_drop_stats()` any reason non-zero, exported by the host | Rows silently missing otherwise ([bigquery analytics](bigquery-analytics.md)) |

Every alert names the dashboard, the trace query and the runbook step ([debugging runbook](debugging-runbook.md)) in its documentation field.

## Online Monitors (vendor, Agent Platform)

Agent and Model Evaluations reached GA on 2026-07-31 (Google Developers Blog). Online Monitors grade a sample of production Cloud Trace spans about every 10 minutes with configurable sampling rate, maximum per run and filters, using judge metrics such as Task Success, Tool Use Quality, Safety, Trajectory and Final Response, with any Model Garden model as judge; scores are written to Cloud Monitoring as `aiplatform.googleapis.com/online_evaluator/scores` labelled by `evaluation_metric_name`, and quality alerts create incidents that link to the graded traces (quality-alerts page, 2026-10-01). Requirements and costs: Cloud Trace export enabled, a per-service agent identity that reads traces, judge model calls billed per evaluation plus GCS storage. Restrict creation of monitors to administrators; each monitor is recurring spend. Treat a monitor score as a sampled estimate with judge error; a drop is a reason to pull the sampled traces into [trace to evaluation](trace-to-evaluation.md), not a verdict.

## Dashboards

One page per agent: request rate and error ratio (`invoke_agent`), latency heatmap, tool error ratio by tool, model latency and errors by model, tokens per invocation, inference calls per invocation, and the quality score when a monitor exists. Add a telemetry-health tile (points per minute) so an export failure is visible on the same page. Keep the queries keyed on attributes observed in your export; the span and metric names are in development and change by ADK version ([compatibility](compatibility.md)).

Independent community project; not affiliated with or endorsed by Google.
