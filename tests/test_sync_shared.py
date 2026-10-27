"""Exercise the shared-snippet copier on temporary, independently built repositories."""

from __future__ import annotations

from contextlib import redirect_stderr, redirect_stdout
import io
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from sync_shared import main, run

CANONICAL = "<!-- Maintainer note.\ncarriers: alpha, beta\n-->\n\n**Rule.** Do the thing.\nSecond line.\n"
BLOCK = "<!-- shared:rule -->\n**Rule.** Do the thing.\nSecond line.\n<!-- /shared:rule -->"


class SyncSharedTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "shared").mkdir()
        (self.root / "shared" / "rule.md").write_text(CANONICAL, encoding="utf-8")
        for name in ("alpha", "beta"):
            (self.root / "skills" / name / "references").mkdir(parents=True)
            self.write(name, f"# {name}\n\nBefore.\n\n{BLOCK}\n\nAfter.\n")

    def write(self, package, text, relative="references/rules.md"):
        path = self.root / "skills" / package / relative
        path.write_text(text, encoding="utf-8")
        return path

    def check(self):
        with redirect_stdout(io.StringIO()):
            return main(["--root", str(self.root), "--check"])

    def test_identical_copies_pass_and_header_is_not_copied(self):
        self.assertEqual(0, self.check())
        result = run(self.root, check=True)
        self.assertEqual([], result.errors)
        self.assertEqual({"alpha", "beta"}, result.carried["rule"])

    def test_drift_fails_check_without_writing(self):
        path = self.write("alpha", f"Before.\n\n{BLOCK.replace('Second', 'Changed')}\n")
        before = path.read_text(encoding="utf-8")
        self.assertEqual(1, self.check())
        self.assertEqual(before, path.read_text(encoding="utf-8"))

    def test_sync_rewrites_only_the_block(self):
        path = self.write("alpha", f"Before.\n\n{BLOCK.replace('Second', 'Changed')}\n\nAfter.\n")
        with redirect_stdout(io.StringIO()):
            self.assertEqual(0, main(["--root", str(self.root)]))
        self.assertEqual(f"Before.\n\n{BLOCK}\n\nAfter.\n", path.read_text(encoding="utf-8"))
        self.assertEqual(0, self.check())

    def test_unclosed_nested_and_mismatched_markers_fail(self):
        cases = {
            "unclosed": "<!-- shared:rule -->\ntext\n",
            "nested": "<!-- shared:rule -->\n<!-- shared:rule -->\n<!-- /shared:rule -->\n",
            "mismatched": "<!-- shared:rule -->\ntext\n<!-- /shared:other -->\n",
            "stray close": "text\n<!-- /shared:rule -->\n",
        }
        for label, text in cases.items():
            with self.subTest(label=label):
                path = self.write("beta", f"{BLOCK}\n")
                self.write("alpha", text)
                result = run(self.root, check=False)
                self.assertTrue(result.errors, label)
                self.assertEqual(text, (self.root / "skills/alpha/references/rules.md").read_text(encoding="utf-8"))
                self.assertTrue(path.exists())

    def test_unknown_snippet_fails(self):
        self.write("alpha", f"{BLOCK}\n\n<!-- shared:missing -->\nx\n<!-- /shared:missing -->\n", "SKILL.md")
        self.assertEqual(1, self.check())

    def test_listed_carrier_without_block_fails(self):
        self.write("beta", "No block here.\n")
        result = run(self.root, check=True)
        self.assertTrue(any("beta" in e and "missing" in e for e in result.errors), result.errors)

    def test_unlisted_carrier_fails(self):
        (self.root / "skills" / "gamma").mkdir()
        self.write("gamma", f"{BLOCK}\n", "SKILL.md")
        result = run(self.root, check=True)
        self.assertTrue(any("gamma" in e and "does not list" in e for e in result.errors), result.errors)

    def test_absent_carrier_package_is_not_required(self):
        (self.root / "shared" / "rule.md").write_text(CANONICAL.replace("beta", "beta, delta"), encoding="utf-8")
        self.assertEqual(0, self.check())

    def test_missing_shared_directory_is_a_usage_error(self):
        with tempfile.TemporaryDirectory() as other:
            with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
                self.assertEqual(2, main(["--root", other, "--check"]))

    def test_repository_copies_are_in_sync(self):
        root = Path(__file__).resolve().parents[1]
        if not (root / "shared").is_dir():
            self.skipTest("no shared/ directory in this checkout")
        result = run(root, check=True)
        self.assertEqual([], result.errors)
        self.assertEqual([], result.drifted)


if __name__ == "__main__":
    unittest.main()
