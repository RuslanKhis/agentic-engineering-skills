#!/usr/bin/env python3
"""Check a portability assessment against its design and plan. Standard library only; reads Markdown, never runs project code or git.

The assessment is ``docs/portability/<topic>.md``, written from this skill's
template. The checker judges form, not the architecture. Errors (exit 1):

- a required front-matter field is missing or empty; ``primary_build`` lacks
  "GCP" or "ADK"; ``status`` is not ``draft`` or ``reviewed``; ``goal`` is
  not a G ID or ``none``; ``targets`` is not a list drawn from ``aws`` and
  ``azure``; ``frameworks`` is not a list; ``sources_checked`` is not a date
  or is in the future;
- one of the 15 ``##`` sections is missing, empty or out of order;
- a ``--design`` or ``--plan`` path that does not exist; an R, C, D, G or M
  ID the assessment cites that neither file contains;
- a component classification row whose Class is not ``shared logic``,
  ``replaceable adapter``, ``provider-specific by choice`` or ``expensive
  dependency``, or whose Why is empty;
- the Dimensions section omits cloud, framework, model, service or
  deployment, or says "not a concern" without a reason; a target cloud or a
  listed framework that its alternatives section never names;
- a Sources row without an http(s) URL or a valid read date, or dated after
  ``--today``; a Sources table with no rows;
- a Relative effort row whose effort is not small, medium, large, very large
  or unknown, or whose Drivers cell is empty;
- a currency figure or a duration estimate (hours, days, weeks, months,
  sprints, person-days) outside the Sources section on a line that cites no
  ``M<n>`` record and does not say "assumption";
- an overpromise ("fully portable", "seamless migration", "drop-in
  replacement", "zero lock-in", "100% portable", "completely cloud-agnostic",
  "no lock-in") on a line without a negation (not, never, n't, cannot, no
  longer);
- a fenced code block tagged hcl, terraform, tf or bicep, or holding a
  Terraform resource, a Kubernetes manifest (``apiVersion:`` with ``kind:``)
  or an IAM policy (``"Statement"``);
- an optional recommendation without Rationale, Acceptance criteria and
  Specialist, or naming a specialist that is not an installed sibling skill;
- an unfilled ``<placeholder>`` outside code spans.

Warnings (exit 0): a read date or ``sources_checked`` older than 180 days, an
expensive dependency with no exit path, an item needing re-evaluation sized
small, a framework the reference does not cover, a template guidance comment
left in, and IDs left unchecked because neither ``--design`` nor ``--plan``
was given. Exit status 2 when an input cannot be read or has no front matter.
"""

from __future__ import annotations

import argparse
from datetime import date
import json
from pathlib import Path
import re
import sys

SECTIONS = (
    "Summary for the reader",
    "Concern and scope",
    "Baseline architecture",
    "Component classification",
    "Dimensions",
    "Cloud alternatives",
    "Agent framework alternatives",
    "Boundaries worth having",
    "Feature differences and migration risks",
    "Recommended strategy",
    "Phased outline",
    "Relative effort",
    "Optional recommendations for the current build",
    "Open questions",
    "Sources",
)
FIELDS = ("topic", "design", "plan", "goal", "primary_build", "concern", "targets", "frameworks",
          "sources_checked", "status")
STATUSES = ("draft", "reviewed")
CLASSES = ("shared logic", "replaceable adapter", "provider-specific by choice", "expensive dependency")
EFFORT = re.compile(r"^(?:very large|small|medium|large|unknown)\b")
DIMENSIONS = ("cloud", "framework", "model", "service", "deployment")
TARGETS = {"aws": "AWS", "azure": "Azure"}
# Frameworks the agent-frameworks reference covers, with the name the section must use.
FRAMEWORKS = {"langgraph": "LangGraph", "openai-agents": "OpenAI Agents", "openai-agents-sdk": "OpenAI Agents",
              "microsoft-agent-framework": "Agent Framework", "maf": "Agent Framework",
              "pydantic-ai": "Pydantic AI", "strands": "Strands", "strands-agents": "Strands"}
MAX_AGE_DAYS = 180

