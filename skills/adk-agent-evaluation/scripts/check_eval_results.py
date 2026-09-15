#!/usr/bin/env python3
"""Check individual ADK CSV metric rows against an explicit, local contract."""

from __future__ import annotations

import argparse
from collections import Counter
from contextlib import contextmanager
import csv
from decimal import Decimal, InvalidOperation
import io
import json
import os
from pathlib import Path
import stat
import sys


MAX_CSV_BYTES = 10 * 1024 * 1024
MAX_EXPECTATIONS_BYTES = 64 * 1024
MAX_HEADER_BYTES = 16 * 1024
MAX_FIELD_CHARS = 64 * 1024
MAX_ROWS = 100_000
REQUIRED_COLUMNS = {
    "eval_set_id", "eval_id", "metric_name", "threshold", "score", "eval_status"
}


class InvalidInput(Exception):
    """A deliberately sanitised input error, safe to display."""


class SafeParser(argparse.ArgumentParser):
    def error(self, message):
        self.exit(2, "ERROR: invalid command-line arguments; use --help.\n")


@contextmanager
def input_file(path: str, limit: int):
    stream = None
    try:
        # Reject special files before opening, then check the opened descriptor.
        if not Path(path).is_file():
            raise InvalidInput("Inputs must be readable regular files.")
        stream = Path(path).open("rb", buffering=0)
        info = os.fstat(stream.fileno())
        if not stat.S_ISREG(info.st_mode) or info.st_size > limit:
            raise InvalidInput("Input type or size is outside the supported limits.")
        yield stream
    except OSError:
        raise InvalidInput("An input file could not be read.") from None
    finally:
        if stream is not None:
            stream.close()


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise InvalidInput("Expectations contain duplicate JSON keys.")
        result[key] = value
    return result


def identifier(value):
    return isinstance(value, str) and 0 < len(value) <= 256 and value.strip() == value


def expectations(path: str):
    with input_file(path, MAX_EXPECTATIONS_BYTES) as stream:
        raw = stream.read(MAX_EXPECTATIONS_BYTES + 1)
    if len(raw) > MAX_EXPECTATIONS_BYTES:
        raise InvalidInput("Expectations exceed the supported size limit.")
    try:
        value = json.loads(raw.decode("utf-8-sig"), parse_float=Decimal,
                           object_pairs_hook=unique_object)
    except (UnicodeError, ValueError, RecursionError, InvalidOperation):
        raise InvalidInput("Expectations are not valid UTF-8 JSON.") from None
    if not isinstance(value, dict) or set(value) != {
        "eval_set_id", "cases", "runs_per_case", "criteria"
    }:
        raise InvalidInput("Expectations do not match the required schema.")
    cases, runs, criteria = value["cases"], value["runs_per_case"], value["criteria"]
    if (not identifier(value["eval_set_id"]) or not isinstance(cases, list)
            or not cases or not all(identifier(case) for case in cases)
            or len(set(cases)) != len(cases) or type(runs) is not int or runs < 1
            or not isinstance(criteria, dict) or not criteria):
        raise InvalidInput("Expectations contain invalid identities, counts or criteria.")
    if len(cases) * runs * len(criteria) > MAX_ROWS:
        raise InvalidInput("Expected metric row count exceeds the supported limit.")
    for name, criterion in criteria.items():
        if (not identifier(name) or not isinstance(criterion, dict)
                or set(criterion) != {"threshold", "comparison"}
                or criterion["comparison"] not in ("gte", "lte")
                or type(criterion["threshold"]) not in (int, Decimal)):
            raise InvalidInput("A criterion does not match the required schema.")
        criterion["threshold"] = Decimal(criterion["threshold"])
        if not criterion["threshold"].is_finite():
            raise InvalidInput("Criterion thresholds must be finite numbers.")
    return value


def numeric(value: str) -> Decimal:
    try:
        number = Decimal(value)
    except InvalidOperation:
        raise InvalidInput("CSV metric values must be finite numbers.") from None
    if not number.is_finite():
        raise InvalidInput("CSV metric values must be finite numbers.")
    return number


