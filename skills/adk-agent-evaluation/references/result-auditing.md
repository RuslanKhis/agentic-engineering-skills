# Result auditing and release decisions

Use this mode when checking existing evidence, diagnosing aggregate success with failed trials, or designing a gate. First record what constitutes a successful conversation, the expected cases/repetitions/metrics, and where each observation's identity comes from.

## Check the measured units

ADK 2.8.0 can aggregate repetitions into a passing case average while individual CSV rows fail. A CSV row is one metric observation, not necessarily a complete trial. Its detailed CSV has no guaranteed repetition ID. Require provenance before joining metrics into per-trial booleans; identical responses and row position are not reliable identifiers.

For equally repeated cases, observed `pass@k` is the fraction of cases with at least one successful trial; observed `pass^k` is the fraction with all trials successful. Define trial success from all required properties and preserve failed/incomplete attempts. Do not compute `pass@k` by independently taking the best result for each metric. The independent-probability formulas `1-(1-p)^k` and `p^k` are illustrations, not estimators proving that measured trials are independent. A shared idempotent backend can make later trials repeats of an existing effect.

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

## Production extensions

Compare candidates on the same cases, initial state, fixtures, criteria and trial counts; report important risk/language/intent slices rather than only averages. For concrete dataset review, holdout replenishment, fixed-trace judge calibration and release gates, read [evaluation-design.md](evaluation-design.md). Report missing or unavailable scores as incomplete evaluation.

Upper bounds for latency/cost/usage differ from lower bounds for quality. Record clock boundary, versions, workload, concurrency, cache and cold/warm state; a few samples do not establish a production p95. An observer failure after submission is not permission to retry a mutation. Finish with the verified verdict, evidence completeness limits and an actionable next step; implementing a broader production gate requires its own tests.

When measurement itself is in doubt, read [execution-evidence.md](execution-evidence.md) for observer self-tests, concurrent-effect attribution, streaming usage accounting and browser calibration. Preserve unavailable timings and unknown usage instead of replacing them with zero or a fresh submission.
