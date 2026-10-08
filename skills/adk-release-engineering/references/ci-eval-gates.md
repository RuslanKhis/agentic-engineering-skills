# Evaluation gates in CI

Read this when a pull request, merge or nightly job must decide whether an agent change ships. adk-agent-evaluation owns the cases, the dev/holdout discipline and the CSV checker; this reference schedules them, sets the threshold, repeat, cache and cost policy, and defines what NOT RUN means.

## Three tiers

| Tier | Trigger | Runs | Model calls | Gate |
| --- | --- | --- | --- | --- |
| 1 Deterministic | Every pull request | Scripted-model unit and Runner tests; `adk conformance test` in `replay` mode (the default; `--mode=live` is the other choice, verified in `cli/cli_tools_click.py` 2.8.0); schema and eval-set validation with the pinned ADK models; the inventory helper | None | Any failure blocks merge. `adk conformance test` raises `ClickException` with the failed count, so its exit code is usable (verified in `cli/conformance/cli_test.py` 2.8.0) |
| 2 Bounded live | Label (`run-live-eval`) or merge to main | `AgentEvaluator.evaluate(..., num_runs=N, output_file=CSV)` on the CI subset with deterministic criteria `tool_trajectory_avg_score` and `response_match_score`, then `check_eval_results.py` | Agent inference only; no judge | Checker exit 0 required; exit 1 or a missing CSV blocks promotion |
| 3 Judge | Nightly or release candidate | Judge metrics (`final_response_match_v2`, `rubric_based_*`, `hallucinations_v1`, `safety_v1`) with `judge_model` and `num_samples` pinned; efficiency metrics (2.10.0 and later) reported, not gated | Agent plus judge | Compared against the previous nightly; a drop beyond the agreed margin opens a release blocker |

The adk-docs evaluation page (fetched 2026-10-07) recommends `tool_trajectory_avg_score` and `response_match_score` for CI/CD because they are "fast, predictable, and suitable for frequent automated checks", judge metrics with `num_samples` majority vote for semantic checks, and `adk conformance test` as a pull-request gate. Hamel Husain's evals FAQ (2025, practitioner) recommends a CI set of roughly a hundred purpose-built cases (core features, past bugs, edge cases), assertions over LLM judges in CI, and sampled reference-free judges on production traffic. Anthropic's test-development guidance and OpenAI's evaluation best practices (both vendor, fetched 2026-10-07) agree on discriminative cases and continuous evaluation rather than one-off benchmarks.

## Use the gate that already exists

