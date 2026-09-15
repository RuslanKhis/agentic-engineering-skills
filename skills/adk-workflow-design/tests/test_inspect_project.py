"""Offline public-CLI and inspection invariants; standard library only."""

import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "inspect_project.py"
SPEC = importlib.util.spec_from_file_location("workflow_inspector", SCRIPT)
inspector = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(inspector)


class InspectionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def write(self, name, value):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(value)
        return path

    def cli(self, *args):
        return subprocess.run(
            [sys.executable, str(SCRIPT), *map(str, args)],
            text=True,
            capture_output=True,
            timeout=10,
            env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
        )

    def test_help_and_invalid_inputs(self):
        self.assertEqual(self.cli("--help").returncode, 0)
        for args in [
            [],
            ["--project", self.root / "absent"],
            ["--project", self.root, "--max-files", "0"],
            ["--project", self.root, "--require-adk-version", "latest"],
        ]:
            self.assertEqual(self.cli(*args).returncode, 2)

    def test_dry_run_does_not_read_source_or_environment_values(self):
        self.write("app.py", "not valid python: private-value")
        self.write(".env", "GOOGLE_API_KEY=private-value")
        with patch.object(
            inspector.os, "open", side_effect=AssertionError("read attempted")
        ):
            result, status = inspector.inspect(self.root, dry_run=True)
        self.assertEqual(status, 0)
        self.assertFalse(result["project_contents_read"])
        run = self.cli("--project", self.root, "--dry-run")
        self.assertEqual(run.returncode, 0)
        self.assertNotIn("private-value", run.stdout + run.stderr)

    def test_inspection_does_not_execute_target_or_expose_literals(self):
        self.write(
            "app.py",
            'raise RuntimeError("secret-sentinel")\nMODEL="private-model-id"\n',
        )
        self.write(".env", "GOOGLE_API_KEY=secret-sentinel")
        self.write(
            "requirements.txt",
            "google-adk==2.8.0\n--index-url https://user:secret-sentinel@example.invalid\n",
        )
        result = self.cli("--project", self.root)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn("secret-sentinel", result.stdout + result.stderr)
        self.assertNotIn("private-model-id", result.stdout)
        self.assertEqual(
            json.loads(result.stdout)["declarations"][0]["specifier"], "==2.8.0"
        )

    def test_parallel_collision_and_actual_narrow_repair(self):
        source = """from google.adk.agents import LlmAgent as Agent, ParallelAgent
a = Agent(name="a", output_key="shared-private-key")
b = Agent(name="b", output_key="shared-private-key")
root = ParallelAgent(name="root", sub_agents=[a, b])
"""
        self.write("agent.py", source)
        bad = self.cli("--project", self.root)
        self.assertEqual(bad.returncode, 0)
        self.assertIn("parallel-output-key-collision", bad.stdout)
        self.assertNotIn("shared-private-key", bad.stdout)
        self.write(
            "agent.py",
            source.replace(
                'b", output_key="shared-private-key"', 'b", output_key="branch-b"'
            ),
        )
        good = self.cli("--project", self.root)
        self.assertEqual(good.returncode, 0)
        self.assertNotIn("parallel-output-key-collision", good.stdout)

    def test_aliases_loop_bounds_and_unresolved_parallel_keys(self):
        self.write(
            "agent.py",
            """import google.adk.agents as agents
agents.LoopAgent(name="missing")
agents.LoopAgent(name="zero", max_iterations=0)
agents.LoopAgent(name="bool", max_iterations=True)
agents.LoopAgent(name="dynamic", max_iterations=LIMIT)
agents.LoopAgent(name="bounded", max_iterations=5)
agents.ParallelAgent(name="factory", sub_agents=make_children())
""",
        )
        result, status = inspector.inspect(self.root)
        codes = [f["code"] for f in result["findings"]]
        self.assertEqual(status, 0)
        self.assertEqual(codes.count("loop-bound-invalid"), 2)
        self.assertEqual(codes.count("loop-bound-missing"), 1)
        self.assertEqual(codes.count("loop-bound-unresolved"), 1)
        self.assertIn("parallel-children-unresolved", codes)

    def test_installed_and_declared_versions_are_checked_separately(self):
        p = self.write("requirements.txt", "google-adk==2.8.0\n")
        with patch.object(
            inspector.importlib.metadata, "version", return_value="2.8.0"
        ):
            self.assertEqual(inspector.inspect(self.root, required_adk="2.8.0")[1], 0)
            p.write_text("google-adk>=2.8.0\n")
            self.assertEqual(inspector.inspect(self.root, required_adk="2.8.0")[1], 3)
            p.write_text("google-adk==2.7.0\n")
            self.assertEqual(inspector.inspect(self.root, required_adk="2.8.0")[1], 3)
        p.write_text("google-adk==2.8.0\n")
        with patch.object(
            inspector.importlib.metadata,
            "version",
            side_effect=inspector.importlib.metadata.PackageNotFoundError,
        ):
            self.assertEqual(inspector.inspect(self.root, required_adk="2.8.0")[1], 3)

    def test_lockfile_and_untrusted_version_suffix(self):
        self.write("uv.lock", '[[package]]\nname="google-adk"\nversion="2.8.0"\n')
        self.write(
            "requirements.txt", "google-genai==2.23.0\nhttpx==0.28.1secret-sentinel\n"
        )
        result, status = inspector.inspect(self.root)
        self.assertEqual(status, 0)
        self.assertEqual(len(result["declarations"]), 3)
        self.assertIn(
            {"path": "requirements.txt", "package": "httpx", "specifier": "unresolved"},
            result["declarations"],
        )
        self.assertNotIn("secret-sentinel", json.dumps(result))

    def test_comments_and_unrelated_toml_strings_are_not_dependency_pins(self):
        self.write("requirements.txt", "# Historical only: google-adk==2.8.0\n")
        self.write(
            "pyproject.toml",
            '[project]\nname="fixture"\ndescription="google-adk==2.8.0"\n',
        )
        with patch.object(
            inspector.importlib.metadata, "version", return_value="2.8.0"
        ):
            result, status = inspector.inspect(self.root, required_adk="2.8.0")
        self.assertEqual(status, 3)
        self.assertEqual(result["declarations"], [])
        self.write(
            "pyproject.toml",
            '[project]\nname="fixture"\ndependencies=["google-adk==2.8.0"]\n',
        )
        with patch.object(
            inspector.importlib.metadata, "version", return_value="2.8.0"
        ):
            self.assertEqual(inspector.inspect(self.root, required_adk="2.8.0")[1], 0)

    def test_poetry_declarations_cannot_be_hidden_by_a_stale_lock(self):
        self.write("poetry.lock", '[[package]]\nname="google-adk"\nversion="2.8.0"\n')
        for declaration in [
            '"2.9.0"',
            '{version="2.9.0"}',
            '"^2.9.0"',
            '{path="private-source"}',
        ]:
            self.write(
                "pyproject.toml",
                "[tool.poetry.dependencies]\ngoogle-adk=" + declaration + "\n",
            )
            with patch.object(
                inspector.importlib.metadata, "version", return_value="2.8.0"
            ):
                data, status = inspector.inspect(self.root, required_adk="2.8.0")
            self.assertEqual(status, 3, declaration)
            self.assertNotIn("private-source", json.dumps(data))
        self.write(
            "pyproject.toml",
            '[tool.poetry.dependencies]\ngoogle-adk={version="2.8.0"}\n',
        )
        with patch.object(
            inspector.importlib.metadata, "version", return_value="2.8.0"
        ):
            self.assertEqual(inspector.inspect(self.root, required_adk="2.8.0")[1], 0)

    def test_parser_recursion_returns_structured_incomplete_inspection(self):
        self.write("recursive.py", "x = " + "-" * 4000 + "1\n")
        self.write("pyproject.toml", "x = " + "[" * 4000 + "1" + "]" * 4000 + "\n")
        result = self.cli("--project", self.root)
        self.assertEqual(result.returncode, 2)
        self.assertFalse(json.loads(result.stdout)["complete"])
        self.assertNotIn("Traceback", result.stderr)

    def test_parse_and_scan_failures_are_incomplete_not_pass(self):
        self.write("invalid.py", "def secret-sentinel")
        self.assertEqual(self.cli("--project", self.root).returncode, 2)
        self.assertNotIn("secret-sentinel", self.cli("--project", self.root).stdout)
        self.write("other.py", "x = 1")
        self.assertEqual(
            self.cli("--project", self.root, "--max-files", 1).returncode, 2
        )
        self.assertEqual(
            self.cli("--project", self.root, "--max-bytes", 1).returncode, 2
        )

    def test_symlinks_and_environments_are_excluded(self):
        self.write("hidden/.env", "private-value")
        self.write(".adk/session.py", "bad syntax!")
        self.write("custom-env/pyvenv.cfg", "")
        self.write("custom-env/private.py", "bad syntax!")
        outside = self.write("private.txt", "bad syntax!")
        (self.root / "linked.py").symlink_to(outside)
        result, status = inspector.inspect(self.root)
        self.assertEqual(status, 0)
        self.assertEqual([f["path"] for f in result["files"]], ["hidden/.env"])

    def test_explicit_directory_exclusions_preserve_relevant_source(self):
        self.write("generated/a.py", "broken syntax!")
        self.write("nested/generated/b.py", "broken syntax!")
        self.write("app.py", "x = 1")
        result = self.cli(
            "--project", self.root, "--exclude-dir", "generated", "--max-files", "1"
        )
        self.assertEqual(result.returncode, 0)
        data = json.loads(result.stdout)
        self.assertEqual(data["explicitly_excluded_directory_names"], ["generated"])
        self.assertEqual([f["path"] for f in data["files"]], ["app.py"])
        self.assertEqual(
            self.cli("--project", self.root, "--exclude-dir", "../app").returncode, 2
        )

    def test_repeat_is_stable_and_does_not_change_project(self):
        self.write("app.py", "x = 1\n")
        self.write("requirements.txt", "google-adk==2.8.0\n")

        def fingerprints():
            return {
                p.relative_to(self.root)
                .as_posix(): hashlib.sha256(p.read_bytes())
                .hexdigest()
                for p in self.root.rglob("*")
                if p.is_file()
            }

        before = fingerprints()
        first = self.cli("--project", self.root)
        second = self.cli("--project", self.root)
        self.assertEqual(first.returncode, 0)
        self.assertEqual(first.stdout, second.stdout)
        self.assertEqual(before, fingerprints())


if __name__ == "__main__":
    unittest.main()
