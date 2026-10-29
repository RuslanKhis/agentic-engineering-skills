# Situation (judge only): evaluation-paired-difference-and-holdout-size

Context unchanged. Workspace: a standalone overlay (no base). Synthetic trial records generated
with a seeded script (seed 29) on 2026-10-29: 20 development cases in 8 scenarios (claim types,
2 or 3 variants each), three runs per case per version; one v4 run of dev-014 is `infra_error`.

## What the data show

- Pooled run pass rates: v3 38/60 = 63.3%, v4 41/59 = 69.5% (the dashboard's "about 6 points").
- Per-case means averaged first: v3 63.3, v4 70.0; paired difference +6.7 points.
- Clustered on `scenario` (8 clusters, t on 7 df): SE 6.8 points, 95% interval −9.4 to +22.7,
  verdict within noise; correlation between versions' case scores 0.36. Minimum detectable
  difference at 80% power: 22.1 points.
- Unclustered (case as the unit, 20 clusters): SE 8.2, interval −10.6 to +23.9, MDD 24.3; same
  verdict. Either is acceptable for A2 as long as the scenario grouping is considered; clustering
  on scenario is what the skill asks for.
- Holdout sizing for the brief's 5-point lift, from the dev variance: about 295 cases (118
  scenarios) at three runs per case; the five-run figure is not estimable, because the run-noise
  estimate exceeds the observed variance on this small sample (an agent that says so, or plans
  only at three runs, is right). Any figure of the right order (roughly 200 to 450
  cases at three runs, with the method shown) satisfies A4; an unclustered calculation gives
  about 428.
- The budget (600 runs per release, both versions) buys about 100 cases at three runs, which can
  detect about 8.7 points, not 5 (the 60-cases-at-five-runs alternative cannot be judged from this
  sample's noise split). The twelve-case holdout, once labelled, could detect only about 25 to 33
  points depending on how its scenarios fall.

Real output of `python3 scripts/paired_difference.py --baseline runs/baseline-prompt-v3.csv
--candidate runs/candidate-prompt-v4.csv --target-difference 0.05 --plan-cases 100 --plan-runs 5`
(exit 0; helper as of 2026-10-29 after the trial fixes):

```text
cases scored in both: 20; unpaired: 0
infra_error rows left out: baseline 0, candidate 1
baseline 63.3 (SE 11.3); candidate 70.0 (SE 6.9); points on a 0-100 scale
paired difference +6.7 (SE 6.8); clusters 8; correlation 0.36
95% interval -9.4 to +22.7; verdict: within noise
minimum detectable difference at 80% power: 22.1 points
runs per case: baseline 3.00, candidate 2.95
share of the variance from run-to-run noise: not estimable (the run-noise estimate exceeds the observed variance on this sample, so the split between run noise and case variation is not estimable; plan on cases at the current runs per case, or collect more cases first)
planning assumes 2.50 cases per scenario, as in this sample
at 2.98 runs per case, to detect 5.0 points: about 295 cases (118 scenarios)
at 2.98 runs per case, 100 cases could detect: 8.7 points
at 5 runs per case: not estimable (the run-noise estimate exceeds the observed variance on this sample, so the split between run noise and case variation is not estimable; plan on cases at the current runs per case, or collect more cases first)
this sample cannot detect 5.0 points
```

## Assertion map

A1 runs averaged per case, difference per case on the same cases, not pooled run rates; the
infra_error run left out and reported. A2 SE clustered on scenario; interval includes zero; "within
noise". A3 MDD about 22 points stated; no "the change helped" claim to the sponsor (keeping v4 on
other grounds, labelled as within noise, is fine). A4 holdout sized from the 5-point lift with the
dev variance (order of 300 cases at three runs), the 12-case holdout called insufficient, and the
budget trade-off (runs versus cases, or the ~9-point detectable difference the budget buys)
stated. A5 the helper used, or named and reported not run; no model run.
