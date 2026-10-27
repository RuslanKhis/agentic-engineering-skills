"""Scenario fixtures are blind, composable and, where they carry tests, runnable offline.

Everything under evals/fixtures/ is copied into an agent's workspace, and a
scenario's context is shown to the agent verbatim. Neither may carry the
answer: no planted-defect comments, no grader paths, no copies of grader,
trial or skill-package files (a skill's own worked example is visible to the
agent through the installed skill). Each base must be used and each overlay
must belong to a scenario that lists it. A composed workspace whose entry
declares ``"tests": "pass"`` must pass its own unittest suite with the
standard library only; ``"tests": "fail"`` marks a fixture whose suite fails
on purpose (the scenario asks the agent to fix it).
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "evals" / "fixtures"
BASES = FIXTURES / "base"

spec = importlib.util.spec_from_file_location("run_scenarios_for_fixtures", ROOT / "scripts/run_scenarios.py")
scen = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = scen
spec.loader.exec_module(scen)

# Words that mark a fixture as staged or point at the answer. A real project
# does not label its own defects, so none of these belongs in a workspace.
LEAK_PATTERNS = [
    re.compile(r"\bplanted\b", re.IGNORECASE),
    re.compile(r"#\s*(BUG|FIXME|XXX)\b"),
    re.compile(r"\bgrader", re.IGNORECASE),
    re.compile(r"evals/", re.IGNORECASE),
    re.compile(r"expected[_ ]primary", re.IGNORECASE),
    re.compile(r"answer key", re.IGNORECASE),
    re.compile(r"\bdeliberate(ly)?\s+(bug|defect|broken|wrong|missing|omitted|flaw)", re.IGNORECASE),
    re.compile(r"\bthe (agent|model) (should|must) (find|notice|spot|flag)", re.IGNORECASE),
]
# Contexts are the situation as the person asking would state it.
CONTEXT_LEAKS = [
    re.compile(r"\bgrader", re.IGNORECASE),
    re.compile(r"evals/", re.IGNORECASE),
    re.compile(r"fixture_meanings"),
    re.compile(r"^\s*Supply\b"),
]
# Copies from a skill package predate the overlays; the agent can read these
# files in the installed skill anyway, and they carry inputs, not answers.
SKILL_COPY_ALLOWED = {
    "memory-local-document-completeness": "document-coverage.json is the retriever's input observations",
    "memory-retrieval-second-round": "retrieval-gold.json is the gold set the user asks recall on",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fixture_entries() -> dict:
    return json.loads((ROOT / "evals" / "scenario-fixtures.json").read_text(encoding="utf-8"))["scenarios"]


def scenarios() -> dict:
    return {c["id"]: c for c in json.loads((ROOT / "evals" / "scenarios.json").read_text())["cases"]}


def fixture_files() -> list[Path]:
    return [p for p in FIXTURES.rglob("*") if p.is_file() and "__pycache__" not in p.parts] \
        if FIXTURES.is_dir() else []


class LayoutTests(unittest.TestCase):
    def test_every_overlay_belongs_to_a_scenario_that_lists_it(self):
        entries, cases = fixture_entries(), scenarios()
        for folder in sorted(p for p in FIXTURES.iterdir() if p.is_dir() and p.name != "base") \
                if FIXTURES.is_dir() else []:
            with self.subTest(overlay=folder.name):
                self.assertIn(folder.name, cases, "overlay names no scenario")
                self.assertTrue(entries.get(folder.name, {}).get("overlay"),
                                "scenario-fixtures.json does not list this overlay")

    def test_every_base_is_used_and_every_named_base_exists(self):
        used = {name for entry in fixture_entries().values() for name in entry.get("base", [])}
        present = {p.name for p in BASES.iterdir() if p.is_dir()} if BASES.is_dir() else set()
        self.assertEqual(sorted(present - used), [], "unused base")
        self.assertEqual(sorted(used - present), [], "missing base")

    def test_not_representable_entries_give_a_reason_and_build_nothing(self):
        for cid, entry in fixture_entries().items():
            if entry["status"] == "not-representable":
                with self.subTest(scenario=cid):
                    self.assertTrue(entry.get("reason"))
                    self.assertFalse(entry.get("copy") or entry.get("base") or entry.get("overlay"))


class BlindnessTests(unittest.TestCase):
    def test_fixture_files_carry_no_leak_markers(self):
        offenders = []
        for path in fixture_files():
            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            for pattern in LEAK_PATTERNS:
                match = pattern.search(text)
                if match:
                    offenders.append(f"{path.relative_to(ROOT)}: {match.group(0)!r}")
        self.assertEqual(offenders, [])

    def test_fixture_files_copy_no_grader_trial_or_skill_file(self):
        protected = {}
        for base in (ROOT / "evals" / "graders", ROOT / "evals" / "trials", ROOT / "skills"):
            for path in base.rglob("*"):
                if path.is_file() and path.stat().st_size > 64 and "__pycache__" not in path.parts:
                    protected[sha256(path)] = path.relative_to(ROOT).as_posix()
        grader_names = {p.name for p in (ROOT / "evals" / "graders").rglob("*") if p.is_file()}
        offenders = []
        for path in fixture_files():
            rel = path.relative_to(ROOT).as_posix()
            if path.stat().st_size > 64 and sha256(path) in protected:
                offenders.append(f"{rel} copies {protected[sha256(path)]}")
            if path.name in grader_names:
                offenders.append(f"{rel} has the name of grader material")
        self.assertEqual(offenders, [])

    def test_runnable_contexts_name_no_grader_material_or_builder_instructions(self):
        cases, entries = scenarios(), fixture_entries()
        for cid, entry in entries.items():
            if entry["status"] in ("runnable", "repo-fixture"):
                with self.subTest(scenario=cid):
                    context = cases[cid]["context"]
                    for pattern in CONTEXT_LEAKS:
                        self.assertIsNone(pattern.search(context), pattern.pattern)

    def test_no_fixture_copies_from_a_skill_package_unless_recorded(self):
        for cid, entry in fixture_entries().items():
            for item in entry.get("copy", []):
                if item["from"].startswith("skills/"):
                    with self.subTest(scenario=cid, source=item["from"]):
                        self.assertIn(cid, SKILL_COPY_ALLOWED)


class FixtureSuiteTests(unittest.TestCase):
    def test_declared_fixture_suites_run_offline(self):
        for cid, entry in sorted(fixture_entries().items()):
            expected = entry.get("tests")
            if expected is None:
                continue
            with self.subTest(scenario=cid), tempfile.TemporaryDirectory() as tmp:
                workspace = Path(tmp) / "workspace"
                workspace.mkdir()
                scen.build_workspace(ROOT, cid, entry, workspace)
                env = {k: v for k, v in os.environ.items() if not k.startswith("PYTHON")}
                env["PYTHONDONTWRITEBYTECODE"] = "1"
                proc = subprocess.run([sys.executable, "-B", "-m", "unittest", "discover", "-s", "tests",
                                       "-t", "."], cwd=workspace, env=env, capture_output=True, text=True,
                                      timeout=120)
                ok = proc.returncode == 0
                self.assertEqual(ok, expected == "pass", proc.stderr[-2000:])


if __name__ == "__main__":
    unittest.main()