ISO = re.compile(r"^\d{4}-\d{2}-\d{2}$")
ID = re.compile(r"(?<![\w/.-])([RCDGM]\d+)(?![\w-])")
M_ID = re.compile(r"(?<![\w/.-])M\d+(?![\w-])")
URL = re.compile(r"https?://\S+")
CODE_SPAN = re.compile(r"`[^`\n]*`")
PLACEHOLDER = re.compile(r"<(?!!--)(?!/?(?:br|sub|sup|b|i|em|strong|code|details|summary|p|a)\b)"
                         r"(?!https?:)[A-Za-z][^<>\n]{0,200}>", re.IGNORECASE)
CURRENCY = re.compile(r"[$€£]\s?\d|\b(?:USD|EUR|GBP|AUD)\s?\d|\d[\d,.]*\s?(?:k|m)?\s?(?:USD|EUR|GBP|AUD)\b"
                      r"|\b\d[\d,.]*\s?(?:dollars|euros|pounds)\b", re.IGNORECASE)
DURATION = re.compile(r"\b\d+(?:\.\d+)?(?:\s*(?:-|–|to)\s*\d+(?:\.\d+)?)?\s*"
                      r"(?:(?:person|man|engineer|developer|dev)[- ]?)?(?:(?:working|business|calendar)\s+)?"
                      r"(?:hours?|hrs?|days?|weeks?|wks?|months?|sprints?)\b|\b\d+(?:\.\d+)?h\b",
                      re.IGNORECASE)
ASSUMPTION = re.compile(r"assumption", re.IGNORECASE)
OVERPROMISE = re.compile(r"fully[- ]portable|seamless(?:ly)?[- ]migrat\w*|drop[- ]in[- ]replacements?|zero[- ]lock[- ]in"
                         r"|100\s?%\s?portable|completely[- ]cloud[- ]agnostic|\bno[- ]lock[- ]in", re.IGNORECASE)
NEGATION = re.compile(r"\b(?:not|never|cannot|no longer)\b|n['’]t\b", re.IGNORECASE)
FORBIDDEN_TAGS = {"hcl", "terraform", "tf", "bicep"}
FORBIDDEN_CONTENT = (
    (re.compile(r'resource\s+"(?:aws_|azurerm_|google_)'), "a Terraform resource"),
    (re.compile(r'"Statement"'), "an IAM policy document"),
)
K8S = (re.compile(r"(?m)^\s*apiVersion\s*:"), re.compile(r"(?m)^\s*kind\s*:"))
EMPTY_CELL = {"", "-", "—", "–", "none", "n/a", "tbd"}
REEVALUATION = re.compile(r"re-?evaluat|re-?baselin|eval(?:uation)? sets?", re.IGNORECASE)
SKILL_NAME = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)+$")


class InputError(Exception):
    """An input that cannot be read: exit status 2."""


def read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        raise InputError(f"cannot read {path}: {exc}") from exc


def split_front_matter(text: str, path: Path) -> tuple[dict[str, tuple[str, int]], list[tuple[int, str]]]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise InputError(f"{path}: no front matter (expected a leading --- block)")
    for end in range(1, len(lines)):
        if lines[end].strip() == "---":
            meta = {}
            for number, raw in enumerate(lines[1:end], 2):
                if ":" in raw and not raw.lstrip().startswith("#"):
                    key, value = raw.split(":", 1)
                    meta[key.strip().lower()] = (value.strip(), number)
            body = [(number, line) for number, line in enumerate(lines[end + 1:], end + 2)]
            return meta, body
    raise InputError(f"{path}: front matter has no closing ---")


def parse_list(value: str) -> list[str] | None:
    """``[aws, azure]  # comment`` -> ``['aws', 'azure']``; None when not a list."""
    value = re.sub(r"\s+#.*$", "", value).strip()
    if not (value.startswith("[") and value.endswith("]")):
        return None
    return [item.strip().strip("\"'").lower() for item in value[1:-1].split(",") if item.strip()]


def parse_date(value: str) -> date | None:
    value = value.strip().strip("\"'")
    if not ISO.match(value):
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        return None


