#!/usr/bin/env python3
"""Check a statement of work against the plan it was written from. Standard library only; reads Markdown.

Reads the SOW's deliverables, acceptance-criteria, client-dependency and
effort tables (the headers of the designer's SOW template) and the plan's
fenced ``yaml`` schedule block through ``check_schedule.py`` in this directory,
so both checks read hours the same way. It reports a problem when:

- a deliverable cites no plan goal, cites a goal the plan lacks, shares a goal
  with another deliverable, or cites an acceptance criterion the SOW lacks;
- a goal in a priced phase (a phase row of the effort table) belongs to no
  deliverable;
- a phase's hours, or the total, differ from the schedule block's totals;
- fees are not hours times the stated hourly rate, or fees appear without a rate;
- a client dependency lacks an owner or a date (``YYYY-MM-DD`` or
  ``<n> working days after <event>``);
- an acceptance criterion lacks a numeric threshold with a comparator
  (``>= 85%``, ``0 of 25``, ``p95 <= 8 s``), a case count, a method or a date,
  or no deliverable cites it;
- a cell still holds a template placeholder such as ``<date>``.

With ``--design`` the contract IDs in acceptance criteria must exist in the
design's contracts table. With ``--change`` a change request must cite the
contracts, goals and estimate change it makes; its goal IDs must exist in the
plan or be marked new. Exit status: 0 consistent, 1 problems found, 2 input
cannot be read.
"""

import argparse
from datetime import date
import importlib.util
import json
from pathlib import Path
import re
import sys


