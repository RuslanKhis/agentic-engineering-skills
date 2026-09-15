"""Tests for the helper only: no project code or external service is imported."""

import contextlib
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "inspect_project.py"
SPEC = importlib.util.spec_from_file_location("inspect_project", SCRIPT)
inspector = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(inspector)


class InspectProjectTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.project = Path(self.temp.name)

    def write(self, name, text):
        target = self.project / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")
        return target

    def run_cli(self, *args):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            code = inspector.main([str(self.project), *args])
        return code, output.getvalue()

    def codes(self, result, key="manual_review"):
        return {item["code"] for item in result[key]}

    def test_declared_pins_and_known_metadata(self):
        self.write("pyproject.toml", '''
[project]
name = "private-project-id-should-not-appear"
requires-python = ">=3.11,<3.13"
dependencies = ["google-adk==1.2.3", "google-cloud-dlp>=3.1", "google-genai~=1.5", "unrelated-secret-package==9.0"]
[project.optional-dependencies]
private_group_name = ["pydantic>=2.0,<3"]
[tool.pytest.ini_options]
testpaths = ["private-test-directory"]
''')
        self.write("requirements-dev.txt", "google-cloud-modelarmor==0.2.0\n")
        self.write("uv.lock", "CREDENTIALS_MUST_NOT_BE_READ")
        self.write("pytest.ini", "PRIVATE_CONFIG")
        self.write(".python-version", "3.11.4\n")
        code, output = self.run_cli()
        result = json.loads(output)
        self.assertEqual(code, 0)
        self.assertEqual(result["compatibility"], "not_assessed")
        self.assertEqual(result["manifest_paths"], ["pyproject.toml", "requirements-dev.txt"])
        self.assertEqual(result["lock_paths"], ["uv.lock"])
        self.assertEqual(result["package_manager_signals"], ["pip", "uv"])
        self.assertEqual(result["test_config_paths"], ["pyproject.toml", "pytest.ini"])
        self.assertEqual({item["dependency"] for item in result["declared_constraints"]}, inspector.DEPENDENCIES | {"python"})
        for private_value in ("private-project", "private_group", "private-test", "unrelated-secret", "CREDENTIALS", "PRIVATE_CONFIG"):
            self.assertNotIn(private_value, output)
        self.assertNotIn("uv.lock", result["files_read"])
        self.assertNotIn("pytest.ini", result["files_read"])

    def test_environment_source_nested_and_private_files_are_not_read(self):
        self.write(".env", "SENTINEL_DO_NOT_READ=secret")
        self.write(".env.production", "SENTINEL_DO_NOT_READ=secret")
        self.write("private/requirements.txt", "pydantic==99.99")
        self.write(".git/requirements.txt", "pydantic==99.99")
        self.write(".venv/requirements.txt", "pydantic==99.99")
        self.write("agent.py", "raise RuntimeError('SENTINEL_DO_NOT_READ')")
        self.write("requirements-private-account-id.txt", "pydantic==99.99")
        with patch.object(inspector, "read_metadata", side_effect=AssertionError("unexpected content read")):
            code, output = self.run_cli()
        self.assertEqual(code, 0)
        self.assertNotIn("SENTINEL", output)
        self.assertNotIn("private-account", output)
        self.assertEqual(json.loads(output)["declared_constraints"], [])

    def test_symlinks_are_skipped_and_root_symlink_is_refused(self):
        secret = self.write("secret.txt", "SENTINEL_DO_NOT_READ")
        (self.project / ".python-version").symlink_to(secret)
        (self.project / "requirements.txt").symlink_to(secret)
        with patch.object(inspector, "read_metadata", side_effect=AssertionError("symlink read")):
            code, output = self.run_cli()
        self.assertEqual(code, 0)
        result = json.loads(output)
        self.assertEqual(result["files_read"], [])
        self.assertIn("symlink_metadata_skipped", self.codes(result))
        link = self.project / "project-link"
        link.symlink_to(self.project, target_is_directory=True)
        result = inspector.inspect_project(link)
        self.assertIn("symlink_project_root_refused", self.codes(result, "errors"))
        self.assertNotIn("SENTINEL", json.dumps(result))

    def test_direct_references_unsafe_versions_and_private_extras_are_omitted(self):
        self.write("requirements.txt", """
google-adk @ https://user:PRIVATE_TOKEN@example.invalid/package.whl
google-genai==123+PRIVATE_TOKEN
pydantic[PRIVATE_TOKEN]>=2.0; python_version > '3.10'
--index-url https://user:PRIVATE_TOKEN@example.invalid/simple
google-cloud-dlp==PRIVATE_TOKEN
""")
        code, output = self.run_cli()
        result = json.loads(output)
        self.assertEqual(code, 0)
        self.assertNotIn("PRIVATE_TOKEN", output)
        self.assertNotIn("example.invalid", output)
        self.assertNotIn("https", output)
        self.assertEqual([item["dependency"] for item in result["declared_constraints"]], ["pydantic"])
        self.assertIn("unsafe_or_unresolved_constraint_omitted", self.codes(result))
        self.assertIn("conditional_dependency_requires_manual_review", self.codes(result))
        self.assertIn("dependency_extras_omitted", self.codes(result))

    def test_requirements_includes_are_never_followed(self):
        self.write("requirements.txt", "-r /outside/PRIVATE_TOKEN.txt\n-c ../outside.txt\n--requirement=private.txt\npydantic==2.10.0\n")
        self.write("private.txt", "google-adk==99.99")
        code, output = self.run_cli()
        result = json.loads(output)
        self.assertEqual(code, 0)
        self.assertNotIn("outside", output)
        self.assertNotIn("PRIVATE_TOKEN", output)
        self.assertEqual(result["files_read"], ["requirements.txt"])
        self.assertIn("requirements_include_not_followed", self.codes(result))

    def test_poetry_dynamic_and_workspace_constraints_require_review(self):
        self.write("pyproject.toml", '''
[project]
dynamic = ["dependencies"]
[tool.poetry.dependencies]
python = "^3.11"
google-adk = "1.2.3"
pydantic = {version = "^2.5", optional = true}
google-genai = {path = "PRIVATE_PATH", version = "1.0"}
google-cloud-dlp = {workspace = true}
[tool.poetry.group.private_name.dependencies]
google-cloud-modelarmor = ">=0.2,<1"
[tool.uv.workspace]
members = ["PRIVATE_PATH"]
[tool.uv.sources]
google-genai = {workspace = true}
''')
        code, output = self.run_cli()
        result = json.loads(output)
        self.assertEqual(code, 0)
        self.assertNotIn("PRIVATE_PATH", output)
        self.assertNotIn("private_name", output)
        self.assertEqual(result["package_manager_signals"], ["poetry", "uv"])
        self.assertIn("dynamic_metadata_requires_manual_review", self.codes(result))
        self.assertIn("workspace_constraints_require_manual_review", self.codes(result))
        self.assertIn("dependency_source_requires_manual_review", self.codes(result))
        self.assertIn("dependency_sources_require_manual_review", self.codes(result))
        self.assertNotIn("google-genai", {item["dependency"] for item in result["declared_constraints"]})

    def test_malformed_manifest_has_static_safe_error(self):
        self.write("pyproject.toml", 'private = "PRIVATE_TOKEN\n')
        code, output = self.run_cli()
        self.assertEqual(code, 2)
        self.assertIn("invalid_toml", self.codes(json.loads(output), "errors"))
        self.assertNotIn("PRIVATE_TOKEN", output)

    def test_dry_run_reads_no_contents_even_if_metadata_malformed(self):
        self.write("pyproject.toml", 'PRIVATE_TOKEN = "broken\n')
        self.write("requirements.txt", "PRIVATE_TOKEN")
        self.write(".python-version", "PRIVATE_TOKEN")
        with patch.object(inspector, "read_metadata", side_effect=AssertionError("dry run read content")):
            code, output = self.run_cli("--dry-run")
        result = json.loads(output)
        self.assertEqual(code, 0)
        self.assertEqual(result["files_read"], [])
        self.assertEqual(result["declared_constraints"], [])
        self.assertEqual(result["planned_content_reads"], [".python-version", "pyproject.toml", "requirements.txt"])
        self.assertNotIn("PRIVATE_TOKEN", output)

    def test_idempotent_and_no_file_writes(self):
        self.write("requirements.txt", "pydantic>=2,<3\ngoogle-adk==1.2.3\n")
        before = {path.name: (path.read_bytes(), path.stat().st_mtime_ns) for path in self.project.iterdir()}
        first = self.run_cli()
        second = self.run_cli()
        after = {path.name: (path.read_bytes(), path.stat().st_mtime_ns) for path in self.project.iterdir()}
        self.assertEqual(first, second)
        self.assertEqual(before, after)

    def test_missing_path_and_file_path_have_safe_errors(self):
        for path in (self.project / "PRIVATE_MISSING_PATH", self.write("PRIVATE_FILE_PATH", "secret")):
            result = inspector.inspect_project(path)
            self.assertIn("invalid_project_directory", self.codes(result, "errors"))
            self.assertNotIn("PRIVATE", json.dumps(result))

    def test_bounds_and_invalid_utf8_fail_safely(self):
        self.write("requirements.txt", "pydantic==1.0\n" * 3)
        with patch.object(inspector, "MAX_METADATA_BYTES", 10):
            result = inspector.inspect_project(self.project)
        self.assertIn("metadata_file_too_large", self.codes(result, "errors"))
        self.assertEqual(result["files_read"], [])
        with patch.object(inspector, "MAX_ROOT_ENTRIES", 0):
            result = inspector.inspect_project(self.project)
        self.assertIn("root_entry_limit_exceeded", self.codes(result, "errors"))
        with patch.object(inspector, "MAX_REQUIREMENT_LINES", 1):
            result = inspector.inspect_project(self.project)
        self.assertIn("requirement_line_limit_exceeded", self.codes(result, "errors"))
        self.write("requirements.txt", "pydantic==1.0\npydantic==2.0\n")
        with patch.object(inspector, "MAX_DECLARED_CONSTRAINTS", 1):
            result = inspector.inspect_project(self.project)
        self.assertEqual(len(result["declared_constraints"]), 1)
        self.assertIn("constraint_inventory_limit_exceeded", self.codes(result, "errors"))
        (self.project / "requirements.txt").write_bytes(b"PRIVATE_TOKEN\xff")
        code, output = self.run_cli()
        self.assertEqual(code, 2)
        self.assertNotIn("PRIVATE_TOKEN", output)

    def test_unconstrained_and_unresolved_values_do_not_imply_compatibility(self):
        self.write("requirements.txt", "google-adk\npydantic==*\ngoogle-genai==latest\n")
        code, output = self.run_cli()
        result = json.loads(output)
        self.assertEqual(code, 0)
        self.assertEqual(result["compatibility"], "not_assessed")
        self.assertIn("unconstrained_dependency", self.codes(result))
        self.assertIn("unsafe_or_unresolved_constraint_omitted", self.codes(result))
        self.assertNotIn("latest", output)

    def test_help_and_argument_errors(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output), self.assertRaises(SystemExit) as caught:
            inspector.main(["--help"])
        self.assertEqual(caught.exception.code, 0)
        self.assertIn("--dry-run", output.getvalue())
        self.assertIn("root-only", output.getvalue())
        error = io.StringIO()
        with contextlib.redirect_stderr(error), self.assertRaises(SystemExit) as caught:
            inspector.main([str(self.project), "--PRIVATE_TOKEN"])
        self.assertEqual(caught.exception.code, 2)
        self.assertNotIn("PRIVATE_TOKEN", error.getvalue())

    def test_older_interpreter_guard_gives_actionable_error(self):
        source = compile(SCRIPT.read_text(), str(SCRIPT), "exec")
        error = io.StringIO()
        with (
            patch("sys.version_info", (3, 10, 0)),
            contextlib.redirect_stderr(error),
            self.assertRaises(SystemExit) as caught,
        ):
            exec(source, {"__name__": "inspector_version_guard"})
        self.assertEqual(caught.exception.code, 2)
        self.assertIn("requires Python 3.11+", error.getvalue())
        self.assertIn("preserve the target interpreter", error.getvalue())


if __name__ == "__main__":
    unittest.main()