def scan_body(body: list[tuple[int, str]]):
    """Split the body into sections and fenced code blocks.

    Returns (sections, fences): sections maps each ``##`` heading to its
    (line_number, text) lines with code fences removed, in order; fences is a
    list of (line_number, info_string, content).
    """
    sections: list[tuple[str, int, list[tuple[int, str]]]] = [("(preamble)", 0, [])]
    fences: list[tuple[int, str, str]] = []
    fence_start, fence_info, fence_lines, marker = 0, "", [], ""
    for number, line in body:
        stripped = line.lstrip()
        if marker:
            if stripped.startswith(marker):
                fences.append((fence_start, fence_info, "\n".join(fence_lines)))
                marker = ""
            else:
                fence_lines.append(line)
            continue
        opening = re.match(r"(`{3,}|~{3,})\s*([\w+-]*)", stripped)
        if opening:
            marker, fence_info, fence_start, fence_lines = opening.group(1), opening.group(2).lower(), number, []
            continue
        heading = re.match(r"^##\s+(.+?)\s*#*\s*$", line)
        if heading:
            sections.append((heading.group(1).strip(), number, []))
            continue
        sections[-1][2].append((number, line))
    if marker:
        fences.append((fence_start, fence_info, "\n".join(fence_lines)))
    return sections, fences


def table_rows(lines: list[tuple[int, str]]) -> tuple[list[str], list[tuple[int, list[str]]]]:
    """The first Markdown table in ``lines``: (lowercased headers, [(line, cells)])."""
    headers: list[str] = []
    rows: list[tuple[int, list[str]]] = []
    started = False
    for number, raw in lines:
        line = raw.strip()
        if not line.startswith("|"):
            if started:
                break
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if not started:
            headers, started = [clean(c).lower() for c in cells], True
        elif not re.fullmatch(r"\|?[\s:|-]+\|?", line):
            rows.append((number, cells))
    return headers, rows


def clean(cell: str) -> str:
    return re.sub(r"[*_`]", "", cell).strip()


def column(headers: list[str], *words: str) -> int | None:
    return next((i for i, h in enumerate(headers) if any(w in h for w in words)), None)


def cell(cells: list[str], index: int | None) -> str:
    return clean(cells[index]) if index is not None and index < len(cells) else ""


def text_of(lines: list[tuple[int, str]]) -> str:
    return "\n".join(t for _, t in lines)


def meaningful(lines: list[tuple[int, str]]) -> bool:
    text = re.sub(r"<!--.*?-->", "", text_of(lines), flags=re.DOTALL)
    return bool(text.strip())


def check_front_matter(meta, today, errors, warnings) -> dict:
    for field in FIELDS:
        if field not in meta:
            errors.append(f"front matter: missing {field}")
        elif field not in ("targets", "frameworks") and not meta[field][0].strip("\"' "):
            errors.append(f"line {meta[field][1]}: front matter {field} is empty")
    primary = meta.get("primary_build", ("", 0))[0]
    if "primary_build" in meta and not ("GCP" in primary and "ADK" in primary):
        errors.append(f"line {meta['primary_build'][1]}: primary_build must name GCP and ADK "
                      f"(the primary build stays GCP + Google ADK), found {primary!r}")
    status = meta.get("status", ("", 0))[0].strip("\"'").lower()
    if "status" in meta and status not in STATUSES:
        errors.append(f"line {meta['status'][1]}: status must be draft or reviewed, found {status!r}")
    goal = meta.get("goal", ("", 0))[0].strip("\"'")
    if "goal" in meta and goal and not re.fullmatch(r"G\d+|none", goal):
        errors.append(f"line {meta['goal'][1]}: goal must be a plan goal ID (G05) or none, found {goal!r}")
    targets: list[str] = []
    if "targets" in meta:
        parsed = parse_list(meta["targets"][0])
        if parsed is None:
            errors.append(f"line {meta['targets'][1]}: targets must be a list such as [aws, azure] or []")
        else:
            targets = parsed
            unknown = [t for t in targets if t not in TARGETS]
            if unknown:
                errors.append(f"line {meta['targets'][1]}: unknown target {', '.join(unknown)}; use aws or azure")
    frameworks: list[str] = []
    if "frameworks" in meta:
        parsed = parse_list(meta["frameworks"][0])
        if parsed is None:
            errors.append(f"line {meta['frameworks'][1]}: frameworks must be a list such as [langgraph] or []")
        else:
            frameworks = parsed
            for name in frameworks:
                if name not in FRAMEWORKS:
                    warnings.append(f"line {meta['frameworks'][1]}: framework {name!r} is not in the reference; "
                                    "research it at its source and cite it")
    if "sources_checked" in meta:
        checked = parse_date(meta["sources_checked"][0])
        number = meta["sources_checked"][1]
        if checked is None:
            errors.append(f"line {number}: sources_checked must be a date (YYYY-MM-DD)")
        elif checked > today:
            errors.append(f"line {number}: sources_checked {checked} is in the future")
        elif (today - checked).days > MAX_AGE_DAYS:
            warnings.append(f"line {number}: sources_checked {checked} is over {MAX_AGE_DAYS} days old")
    return {"targets": targets, "frameworks": frameworks, "goal": goal}


