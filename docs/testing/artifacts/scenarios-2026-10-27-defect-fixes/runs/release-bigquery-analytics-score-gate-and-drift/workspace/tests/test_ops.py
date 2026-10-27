import json
import os
import subprocess
import tempfile
import unittest
from datetime import date, datetime, timedelta, timezone
from types import SimpleNamespace

from ops import golden_report, score_gate

NOW = datetime(2026, 10, 28, 2, 0, tzinfo=timezone.utc)
CFG = {"project_id": "p", "dataset_id": "d", "retries": 1,
       "checks": [{"evaluator": "error_rate", "threshold": 0.05},
                  {"evaluator": "latency", "threshold": 8000}]}


def runner_returning(*codes):
    """Fake subprocess runner: each call pops the next exit code (or raises it)."""
    queue = list(codes)

    def run(cmd, timeout):
        item = queue.pop(0)
        if isinstance(item, Exception):
            raise item
        return SimpleNamespace(returncode=item, stdout="", stderr="boom")
    run.calls_left = queue
    return run


class ScoreGateTest(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.dir.cleanup)
        self.record = os.path.join(self.dir.name, "rec.json")

    def go(self, runner, cfg=CFG):
        code = score_gate.run(cfg, self.record, runner=runner, sleep=lambda s: None,
                              now=NOW, log=lambda m: None)
        with open(self.record) as fh:
            return code, json.load(fh)

    def test_all_pass(self):
        code, rec = self.go(runner_returning(0, 0))
        self.assertEqual((code, rec["status"]), (0, "pass"))

    def test_failing_check_blocks_with_exit_1(self):
        code, rec = self.go(runner_returning(0, 1))
        self.assertEqual((code, rec["status"]), (1, "fail"))

    def test_bigquery_down_is_not_run_after_retry(self):
        runner = runner_returning(2, 2, 2, 2)
        code, rec = self.go(runner)
        self.assertEqual((code, rec["status"]), (2, "not_run"))
        self.assertEqual(runner.calls_left, [])  # each check tried twice

    def test_transient_error_then_pass(self):
        code, _ = self.go(runner_returning(2, 0, 0))
        self.assertEqual(code, 0)

    def test_fail_outranks_not_run(self):
        code, _ = self.go(runner_returning(1, 2, 2))
        self.assertEqual(code, 1)

    def test_missing_sdk_timeout_and_odd_codes_are_not_run(self):
        for item in (FileNotFoundError(), subprocess.TimeoutExpired("x", 1), 137):
            cfg = dict(CFG, retries=0, checks=CFG["checks"][:1])
            code, _ = self.go(runner_returning(item), cfg)
            self.assertEqual(code, 2, item)

    def test_unset_threshold_is_not_run_and_sdk_not_called(self):
        cfg = dict(CFG, checks=[{"evaluator": "error_rate", "threshold": None}])
        code, _ = self.go(runner_returning(), cfg)  # a call would pop from empty list
        self.assertEqual(code, 2)

    def test_sanitize_neutralises_workflow_commands(self):
        self.assertNotIn("::", score_gate.sanitize("::error::x\x1b[0m"))

    def test_check_requires_fresh_pass(self):
        self.go(runner_returning(0, 0))
        self.assertEqual(score_gate.check_record(self.record, 30, now=NOW + timedelta(hours=3), log=lambda m: None), 0)
        self.assertEqual(score_gate.check_record(self.record, 30, now=NOW + timedelta(hours=40), log=lambda m: None), 2)

    def test_check_blocks_on_fail_missing_and_corrupt(self):
        quiet = lambda m: None  # noqa: E731
        self.assertEqual(score_gate.check_record(self.record, 30, now=NOW, log=quiet), 2)
        self.go(runner_returning(1, 0))
        self.assertEqual(score_gate.check_record(self.record, 30, now=NOW, log=quiet), 1)
        with open(self.record, "w") as fh:
            fh.write("{")
        self.assertEqual(score_gate.check_record(self.record, 30, now=NOW, log=quiet), 2)

    def test_shipped_config_cannot_pass_until_thresholds_are_set(self):
        cfg = score_gate.load_config("ops/score_gate.json")
        self.assertTrue(any(c["threshold"] is None for c in cfg["checks"]))


class GoldenReportTest(unittest.TestCase):
    rows = golden_report.load_golden("bq/golden_questions.csv")

    def test_forty_questions_collapse_to_eight_templates(self):
        self.assertEqual(len(self.rows), 40)
        self.assertEqual(len(golden_report.template_groups(self.rows)), 8)

    def test_render_without_inputs_says_not_available(self):
        text = golden_report.render(self.rows, date(2026, 11, 1))
        self.assertIn("Not available: no drift result", text)
        self.assertIn("Not available: no pass history", text)
        self.assertIn("distinct after masking order ids: 8", text)

    def test_saturation_needs_enough_runs(self):
        hist = {"gq-001": [True] * 10, "gq-002": [True] * 3, "gq-003": [True] * 9 + [False]}
        self.assertEqual(golden_report.saturated(hist, 10), ["gq-001"])

    def test_staleness_and_drift_section(self):
                # 2026-11-01 is 92 and 91 days after the 08-01 and 08-02 reviews; 08-03 is exactly 90.
        self.assertEqual(golden_report.stale_questions(self.rows, date(2026, 11, 1), 90),
                         ["gq-001", "gq-002", "gq-029", "gq-030"])
        self.assertEqual(len(golden_report.stale_questions(self.rows, date(2026, 11, 1), 90)), 4)
        drift = {"coverage_percentage": 62.5, "uncovered_questions": ["Please cancel HO-10007"], "details": {}}
        text = golden_report.render(self.rows, date(2026, 11, 1), drift=drift)
        self.assertIn("62.5%", text)
        self.assertIn("Please cancel HO-10007", text)


if __name__ == "__main__":
    unittest.main()
