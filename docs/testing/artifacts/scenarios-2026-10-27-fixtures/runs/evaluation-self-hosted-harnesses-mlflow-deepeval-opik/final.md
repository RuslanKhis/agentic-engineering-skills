All three can run inside your GCP project, but deepeval's ADK integration can't. I haven't run or installed anything. The findings come from the repo's bundled skill notes, which record offline spikes on mlflow 3.17.2, deepeval 4.3.1 and Opik commit 763a2ec. Confirm them on the versions you install. The full write-up is in `docs/eval-harness-plan.md`.

## What you can use

- **deepeval:** use its metrics only. Don't call `instrument_google_adk()`.
  - It exports to Confident AI, has no local sink, raises without `CONFIDENT_API_KEY`, and replaced ADK's native spans in the spike.
  - Set `DEEPEVAL_TELEMETRY_OPT_OUT=1` and `DEEPEVAL_DISABLE_DOTENV=1`, so a stray `.env` key can't turn uploads on.
  - Give every metric an explicit Vertex-backed judge. Otherwise `ToolCorrectnessMetric` builds an OpenAI client. I haven't tested the custom model wrapper this needs.
  - Set `should_exact_match=True`, because an extra tool call otherwise passes. Add a separate forbidden-call assertion.
  - Build test cases from session events, not spans.
- **MLflow ADK scorers:** use them against a self-hosted server in your project.
  - The server needs a SQL backend (Cloud SQL).
  - Set `MLFLOW_DISABLE_TELEMETRY=true`, `DO_NOT_TRACK=true` and `LITELLM_LOCAL_MODEL_COST_MAP=True` on both client and server.
  - Give the scorers an explicit `threshold` and pin the judge model and sample count. The default judge is `gemini-2.5-flash` with five samples.
  - Install `google-adk[eval]`.
- **Opik:** use it for traces, self-hosted. Its SDK defaults to Comet's cloud, which would break your rule.
  - Set `OPIK_URL_OVERRIDE` to your in-project URL.
  - Set `OPIK_SENTRY_ENABLE=false`, `OPIK_ANALYTICS_ENABLE=false` and `OPIK_ENABLE_LITELLM_MODELS_MONITORING=false`. On the server, set `OPIK_USAGE_REPORT_ENABLED=false`.
  - Its ADK integration patches ADK's tracer for the whole process. A guard callback that short-circuits may hide blocked calls from it. This was read in the source, not run.
  - With content capture off, Opik traces show structure, timing and errors but no content. Keep capture off in production.

## How the nightly job should record MLflow's results

Score from session events joined to traces on `gen_ai.conversation.id`. With capture off, spans have no tool arguments or text.

- **Tool trajectory:** pass `actual_tool_calls` from the session events. Read from traces, `ToolTrajectory` takes tool names from span names, so they never match.
- **Hallucination:** call ADK's `HallucinationsV1Evaluator` directly. MLflow's scorer passes no tool names or results, so tool-grounded answers get graded as unsupported.
- **Zeros:** MLflow turns a missing ADK score into 0.0 and "no", and a judge failure inside ADK looks the same. A 0.0 is not a fail until you've checked the row.
- **Outcomes:** each row gets `pass`, `fail`, `blocked` or `not run`, plus a tier label (the nightly scoring is `live`). Errors, missing values and unverified zeros are `not run` or `blocked`, never `fail`. An empty cohort is `not run`.
- **Counts:** record the expected, scored and errored row counts. Report per-metric rates with denominators, such as 42/50 scored and 8 not run, not one blended number.
- **Provenance:** keep failed and errored rows, and don't rerun until green. Record the mlflow, google-adk, google-genai and deepeval versions, the judge id, sample count, threshold and the agent's prompt/config version.
- **Controls:** run one canary session with a known verdict each night, and mark the judge metric `blocked` if it returns 0.0. Add a do-nothing control that must fail action cases. The canary costs a judge call, so it needs approval before the first run.
- **Storage and alerts:** log one MLflow run per night, with the rows as an artifact and the counts as metrics. Alert when the `not run` share rises, not only when pass rate falls.
- **Reliability figure:** don't call the result pass^k. Scoring existing sessions gives one observation each.

## Questions I couldn't ask, and what I assumed

1. **Where does the nightly job run?** I assumed a Cloud Run job in your project, using the Vertex service account.
2. **Are full session events retained?** I assumed yes.
3. **Which judge?** I assumed a pinned Gemini model on Vertex in your project. Judge calls send transcripts to Vertex, so Compliance should approve that as a data flow.
4. **Where are MLflow and Opik hosted?** I assumed in your project: Cloud SQL and GCS for MLflow, GKE or a VM for Opik.

## What I did and left undone

- **Done:** read the repo's instructions and the bundled evaluation and observability notes, then wrote `docs/eval-harness-plan.md`.
- **Left undone:** no packages installed, no code or config changes, no model, network or cloud calls. Nothing is verified on your pinned stack. The deepeval Vertex wrapper, Opik with guard callbacks and real egress behaviour are unconfirmed.
- **For Compliance:** a network-level egress check before first use.