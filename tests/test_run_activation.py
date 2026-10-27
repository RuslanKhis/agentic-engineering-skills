"""Offline checks for the activation runner; no model or network calls."""

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


act = load_module("run_activation", ROOT / "scripts/run_activation.py")
scen = load_module("run_scenarios", ROOT / "scripts/run_scenarios.py")
backends = sys.modules["model_backends"]


def make_root(base: Path) -> Path:
    """A miniature repository: three skills and six activation cases."""
    skills = {
        "alpha-skill": 'name: alpha-skill\ndescription: "Alpha work. Do not activate for beta work."',
        "beta-skill": "name: beta-skill\ndescription: >-\n  Beta work across\n  two lines.\nlicense: MIT",
        "gamma-skill": "name: gamma-skill\ndescription: Gamma work\n  continued plainly.\nmetadata:\n  version: x",
    }
    for name, front in skills.items():
        (base / "skills" / name).mkdir(parents=True)
        (base / "skills" / name / "SKILL.md").write_text(f"---\n{front}\n---\n\n# {name}\n")
    cases = []
    for skill in skills:
        cases.append({"id": f"{skill}-positive", "skill": skill, "prompt": f"Please do {skill} things.",
                      "should_trigger": True, "rationale": "r"})
        cases.append({"id": f"{skill}-near-miss", "skill": skill, "prompt": f"Not {skill} at all.",
                      "should_trigger": False, "rationale": "r"})
    (base / "evals").mkdir()
    (base / "evals" / "activation.json").write_text(json.dumps({"version": 1, "cases": cases}))
    return base


def answer_all(batch, chooser):
    return json.dumps({"answers": [{"item": act.item_label(i), "primary": chooser(case),
                                    "supporting": [], "reason": "because"}
                                   for i, case in enumerate(batch)]})


class CatalogueTests(unittest.TestCase):
    def test_frontmatter_scalar_styles(self):
        with tempfile.TemporaryDirectory() as tmp:
            catalogue = act.load_catalogue(make_root(Path(tmp)))
        self.assertEqual([e["name"] for e in catalogue], ["alpha-skill", "beta-skill", "gamma-skill"])
        self.assertEqual(catalogue[0]["description"], "Alpha work. Do not activate for beta work.")
        self.assertEqual(catalogue[1]["description"], "Beta work across two lines.")
        self.assertEqual(catalogue[2]["description"], "Gamma work continued plainly.")

    def test_single_quotes_and_missing_frontmatter(self):
        fields = act.parse_frontmatter("---\nname: x\ndescription: 'It''s here'\n---\n")
        self.assertEqual(fields["description"], "It's here")
        with self.assertRaises(ValueError):
            act.parse_frontmatter("# no frontmatter\n")

    def test_installed_skills_match_yaml(self):
        try:
            import yaml
        except ImportError:
            self.skipTest("PyYAML is not installed")
        for entry in act.load_catalogue(ROOT):
            text = (ROOT / "skills" / entry["name"] / "SKILL.md").read_text(encoding="utf-8")
            front = yaml.safe_load(text.split("---", 2)[1])
            self.assertEqual(entry["name"], front["name"])
            self.assertEqual(entry["description"], front["description"].strip(), entry["name"])

    def test_catalogue_hash_is_order_independent_of_dict_keys(self):
        a = [{"name": "x", "description": "d"}]
        b = [{"description": "d", "name": "x"}]
        self.assertEqual(act.catalogue_sha256(a), act.catalogue_sha256(b))


class BatchingTests(unittest.TestCase):
    def setUp(self):
        self.cases = [{"id": f"case-{i:03d}", "prompt": str(i)} for i in range(114)]

    def test_deterministic_and_independent_of_file_order(self):
        first = act.make_batches(self.cases, 14, "seed:1")
        again = act.make_batches(list(reversed(self.cases)), 14, "seed:1")
        self.assertEqual([[c["id"] for c in b] for b in first], [[c["id"] for c in b] for b in again])
        other = act.make_batches(self.cases, 14, "seed:2")
        self.assertNotEqual([c["id"] for c in first[0]], [c["id"] for c in other[0]])

    def test_balanced_batches_cover_every_case_once(self):
        batches = act.make_batches(self.cases, 14, 7)
        sizes = [len(b) for b in batches]
        self.assertEqual(len(batches), 9)
        self.assertLessEqual(max(sizes) - min(sizes), 1)
        self.assertLessEqual(max(sizes), 14)
        ids = [c["id"] for b in batches for c in b]
        self.assertEqual(sorted(ids), sorted(c["id"] for c in self.cases))

    def test_repeats_reshuffle(self):
        jobs = act.plan(self.cases, 2, 14, 5)
        self.assertEqual({j[0] for j in jobs}, {1, 2})
        self.assertNotEqual([c["id"] for c in jobs[0][2]], [c["id"] for c in jobs[9][2]])

    def test_prompt_hides_ids_and_labels(self):
        batch = [{"id": "secret-near-miss", "skill": "alpha-skill", "should_trigger": False,
                  "rationale": "hidden rationale", "prompt": "Do a thing."}]
        prompt = act.build_prompt([{"name": "alpha-skill", "description": "d"}], batch)
        self.assertIn("Do a thing.", prompt)
        self.assertIn("R01", prompt)
        for leak in ("secret-near-miss", "hidden rationale", "should_trigger"):
            self.assertNotIn(leak, prompt)


