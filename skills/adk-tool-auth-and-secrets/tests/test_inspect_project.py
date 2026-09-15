"""Contract tests use temporary synthetic projects; no credentials or services."""
from __future__ import annotations

import contextlib
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "inspect_project.py"
SPEC = importlib.util.spec_from_file_location("skill_static_inspector", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
inspector = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(inspector)  # Only the trusted helper, never target code.
CANARY = "PRIVATE_PAYLOAD_CANARY_926517"


class InspectorTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "project"
        self.root.mkdir()

    def write(self, relative, text):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
        return path

    def run_inspection(self, *args):
        output, errors = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(output), contextlib.redirect_stderr(errors):
            try:
                code = inspector.main([str(self.root), *args])
            except SystemExit as exc:
                code = exc.code
        self.assertNotIn(CANARY, output.getvalue() + errors.getvalue())
        return code, json.loads(output.getvalue()), errors.getvalue()

    def test_expected_pin_dry_run_and_repeat_are_identical_and_read_only(self):
        self.write("requirements.txt", "google-adk==2.8.0\nhttpx>=0.28,<1\n")
        self.write("agent.py", "async def action(tool_context: ToolContext):\n    return None\n")
        before = {p.relative_to(self.root): p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        first = self.run_inspection("--expect-adk", "2.8.0")
        self.assertEqual(first, self.run_inspection("--expect-adk", "2.8.0", "--dry-run"))
        self.assertEqual(first, self.run_inspection("--expect-adk", "2.8.0"))
        self.assertEqual(first[0], 0)
        self.assertEqual(first[1]["adk_expectation"]["result"], "static_pins_match")
        self.assertEqual(first[1]["security_verdict"], "not_assessed")
        after = {p.relative_to(self.root): p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        self.assertEqual(before, after)

    def test_secret_payloads_and_dependency_directories_are_not_read(self):
        for relative in (".env", ".env.example", "secrets/hidden.py", "credentials/key.py",
                         "logs/history.py", "data/state.py", ".git/config.py",
                         ".venv/lib/injected.py", "node_modules/injected.py"):
            self.write(relative, CANARY + " not Python or TOML")
        self.write("refresh-tokens.json", CANARY)
        code, result, _ = self.run_inspection()
        self.assertEqual(code, 0)
        self.assertEqual(result["counts"]["candidate_files"], 0)

    def test_import_side_effect_is_not_executed_and_source_literals_not_echoed(self):
        marker = self.root / "EXECUTED"
        self.write("agent.py", f"from pathlib import Path\nPath({str(marker)!r}).touch()\nSECRET = {CANARY!r}\n")
        code, result, _ = self.run_inspection()
        self.assertEqual(code, 0)
        self.assertFalse(marker.exists())
        self.assertEqual(result["counts"]["candidate_files"], 1)

    def test_target_symlinks_are_skipped(self):
        outside = Path(self.temp.name) / "outside.py"
        outside.write_text(CANARY + " not valid Python")
        (self.root / "linked.py").symlink_to(outside)
        (self.root / "linked-dir").symlink_to(outside.parent, target_is_directory=True)
        code, result, _ = self.run_inspection()
        self.assertEqual(code, 0)
        self.assertEqual(result["counts"]["symlinks_skipped"], 2)
        self.assertEqual(result["counts"]["candidate_files"], 0)

    def test_private_requirement_urls_and_directives_are_not_echoed_or_followed(self):
        self.write("requirements.txt", f"--index-url https://user:{CANARY}@example.invalid/simple\n"
                   f"google-adk @ https://user:{CANARY}@example.invalid/wheel\n-r private.txt\n")
        self.write("private.txt", CANARY)
        code, result, _ = self.run_inspection("--expect-adk", "2.8.0")
        self.assertEqual(code, 3)
        self.assertEqual(result["dependencies"][0]["constraint_kind"], "unknown")
        self.assertEqual(result["dependencies"][0]["numeric_versions"], [])
        self.assertEqual(result["counts"]["candidate_files"], 1)

    def test_candidates_are_observations_not_safety_verdicts(self):
        self.write("tools.py", f"""async def search(user_id: str, refresh_token: str, ctx: ToolContext):
    target = 'projects/private/secrets/{CANARY}/versions/latest'
    return event.model_dump()

def ordinary_server_function(user_id: str):
    return user_id
""")
        code, result, _ = self.run_inspection()
        codes = {item["code"] for item in result["observations"]}
        self.assertEqual(code, 0)
        self.assertTrue({"TOOL_CONTEXT_PARAMETER", "TOOL_IDENTITY_PARAMETER_CANDIDATE",
                         "TOOL_CREDENTIAL_PARAMETER_CANDIDATE", "LATEST_SECRET_REFERENCE_CANDIDATE",
                         "RAW_EVENT_SERIALIZATION_CANDIDATE"} <= codes)
        self.assertEqual(sum(item["code"] == "TOOL_IDENTITY_PARAMETER_CANDIDATE"
                             for item in result["observations"]), 1)
        for item in result["observations"]:
            self.assertEqual(set(item), {"code", "path", "line"})

    def test_manifest_shapes_numeric_constraints_and_lockfiles(self):
        self.write("pyproject.toml", """[project]
requires-python = ">=3.11,<4"
dependencies = ["google-adk==2.8.0", "httpx>=0.28,<1"]
[tool.poetry.dependencies]
python = "^3.11"
firebase-admin = { version = "7.5.0" }
""")
        self.write("uv.lock", '[[package]]\nname="google-adk"\nversion="2.8.0"\n')
        self.write("poetry.lock", '[[package]]\nname="google-genai"\nversion="2.23.0"\n')
        code, result, _ = self.run_inspection("--expect-adk", "2.8.0")
        self.assertEqual(code, 0)
        adk = [item for item in result["dependencies"] if item["dependency"] == "google-adk"]
        self.assertEqual({item["origin"] for item in adk}, {"declaration", "lockfile"})
        self.assertTrue(all(item["numeric_versions"] == ["2.8.0"] for item in adk))
        self.assertEqual(result["runtime_compatibility"], "not_verified")

    def test_expected_adk_missing_different_and_ranged_are_unproven(self):
        for content in ("", "google-adk==2.9.0\n", "google-adk>=2.8.0,<3\n",
                        "google-adk==2.8.0\n-r uninspected.txt\n"):
            with self.subTest(content=content):
                self.write("requirements.txt", content)
                code, result, _ = self.run_inspection("--expect-adk", "2.8.0")
                self.assertEqual(code, 3)
                self.assertEqual(result["adk_expectation"]["result"], "missing_different_or_unproven")

    def test_malformed_source_and_toml_use_fixed_diagnostics(self):
        self.write("bad.py", f"def {CANARY}(\n")
        self.write("pyproject.toml", f'key = "{CANARY}\n')
        code, result, _ = self.run_inspection("--expect-adk", "2.8.0")
        self.assertEqual(code, 2)
        self.assertFalse(result["complete"])
        self.assertEqual({item["code"] for item in result["diagnostics"]},
                         {"PYTHON_PARSE_ERROR", "TOML_PARSE_ERROR"})

    def test_file_count_size_and_total_limits(self):
        self.write("a.py", "pass\n")
        self.write("b.py", "pass\n")
        for args, expected in ((["--max-files", "1"], "FILE_COUNT_LIMIT"),
                               (["--max-file-bytes", "4"], "FILE_SIZE_LIMIT"),
                               (["--max-total-bytes", "7"], "TOTAL_BYTES_LIMIT")):
            with self.subTest(args=args):
                code, result, _ = self.run_inspection(*args)
                self.assertEqual(code, 2)
                self.assertFalse(result["complete"])
                self.assertIn(expected, {item["code"] for item in result["diagnostics"]})

    def test_directory_entry_traversal_is_bounded_even_for_ignored_files(self):
        for i in range(1002):
            self.write(f"ignored-{i}.json", "{}")
        code, result, _ = self.run_inspection("--max-files", "1")
        self.assertEqual(code, 2)
        self.assertIn("TRAVERSAL_ENTRY_LIMIT", {item["code"] for item in result["diagnostics"]})
        self.assertLessEqual(result["counts"]["traversal_entries"], 1001)

    def test_invalid_cli_arguments_do_not_echo_values(self):
        code, result, _ = self.run_inspection("--max-files", CANARY)
        self.assertEqual(code, 2)
        self.assertEqual(result["diagnostics"], [{"code": "INVALID_ARGUMENTS"}])

    def test_help_exits_successfully_without_inspection(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output), self.assertRaises(SystemExit) as raised:
            inspector.main(["--help"])
        self.assertEqual(raised.exception.code, 0)
        self.assertIn("--dry-run", output.getvalue())
        self.assertIn("--expect-adk", output.getvalue())

    def test_invalid_root_is_fixed_error(self):
        self.root.rmdir()
        code, result, _ = self.run_inspection()
        self.assertEqual(code, 2)
        self.assertEqual(result["diagnostics"], [{"code": "INVALID_PROJECT_ROOT"}])


if __name__ == "__main__":
    unittest.main()
