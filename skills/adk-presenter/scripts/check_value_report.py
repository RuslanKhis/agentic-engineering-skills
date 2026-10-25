#!/usr/bin/env python3
"""Check a monthly value report against the plan's measurement and incident records. Standard library only.

The report format is ``assets/value-report-template.md``: front matter with
``stage: value-report``, ``period``, ``decider`` and ``call`` (stop, continue
or scale), then the sections Outcome, Counter-metric, Adoption, Cost per
outcome, Incidents, Thresholds and Call. The plan (and any ticket files given
with it) holds the records the report cites, one per line or as table rows:

    - M3: metric resolved claims per week; value 412; baseline 388 (brief §4, Q2 2026);
      window 2026-09-01 to 2026-09-30; sample all claims; method claims system export; owner ops lead; build v1.4.2
    - I2: date 2026-09-14; severity 2; effect 31 replies quoted a withdrawn clause; response paused auto-send; fix C4 test

Wrapped bullets and paragraphs are read as one logical line. Fields are separated by semicolons; ``key: value`` and ``key value`` both work.
Windows and dates are ISO (2026-09-01, or 2026-09 for a month). A record
with ``kind baseline`` is a baseline measurement and is exempt from the
window check, as is an assumption record: one whose method or kind says
assumed, assumption, estimated, projected, extrapolated, modelled or
forecast, which is not a measurement. A report line is in the measured voice unless it opens
with Estimate, Target, Threshold, Assumption or Projected, says "we
estimate", or sits in the Thresholds section.

The checker reports:

- a figure (percentage, money, count, duration) on a line that cites no M or
  I record; a line in the estimate, target or threshold voice may cite a
  plan ID (C, D, G, R) or a file path (the brief) instead;
- a cited M or I ID the plan does not hold;
- a missing baseline: an M record cited under Outcome or Counter-metric with
  no baseline (a warning on a counter-metric line that says "no baseline"), an Outcome section that cites no M record, and with
  ``--brief`` a discovery brief whose Baseline field is unknown;
- a measurement window that ends before the report period starts (or that
  is missing), so last month's figure is not reported as this month's; a
  line that says "last period" or "previous month" may cite one as context;
- a figure derived from an assumption presented as measured, and stacked
  assumptions: one line resting on two or more assumption records;
- a cost per outcome that does not cite both its numerator (a cost record)
  and its denominator (an outcome-count record);
- an incident dated inside the period that the report does not cite, and a
  scale call while a severity 1 or 2 incident record is not ``status closed``;
- missing sections, period, decider or call.

Exit status: 0 clean (warnings allowed), 1 when any error is found, 2 when a
file cannot be read or the report has no front matter.
"""

from __future__ import annotations

import argparse
from datetime import date, timedelta
import json
from pathlib import Path
import re
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from check_deck import IDENTIFIER, NUMERIC_CLAIM, InputError, parse_front_matter  # noqa: E402

SECTIONS = {   # matched in this order, so "Cost per outcome" is the cost section, not the outcome
    "counter-metric": re.compile(r"counter[- ]?metric", re.IGNORECASE),
    "cost": re.compile(r"\bcost\b", re.IGNORECASE),
    "adoption": re.compile(r"\badoption\b", re.IGNORECASE),
    "incidents": re.compile(r"\bincidents?\b", re.IGNORECASE),
    "thresholds": re.compile(r"\bthresholds?\b", re.IGNORECASE),
    "call": re.compile(r"\bcall\b|\bdecision\b", re.IGNORECASE),
    "outcome": re.compile(r"\boutcome\b", re.IGNORECASE),
}
CALLS = ("stop", "continue", "scale")
RECORD_LINE = re.compile(r"^\s*(?:[-*]\s+)?(?:\*\*)?\b([MI]\d+)\b(?:\*\*)?\s*(?::|—|–|-)\s*(.+)$")
RECORD_ID = re.compile(r"(?<![\w/-])([MI]\d+)(?![\w/-])")
PLAN_ID = re.compile(r"(?<![\w/-])(?:G\d+(?:/A\d+)?|[CDR]\d+)(?![\w/-])")
PATH_OR_URL = re.compile(r"https?://\S+|\S+\.(?:md|json|csv|txt|yaml|yml)\b")
KEYS = ("metric", "kind", "value", "baseline", "window", "sample", "method", "owner", "build", "source",
        "date", "severity", "effect", "response", "fix", "status")
