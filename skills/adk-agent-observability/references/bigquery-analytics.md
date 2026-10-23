# BigQuery Agent Analytics

Read when structured per-event analytics, cohort queries or joins to feedback are needed. Source statements are `plugins/bigquery_agent_analytics_plugin.py` in google-adk 2.8.0; documented behaviour is adk-docs `integrations/bigquery-agent-analytics.md` (2026-10-05). The plugin is a row writer, not a tracer: it emits no OpenTelemetry spans and inherits `trace_id` from the ambient span.

## Constructor and configuration (2.8.0)

`BigQueryAgentAnalyticsPlugin(project_id, dataset_id, table_id=None, config=None, location="US", **kwargs)`; unknown kwargs log a warning, known ones override `BigQueryLoggerConfig` fields. The plugin requires the `bigquery-analytics` extra (`pyarrow`) and uses the Storage Write API (billed).

| `BigQueryLoggerConfig` field | Default | Operational meaning |
| --- | --- | --- |
| `table_id` | `agent_events` | Created on first use, partitioned by day on `timestamp` |
| `clustering_fields` | `event_type`, `agent`, `user_id` | Query cost on the common filters |
| `event_allowlist`, `event_denylist` | none | Drop event types you do not need (for example `LLM_REQUEST` when prompts must not leave the process) |
| `max_content_length` | 500 KiB per text block | Truncation sets `is_truncated` |
| `batch_size`, `batch_flush_interval` | 1, 1.0 s | Default writes one row per batch; raise `batch_size` under load and watch `queue_full` drops |
| `queue_max_size` | 10000 | In-memory queue bound; overflow drops with reason `queue_full` |
| `shutdown_timeout` | 10 s | Rows left after this are dropped (`shutdown_timeout`, `shutdown_cancelled`) |
| `flush_on_run_end` | `True` | Synchronous flush on the response path; `False` moves it to the background writer at the cost of landing delay |
| `exactly_once_delivery` | `False` | Committed streams with explicit offsets; not lossless (drops after retry exhaustion, offset conflicts, replacement-stream failure, rotation backoff); consumes `CreateWriteStream` quota |
| `content_formatter` | none | `Callable[[content, event_type], Any]` run first on raw content; a raising formatter writes `[FORMATTER_FAILED]` and increments an incident counter |
| `payload_column_denylist` | none | Project out `content`, `content_parts`, `attributes` or `latency_ms` at write time; identity and correlation columns cannot be denied; denying `attributes` also removes `attributes.otel` and `custom_metadata` |
| `enable_otel_correlation` | `False` | Adds `attributes.otel.{trace_id, span_id}` from the ambient span at emission time; a join key, not a foreign key |
| `custom_metadata_allowlist` | none | Keys or `prefix*` patterns copied from `event.custom_metadata` through the same safety pipeline |
| `log_session_metadata`, `custom_tags` | `True`, `{}` | Session metadata into `attributes.session_metadata`; static tags such as environment |
| `gcs_bucket_name`, `connection_id` | none | Offload large or binary content to GCS with `ObjectRef` columns |
| `create_views`, `view_prefix` | `True`, `v` | One typed view per event type (`v_llm_response`, `v_tool_error`, ...); set a distinct prefix per table in a shared dataset |
| `final_response_tool_names` | empty | Treat a named tool's completion as the `AGENT_RESPONSE` |
| `auto_schema_upgrade` | `True` | Additive column changes only, once per schema version (table label `adk_schema_version`, value `2` in 2.8.0) |

## Rows that matter for operations

| Event type | Use |
| --- | --- |
| `LLM_RESPONSE` | `usage_prompt_tokens`, `usage_completion_tokens`, `usage_total_tokens`, `usage_cached_tokens`, `usage_thinking_tokens`, `usage_tool_use_tokens`, `total_ms`, `ttft_ms`, `model_version`, `finish_reason`, and a sanitised `error_message` while `status` stays `OK` (2.7.0 and later) |
| `LLM_ERROR`, `TOOL_ERROR`, `AGENT_ERROR`, `INVOCATION_ERROR`, `NODE_ERROR` | Failure cohorts; tracebacks are sanitised |
| `TOOL_STARTING`, `TOOL_COMPLETED`, `TOOL_ERROR` | `tool_name`, `tool_origin` (`LOCAL`, `MCP`, `SUB_AGENT`, `A2A`, `TRANSFER_AGENT`, `TRANSFER_A2A`, `UNKNOWN`), `total_ms` |
| `AGENT_TRANSFER`, `AGENT_STATE_CHECKPOINT`, `EVENT_COMPACTION`, `TOOL_PAUSED` | Multi-agent and long-running flows; the `attributes.adk` envelope carries `source_event_id`, `node`, `branch`, `scope`, `pause_kind`, `function_call_id` |
| `USER_MESSAGE_RECEIVED`, `AGENT_RESPONSE` | Join points for feedback and for eval-case selection |
| `HITL_*` | Human-in-the-loop requests; credential requests carry arguments, see redaction limits |

