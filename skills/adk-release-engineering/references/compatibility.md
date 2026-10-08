# Compatibility and evidence boundaries

Read this before relying on any version-dependent behaviour in this skill. The pinned reference is google-adk **2.8.0** (tag `v2.8.0`, released 2026-08-25), whose source was read on 2026-10-07. Later behaviour comes from the adk-python main branch at 2.11.0 (2026-10-01) and its CHANGELOG. Keep the target's pins; a version decision is a separate request.

## Verified in 2.8.0 source

| Surface | Behaviour | File |
| --- | --- | --- |
| `adk eval AGENT EVAL_SET...` | Options `--config_file_path`, `--print_detailed_results`, `--eval_storage_uri`; `eval_set.json:case_a,case_b` selects cases; auto-discovers `test_config.json` beside a single eval set file; prints per-set passed and failed counts and exits 0 whatever the counts (only missing dependencies raise `ClickException`); no `--num_runs` option | `cli/cli_tools_click.py` |
| `AgentEvaluator.evaluate` / `evaluate_eval_set` | `num_runs` default `NUM_RUNS = 2`; per metric, `statistics.mean(scores)` across runs is compared with the threshold; `output_file` writes one CSV row per metric per invocation (`eval_set_id, eval_id, metric_name, threshold, score, eval_status`, written with pandas) before `assert not failures`; `criteria=` dict is deprecated in favour of `eval_config`; `migrate_eval_data_to_new_schema` converts legacy `.test.json` | `evaluation/agent_evaluator.py` |
| `EvalConfig.criteria` | Metric name to a bare float threshold or a criterion object (`LlmAsAJudgeCriterion`, `RubricsBasedCriterion`, `HallucinationsCriterion`, `ToolTrajectoryCriterion` with `match_type` `EXACT`, `IN_ORDER`, `ANY_ORDER`); defaults without a config `tool_trajectory_avg_score: 1.0`, `response_match_score: 0.8`; `custom_metrics` with `code_config` | `evaluation/eval_config.py`, `evaluation/eval_metrics.py` |
| `JudgeModelOptions` | `judge_model` default `"gemini-2.5-flash"`, `num_samples` default 5, `parallelism_limit` default 1; the LLM-backed and audio user simulators also default to `gemini-2.5-flash` | `evaluation/eval_metrics.py` L84, `evaluation/simulation/llm_backed_user_simulator.py` L60 |
| Environment simulation | `InjectionConfig` with `injection_probability`, `match_args`, `injected_latency_seconds` (at most 120) and `random_seed`; mock strategy applied when no injection matches | `tools/environment_simulation/environment_simulation_config.py` |
| `PrebuiltMetrics` | `tool_trajectory_avg_score`, `response_evaluation_score`, `response_match_score`, `safety_v1`, `final_response_match_v2`, `rubric_based_final_response_quality_v1`, `hallucinations_v1`, `rubric_based_tool_use_quality_v1`, `per_turn_user_simulator_quality_v1`, `multi_turn_task_success_v1`, `multi_turn_trajectory_quality_v1`, `multi_turn_tool_use_quality_v1`; no efficiency metrics | `evaluation/eval_metrics.py` |
| Eval set files | `.evalset.json` (local and GCS managers), legacy `.test.json` for `AgentEvaluator`, results under `.adk/eval_history/*.evalset_result.json` locally or `evals/eval_history/` on GCS | `evaluation/local_eval_sets_manager.py`, `gcs_eval_sets_manager.py`, `local_eval_set_results_manager.py` |
| `adk conformance record` / `test` | `test --mode replay` (default) or `live`, `--generate_report`, `--report_dir`; failed tests raise `ClickException` with the count | `cli/cli_tools_click.py`, `cli/conformance/cli_test.py` |
| `adk deploy cloud_run` | Project, region, service name, app name, port, ADK version and related options; no traffic, tag or revision options | `cli/cli_tools_click.py` |
| `adk deploy agent_engine` | `--agent_engine_id` updates an existing resource; `--env_file`, `--requirements_file`, `--agent_engine_config_file` | `cli/cli_tools_click.py` |
| `adk optimize` | Experimental GEPA prompt optimisation via sampler and optimizer config files | `cli/cli_tools_click.py` |
| Default agent model | `LlmAgent.DEFAULT_MODEL = 'gemini-3.5-flash'` | `agents/llm_agent.py` L239 |

