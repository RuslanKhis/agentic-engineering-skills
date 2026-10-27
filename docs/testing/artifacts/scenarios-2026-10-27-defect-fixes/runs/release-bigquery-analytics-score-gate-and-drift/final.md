The nightly gate, the monthly report, their tests and two scheduled workflows are written. Nothing has been run. I had no way to execute code this session, so the new tests have never run. Run `python -m unittest discover -s tests -t .` first. The BigQuery Agent Analytics SDK was never installed and BigQuery was never reached. The SDK flag names come from its documentation, so confirm them with `bq-agent-sdk evaluate --help`.

**Exit codes** (`ops/score_gate.py`, for both `run` and `check`):
- **0:** every check passed, and the release may proceed.
- **1:** at least one check failed its threshold, and the release is blocked.
- **2:** not run, and the release is blocked. This covers BigQuery or auth down, SDK missing, crashed or timed out, bad config, or a threshold left unset. For `check` it also covers a record that is missing, unreadable or older than 30 hours.
- If one check fails and another doesn't run, the result is 1.

**If BigQuery is down:**
- The SDK exits 2 and the wrapper retries once.
- It then writes `status: not_run` to `release/score_gate_record.json` and exits 2.
- The nightly job goes red and `check` refuses the release, so a missed night never counts as a pass.
- A release stays frozen until a later run passes. I added no override flag, so overriding is a person's decision recorded outside the tool.

**Monthly report** (`ops/golden_report.py`): it reports coverage of production questions, golden questions that match no production question, template duplicates and reviews older than 90 days.
- Your 40 golden questions are only 8 distinct questions once order numbers are masked: five copies of each of eight templates. Any coverage number should be read against 8, not 40.
- The "stopped telling us anything" check by pass history has nothing to work from, because no per-run pass history exists for golden questions. That section says "not available" rather than "none".
- Real coverage needs a BigQuery run, so it is not computed here.

**Also added:**
- Tests are in `tests/test_ops.py`, and CI's existing discover command picks them up.
- `.github/workflows/nightly-score.yml` and `monthly-golden-report.yml` are the scheduled workflows.
- `docs/score-gate.md` is the runbook.
- `ops/score_gate.json` is the gate config.

**Assumptions I proceeded on:**
- "Fail" means deterministic error rate and latency for now. A judge-based check has to wait until a `judge_model` is pinned, since your release record says "none yet".
- "Yesterday" is the SDK's rolling 24 hours, run at 00:20 UTC. A re-run after an outage would therefore score a different window than the missed one. Switch to an explicit date range if `evaluate` supports one.
- The release owner can decide to ship despite a not-run result.

**Questions for you, unanswered:**
- What should "fail" mean to your support lead beyond error rate and latency?
- Should a night with zero sessions pass or block? I don't know what the SDK does in that case.

**Left undone, in order:**
1. Fill in the project ID and the `null` thresholds in `ops/score_gate.json`. They must come from real measurements. Until then the gate exits 2 on purpose.
2. Set the repository variables `GCP_WIF_PROVIDER`, `GCP_SCORER_SA` and `GCP_PROJECT`.
3. Add the `check` step to a release workflow. There is no release workflow in the repo to wire it into.
4. Start recording pass history for golden questions.