#!/usr/bin/env python3
"""Compare local JSON result rows with an explicit, exact numeric contract.

Expected: {"key_columns": ["cohort"], "metrics": {"count": ["count", "total"]},
           "rows": [{"cohort": "example", "count": 2}]}
Actual:   {"rows": [{"cohort": "example", "total": "2.00"}]}

Top-level keys and expected-row fields are strict. Actual-row extra nonmetric
fields are ignored; duplicate JSON keys are rejected even inside ignored fields.
Cohort keys are nonblank strings or finite JSON numbers. Strings and numbers
remain different keys; equivalent numeric forms identify the same key. Metric
strings must use JSON number syntax (no whitespace, underscores, or leading +).
Canonical metric names must be included in their approved alias lists. All
simultaneously present aliases must be valid, finite, and numerically identical.
Rows are unordered. This checker does not verify route, SQL, job evidence,
authorisation, source freshness, latency, or completeness beyond the supplied
contract. It reads local regular files only, at most 1 MiB and 10,000 rows each.
Symlink path components are rejected. It performs no network calls or writes.

Normal output is a JSON status and fixed reason codes, never input values or
paths. Exit codes: 0 PASS/DRY_RUN/help, 1 comparison FAIL, 2 INVALID input or CLI.
Missing/invalid metric fields or conflicting aliases are INVALID, not verdicts.
--dry-run validates shapes and numeric/alias consistency only: no verdict about
cross-input row counts, cohort sets, or metric equality is produced. --help
prints this static usage documentation instead of a comparison result.
"""

# Adapted from the strict alias checks in agentic-engineering-adk-gcp.
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

from __future__ import annotations

import argparse
from decimal import Decimal, InvalidOperation
import json
import os
from pathlib import Path
import re
import stat
import sys


MAX_BYTES = 1024 * 1024
MAX_ROWS = 10_000
NUMBER = re.compile(r"-?(?:0|[1-9][0-9]*)(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?\Z")


class InvalidInput(Exception):
    """Carry a fixed public code, never an input value or exception message."""

    def __init__(self, code: str):
        self.code = code
        super().__init__(code)


class SafeArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        # argparse's ordinary error text can include arbitrary argument values.
        raise InvalidInput("INVALID_ARGUMENTS")


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise InvalidInput("DUPLICATE_JSON_KEY")
        result[key] = value
    return result


def _reject_constant(value):
    raise InvalidInput("NONFINITE_JSON_NUMBER")


def _read_json(filename: str):
    """Bound reads; check symlinks, regular-file type, and open-file identity."""
    descriptor = None
    try:
        path = Path(filename).absolute()
        # Do not resolve(): resolving first would hide symlinks from this check.
        for component in reversed((path, *path.parents)):
            if stat.S_ISLNK(component.lstat().st_mode):
                raise InvalidInput("SYMLINK_REJECTED")
        before = path.lstat()
        if not stat.S_ISREG(before.st_mode):
            raise InvalidInput("NOT_REGULAR_FILE")
        if before.st_size > MAX_BYTES:
            raise InvalidInput("FILE_TOO_LARGE")
        flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_NONBLOCK", 0)
        descriptor = os.open(path, flags)
        opened = os.fstat(descriptor)
        if not stat.S_ISREG(opened.st_mode):
            raise InvalidInput("NOT_REGULAR_FILE")
        if (opened.st_dev, opened.st_ino) != (before.st_dev, before.st_ino):
            raise InvalidInput("FILE_CHANGED")
        if opened.st_size > MAX_BYTES:
            raise InvalidInput("FILE_TOO_LARGE")
        with os.fdopen(descriptor, "rb") as stream:
            descriptor = None
            data = stream.read(MAX_BYTES + 1)
        if len(data) > MAX_BYTES:
            raise InvalidInput("FILE_TOO_LARGE")
    except (OSError, ValueError):
        raise InvalidInput("FILE_UNREADABLE") from None
    finally:
        if descriptor is not None:
            os.close(descriptor)
    try:
        return json.loads(data.decode("utf-8"), object_pairs_hook=_unique_object,
                          parse_float=Decimal, parse_int=Decimal,
                          parse_constant=_reject_constant)
    except (UnicodeError, ValueError, InvalidOperation, RecursionError):
        raise InvalidInput("MALFORMED_JSON") from None


def _object_fields(value, required: set[str]):
    if not isinstance(value, dict):
        raise InvalidInput("INVALID_SHAPE")
    if set(value) - required:
        raise InvalidInput("UNKNOWN_KEYS")
    if required - set(value):
        raise InvalidInput("MISSING_FIELDS")


def _name(value) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _rows(value, *, expected: bool):
    if not isinstance(value, list):
        raise InvalidInput("INVALID_ROWS")
    if len(value) > MAX_ROWS:
        raise InvalidInput("ROW_LIMIT_EXCEEDED")
    if expected and not value:
        raise InvalidInput("EMPTY_EXPECTED_ROWS")
    if any(not isinstance(row, dict) for row in value):
        raise InvalidInput("INVALID_ROW")
    return value


