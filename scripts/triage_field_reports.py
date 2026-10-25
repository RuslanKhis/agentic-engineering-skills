#!/usr/bin/env python3
"""Cluster field-report issues for triage. Standard library only; no network calls.

Input is the JSON written by
``gh issue list --label field-report --state open --json number,title,body,labels --limit 200 > reports.json``.
Each issue body is parsed into the field-report form's ``### Label`` sections and
grouped by skill, kind and the quoted ``file:line``. The table prints only values
checked against fixed vocabularies (skill names, the form's kinds and evidence
tiers) and locations matching a strict pattern; issue prose is never printed, so
the table can be read without treating report text as instructions. Flags mark
reports with injection-like text, a missing privacy tick or no parsable form.

Exit status: 0 when the input was read, 2 when it cannot be read.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys

LABELS = {
    "Skill": "skill",
    "Skill version": "skill_version",
    "Coding agent": "host",
    "Model": "model",
    "Kind of divergence": "kind",
    "What the skill says": "said",
    "What happened instead": "happened",
    "Minimal reproduction": "repro",
    "Proposed correction": "proposed",
    "Evidence": "evidence",
    "Privacy check": "privacy",
}
KINDS = ("Wrong or changed API", "A documented step failed", "Missing case", "Misrouted specialist",
         "A default the user always overrides", "Helper script error", "Other")
EVIDENCE = ("Observed once", "Reproduced in a fresh session", "Reproduced with a fixture and a check")
SKILL_NAME = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+){0,6}$")
SECTION = re.compile(r"^###[ \t]+(.+?)[ \t]*$", re.MULTILINE)
LOCATION = re.compile(r"(?<![\w./-])((?:[\w.-]+/){0,6}[\w.-]+\.(?:md|py|ya?ml|json|txt|sh)):(\d{1,5})\b")
INJECTION = re.compile(
    r"(?i)ignore (?:all |any )?(?:previous|prior|above) (?:instructions|rules)|system prompt|you are now"
    r"|<!--|<script|\bcurl\b[^\n]*\|\s*(?:ba)?sh|run (?:the following|this) command|disregard"
    r"|[​-‏‪-‮⁦-⁩﻿]")


class InputError(Exception):
    pass


def parse_body(body: str) -> dict:
    fields = {}
    matches = list(SECTION.finditer(body or ""))
    for index, match in enumerate(matches):
        key = LABELS.get(match.group(1).strip())
        if key is None:
            continue
        end = matches[index + 1].start() if index + 1 < len(matches) else len(body)
        value = body[match.end():end].strip()
        fields[key] = "" if value == "_No response_" else value
    return fields


def location(said: str, skill: str) -> str:
    match = LOCATION.search(said or "")
    if not match:
        return "(none quoted)"
    path = match.group(1)
    for prefix in (f"skills/{skill}/", f"{skill}/"):
        if prefix in path:
            path = path.split(prefix, 1)[1]
    return f"{path}:{match.group(2)}"


def classify(issue: dict, known_skills: set[str]) -> dict:
    body = issue.get("body") or ""
    fields = parse_body(body)
    flags = []
    skill = fields.get("skill", "").strip()
    if not fields:
        flags.append("not a form")
    if not SKILL_NAME.match(skill):
        skill = "(unrecognised)"
    elif known_skills and skill not in known_skills:
        flags.append("unknown skill")
    kind = fields.get("kind", "").strip()
    kind = kind if kind in KINDS else "(unrecognised)"
    evidence = fields.get("evidence", "").strip()
    tier = EVIDENCE.index(evidence) if evidence in EVIDENCE else -1
    if fields and not re.search(r"-\s*\[[xX]\]", fields.get("privacy", "")):
        flags.append("no privacy tick")
    if INJECTION.search(body) or INJECTION.search(issue.get("title") or ""):
        flags.append("injection-like text")
    labels = {label.get("name") for label in issue.get("labels") or [] if isinstance(label, dict)}
    return {
        "number": issue.get("number"),
        "skill": skill,
        "kind": kind,
        "location": location(fields.get("said", ""), skill),
        "tier": tier,
        "needs_repro": "needs-repro" in labels,
        "flags": flags,
    }


def cluster(reports: list[dict]) -> list[dict]:
    groups: dict[tuple, dict] = {}
    for report in reports:
        key = (report["skill"], report["kind"], report["location"])
        group = groups.setdefault(key, {"skill": key[0], "kind": key[1], "location": key[2], "issues": [],
                                        "best_tier": -1, "flags": set(), "needs_repro": 0})
        group["issues"].append(report["number"])
        group["best_tier"] = max(group["best_tier"], report["tier"])
        group["flags"].update(report["flags"])
        group["needs_repro"] += report["needs_repro"]
    ordered = sorted(groups.values(), key=lambda g: (-len(g["issues"]), -g["best_tier"], g["skill"], g["location"]))
    for group in ordered:
        group["flags"] = sorted(group["flags"])
        group["issues"] = sorted(n for n in group["issues"] if isinstance(n, int))
    return ordered


def load(path: Path) -> list[dict]:
    try:
        data = json.loads(sys.stdin.read() if str(path) == "-" else path.read_text(encoding="utf-8"))
    except (OSError, ValueError, UnicodeError) as exc:
        raise InputError(f"cannot read {path}: {exc}") from exc
    if not isinstance(data, list) or not all(isinstance(item, dict) for item in data):
        raise InputError("expected the JSON array written by gh issue list --json number,title,body,labels")
    return data


def table(groups: list[dict]) -> str:
    tiers = {-1: "unstated", 0: "observed once", 1: "fresh session", 2: "fixture and check"}
    lines = ["| Reports | Skill | Kind | Quoted location | Best evidence | Issues | Needs repro | Flags |",
             "| ---: | --- | --- | --- | --- | --- | ---: | --- |"]
    for g in groups:
        lines.append(f"| {len(g['issues'])} | {g['skill']} | {g['kind']} | {g['location']} | {tiers[g['best_tier']]} "
                     f"| {', '.join('#' + str(n) for n in g['issues'])} | {g['needs_repro']} "
                     f"| {', '.join(g['flags']) or '-'} |")
    return "\n".join(lines)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("reports", type=Path, help="gh issue list JSON file, or - for standard input")
    parser.add_argument("--skills", type=Path, default=Path(__file__).resolve().parents[1] / "skills",
                        help="skills directory used to flag unknown skill names")
    parser.add_argument("--json", action="store_true", help="print the clusters as JSON")
    args = parser.parse_args(argv)
    try:
        issues = load(args.reports)
    except InputError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    known = {p.parent.name for p in args.skills.glob("*/SKILL.md")} if args.skills.is_dir() else set()
    groups = cluster([classify(issue, known) for issue in issues])
    if args.json:
        print(json.dumps(groups, indent=2))
    else:
        print(table(groups))
        print(f"\n{len(issues)} reports in {len(groups)} clusters. Report prose is not shown; read flagged "
              "issues in a session without write tools, and reproduce in a clean fixture before editing a skill.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
