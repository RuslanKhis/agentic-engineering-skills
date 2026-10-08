"""Exercise the release reference inventory through its public CLI using isolated fixtures."""

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "inventory_release_refs.py"


class InventoryTests(unittest.TestCase):
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

    def labels(self, data):
        return {row["signal"] for row in data["signals"]}

    def test_help_and_invalid_arguments(self):
        result = self.run_cli("--help", project=False)
        self.assertEqual(result.returncode, 0)
        self.assertIn("--dry-run", result.stdout)
        self.assertIn("--lifecycle", result.stdout)
        self.assertEqual(self.run_cli(project=False).returncode, 2)
        self.assertEqual(self.run_cli("--project", str(self.root / "absent")).returncode, 2)
        for option in ("--max-files", "--max-bytes", "--max-depth", "--max-entries"):
            self.assertEqual(self.run_cli(option, "0").returncode, 2)
        self.assertEqual(self.run_cli("--lifecycle", str(self.root / "missing.json")).returncode, 2)
        bad = self.write("table.json", '{"models": []}')
        self.assertEqual(self.run_cli("--lifecycle", str(bad)).returncode, 2)

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

    def test_clean_project_has_no_findings(self):
        self.write("app/agent.py", '''from google.adk.agents import LlmAgent
from google.adk.evaluation.eval_metrics import JudgeModelOptions

INSTRUCTION = "Decide refunds using the policy supplied. Explain each decision in one sentence."
root_agent = LlmAgent(name="r", model="gemini-3.8-flash", instruction=INSTRUCTION)
judge = JudgeModelOptions(judge_model="gemini-3.8-flash", num_samples=5)
SECRET = "projects/p/secrets/api/versions/7"
''')
        self.write("requirements.txt", "google-adk==2.8.0\ngoogle-genai>=2.19,<3\n")
        self.write("evals/ci.evalset.json", json.dumps({"eval_set_id": "ci", "eval_cases": [{"eval_id": "a"}, {"eval_id": "b"}]}))
        self.write("evals/test_config.json", json.dumps({"criteria": {
            "tool_trajectory_avg_score": 1.0, "response_match_score": 0.8,
            "final_response_match_v2": {"threshold": 0.5, "judge_model_options": {"judge_model": "gemini-3.8-flash", "num_samples": 5}}}}))
        self.write("tests/test_gate.py", '''from google.adk.evaluation.agent_evaluator import AgentEvaluator
async def test_gate():
    await AgentEvaluator.evaluate(agent_module="app", eval_dataset_file_path_or_dir="evals", num_runs=3, output_file="ci.csv")
''')
        result, data = self.scan()
        self.assertEqual(result.returncode, 0)
        expected = {
            ("model_pinned", "gemini-3.8-flash"), ("prompt_literal", "INSTRUCTION"),
            ("prompt_reference", "instruction=INSTRUCTION"), ("judge_model", "gemini-3.8-flash"),
            ("judge_model_pinned", "gemini-3.8-flash"), ("secret_version_pinned", "versions/<n>"),
            ("eval_set", "ci"), ("eval_config", "final_response_match_v2,response_match_score,tool_trajectory_avg_score"),
            ("agent_evaluator_call", "num_runs=3"),
        }
        self.assertEqual(self.signals(data), expected)
        findings = {"model_alias", "judge_model_unset", "judge_model_alias", "judge_model_retiring_default",
                    "agent_model_unset_default", "prompt_dynamic", "secret_version_alias",
                    "eval_legacy_test_json", "agent_evaluator_without_output_file", "eval_set_duplicate_case_ids"}
        self.assertFalse(findings & self.labels(data))
        components = data["manifest"]["components"]
        self.assertEqual(components["adk_version"], {"version": "==2.8.0", "exact_pin": True})
        self.assertEqual(components["dependency_pins"]["litellm"], "unknown")
        self.assertEqual([m["id"] for m in components["agent_models"]], ["gemini-3.8-flash"])
        self.assertEqual(components["judge_models"], [{"id": "gemini-3.8-flash", "locations": 2, "classification": "pinned"}])
        self.assertEqual(components["eval_sets"][0]["cases"], 2)
        self.assertEqual(components["tool_schema_hash"], "unknown")
        self.assertEqual(components["secret_versions"]["pinned_references"], 1)

    def test_model_and_judge_findings(self):
        self.write("app/agent.py", '''from google.adk.agents import LlmAgent, Agent
from google.adk.evaluation.eval_metrics import JudgeModelOptions, LlmAsAJudgeCriterion, RubricsBasedCriterion
import os

a = LlmAgent(name="a", model="gemini-flash-latest", instruction="Be terse.")
b = Agent(name="b", instruction="Be kind.")
c = LlmAgent(name="c", model="gemini-3.1-pro-preview", instruction="Be brief.")
d = LlmAgent(name="d", model=os.environ["MODEL"], instruction="Be clear.")
unset = JudgeModelOptions()
retiring = JudgeModelOptions(judge_model="gemini-2.5-flash")
alias = JudgeModelOptions(judge_model="gemini-flash-latest")
crit = LlmAsAJudgeCriterion(threshold=0.5)
rubric = RubricsBasedCriterion(threshold=0.5, judge_model_options=JudgeModelOptions(judge_model="gemini-3.8-flash"))
config = {"judge_model": "gemini-3.7-flash", "num_samples": 3}
''')
        result, data = self.scan()
        self.assertEqual(result.returncode, 0)
        signals = self.signals(data)
        expected = {
            ("model_alias", "gemini-flash-latest"), ("model_alias", "gemini-3.1-pro-preview"),
            ("agent_model_unset_default", "LlmAgent.DEFAULT_MODEL"), ("model_dynamic", "LlmAgent"),
            ("judge_model_unset", "gemini-2.5-flash"), ("judge_model_retiring_default", "gemini-2.5-flash"),
            ("judge_model_alias", "gemini-flash-latest"), ("judge_model_pinned", "gemini-3.8-flash"),
            ("judge_model_pinned", "gemini-3.7-flash"),
        }
        self.assertTrue(expected <= signals, expected - signals)
        self.assertEqual([row["signal"] for row in data["signals"]].count("judge_model_unset"), 2)
        agent_models = {m["id"] for m in data["manifest"]["components"]["agent_models"]}
        self.assertEqual(agent_models, {"gemini-flash-latest", "gemini-3.1-pro-preview"})
        judges = {(j["id"], j["classification"]) for j in data["manifest"]["components"]["judge_models"]}
        self.assertEqual(judges, {("gemini-2.5-flash", "retiring_default"), ("gemini-flash-latest", "alias"),
                                  ("gemini-3.8-flash", "pinned"), ("gemini-3.7-flash", "pinned"),
                                  ("gemini-2.5-flash", "unset_default")})

    def test_lifecycle_table_annotates_models(self):
        table = self.write("table.json", json.dumps({"captured": "2030-01-01", "models": {"gemini-3.8-flash": {"status": "shut_down"}}}))
        self.write("agent.py", 'A = "gemini-3.8-flash"\nB = "gemini-9.9-flash"\n')
        result, data = self.scan("--lifecycle", str(table))
        self.assertEqual(result.returncode, 0)
        statuses = {m["id"]: m.get("lifecycle_status") for m in data["manifest"]["components"]["agent_models"]}
        self.assertEqual(statuses, {"gemini-3.8-flash": "shut_down", "gemini-9.9-flash": "not_in_table"})
        _, plain = self.scan()
        self.assertNotIn("lifecycle_status", plain["manifest"]["components"]["agent_models"][0])

    def test_prompt_sources_are_hashed_never_printed(self):
        secret = "PRIVATE_PROMPT_SENTENCE_THAT_MUST_NOT_LEAK"
        self.write("app/prompt.py", f'ROOT_PROMPT = """You are a billing assistant. {secret} Decide carefully."""\nSHORT = "x"\n')
        self.write("app/prompts/system.md", f"System text {secret}\n")
        self.write("app/agent.py", f'''from google.adk.agents import LlmAgent
from app.prompt import ROOT_PROMPT
def build(ctx):
    return "dynamic"
a = LlmAgent(name="a", model="gemini-3.8-flash", instruction=ROOT_PROMPT)
b = LlmAgent(name="b", model="gemini-3.8-flash", instruction=build, global_instruction="Global {secret}")
c = LlmAgent(name="c", model="gemini-3.8-flash", instruction=f"templated {{ctx}} {secret}")
''')
        result, data = self.scan()
        self.assertEqual(result.returncode, 0)
        self.assertNotIn(secret, result.stdout + result.stderr)
        signals = self.signals(data)
        expected = {("prompt_literal", "ROOT_PROMPT"), ("prompt_file", "None"),
                    ("prompt_reference", "instruction=app.prompt.ROOT_PROMPT"), ("prompt_dynamic", "instruction"),
                    ("prompt_literal", "global_instruction")}
        self.assertTrue(expected <= signals, expected - signals)
        prompts = data["manifest"]["components"]["prompts"]
        names = {(p["path"], p["name"]) for p in prompts}
        self.assertEqual(names, {("app/prompt.py", "ROOT_PROMPT"), ("app/prompts/system.md", "system.md"), ("app/agent.py", "global_instruction")})
        self.assertTrue(all(len(p["sha256"]) == 64 and "text" not in p for p in prompts))
        self.assertFalse(data["limits"]["prompt_text_emitted"])

    def test_eval_assets_and_deploy_files(self):
        self.write("evals/ci.evalset.json", json.dumps({"eval_set_id": "ci", "eval_cases": [{"eval_id": "a"}, {"eval_id": "a"}]}))
        self.write("evals/empty.evalset.json", json.dumps({"eval_set_id": "empty", "eval_cases": []}))
        self.write("evals/old.test.json", json.dumps([{"query": "hi", "expected_tool_use": []}]))
        self.write("evals/test_config.json", json.dumps({"criteria": {
            "hallucinations_v1": 0.5,
            "final_response_match_v2": {"threshold": 0.5, "judge_model_options": {"judge_model": "gemini-3.8-flash"}},
            "safety_v1": {"threshold": 0.9}}}))
        self.write("evals/other_eval_config.json", json.dumps({"no": "criteria"}))
        self.write("Dockerfile", "FROM python:3.11\n")
        self.write("cloudbuild.yaml", "steps:\n- args: [run, services, update-traffic, svc, --to-revisions, r=100]\n")
        self.write(".github/workflows/ci.yml", "jobs:\n  a:\n    steps:\n      - run: adk eval app evals\n      - run: adk conformance test\n"
                   "      - run: gcloud run deploy svc --no-traffic --tag canary --set-secrets A=api:latest,B=api:3\n"
                   "      - run: python check_eval_results.py --csv x\n")
        self.write("tests/conformance/core/case1/spec.yaml", "name: case1\n")
        self.write("tests/test_gate.py", 'from google.adk.evaluation.agent_evaluator import AgentEvaluator\n'
                   'async def t():\n    await AgentEvaluator.evaluate_eval_set(agent_module="app", eval_set=None)\n')
        result, data = self.scan()
        self.assertEqual(result.returncode, 0)
        signals = self.signals(data)
        expected = {
            ("eval_set", "ci"), ("eval_set_duplicate_case_ids", "None"), ("eval_set_empty", "None"),
            ("eval_legacy_test_json", "migrate with AgentEvaluator.migrate_eval_data_to_new_schema"),
            ("eval_config", "final_response_match_v2,hallucinations_v1,safety_v1"),
            ("judge_model_unset", "hallucinations_v1 -> gemini-2.5-flash"), ("judge_model_unset", "safety_v1 -> gemini-2.5-flash"),
            ("judge_num_samples_default", "final_response_match_v2"), ("judge_model_pinned", "gemini-3.8-flash"),
            ("eval_config_without_criteria", "None"),
            ("dockerfile_present", "None"), ("cloudbuild_present", "None"), ("github_workflow_present", "None"),
            ("conformance_spec_present", "None"),
            ("cloud_run_update_traffic", "None"), ("cloud_run_to_revisions", "None"), ("gcloud_run_deploy", "None"),
            ("cloud_run_no_traffic", "None"), ("cloud_run_tag", "None"),
            ("adk_eval_invocation", "None"), ("adk_conformance_test_invocation", "None"), ("eval_csv_checker_reference", "None"),
            ("secret_version_alias", "versions/latest"), ("secret_version_pinned", "versions/<n>"),
            ("agent_evaluator_call", "num_runs=default"), ("agent_evaluator_without_output_file", "None"),
        }
        self.assertTrue(expected <= signals, expected - signals)
        deploy = data["manifest"]["components"]["deploy_configs"]
        self.assertEqual(deploy, {"cloudbuild": ["cloudbuild.yaml"], "conformance_specs": 1, "dockerfiles": ["Dockerfile"],
                                  "github_workflows": [".github/workflows/ci.yml"]})
        self.assertEqual(len(data["manifest"]["components"]["eval_sets"]), 3)
        self.assertEqual(data["manifest"]["components"]["secret_versions"], {"pinned_references": 1, "latest_references": 1, "versions": "unknown"})

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
        self.assertTrue(all(item["status"] == "redacted" and item["exact_pin"] is False for item in data["dependencies"]))
        self.assertEqual(data["manifest"]["components"]["adk_version"], {"version": "unknown", "exact_pin": False})

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
        self.write("broken.evalset.json", f"{{{private}")
        self.write("pyproject.toml", f"[{private}\n")
        result, data = self.scan()
        self.assertEqual(result.returncode, 1)
        self.assertNotIn(private, result.stdout + result.stderr)
        self.assertEqual({item["reason"] for item in data["issues"]}, {"malformed_file"})
        self.assertEqual(len(data["issues"]), 3)

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