In 2.8.0 and on main, `adk eval` prints an "Eval Run Summary" with "Tests failed: N" and exits 0 whatever the counts; only missing dependencies raise `ClickException` (verified in `cli/cli_tools_click.py`). A shell step that runs `adk eval` and checks `$?` is a report, not a gate. It also has no `--num_runs` or parallelism option (community issue #4410, open). Google's own `agents-cli` eval skill says the same of its command: "`eval run` exits 0 whatever the scores are, so the numbers you paste are the gate, not the exit code" (fetched 2026-10-07, vendor).

Three gates do fail by exit code:

1. `AgentEvaluator.evaluate` and `evaluate_eval_set` write the detailed CSV when `output_file` is set and then `assert not failures` (verified in `evaluation/agent_evaluator.py` 2.8.0), so a pytest test produces both the CSV and a failing exit code. Without a `test_config.json`, the defaults are `tool_trajectory_avg_score: 1.0` and `response_match_score: 0.8` (`_DEFAULT_EVAL_CONFIG`, `evaluation/eval_config.py`); write the config anyway so the thresholds are reviewed.
2. adk-agent-evaluation's `scripts/check_eval_results.py` over that CSV. Rows are one per metric per invocation (one per run), carrying `eval_set_id, eval_id, metric_name, threshold, score, eval_status`; the checker enforces exact row counts (`cases x runs_per_case x criteria`), thresholds equal to the contract, every row `PASSED`, finite scores.
3. `adk conformance test` in replay mode, which raises `ClickException` with the failed count (verified in `cli/conformance/cli_test.py`). `--mode live` is reported as unimplemented (community issue #7290, open 2026-09-25); treat replay as the only conformance tier.

Point the gate at the installed sibling skill:

```bash
CHECKER="${ADK_AGENT_EVALUATION_DIR:?path to the installed adk-agent-evaluation skill}/scripts/check_eval_results.py"
python "$CHECKER" --csv results/ci.csv --expectations evals/ci-expectations.json
```

The expectations file names the `eval_set_id`, every case ID, `runs_per_case` and each criterion's threshold and comparison. Keep it in git beside the eval set; a case added to the set without a row in the expectations is a count mismatch and fails, which is the intended behaviour.

## Threshold and repeat policy

- `tool_trajectory_avg_score` at `1.0` for cases whose tool sequence is the requirement; use `match_type` `EXACT`, `IN_ORDER` or `ANY_ORDER` in `ToolTrajectoryCriterion` (2.8.0) when order is not the requirement, `ignore_args` from 2.9.0 when argument values vary, and add a deterministic assertion for prohibited extra mutations, which trajectory matching does not catch.
- `response_match_score` (ROUGE) at a threshold measured on the baseline, not guessed. Run the baseline five times, take the minimum per case, and set the threshold below it with a margin; record the measurement in the changelog.
- Repeats: `num_runs=3` on tier 2 (`AgentEvaluator` defaults to `NUM_RUNS = 2`). Two aggregation rules apply and the record must say which one gated. ADK passes a case when `statistics.mean(scores)` across the runs meets the threshold (`agent_evaluator.py` 2.8.0), so the pytest step is an averaging gate. The sibling checker reads the per-run rows and requires every one to be `PASSED`, so it is a strict gate: a case that passes two of three fails and is visible. Run both; a case that passes on the mean and fails the strict check is the flakiness list for the release. For each such case, make the behaviour deterministic (trajectory criterion, tighter tool contract, mocked tool with `random_seed` in environment simulation, rubric) or move it to tier 3 with a recorded pass-rate target. Do not delete it; Google's `agents-cli` eval skill (fetched 2026-10-07, vendor) says the same: flaky evals reveal non-determinism, fix with rubrics or more specific instructions, do not delete the signal. It also suggests `temperature=0`; on Gemini 3 models adk-model-and-output-contracts keeps temperature at 1.0, so prefer rubrics, repeats and trajectory criteria there.
- Mocked tools: `tools/environment_simulation` (2.8.0, experimental) injects tool results with `InjectionConfig` (`match_args`, `injection_probability`, `injected_latency_seconds`, `random_seed`) and a mock strategy; pin `random_seed` in CI so the injected outcome is the same on every run.
- Judge metrics: `num_samples=5` (the 2.8.0 default and the built-in flake control through majority vote; `num_samples=0` is rejected from 2.10.0) and a pinned `judge_model`. Report the judge disagreement rate across samples alongside the score; rising disagreement is a case-quality finding. Rate-limit judge calls (`parallelism_limit` in `JudgeModelOptions`; `agents-cli eval grade --qps 5` is the equivalent there).

## Cache and cost ceiling

ADK 2.8.0 has no response cache for evaluation runs; conformance replay is the no-model-call tier. For tier 2 and 3:

- Cache `.adk/eval_history/*.evalset_result.json` (written by `LocalEvalSetResultsManager`, verified in 2.8.0) between runs keyed on the eval-set hash, prompt hash, model ID and judge ID, so a run on unchanged inputs can be compared with the previous result and so a re-run after an infrastructure failure does not discard earlier evidence. promptfoo's CI guide (fetched 2026-10-07, vendor) caches provider responses for 24 hours and tags runs with the commit SHA; tag the ADK result files the same way (directory named by SHA).
- Set a cost ceiling the test enforces before dispatch: `EVAL_MAX_CASES` and `EVAL_MAX_RUNS` read by the pytest module, which skips with a NOT RUN marker when `cases x runs` exceeds the ceiling rather than running a partial cohort. ADK does not enforce spend; the test does. adk-operational-guardrails owns runtime budgets; this is a CI budget.
- Record the planned and actual case, run and judge-sample counts in the job summary. A cohort that stopped early is reported as partial, with the unrun cases named.

## NOT RUN semantics

A skipped job, a missing CSV, a zero-case eval, an empty expectations list or a checker exit 2 is NOT RUN, and NOT RUN blocks promotion exactly as a failure does. The workflow asset makes the checker step depend on the CSV existing and fails the job when it does not. Never let a green deterministic tier stand in for an unrun live tier in the release record; the changelog row names the tier that ran. From 2.10.0, `AgentEvaluator.evaluate` raises `ValueError` when no eval cases are evaluated instead of passing (CHANGELOG, 2026-09-24); on 2.8.0 the checker's exact-count rule catches the same condition.

## Known pitfalls to test for

Community reports (google/adk-python issues, not reproduced here; check the target's version against each):

| Report | Effect on a gate | Status |
| --- | --- | --- |
| #7258 `safety_v1` resolved to a newer managed metric version with an inverted scale | Safety threshold silently meant the opposite | Fixed 2.10.0 ("pin the specific version for safety_v1", CHANGELOG 2026-09-24) |
| #7414 lower-is-better custom metric fails although rows say `PASSED` | Custom metric direction disagrees with the gate | Open as of 2026-10-05; the sibling checker's `comparison: lte` handles direction at the gate |
| #6725 `NOT_EVALUATED` results discarded | A metric that never ran looked like no failure | 2.9.0 maps a metric that never ran to `NOT_EVALUATED`; the exact-count rule in the checker treats a missing row as a failure |
| #4155 MCP toolset race under parallel evaluation | Intermittent tool failures that look like flakiness | Serialise MCP-backed cases or isolate toolsets per run |
| #6683 Vertex session IDs rejected in evals | Eval setup fails against `VertexAiSessionService` | Use an in-memory or isolated session service for eval runs |
| Legacy `.test.json` schema | Old files need `AgentEvaluator.migrate_eval_data_to_new_schema` (2.8.0) | Migrate and store as `.evalset.json`; the inventory helper flags legacy files |
| 2.7.0: `adk eval` previously bypassed `App.plugins` (#5503); agent crash before any metric now fails the eval | Older versions could pass without exercising plugins or on a crash | Fixed 2.7.0 |

## Separate CI cases from the holdout

The CI set is the development set plus regression cases from incidents. The holdout is run once per release candidate with the frozen method (adk-agent-evaluation's quality-iteration reference) and its result recorded in the changelog; it is not a nightly job, because a nightly holdout stops being a holdout. Replenish it from reviewed production samples ([production feedback](production-feedback.md)).

## Completion

Each tier has a trigger, a command, a gate and an evidence destination; the expectations file matches the eval set; the pass-rate policy for any repeated case is written down; the cost ceiling is enforced in code; NOT RUN is a failure in the workflow; the holdout is used once per release and recorded.
