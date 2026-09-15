"""Offline stdlib tests for the read-only inspector; no project imports or cloud calls."""
from __future__ import annotations

from contextlib import redirect_stdout
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import socket
import tempfile
import unittest
from unittest.mock import patch


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "inspect_project.py"
SPEC = importlib.util.spec_from_file_location("chapter10_inspector", SCRIPT)
inspector = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(inspector)


class InspectorTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        # /tmp can be a symlink on macOS; use the real path deliberately.
        self.root = Path(self.temp.name).resolve()
        self.addCleanup(self.temp.cleanup)
        self.net = patch.object(socket.socket, "connect", side_effect=AssertionError("Network forbidden"))
        self.net.start()
        self.addCleanup(self.net.stop)
        self.metadata = patch.object(inspector.importlib.metadata, "version", return_value="2.8.0")
        self.metadata.start()
        self.addCleanup(self.metadata.stop)

    def write(self, name, content):
        target = self.root / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        return target

    def run_cli(self, *args):
        output = io.StringIO()
        with redirect_stdout(output):
            code = inspector.main(["--project", str(self.root), *args])
        return code, output.getvalue(), json.loads(output.getvalue())

    def snapshot(self):
        return {str(path.relative_to(self.root)): hashlib.sha256(path.read_bytes()).hexdigest()
                for path in self.root.rglob("*") if path.is_file() and not path.is_symlink()}

    def test_requirements_and_python_are_separate_from_interpreter(self):
        self.write("requirements.txt", "google-adk==2.8.0\ngoogle-cloud-bigquery>=3.35.0,<4.0.0\npydantic>=2.11.0,<3.0.0\n")
        self.write("pyproject.toml", '[project]\nrequires-python = ">=3.11,<3.14"\n')
        code, _, result = self.run_cli("--expect-adk", "2.8.0")
        self.assertEqual(code, 0)
        self.assertEqual(result["adk_gate"]["status"], "PASS")
        self.assertEqual(result["python_declarations"][0]["constraint"], ">=3.11,<3.14")
        self.assertIn("not_target_environment", result["interpreter"]["scope"])
        self.assertIn("pip", result["package_manager_hints"])

    def test_project_manager_preserved_and_repeat_byte_stable_no_writes(self):
        self.write("pyproject.toml", '[tool.poetry.dependencies]\npython = ">=3.11,<3.14"\ngoogle-adk = "2.8.0"\n')
        self.write("poetry.lock", "DO_NOT_PARSE_LOCK_SECRET")
        self.write("pnpm-lock.yaml", "PRIVATE_REGISTRY_TOKEN")
        self.write("src/application.py", "raise RuntimeError('Project code must never run')\n")
        before = self.snapshot()
        _, first, result = self.run_cli()
        _, second, _ = self.run_cli()
        self.assertEqual(first, second)
        self.assertEqual(before, self.snapshot())
        self.assertEqual(result["package_manager_hints"], ["pnpm", "poetry"])
        self.assertNotIn("DO_NOT_PARSE", first)
        self.assertNotIn("PRIVATE_REGISTRY", first)
        self.assertIn({"code": "lock_contents_not_parsed", "file": "poetry.lock"}, result["incompleteness"])

    def test_no_secret_values_or_direct_urls_echoed(self):
        self.write(".env", "CLOUD_TOKEN=ACTUAL_SECRET_DO_NOT_READ")
        self.write(".env.local", "PASSWORD=SECOND_SECRET")
        self.write(".env.example", "API_KEY=EXAMPLE_SECRET\nexport CLOUD_PROJECT=PROJECT_PRIVATE\n# COMMENT_SECRET\n")
        self.write("requirements.txt", "google-adk @ https://name:URL_SECRET@example.invalid/custom.whl\n--index-url https://INDEX_SECRET@example.invalid\n")
        self.write("pyproject.toml", '[tool.poetry.dependencies]\ngoogle-genai = {git="https://GIT_SECRET@example.invalid/x"}\n')
        self.write("secret.py", "SECRET_FILE_CONTENT")
        _, raw, result = self.run_cli()
        for token in ("ACTUAL_SECRET", "SECOND_SECRET", "EXAMPLE_SECRET", "PROJECT_PRIVATE", "COMMENT_SECRET", "URL_SECRET", "INDEX_SECRET", "GIT_SECRET", "SECRET_FILE_CONTENT"):
            self.assertNotIn(token, raw)
        self.assertEqual(result["environment_files"], {"dotenv_present": True, "example_variable_names": ["API_KEY", "CLOUD_PROJECT"]})
        self.assertNotIn(".env", result["files"])
        self.assertNotIn("secret.py", result["files"])
        self.assertFalse(result["complete_within_supported_scope"])

    def test_hidden_private_and_dependency_directories_skipped(self):
        for name in (".git", ".venv", "venv", "node_modules", "private", "outputs", "audit"):
            self.write(name + "/requirements.txt", "google-adk==999.0")
        self.write("tests/test_app.py", "assert False")
        _, _, result = self.run_cli()
        self.assertEqual(result["files"], ["tests/test_app.py"])
        self.assertEqual(result["dependency_declarations"], [])
        self.assertEqual(result["observed"]["directories_skipped"], 7)

    def test_symlink_files_and_directories_not_followed(self):
        outside = self.write("private/requirements.txt", "google-adk==999.0")
        (self.root / "requirements.txt").symlink_to(outside)
        (self.root / "linked").symlink_to(outside.parent, target_is_directory=True)
        _, _, result = self.run_cli()
        self.assertEqual(result["dependency_declarations"], [])
        self.assertEqual(result["observed"]["symlinks_skipped"], 2)

    def test_oversized_and_total_content_limits_are_signalled(self):
        self.write("requirements.txt", "#" * 50)
        with patch.object(inspector, "MAX_FILE_BYTES", 20):
            _, _, result = self.run_cli()
        self.assertIn({"code": "file_byte_limit", "file": "requirements.txt"}, result["incompleteness"])
        self.assertEqual(result["observed"]["content_bytes_read"], 0)
        self.write("requirements.txt", "google-adk==2.8.0\n")
        self.write("requirements-dev.txt", "pytest==9.1.1\n")
        with patch.object(inspector, "MAX_TOTAL_BYTES", 20):
            _, _, result = self.run_cli()
        self.assertIn({"code": "total_byte_limit"}, result["incompleteness"])
        self.assertLessEqual(result["observed"]["content_bytes_read"], 20)

    def test_file_entry_and_depth_scan_bounds(self):
        for index in range(6):
            self.write(f"file{index}.py", "pass")
        with patch.object(inspector, "MAX_FILES", 2):
            _, _, result = self.run_cli()
        self.assertIn({"code": "file_count_limit"}, result["incompleteness"])
        self.assertEqual(len(result["files"]), 2)
        with patch.object(inspector, "MAX_ENTRIES", 2):
            _, _, result = self.run_cli()
        self.assertIn({"code": "entry_limit"}, result["incompleteness"])
        self.write("deep/deeper/deepest/app.py", "pass")
        with patch.object(inspector, "MAX_DEPTH", 1):
            _, _, result = self.run_cli()
        self.assertIn({"code": "depth_limit"}, result["incompleteness"])

    def test_malformed_and_invalid_utf8_are_safe(self):
        self.write("pyproject.toml", "[PRIVATE_PARSE_SECRET")
        (self.root / "requirements.txt").write_bytes(b"\xffPRIVATE_ENCODING_SECRET")
        _, raw, result = self.run_cli()
        self.assertNotIn("PRIVATE_PARSE", raw)
        self.assertNotIn("PRIVATE_ENCODING", raw)
        self.assertEqual({row["code"] for row in result["incompleteness"]}, {"malformed_manifest", "unreadable_or_non_utf8_file"})

    def test_pep621_poetry_optional_and_conditional_constraints(self):
        self.write("pyproject.toml", '''[project]
dependencies = ["google-adk==2.8.0", "google-genai>=2.23.0,<3.0.0"]
[project.optional-dependencies]
test = ["pytest==9.1.1"]
[tool.poetry.dependencies]
google-auth = {version=">=2.40.0,<3.0.0"}
sqlglot = "^29.0.1"
pydantic = {version="2.13.5", markers="PRIVATE_MARKER_SECRET"}
''')
        _, raw, result = self.run_cli()
        self.assertNotIn("PRIVATE_MARKER_SECRET", raw)
        declarations = {row["package"]: row for row in result["dependency_declarations"]}
        self.assertEqual(declarations["pytest"]["exact_version"], "9.1.1")
        self.assertIsNone(declarations["sqlglot"]["constraint"])
        self.assertTrue(declarations["pydantic"]["conditional"])

    def test_expected_version_mismatch_absence_range_and_conflict(self):
        variants = [
            ("google-adk==2.7.0\n", "target_adk_declaration_mismatch"),
            ("pytest==9.1.1\n", "target_adk_declaration_absent"),
            ("google-adk>=2.8.0,<3.0.0\n", "target_adk_declaration_unresolved"),
            ("google-adk==2.8.0\ngoogle-adk==2.7.0\n", "target_adk_declarations_conflict"),
            ("google-adk==2.8.0; python_version > 'PRIVATE_MARKER'\n", "target_adk_declaration_unresolved"),
        ]
        for declaration, reason in variants:
            with self.subTest(reason=reason):
                self.write("requirements.txt", declaration)
                code, raw, result = self.run_cli("--expect-adk", "2.8.0")
                self.assertEqual(code, 3)
                self.assertIn(reason, result["adk_gate"]["reasons"])
                self.assertNotIn("PRIVATE_MARKER", raw)

    def test_interpreter_absent_mismatched_or_invalid_not_target_compatibility(self):
        self.write("requirements.txt", "google-adk==2.8.0\n")
        for value in (None, "2.7.0", "PRIVATE_METADATA_VALUE"):
            with self.subTest(value=value):
                if value is None:
                    context = patch.object(inspector.importlib.metadata, "version", side_effect=inspector.importlib.metadata.PackageNotFoundError("PRIVATE_ERROR"))
                else:
                    context = patch.object(inspector.importlib.metadata, "version", return_value=value)
                with context:
                    code, raw, result = self.run_cli("--expect-adk", "2.8.0")
                self.assertEqual(code, 3)
                self.assertNotIn("PRIVATE_", raw)
                self.assertEqual(result["adk_gate"]["status"], "FAIL")

    def test_dry_run_reads_no_file_contents_or_interpreter_metadata(self):
        self.write("requirements.txt", "google-adk==2.8.0\n")
        self.write(".env.example", "API_KEY=SECRET")
        self.write(".env", "API_KEY=SECRET")
        with patch.object(inspector.Inspector, "read_content", side_effect=AssertionError("No content reads")), patch.object(inspector, "interpreter_metadata", side_effect=AssertionError("No metadata reads")):
            code, _, result = self.run_cli("--dry-run", "--expect-adk", "2.8.0")
        self.assertEqual(code, 0)
        self.assertEqual(result["mode"], "dry_run_inventory_only")
        self.assertEqual(result["observed"]["content_bytes_read"], 0)
        self.assertEqual(result["dependency_declarations"], [])
        self.assertEqual(result["adk_gate"]["status"], "NOT_RUN_DRY_RUN")

    def test_invalid_input_is_static_and_safe(self):
        for target in (self.root / "PRIVATE_MISSING_PATH", self.write("file.txt", "data")):
            output = io.StringIO()
            with redirect_stdout(output):
                code = inspector.main(["--project", str(target)])
            self.assertEqual(code, 2)
            self.assertNotIn(str(target), output.getvalue())
        symlink = self.root / "link"
        symlink.symlink_to(self.root, target_is_directory=True)
        with redirect_stdout(io.StringIO()):
            self.assertEqual(inspector.main(["--project", str(symlink)]), 2)
        code, raw, _ = self.run_cli("--expect-adk", "PRIVATE_INVALID_VERSION")
        self.assertEqual(code, 2)
        self.assertNotIn("PRIVATE_INVALID_VERSION", raw)

    def test_help_and_unknown_arguments_are_safe(self):
        output = io.StringIO()
        with redirect_stdout(output), self.assertRaises(SystemExit) as stop:
            inspector.main(["--help"])
        self.assertEqual(stop.exception.code, 0)
        self.assertIn("--project", output.getvalue())
        output = io.StringIO()
        with redirect_stdout(output), self.assertRaises(SystemExit) as stop:
            inspector.main(["--unknown=PRIVATE_ARGUMENT"])
        self.assertEqual(stop.exception.code, 2)
        self.assertNotIn("PRIVATE_ARGUMENT", output.getvalue())

    def test_unsupported_platform_fails_before_inspection(self):
        with patch.object(inspector.os, "supports_fd", set()), patch.object(
            inspector.Inspector, "report", side_effect=AssertionError("No scan")
        ):
            code, _, result = self.run_cli()
        self.assertEqual(code, 2)
        self.assertEqual(result, {"error": "directory_descriptor_scanning_unsupported"})


if __name__ == "__main__":
    unittest.main()
