# Claims intake agent

Helps Kestrel Insurance's claims handlers draft first-notice-of-loss summaries
and check policy cover. Built and run by Brightlane (agency) since the July
pilot; Kestrel's IT operations team takes over running it from 2026-11-17.

- Cloud Run service `claims-intake` in project `kestrel-claims-prod`, europe-west2.
- Model pinned in `claims_agent/agent.py`.
- Deploy: `deploy/deploy.sh`. Alerts: `monitoring/`.

Tests: `python -m unittest discover -s tests -t .`.
