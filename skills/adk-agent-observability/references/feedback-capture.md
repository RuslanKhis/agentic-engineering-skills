# Feedback capture

Read when user or operator feedback should join telemetry and feed evaluation. The pattern below is vendor guidance from Google's agents-cli observability material (`feedback-mechanism.md`, skill version 1.8.0, 2026-09-30) adapted to this toolkit's boundaries; nothing here is an ADK API.

## Record shape

Capture feedback as a structured log record keyed by the same identifiers the rest of the telemetry uses, so one query joins feedback to spans, BigQuery rows and the stored session. `assets/feedback_record.schema.json` is a JSON Schema for the minimal record:

| Field | Source | Note |
| --- | --- | --- |
| `log_type` | constant `feedback` | Sink filter key |
| `service_name` | deployment name | Matches `OTEL_SERVICE_NAME` |
| `session_id` | the ADK session id (`gen_ai.conversation.id` on spans, `session_id` in BigQuery rows) | Opaque identifier; the join key |
| `invocation_id` | the invocation the user rated | Same value as `gcp.vertex.agent.invocation_id` and the BigQuery `invocation_id` column |
| `user_id` | the application's opaque user key | Never an email or display name |
| `score` | bounded numeric or enum (`1`, `-1`, or 1 to 5) | Decide the scale once |
| `category` | optional enum (`wrong_answer`, `tool_failed`, `too_slow`, `unsafe`, `other`) | Enables cohorts without reading text |
| `text` | optional free text | Retains PII until redacted; run protect-adk-sensitive-data's de-identification before storage or drop it |
| `trace_id` | optional, the trace of the rated invocation | Lets an operator open the trace from the feedback row |

Emit it with the host logger as structured JSON (`logger.log_struct` on Cloud Logging clients, or `logging` with a JSON formatter whose fields include `logging.googleapis.com/trace` so the record attaches to the trace). Do not put feedback into span attributes after the fact; spans are immutable once exported.

## Pipeline

1. A `POST /feedback` endpoint on the agent's HTTP surface (or the front-end gateway, adk-frontend-integration) validates the record against the schema, verifies the caller owns `session_id` (adk-tool-auth-and-secrets owns the identity check) and writes the log record.
2. A Cloud Logging sink with filter `jsonPayload.log_type="feedback"` routes records to a BigQuery table in the same dataset as `agent_events`, or to a dedicated feedback dataset with its own retention. Set a table expiration; feedback text ages into liability.
3. Join on `session_id` and `invocation_id` to `v_agent_response`, `v_llm_response` and `v_tool_error` for cohorts (negative feedback by tool, by model version, by latency bucket).
4. Negative feedback selects candidates for [trace to evaluation](trace-to-evaluation.md); the export runs the redaction step regardless of what the feedback record contained.

agents-cli provisions this chain (`agents-cli infra single-project --apply` creates the bucket, the `<project>_telemetry` dataset and sinks) when that collection is installed; the record contract above stays the same whether the infrastructure is generated or hand-built. Creating sinks, datasets and tables are approvals.

## What to watch

- Feedback rate (records per 1000 invocations) and negative share; both are low-volume and lag production by hours, so they inform SLO reviews rather than pages.
- Agreement between feedback and judge scores on the same invocations; disagreement calibrates the judge (adk-agent-evaluation).
- Records without a matching invocation in `agent_events` or in the session store: a correlation bug, usually a client sending its own ids.

Independent community project; not affiliated with or endorsed by Google.
