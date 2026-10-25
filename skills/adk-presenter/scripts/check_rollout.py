#!/usr/bin/env python3
"""Check a rollout pack's structure and contract citations. Standard library only; reads Markdown.

Reads the pack written from the presenter's rollout pack template and reports
a problem when:

- a will, won't or hands-over statement cites no contract (``C3``), or, with
  ``--design``, cites one the design's contracts table lacks; or the table has
  no statement of one of the three kinds;
- the AI disclosure has no status (applies, not legally required: <reason>,
  verify) or no quoted text;
- the adoption metrics do not define "active user" with a number and a window
  (days, weeks or months), or name no counter-metric;
- the feedback rows map to no feedback-record category (wrong_answer,
  tool_failed, too_slow, unsafe, other) or have no owner;
- a hypercare exit criterion lacks a numeric threshold or a window;
- a rollout message for the sponsor, middle managers or frontline users is
  missing, or a training session has no minutes or date;
- the hypercare exit test is neither marked ``Agreed with <name> on YYYY-MM-DD``
  nor ``Status: proposed`` (a proposed test passes with a note);
- there is no assumptions and gaps section;
- the pack still holds a template placeholder such as ``<role>`` anywhere
  outside code fences.

Exit status: 0 consistent, 1 problems found, 2 input cannot be read.
"""

import argparse
import json
from pathlib import Path
import re
import sys

FENCE = re.compile(r"^```.*?^```\s*$", re.MULTILINE | re.DOTALL)
CONTRACT = re.compile(r"(?<![\w/-])C\d+(?![\w/-])")
PLACEHOLDER = re.compile(r"<[A-Za-z][^<>|]*>")
COMPARATOR = re.compile(r"[≥≤<>=]|\bat (?:least|most)\b|\bno (?:more|fewer|less) than\b|\bwithin\b"
                        r"|^\s*\d+(?:\.\d+)?\s*$|\b\d+\s+(?:of|out of)\s+\d+\b", re.IGNORECASE)
WINDOW = re.compile(r"\d+\s*(?:consecutive\s+|working\s+|rolling\s+|calendar\s+)*(?:day|week|month)s?\b"
                    r"|\b(?:day|week|month)s?\b.*\d|\bat exit\b|\bat go-live\b", re.IGNORECASE)
CATEGORIES = ("wrong_answer", "tool_failed", "too_slow", "unsafe", "other")
STATUS = re.compile(r"^\s*status\s*:\s*(applies|not legally required\s*:\s*\S.*|verify)\s*$",
                    re.IGNORECASE | re.MULTILINE)
DISCLOSURE_TEXT = re.compile(r"^\s*text\s*:\s*[\"“].{10,}[\"”]", re.IGNORECASE | re.MULTILINE)
DATE = re.compile(r"\b\d{4}-\d{2}-\d{2}\b")


class InputError(Exception):
    pass


def tables(text):
    found, current = [], None
    for raw in FENCE.sub("", text).splitlines():
        line = raw.strip()
        if not line.startswith("|"):
            current = None
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
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


def section(text, words):
    """Text under the first heading containing every word, up to the next heading of the same or higher level."""
    body = FENCE.sub("", text)
    for match in re.finditer(r"^(#{2,4})\s+(.*)$", body, re.MULTILINE):
        if all(w in match.group(2).lower() for w in words):
            level = len(match.group(1))
            rest = body[match.end():]
            stop = re.search(rf"^#{{1,{level}}}\s", rest, re.MULTILINE)
            return rest[:stop.start()] if stop else rest
    return None


def placeholders(label, rows):
    return [f"{label} {row[0] or '(row)'}: placeholder {m.group(0)!r} left in the table"
            for row in rows for cell in row for m in [PLACEHOLDER.search(cell)] if m]


def design_contracts(path):
    contracts = set()
    for header, rows in tables(path.read_text(encoding="utf-8")):
        if any("invariant" in h for h in header):
            contracts.update(row[0].strip() for row in rows if re.fullmatch(r"C\d+", row[0].strip()))
    if not contracts:
        raise InputError(f"{path}: no contracts table (a table with an Invariant column and C1, C2 rows)")
    return contracts