ASSUMED = re.compile(r"\b(?:assum\w*|estimated|estimation|projected|projection|extrapolat\w*|modell?ed|forecast\w*)\b",
                     re.IGNORECASE)
NO_VALUE = re.compile(r"^\s*(?:|-|—|none|unknown|n/?a|tbd|tbc|not (?:yet )?measured|pending)\s*\.?\s*$",
                      re.IGNORECASE)
COST_WORDS = re.compile(r"\b(?:cost|spend|bill\w*|invoice|tokens?)\b|[$€£]", re.IGNORECASE)
COST_PER = re.compile(r"\bcost per\b|[$€£]\s?\d[\d,.]*\s*(?:per|/|a|an|each)\s+(?!(?:month|week|day|year|hour)s?\b)\w",
                      re.IGNORECASE)
NON_MEASURED_VOICE = re.compile(r"^(?:we estimate|estimated?|estimates|target|threshold|assumption|assumed"
                                r"|projected|projection)\b", re.IGNORECASE)
LAST_PERIOD = re.compile(r"\b(?:last|previous|prior) (?:period|month)\b", re.IGNORECASE)
NO_BASELINE_STATED = re.compile(r"\bno baseline\b|\bbaseline (?:not (?:yet )?measured|unknown)\b", re.IGNORECASE)
ISO_DATE = re.compile(r"\b(\d{4})-(\d{2})(?:-(\d{2}))?\b")


def month_end(year: int, month: int) -> date:
    following = date(year + (month == 12), month % 12 + 1, 1)
    return following - timedelta(days=1)


def dates_in(text: str) -> list[tuple[date, date]]:
    """Each ISO date or year-month in the text as a (first day, last day) span."""
    spans = []
    for year, month, day in ISO_DATE.findall(text):
        try:
            if day:
                single = date(int(year), int(month), int(day))
                spans.append((single, single))
            else:
                spans.append((date(int(year), int(month), 1), month_end(int(year), int(month))))
        except ValueError:
            continue
    return spans


def span_of(text: str) -> tuple[date, date] | None:
    spans = dates_in(text)
    if not spans:
        return None
    return min(start for start, _ in spans), max(end for _, end in spans)


