"""Regression checks for reciprocal routing exclusions between skill descriptions."""

import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts/check_boundaries.py"
spec = importlib.util.spec_from_file_location("check_boundaries", SCRIPT)
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)


class CheckBoundariesTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.root = Path(self.directory.name)
        (self.root / "scripts").mkdir()
        self.allow({"one_way": [], "no_clause": []})

    def tearDown(self):
        self.directory.cleanup()

    def skill(self, name, description):
        folder = self.root / "skills" / name
        folder.mkdir(parents=True, exist_ok=True)
        (folder / "SKILL.md").write_text(
            f"---\nname: {name}\ndescription: >-\n  {description}\n---\n\nBody\n", encoding="utf-8")

    def allow(self, data):
        (self.root / "scripts/boundary_allowlist.json").write_text(json.dumps(data), encoding="utf-8")

    def test_reciprocal_exclusions_pass(self):
        self.skill("alpha-skill", "Do alpha. Do not activate for beta work (beta-skill).")
        self.skill("beta-skill", "Do beta. Do not activate for alpha work (alpha-skill).")
        self.assertEqual(checker.check(self.root), ([], []))

    def test_one_sided_exclusion_fails(self):
        self.skill("alpha-skill", "Do alpha. Do not activate for beta work (beta-skill).")
        self.skill("beta-skill", "Do beta. Do not activate for unrelated work.")
        errors, _ = checker.check(self.root)
        self.assertEqual(len(errors), 1)
        self.assertIn("alpha-skill excludes beta-skill", errors[0])

    def test_allowlisted_one_way_exclusion_passes(self):
        self.skill("alpha-skill", "Do alpha. Do not activate for beta work (beta-skill).")
        self.skill("beta-skill", "Do beta. Do not activate for unrelated work.")
        self.allow({"no_clause": [], "one_way": [
            {"from": "alpha-skill", "to": "beta-skill", "reason": "beta never draws alpha requests"}]})
        self.assertEqual(checker.check(self.root)[0], [])

    def test_mentions_before_the_clause_do_not_count(self):
        self.skill("alpha-skill", "Hands off to beta-skill when done. Do not activate for unrelated work.")
        self.skill("beta-skill", "Do beta. Do not activate for unrelated work.")
        self.assertEqual(checker.check(self.root)[0], [])

    def test_name_inside_a_longer_name_is_not_a_mention(self):
        self.skill("beta", "Do beta. Do not activate for unrelated work.")
        self.skill("alpha-skill", "Do alpha. Do not activate for beta-skill-like work or x-beta tools.")
        self.assertEqual(checker.check(self.root)[0], [])

    def test_missing_clause_fails_unless_listed(self):
        self.skill("router-skill", "Pick the right specialist.")
        errors, _ = checker.check(self.root)
        self.assertIn("router-skill: description has no", errors[0])
        self.allow({"one_way": [], "no_clause": ["router-skill"]})
        self.assertEqual(checker.check(self.root)[0], [])

    def test_stale_and_unknown_allowlist_entries_fail(self):
        self.skill("alpha-skill", "Do alpha. Do not activate for beta work (beta-skill).")
        self.skill("beta-skill", "Do beta. Do not activate for alpha work (alpha-skill).")
        self.allow({"no_clause": ["beta-skill"], "one_way": [
            {"from": "alpha-skill", "to": "beta-skill", "reason": "now reciprocal"},
            {"from": "beta-skill", "to": "gamma-skill", "reason": "unknown skill"}]})
        errors = "\n".join(checker.check(self.root)[0])
        self.assertIn("unknown skill gamma-skill", errors)
        self.assertIn("now reciprocal", errors)
        self.assertIn("stale no_clause entry beta-skill", errors)

    def test_long_description_warns(self):
        self.skill("alpha-skill", "Do alpha " * 110 + "Do not activate for unrelated work.")
        errors, warnings = checker.check(self.root)
        self.assertEqual(errors, [])
        self.assertEqual(len(warnings), 1)
        self.assertIn("over 950", warnings[0])

    def test_malformed_allowlist_fails(self):
        self.skill("alpha-skill", "Do alpha. Do not activate for unrelated work.")
        self.allow({"one_way": [{"from": "alpha-skill"}], "no_clause": []})
        self.assertIn("needs from, to and reason", checker.check(self.root)[0][0])


if __name__ == "__main__":
    unittest.main()