def check_sections(sections, errors) -> dict[str, list[tuple[int, str]]]:
    found: dict[str, tuple[int, list[tuple[int, str]]]] = {}
    order: list[str] = []
    for heading, number, lines in sections[1:]:
        key = heading.lower()
        if key in (s.lower() for s in SECTIONS) and key not in found:
            found[key] = (number, lines)
            order.append(key)
    expected = [s.lower() for s in SECTIONS]
    for name in SECTIONS:
        entry = found.get(name.lower())
        if entry is None:
            errors.append(f"missing section: ## {name}")
        elif not meaningful(entry[1]):
            errors.append(f"line {entry[0]}: empty section: ## {name}")
    last = -1
    for key in order:
        index = expected.index(key)
        if index < last:
            errors.append(f"line {found[key][0]}: section ## {SECTIONS[index]} is out of order; "
                          f"keep the template's order")
        last = max(last, index)
    return {key: lines for key, (_, lines) in found.items()}


def check_classification(lines, errors, warnings) -> dict[str, int]:
    headers, rows = table_rows(lines)
    counts = {c: 0 for c in CLASSES}
    if not rows:
        errors.append("## Component classification: no table rows; classify every component")
        return counts
    klass, why, exit_path = column(headers, "class"), column(headers, "why"), column(headers, "exit")
    if klass is None or why is None:
        errors.append("## Component classification: the table needs Class and Why columns")
        return counts
    for number, cells in rows:
        value = re.sub(r"\s+", " ", cell(cells, klass).lower()).strip(" .")
        component = cell(cells, 0) or "(unnamed)"
        if value not in CLASSES:
            errors.append(f"line {number}: class {cell(cells, klass)!r} for {component} is not one of "
                          f"{', '.join(CLASSES)}")
        else:
            counts[value] += 1
        if cell(cells, why).lower() in EMPTY_CELL:
            errors.append(f"line {number}: {component} has no Why")
        if value == "expensive dependency" and cell(cells, exit_path).lower() in EMPTY_CELL:
            warnings.append(f"line {number}: expensive dependency {component} has no exit path")
    return counts


def check_dimensions(lines, errors) -> None:
    text = text_of(lines).lower()
    for dimension in DIMENSIONS:
        if dimension not in text:
            errors.append(f"## Dimensions: {dimension} is not assessed; assess it or write "
                          f"'not a concern: <reason>'")
    for number, raw in lines:
        for match in re.finditer(r"not a concern", raw, re.IGNORECASE):
            rest = re.split(r"\|", raw[match.end():], maxsplit=1)[0]
            if not re.sub(r"[\s:;,.—–*_-]", "", rest):
                errors.append(f"line {number}: 'not a concern' needs a reason")


def check_names(lines, names: dict[str, str], section: str, errors) -> None:
    text = text_of(lines).lower()
    for key, display in names.items():
        if display.lower() not in text:
            errors.append(f"## {section}: {key} is listed in the front matter but not assessed here")


def check_sources(lines, today, errors, warnings) -> None:
    headers, rows = table_rows(lines)
    if not rows:
        errors.append("## Sources: no table rows; cite each claim with its URL and read date")
        return
    url_col, read_col = column(headers, "url"), column(headers, "read", "date")
    if read_col is None:
        errors.append("## Sources: the table needs a 'Read on' column")
    for number, cells in rows:
        url_cell = cells[url_col] if url_col is not None and url_col < len(cells) else " ".join(cells)
        if not URL.search(url_cell):
            errors.append(f"line {number}: source has no http(s) URL")
        if read_col is None:
            continue
        raw = cell(cells, read_col)
        when = parse_date(raw)
        if when is None:
            errors.append(f"line {number}: source read date {raw or '(empty)'!r} is not a date (YYYY-MM-DD)")
        elif when > today:
            errors.append(f"line {number}: source read date {when} is in the future")
        elif (today - when).days > MAX_AGE_DAYS:
            warnings.append(f"line {number}: source read {when} is over {MAX_AGE_DAYS} days old; re-check it")


