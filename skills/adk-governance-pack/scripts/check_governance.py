#!/usr/bin/env python3
"""Check governance drafts for citations, counsel flags and dated legal claims. Standard library only.

A draft is a Markdown file written from one of this skill's templates. It
opens with front matter naming its ``document`` type and ``counsel_required``
(``yes``, ``no`` or ``pending``). The checker never judges the law. It reports
what a reviewer would otherwise find by hand:

- a required section (``##`` heading) that is missing or empty;
- a statement (a bullet, a table data row or a prose paragraph) that cites
  nothing: no design, plan or evidence ID (``R``, ``C``, ``D``, ``SB``, ``G``
  with ``/A``, ``M``, ``I``, ``W``, ``O``), no project file path, no dated
  source (``source: <who or what>, <YYYY-MM-DD>`` or ``checked <YYYY-MM-DD>``)
  and no ``assumption:``, ``counsel:``, ``gap:``, ``deferred:``,
  ``hypothesis:`` or ``n/a:`` marker;
- an Annex III trigger phrase (employment, education, credit, essential
  services, biometrics and the other listed areas) in the draft or in a
  ``--source`` file while ``counsel_required`` is not ``yes``; sections headed as
  out-of-scope or excluded uses, and the memo's prohibited-practices,
  high-risk and transparency checklists, are not scanned;
- a line that states when a law or one of its articles applies (a legal
  reference, an applicability word and a date written in words, such as
  "2 August 2026") without ``checked <date>``; ISO dates are treated as
  project or provenance dates, and "read", "updated" or "published" dates
  are ignored;
  a checked date in the future is an error, one older than ``--max-age-days``
  a warning;
- with ``--source``, a cited R, C, D, SB, M, I, W or O ID that no source
  file contains (an invented reference); an SB rule named on a ``gap:``,
  ``n/a:`` or ``deferred:`` line is exempt, because the baseline lists rules
  a design may omit; a cited ``docs/`` file that does not exist from the
  current directory is a warning;
- an unfilled template placeholder (``<...>``).

Exit status: 0 clean (warnings allowed), 1 when any error is found, 2 when a
file cannot be read, has no front matter or names an unknown document type.
"""

from __future__ import annotations

import argparse
from datetime import date
import json
from pathlib import Path
import re
import sys

REQUIRED = {
    "classification-memo": (
        "Summary", "System and intended purpose", "Roles", "Prohibited practices",
        "High-risk classification", "Transparency obligations", "General-purpose AI model",
        "Applicable dates", "Questions for counsel"),
    "impact-assessment": (
        "Scope and intended use", "Interested parties", "System information",
        "Impacts", "Measures", "Residual risk and decision", "NIST AI RMF mapping",
        "Monitoring and review"),
    "dpia-input-pack": (
        "Screening", "Processing description", "Data flows", "Data subjects and categories",
        "Legal basis", "Necessity and proportionality", "Retention and erasure",
        "Recipients, processors and regions", "Model provider data use",
        "Risks and measures", "Questions for counsel"),
    "system-card": (
        "Intended use", "Out-of-scope use", "Limits", "Evaluation results",
        "Human oversight", "Data", "Contact"),
    "processing-records": ("Processing activities",),
    "security-questionnaire": ("Answer bank",),
    "poc-note": ("Classification", "Data flow summary", "Questions for counsel"),
}
COUNSEL_VALUES = {"yes", "no", "pending"}

