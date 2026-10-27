I wrote a reliability gate and an end-state grader, but nothing has been run. This session had no shell, no google-adk and no model access. The first check is `python -m unittest tests.test_end_state`, which tests both new modules.

**Why it flips between Monday and Tuesday.** The grader is order-sensitive and each run is a single sample. `test_config.json` uses `tool_trajectory_avg_score` with `EXACT`, so any reordering of calls fails. The `final_response_match_v2` check at 0.8 rejects correct paraphrases, and `test_evalset.py` runs `num_runs=1`. In the 10-21 report, two of the three failures are call-order only and one is wording.

**Reliability number: pass^3 over 5 trials per case.** This is the unbiased estimate `C(c,3)/C(5,3)` per case, averaged over the 40 cases. It reads as the chance that three runs in a row all get a correct outcome. A short cohort, a missing case or a missing file counts as NOT RUN (exit 3), never a pass. Infrastructure errors stay out of the denominator but are reported.

**Grading bookings regardless of call order.** `tests/end_state.py` replays each case's reference calls on a fresh seeded backend. The agent's run passes if it matches on three things:
- the same changed tables and the same record and field changes, across the whole backend;
- the same set of successful booking and cancel calls, so a book-then-cancel detour that nets out still fails;
- one order rule kept on purpose: in a move, cancel only after the new booking succeeds, so a failed booking can't leave the patient with nothing.

Different read order and extra reads pass. A do-nothing control is tested over all 40 cases and must fail every action case.

**Findings:**
- **Report IDs don't match the eval set.** The 10-21 report names `booking-06-move` and `booking-14-move`, but in the eval set 06 and 14 are cancel cases.
- **Only four distinct prompts.** The 40 cases are move, cancel, status and book, repeated ten times each. There are no refusal, foreign-booking or taken-slot cases.
- **`seed_bookings` is read by nothing.** `tools.backend` is a global shared across cases, so IDs like `B-001` depend on case order and leaked state. That alone could cause night-to-night drift.

**Questions I couldn't ask, and what I assumed:**
- Is 0.85 an acceptable pass^3 floor? I assumed yes, as a provisional value. Two n=1 reports can't set it. Run 5 trials once, or 5–7 nightlies, then set it a margin below what the agent actually clears.
- Is cancel-before-book a failure? I assumed yes.
- Is 200 conversations a night (40 × 5) within budget? I couldn't price it. If it isn't, gate nightly on a 20-case critical subset and run the full set weekly.
- Are the current reference trajectories correct? I assumed yes and did not review them.

**Left undone:**
- There is no live runner yet. The nightly job still calls `AgentEvaluator` with `num_runs=1`. It needs a loop that builds a fresh seeded backend and a new session per trial, captures calls and results, runs `end_state.grade`, and writes JSONL for the gate.
- The `final_response_match_v2` check is not replaced.
- No new refusal, ownership or taken-slot cases were added.
- The reference trajectories were not validated by execution.

Files are in the workspace:
- `EVAL_RELIABILITY.md`
- `tests/end_state.py`
- `tests/reliability.py`
- `tests/test_end_state.py`