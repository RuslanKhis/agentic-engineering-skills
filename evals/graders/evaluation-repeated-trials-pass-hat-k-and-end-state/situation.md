# Situation (judge only): evaluation-repeated-trials-pass-hat-k-and-end-state

Context unchanged. Workspace: a standalone booking agent (no base).

## Planted

- `eval_cases/test_config.json`: tool_trajectory_avg_score with match_type EXACT at 1.0, and
  final_response_match_v2 at 0.8 with no judge pinned.
- `reports/nightly-2026-10-20.json` (40/40) and `nightly-2026-10-21.json` (37/40): two "move"
  failures are only call-order differences (get_my_bookings and search_slots swapped; book then
  cancel vs cancel then book — the second can leave the patient briefly with no booking, which an
  end-state comparison would still accept if the end state matches), one is a response-match
  score; `judge_model: "default"`, `num_runs: 1`.
- `.github/workflows/nightly-eval.yml` runs the evalset once per night.
- `booking_agent/backend.py` has `snapshot()`; a reference-trajectory replay on a fresh backend is
  possible offline. `tests/scripted_model.py` is the scripted-model harness; Runner/evaluator tests
  skip without google-adk.

## Assertion map

A1 repeated trials per case, unbiased pass^k = C(c,k)/C(n,k), refuse k > n, infra failures
outside the denominator but reported, success = whole case; A2 grade by replaying the reference
trajectory on a fresh backend and comparing end states (different correct order passes, extra
mutation fails) rather than switching to ANY_ORDER; A3 any stop other than agent/user finish
scores 0, multiply components, undefined criterion = not evaluated; A4 pin judge and model ids in
the gate manifest, judge change = new baseline, model runs reported not run.
