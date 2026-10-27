"""Offline checks for the scenario runner; no agent, model or network calls."""

from contextlib import redirect_stderr, redirect_stdout
import importlib.util
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


scen = load_module("run_scenarios", ROOT / "scripts/run_scenarios.py")


def make_root(base: Path) -> Path:
    for name in ("alpha-skill", "beta-skill"):
        (base / "skills" / name / "tests").mkdir(parents=True)
        (base / "skills" / name / "SKILL.md").write_text(f"---\nname: {name}\ndescription: d\n---\n")
        (base / "skills" / name / "tests" / "test_x.py").write_text("")
    (base / "fixtures" / "seed").mkdir(parents=True)
    (base / "fixtures" / "seed" / "service.py").write_text("print('seed')\n")
    cases = [
        {"id": "empty-design", "prompt": "Design a thing.", "expected_primary": "alpha-skill",
         "available_skills": ["alpha-skill", "external-skill"], "context": "An empty workspace. Docs only.",
         "assertions": ["Writes a design note.", "Names a risk."]},
        {"id": "with-seed", "prompt": "Fix the service.", "expected_primary": "beta-skill",
         "available_skills": ["beta-skill"], "context": "Use the seed service.", "assertions": ["Fixes it."]},
        {"id": "imaginary-project", "prompt": "Fix our agent.", "expected_primary": None,
         "available_skills": ["alpha-skill"], "context": "An ADK 2.12 agent with six tools. No network.",
         "assertions": ["Does nothing harmful."]},
        {"id": "broken-fixture", "prompt": "x", "expected_primary": None, "available_skills": ["alpha-skill"],
         "context": "c.", "assertions": ["a"]},
    ]
    (base / "evals").mkdir()
    (base / "evals" / "scenarios.json").write_text(json.dumps({"version": 1, "cases": cases}))
    (base / "evals" / "scenario-fixtures.json").write_text(json.dumps({"version": 1, "scenarios": {
        "empty-design": {"status": "runnable", "note": "n"},
        "with-seed": {"status": "repo-fixture", "copy": [{"from": "fixtures/seed", "to": "."}]},
        "broken-fixture": {"status": "repo-fixture", "copy": [{"from": "fixtures/absent", "to": "."}]},
    }}))
    return base


