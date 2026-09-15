"""Exercise the real CLI with synthetic files; no ADK or provider dependency."""

import csv
from copy import deepcopy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "check_eval_results.py"
HEADER = ["eval_set_id", "eval_id", "metric_name", "threshold", "score", "eval_status",
          "prompt", "actual_response", "actual_tool_calls"]
SECRET = "NEVER_PRINT_PRIVATE_EVIDENCE_92f61"


class CheckResultsTests(unittest.TestCase):
    def setUp(self):
        self.workspace = tempfile.TemporaryDirectory(prefix=SECRET)
        self.addCleanup(self.workspace.cleanup)
        self.root = Path(self.workspace.name)
        self.csv_path = self.root / "results.csv"
        self.expected_path = self.root / "expectations.json"
        self.expected = {
            "eval_set_id": "refund_flow",
            "cases": ["eligible_damaged_order", "final_sale_order",
                      "other_customers_order", "missing_order_id"],
            "runs_per_case": 5,
            "criteria": {
                "tool_trajectory_avg_score": {"threshold": 1.0, "comparison": "gte"},
                "response_match_score": {"threshold": 0.3, "comparison": "gte"},
            },
        }
        self.rows = [
            ["refund_flow", case, metric, str(rule["threshold"]), "1.0", "PASSED",
             SECRET + '\nquoted "prompt"', SECRET, SECRET]
            for case in self.expected["cases"]
            for metric, rule in self.expected["criteria"].items()
            for _ in range(5)
        ]
        self.write_expected()
        self.write_csv()

    def write_expected(self):
        self.expected_path.write_text(json.dumps(self.expected), encoding="utf-8")

    def write_csv(self, rows=None, header=None):
        with self.csv_path.open("w", encoding="utf-8", newline="") as stream:
            writer = csv.writer(stream)
            writer.writerow(HEADER if header is None else header)
            writer.writerows(self.rows if rows is None else rows)

    def invoke(self, *extra, expected_code=0):
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "--csv", str(self.csv_path),
             "--expectations", str(self.expected_path), *extra],
            text=True, capture_output=True, timeout=10, check=False,
        )
        self.assertEqual(result.returncode, expected_code, result.stdout + result.stderr)
        self.assertNotIn(SECRET, result.stdout + result.stderr)
        self.assertNotIn(str(self.root), result.stdout + result.stderr)
        return result

    def test_valid_complete_gate_is_repeatable_and_read_only(self):
        before = (self.csv_path.read_bytes(), self.expected_path.read_bytes())
        first = self.invoke()
        second = self.invoke()
        self.assertEqual(first.stdout, second.stdout)
        self.assertIn("all 40 metric rows", first.stdout)
        self.assertEqual(before, (self.csv_path.read_bytes(), self.expected_path.read_bytes()))

    def test_chapter_aggregate_can_pass_with_two_failed_individual_rows(self):
        rows = [row for row in self.rows
                if row[1:3] == ["other_customers_order", "response_match_score"]]
        for row in rows[:2]:
            row[4:6] = ["0.2", "FAILED"]
        self.assertGreater(sum(float(row[4]) for row in rows) / 5, 0.3)
        self.write_csv()
        self.assertIn("2 rows failed", self.invoke(expected_code=1).stdout)

    def test_missing_and_duplicate_rows_fail_exact_counts(self):
        for rows in (self.rows[:-1], self.rows + [self.rows[0]], []):
            with self.subTest(length=len(rows)):
                self.write_csv(rows=rows)
                self.assertIn("count mismatches", self.invoke(expected_code=1).stdout)

    def test_unknown_set_case_and_metric_fail_without_echoing_values(self):
        for column in (0, 1, 2):
            with self.subTest(column=column):
                rows = deepcopy(self.rows)
                rows[0][column] = SECRET
                self.write_csv(rows=rows)
                self.invoke(expected_code=1)

    def test_changed_threshold_and_inconsistent_passed_score_fail(self):
        for column, value in ((3, "0.5"), (4, "0.0"), (5, ""), (5, "NOT_EVALUATED")):
            with self.subTest(column=column, value=value):
                rows = deepcopy(self.rows)
                rows[0][column] = value
                self.write_csv(rows=rows)
                self.invoke(expected_code=1)

    def test_nonfinite_blank_and_invalid_numeric_cells_are_invalid_input(self):
        for column in (3, 4):
            for value in ("NaN", "Infinity", "-Infinity", "", SECRET):
                with self.subTest(column=column, value=value):
                    rows = deepcopy(self.rows)
                    rows[0][column] = value
                    self.write_csv(rows=rows)
                    self.invoke(expected_code=2)

    def test_lower_is_better_and_decimal_threshold_equality(self):
        self.expected["criteria"]["response_match_score"] = {
            "threshold": 0.3, "comparison": "lte"}
        for row in self.rows:
            if row[2] == "response_match_score":
                row[3:5] = ["0.3000", "0.3"]
        self.write_expected()
        self.write_csv()
        self.invoke()
        self.rows[-1][4] = "0.30000000000000001"
        self.write_csv()
        self.invoke(expected_code=1)

    def test_missing_extra_cells_and_invalid_quoting_are_invalid(self):
        for row in (self.rows[0][:-1], self.rows[0] + [SECRET]):
            self.write_csv(rows=[row])
            self.invoke(expected_code=2)
        self.csv_path.write_text(
            ",".join(HEADER) + '\n"unterminated,' + SECRET, encoding="utf-8")
        self.invoke(expected_code=2)

    def test_duplicate_missing_and_empty_header_names_are_invalid(self):
        for header in (HEADER + ["score"], HEADER[1:], HEADER + [""], []):
            with self.subTest(header=header):
                self.write_csv(rows=[], header=header)
                self.invoke(expected_code=2)

    def test_invalid_json_and_duplicate_keys_are_rejected(self):
        for content in ("{" + SECRET, '{"eval_set_id":"a","eval_set_id":"b"}',
                        "[]", json.dumps({**self.expected, "secret": SECRET})):
            self.expected_path.write_text(content, encoding="utf-8")
            self.invoke(expected_code=2)

    def test_unrepresentable_json_number_has_a_sanitised_error(self):
        content = json.dumps(self.expected).replace(
            '"threshold": 0.3', '"threshold": 1e999999999999999999999999999')
        self.expected_path.write_text(content, encoding="utf-8")
        self.invoke(expected_code=2)

    def test_expectations_schema_rejects_bad_counts_cases_and_criteria(self):
        variants = []
        for value in (0, -1, True, 1.5, 100_001):
            variants.append({**self.expected, "runs_per_case": value})
        for value in ([], ["a", "a"], [""], [True], "a"):
            variants.append({**self.expected, "cases": value})
        for value in ({}, {"x": {"threshold": True, "comparison": "gte"}},
                      {"x": {"threshold": float("nan"), "comparison": "gte"}},
                      {"x": {"threshold": 0, "comparison": "eq"}},
                      {"x": {"threshold": 0, "comparison": "gte", "extra": SECRET}}):
            variants.append({**self.expected, "criteria": value})
        for value in variants:
            with self.subTest(value=value):
                self.expected_path.write_text(json.dumps(value), encoding="utf-8")
                self.invoke(expected_code=2)

    def test_dry_run_only_validates_header_and_expectations(self):
        self.csv_path.write_bytes((",".join(HEADER) + "\n").encode()
                                  + b'"unterminated,' + b'\xff' + SECRET.encode())
        result = self.invoke("--dry-run")
        self.assertIn("not a gate verdict", result.stdout)
        self.assertIn("Data rows were not read or evaluated", result.stdout)
        self.invoke(expected_code=2)
        self.write_csv(rows=[], header=["wrong"])
        self.invoke("--dry-run", expected_code=2)

    def test_file_size_and_field_limits_fail_closed(self):
        with self.csv_path.open("wb") as stream:
            stream.truncate(10 * 1024 * 1024 + 1)
        self.invoke("--dry-run", expected_code=2)
        self.rows[0][-1] = "x" * (64 * 1024 + 1)
        self.write_csv()
        self.invoke(expected_code=2)
        self.expected_path.write_text(" " * (64 * 1024 + 1), encoding="utf-8")
        self.invoke(expected_code=2)

    def test_unreadable_input_help_and_cli_errors_do_not_disclose_paths(self):
        self.csv_path.unlink()
        self.invoke(expected_code=2)
        result = self.invoke("--help")
        self.assertIn("comparison", result.stdout)
        self.assertIn("No trial-ID pairing", result.stdout)
        self.invoke("--unknown=" + SECRET, expected_code=2)
        result = subprocess.run([sys.executable, str(SCRIPT)], text=True,
                                capture_output=True, timeout=10, check=False)
        self.assertEqual(result.returncode, 2)


if __name__ == "__main__":
    unittest.main()
