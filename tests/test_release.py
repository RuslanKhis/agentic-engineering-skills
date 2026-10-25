"""Exercise release stamping, CHANGELOG sections and tagging in throwaway git repositories."""

from __future__ import annotations

from contextlib import redirect_stderr, redirect_stdout
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import release


SKILL = """---
name: {name}
description: Help with {name}.
license: MIT
metadata:
  author: A maintainer
  source-book: Agentic Engineering
---

# {name}
"""


class ReleaseTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for name in ("alpha-skill", "beta-skill"):
            path = self.root / "skills" / name / "SKILL.md"
            path.parent.mkdir(parents=True)
            path.write_text(SKILL.format(name=name), encoding="utf-8")
        (self.root / ".claude-plugin").mkdir()
        (self.root / ".claude-plugin" / "plugin.json").write_text(
            json.dumps({"name": "sample", "version": "2026.01.01"}, indent=2) + "\n", encoding="utf-8")
        (self.root / "gemini-extension.json").write_text(
            json.dumps({"name": "sample", "version": "2026.01.01"}) + "\n", encoding="utf-8")
        (self.root / "plugin.json").write_text(json.dumps({"name": "sample"}) + "\n", encoding="utf-8")

    def git(self, *args):
        subprocess.run(["git", *args], cwd=self.root, check=True, capture_output=True,
                       env={"GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@example.com",
                            "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@example.com",
                            "HOME": self.temp.name, "PATH": "/usr/bin:/bin:/usr/local/bin:/opt/homebrew/bin"})

    def init(self):
        # The release script runs git with the ambient environment, so the
        # identity must live in the repository's own config (CI has none).
        self.git("init", "-q", "-b", "main")
        self.git("config", "user.name", "t")
        self.git("config", "user.email", "t@example.com")

    def run_cli(self, *args):
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = release.main(["--root", str(self.root), *args])
        return code, out.getvalue(), err.getvalue()

    def test_stamp_inserts_then_replaces_version_and_leaves_other_metadata(self):
        release.stamp(self.root, "2026.10.25")
        text = (self.root / "skills/alpha-skill/SKILL.md").read_text(encoding="utf-8")
        self.assertIn('  source-book: Agentic Engineering\n  version: "2026.10.25"\n---', text)
        release.stamp(self.root, "2026.10.26.1")
        text = (self.root / "skills/alpha-skill/SKILL.md").read_text(encoding="utf-8")
        self.assertEqual(1, text.count("version:"))
        self.assertIn('version: "2026.10.26.1"', text)
        self.assertEqual({"2026.10.26.1"}, set(release.versions(self.root).values()))
        self.assertNotIn("version", json.loads((self.root / "plugin.json").read_text()))

    def test_stamp_adds_metadata_block_when_absent_and_rejects_bad_versions(self):
        path = self.root / "skills/beta-skill/SKILL.md"
        path.write_text("---\nname: beta-skill\ndescription: x.\n---\n\nBody\n", encoding="utf-8")
        release.stamp(self.root, "2026.10.25")
        self.assertEqual("2026.10.25", release.read_skill_version(path))
        with self.assertRaises(release.ReleaseError):
            release.stamp(self.root, "1.0")

    def test_show_reports_a_missing_version(self):
        code, out, _ = self.run_cli("show")
        self.assertEqual(0, code)
        self.assertIn("MISSING  skills/alpha-skill/SKILL.md", out)

    def test_prepare_then_tag_moves_stable_and_never_pushes(self):
        self.init()
        self.git("add", "-A")
        self.git("commit", "-q", "-m", "Initial skills")
        code, out, err = self.run_cli("prepare", "--date", "2026-10-25")
        self.assertEqual(0, code, err)
        changelog = (self.root / "CHANGELOG.md").read_text(encoding="utf-8")
        self.assertIn("## 2026.10.25 · 25 October 2026", changelog)
        self.assertIn("First tagged release", changelog)
        code, _, err = self.run_cli("tag")
        self.assertEqual(1, code)
        self.assertIn("uncommitted", err)
        self.git("add", "-A")
        self.git("commit", "-q", "-m", "Release 2026.10.25")
        code, out, err = self.run_cli("tag")
        self.assertEqual(0, code, err)
        self.assertIn("git push origin v2026.10.25", out)
        self.assertIn("Nothing was pushed", out)
        tagged = subprocess.run(["git", "rev-parse", "v2026.10.25^{commit}", "stable"], cwd=self.root,
                                capture_output=True, text=True, check=True).stdout.split()
        self.assertEqual(tagged[0], tagged[1])

    def test_second_release_same_day_gets_a_suffix_and_lists_commits(self):
        self.init()
        release.stamp(self.root, "2026.10.25")
        release.add_changelog(self.root, "## 2026.10.25 · 25 October 2026\n\n- First.\n", "2026.10.25")
        self.git("add", "-A")
        self.git("commit", "-q", "-m", "First release")
        self.git("tag", "-a", "v2026.10.25", "-m", "r")
        (self.root / "skills/alpha-skill/SKILL.md").write_text(
            (self.root / "skills/alpha-skill/SKILL.md").read_text() + "More.\n", encoding="utf-8")
        self.git("commit", "-qam", "Clarify alpha")
        code, out, err = self.run_cli("prepare", "--date", "2026-10-25")
        self.assertEqual(0, code, err)
        changelog = (self.root / "CHANGELOG.md").read_text(encoding="utf-8")
        self.assertLess(changelog.index("## 2026.10.25.1"), changelog.index("## 2026.10.25 "))
        self.assertIn("- Clarify alpha", changelog)
        code, _, err = self.run_cli("prepare", "--version", "2026.10.25.1", "--date", "2026-10-25")
        self.assertEqual(1, code)
        self.assertIn("already has a section", err)

    def test_tag_refuses_inconsistent_versions(self):
        self.init()
        release.stamp(self.root, "2026.10.25")
        stamped = self.root / "skills/beta-skill/SKILL.md"
        stamped.write_text(stamped.read_text().replace("2026.10.25", "2026.10.24"), encoding="utf-8")
        self.git("add", "-A")
        self.git("commit", "-q", "-m", "Mixed")
        code, _, err = self.run_cli("tag")
        self.assertEqual(1, code)
        self.assertIn("versions differ", err)


if __name__ == "__main__":
    unittest.main()
