#!/usr/bin/env python3
"""Check that skill descriptions draw routing boundaries from both sides.

A host picks a skill from its name and description alone. When one skill's
"Do not activate" clause names another skill, a request that belongs to the
named skill can still land on it unless the named skill's own description
names the first one back. This check requires that reciprocal mention, or an
entry in the one-way allowlist (scripts/boundary_allowlist.json) saying why
the named skill has no reason to name it back. It also requires every skill
not listed in that file's ``no_clause`` to have an exclusion clause, and warns
when a description passes the headroom limit below the 1024-character cap.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys

import yaml

WARN_LENGTH = 950
CLAUSE = re.compile(r"\bDo not activate\b", re.IGNORECASE)
ALLOWLIST = Path("scripts/boundary_allowlist.json")


def read_descriptions(root: Path) -> dict[str, str]:
    """Map each skill directory name to its frontmatter description."""
    result: dict[str, str] = {}
    for path in sorted((root / "skills").glob("*/SKILL.md")):
        parts = path.read_text(encoding="utf-8").split("\n---", 1)
        frontmatter = parts[0].removeprefix("---\n")
        data = yaml.safe_load(frontmatter) if len(parts) == 2 else None
        description = data.get("description") if isinstance(data, dict) else None
        result[path.parent.name] = description if isinstance(description, str) else ""
    return result


def excluded(description: str, names: list[str], own: str) -> set[str]:
    """Skills named after the first "Do not activate" in a description."""
    match = CLAUSE.search(description)
    if not match:
        return set()
    clause = description[match.start():]
    return {name for name in names if name != own and
            re.search(rf"(?<![\w-]){re.escape(name)}(?![\w-])", clause)}


def load_allowlist(path: Path) -> tuple[set[tuple[str, str]], set[str], list[str]]:
    errors: list[str] = []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        return set(), set(), [f"{path.name}: {exc}"]
    pairs: set[tuple[str, str]] = set()
    entries = data.get("one_way") if isinstance(data, dict) else None
    no_clause = data.get("no_clause", []) if isinstance(data, dict) else None
    if not isinstance(entries, list) or not isinstance(no_clause, list):
        return set(), set(), [f"{path.name}: expected one_way and no_clause lists"]
    for entry in entries:
        if (not isinstance(entry, dict) or not all(
                isinstance(entry.get(k), str) and entry[k].strip() for k in ("from", "to", "reason"))):
            errors.append(f"{path.name}: each one_way entry needs from, to and reason")
            continue
        pair = (entry["from"], entry["to"])
        if pair in pairs:
            errors.append(f"{path.name}: duplicate one_way entry {pair[0]} -> {pair[1]}")
        pairs.add(pair)
    return pairs, {n for n in no_clause if isinstance(n, str)}, errors


def check(root: Path, allowlist: Path | None = None) -> tuple[list[str], list[str]]:
    """Return (errors, warnings) for the repository at root."""
    descriptions = read_descriptions(root)
    names = sorted(descriptions)
    pairs, no_clause, errors = load_allowlist(allowlist or root / ALLOWLIST)
    warnings: list[str] = []
    for skill in sorted({s for pair in pairs for s in pair} | no_clause):
        if skill not in descriptions:
            errors.append(f"allowlist names unknown skill {skill}")
    named = {name: excluded(text, names, name) for name, text in descriptions.items()}
    for name, text in descriptions.items():
        if len(text) > WARN_LENGTH:
            warnings.append(f"{name}: description is {len(text)} characters "
                            f"(over {WARN_LENGTH}; the cap is 1024)")
        if name not in no_clause and not CLAUSE.search(text):
            errors.append(f"{name}: description has no \"Do not activate\" clause")
        for other in sorted(named[name]):
            reciprocal = name in named.get(other, set())
            if not reciprocal and (name, other) not in pairs:
                errors.append(f"{name} excludes {other}, but {other} does not name {name} back "
                              f"(add a reciprocal exclusion or a one_way allowlist entry)")
    for source, target in sorted(pairs):
        if source in named and target not in named[source]:
            errors.append(f"stale allowlist entry {source} -> {target}: {source} no longer names it")
        elif target in named and source in named[target]:
            errors.append(f"stale allowlist entry {source} -> {target}: the exclusion is now reciprocal")
    for name in sorted(no_clause & set(descriptions)):
        if CLAUSE.search(descriptions[name]):
            errors.append(f"stale no_clause entry {name}: it now has a \"Do not activate\" clause")
    return errors, warnings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args(argv)
    errors, warnings = check(args.root.resolve())
    for line in warnings:
        print(f"WARNING: {line}")
    for line in errors:
        print(f"ERROR: {line}", file=sys.stderr)
    if errors:
        return 1
    print("Skill boundaries are reciprocal or allowlisted.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
