# Situation: observability-semconv-drift-and-evaluation-events

Overlay on support-assistant: google-adk 2.11.0; OTLP/HTTP to a third-party backend
(`deploy/service.env`, `app/telemetry.py`); `dashboards/agent-overview.json` keyed on
`gen_ai.system` (A1: rekey on gen_ai.provider.name, gen_ai.operation.name, gen_ai.agent.name;
keep gcp.vertex.agent.* as ADK joins); `jobs/nightly_judge.py` writes scores with trace and span
ids to BigQuery only (A3: emit gen_ai.evaluation.result events parented to the evaluated span with
judge identity, not run without the SDK). A2 (reference scenario and Weaver live-check pinned to
2.11.0) and A4 (Development status) graded from the answer. Context unchanged.