class GradingTests(unittest.TestCase):
    def test_eight_october_rules(self):
        g = act.grade
        self.assertEqual(g(True, "a", "a", []), "PASS")
        self.assertEqual(g(True, "a", "b", ["a"]), "PARTIAL")
        self.assertEqual(g(True, "a", "none", []), "FAIL")
        self.assertEqual(g(False, "a", "b", []), "PASS")
        self.assertEqual(g(False, "a", "none", []), "PASS")
        self.assertEqual(g(False, "a", "b", ["a"]), "PARTIAL")
        self.assertEqual(g(False, "a", "a", ["b"]), "FAIL")

    def test_parse_answers_tolerates_fences_and_flags_unknown_names(self):
        text = ("Here you go:\n```json\n" + json.dumps({"answers": [
            {"item": "R01", "primary": "alpha-skill", "supporting": ["ghost", "beta-skill", "gamma-skill"],
             "reason": "r"}]}) + "\n```")
        answers = act.parse_answers(text, 1, {"alpha-skill", "beta-skill", "gamma-skill"})
        self.assertEqual(answers["R01"]["supporting"], ["ghost", "beta-skill"])
        self.assertEqual(answers["R01"]["unknown_names"], ["ghost"])
        self.assertEqual(answers["R01"]["supporting_trimmed"], ["gamma-skill"])

    def test_unusable_reply_grades_error(self):
        with self.assertRaises(backends.BackendError):
            act.parse_answers("no json here", 2, set())
        rows = act.grade_batch([{"id": "x", "skill": "a", "should_trigger": True}], None, 1, "boom")
        self.assertEqual(rows[0]["grade"], "ERROR")
        self.assertEqual(rows[0]["error"], "boom")

    def test_missing_item_grades_error(self):
        batch = [{"id": "x", "skill": "a", "should_trigger": True},
                 {"id": "y", "skill": "a", "should_trigger": False}]
        rows = act.grade_batch(batch, {"R01": {"primary": "a", "supporting": [], "reason": ""}}, 1)
        self.assertEqual([r["grade"] for r in rows], ["PASS", "ERROR"])


