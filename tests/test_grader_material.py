"""Grader-side material stays out of skill packages.

A scenario's expected answers, labels or generator knowledge are listed under
``grader`` in evals/scenario-fixtures.json and live in evals/graders/. Trial
oracles live in evals/trials/. Skill packages are installed where agents can
read them, so none of those files, by path, name or content, may be shipped
inside skills/.
"""

from collections import defaultdict
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
GRADERS = ROOT / "evals" / "graders"
TRIALS = ROOT / "evals" / "trials"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def skill_files() -> list[Path]:
    return [p for p in (ROOT / "skills").rglob("*")
            if p.is_file() and "__pycache__" not in p.parts]


def grader_entries() -> dict[str, list[str]]:
    data = json.loads((ROOT / "evals" / "scenario-fixtures.json").read_text(encoding="utf-8"))
    return {cid: [item["from"] for item in entry.get("grader", [])]
            for cid, entry in data["scenarios"].items()}


class GraderMaterialTests(unittest.TestCase):
    def test_listed_grader_material_exists_under_evals_graders(self):
        listed = [path for paths in grader_entries().values() for path in paths]
        self.assertTrue(listed, "scenario-fixtures.json lists no grader material")
        for path in listed:
            with self.subTest(path=path):
                self.assertTrue(path.startswith("evals/graders/"), path)
                self.assertTrue((ROOT / path).is_file(), path)

    def test_every_grader_file_is_listed_for_a_scenario(self):
        listed = {path for paths in grader_entries().values() for path in paths}
        for path in sorted(GRADERS.rglob("*")):
            if path.is_file():
                rel = path.relative_to(ROOT).as_posix()
                self.assertIn(rel, listed, f"{rel} is not listed under grader in scenario-fixtures.json")

    def test_no_skill_package_ships_grader_or_trial_material(self):
        protected = [p for base in (GRADERS, TRIALS) for p in base.rglob("*") if p.is_file()]
        self.assertTrue(protected)
        by_hash = {sha256(p): p for p in protected}
        grader_names = {p.name for p in GRADERS.rglob("*") if p.is_file()}
        offenders = defaultdict(list)
        for path in skill_files():
            rel = path.relative_to(ROOT).as_posix()
            if path.name in grader_names:
                offenders[rel].append("same name as grader material")
            match = by_hash.get(sha256(path))
            if match is not None:
                offenders[rel].append(f"same content as {match.relative_to(ROOT).as_posix()}")
        self.assertEqual(dict(offenders), {})

    def test_fixtures_never_copy_grader_material_into_a_workspace(self):
        data = json.loads((ROOT / "evals" / "scenario-fixtures.json").read_text(encoding="utf-8"))
        for cid, entry in data["scenarios"].items():
            for item in entry.get("copy", []):
                with self.subTest(scenario=cid, source=item["from"]):
                    self.assertFalse(item["from"].startswith(("evals/graders", "evals/trials")))

    def test_committed_ingestion_pack_and_inventory_match_their_generator(self):
        # The scenario has its own pack (not the memory skill's worked example); its
        # generator is grader material, and both its outputs are committed.
        script = GRADERS / "memory-ingestion-scan-detection" / "make_pack.py"
        spec = importlib.util.spec_from_file_location("make_pack", script)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        committed_pack = ROOT / "evals" / "fixtures" / "memory-ingestion-scan-detection" / "pack"
        with tempfile.TemporaryDirectory() as tmp:
            module.write_pack(Path(tmp) / "pack", Path(tmp) / "inventory.json")
            generated = (Path(tmp) / "inventory.json").read_bytes()
            pdfs = {p.name: p.read_bytes() for p in (Path(tmp) / "pack").iterdir()}
        committed = (GRADERS / "memory-ingestion-scan-detection" / "inventory.json").read_bytes()
        self.assertEqual(generated, committed)
        self.assertEqual(pdfs, {p.name: p.read_bytes() for p in committed_pack.iterdir()})


if __name__ == "__main__":
    unittest.main()
