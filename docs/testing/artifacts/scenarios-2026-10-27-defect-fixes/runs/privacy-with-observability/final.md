I fixed both leaks in the code, but I couldn't run any tests: this session had no shell tool. All changes are unverified until you run `python -m unittest discover -s tests/unit` with the project's interpreter.

**What was leaking**
1. **Completion upload.** `setup_telemetry()` in `app/app_utils/telemetry.py` enabled the upload hook whenever the capture setting was anything other than the string `"false"`. Your deployed value is `NO_CONTENT`, so the hook switched on and wrote prompts to `gs://<bucket>/completions`. That bucket is also exposed as the BigQuery `completions` external table.
2. **Analytics exporter.** `BigQueryAgentAnalyticsPlugin` in `app/agent.py` ran with default settings, which log full request, tool-argument and response content. The tool arguments include passport details.

**What I changed**
- **`telemetry.py`:** upload now turns on only for an explicit content mode (`true`, `1`, `span_only`, `event_only`, `span_and_event`). `NO_CONTENT`, `false`, unset and unknown values all leave it off.
- **New `app/app_utils/analytics_privacy.py` and `agent.py`:** the plugin config now skips the `USER_MESSAGE_RECEIVED`, `LLM_REQUEST` and `TOOL_STARTING` events entirely. It also replaces the content of every remaining event with a placeholder and turns off multimodal content logging.
- **What you keep:** timings, token counts and error events should still be logged, since they sit outside the content field.
- **Tests:** in `tests/unit/test_tools_and_telemetry.py`, using made-up data:
  - The `NO_CONTENT`, `false`, empty and unknown settings never enable upload.
  - An unset capture setting never enables upload.
  - An explicit content mode still does.
  - The formatter removes a fake passport string from string, dict and list payloads.
  - The denylist covers the content events and not the error or timing ones.

**Assumptions and questions**
- I assumed `BigQueryLoggerConfig` in google-adk 2.12.0 accepts `event_denylist`, `content_formatter` and `log_multi_modal_content`. I couldn't import or read the installed package. If any name is wrong, the app will fail at startup, so check this first.
- Do the plugin's error events carry content, such as an exception message that quotes the prompt? I didn't check, and the formatter doesn't touch the `error_message` field. I left it alone because you asked to keep errors.
- I didn't test the plugin end to end with a stub model.

**Left undone**
- Files already in the completions bucket and the existing BigQuery analytics rows may still hold prompts. Review and purge them yourself. I touched no cloud resources.
- I didn't change Terraform. The `completions` external table and the log sink remain, and they're harmless now but worth removing if you don't need them.
- The code sets `OTEL_INSTRUMENTATION_GENAI_COMPLETION_HOOK` only with `setdefault`. If that variable is set elsewhere in the environment, it would bypass this fix.
- I didn't set the other telemetry settings the skill's reference recommends (`ADK_TELEMETRY_IGNORE_RUN_CONFIG`, `ADK_EXPERIMENTAL_TELEMETRY`, `ADK_CAPTURE_MCP_HTTP_BODIES`), so they're still at their defaults.