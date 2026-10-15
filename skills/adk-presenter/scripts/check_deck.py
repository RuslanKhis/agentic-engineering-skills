#!/usr/bin/env python3
"""Check a presentation outline for evidence, coverage and timing. Standard library only; reads Markdown.

The deck format is the one in ``assets/deck-format.md``: YAML-like front
matter with ``stage``, ``audience`` and ``minutes``; slides separated by
``---`` lines; each slide opening with an action title (``## <claim>``) and
carrying ``Covers:`` tags, an ``Evidence:`` line and ``Notes:`` for the
speaker. The checker never judges whether the story is good. It reports what a
reviewer would otherwise find by hand:

- a slide with no ``Evidence:`` line, or one that cites nothing (no goal or
  acceptance ID such as ``G03/A2``, contract or decision ID, file path, URL,
  or the labels ``hypothesis``, ``assumption``, ``measured`` or ``n/a: <why>``);
- a number (a percentage, money, hours, counts) on a slide whose evidence is
  ``n/a`` or missing;
- stage and audience coverage: every tag the stage needs appears on some slide;
- titles that are labels rather than claims, slides without speaker notes,
  a timed slide count (title and appendix slides excluded) that does not fit
  the minutes, notes whose spoken length (about 130 words a minute) does not
  fit the minutes, and front matter without a decider and a date;
- on a ``case-study`` deck, wording Google's co-branding guidelines do not
  allow (``GCP``, ``powered by Google``, ``with Google Cloud AI``, partner or
  preference claims).

Exit status: 0 clean (warnings allowed), 1 when any error is found, 2 when the
file cannot be read or has no front matter.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys

STAGES = {
    "poc-approval": ("problem", "hypothesis", "success-criteria", "scope", "cost", "risks", "ask"),
    "production-approval": ("criteria-results", "learned", "production-scope", "cost", "risks", "ask"),
    "final-results": ("outcome", "adoption", "cost", "incidents", "next", "ask"),
    "case-study": ("challenge", "solution", "results", "next"),
}
TECHNICAL = {
    "poc-approval": ("architecture", "contracts", "evidence-plan", "dependencies"),
    "production-approval": ("architecture", "contracts", "evidence", "operations"),
    "final-results": ("architecture", "evidence", "operations", "handover"),
    "case-study": (),
}
AUDIENCES = ("business", "technical", "public")
ALL_TAGS = sorted({tag for tags in list(STAGES.values()) + list(TECHNICAL.values()) for tag in tags}
                  | {"title", "agenda", "summary", "method", "demo", "team", "timeline", "questions", "appendix"})
UNTIMED = {"title", "questions", "appendix"}
WORDS_PER_MINUTE = 130
GENERIC_TITLES = {"overview", "agenda", "introduction", "background", "results", "architecture",
                  "summary", "conclusion", "next steps", "questions", "thank you", "demo", "appendix",
                  "risks", "costs", "cost", "timeline", "team", "recommendation", "the ask"}
CITATION = re.compile(r"(?<![\w/-])(?:G\d+(?:/A\d+)?|[CDR]\d+|W\d+)(?![\w/-])")
PATH_OR_URL = re.compile(r"https?://\S+|\S+\.(?:md|json|csv|txt|png|svg|pdf|yaml|yml|ipynb)\b")
LABEL = re.compile(r"\b(?:hypothesis|assumption|measured|estimate[ds]?)\b", re.IGNORECASE)
NOT_APPLICABLE = re.compile(r"^\s*n/a\s*:\s*\S", re.IGNORECASE)
IDENTIFIER = re.compile(r"\b[A-Z]{1,2}\d+(?:/A\d+)?\b")
NUMERIC_CLAIM = re.compile(
    r"(?:[$€£]\s?\d[\d,.]*|\b(?:AUD|USD|EUR|GBP|CHF|JPY)\s?\d[\d,.]*"
    r"|\b\d+\s+of\s+\d+\b"
    r"|\d+(?:[.,]\d+)?\s*(?:%|percent|×|x\b|k\b|m\b|bn\b|million|billion|thousand"
    r"|hours?|hrs?|days?|weeks?|months?|minutes?|mins?|seconds?|secs?|ms\b"
    r"|conversations?|sessions?|users?|customers?|tickets?|orders?|calls?|requests?|cases?|advertisers?|bookings?))",
    re.IGNORECASE)
RULE = re.compile(r"^\s*(?:-{3,}|\*{3,}|_{3,})\s*$")
# Wording Google's customer co-branding guidelines (April 2026) and trademark rules do not allow.
BANNED_WORDING = (
    (re.compile(r"\bGCP\b"), "GCP (write Google Cloud in full)"),
    (re.compile(r"\bpowered by google", re.IGNORECASE), "'powered by Google' (reserved for co-engineering; needs brand approval)"),
    (re.compile(r"\bwith google cloud ai\b", re.IGNORECASE), "'with Google Cloud AI' (use 'Built with AI from Google Cloud')"),
    (re.compile(r"\b(?:a )?partner of google cloud\b", re.IGNORECASE), "'partner of Google Cloud' (only with a partner agreement, in its wording)"),
    (re.compile(r"\bpreferred by google\b", re.IGNORECASE), "'preferred by Google' (not an approved claim)"),
    (re.compile(r"\bgoogle cloud solution\b", re.IGNORECASE), "'<Company> Google Cloud solution' (do not combine the names)"),
)
TITLE = re.compile(r"^\s*##\s+(.+?)\s*$")


class InputError(Exception):
    pass


def parse_front_matter(text: str) -> tuple[dict[str, str], str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise InputError("deck must begin with front matter delimited by --- lines")
    end = next((index for index in range(1, len(lines)) if lines[index].strip() == "---"), None)
    if end is None:
        raise InputError("front matter has no closing --- line")
    meta = {}
    for raw in lines[1:end]:
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        key, separator, value = raw.partition(":")
        if not separator:
            raise InputError(f"front matter line is not key: value: {raw.strip()!r}")
        meta[key.strip().lower()] = value.strip().strip("'\"")
    return meta, "\n".join(lines[end + 1:])


def split_slides(body: str) -> list[tuple[int, list[str]]]:
    """Return (first line number within body, lines) per slide, split on horizontal rules outside code fences."""
    slides, current, start, in_fence = [], [], 1, False
    for number, line in enumerate(body.splitlines(), start=1):
        if line.strip().startswith("```"):
            in_fence = not in_fence
        if not in_fence and RULE.match(line):
            if any(part.strip() for part in current):
                slides.append((start, current))
            current, start = [], number + 1
            continue
        current.append(line)
    if any(part.strip() for part in current):
        slides.append((start, current))
    return slides


def tagged_line(lines: list[str], tag: str) -> str | None:
    pattern = re.compile(r"^\s*(?:\*\*)?" + tag + r"(?:\*\*)?\s*:\s*(.*)$", re.IGNORECASE)
    for line in lines:
        match = pattern.match(line)
        if match:
            return match.group(1).strip()
    return None


def notes_text(lines: list[str]) -> str | None:
    """Everything from the Notes: marker to the end of the slide, or None when there is no marker."""
    pattern = re.compile(r"^\s*(?:\*\*)?notes(?:\*\*)?\s*:\s*(.*)$", re.IGNORECASE)
    for index, line in enumerate(lines):
        match = pattern.match(line)
        if match:
            rest = [match.group(1)] + [later for later in lines[index + 1:]
                                       if not re.match(r"^\s*(?:\*\*)?(?:evidence|covers)(?:\*\*)?\s*:", later, re.IGNORECASE)]
            return " ".join(part.strip() for part in rest if part.strip())
    return None


def evidence_kind(evidence: str | None) -> str:
    """'none', 'n/a', 'cited' or 'labelled' (only a hypothesis/assumption label, no citation)."""
    if evidence is None or not evidence.strip():
        return "none"
    if NOT_APPLICABLE.match(evidence):
        return "n/a"
    if CITATION.search(evidence) or PATH_OR_URL.search(evidence):
        return "cited"
    if LABEL.search(evidence):
        return "labelled"
    return "none"


def numbers_in(lines: list[str]) -> list[str]:
    found = []
    for line in lines:
        stripped = line.strip()
        if re.match(r"^\s*(?:\*\*)?(?:evidence|covers|notes)(?:\*\*)?\s*:", stripped, re.IGNORECASE):
            continue
        scrubbed = IDENTIFIER.sub("", stripped)
        for match in NUMERIC_CLAIM.finditer(scrubbed):
            found.append(match.group(0).strip())
    return found


def check_deck(text: str) -> dict:
    meta, body = parse_front_matter(text)
    errors, warnings = [], []
    stage = meta.get("stage", "")
    audience = meta.get("audience", "")
    if stage not in STAGES:
        errors.append(f"front matter: stage must be one of {', '.join(STAGES)}, got {stage!r}")
    if audience not in AUDIENCES:
        errors.append(f"front matter: audience must be one of {', '.join(AUDIENCES)}, got {audience!r}")
    minutes = None
    try:
        minutes = int(meta.get("minutes", ""))
        if minutes <= 0:
            raise ValueError
    except ValueError:
        errors.append(f"front matter: minutes must be a positive whole number, got {meta.get('minutes')!r}")
    for key in ("decider", "date"):
        if not meta.get(key):
            warnings.append(f"front matter: no {key}; name who decides and when")
    slides = split_slides(body)
    if not slides:
        errors.append("deck has no slides")
    covered = set()
    report_slides = []
    timed_slides = 0
    spoken_words = 0
    for position, (line_number, lines) in enumerate(slides, start=1):
        first = next((line for line in lines if line.strip()), "")
        match = TITLE.match(first)
        title = match.group(1) if match else ""
        where = f"slide {position} (line {line_number}{', ' + title if title else ''})"
        if not match:
            errors.append(f"{where}: must open with an action title line '## <claim>'")
        else:
            words = re.findall(r"[\w'-]+", title)
            if title.lower().strip(" .:") in GENERIC_TITLES or (position > 1 and len(words) < 5) or title.endswith(":"):
                warnings.append(f"{where}: title is a label, not a claim; say what the slide proves")
        covers = tagged_line(lines, "covers")
        tags = [tag.strip().lower() for tag in covers.split(",")] if covers else []
        for tag in tags:
            if tag and tag not in ALL_TAGS:
                warnings.append(f"{where}: unknown Covers tag {tag!r}; known tags: {', '.join(ALL_TAGS)}")
        covered.update(tag for tag in tags if tag)
        evidence = tagged_line(lines, "evidence")
        kind = evidence_kind(evidence)
        numbers = numbers_in(lines)
        if kind == "none":
            if position == 1 and "title" in tags:
                pass
            elif evidence is None:
                errors.append(f"{where}: no Evidence line")
            else:
                errors.append(f"{where}: Evidence cites nothing; use a goal or acceptance ID, contract or "
                              f"decision ID, path, URL, or the label hypothesis, assumption, measured or n/a: <why>")
        if numbers and kind in ("none", "n/a"):
            errors.append(f"{where}: numbers without evidence: {', '.join(numbers[:4])}")
        elif numbers and kind == "labelled":
            warnings.append(f"{where}: numbers on a hypothesis or assumption slide; the title must read as expected, not measured")
        notes = notes_text(lines)
        if notes is None and not (position == 1 and "title" in tags):
            warnings.append(f"{where}: no speaker Notes")
        if not (set(tags) & UNTIMED):
            timed_slides += 1
        spoken_words += len(notes.split()) if notes else 0
        report_slides.append({"position": position, "line": line_number, "title": title, "covers": tags,
                              "evidence": kind, "numbers": numbers})
    if stage == "case-study":
        for pattern, why in BANNED_WORDING:
            for line_number, line in enumerate(body.splitlines(), start=1):
                if pattern.search(line):
                    errors.append(f"line {line_number}: wording not allowed in a public story: {why}")
    if stage in STAGES:
        required = list(STAGES[stage])
        if audience == "technical":
            required += list(TECHNICAL[stage])
        missing = [tag for tag in required if tag not in covered]
        if missing:
            errors.append(f"coverage: no slide Covers {', '.join(missing)} (required for {stage}, {audience})")
    spoken_minutes = round(spoken_words / WORDS_PER_MINUTE, 1)
    if minutes and timed_slides:
        if timed_slides > minutes:
            warnings.append(f"timing: {timed_slides} timed slides for {minutes} minutes is more than one a minute")
        elif timed_slides * 3 < minutes:
            warnings.append(f"timing: {timed_slides} timed slides for {minutes} minutes leaves over three minutes a slide; "
                            f"check the talk is not carried by unrecorded material")
        if spoken_words and spoken_minutes > minutes * 1.1:
            warnings.append(f"timing: the notes hold {spoken_words} words, about {spoken_minutes} minutes at "
                            f"{WORDS_PER_MINUTE} a minute, for a {minutes}-minute slot")
        elif spoken_words and spoken_minutes < minutes * 0.5:
            warnings.append(f"timing: the notes hold {spoken_words} words, about {spoken_minutes} minutes at "
                            f"{WORDS_PER_MINUTE} a minute, for a {minutes}-minute slot; the rest is unscripted")
    return {"stage": stage, "audience": audience, "minutes": minutes, "slides": report_slides,
            "timed_slides": timed_slides, "spoken_words": spoken_words, "spoken_minutes": spoken_minutes,
            "covered": sorted(covered), "errors": errors, "warnings": warnings}


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--deck", type=Path, required=True, help="deck outline Markdown file")
    parser.add_argument("--json", action="store_true", help="print a JSON report instead of text")
    args = parser.parse_args(argv)
    try:
        report = check_deck(args.deck.read_text(encoding="utf-8"))
    except (OSError, UnicodeError) as exc:
        print(f"ERROR cannot read deck: {exc}", file=sys.stderr)
        return 2
    except InputError as exc:
        print(f"ERROR {exc}", file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(f"{report['stage'] or '?'} deck for a {report['audience'] or '?'} audience, "
              f"{report['minutes'] or '?'} minutes, {len(report['slides'])} slides "
              f"({report['timed_slides']} timed), notes about {report['spoken_minutes']} spoken minutes")
        for slide in report["slides"]:
            print(f"  {slide['position']:>2}. [{slide['evidence']:<8}] {slide['title'] or '(no title)'}"
                  + (f"  covers: {', '.join(slide['covers'])}" if slide["covers"] else ""))
        for message in report["errors"]:
            print(f"ERROR {message}")
        for message in report["warnings"]:
            print(f"WARNING {message}")
        if not report["errors"]:
            print("Every slide cites evidence or says why not, and the stage's coverage is complete.")
    return 1 if report["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