def check_pack(text, contracts=None):
    problems, notes = [], []
    for number, raw in enumerate(FENCE.sub("", text).splitlines(), 1):
        if not raw.strip().startswith("|"):
            for match in PLACEHOLDER.finditer(raw):
                problems.append(f"line {number}: placeholder {match.group(0)!r} left in the text")
    if section(text, ("assumptions",)) is None:
        problems.append("no 'Assumptions and gaps' section; record assumed dates and missing inputs at the top")

    header, rows = find_table(text, ("statement", "contract"), "will / won't / hands over")
    problems += placeholders("statement", rows)
    kinds = set()
    for row in rows:
        statement = row[0]
        kind = re.match(r"\s*(will|won['’]?t|will not|hands over|a person steps in)\b", statement, re.I)
        if kind:
            word = kind.group(1).lower()
            kinds.add("will" if word == "will" else "hands over" if word in ("hands over", "a person steps in")
                      else "won't")
        cited = CONTRACT.findall(column(header, row, "contract"))
        if not cited:
            problems.append(f"statement {statement[:50]!r} cites no contract; cite the C ID that enforces it or "
                            "leave the statement out")
        for contract in cited:
            if contracts is not None and contract not in contracts:
                problems.append(f"statement {statement[:50]!r} cites {contract}, which is not in the design")
    for kind in ("will", "won't", "hands over"):
        if kind not in kinds:
            problems.append(f"no '{kind.capitalize()}:' statement; users need what it does, what it never does "
                            "and when a person steps in")

    disclosure = section(text, ("disclosure",))
    if disclosure is None:
        problems.append("no AI disclosure section")
    else:
        if not STATUS.search(disclosure):
            problems.append("AI disclosure: set 'Status: applies', 'Status: not legally required: <reason>' or "
                            "'Status: verify'")
        if not DISCLOSURE_TEXT.search(disclosure):
            problems.append("AI disclosure: give the exact quoted text on a 'Text:' line")

    header, rows = find_table(text, ("metric", "definition"), "adoption metrics")
    problems += placeholders("metric", rows)
    active = [r for r in rows if r[0].lower().startswith("active user")]
    if not active:
        problems.append("adoption metrics: define 'Active user'")
    else:
        row = active[0]
        defined = " ".join([column(header, row, "definition"), column(header, row, "window")])
        if not (re.search(r"\d", defined) and WINDOW.search(defined)):
            problems.append("adoption metrics: 'Active user' needs a threshold and a window "
                            "(e.g. at least 1 completed invocation in 7 days)")
    if not any("counter" in r[0].lower() for r in rows):
        problems.append("adoption metrics: name the counter-metric from the discovery brief")

    header, rows = find_table(text, ("user action", "record category"), "feedback channel")
    problems += placeholders("feedback", rows)
    mapped = [r for r in rows if any(c in column(header, r, "record category") for c in CATEGORIES)]
    if not mapped:
        problems.append("feedback channel: map user actions to the feedback record categories "
                        f"({', '.join(CATEGORIES)})")
    for row in rows:
        if not column(header, row, "owner").strip():
            problems.append(f"feedback {row[0]!r}: no owner")

    header, rows = find_table(text, ("criterion", "threshold", "window"), "hypercare exit test")
    problems += placeholders("exit", rows)
    if not rows:
        problems.append("hypercare exit test has no criteria")
    exit_text = section(text, ("exit",)) or ""
    if re.search(r"(?i)\bstatus\s*:\s*proposed\b", exit_text):
        notes.append("hypercare exit test is proposed, not yet agreed with the sponsor")
    elif not re.search(r"(?i)\bagreed with\b[^\n]*\b\d{4}-\d{2}-\d{2}\b", exit_text):
        problems.append("hypercare exit test: write 'Agreed with <name> on YYYY-MM-DD' or 'Status: proposed'")
    for row in rows:
        threshold = column(header, row, "threshold")
        if not (re.search(r"\d", threshold) and COMPARATOR.search(threshold)) and \
                threshold.strip().lower() not in ("passed", "pass"):
            problems.append(f"exit criterion {row[0]!r}: threshold {threshold!r} needs a number and a comparator")
        if not WINDOW.search(column(header, row, "window")):
            problems.append(f"exit criterion {row[0]!r}: window {column(header, row, 'window')!r} needs a period")

    for words, label in ((("sponsor",), "sponsor"), (("manager",), "middle managers"),
                         (("frontline",), "frontline users")):
        body = section(text, words)
        if body is None:
            problems.append(f"rollout messages: no message for {label} (a heading naming them)")
            continue
        words_left = PLACEHOLDER.sub("", re.sub(r"(?im)^\s*sender\s*:.*$", "", body)).split()
        if len(words_left) < 15:
            problems.append(f"rollout messages: the {label} message is empty or still a placeholder")

    header, rows = find_table(text, ("session", "minutes"), "training plan")
    problems += placeholders("training", rows)
    if not rows:
        problems.append("training plan has no sessions")
    for row in rows:
        if not re.search(r"\d", column(header, row, "minutes")):
            problems.append(f"training {row[0]!r}: no minutes")
        if not DATE.search(column(header, row, "date")):
            problems.append(f"training {row[0]!r}: no date (YYYY-MM-DD)")
    return problems, notes


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--pack", type=Path, required=True, help="rollout pack Markdown")
    parser.add_argument("--design", type=Path, help="design Markdown whose contracts table the statements cite")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    try:
        contracts = design_contracts(args.design) if args.design else None
        problems, notes = check_pack(args.pack.read_text(encoding="utf-8"), contracts)
    except (InputError, OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps({"problems": problems, "notes": notes}, indent=1))
    else:
        for note in notes:
            print(f"NOTE: {note}")
        for problem in problems:
            print(f"PROBLEM: {problem}")
        if not problems:
            print("Rollout pack structure and contract citations are consistent. Clarity is not checked; "
                  "read the guide with a frontline user.")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