Known gap (community, open at 2026-10-07): MCP results with `isError` can be logged as `TOOL_COMPLETED` with `status=OK` (issue #7112). Until fixed, detect MCP errors in the `tool_result` JSON in your queries, and offline with `invocation_summary.py`, which treats `isError` / `is_error` as a tool error.

## Deduplication and delivery

- Every row has `event_id` (32 hex, assigned before enqueue; 2.7.0 and later), preserved across Storage Write API retries. Deduplicate with `ROW_NUMBER() OVER (PARTITION BY event_id ORDER BY timestamp)` and keep row 1; rows written before schema version 2 have `NULL` and need `timestamp, event_type, span_id` instead. Duplicate rows on retry were reported as issue #6465 (community) before `event_id`.
- Poll `plugin.get_drop_stats()` from the host and export the counters as a metric; alert on any non-zero reason: `queue_full`, `arrow_prep_failed`, `retry_exhausted`, `non_retryable`, `unexpected_error`, `shutdown_timeout`, `shutdown_cancelled`, plus offset-conflict reasons in exactly-once mode (documented behaviour).
- `await plugin.flush()` waits for the current loop's pending rows; call it in the shutdown path before the loop closes.
- Cross-region datasets (outside the `US` multi-region) route to the region owning the write stream (documented fix); verify with a synthetic row before relying on an `EU` dataset.
- A view-DDL re-run on every request produced thousands of jobs per hour on earlier versions (issue #7017, community) and is listed as fixed in 2.10.0; on 2.8.0 check the BigQuery jobs history after deployment.

## IAM and prerequisites (documented)

BigQuery API enabled; dataset created in advance (the table is created by the plugin); the agent principal holds `roles/bigquery.jobUser` at project level and `roles/bigquery.dataEditor` on the table (or the dataset when the plugin must create the table); `roles/storage.objectCreator` and `roles/storage.objectViewer` on the bucket for GCS offload. Agent Runtime deployments need the plugin on an `App` and ADK at or above the version the doc names for that path. Creating datasets and granting roles are approvals. An Agents CLI project scaffolded with `--bq-analytics` wires the plugin from `BQ_ANALYTICS_DATASET_ID`, `BQ_ANALYTICS_CONNECTION_ID` (`{location}.{connection_id}`) and `BQ_ANALYTICS_GCS_BUCKET`, provisions the dataset, connection and bucket in Terraform and grants the runtime identity `roles/bigquery.dataOwner` and `roles/bigquery.jobUser` (Agents CLI 1.11.0, `google-agents-cli-observability` skill and scaffold `service.tf`, read 22 October 2026); when that generated infrastructure is the deliverable, consult the installed `google-agents-cli-observability` skill; if it is not installed, adk-engineer explains how to get it.

## Redaction limits (delegated policy, operational facts here)

Built-in redaction replaces values under an exact set of credential key names (lower-cased, hyphens normalised) and any `temp:`-prefixed key, recursively, and sanitises credential patterns in error text and URIs. It does not match camelCase variants (`clientSecret`, `accessToken`; issue #3845, community, open per the doc), application-specific key names or free text. Decide the capture policy with protect-adk-sensitive-data; then implement it here with `event_denylist` (drop `LLM_REQUEST`, `HITL_CREDENTIAL_REQUEST`), `content_formatter` (mask fields before serialisation) and `payload_column_denylist` (never store `content`). Masking in a dashboard is too late; BigQuery retention and access are separate approvals.

## Correlation to traces and logs

Rows carry `trace_id`, `span_id` and `parent_span_id`. `trace_id` is the ambient OpenTelemetry trace id when a span is active (Agent Runtime's invocation span, the ADK runner span, or one you opened), else a generated 32-hex per-invocation id. `span_id` values are plugin-internal; only `trace_id` joins to Cloud Trace. With `enable_otel_correlation=True`, `attributes.otel.span_id` is the real ambient span id at emission time. The `invocation_id` column equals the ADK invocation id, which also appears as `gcp.vertex.agent.invocation_id` on spans and as `invocation_id` in `invocation_summary.py` rows, so the three sources join on it.

## Query recipes to adapt

```sql
-- Tool error ratio by tool and day (deduplicated)
WITH rows AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY event_id ORDER BY timestamp) AS rn
  FROM `project.dataset.agent_events`
  WHERE event_type IN ('TOOL_COMPLETED', 'TOOL_ERROR')
    AND DATE(timestamp) >= DATE_SUB(CURRENT_DATE(), INTERVAL 7 DAY))
SELECT DATE(timestamp) AS day, JSON_VALUE(content, '$.tool') AS tool_name,
       COUNTIF(event_type = 'TOOL_ERROR') / COUNT(*) AS error_ratio, COUNT(*) AS calls
FROM rows WHERE rn = 1 GROUP BY day, tool_name ORDER BY day, error_ratio DESC;
```

Check the view columns in your dataset (`v_tool_completed.tool_name`, `v_llm_response.usage_total_tokens`) before using them; column names are documented behaviour at 2026-10-05, not a contract. Looker Studio templates and a Looker Block exist (vendor); switch a shared Looker Studio report to viewer credentials before sharing it.

## Reading the table with the Agent Analytics SDK

Google's `bigquery-agent-analytics` package (GoogleCloudPlatform/BigQuery-Agent-Analytics-SDK, v0.6.1 of 2026-10-20, commit 68ef3fa; Apache-2.0, no NOTICE; `README.md`, `SDK.md`, `CHANGELOG.md` and `examples/`, read 2026-10-22; vendor library, not executed here) is the read side of the `agent_events` table the plugin writes. It depends on `google-adk>=1.0.0`, so it installs beside an existing pin. What it adds that this reference's SQL does not: trace reconstruction across `trace_id`, `span_id` and `attributes.adk.source_event_id`; seven deterministic `SystemEvaluator` metrics (latency, turn count, tool error rate, token efficiency, context-cache hit rate, cost per session, time to first token) and judge metrics over stored sessions; a CLI (`bq-agent-sdk evaluate ... --exit-code`, exit 0 pass, 1 fail, 2 infrastructure error) that adk-release-engineering can gate on; continuous-query SQL templates for session scoring, error analysis and Pub/Sub alerting that need a BigQuery Enterprise reservation with continuous-query slots (its README prices that at roughly $6 an hour for 100 slots, vendor figure dated 2026-10-20, and points to a Cloud Scheduler plus Cloud Run streaming evaluation as the cheaper form); and a label on every job it submits (`sdk`, `sdk_version`, `sdk_surface`, `sdk_feature`) so its own spend is attributable in `INFORMATION_SCHEMA.JOBS_BY_PROJECT`. Three of its own caveats carry into any number you publish from it: `token_efficiency` prefers the provider's total, which on Gemini includes thought tokens, while `cost_per_session` multiplies only input and output tokens and so is not an invoice reconciliation when thinking is on, which is why this reference's own arithmetic (output = candidates plus thoughts) stays the dashboard definition; `context_cache_hit_rate` passes by default when the telemetry lacks `cached_content_token_count` unless `fail_on_missing_telemetry=True`; and its `pass^k` is `(c/n)^n`, not the unbiased estimator adk-agent-evaluation records. The SDK's view of the table was written against the plugin's documented columns; confirm it reads the schema version your plugin writes (`adk_schema_version` label above) before trusting a metric.

The call shapes, as documented at v0.6.1 (`SDK.md`, read 2026-10-22; confirm each with `bq-agent-sdk <command> --help` and the installed package before relying on a name):

- `Client(project_id=, dataset_id=, table_id="agent_events", location=None, gcs_bucket_name=None, endpoint=<AI.GENERATE endpoint>, connection_id=None, verify_schema=True)`.
- CLI global options `--project-id` (`BQ_AGENT_PROJECT`), `--dataset-id` (`BQ_AGENT_DATASET`), `--table-id`, `--location`, `--format json|text|table`; `doctor` for a health check; `get-trace --session-id=` or `--trace-id=` with `--user-id`, `--root-agent-name`, `--experiment-id`, `--label` filters.
- `evaluate --evaluator=<latency|error_rate|turn_count|token_efficiency|context_cache_hit_rate|ttft|cost|llm-judge> [--criterion=correctness] [--threshold=] [--agent-id=] [--last=24h] --exit-code`; `evalbench-score --job-id= --evaluator=<correctness|hallucination|sentiment> --threshold= --exit-code --format text [--import-version=]`.
- `client.drift_detection(golden_dataset="<one table name in the client's dataset>", filters=TraceFilter(agent_id=, start_time=))` returns a `DriftReport` with `coverage_percentage`, `uncovered_questions`, `details` (raw and unique counts, method) and `summary()`; `client.deep_analysis(filters=, configuration=AnalysisConfig(mode="auto_group_using_semantics", top_k=))` returns categories with counts and examples.
- `EvalSuite(name=)` holds `EvalTaskDef(task_id=, session_id=, description=, category=EvalCategory.CAPABILITY | REGRESSION, expected_trajectory=, expected_response=, thresholds=, tags=, is_positive_case=)`; `check_health(pass_history={task_id: [bool, ...]})` and `auto_graduate(pass_history=, threshold_runs=)` take the run history you supply, so persisting it is the project's work; `to_json()` and `from_json()` version the suite in git; `to_eval_dataset(category=)` feeds `PerformanceEvaluator.evaluate_batch`.

This section is the one home for these facts; the release skill's gate and feedback references point here rather than restating them.

Independent community project; not affiliated with or endorsed by Google.
