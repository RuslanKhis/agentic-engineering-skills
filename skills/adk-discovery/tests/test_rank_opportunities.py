"""Exercise the opportunity ranking helper through its public CLI with hand-computed fixtures."""

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "rank_opportunities.py"

BRIEF = """# Discovery brief: advertising self-service

Some prose with a number 42 that the helper ignores.

## Opportunity portfolio

| ID | Opportunity | Value (1-5) | Feasibility (1-5) | Data readiness (1-5) | Risk (1-5) | Technology fit | Outcome measure | Baseline |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| O1 | Brief interpretation and product recommendation | 4 | 4 | 3 | 2 | agent | Checkout completion rate for eligible advertisers | 31% last quarter |
| O2 | Creative asset search with rights filter | 3 | 3 | 2 | 2 | llm | Time to first usable creative | unknown |
| O3 | Pricing forecast | 3 | 2 | 4 | 3 | ml | Forecast error | known |
| O4 | Autonomous spend changes | 5 | 1 | 2 | 5 | agent | tbd | - |
"""


def run(*args, text=BRIEF):
    with tempfile.TemporaryDirectory() as directory:
        brief = Path(directory) / "brief.md"
        brief.write_text(text, encoding="utf-8")
        result = subprocess.run([sys.executable, "-I", "-B", str(SCRIPT), "--brief", str(brief), *args],
                                capture_output=True, text=True)
    return result


class RankingTests(unittest.TestCase):
    def test_ranks_by_score_and_reports_ready(self):
        result = run("--json")
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        report = json.loads(result.stdout)
        order = [entry["id"] for entry in report["ranked"]]
        # O1: 4+4+3-2 = 9; O2: 3+3+2-2 = 6; O3: 3+2+4-3 = 6; O4: 5+1+2-5 = 3.
        self.assertEqual(order[0], "O1")
        self.assertEqual(order[-1], "O4")
        self.assertEqual(report["ranked"][0]["score"], 9)
        self.assertEqual(report["first"], "O1")
        self.assertEqual(report["blocking"], [])

    def test_tie_breaks_on_lower_risk_and_warns(self):
        report = json.loads(run("--json").stdout)
        # O2 and O3 both score 6; O2 has the lower risk and comes first.
        self.assertEqual([entry["id"] for entry in report["ranked"]][1:3], ["O2", "O3"])
        tie = [message for message in report["warnings"] if "ties" in message]
        self.assertEqual(tie, [])  # ties are only reported against the first candidate
        result = run("--pick", "O2", "--json")
        report = json.loads(result.stdout)
        self.assertTrue(any("O3 ties with O2" in message for message in report["warnings"]))
        self.assertTrue(any("ranked 2, not 1" in message for message in report["warnings"]))

    def test_weights_change_the_order(self):
        report = json.loads(run("--weights", "risk=3", "--json").stdout)
        # O1: 4+4+3-6 = 5; O3: 3+2+4-9 = 0; O2: 3+3+2-6 = 2; O4: 5+1+2-15 = -7.
        self.assertEqual([entry["id"] for entry in report["ranked"]], ["O1", "O2", "O3", "O4"])
        self.assertEqual(report["ranked"][0]["score"], 5)

    def test_first_candidate_without_measure_blocks(self):
        result = run("--pick", "O4")
        self.assertEqual(result.returncode, 1)
        self.assertIn("BLOCKING O4: no outcome measure", result.stdout)
        self.assertIn("risk 5 of 5", result.stdout)
        self.assertIn("baseline unknown", result.stdout)

    def test_unclear_fit_blocks_and_process_fit_warns(self):
        text = BRIEF.replace("| agent | Checkout completion", "| unclear | Checkout completion")
        result = run(text=text)
        self.assertEqual(result.returncode, 1)
        self.assertIn("technology fit is unclear", result.stdout)
        text = BRIEF.replace("| agent | Checkout completion", "| process | Checkout completion")
        result = run(text=text)
        self.assertEqual(result.returncode, 0)
        self.assertIn("not the next step", result.stdout)

    def test_invalid_score_and_duplicate_id_are_errors(self):
        text = BRIEF.replace("| O2 | Creative", "| O1 | Creative").replace("| 3 | 2 | 4 | 3 | ml", "| 3 | 2 | 9 | 3 | ml")
        result = run(text=text)
        self.assertEqual(result.returncode, 1)
        self.assertIn("duplicate ID O1", result.stdout)
        self.assertIn("data must be 1-5, got 9", result.stdout)

    def test_missing_table_exits_two(self):
        result = run(text="# Brief\n\nNo table here.\n")
        self.assertEqual(result.returncode, 2)
        self.assertIn("no opportunity table", result.stderr)

    def test_bad_weight_exits_two(self):
        result = run("--weights", "charm=2")
        self.assertEqual(result.returncode, 2)
        self.assertIn("unknown weight", result.stderr)

    def test_cell_emphasis_is_stripped_but_identifiers_keep_underscores(self):
        text = BRIEF.replace("| Checkout completion rate for eligible advertisers |", "| **time_to_first_creative** |")
        report = json.loads(run("--json").stdout)
        self.assertEqual(report["ranked"][0]["measure"], "Checkout completion rate for eligible advertisers")
        report = json.loads(run("--json", text=text).stdout)
        self.assertEqual(report["ranked"][0]["measure"], "time_to_first_creative")

    def test_estimated_baseline_warns(self):
        text = BRIEF.replace("| 31% last quarter |", "| ~4 min (reported estimate, unmeasured) |")
        report = json.loads(run("--json", text=text).stdout)
        self.assertTrue(any("baseline is a reported estimate" in message for message in report["warnings"]))
        self.assertFalse(any("reported estimate" in message for message in json.loads(run("--json").stdout)["warnings"]))

    def test_text_output_lists_ranked_rows(self):
        result = run()
        self.assertEqual(result.returncode, 0)
        self.assertIn("First use case: O1", result.stdout)
        self.assertIn("Ready for adk-system-designer", result.stdout)


if __name__ == "__main__":
    unittest.main()