class ClassificationTests(unittest.TestCase):
    def test_statuses(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = make_root(Path(tmp))
            cases, _ = scen.load_scenarios(root)
            fixtures = scen.load_fixtures(root)
            status = {c["id"]: scen.classify(c, fixtures, root) for c in cases}
        self.assertEqual(status["empty-design"]["status"], "runnable")
        self.assertEqual(status["empty-design"]["skills_missing"], ["external-skill"])
        self.assertEqual(status["with-seed"]["status"], "repo-fixture")
        self.assertEqual(status["imaginary-project"]["status"], "fixture-missing")
        self.assertEqual(status["imaginary-project"]["needs"], "An ADK 2.12 agent with six tools.")
        self.assertEqual(status["broken-fixture"]["status"], "fixture-missing")
        self.assertIn("fixtures/absent", status["broken-fixture"]["partial"])

    def test_repository_manifest_matches_scenarios(self):
        cases, _ = scen.load_scenarios(ROOT)
        ids = {c["id"] for c in cases}
        fixtures = scen.load_fixtures(ROOT)
        self.assertTrue(fixtures)
        for cid, entry in fixtures.items():
            self.assertIn(cid, ids, f"{cid} is not a scenario")
            self.assertIn(entry["status"], scen.STATUSES)
            for item in entry.get("copy", []):
                self.assertTrue((ROOT / item["from"]).exists(), item["from"])
        listing = scen.format_list(cases, fixtures, ROOT)
        self.assertIn("## runnable", listing)
        self.assertIn("## fixture-missing", listing)

    def test_list_command(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = make_root(Path(tmp))
            out = io.StringIO()
            with redirect_stdout(out):
                self.assertEqual(scen.main(["list", "--root", str(root)]), 0)
        self.assertIn("## runnable (1)", out.getvalue())
        self.assertIn("## fixture-missing (2)", out.getvalue())
        self.assertIn("external skills absent: external-skill", out.getvalue())


class PrepareTests(unittest.TestCase):
    def test_workspaces_skills_and_missing_fixtures(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = make_root(Path(tmp) / "repo")
            cases, _ = scen.load_scenarios(root)
            run_dir, manifest = scen.prepare(root, cases, scen.load_fixtures(root), Path(tmp) / "runs")
            self.assertTrue(run_dir.name.startswith("aes-scenarios-"))
            self.assertEqual(run_dir.parent, Path(tmp) / "runs")
            ws = run_dir / "empty-design" / "workspace"
            self.assertTrue((ws / ".claude/skills/alpha-skill/SKILL.md").exists())
            self.assertFalse((ws / ".claude/skills/alpha-skill/tests").exists())
            self.assertFalse((ws / ".claude/skills/beta-skill").exists())
            self.assertTrue((run_dir / "with-seed/workspace/service.py").exists())
            self.assertFalse((run_dir / "imaginary-project").exists())
            task = (run_dir / "empty-design/task.md").read_text()
            self.assertTrue(task.startswith("Design a thing."))
            self.assertIn("Situation (from the person asking): An empty workspace. Docs only.", task)
            self.assertNotIn("Writes a design note", task)
            statuses = {e["id"]: e["status"] for e in manifest["scenarios"]}
            self.assertEqual(statuses["imaginary-project"], "fixture-missing")
            self.assertEqual(manifest["scenarios"][0]["skills_installed"], ["alpha-skill"])

    def test_fixture_cannot_escape_workspace(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = make_root(Path(tmp) / "repo")
            cases, _ = scen.load_scenarios(root)
            fixtures = {"with-seed": {"status": "repo-fixture",
                                      "copy": [{"from": "fixtures/seed", "to": "../../escape"}]}}
            with self.assertRaises(scen.InputError):
                scen.prepare(root, [cases[1]], fixtures, Path(tmp) / "runs")

    def test_select(self):
        cases = [{"id": "a", "expected_primary": "x"}, {"id": "b", "expected_primary": "y"}]
        self.assertEqual([c["id"] for c in scen.select(cases, None, "y")], ["b"])
        with self.assertRaises(scen.InputError):
            scen.select(cases, ["zzz"], None)
        with self.assertRaises(scen.InputError):
            scen.select(cases, None, None)


TRANSCRIPT = [
    json.dumps({"type": "system", "subtype": "init", "skills": ["alpha-skill"]}),
    json.dumps({"type": "assistant", "message": {"content": [
        {"type": "tool_use", "name": "Skill", "input": {"skill": "alpha-skill"}},
        {"type": "tool_use", "name": "Read", "input": {"file_path": "/w/.claude/skills/beta-skill/SKILL.md"}},
        {"type": "tool_use", "name": "Read", "input": {"file_path": "/w/.claude/skills/gamma-skill/references/x.md"}},
        {"type": "text", "text": "Working."}]}}),
    "not json",
    json.dumps({"type": "result", "subtype": "success", "is_error": False, "num_turns": 3,
                "total_cost_usd": 0.2, "result": "Wrote design.md with one risk: cost."}),
]


class AgentAndJudgeTests(unittest.TestCase):
    def test_parse_transcript(self):
        summary = scen.parse_transcript(TRANSCRIPT)
        self.assertEqual(summary["skills_loaded"], ["alpha-skill", "beta-skill"])
        self.assertEqual(summary["skill_files_read"], ["beta-skill/SKILL.md", "gamma-skill/references/x.md"])
        self.assertEqual(summary["final"], "Wrote design.md with one risk: cost.")
        self.assertEqual(summary["result"]["num_turns"], 3)
        self.assertEqual(len(summary["tool_calls"]), 3)

    def test_agent_command_is_bounded_and_project_scoped(self):
        command = scen.agent_command("claude-sonnet-5-5", 30, scen.AGENT_TOOLS, 2.5)
        self.assertEqual(command[command.index("--setting-sources") + 1], "project")
        self.assertEqual(command[command.index("--max-turns") + 1], "30")
        self.assertEqual(command[command.index("--max-budget-usd") + 1], "2.5")
        self.assertNotIn("Bash", command[command.index("--tools") + 1])

    def test_agent_then_files_judge_round_trip(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = make_root(Path(tmp) / "repo")
            cases, _ = scen.load_scenarios(root)
            run_dir, manifest = scen.prepare(root, cases[:2], scen.load_fixtures(root), Path(tmp))
            seen = {}

            class Proc:
                returncode = 0
                stdout = "\n".join(TRANSCRIPT)

            def runner(command, **kwargs):
                seen.update(kwargs)
                (kwargs["cwd"] / "design.md").write_text("# Design\n\nRisk: cost overrun.\n")
                return Proc()

            entry = manifest["scenarios"][0]
            record = scen.run_agent(run_dir, entry, "m", 5, 60, scen.AGENT_TOOLS, None, runner=runner)
            self.assertEqual(record["skills_loaded"], ["alpha-skill", "beta-skill"])
            self.assertTrue(seen["env"]["AGENTIC_ENGINEERING_HOME"].startswith(str(run_dir)))
            case = cases[0]
            pending = scen.judge_case(run_dir, case, "files", "human", 60)
            self.assertEqual(pending["status"], "awaiting-judge")
            prompt = (run_dir / "empty-design/judge-prompt.md").read_text()
            self.assertIn("A2: Names a risk.", prompt)
            self.assertIn("Risk: cost overrun.", prompt)
            self.assertNotIn(".claude/skills", prompt.split("### Files written or changed")[1])
            (run_dir / "empty-design/judge-answer.json").write_text(json.dumps({"verdicts": [
                {"assertion": "A1", "verdict": "PASS", "quote": "# Design", "reason": "file exists"},
                {"assertion": "A2", "verdict": "pass", "quote": "Risk:   cost overrun.", "reason": "named"}]}))
            graded = scen.judge_case(run_dir, case, "files", "human", 60)
            self.assertEqual(graded["status"], "graded")
            self.assertEqual((graded["passed"], graded["total"]), (2, 2))
            self.assertTrue(all(row["quote_found"] for row in graded["assertions"]))
            self.assertEqual(graded["files"], ["design.md"])
            results = scen.build_results(root, run_dir, manifest, {c["id"]: c for c in cases},
                                         {"empty-design": graded}, "h", {"agent_backend": "claude-cli"})
        rows = {row["id"]: row for row in results["cases"]}
        self.assertEqual(results["schema"], scen.SCHEMA)
        self.assertEqual(rows["empty-design"]["status"], "graded")
        self.assertTrue(rows["empty-design"]["primary_loaded"])
        self.assertTrue(rows["empty-design"]["primary_consulted"])
        self.assertEqual(rows["with-seed"]["status"], "not-run")
        self.assertIn("| empty-design | graded | 2/2 | yes | yes |", scen.format_results(results))

    def test_verdicts_flag_invented_quotes_and_missing_items(self):
        case = {"assertions": ["one", "two"]}
        rows = scen.parse_verdicts(json.dumps({"verdicts": [
            {"assertion": "A1", "verdict": "PASS", "quote": "never said", "reason": "r"}]}), case, "evidence")
        self.assertFalse(rows[0]["quote_found"])
        self.assertEqual(rows[1]["verdict"], "UNGRADED")

    def test_files_backend_run_only_prepares(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = make_root(Path(tmp) / "repo")
            out = io.StringIO()
            with redirect_stdout(out), redirect_stderr(io.StringIO()):
                code = scen.main(["run", "--root", str(root), "--ids", "empty-design,imaginary-project",
                                  "--backend", "files", "--tmp-root", str(Path(tmp) / "runs")])
            self.assertEqual(code, 0)
            self.assertIn("final.md", out.getvalue())


if __name__ == "__main__":
    unittest.main()