def check(path: str, expected, dry_run: bool) -> int:
    csv.field_size_limit(MAX_FIELD_CHARS)
    with input_file(path, MAX_CSV_BYTES) as stream:
        # ADK writes a single physical header line. Dry-run never reads its body.
        header_bytes = stream.readline(MAX_HEADER_BYTES + 1)
        if not header_bytes or len(header_bytes) > MAX_HEADER_BYTES:
            raise InvalidInput("CSV header is missing or exceeds the supported limit.")
        header = next(csv.reader([header_bytes.decode("utf-8-sig")], strict=True))
        if (not header or any(not name.strip() for name in header)
                or len(set(header)) != len(header)
                or not REQUIRED_COLUMNS.issubset(header)):
            raise InvalidInput("CSV header is missing required columns or has duplicates.")
        total_expected = len(expected["cases"]) * expected["runs_per_case"] * len(expected["criteria"])
        if dry_run:
            print(f"DRY RUN: expectations and header valid; {total_expected} metric rows expected.")
            print("Planned checks: identities, exact counts, thresholds, finite scores, "
                  "PASSED status and numeric comparisons.")
            print("Data rows were not read or evaluated; this is not a gate verdict.")
            return 0
        body = stream.read(MAX_CSV_BYTES - len(header_bytes) + 1)
        if len(header_bytes) + len(body) > MAX_CSV_BYTES:
            raise InvalidInput("CSV exceeds the supported size limit.")
    columns = {name: header.index(name) for name in REQUIRED_COLUMNS}
    counts = Counter()
    failures = 0
    rows = 0
    cases = set(expected["cases"])
    for row in csv.reader(io.StringIO(body.decode("utf-8"), newline=""), strict=True):
        rows += 1
        if rows > MAX_ROWS:
            raise InvalidInput("CSV metric row count exceeds the supported limit.")
        if len(row) != len(header):
            raise InvalidInput("CSV has missing or extra cells.")
        record = {name: row[index] for name, index in columns.items()}
        threshold, score = numeric(record["threshold"]), numeric(record["score"])
        case, metric = record["eval_id"], record["metric_name"]
        if (record["eval_set_id"] != expected["eval_set_id"] or case not in cases
                or metric not in expected["criteria"]):
            failures += 1
            continue
        counts[case, metric] += 1
        criterion = expected["criteria"][metric]
        meets_threshold = (score >= criterion["threshold"] if criterion["comparison"] == "gte"
                           else score <= criterion["threshold"])
        if (threshold != criterion["threshold"] or record["eval_status"] != "PASSED"
                or not meets_threshold):
            failures += 1
    count_errors = sum(counts[case, metric] != expected["runs_per_case"]
                       for case in cases for metric in expected["criteria"])
    if failures or count_errors:
        print(f"FAIL: {rows} metric rows; {failures} rows failed contract checks; "
              f"{count_errors} case/metric count mismatches.")
        return 1
    print(f"PASS: all {rows} metric rows satisfy the explicit contract and exact counts.")
    return 0


def main(argv=None) -> int:
    parser = SafeParser(
        prog="check_eval_results.py", allow_abbrev=False,
        description="Read-only strict gate for ADK detailed CSV metric rows. "
        "Evidence columns and supplied identifiers/paths are never printed.",
        epilog='Expectations JSON: {"eval_set_id":"suite", "cases":["case-a"], '
        '"runs_per_case":5, "criteria":{"metric":{"threshold":0.8,"comparison":"gte"}}}. '
        "All keys shown are required; unknown keys are rejected. IDs are nonempty, "
        "unique strings (at most 256 characters); runs is a positive integer. "
        "Thresholds must be finite JSON numbers; comparison is gte or lte. "
        "Limits: CSV 10 MiB, expectations 64 KiB, one-line CSV header 16 KiB, "
        "CSV fields 64 Ki characters, metric rows 100000. Inputs must be regular "
        "UTF-8 files. Exit 0: pass (or successful dry-run); 1: failed/incomplete "
        "gate; 2: invalid input/schema. No trial-ID pairing, independence claim, "
        "or pass@k calculation is performed.",
    )
    parser.add_argument("--csv", required=True, help="ADK detailed CSV input")
    parser.add_argument("--expectations", required=True, help="Explicit JSON gate contract")
    parser.add_argument("--dry-run", action="store_true",
                        help="Validate expectations, size limits and CSV header only; "
                        "do not read or evaluate data rows, and do not report a gate pass")
    args = parser.parse_args(argv)
    try:
        return check(args.csv, expectations(args.expectations), args.dry_run)
    except InvalidInput as error:
        print(f"ERROR: {error}", file=sys.stderr)
    except (csv.Error, UnicodeError, ValueError, OverflowError):
        print("ERROR: invalid CSV encoding or structure.", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
