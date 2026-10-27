# Self-hosted evaluation harnesses for the ADK 2.12 agent

Status: design only. Nothing here was installed or run; no model, network or
cloud calls were made. Facts come from the repo's bundled skill notes
(`adk-agent-evaluation/references/provider-compatibility.md`,
`adk-agent-observability/references/export-paths.md`, `signals-and-schema.md`),
which record source reads and offline spikes from 2026-10-25 on mlflow 3.17.2,
deepeval 4.3.1 and Opik commit 763a2ec. Treat them as `guidance`/`historical`
and confirm on the versions you install.

## Assumptions (questions nobody was available to answer)

1. Where does the nightly job run? Assumed: a Cloud Run job in the same GCP
   project, as the service account that already has Vertex AI access.
2. Are full session events retained (Vertex AI Session Service or a database in
   the project)? Assumed yes. Content capture is off in spans, so sessions are
   the only source of tool arguments and message text.
3. Which judge? Assumed a Gemini model on Vertex in this project and region,
   pinned by exact id. Judge calls send transcripts to Vertex; that stays in the
   project but needs Compliance sign-off as a data flow.
4. Hosts for MLflow and Opik: assumed in-project (Cloud SQL plus GCS for MLflow;
   GKE or a VM for Opik).
5. Do not turn content capture on in production to feed these tools.

## Verdict

| Tool | Use? | How |
| --- | --- | --- |
| deepeval | Metrics only | Do **not** call `instrument_google_adk()`. It exports to Confident AI, has no local sink, raises without `CONFIDENT_API_KEY`, and replaced ADK's native spans in the spike. |
| MLflow ADK scorers | Yes, with substitutions | Self-hosted server. Scorers wrap ADK evaluators and change what a result means (below). |
| Opik | Yes, for traces, self-hosted | Point the SDK at your own Opik. The default is Comet cloud, which breaks the compliance rule. |

## Configuration

Set these before any import of the tools (env in the job and service definitions).

deepeval
- `DEEPEVAL_TELEMETRY_OPT_OUT=1`
- `DEEPEVAL_DISABLE_DOTENV=1` (`import deepeval` otherwise loads `.env` from the
  working directory, so a stray key turns uploads on)
- no `CONFIDENT_API_KEY` anywhere
- every metric gets an explicit Vertex-backed model; `ToolCorrectnessMetric`
  builds an OpenAI client if given none. Writing the custom model wrapper is
  untested here.
- `should_exact_match=True` for tool correctness (an extra call otherwise
  passes), plus a separate forbidden-call assertion
- build test cases from session events, not spans

MLflow (self-hosted)
- server needs a SQL backend store (Cloud SQL) for OTLP ingestion; spans go to
  `/v1/traces` with the `x-mlflow-experiment-id` header
- `MLFLOW_DISABLE_TELEMETRY=true`, `DO_NOT_TRACK=true`,
  `LITELLM_LOCAL_MODEL_COST_MAP=True` on both client and server. Cloud Run jobs
  set `CLOUD_RUN_EXECUTION`, which also disables telemetry, but a Cloud Run
  service does not, and pytest cannot prove egress behaviour. Set the three
  explicitly.
- install `google-adk[eval]` for `ResponseMatch` and `Safety`
- explicit `threshold` on ADK scorers (needed to construct on 3.17.2)
- pin the judge. The default is `gemini-2.5-flash` with five samples; set the
  id and sample count yourself.
- verify egress with a network policy or VPC egress deny, not by trust

Opik (self-hosted)
- `OPIK_URL_OVERRIDE=<in-project URL>`
- `OPIK_SENTRY_ENABLE=false`, `OPIK_ANALYTICS_ENABLE=false`,
  `OPIK_ENABLE_LITELLM_MODELS_MONITORING=false`; server:
  `OPIK_USAGE_REPORT_ENABLED=false`
- its ADK integration patches ADK's global tracer and `LlmResponse.create` for
  the whole process and appends callbacks after existing ones. A guard callback
  that short-circuits may hide blocked calls from it. This was read, not run.
- do not stack a second instrumentor (for example openinference) without
  checking for one `invoke_agent` span per invocation

Production capture
- keep `ADK_CAPTURE_MESSAGE_CONTENT_IN_SPANS=false` and
  `OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT=NO_CONTENT`. Opik traces
  then show structure, timing and errors but not content. Say so in the handover.
- set `ADK_TELEMETRY_SCHEMA_VERSION_OPT_IN` explicitly and let the first trace
  show which model span name to expect.

## Nightly MLflow scoring: what to do and record

Read inputs from session events, joined to traces on `gen_ai.conversation.id`.
Never score from spans with capture off.

1. `ToolTrajectory`: supply `actual_tool_calls` from the session events. From
   traces it takes names from span names (`execute_tool get_order`), so it never
   matches. Arguments are `"{}"` with capture off, and parallel calls merge into
   one span that errors.
2. `Hallucination`: it passes no tool names or results, so tool-grounded answers
   are graded as unsupported. Call ADK's `HallucinationsV1Evaluator` directly
   with the session invocations and app details.
3. A missing ADK score is coerced to `0.0`/"no". A judge failure inside ADK
   (no credentials, wrong judge id, content absent) also returns "no"/`0.0`. A
   0.0 in MLflow is therefore not evidence of a fail until you check the row.

Record one row per (case or session, metric), with:
- `tier` (`offline`, `local`, `live` or `release`) and `outcome`
  (`pass`, `fail`, `blocked` or `not run`). The nightly scoring is `live`.
- `outcome=pass/fail` only when a real judge verdict exists. Exception, missing
  value, "not evaluated" and an unverified 0.0 from a judge metric are
  `not run` (or `blocked` for credentials/access), never `fail`.
- expected row count (sessions times metrics), scored count, error count. The
  run is incomplete if scored plus errors differs from expected. An empty
  cohort is `not run`, not a pass.
- raw value and rationale where available, error text, session id, trace id.
  Keep failed and errored rows; do not rerun until green.
- versions: mlflow, google-adk, google-genai, deepeval, judge model id, sample
  count, threshold, scorer names, prompt/config version of the agent under test.
- a judge canary row per night: one session with a known verdict. If it comes
  back 0.0, mark the whole judge metric `blocked`. This costs one judge call, so
  it needs approval before the first run.
- a do-nothing control (empty or wrong tool calls) that must fail action cases,
  to show the scorer can fail.
- report per-metric rates with denominators (for example 42/50 scored, 8 not
  run), never one blended number. Nightly scoring of existing sessions is a
  single observation per session, so do not call it pass^k.

Log to the in-project MLflow experiment, one run per night, with the rows as an
artifact (CSV or JSON) plus the counts above as metrics. Alert on `not run`
share rising, not only on pass rate falling.

## Left undone

- no packages installed, no config files added, no code written
- nothing verified on the pinned stack; the deepeval Vertex model wrapper, the
  Opik behaviour under guard callbacks and egress behaviour are unconfirmed
- nothing sent to any service. Compliance should approve the judge data flow and
  a network-level egress check before first use.
