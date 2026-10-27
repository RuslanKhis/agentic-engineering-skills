I've fixed the completion-upload bug and updated its tests. I have no shell tool in this session, so I haven't run them.

**Cause:** `app/app_utils/telemetry.py` enabled the upload hook whenever the capture setting was anything other than `"false"`. Your setting is `NO_CONTENT`, which is not `"false"`, so the hook turned on and wrote completions to `gs://<bucket>/completions`. The BigQuery `completions` external table reads from that path.

**Fix:** the hook now turns on only for `true`, `span_only`, `event_only` or `span_and_event` (case-insensitive). `NO_CONTENT`, `false`, unset and unknown values leave it off. `GOOGLE_CLOUD_AGENT_ENGINE_ENABLE_TELEMETRY` is untouched, so spans, timings and errors stay. I also corrected the log line that claimed "NO_CONTENT" while uploading.

**Tests:** in `tests/unit/test_tools_and_telemetry.py` I replaced the old test, which asserted that upload was on under `NO_CONTENT`. The new tests check that content-capture modes enable upload. They also check that `NO_CONTENT`, `false`, empty, bogus and unset values never set the hook or base path while telemetry stays on. They use made-up values only. Run them with `python -m unittest tests.unit.test_tools_and_telemetry`.

**Still open:**
- **Analytics exporter:** `BigQueryAgentAnalyticsPlugin` in `app/agent.py` writes to `travel_desk_analytics`, and its default config logs event content. That content can include tool arguments like `passport_expiry`. I couldn't inspect the installed plugin to confirm which config option (a content formatter or event filter) turns this off in `google-adk` 2.12.0, and a guessed option could break app startup. I left it unchanged. This is probably the next place prompts leak, so please check it before relying on this fix.
- **Existing data:** anything already uploaded to `<project>-travel-desk-logs/completions` or the analytics dataset is still there. I did not touch cloud resources.
- **Question I couldn't ask:** should the analytics plugin keep logging content? I assumed no, given PRIV-212.