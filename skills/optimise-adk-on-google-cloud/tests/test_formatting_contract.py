"""Offline checks for the optional bounded current-result handoff component."""

import copy
import importlib.metadata
import importlib.util
import json
from pathlib import Path
import sys
import traceback
import unittest
from unittest.mock import patch


def payload():
    return {
        "correlation_id": "query-synthetic-001",
        "columns": ["name", "amount", "active", "note"],
        "rows": [["Synthetic", 12.5, True, None]],
    }


def encoded_size(value):
    return len(json.dumps(value, ensure_ascii=False, separators=(",", ":")).encode("utf-8"))


def sized_payload(size, prefix=""):
    """Create a legal shape with an exact encoded size, independent of the asset."""
    value = {
        "correlation_id": "query-synthetic-001",
        "columns": [f"c{i:02}" for i in range(64)],
        "rows": [[""] * 64 for _ in range(2)],
    }
    value["rows"][0][0] = prefix
    remaining = size - encoded_size(value)
    if remaining < 0:
        raise AssertionError("Requested size is below fixture overhead")
    for row in value["rows"]:
        for index, cell in enumerate(row):
            count = min(1_000 - len(cell), remaining)
            row[index] += "x" * count
            remaining -= count
    if remaining or encoded_size(value) != size:
        raise AssertionError("Requested size exceeds fixture capacity")
    return value


