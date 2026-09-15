"""Exercise the inventory through its public CLI using isolated local fixtures."""

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "inspect_project.py"


class InspectionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "project"
        self.root.mkdir()

    def write(self, name, content):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
        return path

    def run_cli(self, *args, project=True):
        command = [sys.executable, str(SCRIPT)]
        if project:
            command += ["--project", str(self.root)]
        return subprocess.run(command + list(args), capture_output=True, text=True, check=False)

    def scan(self, *args):
        result = self.run_cli(*args)
        self.assertIn(result.returncode, (0, 1), result.stderr)
        return result, json.loads(result.stdout)

    def test_help_and_invalid_arguments(self):
        result = self.run_cli("--help", project=False)
        self.assertEqual(result.returncode, 0)
        self.assertIn("--dry-run", result.stdout)
        self.assertEqual(self.run_cli(project=False).returncode, 2)
        for option in ("--max-files", "--max-bytes", "--max-depth", "--max-entries"):
            for value in ("0", "-1", "not-a-number"):
                self.assertEqual(self.run_cli(option, value).returncode, 2)
        self.assertEqual(self.run_cli("--project", str(self.root / "absent")).returncode, 2)

    def test_dry_run_is_read_only_and_repeatable(self):
        marker = self.root / "executed.txt"
        source = self.write("tool.py", f"from pathlib import Path\nPath({str(marker)!r}).write_text('executed')\n")
        before = {p.relative_to(self.root): (p.read_bytes(), p.stat().st_mtime_ns)
                  for p in self.root.rglob("*") if p.is_file()}
        first, data = self.scan("--dry-run")
        second, _ = self.scan("--dry-run")
        self.assertEqual(first.returncode, 0)
        self.assertEqual(first.stdout, second.stdout)
        self.assertTrue(data["read_only"])
        self.assertTrue(data["dry_run"])
        self.assertFalse(data["changes_made"])
        regular, regular_data = self.scan()
        regular_data["dry_run"] = True
        self.assertEqual(data, regular_data)
        self.assertEqual(regular.returncode, 0)
        after = {p.relative_to(self.root): (p.read_bytes(), p.stat().st_mtime_ns)
                 for p in self.root.rglob("*") if p.is_file()}
        self.assertEqual(before, after)
        self.assertTrue(source.exists())
        self.assertFalse(marker.exists())

    def test_dependencies_and_numeric_constraints(self):
        self.write("requirements-dev.txt", "google-adk==2.8.0\nhttpx >=0.28,<1 ; python_version >= '3.11'\ntenacity==9.1.4 # comment\n")
        self.write("pyproject.toml", '[project]\nrequires-python = ">=3.11,<4"\ndependencies = ["google-genai~=1.2"]\n[tool.poetry.dependencies]\npython = "^3.11"\nhttpx = {version = "~0.28"}\n[tool.poetry.group.dev.dependencies]\ntenacity = "9.1.4"\n')
        self.write(".python-version", "3.11.14\n")
        result, data = self.scan()
        self.assertEqual(result.returncode, 0)
        found = {(item["name"], item["constraint"]) for item in data["dependencies"]}
        self.assertTrue({("google-adk", "==2.8.0"), ("httpx", ">=0.28,<1"),
                         ("python", ">=3.11,<4"), ("python", "3.11.14"),
                         ("python", "^3.11"), ("httpx", "~0.28"),
                         ("google-genai", "~=1.2"), ("tenacity", "9.1.4")} <= found)

    def test_redaction_and_sensitive_exclusions(self):
        marker = "CREDENTIAL_VALUE_THAT_MUST_NOT_APPEAR"
        self.write("requirements.txt", f"httpx @ https://user:{marker}@invalid.example/archive\ngoogle-adk=={marker}\n")
        self.write("pyproject.toml", f'[tool.poetry.dependencies]\ntenacity = {{git = "https://{marker}", version = "1.0"}}\n')
        self.write("tool.py", f'PROVIDER_URL = "https://{marker}"\n')
        for name in (".env", ".env.local", "credentials.json", "secrets.py", ".venv/leak.py", "node_modules/leak.py"):
            self.write(name, marker)
        self.write("poetry.lock", marker + "\x00" * 100)
        result, data = self.scan()
        self.assertEqual(result.returncode, 0)
        self.assertNotIn(marker, result.stdout + result.stderr)
        self.assertNotIn(str(self.root), result.stdout)
        self.assertEqual(data["lockfiles"], ["poetry.lock"])
        self.assertEqual(len(data["dependencies"]), 3)
        self.assertTrue(all(item["status"] == "redacted" and item["constraint"] is None
                            for item in data["dependencies"]))

    def test_bounds_report_partial_scan(self):
        self.write("a.py", "a = 1\n")
        self.write("b.py", "b = 2\n")
        result, data = self.scan("--max-files", "1")
        self.assertEqual(result.returncode, 1)
        self.assertEqual(data["files_inspected"], 1)
        self.assertIn("file_count_limit", {item["reason"] for item in data["issues"]})
        result, data = self.scan("--max-bytes", "1")
        self.assertEqual(result.returncode, 1)
        self.assertTrue(all(item["reason"] == "file_size_limit" for item in data["issues"]))
        self.write("one/two/hidden.py", "pass\n")
        result, data = self.scan("--max-depth", "1")
        self.assertEqual(result.returncode, 1)
        self.assertIn({"path": "one/two", "reason": "depth_limit"}, data["issues"])

    def test_symlinks_are_skipped(self):
        outside = Path(self.temp.name) / "outside.py"
        outside.write_text("import httpx\nhttpx.AsyncClient()\n")
        (self.root / "link.py").symlink_to(outside)
        (self.root / "directory").symlink_to(self.root, target_is_directory=True)
        result, data = self.scan()
        self.assertEqual(result.returncode, 1)
        self.assertEqual(data["signals"], [])
        self.assertEqual({item["reason"] for item in data["issues"]}, {"symlink_skipped"})
        self.assertEqual(self.run_cli("--project", str(self.root / "directory")).returncode, 2)

    def test_entry_cap_bounds_ineligible_files_and_stops_globally(self):
        for index in range(12):
            self.write(f"ignored-{index}.bin", "irrelevant")
        self.write("tool.py", "import httpx\nhttpx.AsyncClient()\n")
        result, data = self.scan("--max-entries", "5")
        self.assertEqual(result.returncode, 1)
        self.assertEqual(data["directory_entries_seen"], 5)
        self.assertEqual(data["files_inspected"], 0)
        self.assertEqual(data["issues"], [{"path": ".", "reason": "entry_count_limit"}])
        self.assertEqual(result.stdout, self.run_cli("--max-entries", "5").stdout)
        for path in self.root.iterdir():
            path.unlink()
        self.write("a/first.py", "pass\n")
        self.write("b/second.py", "pass\n")
        result, data = self.scan("--max-entries", "3")
        self.assertEqual(result.returncode, 1)
        self.assertEqual(data["issues"], [{"path": "a", "reason": "entry_count_limit"}])
        self.assertEqual(data["directory_entries_seen"], 3)

    def test_malformed_files_are_partial_without_content(self):
        marker = "PRIVATE_SOURCE_TEXT"
        self.write("bad.py", f"def {marker}(\n")
        self.write("pyproject.toml", f"[{marker}\n")
        (self.root / "binary.py").write_bytes(b"\xff")
        result, data = self.scan()
        self.assertEqual(result.returncode, 1)
        self.assertNotIn(marker, result.stdout + result.stderr)
        self.assertEqual(len(data["issues"]), 3)

    def test_invalid_manifest_shapes_are_partial(self):
        for value in ('"httpx==0.28"', '[42]'):
            self.write("pyproject.toml", f"[project]\ndependencies = {value}\n")
            result, data = self.scan()
            self.assertEqual(result.returncode, 1)
            self.assertEqual(data["issues"], [{"path": "pyproject.toml", "reason": "malformed_file"}])

    def test_unreadable_source_is_reported_without_exception_text(self):
        path = self.write("locked.py", "pass\n")
        path.chmod(0)
        try:
            result, data = self.scan()
            if result.returncode == 0:
                self.skipTest("the test process can read files without permission bits")
            self.assertEqual(result.returncode, 1)
            self.assertIn({"path": "locked.py", "reason": "unreadable_file"}, data["issues"])
            self.assertNotIn(str(self.root), result.stdout + result.stderr)
        finally:
            path.chmod(0o600)

    def test_ast_signals_and_import_aliases(self):
        self.write("tools.py", '''import asyncio as aio
import httpx as hx
import time as clock
from uuid import uuid4 as new_id
from tenacity import retry as again
from google.adk.tools import FunctionTool as Tool

@again(stop=None)
async def pay():
    key = new_id()
    clock.sleep(1)
    async with aio.timeout(2) as deadline:
        await aio.sleep(0)
    deadline.expired()
    hx.AsyncClient(timeout=hx.Timeout(2))
    def separate_sync():
        clock.sleep(1)

Tool(pay, require_confirmation=True)
Tool(pay, require_confirmation=False)
Tool(pay, require_confirmation=callback)
Tool(pay)
''')
        result, data = self.scan()
        self.assertEqual(result.returncode, 0)
        labels = [item["signal"] for item in data["signals"]]
        self.assertTrue({"retry_decorator", "uuid_inside_retry_function", "cooperative_deadline",
                         "deadline_expiry_check", "httpx_async_client", "httpx_transport_timeout",
                         "confirmation_required", "confirmation_disabled", "confirmation_dynamic",
                         "confirmation_not_configured"} <= set(labels))
        self.assertEqual(labels.count("blocking_call_in_async"), 1)
        self.assertNotIn("callback", result.stdout)

    def test_imported_local_retry_wrapper(self):
        self.write("tool.py", "from safe_api import safe_api_call as bounded\nimport uuid\n@bounded(max_attempts=3)\nasync def pay():\n    return uuid.uuid4()\n")
        result, data = self.scan()
        self.assertEqual(result.returncode, 0)
        self.assertEqual({item["signal"] for item in data["signals"]},
                         {"retry_decorator", "uuid_inside_retry_function"})


if __name__ == "__main__":
    unittest.main()
