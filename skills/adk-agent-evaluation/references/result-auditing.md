# Result auditing and release decisions

Use this mode when checking existing evidence, diagnosing aggregate success with failed trials, or designing a gate. First record what constitutes a successful conversation, the expected cases/repetitions/metrics, and where each observation's identity comes from.

## Check the measured units

ADK 2.8.0 can aggregate repetitions into a passing case average while individual CSV rows fail. A CSV row is one metric observation, not necessarily a complete trial. Its detailed CSV has no guaranteed repetition ID. Require provenance before joining metrics into per-trial booleans; identical responses and row position are not reliable identifiers.

For equally repeated cases, observed `pass@k` is the fraction of cases with at least one successful trial; observed `pass^k` is the fraction with all trials successful. When cases are variants of one scenario (same intent, different data), also report the scenario score, where a scenario passes only when every variant passes: a case average hides an agent that solves one variant and fails its sibling, and this consistency across variants is not `pass^k` across repeated trials (AppWorld's `scenario_goal_completion`, StonyBrookNLP/appworld commit 42b5bcf, `src/appworld/evaluator.py`, read 2026-10-25). Libraries estimate rather than observe: Google's BigQuery Agent Analytics SDK (v0.6.1, `multi_trial_performance_evaluator.py`, read 2026-10-22) computes `pass@k` as `1 - C(n-c, k) / C(n, k)` and `pass^k` as `(c/n)^n`, with `n` trials and `c` passes; the second is a plug-in estimate that differs from the unbiased `C(c, k) / C(n, k)`, so say which formula a reported figure used and never compare the two as if they were one. tau2-bench's `pass_hat_k(num_trials, success_count, k)` is the unbiased form, `math.comb(success_count, k) / math.comb(num_trials, k)`, and raises when trials are fewer than `k` rather than returning a number; it counts a trial successful only when its reward is within 1e-6 of 1, excludes simulations that ended in an infrastructure error from the denominator, and reports `pass_hat_k` for every `k` up to the smallest trial count any case has (`src/tau2/metrics/agent_metrics.py`; sierra-research/tau2-bench v2.0 line, commit 05736c2, MIT, read 2026-10-22; benchmark method, not benchmark data). Restate those three rules for any helper you write: refuse `k` above the trial count, keep infrastructure failures out of the denominator but in the report, and define success from the full reward, not one metric. Inspect AI's reducers make the same choices with one difference worth copying: `pass_k(k)` is the same `C(correct, k) / C(total, k)`, `pass_at(k)` is the Chen 2021 estimator, and both return `NaN` instead of a number when fewer than `k` scored trials remain, so an incomplete campaign surfaces as "unscored" rather than as a spurious 1.0; `at_least(k, value)` scores a case 1 when at least `k` trials reach the threshold (`src/inspect_ai/scorer/_reducer/reducer.py`; UKGovernmentBEIS/inspect_ai commit c2fc3d9, MIT; package inspect-ai 0.3.283; read 2026-10-22). A gate that reads a reliability figure treats NaN, a raised error and a missing row alike: not run, never passed. The trial record the figure is computed from has one row per trial with at least `trial_id`, `case_id`, `run_id`, `started_at`, `outcome` (`pass`, `fail`, `infra_error`), `reward` and the grader version, written by the runner, not reconstructed from a CSV; a case with any `infra_error` row keeps it in the report and out of the denominator. Define trial success from all required properties and preserve failed/incomplete attempts. Do not compute `pass@k` by independently taking the best result for each metric. The independent-probability formulas `1-(1-p)^k` and `p^k` are illustrations, not estimators proving that measured trials are independent. A shared idempotent backend can make later trials repeats of an existing effect.

ROUGE failures can be wording failures even when every action was correct. A high overlap score can also hide negation or a false completion claim. Attribute a failure to its first violated boundary: fixture/state, decision, arguments, tool result, effect, final account or evaluator. For generated transaction receipts, stable text is an application contract; it is not improved model prose.

## Bundled strict CSV checker

Resolve this skill's directory from the loaded `SKILL.md`. Run its script with the target project's Python 3.11+ interpreter; the checker requires only the standard library and makes no external calls. It does not import the project or ADK.

Copy [evaluation-expectations.json](../assets/evaluation-expectations.json) to an appropriate test location and replace the **synthetic** case IDs, eval-set ID, repetitions and criteria with the intended experiment. The example is complete data, not a universal threshold recommendation. Define expectations before looking for a passing result.

The JSON schema has exactly these fields: `eval_set_id` (nonempty string), `cases` (unique nonempty strings), `runs_per_case` (positive integer), and `criteria` (metric name mapped to a finite numeric `threshold` and `comparison`, either `gte` or `lte`). Use `lte` for a lower-is-better metric only when that metric's producer uses the same meaning and status contract. Unknown fields are rejected.

Commands below assume `SKILL_DIR` is the resolved skill directory and the current directory contains the chosen evidence files. Supply your own paths; shell variables are not expanded inside JSON.

```bash
python "$SKILL_DIR/scripts/check_eval_results.py" --help
python "$SKILL_DIR/scripts/check_eval_results.py" \
  --csv results.csv --expectations expectations.json --dry-run
python "$SKILL_DIR/scripts/check_eval_results.py" \
  --csv results.csv --expectations expectations.json
```

Dry-run checks the expectation schema and CSV header, then reports the planned checks; it does **not** evaluate records or establish a gate pass. Normal mode checks the exact case/metric row counts, set membership, finite scores, expected thresholds, numeric comparisons and `PASSED` status. It never prints evidence cells, case IDs, metric names, supplied paths or raw diagnostics. Inspect sensitive trace details separately under the project's data policy.

Exit codes: `0` strict pass (or a valid, explicitly identified dry-run), `1` failed/incomplete gate, `2` malformed input or schema. Require normal mode for CI. The helper is read-only and repeatable; it does not delete or rewrite evidence.

Counts alone cannot distinguish duplicated rows from independent repetitions, prove an actual business effect, or establish who generated the CSV. This checker intentionally does not calculate `pass@k`, claim trial independence or replace trace provenance. For strong release evidence, store explicit invocation/trial IDs in an additional structured result format and reject duplicates there.

## Agents CLI results are JSON, not CSV

`agents-cli eval grade` and `eval run` write `artifacts/grade_results/results_<YYYYMMDD_HHMMSS>.json` (an `agentplatform.types.EvaluationResult` dump with a `metadata.dataset` row list added) and an `.html` report; `eval results` writes the same for a cloud run. There is no `eval_set_id`, `eval_id`, `threshold` or `eval_status` column, so the checker above cannot read or gate this output, and `eval compare` is a recursive dictionary diff that reports a per-case list as one changed value (Agents CLI 1.11.0, `src/google/agents/cli/eval/{eval_utils,cmd_compare,cmd_generate}.py`, read 22 October 2026). The producer exits 0 whatever the scores are, and `eval generate` writes only the cases that succeeded.

A gate over `results_<ts>.json` therefore checks, with the project's own small reader:

1. the number of rows in `metadata.dataset` and of per-case results equals the number of cases in the input dataset, not the trace file, because a failed inference is dropped before grading;
2. every expected `eval_case_id` is present, and every expected metric name appears in `summary_metrics`;
3. `num_cases_error` is 0 for every metric, since the mean averages only the cases that graded;
4. each per-case score meets the agreed threshold and comparison, with `rubric_verdicts` retained where rubric groups were used;
5. a missing file, zero cases or an exception is NOT RUN.

Write the expectations beside the dataset as this skill does for CSV, and keep the reader in the target project's test suite. Consult the installed `google-agents-cli-eval` skill for the result and command details; if it is not installed, adk-engineer explains how to get it. This skill decides what complete evidence is; Google's skill operates the commands that produce it.

## Production extensions

Compare candidates on the same cases, initial state, fixtures, criteria and trial counts; report important risk/language/intent slices rather than only averages. For concrete dataset review, holdout replenishment, fixed-trace judge calibration and release gates, read [evaluation-design.md](evaluation-design.md). Report missing or unavailable scores as incomplete evaluation.

Upper bounds for latency/cost/usage differ from lower bounds for quality. Record clock boundary, versions, workload, concurrency, cache and cold/warm state; a few samples do not establish a production p95. An observer failure after submission is not permission to retry a mutation. Finish with the verified verdict, evidence completeness limits and an actionable next step; implementing a broader production gate requires its own tests.

When measurement itself is in doubt, read [execution-evidence.md](execution-evidence.md) for observer self-tests, concurrent-effect attribution, streaming usage accounting and browser calibration. Preserve unavailable timings and unknown usage instead of replacing them with zero or a fresh submission.
