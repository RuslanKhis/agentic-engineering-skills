# Dashboards note (Marta, 2026-10-24)

Since the upgrade to google-adk 2.11 two panels on the vendor dashboard show
"no data" on some days and the provider panel lists only one value. Judge
scores live in BigQuery only, so we can't click from a bad score to the trace.

## Findings (2026-10-27, offline review; nothing run against the backend)

- All four panels keyed on `gen_ai.system`. The GenAI conventions removed it
  (`gen_ai.provider.name` replaces it); ADK 2.11 still sets `gen_ai.system=gcp.vertex.agent`
  only in its legacy call attributes, so it is a constant (one provider value) and absent on
  spans from other paths (the "no data" days). Expected per the 2.11.0 conformance list.
- "Tool latency" grouped by `gcp.vertex.agent.tool_name`, which ADK is not documented to emit;
  the tool name is `gen_ai.tool.name`.
- `dashboards/agent-overview.json` now keys on `gen_ai.operation.name`, `gen_ai.agent.name`,
  `gen_ai.tool.name`, `gen_ai.provider.name`. **Unverified:** whether `gen_ai.provider.name` and
  `gen_ai.request.model` are present on your exported `generate_content` spans. Run the drift check
  on a day of exported spans before trusting the first two panels.
- `app/telemetry.py:setup_tracing` is not called anywhere in this repo. If production relies on
  it, nothing is exported from `app/server.py`; if something else sets the provider, that is a second
  owner. Confirm which.

## Drift warning

`python -m app.semconv_drift dashboards/agent-overview.json spans.json` (spans.json: list of
`{"name", "attributes"}` exported from the backend) exits 1 and prints a warning when a panel uses a
removed key or a key no span carries. Run it nightly after the span export; wiring that into a scheduler
or alert is not done.

## Judge scores on traces

`jobs/nightly_judge.py:write_trace_events(rows)` emits `gen_ai.evaluation.result` log events (OTLP logs)
carrying the evaluated span's trace/span id, plus `support.judge.model` and `support.judge.rubric_version`.
Not yet called from a job entry point (none exists in the repo). Assumptions: `judge_scores.trace_id` and
`span_id` are lowercase hex (32/16 chars); the vendor backend accepts OTLP logs and links them to traces.
`LogRecord(event_name=...)` availability in opentelemetry 1.37 was not checked (no install).
