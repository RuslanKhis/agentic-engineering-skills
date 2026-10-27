The dashboard fix, the drift check and the score-to-trace events are written, but none of it has been run. I had no shell here, so the new tests, `python -m app.semconv_drift` and the OpenTelemetry log calls are all unexecuted. I also haven't checked any of it against your backend.

**Are the dashboards still using the right names?** No.
- **`gen_ai.system`:** all four panels were keyed on it. The GenAI conventions removed it in favour of `gen_ai.provider.name`. ADK 2.11 still sets `gen_ai.system=gcp.vertex.agent`, but only on its legacy model-call attributes. That explains the single provider value and the "no data" days. The skill's 2.11.0 conformance list marks this as an expected deviation.
- **Tool latency grouping:** it used `gcp.vertex.agent.tool_name`, which I found no source documenting ADK as emitting. The tool name attribute is `gen_ai.tool.name`.
- **Fix:** `dashboards/agent-overview.json` now keys on `gen_ai.operation.name`, `gen_ai.agent.name`, `gen_ai.tool.name` and `gen_ai.provider.name`.
- **Unverified:** I don't know whether `gen_ai.provider.name` and `gen_ai.request.model` appear on your exported `generate_content` spans. Run the drift check on a day of exported spans before trusting the first two panels.

**Drift warning:** `app/semconv_drift.py` takes the dashboard JSON and a span export (a list of `{name, attributes}`). It exits 1 and prints a warning when a panel uses a removed key or a key no span carries. Nothing schedules it yet, so it isn't an alert.

**Judge scores on traces:**
- **Events:** `app/eval_events.py` turns each `judge_scores` row into a `gen_ai.evaluation.result` log event. The event carries the evaluated span's trace and span id, the score and label, and `support.judge.model` and `support.judge.rubric_version`.
- **Wiring:** `jobs/nightly_judge.py:write_trace_events` sends the events over OTLP logs. It is not called from anywhere because the repo has no job entry point.
- **Tests:** `tests/test_telemetry_contracts.py`.

**Questions I couldn't ask, and what I assumed:**
- **Exporter:** is `app/telemetry.py:setup_tracing` called anywhere? Nothing in this repo calls it, so `app/server.py` may export nothing, or a second tracer-provider owner may exist elsewhere. I assumed spans do reach the backend, since the dashboards show data. Please confirm which it is.
- **IDs:** I assumed `trace_id` and `span_id` in `judge_scores` are lowercase hex (32 and 16 characters). Rows that don't match are skipped and counted.
- **Backend:** I assumed it accepts OTLP logs and links them to traces.
- **OpenTelemetry API:** I didn't check that `LogRecord(event_name=...)` exists in the pinned opentelemetry 1.37.

**Left undone:** I did not run the tests, schedule the drift check, add a job entry point for the judge, or check any of this against the backend. The same summary is in `docs/notes/dashboards.md`.