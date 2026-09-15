"""Offline checks for the read-only project inspector."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "inspect_project.py"
spec = importlib.util.spec_from_file_location("guardrail_inspector", SCRIPT)
inspector = importlib.util.module_from_spec(spec)
spec.loader.exec_module(inspector)


class InspectorTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name).resolve()
        self.addCleanup(self.temporary.cleanup)

    def run_cli(self, *args):
        return subprocess.run([sys.executable, str(SCRIPT), *args], cwd=self.root,
                              capture_output=True, text=True, timeout=20)

    def write(self, name, content):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return path

    def test_help_requires_no_project(self):
        result = self.run_cli("--help")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("--dry-run", result.stdout)
        self.assertIn("--require-adk", result.stdout)

    def test_dry_run_equivalence_and_no_writes_or_project_execution(self):
        self.write("pyproject.toml", '[project]\nrequires-python = ">=3.11"\ndependencies = ["google-adk==2.8.0", "google-genai>=1.0,<2"]\n')
        self.write("agent.py", 'raise RuntimeError("MUST NOT EXECUTE")\n# SafeAgentRuntime usage_metadata\n')
        self.write("uv.lock", "DO NOT PARSE THE LOCK CONTENT")
        before = {str(p.relative_to(self.root)): p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        normal = self.run_cli("--project", str(self.root))
        dry = self.run_cli("--project", str(self.root), "--dry-run")
        self.assertEqual(normal.returncode, 0, normal.stderr + normal.stdout)
        self.assertEqual(dry.returncode, normal.returncode)
        self.assertEqual(json.loads(dry.stdout), json.loads(normal.stdout))
        report = json.loads(normal.stdout)
        self.assertEqual(report["declared"]["google-adk"], ["==2.8.0"])
        self.assertEqual(report["declared"]["python"], [">=3.11"])
        self.assertIn("uv.lock", report["config_files"])
        self.assertEqual(report["guardrail_identifiers"]["usage_metadata"]["occurrences"], 1)
        after = {str(p.relative_to(self.root)): p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        self.assertEqual(after, before)

    def test_secrets_and_malicious_dependency_values_are_not_printed(self):
        sentinel = "DO_NOT_DISCLOSE_982371"
        self.write(".env", "GOOGLE_API_KEY=" + sentinel)
        self.write("credentials.py", "usage_metadata = " + repr(sentinel))
        self.write("service-account.json", sentinel)
        self.write("credentials/config.py", "MockBudgetStore = " + repr(sentinel))
        self.write("requirements.txt", "google-adk==" + sentinel + "\ngoogle-genai @ https://" + sentinel + "\n")
        self.write("pyproject.toml", '[project]\ndependencies = ["google-adk==2.8.0; secret == ' + "'" + sentinel + "'" + '"]\n')
        result = self.run_cli("--project", str(self.root))
        self.assertEqual(result.returncode, 1)
        self.assertNotIn(sentinel, result.stdout + result.stderr)
        report = json.loads(result.stdout)
        self.assertFalse(report["complete_within_scope"])
        self.assertFalse(report["guardrail_identifiers"])
        self.assertEqual(report["declared"]["google-adk"], [])

    def test_symlinks_and_dependency_directories_are_skipped(self):
        outside = self.root / "outside"
        outside.mkdir()
        (outside / "source.py").write_text("MockBudgetStore", encoding="utf-8")
        target = self.root / "target"
        target.mkdir()
        (target / "linked").symlink_to(outside, target_is_directory=True)
        (target / "linked.py").symlink_to(outside / "source.py")
        for directory in (".git", ".venv", "node_modules", "build"):
            (target / directory).mkdir()
            (target / directory / "source.py").write_text("MockBudgetStore", encoding="utf-8")
        result = self.run_cli("--project", str(target))
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report["excluded_symlinks"], 2)
        self.assertFalse(report["guardrail_identifiers"])
        link = self.root / "root-link"
        link.symlink_to(target, target_is_directory=True)
        self.assertEqual(self.run_cli("--project", str(link)).returncode, 2)

    def test_invalid_directory_and_exact_version_argument(self):
        self.assertEqual(self.run_cli("--project", str(self.root / "missing")).returncode, 2)
        path = self.write("file.txt", "test")
        self.assertEqual(self.run_cli("--project", str(path)).returncode, 2)
        result = self.run_cli("--project", str(self.root), "--require-adk", "SECRET_VERSION")
        self.assertEqual(result.returncode, 2)
        self.assertNotIn("SECRET_VERSION", result.stderr)

    def test_malformed_configuration_and_large_file_are_explicitly_limited(self):
        self.write("pyproject.toml", "[project\nsecret = 'not echoed'")
        self.write("huge.py", "x" * (inspector.MAX_BYTES + 1))
        result = self.run_cli("--project", str(self.root))
        self.assertEqual(result.returncode, 1)
        warnings = json.loads(result.stdout)["warnings"]
        self.assertIn("file_unreadable_or_configuration_malformed", warnings)
        self.assertIn("file_size_limit_reached", warnings)
        self.assertNotIn("not echoed", result.stdout + result.stderr)

    def test_metadata_probe_and_exact_adk_check(self):
        with mock.patch.object(inspector.metadata, "version", side_effect=["2.8.0", "1.5.0"]) as probe:
            report = inspector.inspect(self.root, "2.8.0")
        self.assertEqual(probe.call_args_list, [mock.call("google-adk"), mock.call("google-genai")])
        self.assertTrue(report["adk_compatibility"]["matches"])
        self.assertTrue(report["complete_within_scope"])
        with mock.patch.object(inspector.metadata, "version", return_value="2.9.0"):
            mismatch = inspector.inspect(self.root, "2.8.0")
            generic = inspector.inspect(self.root)
        self.assertFalse(mismatch["complete_within_scope"])
        self.assertNotIn("adk_compatibility", generic)
        self.assertTrue(generic["complete_within_scope"])

    def test_metadata_values_are_sanitized_and_probe_failures_reported(self):
        with mock.patch.object(inspector.metadata, "version", side_effect=["SECRET_VERSION", RuntimeError("SECRET_ERROR")]):
            report = inspector.inspect(self.root)
        serialized = json.dumps(report)
        self.assertNotIn("SECRET_VERSION", serialized)
        self.assertNotIn("SECRET_ERROR", serialized)
        self.assertFalse(report["complete_within_scope"])
        self.assertIn("installed_metadata_unreadable", report["warnings"])

    def test_depth_file_count_and_unsafe_filename_limits(self):
        self.write("a/b/c/source.py", "MockBudgetStore")
        self.write("bad\nname.py", "MockBudgetStore")
        with mock.patch.object(inspector, "MAX_DEPTH", 1):
            report = inspector.inspect(self.root)
        self.assertIn("directory_depth_limit_reached", report["warnings"])
        self.assertIn("unsafe_filename_omitted", report["warnings"])
        self.assertFalse(report["guardrail_identifiers"])
        with mock.patch.object(inspector, "MAX_FILES", 1):
            report = inspector.inspect(self.root)
        self.assertIn("file_count_limit_reached", report["warnings"])

    def test_directory_count_and_total_read_limits(self):
        self.write("a/source.py", "MockBudgetStore")
        self.write("b/source.py", "MockBudgetStore")
        with mock.patch.object(inspector, "MAX_DIRS", 1):
            report = inspector.inspect(self.root)
        self.assertIn("directory_count_limit_reached", report["warnings"])
        with mock.patch.object(inspector, "MAX_TOTAL_BYTES", 2):
            report = inspector.inspect(self.root)
        self.assertIn("total_read_limit_reached", report["warnings"])
        self.assertFalse(report["guardrail_identifiers"])

    def test_python_version_pin_file(self):
        self.write(".python-version", "3.11.4\n")
        report = inspector.inspect(self.root)
        self.assertEqual(report["declared"]["python"], ["3.11.4"])
        self.assertIn(".python-version", report["config_files"])

    def test_malformed_dependency_shape_is_reported(self):
        self.write("pyproject.toml", '[project]\ndependencies = "not a dependency list"\n')
        report = inspector.inspect(self.root)
        self.assertIn("malformed_dependency_list", report["warnings"])

    def test_read_error_is_reported_without_exception_details(self):
        self.write("agent.py", "MockBudgetStore")
        with mock.patch.object(inspector.os, "open", side_effect=PermissionError("SECRET_ERROR")):
            report = inspector.inspect(self.root)
        self.assertIn("file_unreadable_or_configuration_malformed", report["warnings"])
        self.assertNotIn("SECRET_ERROR", json.dumps(report))


if __name__ == "__main__":
    unittest.main()
