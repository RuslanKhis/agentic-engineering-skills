"""Offline inspector contracts; no application imports or provider calls."""
# Adapted from deploy-adk-on-google-cloud. Copyright (c) 2026 RuslanKhis.
# SPDX-License-Identifier: MIT

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
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return path

    def run_helper(self, *args):
        environment = dict(os.environ, PATH="", PYTHONDONTWRITEBYTECODE="1")
        return subprocess.run(
            [sys.executable, str(HELPER), "--root", str(self.root), *args],
            text=True, capture_output=True, env=environment, timeout=15,
        )

    def report(self, *args, expected=0):
        result = self.run_helper(*args)
        self.assertEqual(result.returncode, expected, result.stderr)
        return json.loads(result.stdout)

    def snapshot(self):
        return {
            str(path.relative_to(self.root)): (
                hashlib.sha256(path.read_bytes()).hexdigest(),
                path.stat().st_mtime_ns,
            )
            for path in self.root.rglob("*")
            if path.is_file() and not path.is_symlink()
        }

    def test_help_and_supported_modes(self):
        result = subprocess.run(
            [sys.executable, str(HELPER), "--help"],
            text=True, capture_output=True, timeout=15,
        )
        self.assertEqual(result.returncode, 0)
        for term in ("--dry-run", "--require-baseline", "Exit 0", "2:",
                     "3:", "offline", ".env", "application", "cloud-run", "agent-runtime", "gke"):
            self.assertIn(term, result.stdout)
        for mode in ("auto", "application", "cloud-run"):
            self.write("requirements.txt", "google-adk==2.8.0\n")
            self.assertTrue(self.report("--mode", mode, "--require-baseline")
                            ["baseline_gate_passed"])

    def runtime_requirements(self, sdk="google-cloud-aiplatform[agent_engines]==1.153.1",
                             genai="google-genai==2.19.0"):
        return "\n".join(("google-adk[a2a]==2.8.0", sdk, genai)) + "\n"

    def test_agent_runtime_requires_three_exact_unconditional_direct_pins(self):
        self.write("requirements.txt", self.runtime_requirements())
        before = self.snapshot()
        report = self.report("--mode", "agent-runtime", "--require-baseline", "--dry-run")
        required = {name for name, item in report["packages"].items()
                    if item["required_for_selected_mode"]}
        self.assertEqual(required, {"google-adk", "google-cloud-aiplatform", "google-genai"})
        self.assertTrue(report["baseline_gate_passed"])
        self.assertEqual(report["packages"]["google-cloud-aiplatform"]["recorded_baseline"], "1.153.1")
        self.assertEqual(report["packages"]["google-genai"]["recorded_baseline"], "2.19.0")
        extras = report["packages"]["google-cloud-aiplatform"]["declarations"][0]["known_extras"]
        self.assertEqual(extras, {"adk": False, "agent_engines": True})
        self.assertEqual(before, self.snapshot())

    def test_runtime_directory_hints_do_not_change_auto_or_part1_gates(self):
        self.write("requirements.txt", "google-adk==2.8.0\ngoogle-genai==2.23.0\n")
        self.write("agent-runtime/agent.py", "SECRET_RUNTIME_SOURCE")
        self.write("agent-engine/deploy.sh", "SECRET_RUNTIME_SOURCE")
        self.write("cloud-run/main.py", "SECRET_RUNTIME_SOURCE")
        for mode in ("auto", "application", "cloud-run"):
            with self.subTest(mode=mode):
                report = self.report("--mode", mode, "--require-baseline")
                required = {name for name, item in report["packages"].items()
                            if item["required_for_selected_mode"]}
                self.assertEqual(required, {"google-adk"})
                self.assertIn("agent_runtime_directory", report["architecture_hints"])
                self.assertIn("cloud_run_directory", report["architecture_hints"])
                self.assertNotIn("other_hosting_directory_requires_scope_review", report["architecture_hints"])
                self.assertNotIn("SECRET_", json.dumps(report))
        report = self.report("--mode", "agent-runtime", "--require-baseline", expected=3)
        self.assertIn("no_declaration_found", report["packages"]["google-cloud-aiplatform"]["reasons"])
        self.assertIn("different_from_recorded_baseline", report["packages"]["google-genai"]["reasons"])

    def test_runtime_unverified_sdk_declarations_remain_unchanged(self):
        for sdk, reason in (
            ("", "no_declaration_found"),
            ("google-cloud-aiplatform>=1.153.1", "declaration_not_an_exact_pin"),
            ("google-cloud-aiplatform==1.152.0", "different_from_recorded_baseline"),
            ('google-cloud-aiplatform==1.153.1; python_version >= "3.11"',
             "conditional_or_optional_declaration_requires_review"),
            ("google-cloud-aiplatform==1.153.1\ngoogle-cloud-aiplatform==1.152.0",
             "conflicting_exact_pins"),
        ):
            with self.subTest(reason=reason):
                self.write("requirements.txt", self.runtime_requirements(sdk=sdk))
                before = self.snapshot()
                report = self.report("--mode", "agent-runtime", "--require-baseline", expected=3)
                self.assertIn(reason, report["packages"]["google-cloud-aiplatform"]["reasons"])
                self.assertEqual(before, self.snapshot())

    def test_runtime_optional_and_constraint_only_pins_do_not_pass(self):
        self.write("pyproject.toml", '''[project]
dependencies = ["google-adk==2.8.0", "google-genai==2.19.0"]
[project.optional-dependencies]
host = ["google-cloud-aiplatform[agent_engines]==1.153.1"]
''')
        report = self.report("--mode", "agent-runtime", "--require-baseline", expected=3)
        self.assertIn("conditional_or_optional_declaration_requires_review",
                      report["packages"]["google-cloud-aiplatform"]["reasons"])
        (self.root / "pyproject.toml").unlink()
        self.write("requirements.txt", "google-adk==2.8.0\n-c constraints.txt\n")
        self.write("constraints.txt", "google-cloud-aiplatform==1.153.1\ngoogle-genai==2.19.0\n")
        report = self.report("--mode", "agent-runtime", "--require-baseline", expected=3)
        for package in ("google-cloud-aiplatform", "google-genai"):
            self.assertIn("only_constraint_declarations_found", report["packages"][package]["reasons"])

    def test_runtime_genai_is_a_gate_while_part1_preserves_target_pins(self):
        for declaration in ("", "google-genai>=2.19,<3", "google-genai==2.23.0",
                            'google-genai==2.19.0; python_version >= "3.11"'):
            with self.subTest(declaration=declaration):
                self.write("requirements.txt", self.runtime_requirements(genai=declaration))
                before = self.snapshot()
                report = self.report("--mode", "agent-runtime", "--require-baseline", expected=3)
                self.assertEqual(report["packages"]["google-genai"]["status"], "unverified")
                self.assertTrue(self.report("--mode", "application", "--require-baseline")
                                ["baseline_gate_passed"])
                self.assertEqual(before, self.snapshot())

    def test_known_incompatible_adk_extra_has_fixed_reason_and_mode_scope(self):
        self.write("requirements.txt", self.runtime_requirements(
            sdk="google-cloud-aiplatform[ADK,agent-engines]==1.153.1"))
        before = self.snapshot()
        for mode in ("agent-runtime", "gke"):
            with self.subTest(mode=mode):
                report = self.report("--mode", mode, "--require-baseline", expected=3)
                sdk = report["packages"]["google-cloud-aiplatform"]
                self.assertIn("adk_extra_conflicts_with_recorded_adk_baseline", sdk["reasons"])
                self.assertEqual(sdk["declarations"][0]["known_extras"],
                                 {"adk": True, "agent_engines": True})
        self.assertEqual(before, self.snapshot())
        for mode in ("auto", "application", "cloud-run"):
            self.assertTrue(self.report("--mode", mode, "--require-baseline")["baseline_gate_passed"])

    def test_unknown_packages_and_extras_are_never_echoed(self):
        secret = "CONFIDENTIAL_EXTRA_987654"
        self.write("requirements.txt", self.runtime_requirements(
            sdk=f"google-cloud-aiplatform[agent_engines,{secret}]==1.153.1") +
            f"{secret}[{secret}]==123.456.789\n")
        result = self.run_helper("--mode", "agent-runtime", "--require-baseline")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn(secret, result.stdout + result.stderr)
        self.assertNotIn("123.456.789", result.stdout)
        sdk = json.loads(result.stdout)["packages"]["google-cloud-aiplatform"]
        self.assertEqual(sdk["declarations"][0]["known_extras"], {"adk": False, "agent_engines": True})

    def test_poetry_sdk_table_remains_unparsed_but_flags_known_extra_without_leaks(self):
        self.write("pyproject.toml", '''[tool.poetry.dependencies]
google-adk = "2.8.0"
google-genai = "2.19.0"
google-cloud-aiplatform = {version="1.153.1", extras=["adk", "SECRET_EXTRA"]}
''')
        result = self.run_helper("--mode", "agent-runtime", "--require-baseline")
        self.assertEqual(result.returncode, 3, result.stderr)
        self.assertNotIn("SECRET_EXTRA", result.stdout + result.stderr)
        sdk = json.loads(result.stdout)["packages"]["google-cloud-aiplatform"]
        self.assertIn("declaration_not_an_exact_pin", sdk["reasons"])
        self.assertIn("adk_extra_conflicts_with_recorded_adk_baseline", sdk["reasons"])
        self.assertEqual(sdk["declarations"][0]["kind"], "unparsed")

    def test_gke_requires_two_pins_and_does_not_impose_a_genai_version(self):
        for declaration in ("", "google-genai>=2.19,<3", "google-genai==2.23.0",
                            "google-genai==2.19.0"):
            with self.subTest(declaration=declaration):
                self.write("requirements.txt", self.runtime_requirements(genai=declaration))
                before = self.snapshot()
                report = self.report("--mode", "gke", "--require-baseline", "--dry-run")
                required = {name for name, item in report["packages"].items()
                            if item["required_for_selected_mode"]}
                self.assertEqual(required, {"google-adk", "google-cloud-aiplatform"})
                self.assertTrue(report["baseline_gate_passed"])
                self.assertEqual(report["packages"]["google-cloud-aiplatform"]
                                 ["recorded_baseline"], "1.153.1")
                self.assertIsNone(report["packages"]["google-genai"]["recorded_baseline"])
                self.assertEqual(before, self.snapshot())
                runtime = self.report("--mode", "agent-runtime", "--require-baseline",
                                      expected=0 if declaration == "google-genai==2.19.0" else 3)
                self.assertTrue(runtime["packages"]["google-genai"]["required_for_selected_mode"])

    def test_gke_missing_or_unverified_sdk_does_not_pass_or_rewrite(self):
        for sdk, reason in (
            ("", "no_declaration_found"),
            ("google-cloud-aiplatform>=1.153.1", "declaration_not_an_exact_pin"),
            ("google-cloud-aiplatform==1.152.0", "different_from_recorded_baseline"),
            ('google-cloud-aiplatform==1.153.1; python_version >= "3.11"',
             "conditional_or_optional_declaration_requires_review"),
            ("google-cloud-aiplatform==1.153.1\ngoogle-cloud-aiplatform==1.152.0",
             "conflicting_exact_pins"),
        ):
            with self.subTest(reason=reason):
                self.write("requirements.txt", "google-adk==2.8.0\n" + sdk + "\n")
                before = self.snapshot()
                report = self.report("--mode", "gke", "--require-baseline", expected=3)
                self.assertIn(reason, report["packages"]["google-cloud-aiplatform"]["reasons"])
                self.assertFalse(report["baseline_gate_passed"])
                self.assertEqual(before, self.snapshot())

    def test_gke_optional_and_constraint_only_sdk_do_not_pass(self):
        self.write("pyproject.toml", '''[project]
dependencies = ["google-adk==2.8.0"]
[project.optional-dependencies]
host = ["google-cloud-aiplatform[agent-engines]==1.153.1"]
''')
        report = self.report("--mode", "gke", "--require-baseline", expected=3)
        self.assertIn("conditional_or_optional_declaration_requires_review",
                      report["packages"]["google-cloud-aiplatform"]["reasons"])
        (self.root / "pyproject.toml").unlink()
        self.write("requirements.txt", "google-adk==2.8.0\n-c constraints.txt\n")
        self.write("constraints.txt", "google-cloud-aiplatform[agent-engines]==1.153.1\n")
        report = self.report("--mode", "gke", "--require-baseline", expected=3)
        self.assertIn("only_constraint_declarations_found",
                      report["packages"]["google-cloud-aiplatform"]["reasons"])

    def test_gke_hints_are_content_free_and_do_not_select_the_gate(self):
        requirements = "google-adk==2.8.0\n"
        self.write("requirements.txt", requirements)
        for name in ("gke/app.py", "gke/k8s/deployment.yaml", "gke/k8s/service.yml",
                     "gke/k8s/hpa.yaml", "gke/k8s/pdb.yml",
                     "gke/k8s/vpa-recommendation-only.yaml"):
            self.write(name, "SECRET_CONFIGURATION_VALUE: [INVALID YAML")
        before = self.snapshot()
        for mode in ("auto", "application", "cloud-run"):
            with self.subTest(mode=mode):
                report = self.report("--mode", mode, "--require-baseline")
                self.assertIn("gke_directory", report["architecture_hints"])
                self.assertIn("kubernetes_directory", report["architecture_hints"])
                self.assertTrue(all(report["configuration_file_presence"][key] for key in
                                    ("kubernetes_deployment_candidate", "kubernetes_service_candidate",
                                     "kubernetes_hpa_candidate", "kubernetes_pdb_candidate",
                                     "kubernetes_vpa_candidate")))
                required = {name for name, item in report["packages"].items()
                            if item["required_for_selected_mode"]}
                self.assertEqual(required, {"google-adk"})
                self.assertEqual(report["coverage"]["manifest_bytes_read"], len(requirements))
                self.assertNotIn("SECRET_", json.dumps(report))
        first = self.run_helper("--mode", "gke")
        second = self.run_helper("--mode", "gke", "--dry-run")
        self.assertEqual(first.returncode, 0)
        self.assertEqual(first.stdout, second.stdout)
        self.assertFalse(json.loads(first.stdout)["baseline_gate_passed"])
        self.assertEqual(before, self.snapshot())

    def test_unsupported_python_refuses_before_tomllib_import(self):
        # Simulates the version guard, not an actual Python 3.10 installation.
        probe = ("import sys,runpy;sys.version_info=(3,10,0);"
                 "runpy.run_path(sys.argv[1],run_name='__main__')")
        result = subprocess.run(
            [sys.executable, "-c", probe, str(HELPER), "--help"],
            text=True, capture_output=True, timeout=15,
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("requires Python 3.11 or newer", result.stderr)

    def test_dry_run_is_identical_and_never_reads_code_env_or_lockfiles(self):
        self.write("requirements.txt", "google-adk==2.8.0\n")
        marker = Path(self.temp.name) / "EXECUTED"
        self.write("agent.py", f"open({str(marker)!r}, 'w').write('bad')\n")
        self.write(".env", "SECRET_DOTENV_VALUE\n")
        self.write(".env.example", "SECRET_TEMPLATE_VALUE\n")
        self.write("uv.lock", "SECRET_LOCK_VALUE\n")
        self.write("Dockerfile", "SECRET_BUILD_VALUE\n")
        before = self.snapshot()
        first = self.run_helper()
        second = self.run_helper("--dry-run")
        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertEqual(first.stdout, second.stdout)
        self.assertEqual(before, self.snapshot())
        self.assertFalse(marker.exists())
        self.assertFalse((self.root / "__pycache__").exists())
        self.assertNotIn("SECRET_", first.stdout + first.stderr)
        report = json.loads(first.stdout)
        self.assertEqual(report["network_calls"], 0)
        self.assertEqual(report["writes"], 0)
        self.assertTrue(report["configuration_file_presence"]["dotenv"])
        self.assertTrue(report["configuration_file_presence"]["dotenv_example"])
        self.assertIn("uv", report["package_manager_indicators"])

    def test_pep621_optional_dependencies_ranges_and_python(self):
        self.write("pyproject.toml", '''[project]
requires-python = ">=3.11,<3.14"
dependencies = ["google-adk==2.8.0", "pandas>=2.2,<4", "google-genai==2.23.0"]
[project.optional-dependencies]
test = ["pydantic>=2.12,<3"]
''')
        report = self.report("--mode", "application", "--require-baseline")
        self.assertEqual(report["packages"]["google-genai"]["exact_pins"], ["2.23.0"])
        self.assertIsNone(report["packages"]["google-genai"]["recorded_baseline"])
        self.assertFalse(report["packages"]["pandas"]["required_for_selected_mode"])
        self.assertEqual(report["packages"]["pandas"]["declarations"][0]["specifier"], ">=2.2,<4")
        self.assertEqual(report["packages"]["pydantic"]["declarations"][0]["scope"], "optional")
        self.assertEqual(report["python"]["declared_requirements"][0]["specifier"], ">=3.11,<3.14")
        self.assertEqual(report["python"]["requirement_satisfaction"], "not_evaluated")

    def test_preserve_missing_different_ranged_conditional_and_conflicting_pins(self):
        for text, reason in (
            ("", "no_declaration_found"),
            ("google-adk>=2.8,<3", "declaration_not_an_exact_pin"),
            ("google-adk==9.8.7", "different_from_recorded_baseline"),
            ('google-adk==2.8.0; python_version >= "3.11"',
             "conditional_or_optional_declaration_requires_review"),
            ("google-adk==2.8.0\ngoogle-adk==2.7.0", "conflicting_exact_pins"),
        ):
            with self.subTest(reason=reason):
                self.write("requirements.txt", text + "\n")
                before = self.snapshot()
                report = self.report("--require-baseline", expected=3)
                self.assertIn(reason, report["packages"]["google-adk"]["reasons"])
                self.assertEqual(report["packages"]["google-adk"]["status"], "unverified")
                self.assertEqual(before, self.snapshot())

    def test_optional_adk_does_not_satisfy_runtime_baseline(self):
        self.write("pyproject.toml", '[project.optional-dependencies]\ntest=["google-adk==2.8.0"]\n')
        self.assertFalse(self.report("--require-baseline", expected=3)["baseline_gate_passed"])

    def test_poetry_and_normalised_names(self):
        self.write("pyproject.toml", '''[tool.poetry.dependencies]
python = "^3.11"
Google_ADK = "2.8.0"
pydantic = ">=2.12,<3"
''')
        report = self.report("--require-baseline")
        self.assertIn("poetry", report["package_manager_indicators"])
        self.assertEqual(report["packages"]["google-adk"]["exact_pins"], ["2.8.0"])

    def test_constraints_includes_cycles_and_dual_scope(self):
        self.write("requirements.txt", "-c shared.txt\n-r shared.txt\n")
        self.write("shared.txt", "-r requirements.txt\ngoogle-adk == 2.8.0\n")
        report = self.report("--require-baseline")
        self.assertEqual(len(report["manifests"]), 2)
        self.assertEqual({item["scope"] for item in report["packages"]["google-adk"]["declarations"]},
                         {"runtime", "constraint"})
        self.write("requirements.txt", "-c shared.txt\n")
        self.write("shared.txt", "google-adk==2.8.0\n")
        report = self.report("--require-baseline", expected=3)
        self.assertIn("only_constraint_declarations_found", report["packages"]["google-adk"]["reasons"])
        self.write("requirements.txt", "google-adk==2.8.0\n--constraint=shared.txt\n")
        self.write("shared.txt", "google-adk==2.7.0\n")
        report = self.report("--require-baseline", expected=3)
        self.assertIn("conflicting_exact_pins", report["packages"]["google-adk"]["reasons"])

    def test_secrets_urls_paths_and_unknown_arguments_are_never_echoed(self):
        secret = "CONFIDENTIAL_TOKEN_987654"
        self.write(f"requirements-{secret}.txt", f"google-adk @ https://user:{secret}@example.invalid/pkg.whl\n")
        self.write("pyproject.toml", f'[project]\nrequires-python="{secret}"\n')
        result = self.run_helper()
        self.assertEqual(result.returncode, 0)
        self.assertNotIn(secret, result.stdout + result.stderr)
        self.assertNotIn(str(self.root), result.stdout + result.stderr)
        self.assertEqual(json.loads(result.stdout)["packages"]["google-adk"]["declarations"][0]["kind"],
                         "direct_reference")
        for args in (("--mode", secret), ("--" + secret,), ("--project", secret),
                     ("--mode", "non-adk")):
            bad = self.run_helper(*args)
            self.assertEqual(bad.returncode, 2)
            self.assertNotIn(secret, bad.stdout + bad.stderr)

    def test_presence_signals_do_not_parse_or_claim_wiring(self):
        for name in ("optimized_agent/agent.py", "optimized_agent/skills.py",
                     "optimized_agent/schema.py", "optimized_agent/bigquery_tools.py",
                     "optimized_agent/prompts/root_agent.txt", "cloud-run/main.py",
                     "cloud-run/Dockerfile", "cloud-run/delete.sh"):
            self.write(name, "SECRET_CONFIGURATION_VALUE")
        report = self.report()
        self.assertTrue(all(report["configuration_file_presence"][key] for key in
                            ("agent_entrypoint", "agent_skills_module", "schema_module",
                             "tool_module", "root_prompt", "server_entrypoint", "cleanup_script")))
        self.assertIn("application_directory", report["architecture_hints"])
        self.assertIn("cloud_run_directory", report["architecture_hints"])
        self.assertNotIn("SECRET_", json.dumps(report))
        self.assertEqual(report["coverage"]["manifest_bytes_read"], 0)

    def test_symlink_files_and_directories_are_never_followed(self):
        outside = Path(self.temp.name) / "outside"
        outside.mkdir()
        (outside / "requirements.txt").write_text("google-adk==9.8.7\n")
        (self.root / "requirements.txt").symlink_to(outside / "requirements.txt")
        (self.root / "external").symlink_to(outside, target_is_directory=True)
        report = self.report()
        self.assertEqual(report["coverage"]["symlinks_skipped"], 2)
        self.assertEqual(report["manifests"], [])

    def test_symlink_root_and_include_ancestors_are_refused(self):
        outside = Path(self.temp.name) / "outside"
        outside.mkdir()
        (outside / "requirements.txt").write_text("SECRET_EXTERNAL_DATA\n")
        linked = Path(self.temp.name) / "root-link"
        linked.symlink_to(self.root, target_is_directory=True)
        result = self.run_helper("--root", str(linked))
        self.assertEqual(result.returncode, 2)
        (self.root / "linked").symlink_to(outside, target_is_directory=True)
        self.write("requirements.txt", "-r linked/requirements.txt\n")
        result = self.run_helper()
        self.assertEqual(result.returncode, 2)
        self.assertNotIn("SECRET_", result.stdout + result.stderr)

    def test_unsafe_missing_and_nonregular_includes_fail_without_leaks(self):
        outside = Path(self.temp.name) / "outside.txt"
        outside.write_text("SECRET_EXTERNAL_DATA\n")
        self.write(".env", "SECRET_ENV_DATA")
        self.write(".env.private.txt", "SECRET_ENV_DATA")
        (self.root / "directory.txt").mkdir()
        (self.root / "linked.txt").symlink_to(outside)
        os.mkfifo(self.root / "fifo.txt")
        for include in ("linked.txt", "../outside.txt", ".env", ".env.private.txt",
                        "https://SECRET_HOST/a.txt", "SECRET_MISSING.txt",
                        "directory.txt", "fifo.txt"):
            with self.subTest(include=include):
                self.write("requirements.txt", "-r " + include + "\n")
                result = self.run_helper()
                self.assertEqual(result.returncode, 2)
                self.assertNotIn("SECRET_", result.stdout + result.stderr)

    def test_invalid_manifest_and_utf8_errors_are_sanitised(self):
        for content in ('[project]\ndependencies=["SECRET_UNFINISHED"\n',
                        '[project]\ndependencies="SECRET_WRONG_TYPE"\n',
                        '[project]\ndependencies=[4]\n'):
            self.write("pyproject.toml", content)
            result = self.run_helper()
            self.assertEqual(result.returncode, 2)
            self.assertNotIn("SECRET_", result.stdout + result.stderr)
        (self.root / "pyproject.toml").unlink()
        self.write("requirements.txt", "").write_bytes(b"SECRET_INVALID_UTF8\xff")
        result = self.run_helper()
        self.assertEqual(result.returncode, 2)
        self.assertNotIn("SECRET_", result.stdout + result.stderr)

    def test_depth_and_explicit_include_depth_are_bounded(self):
        self.write("requirements.txt", "google-adk==2.8.0\n")
        self.write("a/b/c/d/e/requirements.txt", "google-adk==9.8.7\n")
        report = self.report("--require-baseline", expected=3)
        self.assertTrue(report["coverage"]["depth_limit_reached"])
        self.write("requirements.txt", "-r a/b/c/d/e/requirements.txt\n")
        self.assertEqual(self.run_helper().returncode, 2)

    def test_per_file_aggregate_and_line_byte_limits(self):
        self.write("requirements.txt", "#" * 131073)
        result = self.run_helper()
        self.assertEqual(result.returncode, 2)
        self.assertIn("byte limit", result.stderr)
        self.write("requirements.txt", "#" * 4097 + "\n")
        self.assertIn("line limit", self.run_helper().stderr)
        self.write("requirements.txt", "")
        for number in range(9):
            self.write(f"requirements-{number}.txt", "# padding\n" * 12500)
        result = self.run_helper()
        self.assertEqual(result.returncode, 2)
        self.assertIn("byte limit", result.stderr)

    def test_manifest_and_directory_entry_counts_are_bounded(self):
        for number in range(65):
            self.write(f"requirements-{number}.txt", "google-adk==2.8.0\n")
        self.assertIn("Manifest count limit", self.run_helper().stderr)
        for path in self.root.iterdir():
            path.unlink()
        for number in range(4097):
            self.write(f"ignored-{number}", "")
        result = self.run_helper()
        self.assertEqual(result.returncode, 2)
        self.assertIn("Directory entry limit", result.stderr)


if __name__ == "__main__":
    unittest.main()
