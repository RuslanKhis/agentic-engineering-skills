"""The garak CI gate fails on every way a run can look clean without being clean. No SDK, no garak."""
import json
import tempfile
import unittest
from pathlib import Path

from redteam.check_garak import check
from redteam.effects import findings_from_effects

PREFIX = "ci-1"


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(json.dumps(r) for r in rows) + "\n", encoding="utf-8")


class GateTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.runs = self.tmp / "garak" / "garak_runs"
        self.sidecar = self.tmp / "sidecar.jsonl"
        self.clean_report = [
            {"entry_type": "attempt", "uuid": "a1", "probe": "p.A"},
            {"entry_type": "eval", "probe": "p.A", "detector": "d.X", "passed": 1, "fails": 0, "nones": 0},
            {"entry_type": "completion"},
        ]
        self.clean_sidecar = [{"findings": []}]

    def write(self, report=None, sidecar=None, hitlog=False):
        write_jsonl(self.runs / f"{PREFIX}.report.jsonl", self.clean_report if report is None else report)
        write_jsonl(self.sidecar, self.clean_sidecar if sidecar is None else sidecar)
        if hitlog:
            write_jsonl(self.runs / f"{PREFIX}.hitlog.jsonl", [{"x": 1}])

    def problems(self):
        return check(self.tmp, PREFIX, self.sidecar)

    def test_clean_run_passes(self):
        self.write()
        self.assertEqual(self.problems(), [])

    def test_missing_report_fails(self):
        self.assertTrue(any("no garak report" in p for p in self.problems()))

    def test_missing_completion_fails(self):
        self.write(report=self.clean_report[:-1])
        self.assertTrue(any("completion" in p for p in self.problems()))

    def test_probe_without_eval_row_fails(self):
        self.write(report=[self.clean_report[0], self.clean_report[2]])
        self.assertTrue(any("no eval row" in p for p in self.problems()))

    def test_failing_and_unevaluated_outputs_fail(self):
        bad = dict(self.clean_report[1], fails=2, nones=1)
        self.write(report=[self.clean_report[0], bad, self.clean_report[2]])
        text = " ".join(self.problems())
        self.assertIn("2 failing", text)
        self.assertIn("never evaluated", text)

    def test_hitlog_fails(self):
        self.write(hitlog=True)
        self.assertTrue(any("hit log" in p for p in self.problems()))

    def test_attempt_count_mismatch_fails(self):
        self.write(sidecar=[{"findings": []}, {"findings": []}])
        self.assertTrue(any("sidecar has 2" in p for p in self.problems()))

    def test_sidecar_effect_fails_even_when_garak_passes(self):
        finding = findings_from_effects([], [{"method": "POST", "url": "u", "json": {"to": "x@collector.invalid"}}])
        self.write(sidecar=[{"findings": finding}])
        text = " ".join(self.problems())
        self.assertIn("ASI02", text)
        self.assertIn("collector.invalid", text)


class EffectTests(unittest.TestCase):
    def test_no_requests_no_findings(self):
        self.assertEqual(findings_from_effects([], []), [])

    def test_payment_and_mail_are_findings_but_mail_reads_are_not(self):
        found = findings_from_effects([{"method": "POST", "url": "https://payments.test/v1/refunds"}],
                                      [{"method": "GET", "url": "m"}, {"method": "POST", "url": "m", "json": {"to": "a"}}])
        self.assertEqual([f["effect"] for f in found], ["payments_request", "mail_sent"])


if __name__ == "__main__":
    unittest.main()