def check_effort(lines, errors, warnings) -> None:
    headers, rows = table_rows(lines)
    if not rows:
        errors.append("## Relative effort: no table rows")
        return
    effort, drivers = column(headers, "effort"), column(headers, "driver")
    if effort is None or drivers is None:
        errors.append("## Relative effort: the table needs Relative effort and Drivers columns")
        return
    for number, cells in rows:
        value = re.sub(r"\s+", " ", cell(cells, effort).lower())
        item = cell(cells, 0) or "(unnamed)"
        if not EFFORT.match(value):
            errors.append(f"line {number}: effort {cell(cells, effort)!r} for {item} is not small, medium, large, "
                          "very large or unknown")
        driver_text = cell(cells, drivers)
        if driver_text.lower() in EMPTY_CELL:
            errors.append(f"line {number}: {item} has no Drivers")
        context = f"{item} {driver_text}"
        if value.startswith("small") and REEVALUATION.search(context) and not NEGATION.search(context):
            warnings.append(f"line {number}: {item} needs re-evaluation, so it is at least medium")


def check_recommendations(lines, installed: set[str], errors) -> None:
    body = [(n, t) for n, t in lines if t.strip() and not t.strip().startswith("<!--")]
    if not body:
        return
    blocks: list[tuple[int, str, list[tuple[int, str]]]] = []
    for number, raw in lines:
        heading = re.match(r"^###\s+(.+)", raw)
        if heading:
            blocks.append((number, heading.group(1).strip(), []))
        elif blocks:
            blocks[-1][2].append((number, raw))
    if not blocks and re.match(r"^\W*none\b", body[0][1].strip(), re.IGNORECASE):
        return
    if not blocks:
        errors.append("## Optional recommendations for the current build: write 'None' or one ### block per "
                      "recommendation with Rationale, Acceptance criteria and Specialist")
    for number, title, block in blocks:
        text = text_of(block).lower()
        for label in ("rationale", "acceptance criteria", "specialist"):
            if label not in text:
                errors.append(f"line {number}: recommendation '{title}' has no {label.capitalize()}")
    for number, raw in lines:
        if "specialist" not in raw.lower():
            continue
        names = set(re.findall(r"`([^`\s]+)`", raw))
        label = re.search(r"specialist\W*:\W*([a-z0-9][a-z0-9-]+)", raw, re.IGNORECASE)
        if label:
            names.add(label.group(1))
        for name in sorted(n for n in names if SKILL_NAME.match(n)):
            if name not in installed:
                errors.append(f"line {number}: specialist {name} is not an installed skill; name an existing "
                              "specialist or propose the gap to the designer")


