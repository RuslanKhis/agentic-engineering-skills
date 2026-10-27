# Situation: release-bigquery-analytics-score-gate-and-drift

Overlay on support-assistant:
- `app/agent.py`: App with BigQueryAgentAnalyticsPlugin (support_analytics.agent_events).
- `bq/golden_questions.sql` + `.csv`: 40 reviewed questions.
- `release/record.yaml`: pins, judge model "none yet", PR gate = unit tests only.
- `.github/workflows/ci.yml`: unit tests only.
- No BigQuery access, SDK not installed (A1: pin bigquery-agent-analytics >= 0.6.1, evaluate
  --exit-code as tier-3 gate, exit 1 block, exit 2 NOT RUN; A2 deterministic PR gate primary,
  nightly as comparison against previous night with pinned judge; A3 cost caveats; A4 drift
  report and saturation flag, live commands not run).
Context unchanged.
