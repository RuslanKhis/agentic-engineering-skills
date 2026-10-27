# privacy-with-observability: what the fixture holds

Standalone Agents CLI 1.11.0 project (no base): `agents-cli-manifest.yaml`,
`uv.lock`, `pyproject.toml` (google-adk 2.12.0 with the bigquery-analytics extra),
Cloud Run Terraform. README says prompts carry personal data and that content
capture in tracing was switched off.

Three export paths, each to be inspected independently (A2):

1. Spans and log events: `.env` and `service.tf` set
   `ADK_CAPTURE_MESSAGE_CONTENT_IN_SPANS=false` and
   `OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT=NO_CONTENT`. This path is
   fine; it is the setting the user believes covers everything (A3).
2. Completion upload: `app/app_utils/telemetry.py` `setup_telemetry()` enables
   `OTEL_INSTRUMENTATION_GENAI_COMPLETION_HOOK=upload` with
   `UPLOAD_BASE_PATH=gs://<LOGS_BUCKET_NAME>/completions` whenever the bucket is set
   and the capture variable is not the literal "false" — `NO_CONTENT` passes that
   test, and the log line claims "NO_CONTENT (metadata only, no prompts/responses)".
   `service.tf` sets `LOGS_BUCKET_NAME`; `telemetry.tf` exposes the uploaded
   completions as the BigQuery external table `completions`. Uploads do not honour
   the capture setting, so full prompts and responses land in GCS and BigQuery.
3. Analytics export: `app/agent.py` registers `BigQueryAgentAnalyticsPlugin` with
   default content handling (no event denylist, no `payload_column_denylist`, no
   `content_formatter`), so LLM request/response content and tool arguments reach
   BigQuery rows.

Smallest fix: switch off the completion upload (remove the hook settings or gate
them correctly) and deny content columns or content-bearing event types in the
analytics plugin, while keeping timings, errors, token counts and status (the
user wants timings and errors). A4: synthetic canary per forbidden payload with
tests that keep the approved metadata. A1/A5: protect-adk-sensitive-data primary,
observability guidance only for the configured paths, the optimise skill not
loaded. A6: live export verification left unverified.

The stdlib suite (`tests/unit/test_tools_and_telemetry.py`) passes offline; the
google-agents-cli-observability skill named in available_skills is not installed
by the runner. Context unchanged from scenarios.json.
