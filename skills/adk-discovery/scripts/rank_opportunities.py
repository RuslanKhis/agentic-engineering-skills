#!/usr/bin/env python3
"""Rank the opportunity portfolio in a discovery brief. Standard library only; reads Markdown, never runs project code.

Reads the first Markdown pipe table whose header has the columns ``ID``,
``Opportunity``, ``Value``, ``Feasibility``, ``Data``, ``Risk``, ``Fit`` and
``Measure`` (case-insensitive; ``Baseline`` is optional). Scores 1 to 5 are
the user's judgements recorded in the brief; the helper only adds them up so
the arithmetic and the ordering are not done in the model's head:

    score = value + feasibility + data - risk        (default weights 1)

``Fit`` names the technology the brief chose for the opportunity: ``agent``,
``llm``, ``ml``, ``rules``, ``process`` or ``unclear``. ``Measure`` is the
outcome metric the first use case would be judged on; ``Baseline`` says
whether that metric has a known starting value.

Reports the ranked portfolio, then findings. Exit status: 0 when every row is
valid and the chosen first candidate has a measure and a technology fit, 1
when a row is invalid or the first candidate is not ready to hand to design,
2 when the input cannot be read.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys

REQUIRED = ("id", "opportunity", "value", "feasibility", "data", "risk", "fit", "measure")
OPTIONAL = ("baseline",)
FITS = ("agent", "llm", "ml", "rules", "process", "unclear")
SCORED = ("value", "feasibility", "data", "risk")
NO_VALUE = {"", "-", "n/a", "none", "tbd", "unknown", "?"}
ROW = re.compile(r"^\s*\|.*\|\s*$")
SEPARATOR = re.compile(r"^\s*\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)*\|?\s*$")


class InputError(Exception):
    pass


def split_row(line: str) -> list[str]:
    cells = line.strip().strip("|").split("|")
    return [cell.strip().strip("`*").strip() for cell in cells]


def normalise(header: str) -> str:
    """Map a header cell to its canonical column name, or '' when unknown."""
    key = header.lower()
    for name in REQUIRED + OPTIONAL:
        if key == name or key.startswith(name + " ") or key.startswith(name + "/"):
            return name
    if key.startswith("data"):
        return "data"
    if key.startswith("tech") or key.startswith("fit"):
        return "fit"
    if key.startswith("outcome") or key.startswith("metric"):
        return "measure"
    return ""


def find_table(text: str) -> tuple[dict[str, int], list[tuple[int, list[str]]]]:
    lines = text.splitlines()
    index = 0
    while index < len(lines) - 1:
        if ROW.match(lines[index]) and SEPARATOR.match(lines[index + 1]):
            columns = {}
            for position, cell in enumerate(split_row(lines[index])):
                name = normalise(cell)
                if name and name not in columns:
                    columns[name] = position
            if all(name in columns for name in REQUIRED):
                rows = []
                cursor = index + 2
                while cursor < len(lines) and ROW.match(lines[cursor]):
                    rows.append((cursor + 1, split_row(lines[cursor])))
                    cursor += 1
                return columns, rows
        index += 1
    raise InputError("no opportunity table found; the header needs the columns "
                     + ", ".join(name.capitalize() for name in REQUIRED))


def cell(row: list[str], columns: dict[str, int], name: str) -> str:
    position = columns.get(name)
    if position is None or position >= len(row):
        return ""
    return row[position]


def parse_rows(columns, rows, weights):
    opportunities, errors = [], []
    seen = set()
    for line_number, row in rows:
        where = f"line {line_number}"
        identifier = cell(row, columns, "id")
        if not identifier:
            errors.append(f"{where}: row has no ID")
            continue
        if identifier in seen:
            errors.append(f"{where}: duplicate ID {identifier}")
            continue
        seen.add(identifier)
        entry = {"id": identifier, "opportunity": cell(row, columns, "opportunity")}
        valid = True
        for name in SCORED:
            raw = cell(row, columns, name)
            try:
                number = int(raw)
            except ValueError:
                errors.append(f"{where} ({identifier}): {name} must be a whole number 1-5, got {raw!r}")
                valid = False
                continue
            if not 1 <= number <= 5:
                errors.append(f"{where} ({identifier}): {name} must be 1-5, got {number}")
                valid = False
            entry[name] = number
        fit = cell(row, columns, "fit").lower()
        if fit not in FITS:
            errors.append(f"{where} ({identifier}): fit must be one of {', '.join(FITS)}, got {fit!r}")
            valid = False
        entry["fit"] = fit
        measure = cell(row, columns, "measure")
        entry["measure"] = "" if measure.lower() in NO_VALUE else measure
        baseline = cell(row, columns, "baseline")
        entry["baseline"] = "" if baseline.lower() in NO_VALUE else baseline
        if valid:
            entry["score"] = (weights["value"] * entry["value"] + weights["feasibility"] * entry["feasibility"]
                              + weights["data"] * entry["data"] - weights["risk"] * entry["risk"])
        opportunities.append(entry)
    return opportunities, errors


def rank(opportunities):
    scored = [entry for entry in opportunities if "score" in entry]
    scored.sort(key=lambda entry: (-entry["score"], entry["risk"], -entry["value"], entry["id"]))
    for position, entry in enumerate(scored, start=1):
        entry["rank"] = position
    return scored


def review_first(first, opportunities):
    """Findings about the candidate that would go to design next."""
    blocking, warnings = [], []
    if first is None:
        return ["no valid opportunity to hand to design"], warnings
    if not first["measure"]:
        blocking.append(f"{first['id']}: no outcome measure; design cannot set a success target without one")
    if first["fit"] == "unclear":
        blocking.append(f"{first['id']}: technology fit is unclear; settle agent, llm, ml, rules or process first")
    if first["fit"] == "process":
        warnings.append(f"{first['id']}: fit is a process change, not software; adk-system-designer is not the next step")
    if not first["baseline"]:
        warnings.append(f"{first['id']}: baseline unknown; the first goal is to measure the current journey")
    if first["risk"] >= 4:
        warnings.append(f"{first['id']}: risk {first['risk']} of 5 for a first use case; prefer a lower-risk start or a human before every effect")
    if first["data"] <= 2:
        warnings.append(f"{first['id']}: data readiness {first['data']} of 5; expect a data-access discovery goal before any build")
    for entry in opportunities:
        if "score" in entry and entry is not first and entry["score"] == first["score"]:
            warnings.append(f"{entry['id']} ties with {first['id']} on score {first['score']}; the brief should say why one goes first")
    return blocking, warnings


def parse_weights(text):
    weights = {name: 1 for name in SCORED}
    if not text:
        return weights
    for item in text.split(","):
        if "=" not in item:
            raise InputError(f"weights must look like value=2,risk=1; got {item!r}")
        name, _, value = item.partition("=")
        name = name.strip().lower()
        if name not in weights:
            raise InputError(f"unknown weight {name!r}; use {', '.join(SCORED)}")
        try:
            weights[name] = float(value)
        except ValueError as exc:
            raise InputError(f"weight {name} must be a number") from exc
    return weights


def format_table(ranked):
    header = ["Rank", "ID", "Score", "Value", "Feas.", "Data", "Risk", "Fit", "Measure", "Opportunity"]
    lines = [" | ".join(header)]
    for entry in ranked:
        lines.append(" | ".join(str(part) for part in (
            entry["rank"], entry["id"], entry["score"], entry["value"], entry["feasibility"], entry["data"],
            entry["risk"], entry["fit"], entry["measure"] or "(none)", entry["opportunity"])))
    return "\n".join(lines)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--brief", type=Path, required=True, help="discovery brief Markdown file")
    parser.add_argument("--pick", help="ID of the opportunity chosen as the first use case (default: rank 1)")
    parser.add_argument("--weights", help="comma-separated weights, e.g. value=2,risk=1.5")
    parser.add_argument("--json", action="store_true", help="print a JSON report instead of text")
    args = parser.parse_args(argv)
    try:
        text = args.brief.read_text(encoding="utf-8")
        weights = parse_weights(args.weights)
        columns, rows = find_table(text)
        opportunities, errors = parse_rows(columns, rows, weights)
    except (OSError, UnicodeError) as exc:
        print(f"ERROR cannot read brief: {exc}", file=sys.stderr)
        return 2
    except InputError as exc:
        print(f"ERROR {exc}", file=sys.stderr)
        return 2
    ranked = rank(opportunities)
    first = None
    if args.pick:
        first = next((entry for entry in ranked if entry["id"] == args.pick), None)
        if first is None:
            errors.append(f"--pick {args.pick}: no valid opportunity with that ID")
    elif ranked:
        first = ranked[0]
    blocking, warnings = review_first(first, opportunities)
    if first is not None and args.pick and first["rank"] != 1:
        warnings.append(f"{first['id']} is ranked {first['rank']}, not 1; the brief should record why it goes first")
    report = {"weights": weights, "ranked": ranked, "first": first["id"] if first else None,
              "errors": errors, "blocking": blocking, "warnings": warnings}
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        if ranked:
            print(format_table(ranked))
        if first:
            print(f"\nFirst use case: {first['id']} ({first['opportunity']})")
        for message in errors:
            print(f"ERROR {message}")
        for message in blocking:
            print(f"BLOCKING {message}")
        for message in warnings:
            print(f"WARNING {message}")
        if not errors and not blocking:
            print("Ready for adk-system-designer: the first use case has a measure and a technology fit."
                  if first else "Nothing to hand over.")
    return 1 if errors or blocking else 0


if __name__ == "__main__":
    raise SystemExit(main())
