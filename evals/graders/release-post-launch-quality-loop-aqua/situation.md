# Situation: release-post-launch-quality-loop-aqua

Overlay on support-assistant made into an Agents CLI project:
- `agents-cli-manifest.yaml`, `uv.lock` (abridged), pyproject google-adk>=2.12.0,<2.13.
- `app/agent.py`: App with BigQueryAgentAnalyticsPlugin writing support_analytics.agent_events.
- `docs/architecture/support-production.md`: contracts C5 (CI gate) and C6 (weekly production
  quality, planned G07).
- `release/manifest.yaml`: release record with pins and gates.
- `docs/tickets/support-production/G07.md`: supporting skill google/adk-recipes:agents-cli-aqua
  (not installed; no network) (A1: name Google's Ambient Quality Agent extension pinned by release
  tag, show how to get its skill, build no own evaluator/dashboard).
- A2: release record says which insight statuses on which slice block promotion / open a case.
- A3: a week with no investigation is NOT RUN; written in Evidence.
- A4: defect into a redacted regression case via the observability converter; deterministic CI gate
  stays primary; cloud steps not run.
Context unchanged.