class FormattingContract(unittest.TestCase):
    def setUp(self):
        try:
            installed = importlib.metadata.version("pydantic")
        except importlib.metadata.PackageNotFoundError:
            self.skipTest("Pydantic is absent; preserve target dependencies")
        if installed.split(".", 1)[0] != "2":
            self.skipTest("Pydantic 2 is required; preserve target dependencies")

        for target in (
            "socket.socket.connect", "socket.socket.connect_ex",
            "socket.create_connection", "socket.getaddrinfo",
        ):
            guard = patch(target, side_effect=AssertionError("Network is prohibited"))
            guard.start()
            self.addCleanup(guard.stop)

        path = Path(__file__).resolve().parents[1] / "assets/formatting_contract.py"
        module_name = "formatting_contract_under_test"
        spec = importlib.util.spec_from_file_location(module_name, path)
        self.contract = importlib.util.module_from_spec(spec)
        previous = sys.modules.get(module_name)
        sys.modules[module_name] = self.contract
        self.addCleanup(self.restore_module, module_name, previous)
        spec.loader.exec_module(self.contract)

    @staticmethod
    def restore_module(name, previous):
        if previous is None:
            sys.modules.pop(name, None)
        else:
            sys.modules[name] = previous

    def assert_invalid(self, value):
        with self.assertRaises(self.contract.FormattingInputError) as caught:
            self.contract.parse_formatting_input(value)
        self.assertEqual(str(caught.exception), "invalid_formatting_input")
        self.assertIsNone(caught.exception.__cause__)
        self.assertIsNone(caught.exception.__context__)
        return caught.exception

    def test_valid_types_and_input_are_preserved_without_aliasing(self):
        value = payload()
        value["rows"] = [["12.50", 12, False, None], ["Synthetic", 12.5, True, "ok"]]
        before = copy.deepcopy(value)
        result = self.contract.parse_formatting_input(value)
        self.assertEqual(value, before)
        self.assertEqual(result.model_dump(), before)
        self.assertIs(type(result.rows[0][1]), int)
        self.assertIs(type(result.rows[0][2]), bool)
        self.assertIs(type(result.rows[1][1]), float)
        value["rows"][0][0] = "caller-changed"
        value["columns"].append("caller-column")
        self.assertEqual(result.model_dump(), before)
        self.assertEqual(json.loads(result.canonical_bytes()), before)

    def test_empty_rows_are_valid_and_preserved(self):
        value = payload()
        value["rows"] = []
        self.assertEqual(self.contract.parse_formatting_input(value).rows, [])
        self.assertEqual(json.loads(self.contract.encode_formatting_input(value)), value)

    def test_correlation_character_and_length_bounds(self):
        for correlation in ("a" * 16, "a" * 128, "query.synthetic:_-01"):
            with self.subTest(valid=correlation):
                self.contract.parse_formatting_input({**payload(), "correlation_id": correlation})
        for correlation in ("a" * 15, "a" * 129, "query synthetic-001", "query-synthetic-001\n", 123):
            with self.subTest(invalid=correlation):
                self.assert_invalid({**payload(), "correlation_id": correlation})

    def test_column_count_names_and_unique_names(self):
        for columns in ([], ["x"] * 65, ["duplicate", "duplicate"], [""], ["x" * 129], [1]):
            with self.subTest(columns=columns):
                self.assert_invalid({**payload(), "columns": columns, "rows": []})
        value = {**payload(), "columns": ["x" * 128], "rows": [[1]]}
        self.contract.parse_formatting_input(value)

    def test_row_count_and_exact_column_width(self):
        value = {**payload(), "columns": ["one"], "rows": [[1]] * 20}
        self.contract.parse_formatting_input(value)
        for rows in ([[1]] * 21, [[]], [[1, 2]]):
            with self.subTest(rows=rows):
                self.assert_invalid({**value, "rows": rows})

    def test_string_character_boundary_is_independent_of_byte_boundary(self):
        value = {**payload(), "columns": ["text"], "rows": [["🌏" * 1_000]]}
        self.contract.parse_formatting_input(value)
        self.assert_invalid({**value, "rows": [["x" * 1_001]]})

    def test_exact_inclusive_utf8_json_byte_boundary(self):
        for prefix in ("", "é🌏", '"\\\n'):
            with self.subTest(prefix=prefix):
                value = sized_payload(64 * 1024, prefix)
                encoded = self.contract.encode_formatting_input(value)
                self.assertEqual(len(encoded), 64 * 1024)
                self.assertEqual(json.loads(encoded), value)
                self.assert_invalid(sized_payload(64 * 1024 + 1, prefix))

    def test_unicode_is_encoded_literally_and_escapes_count_towards_bytes(self):
        value = {**payload(), "columns": ["text"], "rows": [['é🌏"\\\n']]}
        encoded = self.contract.encode_formatting_input(value)
        self.assertIn("é🌏".encode("utf-8"), encoded)
        self.assertNotIn(b"\\u00e9", encoded)
        self.assertEqual(len(encoded), encoded_size(value))
        self.assertEqual(json.loads(encoded), value)

    def test_nonfinite_and_unsupported_scalar_types_are_rejected(self):
        from decimal import Decimal

        for cell in (float("nan"), float("inf"), -float("inf"), Decimal("1.2"), b"data", {}, []):
            with self.subTest(cell_type=type(cell).__name__):
                self.assert_invalid({**payload(), "columns": ["value"], "rows": [[cell]]})

    def test_strict_collections_extra_fields_and_wrong_top_level(self):
        for value in (
            {**payload(), "columns": ("name", "amount", "active", "note")},
            {**payload(), "rows": (("Synthetic", 12.5, True, None),)},
            {**payload(), "rows": [("Synthetic", 12.5, True, None)]},
            {**payload(), "extra": "private"},
            json.dumps(payload()), None, [],
        ):
            with self.subTest(value_type=type(value).__name__):
                self.assert_invalid(value)
        self.assert_invalid(self.contract.parse_formatting_input(payload()))

    def test_failed_validation_does_not_change_input_or_expose_payload(self):
        marker = "SYNTHETIC_PRIVATE_PREVIEW_802"
        value = {**payload(), "columns": [marker, marker], "rows": [[marker]]}
        before = copy.deepcopy(value)
        error = self.assert_invalid(value)
        self.assertEqual(value, before)
        self.assertNotIn(marker, str(error))
        self.assertNotIn(marker, repr(error))
        self.assertNotIn(marker, "".join(traceback.format_exception(error)))

    def test_invalid_unicode_is_a_fixed_public_failure(self):
        value = {**payload(), "columns": ["text"], "rows": [["\ud800"]]}
        self.assert_invalid(value)

    def test_reencoding_revalidates_mutated_model_contents(self):
        result = self.contract.parse_formatting_input(payload())
        result.rows[0].append("unexpected-column")
        with self.assertRaises(self.contract.FormattingInputError):
            result.canonical_bytes()


if __name__ == "__main__":
    unittest.main()
