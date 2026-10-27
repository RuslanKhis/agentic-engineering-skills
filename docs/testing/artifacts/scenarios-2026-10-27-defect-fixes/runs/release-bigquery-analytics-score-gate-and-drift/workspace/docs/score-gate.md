# Nightly production score gate and monthly golden report

Status: written offline. The SDK (`bigquery-agent-analytics` 0.6.1) was never installed or run, and
BigQuery was never reached. Flag names come from the SDK's documentation; confirm each with
`bq-agent-sdk evaluate --help` before the first real run.

## Exit codes (`ops/score_gate.py`, for both `run` and `check`)

| Code | Meaning | Release |
| --- | --- | --- |
| 0 | Every check passed | May proceed |
| 1 | At least one check failed its threshold | Blocked |
| 2 | Not run: BigQuery or auth unavailable, SDK missing or crashed, timeout, bad config, threshold unset; for `check` also record missing, unreadable or older than 30 h | Blocked |

If one check fails and another is not run, the result is 1. The SDK's own codes are 0 pass, 1 fail, 2
infrastructure error or bad input; the wrapper maps any other code (crash, signal) to 2.

## If BigQuery is down

The SDK exits 2, the wrapper retries once after 30 s, then writes `status: not_run` to
`release/score_gate_record.json` and exits 2. The nightly job goes red, and `check` refuses the release
because the record is not a fresh pass. Nothing is skipped silently. Cost: a release is frozen until a
later run passes. To release anyway, a person decides that outside this tooling and records why in the
release record; there is deliberately no override flag.

## Wiring a release to it

No release workflow exists in the repo, so this is not wired. Add a step before promotion:
`python ops/score_gate.py check --record release/score_gate_record.json` and fail the release on non-zero.
The record has to reach the release job (artifact download or a bucket object); the nightly workflow
uploads it as an artifact only.

## Before the first run

1. Replace `REPLACE_WITH_GCP_PROJECT` and the `null` thresholds in `ops/score_gate.json` with values
   measured over a couple of weeks of real sessions. A null threshold gives exit 2 on purpose.
2. Set repository variables `GCP_WIF_PROVIDER`, `GCP_SCORER_SA` (read-only BigQuery) and `GCP_PROJECT`.
3. Pick the evaluator names from `bq-agent-sdk evaluate --help`; `error_rate` and `latency` are the
   documented ones.

## Monthly report (`ops/golden_report.py`)

`fetch` runs the SDK's drift detection against `golden_questions` (needs BigQuery); `render` is offline
and joins it with `bq/golden_questions.csv`. It reports coverage, golden questions matching no
production question, template duplicates, and reviews older than 90 days. "Saturated" questions need a
per-run pass history that does not exist yet, so that section says "not available". The coverage number
is keyword overlap, not a judgement of whether an answer is still right.

## Open questions and the assumptions made

- Which dimension does Priya mean by "fail"? Assumed: deterministic error rate and latency now. A judge
  criterion (`llm-judge`) waits for a pinned `judge_model`, which the release record lists as "none yet".
- "Yesterday" is the SDK's rolling `--last=24h`, run at 00:20 UTC, so it includes about 20 minutes of
  today. If `evaluate` accepts an explicit date range, switch to it; a re-run after an outage otherwise
  scores a different window than the one that was missed.
- Zero sessions yesterday: unknown whether the SDK passes or exits 2. Check on the first quiet day.
- Who may release despite a not-run? Assumed: the release owner, outside the tool.