# Phrases that put a system near an Annex III area. A match forces counsel
# review; it does not decide that the system is high-risk.
ANNEX_III = {
    "biometrics": (r"biometric", r"facial recognition", r"face recognition", r"emotion recognition"),
    "critical infrastructure": (r"critical infrastructure", r"road traffic", r"water supply",
                                r"gas supply", r"electricity supply", r"heating supply"),
    "education": (r"(?:student|school|university|college) admissions?", r"student assessment",
                  r"grading students", r"proctoring", r"learning outcomes?", r"educational institution",
                  r"vocational training"),
    "employment": (r"recruit(?:ment|ing)", r"\bhiring\b", r"\bCVs?\b", r"r[eé]sum[eé]s?\b",
                   r"candidate screening", r"job applicants?", r"job applications?",
                   r"shortlist(?:ing)? candidates", r"rank(?:s|ing)? candidates", r"promotion decisions?",
                   r"terminat(?:e|ion) of employment", r"dismissal", r"(?:employee|worker|staff) performance",
                   r"allocat(?:e|ing|ion of) (?:tasks|work|shifts) to (?:employees|workers|staff)",
                   r"monitor(?:ing)? (?:employees|workers|staff)"),
    "essential services": (r"creditworth", r"credit scor", r"credit decision", r"loan (?:approval|decision|application)",
                           r"public (?:assistance|benefits?)", r"social (?:security|benefits?)",
                           r"eligibility for (?:benefits|services)", r"life insurance", r"health insurance",
                           r"insurance pricing", r"emergency (?:calls?|dispatch)", r"patient triage"),
    "law enforcement": (r"law enforcement", r"\bpolice\b", r"criminal (?:offence|risk)", r"recidivism",
                        r"evidence reliability"),
    "migration and border control": (r"\basylum\b", r"\bvisa applications?\b", r"border control", r"immigration"),
    "justice and democratic processes": (r"judicial", r"\bcourt\b", r"dispute resolution", r"\belections?\b",
                                         r"voting behaviour", r"\breferendum\b"),
}
ANNEX_PATTERNS = [(area, re.compile(p, re.IGNORECASE if not p.startswith(r"\bCV") else 0))
                  for area, ps in ANNEX_III.items() for p in ps]
# Sections that list excluded uses, or walk the Article 5 and Annex III
# checklists, name the areas by design; the system's own description and the
# source records still trigger.
EXCLUDED_HEADING = re.compile(r"out[- ]of[- ]scope|excluded|prohibited|not intended|high-risk classification"
                              r"|transparency", re.IGNORECASE)

ID = re.compile(r"(?<![\w/-])(?:G\d+(?:/A\d+)?|SB\d+|[RCDMIWOHB]\d+)(?![\w-])")   # H, B: impact IDs
CHECKABLE_ID = re.compile(r"(?<![\w/-])(SB\d+|[RCDMIWO]\d+)(?![\w/-])")
PATH = re.compile(r"(?<![\w])[\w./-]+\.(?:md|json|csv|yaml|yml|txt|html|pdf)\b")
URL = re.compile(r"https?://\S+")
ISO = r"\d{4}-\d{2}-\d{2}"
DATED_SOURCE = re.compile(r"\bsource:[^\n]*?" + ISO, re.IGNORECASE)
CHECKED = re.compile(r"\bchecked\s+(" + ISO + r")", re.IGNORECASE)
MARKER = re.compile(r"(?<![\w/])(?:assumption|counsel|gap|n/a|hypothesis|deferred)\s*:\s*[^\s|]", re.IGNORECASE)
PLACEHOLDER = re.compile(r"<[A-Za-z][^<>\n]{0,80}>")
HTML_TAG = re.compile(r"</?(?:br|sub|sup|b|i|em|strong|code|details|summary|p|a)\b", re.IGNORECASE)

MONTHS = (r"(?:January|February|March|April|May|June|July|August|September|October|November|December"
          r"|Jan|Feb|Mar|Apr|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)\.?")
# Applicability dates are written in words ("2 August 2026"), as the law and the
# references write them; ISO dates are project and provenance dates.
LEGAL_DATE = re.compile(rf"\b\d{{1,2}}\s+{MONTHS}\s+\d{{4}}\b|\b{MONTHS}\s+\d{{1,2}},?\s+\d{{4}}\b", re.IGNORECASE)
# A date that records when a source was read or updated is not an applicability date.
PROVENANCE = re.compile(rf"\b(?:checked|read|updated|modified|dated|published)\s+(?:on\s+)?(?:{ISO}|"
                        rf"\d{{1,2}}\s+{MONTHS}\s+\d{{4}})", re.IGNORECASE)
GAP_LINE = re.compile(r"(?<![\w/])(?:gap|n/a|deferred)\s*:", re.IGNORECASE)
LEGAL_REF = re.compile(r"\b(?:Art\.|Articles?|Annex|Regulation|Directive|AI Act|GDPR|Omnibus|Chapter)\b",
                       re.IGNORECASE)
APPLICABILITY = re.compile(r"\b(?:appl(?:y|ies|ied|ying|ication|icable)|in force|enters?|entry into force"
                           r"|from|until|deadline|delay(?:ed|s)?|postpone(?:d|s)?|effective"
                           r"|obligations? start)\b",
                           re.IGNORECASE)


