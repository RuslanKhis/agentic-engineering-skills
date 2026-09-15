"""Portable CLI regressions; run with unittest or pytest, without dependencies."""

# Adapted from the strict alias regressions in agentic-engineering-adk-gcp.
# MIT License
# Copyright (c) 2026 RuslanKhis
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from copy import deepcopy
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "check_results.py"
SECRET = "private-cohort-do-not-echo"


def expected_contract():
    return {
        "key_columns": ["cohort"],
        "metrics": {
            "client_count": ["client_count", "total_clients"],
            "ticket_count": ["ticket_count", "total_tickets", "total_ticket_count",
                             "total_support_tickets", "total_ticket_volume"],
            "tickets_per_client": ["tickets_per_client", "avg_tickets_per_client",
                                   "average_tickets_per_client",
                                   "avg_ticket_volume_per_client"],
        },
        "rows": [
            {"cohort": "Renewed", "client_count": 2, "ticket_count": 3,
             "tickets_per_client": "1.5"},
            {"cohort": "Churned", "client_count": 1, "ticket_count": 3,
             "tickets_per_client": 3},
        ],
    }


def actual_rows():
    return {"rows": [
        {"cohort": "Churned", "total_clients": 1, "total_tickets": 3,
         "avg_tickets_per_client": "3.0"},
        {"cohort": "Renewed", "total_clients": 2, "total_tickets": 3,
         "avg_tickets_per_client": "1.5"},
    ]}


class CheckerTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory(prefix="result-checker-")
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name).resolve()
        self.expected = self.root / "expected.json"
        self.actual = self.root / f"{SECRET}.json"

    def invoke(self, *arguments):
        return subprocess.run([sys.executable, str(SCRIPT), *map(str, arguments)],
                              capture_output=True, text=True, timeout=15)

    def check(self, expected=None, actual=None, *, dry_run=False,
              expected_raw=None, actual_raw=None):
        self.expected.write_text(expected_raw if expected_raw is not None else
                                 json.dumps(expected_contract() if expected is None else expected),
                                 encoding="utf-8")
        self.actual.write_text(actual_raw if actual_raw is not None else
                               json.dumps(actual_rows() if actual is None else actual),
                               encoding="utf-8")
        return self.invoke("--expected", self.expected, "--actual", self.actual,
                           *(["--dry-run"] if dry_run else []))

    def assert_outcome(self, result, status, code=None):
        self.assertEqual(result.returncode, {"PASS": 0, "DRY_RUN": 0, "FAIL": 1,
                                            "INVALID": 2}[status])
        self.assertEqual(result.stderr, "")
        self.assertNotIn(str(self.root), result.stdout)
        self.assertNotIn(SECRET, result.stdout)
        payload = json.loads(result.stdout)
        self.assertEqual(set(payload), {"status", "reason_codes"})
        self.assertEqual(payload["status"], status)
        self.assertIsInstance(payload["reason_codes"], list)
        if code:
            self.assertIn(code, payload["reason_codes"])
        return payload

    def test_help_is_safe_and_requires_no_files(self):
        result = self.invoke("--help")
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stderr, "")
        self.assertIn("--expected", result.stdout)
        self.assertIn("--actual", result.stdout)
        self.assertIn("no verdict", result.stdout)
        self.assertIn("ignored", result.stdout)
        self.assertEqual(list(self.root.iterdir()), [])

    def test_recorded_fixture_aliases_pass_in_any_row_order(self):
        self.assert_outcome(self.check(), "PASS", "RESULTS_MATCH")

    def test_all_explicit_aliases_pass(self):
        for canonical, aliases in expected_contract()["metrics"].items():
            for alias in aliases:
                with self.subTest(alias=alias):
                    rows = {"rows": deepcopy(expected_contract()["rows"])}
                    for row in rows["rows"]:
                        row[alias] = row.pop(canonical)
                    self.assert_outcome(self.check(actual=rows), "PASS")

    def test_equivalent_simultaneous_aliases_pass(self):
        rows = actual_rows()
        rows["rows"][0].update(client_count="1.00", ticket_count="3.00",
                                tickets_per_client="3e0")
        self.assert_outcome(self.check(actual=rows), "PASS")

    def test_wrong_fractional_metrics_fail_without_echo(self):
        for field, value in [("total_clients", 2), ("total_clients", "1.5"),
                             ("total_tickets", 4), ("total_tickets", "3.5"),
                             ("avg_tickets_per_client", "1.5")]:
            with self.subTest(field=field, value=value):
                rows = actual_rows()
                rows["rows"][0][field] = value
                self.assert_outcome(self.check(actual=rows), "FAIL", "METRIC_MISMATCH")

    def test_conflicting_aliases_rejected_even_in_dry_run(self):
        rows = actual_rows()
        rows["rows"][0]["client_count"] = 99
        for dry_run in [False, True]:
            with self.subTest(dry_run=dry_run):
                self.assert_outcome(self.check(actual=rows, dry_run=dry_run),
                                    "INVALID", "CONFLICTING_ALIASES")

    def test_invalid_metric_types_and_nonfinite_rejected(self):
        for value in [True, False, None, [], {}, "NaN", "Infinity", "-Infinity",
                      "not-a-number", "1_000", " 3 ", "+3", "03"]:
            with self.subTest(value=value):
                rows = actual_rows()
                rows["rows"][0]["total_tickets"] = value
                self.assert_outcome(self.check(actual=rows), "INVALID")

    def test_invalid_expected_numeric_value_rejected(self):
        contract = expected_contract()
        contract["rows"][0]["client_count"] = None
        self.assert_outcome(self.check(expected=contract), "INVALID", "INVALID_METRIC")

    def test_nonstandard_json_constants_rejected(self):
        for value in ["NaN", "Infinity", "-Infinity"]:
            with self.subTest(value=value):
                raw = json.dumps(actual_rows()).replace('"total_clients": 1',
                                                        '"total_clients": ' + value)
                self.assert_outcome(self.check(actual_raw=raw), "INVALID",
                                    "NONFINITE_JSON_NUMBER")

    def test_missing_metric_rejected(self):
        rows = actual_rows()
        del rows["rows"][0]["total_tickets"]
        self.assert_outcome(self.check(actual=rows), "INVALID", "MISSING_METRIC")

    def test_exact_json_numbers_do_not_round_through_float(self):
        contract = {"key_columns": ["cohort"], "metrics": {"value": ["value"]},
                    "rows": [{"cohort": "one", "value": "9007199254740993"}]}
        exact = '{"rows":[{"cohort":"one","value":9007199254740993}]}'
        wrong = exact.replace("9007199254740993", "9007199254740992")
        self.assert_outcome(self.check(expected=contract, actual_raw=exact), "PASS")
        self.assert_outcome(self.check(expected=contract, actual_raw=wrong), "FAIL")
        contract["rows"][0]["value"] = "0.1000000000000000000000000001"
        decimal_raw = '{"rows":[{"cohort":"one","value":0.1000000000000000000000000001}]}'
        self.assert_outcome(self.check(expected=contract, actual_raw=decimal_raw), "PASS")
        self.assert_outcome(self.check(expected=contract,
                                      actual_raw=decimal_raw.replace("0001", "0002")), "FAIL")
        expected_raw = json.dumps(contract).replace(
            '"0.1000000000000000000000000001"', "0.1000000000000000000000000001")
        self.assert_outcome(self.check(expected_raw=expected_raw, actual_raw=decimal_raw), "PASS")
        self.assert_outcome(self.check(expected_raw=expected_raw,
                                      actual_raw=decimal_raw.replace("0001", "0002")), "FAIL")

    def test_actual_extra_fields_ignored_without_echo(self):
        rows = actual_rows()
        rows["rows"][0][SECRET] = {"private": SECRET}
        self.assert_outcome(self.check(actual=rows), "PASS")

    def test_unknown_top_level_and_expected_row_keys_rejected(self):
        for location in ["expected", "actual", "expected_row"]:
            with self.subTest(location=location):
                contract, rows = expected_contract(), actual_rows()
                target = {"expected": contract, "actual": rows,
                          "expected_row": contract["rows"][0]}[location]
                target[SECRET] = SECRET
                self.assert_outcome(self.check(contract, rows), "INVALID", "UNKNOWN_KEYS")

    def test_duplicate_json_keys_rejected_at_every_level(self):
        raws = [
            '{"rows":[],"rows":[]}',
            '{"rows":[{"cohort":"one","cohort":"two"}]}',
            '{"rows":[{"extra":{"private":1,"private":2}}]}',
        ]
        for raw in raws:
            with self.subTest(raw=raw):
                self.assert_outcome(self.check(actual_raw=raw), "INVALID", "DUPLICATE_JSON_KEY")
        raw = '{"key_columns":["cohort"],"metrics":{"v":["v"],"v":["v"]},"rows":[]}'
        self.assert_outcome(self.check(expected_raw=raw), "INVALID", "DUPLICATE_JSON_KEY")

    def test_invalid_contract_shapes_rejected(self):
        changes = [
            ("key_columns", []), ("key_columns", ["cohort", "cohort"]),
            ("key_columns", [""]), ("key_columns", [" "]), ("key_columns", [1]),
            ("metrics", {}), ("metrics", []), ("rows", []), ("rows", {}),
        ]
        for field, value in changes:
            with self.subTest(field=field, value=value):
                contract = expected_contract()
                contract[field] = value
                self.assert_outcome(self.check(expected=contract), "INVALID")

    def test_invalid_alias_contracts_rejected(self):
        for aliases in [[], ["total_clients"], ["client_count", "client_count"],
                        ["client_count", ""], ["client_count", 1],
                        ["client_count", "cohort"], ["client_count", "total_tickets"]]:
            with self.subTest(aliases=aliases):
                contract = expected_contract()
                contract["metrics"]["client_count"] = aliases
                self.assert_outcome(self.check(expected=contract), "INVALID", "INVALID_ALIASES")

    def test_canonical_alias_can_appear_after_other_aliases(self):
        contract = expected_contract()
        contract["metrics"]["client_count"].reverse()
        self.assert_outcome(self.check(expected=contract), "PASS")

    def test_duplicate_cohorts_rejected(self):
        for target in ["expected", "actual"]:
            with self.subTest(target=target):
                contract, rows = expected_contract(), actual_rows()
                data = contract if target == "expected" else rows
                data["rows"][1]["cohort"] = data["rows"][0]["cohort"]
                self.assert_outcome(self.check(contract, rows), "INVALID", "DUPLICATE_COHORT")

    def test_invalid_row_keys_rejected(self):
        for value in ["", " ", None, True, [], {}]:
            with self.subTest(value=value):
                rows = actual_rows()
                rows["rows"][0]["cohort"] = value
                self.assert_outcome(self.check(actual=rows), "INVALID", "INVALID_ROW_KEY")
        rows = actual_rows()
        del rows["rows"][0]["cohort"]
        self.assert_outcome(self.check(actual=rows), "INVALID", "MISSING_ROW_KEY")

    def test_composite_keys_and_numeric_identity(self):
        contract = {"key_columns": ["cohort", "region"], "metrics": {"v": ["v"]},
                    "rows": [{"cohort": 1, "region": "north", "v": 2},
                             {"cohort": "1", "region": "north", "v": 3}]}
        rows = {"rows": list(reversed(deepcopy(contract["rows"])))}
        self.assert_outcome(self.check(contract, rows), "PASS")
        rows["rows"][0]["cohort"] = 1
        self.assert_outcome(self.check(contract, rows), "INVALID", "DUPLICATE_COHORT")

    def test_cardinality_and_cohort_sets_must_match(self):
        for values in [[], actual_rows()["rows"][:1]]:
            with self.subTest(values=values):
                self.assert_outcome(self.check(actual={"rows": values}), "FAIL", "ROW_COUNT_MISMATCH")
        rows = actual_rows()
        rows["rows"][0]["cohort"] = SECRET
        self.assert_outcome(self.check(actual=rows), "FAIL", "COHORT_SET_MISMATCH")

    def test_dry_run_validates_inputs_but_never_compares_results(self):
        rows = actual_rows()
        rows["rows"][0]["cohort"] = SECRET
        rows["rows"][0]["total_clients"] = 900
        self.assert_outcome(self.check(actual=rows, dry_run=True), "DRY_RUN", "SHAPES_VALID_NO_VERDICT")
        self.assert_outcome(self.check(actual={"rows": []}, dry_run=True), "DRY_RUN")
        self.assert_outcome(self.check(actual_raw="not-json", dry_run=True), "INVALID")

    def test_repeat_is_idempotent_and_read_only(self):
        first = self.check()
        before = {p.name: (p.read_bytes(), p.stat().st_mtime_ns) for p in self.root.iterdir()}
        second = self.invoke("--expected", self.expected, "--actual", self.actual)
        self.assert_outcome(first, "PASS")
        self.assertEqual(first.stdout, second.stdout)
        self.assertEqual(first.returncode, second.returncode)
        self.assertEqual(before, {p.name: (p.read_bytes(), p.stat().st_mtime_ns)
                                  for p in self.root.iterdir()})

    def test_malformed_and_excessively_nested_json_fail_safely(self):
        for raw in ["", "{", "[]", "null", '{"rows":"bad"}',
                    '{"rows":[null]}', '[' * 2000 + '0' + ']' * 2000,
                    '{"rows":[],"secret":"' + SECRET + '" trailing}']:
            with self.subTest(raw_length=len(raw)):
                self.assert_outcome(self.check(actual_raw=raw), "INVALID")

    def test_file_size_limit_and_row_limit(self):
        self.assert_outcome(self.check(actual_raw=" " * (1024 * 1024 + 1)),
                            "INVALID", "FILE_TOO_LARGE")
        self.assert_outcome(self.check(expected_raw=" " * (1024 * 1024 + 1)),
                            "INVALID", "FILE_TOO_LARGE")
        rows = {"rows": [{"cohort": str(i)} for i in range(10001)]}
        self.assert_outcome(self.check(actual=rows), "INVALID", "ROW_LIMIT_EXCEEDED")
        contract = expected_contract()
        contract["rows"] = [{"cohort": str(i)} for i in range(10001)]
        self.assert_outcome(self.check(expected=contract), "INVALID", "ROW_LIMIT_EXCEEDED")

    def test_exactly_ten_thousand_rows_and_one_mib_are_allowed(self):
        contract = {"key_columns": ["k"], "metrics": {"v": ["v"]},
                    "rows": [{"k": str(i), "v": 1} for i in range(10000)]}
        rows = {"rows": list(reversed(contract["rows"]))}
        raw = json.dumps(rows)
        raw += " " * (1024 * 1024 - len(raw.encode("utf-8")))
        self.assert_outcome(self.check(expected=contract, actual_raw=raw), "PASS")

    def test_symlink_missing_directory_and_unreadable_files_rejected(self):
        self.check()
        link = self.root / "link.json"
        try:
            link.symlink_to(self.actual)
        except (OSError, NotImplementedError):
            self.skipTest("Symlinks unavailable")
        for path, code in [(link, "SYMLINK_REJECTED"),
                           (self.root / SECRET, "FILE_UNREADABLE"),
                           (self.root, "NOT_REGULAR_FILE")]:
            with self.subTest(code=code):
                self.assert_outcome(self.invoke("--expected", self.expected, "--actual", path),
                                    "INVALID", code)
        parent_link = self.root / "parent-link"
        parent_link.symlink_to(self.root, target_is_directory=True)
        self.assert_outcome(self.invoke("--expected", self.expected, "--actual",
                                        parent_link / self.actual.name),
                            "INVALID", "SYMLINK_REJECTED")
        self.actual.chmod(0)
        try:
            if not os.access(self.actual, os.R_OK):
                self.assert_outcome(self.invoke("--expected", self.expected, "--actual", self.actual),
                                    "INVALID", "FILE_UNREADABLE")
        finally:
            self.actual.chmod(0o600)

    @unittest.skipUnless(hasattr(os, "mkfifo"), "Named pipes unavailable")
    def test_named_pipe_is_rejected_without_blocking(self):
        self.check()
        pipe = self.root / "pipe"
        os.mkfifo(pipe)
        self.assert_outcome(self.invoke("--expected", self.expected, "--actual", pipe),
                            "INVALID", "NOT_REGULAR_FILE")

    def test_invalid_utf8_rejected_without_exception_text(self):
        self.check()
        self.actual.write_bytes(b"\xff" + SECRET.encode())
        self.assert_outcome(self.invoke("--expected", self.expected, "--actual", self.actual),
                            "INVALID", "MALFORMED_JSON")

    def test_bad_cli_arguments_never_echo_argument_values(self):
        for arguments in [[], ["--expected", SECRET], ["--unknown", SECRET]]:
            with self.subTest(arguments=arguments):
                self.assert_outcome(self.invoke(*arguments), "INVALID", "INVALID_ARGUMENTS")


if __name__ == "__main__":
    unittest.main()
