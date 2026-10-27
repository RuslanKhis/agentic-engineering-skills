# Working on this repository

- Python 3.12; pins in `pyproject.toml`; do not change pins in a feature change.
- Tests: `python -m unittest discover -s tests -t .`; no BigQuery or model calls in tests.
- Only `analytics/agent.py` and `analytics/author.py` import google.adk; keep it that way.
- Templates change only after finance review (`reviewed_by`, `reviewed_on`).
- The agent's runtime identity is `analytics-agent@fernhill-analytics.iam.gserviceaccount.com`
  with BigQuery Job User on the job project and Data Viewer on `sales` only.
