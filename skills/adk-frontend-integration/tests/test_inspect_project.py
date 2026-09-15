"""Offline public-boundary tests for the portable manifest inspector."""

from contextlib import redirect_stdout, redirect_stderr
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "inspect_project.py"
SPEC = importlib.util.spec_from_file_location("skill_inspect_project", SCRIPT)
inspector = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(inspector)
SECRET = "PRIVATE_CUSTOMER_REGISTRY_TOKEN_DO_NOT_EXPOSE"


class InspectorTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.project = self.root / "project"
        self.project.mkdir()

    def write(self, relative, text):
        path = self.project / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return path

    def cli(self, *extra, script=SCRIPT):
        result = subprocess.run([sys.executable, "-I", "-B", str(script), "--project", str(self.project), *extra],
                                cwd=self.root, capture_output=True, text=True, timeout=15)
        self.assertNotIn(SECRET, result.stdout + result.stderr)
        return result, json.loads(result.stdout) if result.stdout else None

    def fake_versions(self, overrides=None):
        values = {name: "1.0.0" for name in inspector.PYTHON_PACKAGES}
        values.update(inspector.TESTED_PINS)
        values.update(overrides or {})
        def version(name):
            if values[name] is None:
                raise inspector.importlib.metadata.PackageNotFoundError(name)
            return values[name]
        return version

    def run_main(self, *extra, versions=None):
        stdout = io.StringIO()
        with patch.object(inspector.importlib.metadata, "version", side_effect=self.fake_versions(versions)), redirect_stdout(stdout):
            code = inspector.main(["--project", str(self.project), *extra])
        self.assertNotIn(SECRET, stdout.getvalue())
        return code, json.loads(stdout.getvalue())

    def test_help_needs_no_project_and_describes_exit_contract(self):
        result = subprocess.run([sys.executable, "-I", "-B", str(SCRIPT), "--help"], capture_output=True, text=True, timeout=15)
        self.assertEqual(result.returncode, 0)
        self.assertIn("--dry-run", result.stdout)
        self.assertIn("--require-tested-stack", result.stdout)
        self.assertIn("Exit codes", result.stdout)

    def test_invalid_arguments_never_echo_pasted_secrets(self):
        for extra in (("--mode", SECRET), ("--unknown-" + SECRET,), (SECRET,)):
            with self.subTest(extra=extra):
                result, data = self.cli(*extra)
                self.assertEqual(result.returncode, 2)
                self.assertIsNone(data)
                self.assertEqual(result.stderr, "error: invalid arguments; use --help for the accepted interface.\n")

    def test_python_version_guard_fails_before_optional_tomllib_import(self):
        # Simulate the unsupported startup version without requiring that runtime.
        code = ('import sys, runpy; sys.version_info = (3, 10, 0); '
                'runpy.run_path(sys.argv[1], run_name="__main__")')
        result = subprocess.run([sys.executable, "-I", "-B", "-c", code, str(SCRIPT)],
                                capture_output=True, text=True, timeout=15)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, "")
        self.assertEqual(result.stderr, "error: inspect_project.py requires Python 3.11 or newer.\n")

    def test_empty_greenfield_is_complete_not_a_compatibility_failure(self):
        code, data = self.run_main()
        self.assertEqual(code, 0)
        self.assertEqual(data["project"]["manifests"], [])
        self.assertTrue(data["project"]["complete_within_scope"])
        self.assertIsNone(data["tested_stack_gate"]["matches_reference_pins"])

    def test_requirements_only_allowlisted_names_versions_and_extras(self):
        self.write("requirements-dev.txt", '\n'.join([
            "google-adk==2.8.0", "google-cloud-aiplatform[agent-engines]==1.153.1",
            'google-genai==2.19.0; python_version >= "3.11"', "fastapi>=0.115.2,<1.0.0",
            "private-customer-package==123", "--extra-index-url https://user:" + SECRET + "@example.invalid",
            "-r ../../" + SECRET, "-c secret-constraints.txt", "httpx @ https://" + SECRET,
            "pydantic==2.12.0 # " + SECRET,
        ]))
        code, data = self.run_main()
        self.assertEqual(code, 0)
        record = data["project"]["manifests"][0]
        deps = {item["name"]: item for item in record["dependencies"]}
        self.assertEqual(deps["google-adk"]["reference_status"], "tested_pin")
        self.assertEqual(deps["google-cloud-aiplatform"]["extras"], ["agent-engines"])
        self.assertTrue(deps["google-genai"]["marker_present"])
        self.assertIsNone(deps["httpx"]["constraint"])
        self.assertEqual(deps["pydantic"]["constraint"], "==2.12.0")
        self.assertNotIn("private-customer-package", json.dumps(data))
        self.assertTrue(all(record["directives_not_followed"].values()))

    def test_partial_custom_pyproject_preserves_constraints_without_resolving(self):
        self.write("pyproject.toml", '\n'.join([
            '[project]', 'name = "' + SECRET + '"', 'requires-python = ">=3.12,<3.14"',
            'dependencies = ["google-adk>=2.0,<3.0", "fastapi>=0.120", "customer-data==9"]',
            '[project.optional-dependencies]', 'custom = ["ag-ui-adk==0.7.0"]',
            '[dependency-groups]', 'test = ["pytest>=9"]',
            '[build-system]', 'build-backend = "' + SECRET + '"',
        ]))
        code, data = self.run_main()
        self.assertEqual(code, 0)
        record = data["project"]["manifests"][0]
        self.assertEqual(record["python_constraints"], [">=3.12,<3.14"])
        deps = {item["name"]: item for item in record["dependencies"]}
        self.assertEqual(deps["google-adk"]["constraint"], ">=2.0,<3.0")
        self.assertEqual(deps["google-adk"]["reference_status"], "unverified")
        self.assertIn("ag-ui-adk", deps)
        self.assertIn("pytest", deps)

    def test_poetry_versions_and_private_sources_are_sanitised(self):
        self.write("pyproject.toml", '\n'.join([
            '[tool.poetry.dependencies]', 'python = ">=3.11,<4.0"', 'google-adk = "2.8.0"',
            'google-genai = { version = "^2.19", source = "' + SECRET + '" }',
            'httpx = { git = "https://' + SECRET + '" }',
        ]))
        _, data = self.run_main()
        record = data["project"]["manifests"][0]
        self.assertEqual(record["python_constraints"], [">=3.11,<4.0"])
        deps = {item["name"]: item for item in record["dependencies"]}
        self.assertEqual(deps["google-adk"]["constraint"], "==2.8.0")
        self.assertIsNone(deps["google-genai"]["constraint"])
        self.assertIsNone(deps["httpx"]["constraint"])

    def test_client_stacks_are_distinct_and_scripts_and_registry_values_omitted(self):
        for mode, pins in inspector.CLIENT_REFERENCES.items():
            self.write(mode + "/package.json", json.dumps({
                "name": SECRET, "scripts": {"postinstall": "echo " + SECRET},
                "dependencies": {name: value for name, value in pins.items() if name != "node"},
                "devDependencies": {"custom-private": SECRET}, "engines": {"node": pins["node"]},
                "publishConfig": {"registry": "https://" + SECRET},
            }))
        code, data = self.run_main()
        self.assertEqual(code, 0)
        records = {item["path"]: item for item in data["project"]["manifests"]}
        for mode, react in (("json", "18.3.1"), ("agui", "19.2.1")):
            record = records[mode + "/package.json"]
            dep = next(item for item in record["dependencies"] if item["name"] == "react")
            self.assertEqual(dep["constraint"], react)
            self.assertEqual(dep["reference_matches"], [mode])

    def test_npm_urls_local_aliases_and_arbitrary_tags_are_unverified_and_redacted(self):
        self.write("package.json", json.dumps({"dependencies": {
            "react": "https://user:" + SECRET + "@example.invalid/react.tgz",
            "next": "file:../" + SECRET, "@ag-ui/client": "npm:" + SECRET,
            "typescript": SECRET, "vite": "^6.4.3",
        }, "packageManager": "pnpm@" + SECRET, "engines": {"node": SECRET}}))
        _, data = self.run_main()
        record = data["project"]["manifests"][0]
        deps = {item["name"]: item for item in record["dependencies"]}
        for name in ("react", "next", "@ag-ui/client", "typescript"):
            self.assertIsNone(deps[name]["constraint"])
            self.assertEqual(deps[name]["reference_status"], "unverified")
        self.assertEqual(deps["vite"]["constraint"], "^6.4.3")
        self.assertIsNone(record["package_manager"])

    def test_allowlisted_nested_override_versions_are_reported(self):
        self.write("package.json", json.dumps({"overrides": {
            "@ai-sdk/provider-utils": {"undici": "6.28.0"}, "next": {"postcss": "8.5.28"},
            "qs": "6.16.0", "customer": {"react": SECRET},
        }}))
        _, data = self.run_main()
        overrides = {item["name"]: item["constraint"] for item in data["project"]["manifests"][0]["dependencies"]}
        self.assertEqual(overrides, {"undici": "6.28.0", "postcss": "8.5.28", "qs": "6.16.0"})

    def test_version_files_validate_values_and_hide_unknown_tools(self):
        self.write(".python-version", "3.11.4\n")
        self.write(".nvmrc", "v22.12.0\n")
        self.write(".node-version", SECRET)
        self.write(".tool-versions", "python 3.12.2\nnodejs 22.12.0\nprivate " + SECRET)
        _, data = self.run_main()
        records = {item["path"]: item for item in data["project"]["manifests"]}
        self.assertEqual(records[".python-version"]["versions"], [{"runtime": "python", "version": "3.11.4"}])
        self.assertEqual(records[".nvmrc"]["versions"], [{"runtime": "node", "version": "22.12.0"}])
        self.assertEqual(records[".node-version"]["status"], "unverified")
        self.assertEqual(len(records[".tool-versions"]["versions"]), 2)

    def test_never_reads_env_source_or_lock_contents_and_never_executes_project(self):
        self.write("requirements.txt", "google-adk==2.8.0\n")
        for name in (".env", ".env.example", ".npmrc", "customer.json", "package-lock.json", "uv.lock"):
            self.write(name, SECRET)
        marker = self.root / "executed"
        evil = 'from pathlib import Path\nPath(' + repr(str(marker)) + ').write_text("executed")\n'
        self.write("sitecustomize.py", evil)
        self.write("setup.py", evil)
        self.write("google/__init__.py", evil)
        self.write("package.json", json.dumps({"scripts": {"postinstall": evil}}))
        real_open = inspector.os.open
        def guarded_open(path, *args, **kwargs):
            if Path(path).name in {".env", ".env.example", ".npmrc", "customer.json", "package-lock.json", "uv.lock", "setup.py", "sitecustomize.py", "__init__.py"}:
                raise AssertionError("non-allowlisted content was opened")
            return real_open(path, *args, **kwargs)
        with patch.object(inspector.os, "open", side_effect=guarded_open):
            code, data = self.run_main()
        self.assertEqual(code, 0)
        self.assertFalse(marker.exists())
        self.assertEqual({item["path"] for item in data["project"]["lockfiles"]}, {"package-lock.json", "uv.lock"})
        result, _ = self.cli()
        self.assertEqual(result.returncode, 0)
        self.assertFalse(marker.exists())

    def test_excluded_dependency_and_environment_directories_are_not_traversed(self):
        for directory in (".git", ".venv", "node_modules", ".next", ".env.production", "dist"):
            self.write(directory + "/requirements.txt", "google-adk==99.0\n" + SECRET)
        self.write("backend/requirements.txt", "google-adk==2.8.0")
        _, data = self.run_main()
        self.assertEqual([item["path"] for item in data["project"]["manifests"]], ["backend/requirements.txt"])

    def test_file_and_directory_symlinks_are_skipped_without_target_reads(self):
        outside = self.root / "outside"
        outside.mkdir()
        (outside / "requirements.txt").write_text("google-adk==99.0\n" + SECRET)
        (self.project / "requirements.txt").symlink_to(outside / "requirements.txt")
        (self.project / "external").symlink_to(outside, target_is_directory=True)
        (self.project / "loop").symlink_to(self.project, target_is_directory=True)
        code, data = self.run_main()
        self.assertEqual(code, 0)
        self.assertEqual(data["project"]["manifests"], [])
        self.assertEqual(data["project"]["counts"]["symlinks_skipped"], 3)

    def test_root_symlink_and_nonexistent_project_fail_without_path_disclosure(self):
        alias = self.root / "alias"
        alias.symlink_to(self.project, target_is_directory=True)
        for path in (alias, self.root / SECRET):
            stdout = io.StringIO()
            with redirect_stdout(stdout):
                code = inspector.main(["--project", str(path)])
            self.assertEqual(code, 2)
            self.assertNotIn(str(self.root), stdout.getvalue())
            self.assertNotIn(SECRET, stdout.getvalue())

    @unittest.skipUnless(hasattr(os, "mkfifo"), "platform has no named pipes")
    def test_manifest_named_pipe_is_never_opened_or_waited_on(self):
        os.mkfifo(self.project / "requirements.txt")
        result, data = self.cli()
        self.assertEqual(result.returncode, 0)
        self.assertEqual(data["project"]["manifests"], [])

    def test_control_characters_in_relative_paths_are_redacted(self):
        self.write("folder\n" + SECRET + "/requirements.txt", "google-adk==2.8.0")
        code, data = self.run_main()
        self.assertEqual(code, 0)
        self.assertEqual(data["project"]["manifests"][0]["path"], "[redacted-path]/requirements.txt")

    def test_invalid_manifests_fail_incomplete_without_echoing_contents(self):
        for name, text in (("package.json", '{"' + SECRET), ("pyproject.toml", '[project\n' + SECRET)):
            with self.subTest(name=name):
                path = self.write(name, text)
                code, data = self.run_main()
                self.assertEqual(code, 4)
                self.assertFalse(data["project"]["complete_within_scope"])
                self.assertEqual(data["project"]["manifests"][0]["status"], "unreadable_invalid_or_changed")
                path.unlink()

    def test_duplicate_package_fields_are_not_silently_overwritten(self):
        self.write("package.json", '{"dependencies":{"react":"18.3.1"},"dependencies":{"react":"19.2.1"}}')
        code, data = self.run_main()
        self.assertEqual(code, 4)
        self.assertEqual(data["project"]["warnings"], ["manifest_not_inspected"])

    def test_installed_metadata_is_not_assumed_to_be_target_environment(self):
        self.write("requirements.txt", "google-adk==1.0.0\n")
        code, data = self.run_main("--mode", "json", "--require-tested-stack")
        self.assertEqual(code, 0)
        self.assertEqual(data["interpreter"]["scope"], "invoking_interpreter_only")
        self.assertEqual(data["project"]["manifests"][0]["dependencies"][0]["constraint"], "==1.0.0")
        self.assertEqual(data["project"]["manifests"][0]["dependencies"][0]["reference_status"], "unverified")
        self.assertNotIn(str(self.root), json.dumps(data))

    def test_strict_gate_checks_only_packages_relevant_to_selected_mode(self):
        cases = {
            "json": {"google-adk", "google-genai"},
            "agui": {"google-adk", "google-genai", "ag-ui-adk", "ag-ui-protocol"},
            "managed-json": {"google-adk", "google-genai", "google-cloud-aiplatform"},
            "managed-agui": set(inspector.TESTED_PINS),
        }
        for mode, expected in cases.items():
            with self.subTest(mode=mode):
                code, data = self.run_main("--mode", mode, "--require-tested-stack", versions={name: None for name in inspector.TESTED_PINS if name not in expected})
                self.assertEqual(code, 0)
                self.assertEqual(set(data["tested_stack_gate"]["checked_packages"]), expected)
                failing = next(iter(expected))
                code, data = self.run_main("--mode", mode, "--require-tested-stack", versions={failing: None})
                self.assertEqual(code, 3)
                self.assertEqual(data["tested_stack_gate"]["failures"][0]["status"], "missing")

    def test_version_mismatch_is_unverified_not_claimed_incompatible(self):
        code, data = self.run_main("--mode", "json", "--require-tested-stack", versions={"google-adk": "3.0.0"})
        self.assertEqual(code, 3)
        self.assertEqual(data["tested_stack_gate"]["failures"][0]["status"], "different_from_tested")
        code, _ = self.run_main("--mode", "json", versions={"google-adk": "3.0.0"})
        self.assertEqual(code, 0)

    def test_suspicious_installed_versions_are_redacted_and_fail_strict(self):
        code, data = self.run_main("--mode", "managed-agui", "--require-tested-stack", versions={"google-adk": "2.8.0+" + SECRET})
        self.assertEqual(code, 3)
        record = next(item for item in data["installed_python"] if item["name"] == "google-adk")
        self.assertIsNone(record["version"])
        self.assertEqual(record["status"], "unverified")

    def test_strict_gate_requires_explicit_mode(self):
        with redirect_stderr(io.StringIO()), self.assertRaises(SystemExit) as error:
            inspector.main(["--project", str(self.project), "--require-tested-stack"])
        self.assertEqual(error.exception.code, 2)

    def test_walk_and_depth_bounds_make_partial_inspection_explicit(self):
        self.write("a/b/requirements.txt", "google-adk==2.8.0")
        limited = dict(inspector.LIMITS, max_depth=0)
        data = inspector.scan_project(self.project, limits=limited)
        self.assertFalse(data["complete_within_scope"])
        self.assertIn("depth_limit_reached", data["warnings"])
        for index in range(10):
            self.write("file" + str(index), SECRET)
        data = inspector.scan_project(self.project, limits=dict(inspector.LIMITS, max_entries=3))
        self.assertLessEqual(data["counts"]["entries"], 3)
        self.assertIn("walk_limit_reached", data["warnings"])

    def test_byte_and_manifest_limits_never_return_partial_raw_content(self):
        self.write("requirements.txt", "google-adk==2.8.0\n" + SECRET)
        data = inspector.scan_project(self.project, limits=dict(inspector.LIMITS, max_file_bytes=5))
        self.assertEqual(data["counts"]["bytes_read"], 0)
        self.assertEqual(data["manifests"][0]["status"], "size_limit_not_read")
        self.assertNotIn(SECRET, json.dumps(data))
        self.write("frontend/package.json", "{}")
        data = inspector.scan_project(self.project, limits=dict(inspector.LIMITS, max_manifests=1))
        self.assertEqual(len(data["manifests"]), 1)
        self.assertIn("manifest_limit_reached", data["warnings"])

    def test_dry_run_repeat_and_clean_copy_have_identical_output_and_no_writes(self):
        self.write("requirements.txt", "google-adk==2.8.0")
        self.write("frontend/package.json", '{"dependencies":{"react":"18.3.1"}}')
        snapshot = {str(path.relative_to(self.project)): hashlib.sha256(path.read_bytes()).hexdigest()
                    for path in self.project.rglob("*") if path.is_file()}
        portable = self.root / "detached" / "inspect_project.py"
        portable.parent.mkdir()
        shutil.copyfile(SCRIPT, portable)
        first, a = self.cli(script=portable)
        second, b = self.cli("--dry-run", script=portable)
        third, c = self.cli(script=portable)
        self.assertEqual((first.returncode, second.returncode, third.returncode), (0, 0, 0))
        self.assertEqual(a, b)
        self.assertEqual(b, c)
        after = {str(path.relative_to(self.project)): hashlib.sha256(path.read_bytes()).hexdigest()
                 for path in self.project.rglob("*") if path.is_file()}
        self.assertEqual(snapshot, after)
        self.assertFalse(list(self.root.rglob("__pycache__")))


if __name__ == "__main__":
    unittest.main()
