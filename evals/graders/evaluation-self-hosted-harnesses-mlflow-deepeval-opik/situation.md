# Situation (judge only): evaluation-self-hosted-harnesses-mlflow-deepeval-opik

Context unchanged. Workspace: support-assistant base plus `deploy/service.yaml` (Vertex AI under a
service account, content capture off), `docs/requests/eval-tooling.md` (the request and the
compliance position: no data leaves the project, no Confident AI or Comet account),
`nightly/run_nightly.sh` (adk eval only) and a three-case eval set. Nothing is planted beyond the
request; this is an advisory/configuration scenario. All assertions concern vendor facts the
evaluation skill's references carry (deepeval CONFIDENT_API_KEY export and opt-out variables;
MLflow Feedback error = NOT RUN, scorer default judge gemini-2.5-flash, tool_call_args '{}' with
capture off; Opik OPIK_URL_OVERRIDE and the three opt-outs; MLFLOW_DISABLE_TELEMETRY; SQL backend
for OTLP ingestion; Vertex identity rather than a Gemini API key; Runner tests and adk eval stay
primary). Gradeable from the answer and any config written.
