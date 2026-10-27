import os
import unittest
from unittest import mock

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

    def test_bucket_enables_completion_upload(self):
        env = {"LOGS_BUCKET_NAME": "b", "OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT": "NO_CONTENT"}
        with mock.patch.dict(os.environ, env, clear=True):
            setup_telemetry()
            self.assertEqual(os.environ["OTEL_INSTRUMENTATION_GENAI_UPLOAD_BASE_PATH"], "gs://b/completions")


if __name__ == "__main__":
    unittest.main()
