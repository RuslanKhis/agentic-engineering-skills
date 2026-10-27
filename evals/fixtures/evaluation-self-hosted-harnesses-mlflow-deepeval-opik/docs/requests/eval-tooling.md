# Request: evaluation tooling for the support assistant

From: Data Science (Priya N.), 2026-10-23
Reviewed by: Compliance (H. Lambert), 2026-10-24

## What data science wants

1. **deepeval** for agent metrics (task completion, tool correctness), using its Google ADK
   integration (`instrument_google_adk`) so traces of each run are scored automatically.
2. **MLflow** for the nightly job: the GenAI evaluation with MLflow's Google ADK scorers over the
   previous day's evaluation cases, results logged to an MLflow experiment.
3. **Opik** for trace browsing during development.

## Compliance position

No agent data (prompts, responses, tool arguments, traces or evaluation results) may leave the
`harbour-support-prod` GCP project. We have no Confident AI or Comet account and will not open
one. Models are reached through Vertex AI under the service account only; no API keys.

## Current state

- Production tracing exports to Cloud Trace with message content capture off
  (`deploy/service.yaml`).
- The nightly job (`nightly/`) runs `adk eval` on `eval_cases/support.evalset.json`.
- Scripted-model Runner tests exist for the refund flow.
