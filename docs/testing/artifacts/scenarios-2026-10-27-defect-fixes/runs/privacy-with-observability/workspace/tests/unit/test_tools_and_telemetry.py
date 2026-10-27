import os
import unittest
from unittest import mock

from app.app_utils.analytics_privacy import CONTENT_EVENTS, drop_content
from app.app_utils.telemetry import setup_telemetry
from app.tools import draft_booking_request, search_travel_policy


class ToolTests(unittest.TestCase):
    def test_policy_search_finds_rail_rule(self):
        sections = [s["section"] for s in search_travel_policy("Should I take rail to Leeds?")["sections"]]
        self.assertIn("4.3", sections)

    def test_booking_is_only_drafted(self):
        result = draft_booking_request("A. Traveller", "LHR-EDI", "2026-11-03", "2026-11-05", "2031-02-01")
        self.assertEqual(result["status"], "drafted")


class TelemetryTests(unittest.TestCase):
    def test_no_bucket_means_no_upload_settings(self):
        with mock.patch.dict(os.environ, {}, clear=True):
            self.assertIsNone(setup_telemetry())
            self.assertNotIn("OTEL_INSTRUMENTATION_GENAI_COMPLETION_HOOK", os.environ)

    def test_no_content_mode_never_enables_completion_upload(self):
        for value in ("NO_CONTENT", "false", "", "bogus"):
            env = {"LOGS_BUCKET_NAME": "b", "OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT": value}
            with mock.patch.dict(os.environ, env, clear=True):
                setup_telemetry()
                self.assertNotIn("OTEL_INSTRUMENTATION_GENAI_COMPLETION_HOOK", os.environ, value)
                self.assertNotIn("OTEL_INSTRUMENTATION_GENAI_UPLOAD_BASE_PATH", os.environ, value)

    def test_unset_capture_setting_means_no_upload(self):
        with mock.patch.dict(os.environ, {"LOGS_BUCKET_NAME": "b"}, clear=True):
            setup_telemetry()
            self.assertNotIn("OTEL_INSTRUMENTATION_GENAI_COMPLETION_HOOK", os.environ)

    def test_explicit_content_mode_enables_completion_upload(self):
        env = {"LOGS_BUCKET_NAME": "b", "OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT": "SPAN_AND_EVENT"}
        with mock.patch.dict(os.environ, env, clear=True):
            setup_telemetry()
            self.assertEqual(os.environ["OTEL_INSTRUMENTATION_GENAI_UPLOAD_BASE_PATH"], "gs://b/completions")


class AnalyticsPrivacyTests(unittest.TestCase):
    CANARY = "Jo Example passport 000000000 expires 2031-02-01"

    def test_formatter_drops_canary(self):
        for payload in (self.CANARY, {"text": self.CANARY}, [{"parts": [self.CANARY]}]):
            self.assertNotIn("000000000", drop_content(payload, "LLM_RESPONSE"))

    def test_prompt_bearing_events_are_denied(self):
        for event in ("USER_MESSAGE_RECEIVED", "LLM_REQUEST", "TOOL_STARTING"):
            self.assertIn(event, CONTENT_EVENTS)
        for kept in ("LLM_RESPONSE", "LLM_ERROR", "TOOL_ERROR", "TOOL_COMPLETED"):
            self.assertNotIn(kept, CONTENT_EVENTS)


if __name__ == "__main__":
    unittest.main()
