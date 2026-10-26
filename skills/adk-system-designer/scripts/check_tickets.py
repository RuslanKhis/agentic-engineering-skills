#!/usr/bin/env python3
"""Lint ticket files before anyone carries them out. Standard library only; reads Markdown, never runs project code.

Run after writing tickets from the ticket template. Errors (exit 1):

- a required front-matter field is missing or a ``<placeholder>`` is left
  outside the Evidence section;
- the status is not in the template's vocabulary;
- the design or plan path does not exist;
- a contract or security rule ID is not in the design's tables;
- an acceptance item cites no contract, rule or ``(floor)``, or a ticket
  contract is cited by no acceptance item; a ticket whose ``type`` is
  portability may instead tag an item ``(deliverable)``, since it proves a
  separate document rather than a contract, and the tag on any other type is
  the same error;
- a primary or supporting skill is not an installed sibling skill (Google
  product skills, ``google/skills:<name>``, are checked against the
  implementation handoff's dated table and only warned about);
- a ``docs`` path does not resolve under the installed skills;
- a ``pass_to_pass`` item (``G01/A2``) names a goal or acceptance item that
  does not exist;
- a ``blocked_by`` goal ID has no ticket and is not in the plan;
- ``parallel_safe: yes`` while another ticket of the same phase writes one of
  its ``touches``.

Warnings (exit 0): a companion skill without a pinned row in AGENTS.md or the
plan's companion table, an unknown Google product skill, and a ticket whose
named skills and docs add up to more than the context budget or name more
supporting skills than the limit. Exit status 2 when the input cannot be read.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys

from check_schedule import InputError, read_plan
from plan_files import (STATUSES, design_contracts, design_rules, read_tickets, split_list, touches_overlap)

REQUIRED = ("goal", "title", "design", "plan", "primary_skill", "blocked_by", "touches", "contracts", "phase",
            "profile", "estimate", "status")
PLACEHOLDER = re.compile(r"<(?!!--)(?:[A-Za-z][^<>\n]{1,80})>")
PIN = re.compile(r"@\S*\d|\bv?\d+\.\d+|\b[0-9a-f]{7,40}\b|\bpin(?:ned)?\b\s*[:=]?\s*\S+", re.IGNORECASE)
GOAL_REF = re.compile(r"^([A-Z]+\d+)/A(\d+)$")
CHARS_PER_TOKEN = 4
DOCUMENT_TYPES = ("portability",)


def skill_name(entry: str) -> str:
    """``adk-agent-security (threat model)`` -> ``adk-agent-security``."""
    return re.split(r"\s*\(", entry, maxsplit=1)[0].strip().strip("`")


def known_google_skills(skills_dir: Path) -> set[str]:
    handoff = skills_dir / "adk-system-designer" / "references" / "implementation-handoff.md"
    if not handoff.is_file():
        return set()
    text = handoff.read_text(encoding="utf-8")
    table = text.split("google/skills` name(s) |", 1)[-1].split("\n\n", 1)[0]
    return {n for n in re.findall(r"`([a-z0-9][a-z0-9-]+)`", table)}


def companion_rows(paths: list[Path]) -> list[str]:
    rows = []
    for path in paths:
        if path and path.is_file():
            rows += [l for l in path.read_text(encoding="utf-8").splitlines() if l.strip().startswith("|")]
    return rows


def outside_evidence(ticket: dict) -> str:
    body = ticket["body"]
    marker = re.search(r"(?m)^##\s+Evidence\s*$", body)
    if marker:
        rest = body[marker.end():]
        following = re.search(r"(?m)^##\s+", rest)
        body = body[:marker.start()] + (rest[following.start():] if following else "")
    front = "\n".join(f"{k}: {v}" for k, v in ticket["fields"].items() if not isinstance(v, dict))
    nested = "\n".join(f"{k}: {v}" for d in ticket["fields"].values() if isinstance(d, dict) for k, v in d.items())
    return "\n".join([front, nested, body])


def lint(tickets: list[dict], root: Path, skills_dir: Path, design: Path | None, plan: Path | None,
         agents: Path | None, budget: int, max_supporting: int) -> tuple[list[str], list[str], dict]:
    errors, warnings, budgets = [], [], {}
    installed = {p.parent.name for p in skills_dir.glob("*/SKILL.md")}
    google = known_google_skills(skills_dir)
    by_goal = {t["goal"]: t for t in tickets}
    plan_ids = set()
    plan_path = plan or next((root / t["fields"]["plan"] for t in tickets if t["fields"].get("plan")), None)
    if plan_path and plan_path.is_file():
        try:
            plan_ids = {g["goal"] for g in read_plan(plan_path)}
        except InputError as exc:
            warnings.append(f"plan schedule not read: {exc}")
    design_path = design or next((root / t["fields"]["design"] for t in tickets if t["fields"].get("design")), None)
    contracts = design_contracts(design_path) if design_path and design_path.is_file() else {}
    rules = design_rules(design_path) if design_path and design_path.is_file() else {}
    agents_path = agents or next((p / "AGENTS.md" for p in [root, *root.parents] if (p / "AGENTS.md").is_file()), None)
    companions = companion_rows([agents_path, plan_path])
    for ticket in tickets:
        name, fields = ticket["file"].name, ticket["fields"]
        for field in REQUIRED:
            value = fields.get(field)
            if value is None or (isinstance(value, str) and not value.strip()):
                errors.append(f"{name}: missing {field}")
        for match in sorted(set(PLACEHOLDER.findall(outside_evidence(ticket)))):
            errors.append(f"{name}: unfilled placeholder {match}")
        if ticket["status"] and ticket["status"] not in STATUSES:
            errors.append(f"{name}: status {ticket['status']!r} is not one of {', '.join(STATUSES)}")
        for field in ("design", "plan"):
            value = fields.get(field)
            if isinstance(value, str) and value.strip() and not PLACEHOLDER.search(value) \
                    and not (root / value.strip()).is_file():
                errors.append(f"{name}: {field} {value!r} does not exist from {root}")
        if contracts:
            errors += [f"{name}: contract {c} is not in the design's contracts table"
                       for c in ticket["contracts"] if c not in contracts]
        if rules:
            errors += [f"{name}: security rule {r} is not in the design's security baseline table"
                       for r in ticket["security"] if r not in rules]
        cited = set()
        document = ticket["type"] in DOCUMENT_TYPES
        for item, data in ticket["acceptance"].items():
            ids = set(re.findall(r"(?<![\w/-])(?:C|SB)\d+(?![\w/-])", data["text"]))
            if not ids and "(floor)" not in data["text"] and not (document and "(deliverable)" in data["text"]):
                if document:
                    errors.append(f"{name}: acceptance {item} cites no contract, security rule, (floor) or "
                                  "(deliverable)")
                else:
                    errors.append(f"{name}: acceptance {item} cites no contract, security rule or (floor)"
                                  + ("; (deliverable) only on a portability ticket"
                                     if "(deliverable)" in data["text"] else ""))
            cited |= ids
        if not ticket["acceptance"]:
            errors.append(f"{name}: no acceptance items (- [ ] A1 ...)")
        errors += [f"{name}: contract {c} is cited by no acceptance item" for c in ticket["contracts"]
                   if c not in cited]
        errors += [f"{name}: security rule {r} is cited by no acceptance item" for r in ticket["security"]
                   if r not in cited]
        primary = skill_name(fields.get("primary_skill", "") or "")
        supporting = [skill_name(s) for s in split_list(fields.get("supporting_skills", "") or "")]
        loaded = []
        for skill in ([primary] if primary else []) + supporting:
            if skill.startswith("google/skills:"):
                product = skill.split(":", 1)[1]
                if google and product not in google:
                    warnings.append(f"{name}: {skill} is not in the implementation handoff's dated table; confirm "
                                    "it in Google's current catalogue")
            elif "/" in skill or ":" in skill:
                continue  # another collection's skill; the engineer reports it as setup when missing
            elif skill not in installed:
                errors.append(f"{name}: skill {skill!r} is not an installed skill (siblings in {skills_dir})")
            else:
                loaded.append(skills_dir / skill / "SKILL.md")
        if len([s for s in supporting if not s.startswith("google/skills:")]) > max_supporting:
            warnings.append(f"{name}: {len(supporting)} supporting skills; name only those this slice's boundaries "
                            f"need (limit {max_supporting})")
        for doc in split_list(fields.get("docs", "") or ""):
            path = skills_dir / doc.strip("`")
            if not path.is_file():
                errors.append(f"{name}: docs path {doc!r} does not resolve under {skills_dir}")
            else:
                loaded.append(path)
        tokens = sum(p.stat().st_size for p in loaded) // CHARS_PER_TOKEN
        budgets[ticket["goal"]] = tokens
        if tokens > budget:
            warnings.append(f"{name}: its skills and docs come to about {tokens} tokens before any code is read "
                            f"(budget {budget}); move a supporting skill or reference to a sibling ticket, or "
                            "drop docs the acceptance does not need")
        for companion in split_list(fields.get("companion_skills", "") or ""):
            label = skill_name(companion)
            rows = [r for r in companions if re.search(rf"(?<![\w-]){re.escape(label)}(?![\w-])", r)]
            if not companions:
                warnings.append(f"{name}: companion {label} named but no AGENTS.md or plan companion table was "
                                "found; the first goal writes it")
            elif not rows:
                warnings.append(f"{name}: companion {label} has no row in AGENTS.md or the plan's companion table")
            elif not any(PIN.search(r.split(label, 1)[-1]) for r in rows):
                warnings.append(f"{name}: companion {label} has a row but no pin")
        for ref in split_list(fields.get("pass_to_pass", "") or ""):
            match = GOAL_REF.match(ref.strip())
            if not match:
                continue  # an existing test id
            goal, item = match.group(1), f"A{match.group(2)}"
            if goal not in by_goal and goal not in plan_ids:
                errors.append(f"{name}: pass_to_pass {ref} names goal {goal}, which has no ticket or plan entry")
            elif goal in by_goal and item not in by_goal[goal]["acceptance"]:
                errors.append(f"{name}: pass_to_pass {ref}: {goal} has no acceptance item {item}")
        for blocker in ticket["blocked_by"]:
            if re.fullmatch(r"G\d+", blocker) and blocker not in by_goal and blocker not in plan_ids:
                errors.append(f"{name}: blocked_by {blocker} has no ticket and is not in the plan")
        if str(fields.get("parallel_safe", "")).strip().lower() == "yes":
            for other in tickets:
                if other is ticket or other["phase"] != ticket["phase"]:
                    continue
                shared = touches_overlap(ticket["touches"], other["touches"])
                if shared:
                    errors.append(f"{name}: parallel_safe is yes but {other['file'].name} also writes "
                                  f"{', '.join(shared)}")
    return errors, warnings, budgets


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--tickets", type=Path, required=True, help="directory of ticket files")
    parser.add_argument("--root", type=Path, default=Path.cwd(),
                        help="repository root the tickets' design and plan paths start from (default: cwd)")
    parser.add_argument("--design", type=Path, help="design Markdown (default: the tickets' design field)")
    parser.add_argument("--plan", type=Path, help="plan Markdown (default: the tickets' plan field)")
    parser.add_argument("--agents", type=Path, help="AGENTS.md with the companion table (default: found upwards)")
    parser.add_argument("--skills-dir", type=Path, default=Path(__file__).resolve().parents[2],
                        help="directory holding the installed skills (default: this skill's siblings)")
    parser.add_argument("--budget", type=int, default=30000,
                        help="approximate tokens of named skills and docs per ticket before a warning (default 30000)")
    parser.add_argument("--max-supporting", type=int, default=3, help="supporting skills before a warning (default 3)")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    try:
        tickets = read_tickets(args.tickets)
        if not tickets:
            raise InputError(f"{args.tickets}: no ticket files with a goal in their front matter")
        errors, warnings, budgets = lint(tickets, args.root.resolve(), args.skills_dir.resolve(), args.design,
                                         args.plan, args.agents, args.budget, args.max_supporting)
    except (InputError, OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps({"errors": errors, "warnings": warnings, "tokens_per_ticket": budgets}, indent=1))
    else:
        print(f"Checked {len(tickets)} tickets: {len(errors)} errors, {len(warnings)} warnings")
        print("Approximate tokens of named skills and docs: "
              + ", ".join(f"{g} {n}" for g, n in sorted(budgets.items())))
        for warning in warnings:
            print(f"WARNING: {warning}")
        for error in errors:
            print(f"ERROR: {error}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
