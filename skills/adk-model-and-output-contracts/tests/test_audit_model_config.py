"""Exercise the model configuration audit through its public CLI using isolated fixtures."""

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "audit_model_config.py"
TABLE = Path(__file__).resolve().parents[1] / "assets" / "model-lifecycle-2026-10-01.json"


class AuditTests(unittest.TestCase):
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

    def signals(self, data):
        return {(row["signal"], str(row.get("detail"))) for row in data["signals"]}

    def test_help_and_invalid_arguments(self):
        result = self.run_cli("--help", project=False)
        self.assertEqual(result.returncode, 0)
        self.assertIn("--dry-run", result.stdout)
        self.assertEqual(self.run_cli(project=False).returncode, 2)
        self.assertEqual(self.run_cli("--project", str(self.root / "absent")).returncode, 2)
        for option in ("--max-files", "--max-bytes", "--max-depth", "--max-entries"):
            self.assertEqual(self.run_cli(option, "0").returncode, 2)
        self.assertEqual(self.run_cli("--lifecycle", str(self.root / "missing.json")).returncode, 2)
        bad = self.write("table.json", '{"models": []}')
        self.assertEqual(self.run_cli("--lifecycle", str(bad)).returncode, 2)

    def test_bundled_table_is_valid_and_dated(self):
        table = json.loads(TABLE.read_text())
        self.assertEqual(table["captured"], "2026-10-01")
        self.assertIn("Refresh", table["note"])
        statuses = {entry["status"] for entry in table["models"].values()}
        self.assertEqual(statuses, {"stable", "preview", "limited", "retiring", "shut_down"})
        self.assertEqual(table["models"]["gemini-2.5-pro"]["vertex_retirement"], "2026-10-20")

    def test_dry_run_is_read_only_and_repeatable(self):
        marker = self.root / "executed.txt"
        self.write("agent.py", f"from pathlib import Path\nPath({str(marker)!r}).write_text('executed')\nMODEL = 'gemini-3.8-flash'\n")
        first, data = self.scan("--dry-run")
        second, _ = self.scan("--dry-run")
        self.assertEqual(first.returncode, 0)
        self.assertEqual(first.stdout, second.stdout)
        self.assertTrue(data["read_only"] and data["dry_run"])
        self.assertFalse(data["changes_made"])
        self.assertFalse(marker.exists())
        regular, regular_data = self.scan()
        regular_data["dry_run"] = True
        self.assertEqual(data, regular_data)
        self.assertNotIn(str(self.root), first.stdout)

    def test_clean_configuration_produces_only_inventory_signals(self):
        self.write("agent.py", '''from google.adk.agents import LlmAgent
from google.genai import types

agent = LlmAgent(
    name="decider", model="gemini-3.8-flash", instruction="Decide.",
    generate_content_config=types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(thinking_level="low"), max_output_tokens=2048),
    output_schema=dict, output_key="decision",
)
''')
        self.write("requirements.txt", "google-adk==2.8.0\ngoogle-genai>=2.19,<3\n")
        result, data = self.scan()
        self.assertEqual(result.returncode, 0)
        labels = {label for label, _ in self.signals(data)}
        self.assertEqual(labels, {"model_string", "model_kwarg", "model_stable"})
        self.assertEqual({(d["name"], d["constraint"]) for d in data["dependencies"]},
                         {("google-adk", "==2.8.0"), ("google-genai", ">=2.19,<3")})
        self.assertEqual(data["lifecycle_table"]["captured"], "2026-10-01")

    def test_generate_content_config_findings(self):
        self.write("agent.py", '''from google.adk.agents import LlmAgent
from google.adk.planners import BuiltInPlanner
from google.genai import types

MODEL = "gemini-3.7-flash"
config = types.GenerateContentConfig(
    temperature=0.2, tools=[], system_instruction="x", response_schema={"type": "object"},
    thinking_config=types.ThinkingConfig(thinking_budget=512))
agent = LlmAgent(name="a", model=MODEL, generate_content_config=config,
                 planner=BuiltInPlanner(thinking_config=types.ThinkingConfig(thinking_level="low")),
                 output_schema=dict, tools=[len])
legacy = LlmAgent(name="b", model="gemini-2.5-flash",
                  generate_content_config=types.GenerateContentConfig(
                      temperature=0.5,
                      thinking_config=types.ThinkingConfig(thinking_level="high", thinking_budget=1)))
LlmAgent(name="c", model="gemini-2.0-flash", output_schema=dict, output_key="k", mode="task", tools=[])
''')
        result, data = self.scan()
        self.assertEqual(result.returncode, 0)
        signals = self.signals(data)
        expected = {
            ("generate_content_config_rejected_field", "tools -> LlmAgent.tools"),
            ("generate_content_config_rejected_field", "system_instruction -> LlmAgent.instruction"),
            ("generate_content_config_rejected_field", "response_schema -> LlmAgent.output_schema"),
            ("temperature_below_default_on_gemini_3", "0.2"),
            ("temperature_below_default", "0.5"),
            ("thinking_config_planner_precedence", "None"),
            ("thinking_budget_on_gemini_3", "generate_content_config"),
            ("thinking_level_on_gemini_2_5", "generate_content_config"),
            ("thinking_level_and_budget_both_set", "generate_content_config"),
            ("schema_with_tools_path_depends_on_backend", "None"),
            ("output_schema_without_output_key", "None"),
            ("task_mode_skips_output_schema", "None"),
            ("model_stable", "gemini-3.7-flash"),
            ("model_limited", "gemini-2.5-flash"),
            ("model_shut_down", "gemini-2.0-flash"),
        }
        self.assertTrue(expected <= signals, expected - signals)
        labels = [row["signal"] for row in data["signals"]]
        self.assertEqual(labels.count("schema_with_tools_path_depends_on_backend"), 1)
        self.assertEqual(labels.count("thinking_level_on_gemini_2_5"), 1)

    def test_planner_thinking_and_provider_wrappers(self):
        self.write("agent.py", '''from google.adk.agents import Agent
from google.adk.models import FallbackModel
from google.adk.models.lite_llm import LiteLlm
from google.adk.planners import BuiltInPlanner
from google.genai import types
import os

a = Agent(name="a", model="gemini-3.6-flash",
          planner=BuiltInPlanner(thinking_config=types.ThinkingConfig(thinking_budget=256)))
b = Agent(name="b", model=LiteLlm(model="openai/gpt-5"))
c = Agent(name="c", model=FallbackModel(models=["gemini-3.1-pro-preview", "gemini-3.1-flash-lite"]))
d = Agent(name="d", model=os.environ["MODEL"])
backend = os.environ.get("GOOGLE_GENAI_USE_ENTERPRISE")
legacy = os.environ.get("GOOGLE_GENAI_USE_VERTEXAI")
e = Agent(name="e", model="gemini-9.9-future")
f = Agent(name="f", model="gemini-flash-latest")
from google.adk.models import Gemini
g = Agent(name="g", model=Gemini(model="gemini-3.8-flash", client_kwargs={"enterprise": True, "location": "global"}))
''')
        result, data = self.scan()
        self.assertEqual(result.returncode, 0)
        signals = self.signals(data)
        expected = {
            ("thinking_budget_on_gemini_3", "planner"),
            ("litellm_model", "openai/gpt-5"),
            ("model_kwarg", "non_gemini"),
            ("fallback_model", "2"),
            ("model_preview", "gemini-3.1-pro-preview"),
            ("model_retiring", "gemini-3.1-flash-lite"),
            ("model_kwarg", "dynamic"),
            ("backend_variant_env_reference", "GOOGLE_GENAI_USE_ENTERPRISE"),
            ("model_not_in_lifecycle_table", "gemini-9.9-future"),
            ("deprecated_backend_env_name", "GOOGLE_GENAI_USE_VERTEXAI -> GOOGLE_GENAI_USE_ENTERPRISE"),
            ("backend_variant_env_reference", "GOOGLE_GENAI_USE_VERTEXAI"),
            ("model_alias_latest", "gemini-flash-latest"),
            ("gemini_client_kwargs", "enterprise,location"),
        }
        self.assertTrue(expected <= signals, expected - signals)
        self.assertNotIn("thinking_config_planner_precedence", {label for label, _ in signals})

    def test_custom_lifecycle_table_overrides_bundled(self):
        table = self.write("table.json", json.dumps({"captured": "2030-01-01", "note": "test", "models": {
            "gemini-3.8-flash": {"status": "shut_down"}}}))
        self.write("agent.py", 'MODEL = "gemini-3.8-flash"\n')
        result, data = self.scan("--lifecycle", str(table))
        self.assertEqual(result.returncode, 0)
        self.assertIn(("model_shut_down", "gemini-3.8-flash"), self.signals(data))
        self.assertEqual(data["lifecycle_table"]["captured"], "2030-01-01")

    def test_redaction_and_sensitive_exclusions(self):
        marker = "CREDENTIAL_VALUE_THAT_MUST_NOT_APPEAR"
        self.write("requirements.txt", f"google-adk=={marker}\nlitellm @ https://user:{marker}@invalid.example/x\n")
        self.write("pyproject.toml", f'[tool.poetry.dependencies]\ngoogle-genai = {{git = "https://{marker}", version = "1.0"}}\n')
        self.write("agent.py", f'KEY = "{marker}"\nMODEL = "gemini-3.8-flash"\n')
        for name in (".env", "credentials.json", "secrets.py", ".venv/leak.py", "node_modules/leak.py"):
            self.write(name, f'MODEL = "gemini-2.0-flash"  # {marker}\n')
        result, data = self.scan()
        self.assertEqual(result.returncode, 0)
        self.assertNotIn(marker, result.stdout + result.stderr)
        self.assertNotIn("gemini-2.0-flash", result.stdout)
        self.assertEqual(len(data["dependencies"]), 3)
        self.assertTrue(all(item["status"] == "redacted" for item in data["dependencies"]))

    def test_bounds_and_malformed_files_report_partial(self):
        self.write("a.py", "a = 1\n")
        self.write("b.py", "b = 2\n")
        result, data = self.scan("--max-files", "1")
        self.assertEqual(result.returncode, 1)
        self.assertIn("file_count_limit", {item["reason"] for item in data["issues"]})
        result, data = self.scan("--max-bytes", "1")
        self.assertEqual(result.returncode, 1)
        self.assertTrue(all(item["reason"] == "file_size_limit" for item in data["issues"]))
        self.write("one/two/hidden.py", "pass\n")
        result, data = self.scan("--max-depth", "1")
        self.assertEqual(result.returncode, 1)
        self.assertIn({"path": "one/two", "reason": "depth_limit"}, data["issues"])
        private = "PRIVATE_SOURCE_TEXT"
        self.write("bad.py", f"def {private}(\n")
        self.write("pyproject.toml", f"[{private}\n")
        result, data = self.scan()
        self.assertEqual(result.returncode, 1)
        self.assertNotIn(private, result.stdout + result.stderr)
        self.assertEqual({item["reason"] for item in data["issues"]}, {"malformed_file"})

    def test_symlinks_and_entry_cap(self):
        outside = Path(self.temp.name) / "outside.py"
        outside.write_text('MODEL = "gemini-3.8-flash"\n')
        (self.root / "link.py").symlink_to(outside)
        result, data = self.scan()
        self.assertEqual(result.returncode, 1)
        self.assertEqual(data["signals"], [])
        self.assertEqual({item["reason"] for item in data["issues"]}, {"symlink_skipped"})
        (self.root / "link.py").unlink()
        for index in range(12):
            self.write(f"ignored-{index}.bin", "irrelevant")
        result, data = self.scan("--max-entries", "5")
        self.assertEqual(result.returncode, 1)
        self.assertEqual(data["directory_entries_seen"], 5)
        self.assertEqual(data["issues"], [{"path": ".", "reason": "entry_count_limit"}])


if __name__ == "__main__":
    unittest.main()
