"""Offline subprocess contract tests; never contact Google Cloud."""

import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


HELPER = Path(__file__).resolve().parents[1] / "scripts" / "inspect_project.py"


class InspectProjectTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name) / "project"
        self.root.mkdir()

    def tearDown(self):
        self.temp.cleanup()

    def write(self, name, content):
        target = self.root / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        return target

    def run_helper(self, *args, empty_path=False):
        environment = dict(os.environ)
        if empty_path:
            environment["PATH"] = ""
        return subprocess.run([sys.executable, str(HELPER), "--root", str(self.root), *args],
                              text=True, capture_output=True, env=environment, timeout=15)

    def output(self, *args, expected=0, **kwargs):
        result = self.run_helper(*args, **kwargs)
        self.assertEqual(result.returncode, expected, result.stderr)
        return json.loads(result.stdout)

    def snapshot(self):
        return {str(path.relative_to(self.root)): (hashlib.sha256(path.read_bytes()).hexdigest(), path.stat().st_mtime_ns)
                for path in self.root.rglob("*") if path.is_file() and not path.is_symlink()}

    def test_help_documents_contract_and_exit_codes(self):
        result = subprocess.run([sys.executable, str(HELPER), "--help"], text=True, capture_output=True, timeout=15)
        self.assertEqual(result.returncode, 0)
        for term in ("--dry-run", "--require-baseline", "Exit 0", "2:", "3:", "offline", ".env"):
            self.assertIn(term, result.stdout)

    def test_unsupported_python_gate_reports_required_version(self):
        # Exercise the refusal branch under a simulated version; this is not a Python 3.10 run.
        probe = 'import sys,runpy; sys.version_info=(3,10,0); runpy.run_path(sys.argv[1],run_name="__main__")'
        result = subprocess.run([sys.executable, "-c", probe, str(HELPER), "--help"],
                                text=True, capture_output=True, timeout=15)
        self.assertEqual(result.returncode, 2)
        self.assertIn("requires Python 3.11 or newer", result.stderr)

    def test_dry_run_is_identical_and_does_not_write_or_execute(self):
        self.write("requirements.txt", "google-adk==2.8.0\n")
        self.write("agent.py", "raise RuntimeError('MUST_NOT_EXECUTE')\n")
        self.write(".env", "SECRET=DO_NOT_EMIT\n")
        before = self.snapshot()
        first = self.run_helper("--mode", "cloud-run")
        second = self.run_helper("--mode", "cloud-run", "--dry-run")
        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertEqual(first.stdout, second.stdout)
        self.assertEqual(before, self.snapshot())
        self.assertNotIn("DO_NOT_EMIT", first.stdout + first.stderr)
        self.assertTrue(json.loads(first.stdout)["configuration_file_presence"]["dotenv"])
        self.assertFalse((self.root / "__pycache__").exists())

    def test_pyproject_and_includes_distinguish_pins_ranges_and_python(self):
        self.write("pyproject.toml", '[project]\nrequires-python = ">=3.11,<3.14"\ndependencies = ["google-adk==2.8.0"]\n')
        self.write("requirements.txt", "-r dependencies/runtime.txt\n")
        self.write("dependencies/runtime.txt", "google-cloud-aiplatform[agent_engines]==1.153.1\n")
        self.write("uv.lock", "SECRET_LOCK_DATA")
        report = self.output("--mode", "agent-runtime", "--require-baseline")
        self.assertTrue(report["baseline_gate_passed"])
        self.assertEqual(report["packages"]["google-adk"]["exact_pins"], ["2.8.0"])
        self.assertEqual(report["python"]["declared_requirements"][0]["specifier"], ">=3.11,<3.14")
        self.assertIn("uv", report["package_manager_indicators"])
        self.assertEqual(len(report["manifests"]), 3)

    def test_require_baseline_missing_unpinned_different_and_conflicting(self):
        for declaration, reason in (
            ("", "no_declaration_found"),
            ("google-adk>=2.8,<3\n", "declaration_not_an_exact_pin"),
            ("google-adk==9.8.7\n", "different_from_recorded_baseline"),
            ("google-adk==2.8.0\ngoogle-adk==2.7.0\n", "conflicting_exact_pins"),
        ):
            with self.subTest(reason=reason):
                self.write("requirements.txt", declaration)
                report = self.output("--mode", "cloud-run")
                self.assertEqual(report["packages"]["google-adk"]["status"], "unverified")
                self.assertIn(reason, report["packages"]["google-adk"]["reasons"])
                self.output("--mode", "cloud-run", "--require-baseline", expected=3)

    def test_runtime_requires_sdk_and_conditional_pins_need_review(self):
        self.write("requirements.txt", 'google-adk==2.8.0; python_version >= "3.11"\n')
        report = self.output("--mode", "agent-runtime", "--require-baseline", expected=3)
        self.assertIn("conditional_or_optional_declaration_requires_review", report["packages"]["google-adk"]["reasons"])
        self.assertTrue(report["packages"]["google-cloud-aiplatform"]["required_for_selected_mode"])

    def test_constraints_cannot_hide_a_conflicting_pin(self):
        for option in ("-c ", "--constraint=", "--constraint "):
            with self.subTest(option=option):
                self.write("requirements.txt", "google-adk==2.8.0\n" + option + "constraints.txt\n")
                self.write("constraints.txt", "google-adk==2.7.0\n")
                report = self.output("--mode", "cloud-run", "--require-baseline", expected=3)
                self.assertIn("conflicting_exact_pins", report["packages"]["google-adk"]["reasons"])
                self.write("constraints.txt", "google-adk==2.8.0\n")
                self.output("--mode", "cloud-run", "--require-baseline")

    def test_constraint_alone_is_not_a_runtime_dependency(self):
        self.write("requirements.txt", "-c constraints.txt\n")
        self.write("constraints.txt", "google-adk==2.8.0\n")
        report = self.output("--mode", "cloud-run", "--require-baseline", expected=3)
        self.assertIn("only_constraint_declarations_found", report["packages"]["google-adk"]["reasons"])

    def test_sensitive_specifications_and_filenames_never_echo(self):
        secret = "CONFIDENTIAL_ACCESS_TOKEN_987654"
        self.write(f"requirements-{secret}.txt", f"google-adk @ https://user:{secret}@example.test/private.whl\n--index-url https://{secret}@example.test\n")
        self.write("pyproject.toml", f'[project]\nrequires-python = "{secret}"\n')
        result = self.run_helper("--mode", "cloud-run")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn(secret, result.stdout + result.stderr)
        self.assertEqual(json.loads(result.stdout)["packages"]["google-adk"]["declarations"][0]["kind"], "direct_reference")

    def test_malformed_toml_errors_do_not_echo_secret(self):
        self.write("pyproject.toml", '[project]\ndependencies = ["SECRET_PARSE_VALUE"\n')
        result = self.run_helper()
        self.assertEqual(result.returncode, 2)
        self.assertNotIn("SECRET_PARSE_VALUE", result.stdout + result.stderr)
        self.assertIn("invalid TOML", result.stderr)

    def test_invalid_arguments_do_not_echo_secrets(self):
        for args in (("--mode", "SECRET_BAD_MODE"), ("--SECRET_BAD_FLAG",),
                     ("--project", "SECRET_BAD_PROJECT", "--region", "us-central1", "--account", "reader@example.com", "--mode", "gke")):
            result = self.run_helper(*args)
            self.assertEqual(result.returncode, 2)
            self.assertNotIn("SECRET_BAD", result.stdout + result.stderr)

    def test_symlink_files_and_directories_are_skipped(self):
        outside = Path(self.temp.name) / "outside"
        outside.mkdir()
        (outside / "requirements.txt").write_text("google-adk==9.8.7\n")
        (self.root / "requirements.txt").symlink_to(outside / "requirements.txt")
        (self.root / "external").symlink_to(outside, target_is_directory=True)
        report = self.output()
        self.assertEqual(report["coverage"]["symlinks_skipped"], 2)
        self.assertEqual(report["manifests"], [])

    def test_includes_refuse_symlinks_outside_paths_and_dotenv(self):
        outside = Path(self.temp.name) / "outside.txt"
        outside.write_text("SECRET_EXTERNAL_MANIFEST")
        (self.root / "linked.txt").symlink_to(outside)
        self.write(".env", "SECRET_ENV_CONTENT")
        self.write(".env.private.txt", "SECRET_ENV_CONTENT")
        for include in ("linked.txt", "../outside.txt", ".env", ".env.private.txt", "https://SECRET_URL.test/a.txt"):
            with self.subTest(include=include):
                self.write("requirements.txt", "-r " + include + "\n")
                result = self.run_helper()
                self.assertEqual(result.returncode, 2)
                self.assertNotIn("SECRET_", result.stdout + result.stderr)

    def test_include_cycle_is_bounded(self):
        self.write("requirements.txt", "-r second.txt\ngoogle-adk==2.8.0\n")
        self.write("second.txt", "-r requirements.txt\n")
        report = self.output("--mode", "cloud-run", "--require-baseline")
        self.assertEqual(len(report["manifests"]), 2)

    def test_whitespace_exact_pin_and_optional_scope(self):
        self.write("requirements.txt", "google-adk == 2.8.0\n")
        report = self.output("--mode", "cloud-run", "--require-baseline")
        self.assertEqual(report["packages"]["google-adk"]["exact_pins"], ["2.8.0"])
        self.write("pyproject.toml", '[project.optional-dependencies]\ntest = ["google-adk==2.8.0"]\n')
        report = self.output("--mode", "cloud-run", "--require-baseline", expected=3)
        self.assertIn("conditional_or_optional_declaration_requires_review", report["packages"]["google-adk"]["reasons"])

    def test_depth_limit_is_visible_and_cannot_pass_baseline_gate(self):
        self.write("requirements.txt", "google-adk==2.8.0\n")
        self.write("a/b/c/d/e/requirements.txt", "google-adk==9.8.7\n")
        report = self.output("--mode", "cloud-run", "--require-baseline", expected=3)
        self.assertTrue(report["coverage"]["depth_limit_reached"])
        self.assertIn("inspection_depth_limit_reached", report["packages"]["google-adk"]["reasons"])

    def test_invalid_utf8_and_unreadable_manifest_are_sanitized_errors(self):
        path = self.write("requirements.txt", "google-adk==2.8.0\n")
        path.write_bytes(b"SECRET_INVALID_UTF8\xff")
        result = self.run_helper()
        self.assertEqual(result.returncode, 2)
        self.assertNotIn("SECRET_INVALID_UTF8", result.stderr)
        path.write_text("SECRET_UNREADABLE")
        path.chmod(0)
        try:
            if os.geteuid() != 0:
                result = self.run_helper()
                self.assertEqual(result.returncode, 2)
                self.assertNotIn("SECRET_UNREADABLE", result.stderr)
        finally:
            path.chmod(0o600)

    def test_missing_include_and_oversized_manifest_exit_two(self):
        self.write("requirements.txt", "-r SECRET_MISSING.txt\n")
        result = self.run_helper()
        self.assertEqual(result.returncode, 2)
        self.assertNotIn("SECRET_MISSING", result.stderr)
        self.write("requirements.txt", "#" * 131073)
        self.assertEqual(self.run_helper().returncode, 2)

    def test_manifest_count_limit(self):
        for index in range(65):
            self.write(f"requirements-{index}.txt", "google-adk==2.8.0\n")
        result = self.run_helper()
        self.assertEqual(result.returncode, 2)
        self.assertIn("Manifest count limit", result.stderr)

    def test_missing_prerequisites_are_reported_without_execution(self):
        report = self.output("--mode", "gke", empty_path=True)
        for prerequisite in report["prerequisites"].values():
            self.assertFalse(prerequisite["available_on_path"])
        self.assertTrue(report["prerequisites"]["kubectl"]["required_for_selected_mode"])
        self.assertEqual(report["network_calls"], 0)

    def test_architecture_signals_are_presence_only(self):
        self.write("k8s/deployment.yaml", "SECRET_YAML")
        self.write("Dockerfile", "SECRET_DOCKERFILE")
        report = self.output()
        self.assertIn("kubernetes_directory", report["architecture_hints"])
        self.assertTrue(report["configuration_file_presence"]["dockerfile"])
        self.assertNotIn("SECRET_", json.dumps(report))

    def test_targeted_plan_has_explicit_scopes_and_never_executes(self):
        for mode, count in (("cloud-run", 4), ("agent-runtime", 3), ("gke", 4)):
            with self.subTest(mode=mode):
                report = self.output("--mode", mode, "--project", "sample-project-123", "--region", "us-central1", "--account", "reader@example.com", empty_path=True)
                commands = report["planned_read_only_cloud_commands"]
                self.assertEqual(len(commands), count)
                for command in commands:
                    self.assertFalse(command["executed"])
                    self.assertIn("--account=reader@example.com", command["argv"])
                    self.assertIn("--project=sample-project-123", command["argv"])
                    self.assertIn("--billing-project=sample-project-123", command["argv"])
                self.assertEqual(commands[0]["argv"][:4], ["gcloud", "projects", "describe", "sample-project-123"])
                if count == 4:
                    self.assertIn("--region=us-central1", commands[-1]["argv"])

    def test_partial_auto_and_unsafe_targets_are_rejected(self):
        for args in (
            ("--project", "sample-project-123"),
            ("--project", "sample-project-123", "--region", "us-central1", "--account", "reader@example.com"),
            ("--mode", "gke", "--project", "sample-project-123", "--region", "global", "--account", "reader@example.com"),
            ("--mode", "gke", "--project", "sample-project-123", "--region", "us-central1", "--account", "$(SECRET_COMMAND)@example.com"),
        ):
            result = self.run_helper(*args)
            self.assertEqual(result.returncode, 2)
            self.assertNotIn("SECRET_COMMAND", result.stderr)


if __name__ == "__main__":
    unittest.main()
