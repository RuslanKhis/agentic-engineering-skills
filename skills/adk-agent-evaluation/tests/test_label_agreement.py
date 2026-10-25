"""Exercise the label-agreement checker through its CLI with synthetic labels."""

import csv
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "label_agreement.py"
FIELDS = ["case_id", "criterion", "rater", "label", "critique", "labeller", "criteria_version", "labelled_at",
          "split"]


def run(*args):
    completed = subprocess.run([sys.executable, "-I", str(SCRIPT), *map(str, args)],
                               capture_output=True, text=True, timeout=60)
    return completed.returncode, completed.stdout, completed.stderr


def row(case, rater, label, criterion="cites_policy", version="v01", split="", critique=""):
    return {"case_id": case, "criterion": criterion, "rater": rater, "label": label,
            "critique": critique, "labeller": "senior underwriter", "criteria_version": version, "labelled_at": "2026-10-20", "split": split}


def two_raters(both_pass, both_fail, first_only_fail, second_only_fail):
    """Contingency counts to rows: first rater fails a case in both_fail and first_only_fail."""
    rows, number = [], 0
    for count, (a, b) in ((both_pass, ("pass", "pass")), (both_fail, ("fail", "fail")),
                          (first_only_fail, ("fail", "pass")), (second_only_fail, ("pass", "fail"))):
        for _ in range(count):
            number += 1
            rows += [row(f"c{number:03d}", "underwriter_a", a), row(f"c{number:03d}", "underwriter_b", b)]
    return rows


def judge_rows(gold_fail, gold_pass, missed, false_alarms, split="test", prefix=""):
    rows = []
    for index in range(gold_fail):
        case = f"{prefix}f{index:03d}"
        rows.append(row(case, "adjudicated", "fail", split=split))
        rows.append(row(case, "judge", "pass" if index < missed else "fail"))
    for index in range(gold_pass):
        case = f"{prefix}p{index:03d}"
        rows.append(row(case, "adjudicated", "pass", split=split))
        rows.append(row(case, "judge", "fail" if index < false_alarms else "pass"))
    return rows


class LabelAgreementTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)

    def write_csv(self, rows, name="labels.csv"):
        path = self.root / name
        with path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=FIELDS)
            writer.writeheader()
            writer.writerows(rows)
        return path

    def write_jsonl(self, rows, name="labels.jsonl"):
        path = self.root / name
        path.write_text("".join(json.dumps(item) + "\n" for item in rows), encoding="utf-8")
        return path

    def test_kappa_matches_the_textbook_example(self):
        # 20 both yes, 15 both no, 5 and 10 split: observed 0.70, expected 0.50, kappa 0.40.
        path = self.write_csv(two_raters(both_pass=15, both_fail=20, first_only_fail=5, second_only_fail=10))
        code, out, _ = run("--labels", path, "--json", "--min-kappa", "0.3")
        report = json.loads(out)
        pair = report["agreement"][0]
        self.assertEqual(pair["kappa"], 0.4)
        self.assertEqual(pair["percent_agreement"], 70.0)
        self.assertEqual(len(pair["disagreements"]), 15)
        self.assertEqual(code, 0)

    def test_low_kappa_needs_attention_and_lists_disagreements(self):
        path = self.write_csv(two_raters(both_pass=15, both_fail=20, first_only_fail=5, second_only_fail=10))
        code, out, _ = run("--labels", path)
        self.assertEqual(code, 1)
        self.assertIn("kappa 0.40 below 0.60", out)
        self.assertIn("adjudicate c036: underwriter_a=fail underwriter_b=pass", out)

    def test_imbalanced_classes_explain_low_kappa_despite_high_agreement(self):
        path = self.write_csv(two_raters(both_pass=45, both_fail=1, first_only_fail=2, second_only_fail=2))
        code, out, _ = run("--labels", path)
        self.assertEqual(code, 1)
        self.assertIn("classes are imbalanced", out)

    def test_one_label_everywhere_makes_kappa_undefined(self):
        path = self.write_csv(two_raters(both_pass=10, both_fail=0, first_only_fail=0, second_only_fail=0))
        code, out, _ = run("--labels", path)
        self.assertEqual(code, 1)
        self.assertIn("kappa undefined", out)

    def test_critiques_stay_hidden_unless_asked(self):
        rows = [row("c1", "underwriter_a", "fail", critique="PRIVATE customer text"),
                row("c1", "underwriter_b", "pass"), row("c2", "underwriter_a", "pass"),
                row("c2", "underwriter_b", "pass")]
        path = self.write_jsonl(rows)
        _, hidden, _ = run("--labels", path)
        self.assertNotIn("PRIVATE", hidden)
        _, shown, _ = run("--labels", path, "--show-critiques")
        self.assertIn("PRIVATE customer text", shown)

    def test_judge_rates_use_fail_as_positive_on_the_test_split(self):
        rows = judge_rows(gold_fail=40, gold_pass=50, missed=4, false_alarms=10)
        rows += judge_rows(gold_fail=5, gold_pass=5, missed=5, false_alarms=5, split="dev", prefix="dev-")
        path = self.write_csv(rows)
        code, out, _ = run("--labels", path, "--judge", "judge", "--json")
        result = json.loads(out)["judge"][0]
        self.assertEqual(result["split"], "test")
        self.assertEqual((result["reference_fails"], result["reference_passes"]), (40, 50))
        self.assertEqual(result["tpr"], 0.9)
        self.assertEqual(result["tnr"], 0.8)
        self.assertEqual(len(result["missed_failures"]), 4)
        self.assertEqual(code, 0)

    def test_judge_below_threshold_is_flagged(self):
        path = self.write_csv(judge_rows(gold_fail=30, gold_pass=30, missed=12, false_alarms=0))
        code, out, _ = run("--labels", path, "--judge", "judge")
        self.assertEqual(code, 1)
        self.assertIn("judge TPR 0.60 below 0.80", out)
        self.assertIn("missed failure f000", out)

    def test_judge_rates_refused_on_too_few_cases_per_class(self):
        path = self.write_csv(judge_rows(gold_fail=8, gold_pass=60, missed=0, false_alarms=0))
        code, out, _ = run("--labels", path, "--judge", "judge")
        self.assertEqual(code, 1)
        self.assertIn("NOT REPORTED", out)
        self.assertNotIn("TPR 1.00", out)

    def test_unsplit_reference_is_noted_as_not_held_out(self):
        path = self.write_csv(judge_rows(gold_fail=30, gold_pass=30, missed=0, false_alarms=0, split=""))
        code, out, _ = run("--labels", path, "--judge", "judge")
        self.assertEqual(code, 0)
        self.assertIn("not a held-out result", out)

    def test_criteria_drift_asks_for_re_review(self):
        rows = two_raters(both_pass=10, both_fail=10, first_only_fail=0, second_only_fail=0)
        for item in rows[:6]:
            item["criteria_version"] = "v00"
        path = self.write_csv(rows)
        code, out, _ = run("--labels", path)
        self.assertEqual(code, 1)
        self.assertIn("span criteria versions v00, v01", out)
        self.assertIn("re-review the 3 labelled under an older version", out)

    def test_gold_rows_without_provenance_are_reported(self):
        rows = judge_rows(gold_fail=30, gold_pass=30, missed=0, false_alarms=0)
        for item in rows:
            if item["rater"] == "adjudicated":
                item["labelled_at"] = ""
        path = self.write_csv(rows)
        code, out, _ = run("--labels", path, "--judge", "judge")
        self.assertEqual(code, 1)
        self.assertIn("60 adjudicated labels lack labelled_at", out)

    def test_consensus_reference_is_indicative_and_still_needs_cases_per_class(self):
        rows = two_raters(both_pass=35, both_fail=32, first_only_fail=3, second_only_fail=0)
        for index in range(1, 71):
            truth = "fail" if 36 <= index <= 67 else "pass"
            missed = truth == "fail" and index < 40
            rows.append(row(f"c{index:03d}", "judge", "pass" if missed else truth))
        path = self.write_csv(rows)
        code, out, _ = run("--labels", path, "--judge", "judge", "--reference", "consensus")
        self.assertIn("judge on cites_policy (no split, 67 cases: 32 fail, 35 pass): TPR 0.88, TNR 1.00", out)
        self.assertIn("indicative, not a calibration", out)
        code, out, _ = run("--labels", path, "--judge", "judge", "--reference", "consensus", "--min-per-class", "33")
        self.assertIn("NOT REPORTED", out)
        self.assertEqual(code, 1)

    def test_criteria_version_filter_compares_agreement_before_and_after(self):
        rows = two_raters(both_pass=10, both_fail=10, first_only_fail=5, second_only_fail=5)
        for item in rows[:20]:
            item["criteria_version"] = "v00"
        path = self.write_csv(rows)
        _, out, _ = run("--labels", path, "--criteria-version", "v00", "--json")
        self.assertEqual(json.loads(out)["agreement"][0]["cases"], 10)
        _, out, _ = run("--labels", path, "--criteria-version", "v01", "--json")
        self.assertEqual(json.loads(out)["agreement"][0]["cases"], 20)

    def test_judge_at_an_older_criteria_version_is_reported(self):
        rows = judge_rows(gold_fail=30, gold_pass=30, missed=0, false_alarms=0)
        for item in rows:
            if item["rater"] == "judge":
                item["criteria_version"] = "v00"
        path = self.write_csv(rows)
        code, out, _ = run("--labels", path, "--judge", "judge")
        self.assertEqual(code, 1)
        self.assertIn("judge implements criteria v00 but the reference is at v01", out)

    def test_several_files_and_formats_combine(self):
        experts = self.write_csv(two_raters(both_pass=12, both_fail=12, first_only_fail=0, second_only_fail=0))
        judge = self.write_jsonl([row("c001", "judge", "pass")])
        code, out, _ = run("--labels", experts, judge, "--judge", "judge")
        self.assertIn("no 'adjudicated' labels", out)
        self.assertEqual(code, 1)

    def test_invalid_label_and_duplicate_verdicts_exit_2(self):
        bad = self.write_csv([row("c1", "a", "maybe")], name="bad.csv")
        code, _, err = run("--labels", bad)
        self.assertEqual(code, 2)
        self.assertIn("label must be pass or fail", err)
        dup = self.write_csv([row("c1", "a", "pass"), row("c1", "a", "fail")], name="dup.csv")
        code, _, err = run("--labels", dup)
        self.assertEqual(code, 2)
        self.assertIn("second label from a for case c1", err)

    def test_missing_header_field_exits_2(self):
        path = self.root / "short.csv"
        path.write_text("case_id,rater,label\nc1,a,pass\n", encoding="utf-8")
        code, _, err = run("--labels", path)
        self.assertEqual(code, 2)
        self.assertIn("lacks criterion", err)


if __name__ == "__main__":
    unittest.main()
