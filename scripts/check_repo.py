#!/usr/bin/env python3
"""Run package, evaluation-fixture and offline helper checks (no model calls)."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import unittest


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def validate_cases(root: Path) -> list[str]:
    """Validate authored cases, never infer model behavior from their labels."""
    names = {p.parent.name for p in (root / "skills").glob("*/SKILL.md")}
    errors: list[str] = []
    seen: set[str] = set()
    coverage = {name: set() for name in names}
    for filename in ("activation.json", "scenarios.json"):
        try:
            data = json.loads((root / "evals" / filename).read_text(),
                              object_pairs_hook=_unique_object)
        except (OSError, ValueError) as exc:
            errors.append(f"{filename}: {exc}")
            continue
        if (not isinstance(data, dict) or type(data.get("version")) is not int
                or data["version"] != 1 or not isinstance(data.get("cases"), list)
                or not data["cases"]):
            errors.append(f"{filename}: expected version 1 and nonempty cases")
            continue
        for case in data["cases"]:
            if not isinstance(case, dict):
                errors.append(f"{filename}: case must be an object")
                continue
            cid = case.get("id")
            if not isinstance(cid, str) or not cid.strip() or cid in seen:
                errors.append(f"{filename}: missing or duplicate case id")
                continue
            seen.add(cid)
            if not isinstance(case.get("prompt"), str) or not case["prompt"].strip():
                errors.append(f"{cid}: prompt must be nonempty text")
            if filename == "activation.json":
                skill, trigger = case.get("skill"), case.get("should_trigger")
                if not isinstance(skill, str) or skill not in names or type(trigger) is not bool:
                    errors.append(f"{cid}: expected installed skill name and boolean should_trigger")
                else:
                    coverage[skill].add(trigger)
                if not isinstance(case.get("rationale"), str) or not case["rationale"].strip():
                    errors.append(f"{cid}: rationale must be nonempty text")
            else:
                primary = case.get("expected_primary")
                if "expected_primary" not in case or (primary is not None and
                        (not isinstance(primary, str) or primary not in names)):
                    errors.append(f"{cid}: expected_primary must name our skill or be null")
                for field in ("available_skills", "assertions"):
                    values = case.get(field)
                    if (not isinstance(values, list) or not values or
                            not all(isinstance(x, str) and x.strip() for x in values)):
                        errors.append(f"{cid}: {field} must contain nonempty strings")
                    elif len(values) != len(set(values)):
                        errors.append(f"{cid}: duplicate {field}")
                if not isinstance(case.get("context"), str) or not case["context"].strip():
                    errors.append(f"{cid}: context must be nonempty text")
    for name, labels in sorted(coverage.items()):
        if labels != {False, True}:
            errors.append(f"{name}: activation cases need a positive and a near-miss negative")
    return errors


def run_suite(directory: Path, pattern: str) -> int:
    """Called in a fresh process so identically named test modules cannot collide."""
    suite = unittest.TestLoader().discover(str(directory), pattern=pattern)
    if suite.countTestCases() == 0:
        print(f"ERROR: zero tests discovered in {directory}", file=sys.stderr)
        return 2
    result = unittest.TextTestRunner(verbosity=1).run(suite)
    return 0 if result.wasSuccessful() else 1


def run_command(label: str, args: list[str], root: Path) -> bool:
    print(f"\n=== {label} ===", flush=True)
    env = os.environ.copy()
    env.update(PYTHONDONTWRITEBYTECODE="1", PYTEST_DISABLE_PLUGIN_AUTOLOAD="1")
    try:
        return subprocess.run(args, cwd=root, env=env, timeout=180).returncode == 0
    except subprocess.TimeoutExpired:
        print(f"ERROR: {label} exceeded 180 seconds", file=sys.stderr)
        return False


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--suite", type=Path, help=argparse.SUPPRESS)
    parser.add_argument("--pattern", default="test_*.py", help=argparse.SUPPRESS)
    args = parser.parse_args(argv)
    if args.suite:
        return run_suite(args.suite, args.pattern)
    root = args.root.resolve()
    if not run_command("Skill packages", [sys.executable, "-B", str(root / "scripts/validate_skills.py"),
                                          "--root", str(root)], root):
        return 1
    errors = validate_cases(root)
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print("Evaluation case structure valid; model activation has not been evaluated.", flush=True)
    runner = [sys.executable, "-I", "-B", str(Path(__file__).resolve())]
    if not run_command("Repository check tests", runner + ["--suite", str(root / "tests")], root):
        return 1
    test_dirs = sorted((root / "skills").glob("*/tests"))
    if not test_dirs:
        print("ERROR: no helper test directories", file=sys.stderr)
        return 1
    for directory in test_dirs:
        name = directory.parent.name
        if name == "adk-memory-architecture":
            command = [sys.executable, "-I", "-B", "-m", "pytest", str(directory),
                       "-q", "-p", "no:cacheprovider"]
        else:
            pattern = "test_inspect_project.py" if name == "adk-workflow-design" else "test_*.py"
            command = runner + ["--suite", str(directory), "--pattern", pattern]
        if not run_command(name, command, root):
            return 1
    print("\nPackage and offline helper checks passed. Review any optional SDK skips above.")
    print("Live evaluations, cloud behavior and skill-selection quality were not tested.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
