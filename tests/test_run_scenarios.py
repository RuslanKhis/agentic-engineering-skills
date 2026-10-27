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
    (base / "evals" / "graders" / "with-seed").mkdir(parents=True)
    (base / "evals" / "graders" / "with-seed" / "answers.json").write_text('{"fixed": "SECRET-ANSWER"}')
    (base / "evals" / "scenarios.json").write_text(json.dumps({"version": 1, "cases": cases}))
    (base / "evals" / "scenario-fixtures.json").write_text(json.dumps({"version": 1, "scenarios": {
        "empty-design": {"status": "runnable", "note": "n"},
        "with-seed": {"status": "repo-fixture", "copy": [{"from": "fixtures/seed", "to": "."}],
                      "grader": [{"from": "evals/graders/with-seed/answers.json"}]},
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

    def test_grader_material_reaches_the_judge_but_not_the_workspace(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = make_root(Path(tmp) / "repo")
            cases, _ = scen.load_scenarios(root)
            run_dir, manifest = scen.prepare(root, [cases[1]], scen.load_fixtures(root), Path(tmp) / "runs")
            case_dir = run_dir / "with-seed"
            self.assertEqual(manifest["scenarios"][0]["grader_files"], ["answers.json"])
            self.assertTrue((case_dir / "grader/answers.json").exists())
            workspace_text = "".join(p.read_text() for p in (case_dir / "workspace").rglob("*") if p.is_file())
            self.assertNotIn("SECRET-ANSWER", workspace_text)
            self.assertNotIn("SECRET-ANSWER", (case_dir / "task.md").read_text())
            (case_dir / "final.md").write_text("Fixed.")
            pending = scen.judge_case(run_dir, cases[1], "files", "human", 60)
            self.assertEqual(pending["status"], "awaiting-judge")
            prompt = (case_dir / "judge-prompt.md").read_text()
            self.assertIn("SECRET-ANSWER", prompt.split("## Evidence")[0])
            self.assertNotIn("SECRET-ANSWER", prompt.split("## Evidence")[1])

    def test_grader_material_outside_evals_graders_is_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = make_root(Path(tmp) / "repo")
            cases, _ = scen.load_scenarios(root)
            fixtures = {"with-seed": {"status": "repo-fixture", "copy": [{"from": "fixtures/seed", "to": "."}],
                                      "grader": [{"from": "skills/beta-skill/SKILL.md"}]}}
            with self.assertRaises(scen.InputError):
                scen.classify(cases[1], fixtures, root)

    def test_base_and_overlay_compose_a_workspace(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = make_root(Path(tmp) / "repo")
            base = root / "evals/fixtures/base/app"
            (base / "app").mkdir(parents=True)
            (base / "app/agent.py").write_text("BASE = 1\n")
            (base / "app/tools.py").write_text("TOOLS = 1\n")
            (base / "README.md").write_text("base readme\n")
            overlay = root / "evals/fixtures/with-seed"
            (overlay / "app").mkdir(parents=True)
            (overlay / "app/agent.py").write_text("OVERLAY = 1\n")
            (overlay / "tickets").mkdir()
            (overlay / "tickets/T-1.md").write_text("ticket\n")
            cases, _ = scen.load_scenarios(root)
            fixtures = {"with-seed": {"status": "repo-fixture", "base": ["app"], "overlay": True,
                                      "copy": [{"from": "fixtures/seed", "to": "seed"}],
                                      "remove": ["README.md"]}}
            self.assertEqual([c["from"] for c in scen.fixture_copies("with-seed", fixtures["with-seed"])],
                             ["evals/fixtures/base/app", "fixtures/seed", "evals/fixtures/with-seed"])
            self.assertEqual(scen.classify(cases[1], fixtures, root)["status"], "repo-fixture")
            run_dir, _ = scen.prepare(root, [cases[1]], fixtures, Path(tmp) / "runs")
            ws = run_dir / "with-seed/workspace"
            self.assertEqual((ws / "app/agent.py").read_text(), "OVERLAY = 1\n")
            self.assertEqual((ws / "app/tools.py").read_text(), "TOOLS = 1\n")
            self.assertTrue((ws / "tickets/T-1.md").exists())
            self.assertTrue((ws / "seed/service.py").exists())
            self.assertFalse((ws / "README.md").exists())
            digest = json.loads((run_dir / "with-seed/fixture-digest.json").read_text())
            self.assertIn("app/agent.py", digest)
            self.assertNotIn("README.md", digest)

    def test_missing_base_or_overlay_leaves_the_scenario_fixture_missing(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = make_root(Path(tmp) / "repo")
            cases, _ = scen.load_scenarios(root)
            fixtures = {"with-seed": {"status": "repo-fixture", "base": ["absent-app"], "overlay": True}}
            entry = scen.classify(cases[1], fixtures, root)
        self.assertEqual(entry["status"], "fixture-missing")
        self.assertIn("evals/fixtures/base/absent-app", entry["partial"])
        self.assertIn("evals/fixtures/with-seed", entry["partial"])

    def test_removal_must_name_a_supplied_path_inside_the_workspace(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = make_root(Path(tmp) / "repo")
            cases, _ = scen.load_scenarios(root)
            for remove in (["absent.py"], ["../outside"]):
                fixtures = {"with-seed": {"status": "repo-fixture", "copy": [{"from": "fixtures/seed", "to": "."}],
                                          "remove": remove}}
                with self.subTest(remove=remove), self.assertRaises(scen.InputError):
                    scen.prepare(root, [cases[1]], fixtures, Path(tmp) / f"runs-{len(remove[0])}")

    def test_not_representable_needs_a_reason_and_is_never_prepared(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = make_root(Path(tmp) / "repo")
            cases, _ = scen.load_scenarios(root)
            with self.assertRaises(scen.InputError):
                scen.classify(cases[2], {"imaginary-project": {"status": "not-representable"}}, root)
            fixtures = {"imaginary-project": {"status": "not-representable", "reason": "needs a live cloud"}}
            self.assertEqual(scen.classify(cases[2], fixtures, root)["status"], "not-representable")
            listing = scen.format_list(cases, fixtures, root)
            self.assertIn("## not-representable (1)", listing)
            self.assertIn("needs a live cloud", listing)
            run_dir, manifest = scen.prepare(root, [cases[2]], fixtures, Path(tmp) / "runs")
        self.assertFalse((run_dir / "imaginary-project").exists())
        self.assertEqual(manifest["scenarios"][0]["status"], "not-representable")

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
                "total_cost_usd": 0.2, "result": "Wrote design.md with one risk: cost.",
                "permission_denials": [{"tool_name": "Read", "tool_use_id": "t",
                                        "tool_input": {"file_path": "/home/u/.claude/CLAUDE.md"}}]}),
]


def verdicts(*values):
    return json.dumps({"verdicts": [{"assertion": f"A{i}", "verdict": v, "quote": "# Design", "reason": "r"}
                                    for i, v in enumerate(values, 1)]})


class AgentAndJudgeTests(unittest.TestCase):
    def test_parse_transcript(self):
        summary = scen.parse_transcript(TRANSCRIPT)
        self.assertEqual(summary["skills_loaded"], ["alpha-skill", "beta-skill"])
        self.assertEqual(summary["skill_files_read"], ["beta-skill/SKILL.md", "gamma-skill/references/x.md"])
        self.assertEqual(summary["final"], "Wrote design.md with one risk: cost.")
        self.assertEqual(summary["result"]["num_turns"], 3)
        self.assertEqual(len(summary["tool_calls"]), 3)
        self.assertEqual(summary["skill_tool_calls"], ["alpha-skill"])
        self.assertEqual(summary["skill_md_reads"], ["beta-skill"])
        self.assertEqual(summary["permission_denials"][0]["tool"], "Read")

    def test_long_files_keep_head_and_tail_for_the_judge(self):
        text = "HEAD" + "x" * 50_000 + "TAIL"
        clipped = scen.clip(text, limit=3_000)
        self.assertTrue(clipped.startswith("HEAD"))
        self.assertTrue(clipped.endswith("TAIL"))
        self.assertIn("characters omitted", clipped)
        self.assertEqual(scen.clip("short", limit=3_000), "short")

    def test_leading_slash_command_counts_as_loading_a_catalogued_skill(self):
        transcript = [json.dumps({"type": "system", "subtype": "init", "skills": ["alpha-skill", "beta-skill"]})]
        summary = scen.parse_transcript(transcript, "/beta-skill Carry out docs/tickets/G01.md.")
        self.assertEqual(summary["skills_loaded"], ["beta-skill"])
        self.assertEqual(scen.skill_md_loaded(summary, ["beta-skill"])["beta-skill"]["how"], "slash-command")
        self.assertEqual(scen.parse_transcript(transcript, "/gamma-skill go")["skills_loaded"], [])
        self.assertEqual(scen.parse_transcript(transcript, "Use /beta-skill later")["skills_loaded"], [])

    def test_skill_md_loaded_per_installed_skill(self):
        summary = scen.parse_transcript(TRANSCRIPT)
        report = scen.skill_md_loaded(summary, ["alpha-skill", "beta-skill", "gamma-skill"])
        self.assertEqual(report["alpha-skill"]["how"], "skill-tool")
        self.assertEqual(report["beta-skill"]["how"], "read")
        self.assertEqual(report["gamma-skill"], {"loaded": False, "how": None, "other_files_read": 1})

    def test_catalogue_check_flags_repository_skills_that_were_not_installed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = make_root(Path(tmp))
            check = scen.catalogue_check(["alpha-skill", "beta-skill", "dataviz"], ["alpha-skill"], root)
            self.assertEqual(check, {"missing": [], "leaked": ["beta-skill"]})
            self.assertEqual(scen.catalogue_check(["dataviz"], ["alpha-skill"], root)["missing"], ["alpha-skill"])

    def test_agent_command_is_bounded_project_scoped_and_confined(self):
        command = scen.agent_command("claude-sonnet-5-5", 30, scen.AGENT_TOOLS, 2.5)
        value = lambda flag: command[command.index(flag) + 1]
        self.assertEqual(value("--setting-sources"), "project,local")
        self.assertEqual(value("--max-turns"), "30")
        self.assertEqual(value("--max-budget-usd"), "2.5")
        self.assertNotIn("Bash", value("--tools"))
        self.assertEqual(value("--permission-mode"), "dontAsk")
        self.assertEqual(value("--permission-prompts"), "none")
        rules = value("--allowedTools").split(",")
        self.assertEqual(sorted(rules), ["Edit(./**)", "Read(./**)", "Skill", "Write(./**)"])
        self.assertNotIn("Glob", rules)  # a bare Glob rule reaches ~/.claude
        self.assertNotIn("--add-dir", command)
        self.assertIn("--strict-mcp-config", command)
        self.assertTrue(scen.confinement(scen.AGENT_TOOLS, "project")["confined_to_workspace"])
        widened = scen.confinement(scen.AGENT_TOOLS + ",Bash", "project")
        self.assertEqual(widened["unconfined_tools"], ["Bash"])
        self.assertFalse(widened["confined_to_workspace"])

    def test_add_dir_install_keeps_skills_out_of_the_workspace(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = make_root(Path(tmp) / "repo")
            cases, _ = scen.load_scenarios(root)
            run_dir, manifest = scen.prepare(root, cases[:1], scen.load_fixtures(root), Path(tmp) / "runs",
                                             skill_install="add-dir")
            case_dir = run_dir / "empty-design"
            self.assertEqual(manifest["skill_install"], "add-dir")
            self.assertTrue((case_dir / "skills-host/.claude/skills/alpha-skill/SKILL.md").exists())
            self.assertFalse((case_dir / "workspace/.claude").exists())
            seen = {}

            class Proc:
                returncode = 0
                stdout = "\n".join(TRANSCRIPT)

            def runner(command, **kwargs):
                seen["command"] = command
                return Proc()

            scen.run_agent(run_dir, manifest["scenarios"][0], "m", 5, 60, scen.AGENT_TOOLS, None,
                           runner=runner, skill_install="add-dir", root=root)
            self.assertEqual(seen["command"][seen["command"].index("--add-dir") + 1],
                             str(case_dir / "skills-host"))

    def test_skills_are_copied_not_linked(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = make_root(Path(tmp) / "repo")
            (Path(tmp) / "outside.md").write_text("outside")
            (root / "skills/alpha-skill/linked.md").symlink_to(Path(tmp) / "outside.md")
            cases, _ = scen.load_scenarios(root)
            run_dir, _ = scen.prepare(root, cases[:1], scen.load_fixtures(root), Path(tmp) / "runs")
            copied = run_dir / "empty-design/workspace/.claude/skills/alpha-skill"
            self.assertFalse(any(p.is_symlink() for p in copied.rglob("*")))
            self.assertEqual((copied / "linked.md").read_text(), "outside")

    def test_run_directory_inside_the_repository_is_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = make_root(Path(tmp) / "repo")
            cases, _ = scen.load_scenarios(root)
            with self.assertRaises(scen.InputError):
                scen.prepare(root, cases[:1], scen.load_fixtures(root), root / "runs")

    def test_judge_repeats_take_the_majority_and_flag_disagreement(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = make_root(Path(tmp) / "repo")
            cases, _ = scen.load_scenarios(root)
            run_dir, _ = scen.prepare(root, cases[:1], scen.load_fixtures(root), Path(tmp) / "runs")
            case_dir = run_dir / "empty-design"
            (case_dir / "final.md").write_text("# Design")
            replies = iter([verdicts("PASS", "FAIL"), verdicts("PASS", "PASS"), verdicts("PASS", "FAIL")])
            prompts = []

            def caller(backend, prompt, system, model, timeout):
                prompts.append(prompt)
                return scen.call_model.__globals__["ModelReply"](text=next(replies), model=model)

            graded = scen.judge_case(run_dir, cases[0], "claude-cli", "m", 60, repeats=3, caller=caller)
        self.assertEqual(len(prompts), 3)
        self.assertEqual(len(set(prompts)), 1)
        self.assertEqual(graded["judge_repeats"], 3)
        self.assertEqual([r["verdict"] for r in graded["assertions"]], ["PASS", "FAIL"])
        self.assertEqual(graded["assertions"][1]["votes"], ["FAIL", "PASS", "FAIL"])
        self.assertEqual(graded["assertions"][1]["agreement"], 0.67)
        self.assertEqual(graded["unstable"], [2])
        self.assertEqual(graded["passed"], 1)

    def test_judge_cost_is_summed_over_repeats(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = make_root(Path(tmp) / "repo")
            cases, _ = scen.load_scenarios(root)
            run_dir, _ = scen.prepare(root, cases[:1], scen.load_fixtures(root), Path(tmp) / "runs")
            (run_dir / "empty-design" / "final.md").write_text("# Design")

            def caller(backend, prompt, system, model, timeout):
                return scen.call_model.__globals__["ModelReply"](text=verdicts("PASS", "PASS"), model=model,
                                                                 cost_usd=0.125)

            graded = scen.judge_case(run_dir, cases[0], "claude-cli", "m", 60, repeats=2, caller=caller)
        self.assertEqual(graded["judge_cost_usd"], 0.25)

    def test_majority_needs_more_than_half_to_pass(self):
        rows = lambda v: [{"n": 1, "verdict": v, "quote": "", "quote_found": False, "reason": ""}]
        tie = scen.majority([rows("PASS"), rows("FAIL")])[0]
        self.assertEqual((tie["verdict"], tie["unstable"]), ("FAIL", True))
        split = scen.majority([rows("PASS"), rows("UNGRADED"), rows("FAIL")])[0]
        self.assertEqual(split["verdict"], "FAIL")
        self.assertEqual(split["agreement"], 0.33)
        same = scen.majority([rows("PASS")] * 3)[0]
        self.assertEqual((same["verdict"], same["agreement"], same["unstable"]), ("PASS", 1.0, False))

    def test_unreadable_judge_reply_is_asked_for_once_more(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = make_root(Path(tmp) / "repo")
            cases, _ = scen.load_scenarios(root)
            run_dir, _ = scen.prepare(root, cases[:1], scen.load_fixtures(root), Path(tmp) / "runs")
            replies = iter(['{"verdicts": [,}', verdicts("PASS", "PASS")])

            def caller(backend, prompt, system, model, timeout):
                return scen.call_model.__globals__["ModelReply"](text=next(replies), model=model)

            graded = scen.judge_case(run_dir, cases[0], "claude-cli", "m", 60, repeats=1, caller=caller)
            self.assertTrue((run_dir / "empty-design/judge-reply-1-retry.txt").exists())
        self.assertEqual((graded["status"], graded["judge_repeats"], graded["passed"]), ("graded", 1, 2))
        self.assertEqual(len(graded["judge_errors"]), 1)

    def test_judge_errors_on_every_repeat_are_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = make_root(Path(tmp) / "repo")
            cases, _ = scen.load_scenarios(root)
            run_dir, _ = scen.prepare(root, cases[:1], scen.load_fixtures(root), Path(tmp) / "runs")

            def caller(*args):
                raise scen.BackendError("down")

            graded = scen.judge_case(run_dir, cases[0], "claude-cli", "m", 60, repeats=2, caller=caller)
        self.assertEqual(graded["status"], "judge-error")
        self.assertIn("down", graded["error"])

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
            record = scen.run_agent(run_dir, entry, "m", 5, 60, scen.AGENT_TOOLS, None, runner=runner, root=root)
            self.assertEqual(record["skills_loaded"], ["alpha-skill", "beta-skill"])
            self.assertEqual(record["skill_md_loaded"]["alpha-skill"]["how"], "skill-tool")
            self.assertEqual(record["catalogue_check"], {"missing": [], "leaked": []})
            self.assertEqual(record["permission_denials"][0]["tool"], "Read")
            self.assertIn("dontAsk", record["command"])
            self.assertTrue(seen["env"]["AGENTIC_ENGINEERING_HOME"].startswith(str(run_dir)))
            self.assertEqual(seen["env"]["CLAUDE_CODE_DISABLE_AUTO_MEMORY"], "1")
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
        self.assertEqual(rows["empty-design"]["skill_md_loaded"], {"alpha-skill": True})
        self.assertIn("| empty-design | graded | 2/2 | none | 1.00 | yes | yes |", scen.format_results(results))

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