## Version table from the CHANGELOG (2.9.0 to 2.11.0)

| Version | Date | Change relevant to this skill |
| --- | --- | --- |
| 2.2.0 | 2026-06-04 | `LlmAgent` default model moved to `gemini-3-flash-preview`; judge default unchanged |
| 2.7.0 | 2026-08-13 | `test_config.json` auto-discovered for a single eval file; CSV export of eval results; eval fails when the agent crashes before any metric; `App.plugins` wired through eval paths |
| 2.9.0 | 2026-09-10 | `FallbackModel` added (adk-model-and-output-contracts covers it); `ignore_args` on tool trajectory evaluation; LLM-as-judge calls parallelised; per-invocation token spend telemetry |
| 2.10.0 | 2026-09-24 | Efficiency metrics `token_usage_v1`, `invocation_duration_v1`, `inference_call_count_v1`, `tool_call_count_v1`: informational, always on, never fail a case, a threshold on them is rejected (verified in main `eval_metrics.py` and adk-docs criteria page); `AgentEvaluator.evaluate` and `evaluate_eval_set` raise `ValueError` when no eval cases are evaluated; `num_samples=0` rejected at construction; `safety_v1` pinned to a specific metric version; missing conformance recordings raise a clear error |
| 2.11.0 | 2026-10-01 | Conformance runs report replay and recording failures; Vertex multi-turn mapping fix |
| main | 2026-10-07 | `JudgeModelOptions.judge_model` default still `"gemini-2.5-flash"` (main `eval_metrics.py` L113) |

## Vendor documentation state (dated)

| Surface | State | Source (page date) |
| --- | --- | --- |
| adk-docs evaluate page | Recommends `tool_trajectory_avg_score` and `response_match_score` for CI/CD, judge metrics with `num_samples` majority vote, `adk conformance test` as a PR gate; examples use `judge_model: "gemini-flash-latest"` (an alias) | fetched 2026-10-07 |
| Cloud Run traffic | `--no-traffic --tag`, `update-traffic --to-tags`, `--to-revisions`, in-flight requests complete | https://docs.cloud.google.com/run/docs/rollouts-rollbacks-traffic-migration (fetched 2026-10-07) |
| Agent Runtime revisions and traffic split | **Pre-GA (Preview), `v1beta1`**; immutable revisions on versioned-field updates, `trafficSplitManual` or `trafficSplitAlwaysLatest`, direct revision query, keep-n-latest garbage collection, archived revisions unrecoverable, 950 per agent and 6,000 per project-region | https://docs.cloud.google.com/gemini-enterprise-agent-platform/scale/runtime/manage-revisions-and-traffic (2026-10-07) |
| Cloud Deploy canary for Cloud Run | `automaticTrafficControl`, `canaryDeployment.percentages`, verify/predeploy/postdeploy tasks, `gcloud deploy rollouts advance` | Cloud Deploy canary documentation (2026-10-05), reviewed by the research pass |
| Agent Platform Evaluations | GA 2026-07-31; offline over traces filtered by version or time; online monitors with sampling; metric `aiplatform.googleapis.com/online_evaluator/scores` | Reviewed by the research pass 2026-10-07; not exercised |
| `agents-cli` deploy skill v1.8.0 | States Agent Runtime has no revision-based rollback; stale against the page above | fetched 2026-10-07 |
| Gemini deprecations and Vertex model versions | See [model migration](model-migration.md) | both 2026-10-07 |

The Gemini deprecations page, the Vertex model versions page and the Agent Runtime revisions and traffic page were re-read on 2026-10-08: the page dates above moved, and no shutdown or retirement date, replacement, Pre-GA status, traffic-split mode or revision limit used by this skill changed.

## Not verified

- Agent Platform Evaluations, Cloud Deploy canary fields and the developer-forum sizing advice were read from documentation and forum text by the research pass, not exercised.
- Community issue numbers in [CI eval gates](ci-eval-gates.md) are reports, not reproductions.
- Agent Runtime revision behaviour end to end; this skill read the documentation page and did not exercise the API.
- Vertex AI Prompt Management and Langfuse version semantics beyond their documentation pages.
- Any cost figure; cost ceilings in the workflow asset are placeholders the project measures.