class RunAndResultsTests(unittest.TestCase):
    def test_model_backend_results_and_summary(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = make_root(Path(tmp))
            calls = []

            def fake_call(backend, prompt, system, model, timeout):
                calls.append(prompt)
                items = json.loads(prompt.split("## Requests\n\n", 1)[1].rsplit("\n\nReturn", 1)[0])
                answers = [{"item": it["item"], "reason": "r",
                            "primary": "alpha-skill" if "alpha-skill things" in it["request"] else "none",
                            "supporting": []} for it in items]
                return backends.ModelReply(text=json.dumps({"answers": answers}), model=model)

            original = act.call_model
            act.call_model = fake_call
            try:
                out = Path(tmp) / "results.json"
                stdout = io.StringIO()
                with redirect_stdout(stdout), redirect_stderr(io.StringIO()):
                    code = act.main(["--root", str(root), "--backend", "claude-cli", "--repeat", "2",
                                     "--batch-size", "4", "--out", str(out)])
            finally:
                act.call_model = original
            self.assertEqual(code, 0)
            results = json.loads(out.read_text())
        self.assertEqual(results["schema"], act.SCHEMA)
        self.assertEqual(results["model"], "claude-sonnet-5-5")
        self.assertEqual(len(results["catalogue_sha256"]), 64)
        self.assertEqual(len(results["cases"]), 12)
        self.assertEqual(results["summary"]["overall"], {"PASS": 8, "PARTIAL": 0, "FAIL": 4, "ERROR": 0})
        self.assertEqual(sorted(results["summary"]["not_pass"]),
                         ["beta-skill-positive", "gamma-skill-positive"])
        self.assertEqual(len(calls), 4)
        self.assertIn("| all | 8 | 0 | 4 | 0 |", stdout.getvalue())
        row = results["cases"][0]
        for key in ("id", "skill", "should_trigger", "repeat", "primary", "supporting", "reason", "grade"):
            self.assertIn(key, row)

    def test_files_round_trip(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = make_root(Path(tmp) / "repo")
            exchange = Path(tmp) / "exchange"
            with redirect_stdout(io.StringIO()):
                self.assertEqual(act.main(["--root", str(root), "--backend", "files", "--batch-size", "4",
                                           "--export", str(exchange)]), 0)
            manifest = json.loads((exchange / "manifest.json").read_text())
            prompts = sorted((exchange / "prompts").glob("*.md"))
            self.assertEqual(len(prompts), len(manifest["batches"]))
            for path in prompts:
                self.assertNotIn("-near-miss", path.read_text())
            cases = {c["id"]: c for c in json.loads((root / "evals/activation.json").read_text())["cases"]}
            for entry in manifest["batches"]:
                batch = [cases[cid] for _, cid in sorted(entry["items"].items())]
                (exchange / "answers" / f"{entry['stem']}.json").write_text(
                    answer_all(batch, lambda c: c["skill"] if c["should_trigger"] else "none"))
            out = Path(tmp) / "results.json"
            with redirect_stdout(io.StringIO()):
                code = act.main(["--root", str(root), "--backend", "files", "--import", str(exchange),
                                 "--model", "claude-opus-5-5", "--out", str(out)])
            self.assertEqual(code, 0)
            results = json.loads(out.read_text())
        self.assertEqual(results["backend"], "files")
        self.assertEqual(results["model"], "claude-opus-5-5")
        self.assertEqual(results["summary"]["overall"]["PASS"], 6)

    def test_import_refuses_changed_corpus(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = make_root(Path(tmp) / "repo")
            exchange = Path(tmp) / "exchange"
            with redirect_stdout(io.StringIO()):
                act.main(["--root", str(root), "--backend", "files", "--export", str(exchange)])
            data = json.loads((root / "evals/activation.json").read_text())
            data["cases"][0]["prompt"] = "changed"
            (root / "evals/activation.json").write_text(json.dumps(data))
            with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
                code = act.main(["--root", str(root), "--backend", "files", "--import", str(exchange)])
        self.assertEqual(code, 2)

    def test_only_filters_cases_but_keeps_catalogue(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = make_root(Path(tmp))
            cases, _ = act.load_cases(root, ["beta-skill"])
            self.assertEqual({c["skill"] for c in cases}, {"beta-skill"})
            with self.assertRaises(act.InputError):
                act.load_cases(root, ["no-such-skill"])

    def test_compare_reports_changes_and_new_fails(self):
        def results(grades):
            return {"model": "m", "catalogue_sha256": "c", "corpus_sha256": "k",
                    "cases": [{"id": cid, "repeat": 1, "grade": g} for cid, g in grades.items()]}
        old = results({"a": "PASS", "b": "PARTIAL", "c": "FAIL"})
        new = results({"a": "FAIL", "b": "PASS", "c": "FAIL"})
        lines, new_fails = act.compare(old, new)
        self.assertEqual(new_fails, 1)
        self.assertIn("a: PASS -> FAIL  NEW FAIL", lines)
        self.assertIn("b: PARTIAL -> PASS", lines)
        self.assertFalse(any(line.startswith("c:") for line in lines))
        with tempfile.TemporaryDirectory() as tmp:
            paths = [Path(tmp) / "old.json", Path(tmp) / "new.json"]
            paths[0].write_text(json.dumps(old))
            paths[1].write_text(json.dumps(new))
            with redirect_stdout(io.StringIO()):
                self.assertEqual(act.main(["--compare", *map(str, paths)]), 1)
                self.assertEqual(act.main(["--compare", str(paths[0]), str(paths[0])]), 0)


class BackendTests(unittest.TestCase):
    def test_only_keyless_backends_are_offered(self):
        for module in (act, scen):
            with self.assertRaises(SystemExit), redirect_stderr(io.StringIO()):
                module.parse_args(["--backend", "anthropic"] if module is act
                                  else ["judge", "--run-dir", "x", "--judge-backend", "anthropic"])
        self.assertFalse(hasattr(backends, "call_anthropic"))
        with self.assertRaises(backends.BackendError):
            backends.call_model("anthropic", "p", "s", "m")

    def test_claude_cli_isolation_flags_and_parsing(self):
        seen = {}

        class Proc:
            returncode = 0
            stderr = ""
            stdout = json.dumps({"result": '{"answers": []}', "is_error": False,
                                 "modelUsage": {"claude-haiku-5-5": {}}, "usage": {"input_tokens": 3},
                                 "total_cost_usd": 0.01})

        def runner(command, **kwargs):
            seen.update(command=command, **kwargs)
            return Proc()

        reply = backends.call_claude_cli("prompt", "system", "claude-haiku-5-5", runner=runner)
        self.assertEqual(reply.model, "claude-haiku-5-5")
        self.assertEqual(seen["input"], "prompt")
        for flag in ("--safe-mode", "--disable-slash-commands", "--strict-mcp-config", "--no-session-persistence"):
            self.assertIn(flag, seen["command"])
        self.assertEqual(seen["command"][seen["command"].index("--tools") + 1], "")
        self.assertNotEqual(Path(seen["cwd"]).resolve(), ROOT)


if __name__ == "__main__":
    unittest.main()