def _load_schedule():
    path = Path(__file__).resolve().with_name("check_schedule.py")
    spec = importlib.util.spec_from_file_location("designer_check_schedule", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


schedule = _load_schedule()
InputError = schedule.InputError

FENCE = re.compile(r"^```.*?^```\s*$", re.MULTILINE | re.DOTALL)
TOKEN = re.compile(r"(?<![\w/-])([A-Z]{1,3})(\d+)(?:\s*[-–—]\s*(?:\1)?(\d+))?(?![\w/-])")
PLACEHOLDER = re.compile(r"<[A-Za-z][^<>|]*>")
ISO_DATE = re.compile(r"\b(\d{4})-(\d{2})-(\d{2})\b")
RELATIVE_DATE = re.compile(r"\b\d+\s+(?:working\s+|business\s+|calendar\s+)?days?\s+(?:after|from|before)\s+\S+",
                           re.IGNORECASE)
COMPARATOR = re.compile(r"[≥≤<>=]|\bat (?:least|most)\b|\bno (?:more|fewer|less) than\b|\bwithin\b"
                        r"|\bminimum\b|\bmaximum\b|\b\d+(?:\.\d+)?\s+(?:of|out of|in)\s+\d+\b|^\s*0\s+[a-z]",
                        re.IGNORECASE)
MONEY = re.compile(r"(\d[\d,]*(?:\.\d+)?)")
NO_RATE = re.compile(r"to be supplied|\btbc\b|\btbd\b|not supplied|^\s*$|^\s*-\s*$", re.IGNORECASE)


def strip_fences(text):
    return FENCE.sub("", text)


def tables(text):
    """Return (lower-case header cells, rows of cells) for every pipe table outside code fences."""
    found, current = [], None
    for raw in strip_fences(text).splitlines():
        line = raw.strip()
        if not line.startswith("|"):
            current = None
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if current is None:
            current = ([re.sub(r"[`*]", "", c).strip().lower() for c in cells], [])
            found.append(current)
            continue
        if set("".join(cells)) <= set("-: "):
            continue
        current[1].append(cells)
    return found


def find_table(text, required, label):
    for header, rows in tables(text):
        if all(any(cell == key or cell.startswith(key) for cell in header) for key in required):
            return header, rows
    raise InputError(f"no {label} table (a table whose header has: {', '.join(required)})")


def column(header, row, key):
    for index, name in enumerate(header):
        if (name == key or name.startswith(key)) and index < len(row):
            return row[index]
    return ""


def ids_in(cell, prefix=None):
    """IDs named in a cell, expanding ranges such as G01-G04 or G01–G04 with the first ID's zero padding."""
    found = []
    for match in TOKEN.finditer(cell):
        letters, first, last = match.group(1), match.group(2), match.group(3)
        if prefix and letters != prefix:
            continue
        if last is None:
            found.append(letters + first)
            continue
        width = len(first)
        for number in range(int(first), int(last) + 1):
            found.append(f"{letters}{number:0{width}d}")
    return found


def goal_ids_in(cell, known):
    """Plan goal IDs in a cell: known IDs and anything shaped like a goal ID, ranges expanded."""
    found = []
    for match in TOKEN.finditer(cell):
        letters, first, last = match.group(1), match.group(2), match.group(3)
        if letters in ("AC", "DL", "CD", "CR", "C", "D", "R", "SB", "M", "I"):
            continue
        if last is None:
            found.append(letters + first)
        else:
            found.extend(f"{letters}{n:0{len(first)}d}" for n in range(int(first), int(last) + 1))
    for name in known:
        if name not in found and re.search(rf"(?<![\w-]){re.escape(name)}(?![\w-])", cell):
            found.append(name)
    return found


def money_range(cell):
    numbers = [float(n.replace(",", "")) for n in MONEY.findall(cell)]
    if not numbers:
        return None
    return (numbers[0], numbers[1] if len(numbers) > 1 else numbers[0])


def valid_date(cell):
    for match in ISO_DATE.finditer(cell):
        try:
            date(int(match.group(1)), int(match.group(2)), int(match.group(3)))
            return True
        except ValueError:
            return False
    return bool(RELATIVE_DATE.search(cell))


def same_phase(goal_phase, phase):
    phase = phase.strip().lower().removeprefix("phase").strip()
    return goal_phase.strip().lower().removeprefix("phase").strip() == phase


def close(a, b, money=False):
    """Hours must match to the hundredth; money to one currency unit or 0.1 percent."""
    return abs(a - b) <= (max(1.0, 0.001 * max(abs(a), abs(b))) if money else 0.01)


def design_contracts(path):
    contracts = set()
    for header, rows in tables(path.read_text(encoding="utf-8")):
        if any("invariant" in h for h in header):
            contracts.update(row[0].strip() for row in rows if re.fullmatch(r"C\d+", row[0].strip()))
    if not contracts:
        raise InputError(f"{path}: no contracts table (a table with an Invariant column and C1, C2 rows)")
    return contracts


def placeholders(label, rows):
    return [f"{label} {row[0] or '(row)'}: placeholder {m.group(0)!r} left in the table"
            for row in rows for cell in row for m in [PLACEHOLDER.search(cell)] if m]


def check_sow(sow_text, goals, contracts=None):
    by_id = {g["goal"]: g for g in goals}
    problems, notes = [], []

    dl_header, dl_rows = find_table(sow_text, ("id", "deliverable", "plan goals"), "deliverables")
    ac_header, ac_rows = find_table(sow_text, ("id", "threshold", "cases", "method"), "acceptance criteria")
    cd_header, cd_rows = find_table(sow_text, ("id", "owner", "needed by"), "client dependencies")
    ef_header, ef_rows = find_table(sow_text, ("phase", "human hours", "fees"), "effort")
    for label, rows in (("deliverable", dl_rows), ("acceptance", ac_rows), ("dependency", cd_rows),
                        ("effort", ef_rows)):
        problems += placeholders(label, rows)

    criteria = {row[0].strip(): row for row in ac_rows if row and row[0].strip()}
    owner_of, cited_criteria = {}, set()
    for row in dl_rows:
        name = row[0].strip() or "(deliverable)"
        cited = goal_ids_in(column(dl_header, row, "plan goals"), by_id)
        if not cited:
            problems.append(f"{name}: cites no plan goal; list the goal IDs it delivers")
        phases = [p.strip() for p in re.split(r"[,;/]| and ", column(dl_header, row, "phase")) if p.strip()]
        for goal in cited:
            if goal not in by_id:
                problems.append(f"{name}: {goal} is not in the plan's schedule block")
                continue
            if goal in owner_of and owner_of[goal] != name:
                problems.append(f"{goal} belongs to both {owner_of[goal]} and {name}; give it one deliverable")
            owner_of.setdefault(goal, name)
            if phases and not any(same_phase(by_id[goal]["phase"], p) for p in phases):
                problems.append(f"{name}: {goal} is in phase {by_id[goal]['phase']}, not {', '.join(phases)}")
        for criterion in ids_in(column(dl_header, row, "acceptance"), "AC"):
            cited_criteria.add(criterion)
            if criterion not in criteria:
                problems.append(f"{name}: cites {criterion}, which is not in the acceptance criteria table")

    for name, row in criteria.items():
        threshold = column(ac_header, row, "threshold")
        if not (re.search(r"\d", threshold) and COMPARATOR.search(threshold)):
            problems.append(f"{name}: threshold {threshold!r} needs a number and a comparator "
                            "(e.g. '>= 85% pass', '0 of 25', 'p95 <= 8 s'), not a judgement word")
        if not re.search(r"\d", column(ac_header, row, "cases")):
            problems.append(f"{name}: say how many cases (and who agreed them)")
        if not column(ac_header, row, "method").strip():
            problems.append(f"{name}: no method (evaluator, rubric, build, repeats)")
        if not column(ac_header, row, "measured by").strip() and any(h.startswith("measured by") for h in ac_header):
            problems.append(f"{name}: no one named to measure it")
        if not valid_date(column(ac_header, row, "date")):
            problems.append(f"{name}: no valid date (YYYY-MM-DD)")
        if name not in cited_criteria:
            problems.append(f"{name}: no deliverable cites it")
        if contracts is not None:
            for contract in ids_in(column(ac_header, row, "contracts"), "C"):
                if contract not in contracts:
                    problems.append(f"{name}: cites {contract}, which is not in the design's contracts table")

    for row in cd_rows:
        name = row[0].strip() or "(dependency)"
        owner = column(cd_header, row, "owner").strip()
        if not owner or owner.lower() in ("-", "tbc", "tbd", "none", "unknown"):
            problems.append(f"{name}: no owner; name the client role responsible")
        if not valid_date(column(cd_header, row, "needed by")):
            problems.append(f"{name}: no date; write YYYY-MM-DD or '<n> working days after <event>'")
        for goal in goal_ids_in(column(cd_header, row, "blocks"), by_id):
            if goal not in by_id:
                problems.append(f"{name}: blocks {goal}, which is not in the plan's schedule block")

    priced, fee_sum, hour_sum, total_row = [], [0.0, 0.0], [0.0, 0.0], None
    rate_given = False
    for row in ef_rows:
        phase = column(ef_header, row, "phase").strip()
        if not phase:
            continue
        hours_cell = column(ef_header, row, "human hours")
        try:
            hours = schedule.parse_range(hours_cell.replace(",", ""), f"effort row {phase}")
        except InputError as exc:
            problems.append(str(exc))
            continue
        if phase.lower().startswith("total"):
            total_row = (hours, money_range(column(ef_header, row, "fees")))
            continue
        selected = [g for g in goals if same_phase(g["phase"], phase)]
        if not selected:
            problems.append(f"effort phase {phase}: the plan has no goals in this phase")
            continue
        planned = schedule.analyse(goals, phase.lower().removeprefix("phase").strip(), None, None, None, 6.0)
        expected = planned["total_hours"]
        priced.append(phase)
        if hours is None or not (close(hours[0], expected[0]) and close(hours[1], expected[1])):
            problems.append(f"effort phase {phase}: {hours_cell!r} differs from the schedule block's "
                            f"{schedule.fmt(expected)} h")
        hour_sum = [hour_sum[0] + expected[0], hour_sum[1] + expected[1]]
        rate_cell = column(ef_header, row, "rate")
        fees = money_range(column(ef_header, row, "fees"))
        rate = money_range(rate_cell) if not NO_RATE.search(rate_cell) else None
        if rate is None:
            if fees is not None:
                problems.append(f"effort phase {phase}: fees given without an hourly rate; the rate comes from "
                                "the user, never assumed")
            else:
                notes.append(f"phase {phase}: rate not supplied; fees left open")
            continue
        rate_given = True
        want = (expected[0] * rate[0], expected[1] * rate[0])
        if fees is None or not (close(fees[0], want[0], True) and close(fees[1], want[1], True)):
            problems.append(f"effort phase {phase}: fees should be {want[0]:,.0f}-{want[1]:,.0f} "
                            f"({schedule.fmt(expected)} h x {rate[0]:g} per hour)")
        else:
            fee_sum = [fee_sum[0] + fees[0], fee_sum[1] + fees[1]]
    if not priced:
        problems.append("effort table has no phase rows that match the plan")
    if total_row is not None:
        hours, fees = total_row
        if hours is None or not (close(hours[0], hour_sum[0]) and close(hours[1], hour_sum[1])):
            problems.append(f"effort total {schedule.fmt(hours) if hours else '?'} h differs from the priced "
                            f"phases' {schedule.fmt(tuple(hour_sum))} h in the schedule block")
        if rate_given and fees is not None and not (close(fees[0], fee_sum[0], True)
                                                    and close(fees[1], fee_sum[1], True)):
            problems.append(f"effort total fees should be {fee_sum[0]:,.0f}-{fee_sum[1]:,.0f}")
    elif len(priced) > 1:
        problems.append("effort table has several phases but no Total row")

    for goal in goals:
        if any(same_phase(goal["phase"], p) for p in priced) and goal["goal"] not in owner_of \
                and goal["total"][1] > 0:
            problems.append(f"{goal['goal']} (phase {goal['phase']}, {schedule.fmt(goal['total'])} h) belongs to no "
                            "deliverable; add it to one or take its phase out of the price")

    summary = {"deliverables": len(dl_rows), "acceptance_criteria": len(criteria), "dependencies": len(cd_rows),
               "priced_phases": priced, "plan_hours": tuple(hour_sum)}
    return problems, notes, summary


def check_change(text, goals, contracts=None):
    by_id = {g["goal"]: g for g in goals}
    problems = []
    header, rows = find_table(text, ("kind", "ids", "change"), "changes by ID")
    kinds = {column(header, row, "kind").strip().lower(): row for row in rows}
    problems += placeholders("change", rows)
    for needed in ("contracts", "goals"):
        row = next((r for k, r in kinds.items() if k.startswith(needed)), None)
        if row is None:
            problems.append(f"change request: no {needed} row; cite the IDs it changes or write none")
            continue
        cell = column(header, row, "ids")
        if not cell.strip():
            problems.append(f"change request: the {needed} row is empty; cite IDs or write none")
    goal_row = next((r for k, r in kinds.items() if k.startswith("goals")), None)
    if goal_row is not None:
        cell = column(header, goal_row, "ids")
        for part in re.split(r",|;", cell):
            for goal in goal_ids_in(part, by_id):
                if goal not in by_id and "new" not in part.lower():
                    problems.append(f"change request: {goal} is not in the plan; update the plan first or mark it new")
    contract_row = next((r for k, r in kinds.items() if k.startswith("contracts")), None)
    if contract_row is not None and contracts is not None:
        for part in re.split(r",|;", column(header, contract_row, "ids")):
            for contract in ids_in(part, "C"):
                if contract not in contracts and "new" not in part.lower():
                    problems.append(f"change request: {contract} is not in the design; revise the design first "
                                    "or mark it new")
    try:
        est_header, est_rows = find_table(text, ("before", "after"), "estimate change")
    except InputError as exc:
        return problems + [f"change request: {exc}"]
    hours_row = next((r for r in est_rows if r and r[0].strip().lower().startswith("human hours")), None)
    if hours_row is None:
        problems.append("change request: the estimate table has no Human hours row")
    else:
        try:
            before = schedule.parse_range(column(est_header, hours_row, "before"), "change before")
            after = schedule.parse_range(column(est_header, hours_row, "after"), "change after")
        except InputError as exc:
            problems.append(f"change request: {exc}")
        else:
            if before is None or after is None:
                problems.append("change request: give the hours before and after from the schedule check")
    return problems


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--sow", type=Path, help="statement of work Markdown from the SOW template")
    parser.add_argument("--plan", type=Path, required=True, help="plan Markdown with the fenced yaml schedule block")
    parser.add_argument("--design", type=Path, help="design Markdown whose contracts table acceptance cites")
    parser.add_argument("--change", type=Path, action="append", default=[], help="change request Markdown; repeat")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    try:
        if not args.sow and not args.change:
            raise InputError("give --sow, --change or both")
        goals = schedule.read_plan(args.plan)
        contracts = design_contracts(args.design) if args.design else None
        result = {"problems": [], "notes": []}
        if args.sow:
            problems, notes, summary = check_sow(args.sow.read_text(encoding="utf-8"), goals, contracts)
            result.update(summary)
            result["problems"] += problems
            result["notes"] += notes
        for path in args.change:
            result["problems"] += [f"{path.name}: {p}" for p in
                                   check_change(path.read_text(encoding="utf-8"), goals, contracts)]
    except (InputError, OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps(result, indent=1))
    else:
        if "deliverables" in result:
            print(f"SOW: {result['deliverables']} deliverables, {result['acceptance_criteria']} acceptance criteria, "
                  f"{result['dependencies']} client dependencies; priced phases "
                  f"{', '.join(result['priced_phases']) or 'none'}, {schedule.fmt(result['plan_hours'])} h in the plan")
        for note in result["notes"]:
            print(f"NOTE: {note}")
        for problem in result["problems"]:
            print(f"PROBLEM: {problem}")
        if not result["problems"]:
            print("Consistent with the plan. This checks the arithmetic and references, not the estimates or terms.")
    return 1 if result["problems"] else 0


if __name__ == "__main__":
    sys.exit(main())
