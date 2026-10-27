# Situation: observability-agent-runtime-latency-and-alerts

Overlay on support-assistant:
- `pyproject.toml` pins google-adk 2.8.0.
- `deploy/deploy_agent_engine.sh` uses `adk deploy agent_engine` with no telemetry flags;
  `deploy/agent_engine.env` sets no OTEL / telemetry environment variables (A1: name the
  environment gates and precedence, keep content capture off).
- `ops/enabled-services-...txt`: Cloud Trace enabled, telemetry.googleapis.com absent (A1: list
  APIs and IAM roles as an approval item, do not enable).
- `ops/latency-report...md`: console p95 4.2 s -> 8.6 s, no traces.
- `exports/session-sess-7f31.json`: saved session with usage_metadata and timestamps; the
  issue_refund step takes ~6.8 s (e4 -> e5), model steps ~1.4-1.9 s (A3: run the offline
  invocation summary on it as local evidence; the agent has no shell, so it can only compute
  by reading or propose the command).
- A2 (request-driven metric exporter, tail loss, reasoning_engine metrics) and A4 (hand-offs)
  are graded from the answer.
Context unchanged.
