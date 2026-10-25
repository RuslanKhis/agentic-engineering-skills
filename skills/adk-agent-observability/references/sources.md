# Sources

Every claim in this skill is one of: **source-verified** (read in a local checkout of google/adk-python on 2026-10-07), **documented behaviour** (adk-docs with the page date), **vendor guidance** (Google Cloud or another provider's documentation with the date printed on the page or the fetch date), **independent evidence**, or **community** (issue or forum reports, not reproduced). [Compatibility](compatibility.md) lists what was not verified.

## ADK source and changelog

| Reference | Type | Notes |
| --- | --- | --- |
| google/adk-python tag `v2.8.0` (2026-08-25): `telemetry/context.py`, `_schema_version.py`, `_stable_semconv.py`, `_experimental_semconv.py`, `_metrics.py`, `_token_usage.py`, `_instrumentation.py`, `tracing.py`, `node_tracing.py`, `setup.py`, `google_cloud.py`, `_agent_engine.py`, `_agent_engine_metric_exporter.py`, `_adk_attributes.py`; `plugins/bigquery_agent_analytics_plugin.py`, `logging_plugin.py`, `debug_logging_plugin.py`, `auto_tracing_plugin.py`; `evaluation/eval_set.py`, `eval_case.py`, `common.py`, `local_eval_sets_manager.py`, `request_intercepter_plugin.py`; `events/event.py`, `models/llm_response.py`, `models/lite_llm.py`, `flows/llm_flows/functions.py`, `tools/mcp_tool/mcp_tool.py`, `tools/openapi_tool/openapi_spec_parser/rest_api_tool.py`, `cli/cli_deploy.py`, `agents/run_config.py` | source-verified | Pinned behaviour |
| google/adk-python main at 2.11.0 (2026-10-01): `telemetry/context.py` (`ADK_EXPERIMENTAL_TELEMETRY_FEATURES`), `telemetry/google_cloud.py` (`gcp.resource_type`), `CHANGELOG.md` | source-verified | Later behaviour, labelled by version |
| google/adk-docs: `docs/observability/index.md`, `traces.md` (2026-08-07), `metrics.md` (2026-09-18), `logging.md` (2026-09-21), `docs/integrations/bigquery-agent-analytics.md` (2026-10-05), `cloud-trace.md`, `langfuse.md`, `phoenix.md`, `arize-ax.md`, `weave.md`, `mlflow-tracing.md`, `docs/evaluate/index.md` | documented behaviour, fetched 2026-10-07 | Span and metric tables, export setup, plugin configuration, eval set format |

## Google Cloud and OpenTelemetry

| URL | Date | Used for |
| --- | --- | --- |
| https://github.com/open-telemetry/semantic-conventions-genai (agent spans, metrics, registry) | 2026-10-05 | Development status, span and attribute names, Opt-In content attributes, token usage metric naming |
| open-telemetry/semantic-conventions-genai commit 9ffc7e0 (2026-10-21; Apache-2.0): `reference/scenarios/google-adk/{README.md,conformance.yaml,scenario.py,pyproject.toml}`, `docs/gen-ai/gen-ai-events.md`, `gen-ai-agent-spans.md`; open-telemetry/semantic-conventions-conformance commit 3a5dd62: `README.md`, `tools/gen-ai/` | read 2026-10-22 | The reference scenario's implemented operations and expected violations in [signals and schema](signals-and-schema.md); the `gen_ai.evaluation.result` event in [trace to evaluation](trace-to-evaluation.md); the planned Weaver check in [validation](validation.md); neither repository executed |
| https://github.com/Arize-ai/openinference (google-adk instrumentation `CHANGELOG.md`) and https://github.com/open-telemetry/opentelemetry-python-contrib/tree/main/instrumentation-genai (README) | read 2026-10-22 | OpenInference 1.0 floor on ADK 2.10 and 1.0.3 workflow spans; GenAI instrumentations moved to opentelemetry-python-genai |
| https://docs.cloud.google.com/stackdriver/docs/instrumentation/ai-agent-adk | 2026-09-30 | APIs, writer roles, `EVENT_ONLY` guidance, invalid `true` under latest semconv |
| https://docs.cloud.google.com/stackdriver/docs/otlp/overview | fetched 2026-10-07 | Telemetry API OTLP ingestion, quota project header, billing as Prometheus samples |
| https://docs.cloud.google.com/trace/docs/quotas | fetched 2026-10-07 | Span attribute, name, event and retention limits |
| https://docs.cloud.google.com/monitoring/quotas | fetched 2026-10-07 | Custom metric descriptor, label, series and retention limits |
| https://docs.cloud.google.com/trace/docs/troubleshooting | fetched 2026-10-07 | Export troubleshooting (also cited by optimise-adk-on-google-cloud) |
| https://docs.cloud.google.com/logging/docs/structured-logging | fetched 2026-10-07 | `logging.googleapis.com/trace`, `spanId`, `trace_sampled` |
| https://docs.cloud.google.com/agent-builder/agent-engine/manage/tracing | 2026-10-01 | `GOOGLE_CLOUD_AGENT_ENGINE_ENABLE_TELEMETRY`, required APIs, optional semconv and capture settings, legacy `roles/cloudtrace.agent` |
| https://docs.cloud.google.com/gemini-enterprise-agent-platform/scale/runtime/monitoring | 2026-10-01 | `ReasoningEngine` resource, built-in metrics, overview dashboard, ADK metrics as user-defined metrics |
| https://docs.cloud.google.com/agent-builder/agent-engine/manage/logging | fetched 2026-10-07 | `reasoning_engine_stdout`, child resources not logged |
| https://developers.googleblog.com/en/agent-and-model-evaluations-in-gemini-enterprise-agent-platform-are-now-ga/ | 2026-07-31 | Online Monitors GA |
| https://docs.cloud.google.com/gemini-enterprise-agent-platform/optimize/evaluation/quality-alerts | 2026-10-01; re-read 2026-10-20 version on 2026-10-21 | `online_evaluator/scores`, `evaluation_metric_name` values `task_success`, `final_response_quality_v1`, `tool_use_quality_v1`, `hallucination_v1`, alert example, incidents linking to traces |
| https://docs.cloud.google.com/monitoring/api/ref_v3/rest/v3/projects.alertPolicies (Aligner enum) | fetched 2026-10-21 | `ALIGN_MEAN` numeric only; `ALIGN_PERCENTILE_50` for distribution values |
| https://docs.cloud.google.com/trace/docs/analytics | 2026-10-20 | `PROJECT_ID.LOCATION._Trace.Spans._AllSpans`, `observability.googleapis.com`, linked dataset needed for alert policies on query results |
| https://docs.cloud.google.com/stackdriver/docs/otlp/overview | 2026-10-20 | `prometheus.googleapis.com` naming of OTLP metrics through the Telemetry API |
| https://cloud.google.com/bigquery/pricing#data-ingestion-pricing | fetched 2026-10-07 | Storage Write API billing |

## Google recipes

| Reference | Date | Used for |
| --- | --- | --- |
| google/adk-recipes commit be63596: `core/python/ambient-quality-agent/README.md` (Apache-2.0; vendor sample) | read 2026-10-22 | AQuA as a source of failing conversation traces and deduplicated insights in [trace to evaluation](trace-to-evaluation.md); the three telemetry sources it reads |
| GoogleCloudPlatform/BigQuery-Agent-Analytics-SDK v0.6.1 (commit 68ef3fa, 2026-10-20; Apache-2.0, no NOTICE): `README.md`, `SDK.md`, `CHANGELOG.md`, `deploy/continuous_queries/README.md`, `examples/evalbench_score_gate.sh` | read 2026-10-22 | The SDK section of [bigquery analytics](bigquery-analytics.md): evaluators, CLI exit codes, continuous queries, job labels, token and cache caveats |

## Other vendor documentation

| URL | Date | Used for |
| --- | --- | --- |
| https://github.com/google/agents-cli/blob/main/skills/google-agents-cli-observability/SKILL.md, `references/cloud-trace-and-logging.md`, `feedback-mechanism.md`, scaffold `telemetry.tf`, `service.tf`, `fast_api_app.py` and `src/google/agents/cli/deploy/*.py` (v1.11.0, released 2026-10-20) | read 2026-10-22 from a local copy | Completion upload path ignoring the content flag, env defaults set by `agents-cli deploy`, sink filter and host-dependent table names, Go boolean semantics, generated roles, `--bq-analytics` env names, feedback record and sink pattern (unchanged since 1.8.0) |
| https://github.com/google/skills, `skills/cloud/` (`agent-platform-alert-configuration`, `cloud-run-alert-configuration`, `google-cloud-slo-alert-configuration`, `cloud-monitoring-*`, `cloud-trace-querying`, `cloud-logging-*`; Apache-2.0) | read 2026-10-21 from a local copy | Cloud Monitoring names of ADK metrics (vendor guidance), burn-rate PromQL, `_AllSpans` SQL conditions, Online Monitor metric ids and the aligner rule, Cloud Run host metrics, alert-condition gotchas, trace filter grammar, Model Armor span names, notification and sink facts; routed to for the artefacts themselves |
| https://langfuse.com/docs/evaluation/evaluation-methods/llm-as-a-judge | fetched 2026-10-07 | Judges on sampled traces |
| https://langfuse.com/docs/observability/features/masking | fetched 2026-10-07 | `mask_otel_spans` scope |
| https://www.arize.com/docs/ax/evaluate/run-evals-on-traces.md | fetched 2026-10-07 | Evaluations over traces |

## Independent evidence

| Work | Finding used |
| --- | --- |
| Google SRE Workbook, "Implementing SLOs" (https://sre.google/workbook/implementing-slos/) | SLIs as good/total ratios, targets below 100 percent, multiwindow burn-rate alerting |

## Community reports (not reproduced)

google/adk-python issues #7311 (`AuthCredential` fields in tool-call span attributes; `off` does not disable content), #7162 (REST tool keys in args, fixed), #7112 (MCP `isError` rows as `TOOL_COMPLETED`, open), #7024 (service-account key ADC `invalid_scope` on export), #7017 (view DDL per request, fixed 2.10.0), #6915 and #6692 (span retention growth, fixed 2.10.0), #6465 (duplicate BigQuery rows before `event_id`), #6361 (`user.id` dropped with old genai instrumentor), #6328 (mTLS tracing 401, fixed infrastructure-side), #4829 (thinking tokens absent, fixed), #3845 (camelCase credential keys not redacted), #3181 (LiteLLM streaming usage); Arize-ai/openinference issues #3857, #3844, #3177 and an Arize community thread (2026-02-20) on duplicate or orphan spans beside native ADK spans. They are listed as symptoms to test for on the target.

## Repository references

Sibling skills are cited by name: protect-adk-sensitive-data (content policy and capture baseline in `references/implementation-recipes.md`), optimise-adk-on-google-cloud (`references/gke-serving.md`, `assets/session_observation.py`), adk-agent-evaluation (`references/execution-evidence.md` usage-counting rule, evaluation design), deploy-adk-on-google-cloud (first deployment), adk-operational-guardrails (budgets and loop limits), adk-model-and-output-contracts (finish reasons, failover), adk-frontend-integration and adk-tool-auth-and-secrets (feedback endpoint and identity). Google's `google-agents-cli-observability` skill is an optional composition per `docs/integrations/agents-cli.md`.

| promptfoo/promptfoo commit 15bcb0d, `site/docs/guides/evaluate-google-adk.md` | read 2026-10-22 | Native-span assertion shapes in [trace to evaluation](trace-to-evaluation.md); not executed |

## Operations handover and incident review

| URL | Date | Used for |
| --- | --- | --- |
| https://sre.google/sre-book/launch-checklist/ | read 2026-10-25 (book © 2017) | Handover readiness: monitoring the monitoring, alert management, release process, external dependencies, standard procedures |
| https://sre.google/sre-book/postmortem-culture/ and https://sre.google/sre-book/example-postmortem/ | read 2026-10-25 (book © 2017) | Postmortem triggers, blameless review, review before sharing, section order of the template |
| https://ico.org.uk/for-organisations/report-a-breach/personal-data-breach/personal-data-breaches-a-guide/ | read 2026-10-25 (undated; some ICO pages under review after the Data (Use and Access) Act) | The notification decision in the postmortem template |
