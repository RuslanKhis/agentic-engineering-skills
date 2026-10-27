import json
import pathlib
import unittest

from app import eval_events, semconv_drift

ROOT = pathlib.Path(__file__).resolve().parent.parent
ROW = {"trace_id": "a" * 32, "span_id": "b" * 16, "metric": "helpfulness", "score": 0.5,
       "label": "partial", "judge_model": "gemini-3.5-pro-001"}


class DashboardDriftTest(unittest.TestCase):
    def setUp(self):
        self.dashboard = json.loads((ROOT / "dashboards" / "agent-overview.json").read_text())

    def test_dashboard_does_not_use_removed_gen_ai_system(self):
        self.assertFalse([w for w in semconv_drift.check(self.dashboard, []) if "removed" in w])

    def test_old_dashboard_is_flagged(self):
        old = {"panels": [{"title": "p", "query": "count(spans) where gen_ai.system exists"}]}
        self.assertTrue(semconv_drift.check(old, []))

    def test_key_missing_from_export_is_flagged(self):
        spans = [{"name": "x", "attributes": {"gen_ai.operation.name": "invoke_agent"}}]
        self.assertTrue(any("gen_ai.tool.name" in w for w in semconv_drift.check(self.dashboard, spans)))


class EvalEventTest(unittest.TestCase):
    def test_event_carries_trace_context_and_judge_identity(self):
        event = eval_events.build_event(ROW, "v1")
        self.assertEqual(event["trace_id"], int("a" * 32, 16))
        self.assertEqual(event["attributes"]["gen_ai.evaluation.name"], "helpfulness")
        self.assertEqual(event["attributes"]["support.judge.rubric_version"], "v1")

    def test_rows_without_trace_context_are_skipped_and_counted(self):
        sent = []
        skipped = eval_events.emit_events([ROW, {**ROW, "trace_id": ""}], "v1", sent.append)
        self.assertEqual((len(sent), skipped), (1, 1))


if __name__ == "__main__":
    unittest.main()
