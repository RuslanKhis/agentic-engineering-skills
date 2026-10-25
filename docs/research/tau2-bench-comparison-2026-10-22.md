# tau2-bench compared with this toolkit — 22 October 2026

## Scope and snapshot

A review of [sierra-research/tau2-bench](https://github.com/sierra-research/tau2-bench)
at commit `05736c2` (2.0 line), cloned on 22 October 2026 into its own
directory and read, never run (MIT; the repository carries no separate data
licence, and no task data was copied or will be). Files read:
`src/tau2/metrics/agent_metrics.py` (`pass_hat_k`, `is_successful`,
`get_metrics_df`), `src/tau2/evaluator/AGENTS.md` (the evaluator rules),
`docs/evaluation.md` (`reward_basis`, the reference trajectory and the
end-state hash), `README.md` ("Comparing with v1.0.1"), `VERSIONING.md`
and `CHANGELOG.md`.

**Conclusion.** The memo's reading holds in every particular and the source
adds three rules the memo did not quote: success is reward within 1e-6 of
1, infrastructure-errored simulations leave the denominator, and `pass^k`
is reported for every `k` up to the smallest trial count. The evaluation
skill now carries the unbiased helper rules beside the BigQuery SDK's
plug-in estimate, a new section on grading the end state by replaying one
reference trajectory on a fresh backend (which closes the compatibility
table's own note that relaxed ordering cannot classify extra mutations),
the multiplicative, premature-stop and missing-criterion rules, and the
release skill cites tau2-bench 2.0 as the public precedent for "a judge
change is a new baseline". Method only; the benchmark is not imported.

## Method

Code before prose (`agent_metrics.py` for the estimator, `AGENTS.md` and
`docs/evaluation.md` for the evaluator contract, the README for the
comparability rule); each fact placed at the decision with the commit and
the label "benchmark method, not benchmark data". One scenario case covers
the journey; the fresh-agent trial is recorded in the
[testing record](../testing/tau2-bench-alignment-2026-10-22.md).

## Drift corrected

- The memo called the 2.0 change "a judge change"; the README lists seven
  differences, of which the judge is one, and the non-comparability rests on
  the whole set. The release skill names the three that matter to its rule.
- The memo's helper proposal ("a `pass_hat_k` helper next to
  `check_eval_results.py`") is recorded as rules for a helper rather than a
  new script, because `check_eval_results.py` deliberately computes no
  estimator and its tests and `last-tested` would need a re-run.

## Imported, by specialist

- **adk-agent-evaluation.** The estimator rules in result auditing; the
  end-state grading section and the four evaluator rules in evaluation
  design; the pointer from the compatibility table.
- **adk-release-engineering.** The comparability precedent in versioning.

## Routed, not copied

Nothing; tau2-bench is a benchmark, not a skill.

## Vendored assets

None.

## Left out, with reasons

- The user simulator, domains, voice packs, judge catalog and leaderboard
  tooling: benchmark machinery.
- A `pass_hat_k` script in the skill: a helper change with tests, deferred.
- AppWorld's collateral-damage tests, named by the memo as the "extra
  mutation half": the end-state hash already fails an extra mutation; left
  to a later source if reached.

## Limits

Read, not run; the rules were taken from the maintainers' own contract
document and code on one day.

## Correction, 25 October 2026

"The end-state hash already fails an extra mutation" was true only inside
the hashed tables: the skill hashed "the relevant tables", so a mutation
elsewhere passed. The evaluation skill now diffs the whole fixture with a
named ignore list, after AppWorld
([comparison](appworld-mcpmark-comparison-2026-10-25.md)).
