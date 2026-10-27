# Booking agent: reliability gate and end-state grading

Status of everything below: written offline, **not executed** (no shell, no google-adk, no model access in the
authoring session). First action on the pinned interpreter: `python -m unittest tests.test_end_state`.

## Why Monday passes and Tuesday fails

Nothing in the agent changed; the grader is order-sensitive and the run is a single sample.
`test_config.json` uses `tool_trajectory_avg_score` with `EXACT`, so any reordering of calls fails, and
`final_response_match_v2` at 0.8 fails a correct paraphrase. `test_evalset.py` runs `num_runs=1`.
In `reports/nightly-2026-10-21.json`, two of three failures are call-order only and one is wording (0.62).

## The reliability number

**pass^3 over 5 trials per case**, unbiased: `C(c,3) / C(5,3)` per case, averaged over the 40 cases
(`tests/reliability.py`). It is the probability a patient gets a correct outcome three times in a row.
A trial passes only if the end-state grade (below) is clean. Rules, enforced in code:

- k above the scored-trial count, a missing case, an unknown case or a missing file is **NOT RUN** (exit 3), never a pass.
- `infra_error` trials leave the denominator and are reported.
- Gate on the aggregate. Per-scenario (`move`/`cancel`/`status`/`book`) figures and "every variant passed" are printed as diagnostics.
- Exit 0 pass, 1 fail, 3 not run. CI treats both 1 and 3 as red.

**Threshold: provisional 0.85 (assumption, see below).** Two reports at n=1 cannot set it: 77/80 trials passed
(96%) under a grader that is itself unstable. A uniform per-trial rate of 0.96 would give pass^3 near 0.88, so
0.85 is only a starting point. Run 5 trials once, or 5-7 nightlies, then set the threshold a margin below what the
current agent clears and record the date and model ID with it.

## Grading bookings without caring about order

`tests/end_state.py`: replay the case's reference `tool_uses` on a fresh seeded backend to get the target state, then
require from the agent's run:

1. the same set of changed tables (diff over every table, `slots` and `bookings`, not a hash);
2. the same added/removed/changed records and fields;
3. the same multiset of *successful* mutating calls (`book_slot`->`booked`, `cancel_booking`->`cancelled`), so a
   book-then-cancel detour that nets to the same state still fails;
4. one order rule kept on purpose: in a move, cancel only after the new booking succeeded. Cancel-first is a real
   patient-harm path if `book_slot` then fails.

Read order, extra reads and search-before-list all pass. The do-nothing control (`do_nothing_passes`) is tested
over all 40 cases: it must fail every action case and pass every non-action one.

## Findings that need a human

1. **Report IDs do not match the eval set.** The 10-21 report names `booking-06-move` and `booking-14-move`; in
   the eval set 06 and 14 are `cancel` cases. Either the set was regenerated since or the report is mislabelled.
2. **Only 4 distinct prompts.** The 40 cases are 4 scenarios (move, cancel, status, book) repeated 10 times, with no
   refusal, foreign-booking, taken-slot or unavailable-slot case. Forty cases give 4 scenarios of coverage; repeated
   trials tighten the estimate for those 4 only.
3. **`seed_bookings` is not read by anything** outside the eval set (grep: only the 40 case definitions). `tools.backend`
   is a module-level `Backend()` shared across cases in a process, so booking IDs such as `B-001` depend on case order and
   leaked state. This may itself cause night-to-night variation. Each trial needs a fresh backend seeded from the case.
4. `final_response` is "Done." in every case, so the wording check measures nothing useful.

## Questions I could not ask, and the assumptions I proceeded on

- Is a 0.85 pass^3 floor acceptable to the owner? Assumed yes, provisional.
- Is cancel-before-book a failure or just a style difference? Assumed failure (safety rule above).
- Is 200 conversations a night (40 x 5) within budget? Unpriced; no model access here. If not, keep n=5 and
  gate on a 20-case critical subset nightly, full set weekly.
- Who owns the reference trajectories? Assumed the current ones are correct; not reviewed.

## Not done

- No live runner. The nightly job still calls `AgentEvaluator` with `num_runs=1`. Needed: a Runner loop that, per trial, builds a
  fresh seeded backend and a new session, captures function calls and their responses by ID, calls
  `end_state.grade`, and appends a JSONL record (`case_id`, `trial_id`, `outcome`, grader version, model ID).
  The workflow then runs `python -m tests.reliability trials.jsonl --cases cases.txt --k 3 --threshold 0.85`.
- `final_response_match_v2` is not replaced; recommend dropping it from the gate and checking required facts from
  the backend state for status cases.
- No refusal, ownership or taken-slot cases added.
- Reference trajectories not validated by execution (a reference call that errors on the seeded backend would make a
  case silently vacuous; the do-nothing test is the first check).
