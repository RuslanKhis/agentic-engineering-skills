"""Exercise the paired-difference helper through its CLI with synthetic trial records."""

import csv
import importlib.util
import json
import math
import random
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "paired_difference.py"
FIELDS = ["trial_id", "case_id", "scenario", "outcome", "reward"]


def load_module():
    spec = importlib.util.spec_from_file_location("paired_difference", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run(*args):
    completed = subprocess.run([sys.executable, "-I", str(SCRIPT), *map(str, args)],
                               capture_output=True, text=True, timeout=60)
    return completed.returncode, completed.stdout, completed.stderr


def sample_sd(values):
    mean = sum(values) / len(values)
    return math.sqrt(sum((v - mean) ** 2 for v in values) / (len(values) - 1))


class PairedDifferenceTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)

    def write(self, name, rows):
        path = self.root / name
        with path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=FIELDS)
            writer.writeheader()
            for number, row in enumerate(rows):
                writer.writerow({"trial_id": f"{name}-{number}", "scenario": "", "outcome": "", "reward": "", **row})
        return path

    def arms(self, base_scores, cand_scores, scenarios=None):
        """Per-case lists of run scores to two trial files."""
        def rows(scores):
            out = []
            for index, runs in enumerate(scores):
                for value in runs:
                    out.append({"case_id": f"c{index:03d}", "reward": value,
                                "scenario": scenarios[index] if scenarios else ""})
            return out
        return self.write("base.csv", rows(base_scores)), self.write("cand.csv", rows(cand_scores))

    def report(self, base, cand, *extra):
        code, out, err = run("--baseline", base, "--candidate", cand, "--json", *extra)
        self.assertNotEqual(code, 2, err)
        return code, json.loads(out)

    def test_unclustered_se_is_the_sample_sd_over_root_n(self):
        base = [[0.0], [1.0], [0.0], [1.0], [0.5], [0.0], [1.0], [0.0]]
        cand = [[1.0], [1.0], [0.0], [1.0], [1.0], [1.0], [0.0], [1.0]]
        b, c = self.arms(base, cand)
        code, r = self.report(b, c)
        diffs = [cc[0] - bb[0] for bb, cc in zip(base, cand)]
        self.assertEqual(code, 0)
        self.assertAlmostEqual(r["difference"], sum(diffs) / 8)
        self.assertAlmostEqual(r["se"], sample_sd(diffs) / math.sqrt(8))
        self.assertEqual(r["df"], 7)
        half = 2.3646 * r["se"]  # t(0.975, 7)
        self.assertAlmostEqual(r["interval"][1] - r["difference"], half, places=3)

    def test_repeated_runs_count_once_per_case(self):
        base = [[0.0], [1.0], [0.0], [1.0], [0.0], [1.0]]
        cand = [[1.0], [1.0], [0.0], [1.0], [1.0], [1.0]]
        b1, c1 = self.arms(base, cand)
        _, once = self.report(b1, c1)
        b3, c3 = self.arms([r * 3 for r in base], [r * 3 for r in cand])
        _, thrice = self.report(b3, c3)
        self.assertAlmostEqual(once["se"], thrice["se"])
        self.assertEqual(thrice["cases_paired"], 6)

    def test_scenario_clustering_widens_the_error_when_variants_move_together(self):
        base = [[0.0]] * 12
        cand = [[1.0]] * 3 + [[0.0]] * 9  # three variants of one scenario all improve
        scen = ["s1"] * 3 + ["s2"] * 3 + ["s3"] * 3 + ["s4"] * 3
        b, c = self.arms(base, cand)
        _, flat = self.report(b, c)
        b, c = self.arms(base, cand, scen)
        _, clustered = self.report(b, c)
        self.assertEqual(clustered["clusters"], 4)
        self.assertEqual(clustered["df"], 3)
        self.assertGreater(clustered["se"], flat["se"] * 1.5)
        self.assertIn("scenario", clustered["method"])

    def test_verdicts_and_require(self):
        base = [[0.0, 0.0, 0.0]] * 30
        cand = [[1.0, 1.0, 1.0]] * 20 + [[0.0, 0.0, 0.0]] * 10
        b, c = self.arms(base, cand)
        code, r = self.report(b, c, "--require", "improved")
        self.assertEqual((code, r["verdict"], r["require"]["met"]), (0, "improved", True))
        code, r = self.report(c, b, "--require", "improved")
        self.assertEqual((code, r["verdict"]), (1, "worse"))

    def test_within_noise(self):
        base = [[1.0], [0.0]] * 10
        cand = [[1.0], [0.0]] * 9 + [[1.0], [1.0]]
        b, c = self.arms(base, cand)
        code, r = self.report(b, c, "--require", "improved")
        self.assertEqual(code, 1)
        self.assertEqual(r["verdict"], "within noise")
        self.assertLess(r["interval"][0], 0)

    def test_not_worse_with_margin(self):
        base = [[1.0], [1.0], [0.0], [1.0]] * 10
        cand = [[1.0], [1.0], [0.0], [1.0]] * 9 + [[1.0], [0.0], [0.0], [1.0]]
        b, c = self.arms(base, cand)
        code, r = self.report(b, c, "--require", "not-worse", "--margin", 0.10)
        self.assertEqual(code, 0)
        self.assertGreater(r["interval"][0], -0.10)
        code, _ = self.report(b, c, "--require", "not-worse", "--margin", 0.0)
        self.assertEqual(code, 1)

    def test_minimum_detectable_difference_and_plan(self):
        module = load_module()
        # Cases differ in difficulty (between-case variance) and runs disagree within a case (run noise),
        # independently in the two versions.
        rng = random.Random(7)
        difficulty = [rng.random() for _ in range(60)]
        base = [[float(rng.random() < p) for _ in range(3)] for p in difficulty]
        cand = [[float(rng.random() < min(p + 0.1, 1.0)) for _ in range(3)] for p in difficulty]
        b, c = self.arms(base, cand)
        _, r = self.report(b, c, "--target-difference", 0.05, "--plan-runs", 10)
        self.assertNotIn("note", r["variance"])
        df = r["df"]
        expected_mdd = (module.t_quantile(0.975, df) + module.t_quantile(0.8, df)) * r["se"]
        self.assertAlmostEqual(r["minimum_detectable_difference"], expected_mdd)
        per_case_var = r["cases_paired"] * r["se"] ** 2
        z_cases = 7.848879734349086 * per_case_var / 0.05 ** 2
        now, later = r["plan"]["at_current_runs"], r["plan"]["at_planned_runs"]
        self.assertGreaterEqual(now["cases_needed"], math.ceil(z_cases))
        self.assertLess(now["cases_needed"], z_cases * 1.05)
        self.assertFalse(r["plan"]["detectable_now"])
        self.assertGreater(r["variance"]["share_from_run_noise"], 0)
        self.assertLess(later["cases_needed"], now["cases_needed"])

    def test_clustered_plan_counts_scenarios_as_units(self):
        # Two identical variants of each case in one scenario add no information:
        # the SE is unchanged and the plan needs the same number of scenarios, so twice the cases.
        rng = random.Random(3)
        difficulty = [rng.random() for _ in range(30)]
        base = [[float(rng.random() < p) for _ in range(3)] for p in difficulty]
        cand = [[float(rng.random() < min(p + 0.15, 1.0)) for _ in range(3)] for p in difficulty]
        b, c = self.arms(base, cand)
        _, single = self.report(b, c, "--target-difference", 0.1)
        doubled_base = [runs for runs in base for _ in range(2)]
        doubled_cand = [runs for runs in cand for _ in range(2)]
        scen = [f"s{i // 2}" for i in range(60)]
        b, c = self.arms(doubled_base, doubled_cand, scen)
        _, doubled = self.report(b, c, "--target-difference", 0.1)
        self.assertEqual(doubled["clusters"], 30)
        self.assertAlmostEqual(doubled["se"], single["se"])
        one, two = single["plan"]["at_current_runs"], doubled["plan"]["at_current_runs"]
        self.assertEqual(two["scenarios_needed"], one["cases_needed"])
        self.assertEqual(two["cases_needed"], 2 * one["cases_needed"])

    def test_run_noise_overshoot_is_not_estimable(self):
        # Identical run patterns in both versions: the noise estimate overshoots the paired variance.
        base = [[0.0, 1.0, 0.0], [1.0, 1.0, 1.0], [0.0, 0.0, 0.0], [1.0, 0.0, 1.0]] * 5
        cand = [[1.0, 1.0, 0.0], [1.0, 1.0, 1.0], [0.0, 1.0, 0.0], [1.0, 1.0, 1.0]] * 5
        b, c = self.arms(base, cand)
        _, r = self.report(b, c, "--target-difference", 0.05, "--plan-runs", 10)
        self.assertIsNone(r["variance"]["share_from_run_noise"])
        self.assertIn("not estimable", r["variance"]["note"])
        self.assertIn("not_estimable", r["plan"]["at_planned_runs"])
        self.assertIsNotNone(r["plan"]["at_current_runs"]["cases_needed"])

    def test_plan_runs_unknown_with_one_run(self):
        b, c = self.arms([[0.0], [1.0], [0.0]], [[1.0], [1.0], [0.0]])
        _, r = self.report(b, c, "--target-difference", 0.1, "--plan-runs", 3)
        self.assertIn("two runs", r["plan"]["at_planned_runs"]["not_estimable"])

    def test_plan_cases_reports_the_detectable_difference(self):
        module = load_module()
        rng = random.Random(11)
        difficulty = [rng.random() for _ in range(40)]
        base = [[float(rng.random() < p) for _ in range(3)] for p in difficulty]
        cand = [[float(rng.random() < min(p + 0.1, 1.0)) for _ in range(3)] for p in difficulty]
        b, c = self.arms(base, cand)
        _, r = self.report(b, c, "--plan-cases", 160)
        # Four times the cases halves the SE; at the same cases it reproduces the sample's own MDD.
        per_case_var = r["cases_paired"] * r["se"] ** 2
        expected = ((module.t_quantile(0.975, 159) + module.t_quantile(0.8, 159)) * math.sqrt(per_case_var / 160))
        self.assertAlmostEqual(r["plan"]["at_current_runs"]["detectable_with_planned_cases"], expected)
        _, same = self.report(b, c, "--plan-cases", 40)
        self.assertAlmostEqual(same["plan"]["at_current_runs"]["detectable_with_planned_cases"],
                               same["minimum_detectable_difference"])
        code, out, _ = run("--baseline", b, "--candidate", c, "--plan-cases", 160, "--target-difference", 0.05)
        self.assertEqual(code, 0)
        self.assertIn("160 cases could detect", out)
        self.assertIn("cannot detect 5.0 points", out)

    def test_paper_sample_size(self):
        module = load_module()
        # Miller (2024), section 5: omega^2 = 1/9, delta = 0.03, alpha 0.05, power 0.8 gives about 969 with z.
        self.assertIn(module.clusters_needed(1 / 9, 0.03, 0.05, 0.8), range(969, 975))

    def test_t_quantiles_match_tables(self):
        module = load_module()
        for p, df, value in ((0.975, 1, 12.706), (0.975, 9, 2.262), (0.975, 19, 2.093), (0.8, 19, 0.861)):
            self.assertAlmostEqual(module.t_quantile(p, df), value, places=3)

    def test_unpaired_and_infra_errors_are_incomplete(self):
        b = self.write("base.csv", [{"case_id": "a", "reward": 1}, {"case_id": "b", "reward": 0},
                                    {"case_id": "c", "reward": 1}, {"case_id": "d", "outcome": "infra_error"}])
        c = self.write("cand.csv", [{"case_id": "a", "reward": 1}, {"case_id": "b", "reward": 1},
                                    {"case_id": "c", "reward": 1}, {"case_id": "d", "reward": 1}])
        code, out, _ = run("--baseline", b, "--candidate", c, "--json")
        r = json.loads(out)
        self.assertEqual(code, 3)
        self.assertEqual(r["cases_unpaired"], ["d"])
        self.assertEqual(r["infra_error_rows"]["baseline"], 1)
        code, out, _ = run("--baseline", b, "--candidate", c)
        self.assertIn("INCOMPLETE", out)

    def test_outcome_pass_fail_is_scored(self):
        b = self.write("base.csv", [{"case_id": x, "outcome": "fail"} for x in "abcd"])
        c = self.write("cand.csv", [{"case_id": x, "outcome": "pass"} for x in "abcd"])
        code, r = self.report(b, c)
        self.assertEqual(code, 0)
        self.assertEqual(r["difference"], 1.0)
        self.assertIn("note", r)

    def test_bad_input(self):
        good = self.write("good.csv", [{"case_id": "a", "reward": 1}, {"case_id": "b", "reward": 0}])
        cases = {
            "dup.csv": [{"case_id": "a", "reward": 1, "trial_id": "t1"}, {"case_id": "b", "reward": 1, "trial_id": "t1"}],
            "noscore.csv": [{"case_id": "a"}],
            "nan.csv": [{"case_id": "a", "reward": "nan"}],
            "twoscen.csv": [{"case_id": "a", "reward": 1, "scenario": "x"}, {"case_id": "a", "reward": 1, "scenario": "y"}],
        }
        for name, rows in cases.items():
            path = self.root / name
            with path.open("w", newline="", encoding="utf-8") as handle:
                writer = csv.DictWriter(handle, fieldnames=FIELDS)
                writer.writeheader()
                for row in rows:
                    writer.writerow({"trial_id": "", "scenario": "", "outcome": "", "reward": "", **row})
            code, _, err = run("--baseline", good, "--candidate", path)
            self.assertEqual(code, 2, name)
            self.assertIn("paired_difference.py", err)
        code, _, _ = run("--baseline", good, "--candidate", self.root / "missing.csv")
        self.assertEqual(code, 2)
        code, _, _ = run("--baseline", good, "--candidate", good, "--margin", "0.1")
        self.assertEqual(code, 2)

    def test_jsonl_input(self):
        b = self.root / "base.jsonl"
        c = self.root / "cand.jsonl"
        b.write_text("\n".join(json.dumps({"case_id": x, "reward": 0.5}) for x in "abc") + "\n", encoding="utf-8")
        c.write_text("\n".join(json.dumps({"case_id": x, "reward": v}) for x, v in zip("abc", (0.5, 1, 0.75))),
                     encoding="utf-8")
        code, r = self.report(b, c)
        self.assertEqual(code, 0)
        self.assertAlmostEqual(r["difference"], 0.25)


if __name__ == "__main__":
    unittest.main()