def split_front_matter(text: str) -> tuple[dict, list[str], int] | None:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    for end in range(1, len(lines)):
        if lines[end].strip() == "---":
            meta = {}
            for raw in lines[1:end]:
                if ":" in raw and not raw.lstrip().startswith("#"):
                    key, value = raw.split(":", 1)
                    meta[key.strip().lower()] = value.strip().strip("\"'")
            return meta, lines[end + 1:], end + 2
    return None


def sections(body: list[str], offset: int):
    """Yield (heading, [(line_number, text)]) per ``##`` section, code fences removed."""
    heading, current, fenced = "(preamble)", [], False
    for index, line in enumerate(body):
        number = index + offset
        if line.lstrip().startswith("```"):
            fenced = not fenced
            continue
        if fenced:
            continue
        if re.match(r"^##\s+", line):
            yield heading, current
            heading, current = re.sub(r"^##\s+", "", line).strip(), []
            continue
        current.append((number, line))
    yield heading, current


def cites(text: str) -> bool:
    return bool(ID.search(text) or PATH.search(text) or URL.search(text) or DATED_SOURCE.search(text)
                or CHECKED.search(text) or MARKER.search(text))


def statements(lines: list[tuple[int, str]]):
    """Yield (line_number, text) for bullets, table data rows and prose paragraphs."""
    paragraph: list[tuple[int, str]] = []
    table_row = 0

    def flush():
        if paragraph:
            joined = " ".join(t.strip() for _, t in paragraph)
            first = paragraph[0][0]
            paragraph.clear()
            return (first, joined)
        return None

    for number, raw in lines:
        line = raw.strip()
        if not line or line.startswith("#") or line.startswith("<!--") or line == "---":
            item = flush()
            if item:
                yield item
            table_row = 0
            continue
        if line.startswith("|"):
            item = flush()
            if item:
                yield item
            table_row += 1
            if table_row == 1 or re.fullmatch(r"\|?[\s:|-]+\|?", line):
                continue
            cells = [c.strip() for c in line.strip("|").split("|")]
            if any(c and c not in {"-", "—"} for c in cells[1:]) or len(cells) == 1:
                yield number, line
            continue
        table_row = 0
        if re.match(r"^(?:[-*+]|\d+[.)])\s+", line):
            item = flush()
            if item:
                yield item
            yield number, line
            continue
        paragraph.append((number, raw))
    item = flush()
    if item:
        yield item


def lead_in(text: str) -> bool:
    """A short label line such as ``Data flows:`` introduces the statements under it."""
    stripped = re.sub(r"^(?:[-*+]|\d+[.)])\s+", "", text).strip().strip("*_")
    return stripped.endswith(":") and len(stripped.split()) <= 8