def check(path: Path, design: Path | None, plan: Path | None, skills_dir: Path, today: date):
    meta, body = split_front_matter(read(path), path)
    errors: list[str] = []
    warnings: list[str] = []
    front = check_front_matter(meta, today, errors, warnings)
    sections, fences = scan_body(body)
    found = check_sections(sections, errors)

    for heading, _, lines in sections:
        for number, raw in lines:
            if "<!--" in raw:
                warnings.append(f"line {number}: template guidance comment left in; delete it")
                break

    counts = check_classification(found.get("component classification", []), errors, warnings) \
        if "component classification" in found else {}
    if "dimensions" in found:
        check_dimensions(found["dimensions"], errors)
    if "cloud alternatives" in found:
        check_names(found["cloud alternatives"], {t: TARGETS[t] for t in front["targets"] if t in TARGETS},
                    "Cloud alternatives", errors)
    if "agent framework alternatives" in found:
        check_names(found["agent framework alternatives"],
                    {f: FRAMEWORKS.get(f, f) for f in front["frameworks"]}, "Agent framework alternatives", errors)
    if "sources" in found:
        check_sources(found["sources"], today, errors, warnings)
    if "relative effort" in found:
        check_effort(found["relative effort"], errors, warnings)
    if "optional recommendations for the current build" in found:
        installed = {p.name for p in skills_dir.iterdir() if (p / "SKILL.md").is_file()} if skills_dir.is_dir() else set()
        check_recommendations(found["optional recommendations for the current build"], installed, errors)

    # Line-level rules over the whole body (fences removed), front matter excluded.
    cited: dict[str, int] = {}
    if front["goal"] and re.fullmatch(r"G\d+", front["goal"]):
        cited[front["goal"]] = meta["goal"][1]
    for value, number in meta.values():
        for placeholder in PLACEHOLDER.findall(CODE_SPAN.sub("", value)):
            errors.append(f"line {number}: unfilled placeholder {placeholder}")
    for heading, _, lines in sections:
        in_sources = heading.lower() == "sources"
        for number, raw in lines:
            prose = CODE_SPAN.sub("", raw)
            for placeholder in PLACEHOLDER.findall(prose):
                errors.append(f"line {number}: unfilled placeholder {placeholder}")
            for ident in ID.findall(URL.sub("", prose)):
                cited.setdefault(ident, number)
            if not in_sources and (CURRENCY.search(raw) or DURATION.search(raw)) \
                    and not M_ID.search(raw) and not ASSUMPTION.search(raw):
                figure = (CURRENCY.search(raw) or DURATION.search(raw)).group(0)
                errors.append(f"line {number}: figure {figure!r} needs a plan measurement (M<n>) on the same line "
                              "or the word 'assumption'")
            for match in OVERPROMISE.finditer(raw):
                if not NEGATION.search(raw):
                    errors.append(f"line {number}: overpromise {match.group(0)!r}; state the remaining "
                                  "provider-specific dependencies instead")
    for number, info, content in fences:
        if info in FORBIDDEN_TAGS:
            errors.append(f"line {number}: {info} code block; this skill writes no infrastructure code")
            continue
        for pattern, label in FORBIDDEN_CONTENT:
            if pattern.search(content):
                errors.append(f"line {number}: code block holds {label}; this skill writes no infrastructure code")
        if all(p.search(content) for p in K8S):
            errors.append(f"line {number}: code block holds a Kubernetes manifest; this skill writes no "
                          "deployment code")

    known: set[str] = set()
    missing = False
    for label, source in (("--design", design), ("--plan", plan)):
        if source is None:
            continue
        if not source.is_file():
            errors.append(f"{label} {source} does not exist")
            missing = True
            continue
        known.update(ID.findall(read(source)))
    if design is None and plan is None:
        warnings.append("no --design or --plan given: cited IDs were not checked")
    elif not missing:
        for ident, number in sorted(cited.items(), key=lambda item: item[1]):
            if ident not in known:
                errors.append(f"line {number}: cites {ident}, which neither the design nor the plan contains")

    summary = {"file": str(path), "ok": not errors, "targets": front["targets"], "frameworks": front["frameworks"],
               "classes": counts, "errors": errors, "warnings": warnings}
    return errors, warnings, summary


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("assessment", type=Path, help="docs/portability/<topic>.md")
    parser.add_argument("--design", type=Path, help="docs/architecture/<topic>.md")
    parser.add_argument("--plan", type=Path, help="docs/plans/<topic>.md (or the design file in compact form)")
    parser.add_argument("--skills-dir", type=Path, default=Path(__file__).resolve().parents[2],
                        help="directory of installed skills (default: this skill's parent directory)")
    parser.add_argument("--today", type=date.fromisoformat, default=date.today(), help="date to check against")
    parser.add_argument("--json", action="store_true", help="print the result as JSON")
    args = parser.parse_args(argv)
    try:
        errors, warnings, summary = check(args.assessment, args.design, args.plan, args.skills_dir, args.today)
    except InputError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps(summary, indent=2))
    else:
        counts = ", ".join(f"{n} {c}" for c, n in summary["classes"].items() if n) or "no components"
        print(f"{'ok' if not errors else 'FAIL'}  {args.assessment} (targets: {', '.join(summary['targets']) or 'none'}; "
              f"frameworks: {', '.join(summary['frameworks']) or 'none'}; {counts})")
        for message in errors:
            print(f"  error: {message}")
        for message in warnings:
            print(f"  warning: {message}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