def parse_fields(rest: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    for position, segment in enumerate(part.strip() for part in rest.split(";")):
        if not segment:
            continue
        match = re.match(r"^(?:\*\*)?([A-Za-z]+)(?:\*\*)?\s*(?::\s*|\s+)(.*)$", segment)
        key = match.group(1).lower() if match else ""
        if key in KEYS:
            fields[key] = match.group(2).strip()
        elif position == 0:
            fields.setdefault("metric", segment)
        else:
            fields["note"] = (fields.get("note", "") + " " + segment).strip()
    return fields


def parse_records(text: str, source: str) -> dict[str, dict]:
    """M and I records from list lines (with continuation lines) and from tables whose first column is the ID."""
    records: dict[str, dict] = {}
    header: list[str] | None = None
    current: str | None = None
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("|"):
            current = None
            cells = [cell.strip().strip("*") for cell in stripped.strip("|").split("|")]
            if all(re.fullmatch(r":?-{2,}:?", cell) for cell in cells if cell):
                continue
            if cells and RECORD_ID.fullmatch(cells[0]) and header:
                fields = {name: value for name, value in zip(header[1:], cells[1:]) if name in KEYS}
                records[cells[0]] = dict(fields, id=cells[0], source=source, line=stripped)
            elif cells and not RECORD_ID.fullmatch(cells[0]):
                header = [cell.lower() for cell in cells]
            continue
        header = None
        match = RECORD_LINE.match(line)
        if match:
            current = match.group(1)
            records[current] = dict(parse_fields(match.group(2)), id=current, source=source, line=stripped)
            continue
        if current and stripped and line[:1].isspace() and not re.match(r"^\s*[-*]\s", line):
            merged = records[current]["line"] + " " + stripped
            records[current] = dict(parse_fields(RECORD_LINE.match(merged).group(2)), id=current,
                                    source=source, line=merged)
            continue
        current = None
    return records


def is_assumption(record: dict) -> bool:
    return any(ASSUMED.search(record.get(key, "")) for key in ("method", "kind"))


def opening_words(line: str) -> str:
    """The line without list markers, table pipes or emphasis, to read the voice it opens with."""
    return re.sub(r"^[\s|*_>-]+", "", line).lstrip("*_ ")


def is_baseline_record(record: dict) -> bool:
    return "baseline" in record.get("kind", "").lower()


def is_cost_record(record: dict) -> bool:
    return bool(COST_WORDS.search(record.get("metric", "") + " " + record.get("value", "")))


def split_sections(body: str) -> list[tuple[str, int, list[tuple[int, str]]]]:
    sections, title, start, lines, in_fence = [], "", 0, [], False
    for number, line in enumerate(body.splitlines(), start=1):
        if line.strip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        heading = re.match(r"^\s*#{1,3}\s+(.+?)\s*$", line)
        if heading:
            sections.append((title, start, lines))
            title, start, lines = heading.group(1), number, []
            continue
        starts_item = bool(re.match(r"^\s*(?:[-*+]\s|\d+[.)]\s|\|)", line))
        if (line.strip() and not starts_item and lines and lines[-1][1].strip()
                and not lines[-1][1].lstrip().startswith("|")):
            # a wrapped bullet or paragraph: one logical line, numbered from its first physical line
            lines[-1] = (lines[-1][0], lines[-1][1].rstrip() + " " + line.strip())
            continue
        lines.append((number, line))
    sections.append((title, start, lines))
    return sections


def section_kind(title: str) -> str | None:
    for kind, pattern in SECTIONS.items():
        if pattern.search(title):
            return kind
    return None


def check_report(report_text: str, plan_texts: list[tuple[str, str]], brief_text: str | None = None) -> dict:
    meta, body = parse_front_matter(report_text)
    all_lines = report_text.splitlines()
    offset = next(index for index in range(1, len(all_lines)) if all_lines[index].strip() == "---") + 1
    errors, warnings = [], []
    records: dict[str, dict] = {}
    for name, text in plan_texts:
        for record_id, record in parse_records(text, name).items():
            if record_id in records and records[record_id]["line"] != record["line"]:
                warnings.append(f"{record_id} is defined twice ({records[record_id]['source']} and {name}); "
                                f"the later one is used")
            records[record_id] = record
    if meta.get("stage") != "value-report":
        errors.append(f"front matter: stage must be value-report, got {meta.get('stage')!r}")
    period = span_of(meta.get("period", ""))
    if period is None:
        errors.append("front matter: period must name the month (2026-09) or a date range (2026-09-01 to 2026-09-30)")
    if not meta.get("decider"):
        errors.append("front matter: no decider; name the one person who makes the stop, continue or scale call")
    call = meta.get("call", "").lower().strip()
    if call not in CALLS:
        errors.append(f"front matter: call must be one of {', '.join(CALLS)}, got {meta.get('call')!r}")
    if not meta.get("date"):
        warnings.append("front matter: no date for the decision")
    sections = split_sections(body)
    present = {section_kind(title) for title, _, _ in sections if title}
    for kind in SECTIONS:
        if kind not in present:
            errors.append(f"sections: no {kind} section")
    cited_all: set[str] = set()
    current_ids: set[str] = set()   # cited at least once as this period's figure
    for title, _, lines in sections:
        kind = section_kind(title) if title else None
        section_ids: set[str] = set()
        section_text = " ".join(line for _, line in lines)
        for number, line in lines:
            where = f"line {number + offset}"
            stripped = line.strip()
            if not stripped:
                continue
            ids = set(RECORD_ID.findall(stripped))
            section_ids |= ids
            cited_all |= ids
            if not LAST_PERIOD.search(stripped):
                current_ids |= ids
            for record_id in sorted(ids):
                if record_id not in records:
                    errors.append(f"{where}: cites {record_id}, which the plan does not hold")
            figures = [m.group(0).strip() for m in NUMERIC_CLAIM.finditer(IDENTIFIER.sub("", stripped))]
            non_measured = (kind == "thresholds" or bool(NON_MEASURED_VOICE.match(opening_words(stripped)))
                            or bool(re.search(r"\bwe estimate\b", stripped, re.IGNORECASE)))
            if figures and not ids:
                if not (non_measured and (PLAN_ID.search(stripped) or PATH_OR_URL.search(stripped))):
                    errors.append(f"{where}: figure without an M or I citation: {', '.join(figures[:3])}"
                                  + ("" if not non_measured else "; an estimate, target or threshold cites a plan "
                                     "ID or file path")
                                  + ("" if non_measured or not (PLAN_ID.search(stripped) or PATH_OR_URL.search(stripped))
                                     else "; a plan ID or path is enough only on a line that opens with Estimate, "
                                     "Target or Threshold"))
            known = [records[record_id] for record_id in sorted(ids) if record_id in records]
            assumed = [record for record in known if record["id"].startswith("M") and is_assumption(record)]
            stacks = len(assumed) + (1 if re.search(r"\bassuming\b", stripped, re.IGNORECASE) else 0)
            if assumed and not non_measured:
                errors.append(f"{where}: figure rests on an assumption ({', '.join(r['id'] for r in assumed)}) "
                              f"but reads as measured; say 'we estimate' or cite a measurement")
            if stacks >= 2:
                errors.append(f"{where}: stacked assumptions ({stacks}); a figure may rest on one stated assumption")
            if COST_PER.search(stripped) and figures and not non_measured:
                measured = [record for record in known if record["id"].startswith("M")]
                cost = [record for record in measured if is_cost_record(record)]
                count = [record for record in measured if not is_cost_record(record)]
                if not cost or not count:
                    errors.append(f"{where}: cost per outcome must cite its numerator (a cost record) and its "
                                  f"denominator (an outcome-count record); found "
                                  f"{', '.join(r['id'] for r in measured) or 'none'}")
        if kind in ("outcome", "counter-metric"):
            measured_ids = sorted(record_id for record_id in section_ids if record_id.startswith("M"))
            if not measured_ids and not re.search(r"not\s+(?:yet\s+)?measured", section_text, re.IGNORECASE):
                errors.append(f"{kind}: cites no M record; report the measurement or write 'not measured' "
                              f"and the goal that will measure it")
            for record_id in measured_ids:
                record = records.get(record_id)
                if record and not is_baseline_record(record) and NO_VALUE.match(record.get("baseline", "")):
                    stated = any(record_id in line and NO_BASELINE_STATED.search(line) for _, line in lines)
                    if kind == "counter-metric" and stated:
                        warnings.append(f"counter-metric: {record_id} has no baseline, as the report says; "
                                        f"the plan needs the goal that measures one")
                    else:
                        errors.append(f"{kind}: {record_id} has no baseline; the figure cannot be read against "
                                      f"the brief's baseline"
                                      + ("" if kind == "outcome" else "; on the counter-metric, say 'no baseline' "
                                         "on the line that cites it"))
        if kind == "adoption" and not re.search(r"\bactive\b", section_text, re.IGNORECASE):
            warnings.append("adoption: state the definition of an active user")
    for record_id in sorted(current_ids):
        record = records.get(record_id)
        if (not record or not record_id.startswith("M") or is_baseline_record(record) or is_assumption(record)
                or period is None):
            continue
        window = span_of(record.get("window", ""))
        if window is None:
            errors.append(f"{record_id}: no measurement window with dates; the report cannot show which month it covers")
        elif window[1] < period[0]:
            errors.append(f"{record_id}: window ends {window[1].isoformat()}, before the report period starts "
                          f"{period[0].isoformat()}; measure this period, or put 'last period' on the line that cites it")
        elif window[0] > period[1]:
            warnings.append(f"{record_id}: window starts {window[0].isoformat()}, after the report period")
    if period is not None:
        for record_id, record in sorted(records.items()):
            if not record_id.startswith("I"):
                continue
            when = span_of(record.get("date", "") or record["line"])
            if when and period[0] <= when[0] <= period[1] and record_id not in cited_all:
                errors.append(f"incidents: {record_id} ({when[0].isoformat()}) falls in the period but is not reported")
    if call == "scale":
        for record_id, record in sorted(records.items()):
            if not record_id.startswith("I"):
                continue
            severity = re.search(r"\d", record.get("severity", ""))
            status = record.get("status", "").lower()
            if severity and severity.group(0) in "12" and "closed" not in status:
                errors.append(f"call: scale with {record_id} (severity {severity.group(0)}) "
                              f"{'open' if status else 'without a status'}; close it or record why scale proceeds")
    if brief_text is not None:
        baseline = re.search(r"\*\*Baseline:\*\*\s*(.*)", brief_text)
        if baseline is None:
            errors.append("brief: no Baseline field")
        elif re.search(r"\bunknown\b|<value", baseline.group(1), re.IGNORECASE) or not baseline.group(1).strip():
            errors.append(f"brief: baseline is not recorded ({baseline.group(1).strip()[:80]!r}); the outcome "
                          f"cannot be reported against it until a baseline M record exists")
        if not re.search(r"\*\*Threshold sentences:\*\*\s*\S", brief_text):
            warnings.append("brief: no threshold sentences; the Thresholds section has nothing agreed to test")
    return {"period": [d.isoformat() for d in period] if period else None, "call": call,
            "decider": meta.get("decider", ""), "records_found": sorted(records), "cited": sorted(cited_all),
            "errors": errors, "warnings": warnings}


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--report", type=Path, required=True, help="value report Markdown file")
    parser.add_argument("--plan", type=Path, nargs="+", required=True,
                        help="the plan, and any ticket files, holding the M and I records")
    parser.add_argument("--brief", type=Path, help="discovery brief, to check its baseline and threshold sentences")
    parser.add_argument("--json", action="store_true", help="print a JSON report instead of text")
    args = parser.parse_args(argv)
    try:
        report_text = args.report.read_text(encoding="utf-8")
        plans = [(str(path), path.read_text(encoding="utf-8")) for path in args.plan]
        brief = args.brief.read_text(encoding="utf-8") if args.brief else None
        report = check_report(report_text, plans, brief)
    except (OSError, UnicodeError) as exc:
        print(f"ERROR cannot read file: {exc}", file=sys.stderr)
        return 2
    except InputError as exc:
        print(f"ERROR {exc}", file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        period = " to ".join(report["period"]) if report["period"] else "?"
        print(f"value report for {period}; call {report['call'] or '?'} by {report['decider'] or '?'}; "
              f"{len(report['records_found'])} plan records, {len(report['cited'])} cited")
        for message in report["errors"]:
            print(f"ERROR {message}")
        for message in report["warnings"]:
            print(f"WARNING {message}")
        if not report["errors"]:
            print("Every figure cites a current record, the baseline is present and the call has a decider.")
    return 1 if report["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