def check(path: Path, sources: list[Path], today: date, max_age: int) -> tuple[list[str], list[str], dict]:
    text = path.read_text(encoding="utf-8")
    parsed = split_front_matter(text)
    if parsed is None:
        raise ValueError(f"{path}: no front matter (expected a leading --- block)")
    meta, body, offset = parsed
    doc = meta.get("document", "")
    if doc not in REQUIRED:
        raise ValueError(f"{path}: unknown document type {doc!r}; expected one of {sorted(REQUIRED)}")
    errors: list[str] = []
    warnings: list[str] = []
    counsel = meta.get("counsel_required", "").lower().split()[0] if meta.get("counsel_required") else ""
    if counsel not in COUNSEL_VALUES:
        errors.append(f"front matter: counsel_required must be yes, no or pending (found {counsel or 'nothing'!r})")

    found = {}
    for heading, lines in sections(body, offset):
        found[heading.lower()] = lines
    for name in REQUIRED[doc]:
        match = next((h for h in found if h.startswith(name.lower())), None)
        if match is None:
            errors.append(f"missing section: ## {name}")
        elif not any(t.strip() for _, t in found[match]):
            errors.append(f"empty section: ## {name}")

    triggers: dict[str, set[str]] = {}
    cited_ids: dict[str, int] = {}
    for heading, lines in sections(body, offset):
        excluded = bool(EXCLUDED_HEADING.search(heading))
        for number, raw in lines:
            for placeholder in PLACEHOLDER.findall(raw):
                if not HTML_TAG.match(placeholder) and not placeholder.startswith(("<http:", "<https:")):
                    errors.append(f"line {number}: unfilled placeholder {placeholder}")
            if not excluded:
                for area, pattern in ANNEX_PATTERNS:
                    hit = pattern.search(raw)
                    if hit:
                        triggers.setdefault(area, set()).add(f"{path.name}:{number} '{hit.group(0)}'")
            for ident in CHECKABLE_ID.findall(raw):
                # A baseline rule the design does not list may be named as a gap or n/a.
                if not (ident.startswith("SB") and GAP_LINE.search(raw)):
                    cited_ids.setdefault(ident, number)
            for cited in PATH.findall(raw):
                if cited.startswith("docs/") and not Path(cited).exists():
                    warnings.append(f"line {number}: cited file {cited} not found from the current directory")
            undated = PROVENANCE.sub("", raw)
            if LEGAL_REF.search(undated) and APPLICABILITY.search(undated) and LEGAL_DATE.search(undated):
                if not CHECKED.search(raw):
                    errors.append(f"line {number}: legal applicability date without 'checked <YYYY-MM-DD>'")
            for value in CHECKED.findall(raw):
                try:
                    when = date.fromisoformat(value)
                except ValueError:
                    errors.append(f"line {number}: checked date {value} is not a real date")
                    continue
                if when > today:
                    errors.append(f"line {number}: checked date {value} is in the future")
                elif (today - when).days > max_age:
                    warnings.append(f"line {number}: checked {value} is over {max_age} days old; re-check the source")
        if heading == "(preamble)":
            continue
        for number, statement in statements(lines):
            if lead_in(statement) or cites(statement):
                continue
            snippet = statement if len(statement) <= 70 else statement[:67] + "..."
            errors.append(f"line {number}: statement cites no ID, path, dated source or marker: {snippet}")

    source_ids: set[str] = set()
    for source in sources:
        source_text = source.read_text(encoding="utf-8")
        source_ids.update(CHECKABLE_ID.findall(source_text))
        for number, raw in enumerate(source_text.splitlines(), 1):
            for area, pattern in ANNEX_PATTERNS:
                hit = pattern.search(raw)
                if hit:
                    triggers.setdefault(area, set()).add(f"{source.name}:{number} '{hit.group(0)}'")
    if sources:
        for ident, number in sorted(cited_ids.items(), key=lambda item: item[1]):
            if ident not in source_ids:
                errors.append(f"line {number}: cites {ident}, which no source file contains")
    if triggers and counsel != "yes":
        areas = ", ".join(sorted(triggers))
        example = sorted(next(iter(triggers.values())))[0]
        errors.append(f"Annex III trigger ({areas}; e.g. {example}): set counsel_required: yes; "
                      "counsel confirms or rejects the high-risk classification")
    summary = {"file": str(path), "document": doc, "counsel_required": counsel,
               "annex_iii_areas": sorted(triggers), "errors": errors, "warnings": warnings}
    return errors, warnings, summary


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("drafts", nargs="+", type=Path, help="draft files or a directory of drafts")
    parser.add_argument("--source", action="append", type=Path, default=[],
                        help="discovery brief, design, plan or ticket the drafts cite (repeatable)")
    parser.add_argument("--today", type=date.fromisoformat, default=date.today(), help=argparse.SUPPRESS)
    parser.add_argument("--max-age-days", type=int, default=180)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    files: list[Path] = []
    for item in args.drafts:
        files.extend(sorted(item.glob("*.md")) if item.is_dir() else [item])
    if not files:
        print("ERROR: no draft files found", file=sys.stderr)
        return 2
    results, status = [], 0
    for path in files:
        try:
            errors, warnings, summary = check(path, args.source, args.today, args.max_age_days)
        except (OSError, UnicodeDecodeError, ValueError) as exc:
            print(f"ERROR: {exc}", file=sys.stderr)
            return 2
        results.append(summary)
        status = max(status, 1 if errors else 0)
    if args.json:
        print(json.dumps(results, indent=2))
    else:
        for summary in results:
            state = "FAIL" if summary["errors"] else "ok"
            areas = ", ".join(summary["annex_iii_areas"]) or "none"
            print(f"{state}  {summary['file']} ({summary['document']}; counsel_required: "
                  f"{summary['counsel_required'] or '?'}; Annex III areas: {areas})")
            for message in summary["errors"]:
                print(f"  error: {message}")
            for message in summary["warnings"]:
                print(f"  warning: {message}")
    return status


if __name__ == "__main__":
    raise SystemExit(main())
