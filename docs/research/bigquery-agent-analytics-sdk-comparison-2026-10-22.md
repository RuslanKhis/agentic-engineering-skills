# BigQuery Agent Analytics SDK compared with this toolkit — 22 October 2026

## Scope and snapshot

A file-level review of
[GoogleCloudPlatform/BigQuery-Agent-Analytics-SDK](https://github.com/GoogleCloudPlatform/BigQuery-Agent-Analytics-SDK)
(`bigquery-agent-analytics` on PyPI) at commit `68ef3fa` (2026-10-21),
latest tag v0.6.1 (2026-10-20), cloned on 22 October 2026 into its own
directory and read, never run. Licence: Apache-2.0 at the root, no NOTICE;
one example fixture carries its own `LICENSE.md`
(`examples/okf_attested_computation/fixtures/acme_retail/`), not read. Files
read: `README.md`, `CHANGELOG.md` (0.6.1 entry), `SDK.md` sections 3, 5, 7,
8, 9, 14 and the CLI exit-code table, `pyproject.toml`,
`deploy/continuous_queries/README.md`, `examples/evalbench_score_gate.sh`,
`docs/sdk_usage_tracking.md` (header), and
`src/bigquery_agent_analytics/multi_trial_performance_evaluator.py` for the
two pass-rate formulas.

**Conclusion.** The SDK is the read side of the table this toolkit already
tells an agent to write. It adds what the observability skill lacked (a
library and CLI over `agent_events`, deterministic evaluators, continuous
queries, its own job labels) and what the release skill lacked (a score gate
with usable exit codes over stored sessions, a measurable form of dataset
drift, graduation and saturation signals). It was imported as facts with the
SDK's own caveats carried beside them; it is a library, so nothing is
routed, and nothing was vendored.

## Method

Each named section was read; each item was classified and checked against
the specialist that already covers the decision; facts were written at that
decision with the citation `(BigQuery-Agent-Analytics-SDK v0.6.1, <file>,
read 2026-10-22; vendor library, not executed)`. One scenario case and one
fresh-agent trial cover the changed journey (see the
[testing record](../testing/bigquery-agent-analytics-sdk-alignment-2026-10-22.md)).

## Drift corrected

- The memo listed the SDK's `pass^k` among the methods to adopt. The SDK
  documents and implements it as `(c/n)^n`, a plug-in estimate that differs
  from the unbiased `C(c, k) / C(n, k)` tau2-bench uses. The evaluation
  skill records both so a reported figure names its formula; the method to
  restate as a helper comes from tau2-bench, later in this programme.
- The SDK depends on `google-adk>=1.0.0`, so it installs beside an existing
  pin; the memo did not say so and a reader might have expected a conflict.

## Imported, by specialist

- **adk-agent-observability.** A section "Reading the table with the Agent
  Analytics SDK" in the BigQuery reference: what it reads and reconstructs,
  the seven deterministic evaluators and judge metrics, the CLI and its exit
  codes, the continuous-query templates with their Enterprise reservation
  requirement and the vendor's hourly figure, the cheaper streaming
  alternative, the labels on every job it submits, and three caveats the SDK
  states about itself (thought tokens absent from `cost_per_session`, the
  cache metric passing on missing telemetry unless told to fail, the `pass^k`
  formula), with the reminder to confirm it reads the plugin's schema
  version.
- **adk-release-engineering.** A fourth gate in the CI reference:
  `bq-agent-sdk evaluate --exit-code` and `evalbench-score --exit-code` with
  exit 0, 1 and 2 mapped to pass, block and NOT RUN, pinned at 0.6.1 or later
  because that release escapes the text its gates print and refuses a
  non-table golden name, placed in tier 3 beside the nightly judge. In the
  production-feedback reference: drift detection by deduplicated keyword
  overlap with coverage and new-in-production counts, semantic clustering
  of production questions, capability and regression categories with
  automatic graduation after N consecutive passes, saturation and balance
  flags from the health check, and the static validator, written as triggers
  for the dataset-drift row and the retire-or-harden decision that stay as
  this toolkit defines them.
- **adk-agent-evaluation.** The two pass-rate formulas beside the
  result-auditing reference's observed definitions.

## Routed, not copied

Nothing: the SDK is a library and a CLI, not a skill. Its Claude Code
tracing plugin (`.claude-plugin/marketplace.json`) distributes the SDK's own
tooling and changes no decision here.

## Vendored assets

None. The continuous-query SQL templates and the score-gate script were
read and described, not copied.

## Left out, with reasons

- The Agent Context Graph, long-horizon memory, BigQuery AI/ML integration,
  BigFrames evaluator, categorical dashboards and remote-function deployment
  surfaces: product capabilities with no decision in this toolkit to change.
- The continuous-query hourly price as a toolkit fact: it is the vendor's
  figure on a dated README, carried only with that label.
- `MultiTrialPerformanceEvaluator` as a repetition harness: what one "trial"
  re-runs (the agent, or the evaluation of one stored session) was not
  established from the documentation, so the evaluation skill's own fresh
  backend per trial rule stands.
- A spike against BigQuery: no project or credentials in this session; the
  gate is written as a planned verification with the exit-code check as its
  first acceptance item.

## Limits

Read, not run. Exit codes, label names and evaluator names are as documented
at v0.6.1 and may move; the SDK is at 0.x. Whether its session query reads
the plugin's current schema version was not verified, and the reference
says so.
