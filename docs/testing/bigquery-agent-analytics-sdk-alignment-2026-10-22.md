# BigQuery Agent Analytics SDK alignment — 22 October 2026

*What changed, what was checked, and what a fresh agent did with it.*

## Change

See the [comparison note](../research/bigquery-agent-analytics-sdk-comparison-2026-10-22.md).
In the repository:

- **Facts** from GoogleCloudPlatform/BigQuery-Agent-Analytics-SDK v0.6.1
  (commit `68ef3fa`) went into three specialists, cited to the file and
  labelled a vendor library: the SDK section of the observability skill's
  BigQuery reference (what it reads, the evaluators, the CLI and its exit
  codes, continuous queries and their reservation, job labels, the token,
  cache and `pass^k` caveats, and after the trial the call shapes and flag
  names); the fourth gate and the provisional-threshold rule in the release
  skill's CI reference, with drift detection, graduation and saturation in
  its production-feedback reference and the SDK judge in its versioning
  rule; the two pass-rate formulas in the evaluation skill's result-auditing
  reference.
- **No routing line**: the SDK is a library and a CLI.
- **One scenario case** (`release-bigquery-analytics-score-gate-and-drift`)
  and an optional, commented BigQuery gate step in the release skill's
  workflow asset.

## Automated checks

`scripts/validate_skills.py` after the edits: **22 packages**, 0 errors,
0 warnings; the workflow asset still parses as YAML; `git diff --check`
clean. The full `scripts/check_repo.py` counts are in the [testing log](index.md) entry for
this date. No helper script, test or `last-tested` date changed.

## Fresh-agent trial

One trial, in a subagent with a fresh context, the 22 packages readable as
installed skills, no Google skill installed, no credentials, no network, no
ADK or SDK, on a synthetic project, without the expected answers.

### Release engineering: a nightly production score gate and a golden coverage report

Fixture: an ADK 2.12 support agent writing `agent_events` through the
plugin, a 40-row golden-question table, a release record with pins, a CI
workflow that ran unit tests only, and a request for a nightly SDK-based gate
that blocks promotion, with the exit-code meanings and the unreachable case
spelled out, plus a monthly coverage and saturation report, offline only.

Observed: the agent led with adk-release-engineering in the gate and
production-feedback modes, pinned `bigquery-agent-analytics==0.6.1`, built
the gate as one SDK process per evaluator with `--exit-code`, mapped exit 0
to promote, 1 to block and 2 to NOT RUN (blocking exactly like a failure,
never a pass), folded a missing binary, a timeout and any other code into
NOT RUN while still writing the evidence record, refused to produce a verdict
while the thresholds carried no measurement date unless explicitly told the
values are provisional, kept the judge pinned by name and rejected an alias,
wrote the drift report from `drift_detection` over the golden table with a
coverage trigger and a saturation rule applied to local run records, and
listed what must run live. Offline: 35 tests passed and 4 live tests
skipped as NOT RUN on both interpreters it could use. Ease: **3 of 5**; the
skills named the gate, its exit codes, the pin and the concepts, but carried
no flag names, constructor or result shapes, so much of the implementation
was config-driven placeholders marked for confirmation.

Fixed the same day: the observability skill's SDK section now carries the
documented call shapes (client constructor, global options, `evaluate` and
`evalbench-score` flags, `drift_detection` and its report fields,
`EvalSuite` and its health, graduation and serialisation calls, with the
note that the project persists its own run history) and is named as the one
home for them, with the release references pointing there instead of
restating; the release CI reference says where a BigQuery-gate judge is
recorded, since the inventory helper cannot see it, and what to ship before
a baseline exists (report-only with provisional labels, the measurement as
the first live acceptance item, no provisional PASS); the versioning rule
lists that judge; and the workflow asset carries the optional gate step as a
commented stanza under the nightly job. Noted, not changed: the specialist
table's position in the entry skill, which the agent's first read truncated;
and the trial's own choice to compute saturation from local records, which
the fixed reference now explains.

## Limits

One trial on one synthetic project; the SDK was never installed or run, so
every flag name and result field is as documented at v0.6.1 and marked for
confirmation on the installed version. The trial's unmeasured thresholds are
labelled provisional by its own gate.