def _metric(value) -> Decimal:
    if isinstance(value, Decimal):
        number = value
    elif isinstance(value, str) and NUMBER.fullmatch(value):
        try:
            number = Decimal(value)
        except (InvalidOperation, ValueError):
            raise InvalidInput("INVALID_METRIC") from None
    else:
        # JSON numbers were parsed directly as Decimal; bool/null/containers
        # cannot enter by numeric coercion, and permissive Decimal strings fail.
        raise InvalidInput("INVALID_METRIC")
    if not number.is_finite():
        raise InvalidInput("NONFINITE_METRIC")
    return number


def _row_key(row, key_columns):
    key = []
    for column in key_columns:
        if column not in row:
            raise InvalidInput("MISSING_ROW_KEY")
        value = row[column]
        if isinstance(value, str) and value.strip():
            key.append(("string", value))
        elif isinstance(value, Decimal) and value.is_finite():
            key.append(("number", value))
        else:
            raise InvalidInput("INVALID_ROW_KEY")
    return tuple(key)


def _index_rows(rows, key_columns, metrics, *, expected: bool):
    index = {}
    for row in rows:
        if expected:
            if set(row) - set(key_columns) - set(metrics):
                raise InvalidInput("UNKNOWN_KEYS")
        key = _row_key(row, key_columns)
        if key in index:
            raise InvalidInput("DUPLICATE_COHORT")
        values = {}
        for canonical, aliases in metrics.items():
            names = [canonical] if expected else aliases
            present = [name for name in names if name in row]
            if not present:
                raise InvalidInput("MISSING_METRIC")
            numbers = [_metric(row[name]) for name in present]
            if any(number != numbers[0] for number in numbers[1:]):
                raise InvalidInput("CONFLICTING_ALIASES")
            values[canonical] = numbers[0]
        index[key] = values
    return index


def validate_expected(document):
    _object_fields(document, {"key_columns", "metrics", "rows"})
    columns = document["key_columns"]
    if (not isinstance(columns, list) or not columns or
            any(not _name(column) for column in columns) or
            len(set(columns)) != len(columns)):
        raise InvalidInput("INVALID_KEY_COLUMNS")
    metrics = document["metrics"]
    if not isinstance(metrics, dict) or not metrics:
        raise InvalidInput("INVALID_METRICS")
    seen_aliases = set(columns)
    for canonical, aliases in metrics.items():
        if (not _name(canonical) or not isinstance(aliases, list) or not aliases or
                any(not _name(alias) for alias in aliases) or
                canonical not in aliases or len(set(aliases)) != len(aliases) or
                seen_aliases.intersection(aliases)):
            raise InvalidInput("INVALID_ALIASES")
        seen_aliases.update(aliases)
    rows = _rows(document["rows"], expected=True)
    return columns, metrics, _index_rows(rows, columns, metrics, expected=True)


def validate_actual(document, columns, metrics):
    _object_fields(document, {"rows"})
    rows = _rows(document["rows"], expected=False)
    return _index_rows(rows, columns, metrics, expected=False)


def _emit(status: str, code: str) -> int:
    print(json.dumps({"status": status, "reason_codes": [code]}, sort_keys=True))
    return {"PASS": 0, "DRY_RUN": 0, "FAIL": 1, "INVALID": 2}[status]


def main(argv=None) -> int:
    parser = SafeArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter,
                                allow_abbrev=False)
    parser.add_argument("--expected", required=True, metavar="PATH",
                        help="Expected contract JSON, read-only.")
    parser.add_argument("--actual", required=True, metavar="PATH",
                        help="Actual rows JSON, read-only; extra nonmetric fields are ignored.")
    parser.add_argument("--dry-run", action="store_true",
                        help="Validate input shapes and metrics only; no verdict.")
    try:
        arguments = parser.parse_args(argv)
        columns, metrics, expected = validate_expected(_read_json(arguments.expected))
        actual = validate_actual(_read_json(arguments.actual), columns, metrics)
        if arguments.dry_run:
            return _emit("DRY_RUN", "SHAPES_VALID_NO_VERDICT")
        if len(expected) != len(actual):
            return _emit("FAIL", "ROW_COUNT_MISMATCH")
        if expected.keys() != actual.keys():
            return _emit("FAIL", "COHORT_SET_MISMATCH")
        if any(expected[key] != actual[key] for key in expected):
            return _emit("FAIL", "METRIC_MISMATCH")
        return _emit("PASS", "RESULTS_MATCH")
    except InvalidInput as exc:
        return _emit("INVALID", exc.code)
    except (OSError, ValueError, TypeError, ArithmeticError, RecursionError):
        # Defensive boundary for platform/decoder corner cases. Never display
        # exception text: it may contain filenames, row values, or identifiers.
        return _emit("INVALID", "INPUT_PROCESSING_ERROR")


if __name__ == "__main__":
    sys.exit(main())
