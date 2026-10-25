"""Exercise the value-report checker through its CLI with a hand-written plan, brief and report."""

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "check_value_report.py"

PLAN = """# Plan: claims triage

### G09 — First month in production

- **Status and evidence:** verified_live.
  - M1: kind baseline; metric claims triaged within one day; value 61%; window 2026-04-01 to 2026-06-30;
    sample 9,840 claims; method claims system export; owner ops lead
  - M3: metric claims triaged within one day; value 74%; baseline 61% (M1, brief §4); window 2026-09-01 to 2026-09-30;
    sample 3,310 claims; method claims system export; owner ops lead; build v1.4.2
  - M4: metric reopened claims; value 3.1%; baseline 3.0% (brief §4); window 2026-09-01 to 2026-09-30;
    sample 3,310 claims; method claims system export; owner ops lead; build v1.4.2
  - M5: metric model and cloud spend; value £2,540; baseline n/a; window 2026-09-01 to 2026-09-30;
    method billing export filtered by app label; owner platform lead
  - M6: metric claims resolved with the agent's triage; value 4,100; baseline n/a; window 2026-09-01 to 2026-09-30;
    method claims system export; owner ops lead
  - M7: metric active handlers; value 38 of 52; baseline n/a; window 2026-09-01 to 2026-09-30;
    method sign-in log, active means one accepted triage in the month; owner ops lead
  - M8: metric handlers at full rollout; value 160; kind assumption; method assumed from the four-queue headcount
  - M9: metric triage share at full rollout; value 70%; kind assumption; method projected from the pilot queue
  - M2: metric claims triaged within one day; value 70%; baseline 61%; window 2026-08-01 to 2026-08-31;
    method claims system export
  - I1: date 2026-09-14; severity 2; effect 31 replies quoted a withdrawn clause; response paused auto-send; fix C4 test
  - I0: date 2026-08-20; severity 3; effect slow triage page; response restart; fix pool size

| ID | metric | value | baseline | window | method |
| --- | --- | --- | --- | --- | --- |
| M10 | escalations to a senior handler | 212 | 240 | 2026-09-01 to 2026-09-30 | case log |
"""

BRIEF = """## 4. First use case

- **Outcome measure:** share of claims triaged within one working day.
- **Baseline:** 61% (claims system export, Q2 2026, all four queues).
- **Counter-metric:** reopened claims.
- **Threshold sentences:** "If triage within a day for queue A drops below 65%, we will pause the agent."
"""

GOOD = """---
stage: value-report
period: 2026-09
title: Claims triage value report, September 2026
sources: docs/discovery/claims.md, docs/plans/claims.md
decider: Head of Claims Operations
date: 2026-10-07
call: continue
---

# Claims triage: September 2026

## Outcome against baseline

- Claims triaged within one day: 74% against a baseline of 61% (M3; baseline M1).

## Counter-metric

- Reopened claims: 3.1% against 3.0% (M4), within the margin on this sample.

## Adoption

- Active means one accepted triage in the month: 38 of 52 handlers (M7).
- Escalations to a senior handler fell to 212 (M10).

## Cost per outcome

- Actual: £0.62 per resolved claim: £2,540 spend (M5) over 4,100 resolved claims (M6).
- Estimate: £0.55 per resolved claim (C7, the plan's cost contract).

## Incidents

- I1: 2026-09-14, severity 2, 31 replies quoted a withdrawn clause; auto-send paused; C4 test added.

## Thresholds

| Threshold sentence (brief §4) | This period | Fired |
| --- | --- | --- |
| If triage within a day for queue A drops below 65%, we will pause the agent | 74% (M3) | no |

## Call: continue

The Head of Claims Operations decides on 2026-10-07. Continue on one queue; scale waits for the
fix in I1 to hold for a month. If scaled to four queues we estimate £0.58 per resolved claim (C7).
"""


def run(*args):
    completed = subprocess.run([sys.executable, "-I", str(SCRIPT), *map(str, args)],
                               capture_output=True, text=True, timeout=60)
    return completed.returncode, completed.stdout, completed.stderr


class ValueReportTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.plan = self.root / "plan.md"
        self.plan.write_text(PLAN, encoding="utf-8")
        self.brief = self.root / "brief.md"
        self.brief.write_text(BRIEF, encoding="utf-8")

    def check(self, report, *extra, plan=None):
        path = self.root / "report.md"
        path.write_text(report, encoding="utf-8")
        return run("--report", path, "--plan", plan or self.plan, *extra)

    def test_good_report_passes(self):
        code, out, err = self.check(GOOD, "--brief", self.brief)
        self.assertEqual(code, 0, out + err)
        self.assertIn("call continue by Head of Claims Operations", out)

    def test_table_records_are_read(self):
        code, out, _ = self.check(GOOD, "--json")
        self.assertIn("M10", json.loads(out)["records_found"])

    def test_figure_without_record_citation_fails(self):
        report = GOOD.replace("- Escalations to a senior handler fell to 212 (M10).",
                              "- Handlers saved 300 hours this month.")
        code, out, _ = self.check(report)
        self.assertEqual(code, 1)
        self.assertIn("figure without an M or I citation: 300 hours", out)

    def test_plan_id_alone_is_not_enough_for_a_measured_figure(self):
        report = GOOD.replace("38 of 52 handlers (M7)", "38 of 52 handlers (G09)")
        code, out, _ = self.check(report)
        self.assertEqual(code, 1)
        self.assertIn("opens with Estimate, Target or Threshold", out)

    def test_unknown_record_fails(self):
        code, out, _ = self.check(GOOD.replace("(M10)", "(M42)"))
        self.assertEqual(code, 1)
        self.assertIn("cites M42, which the plan does not hold", out)

    def test_outcome_record_without_baseline_fails(self):
        plan = PLAN.replace("baseline 61% (M1, brief §4); ", "")
        path = self.root / "plan-no-baseline.md"
        path.write_text(plan, encoding="utf-8")
        code, out, _ = self.check(GOOD, plan=path)
        self.assertEqual(code, 1)
        self.assertIn("outcome: M3 has no baseline", out)

    def test_brief_with_unknown_baseline_fails(self):
        self.brief.write_text(BRIEF.replace("61% (claims system export, Q2 2026, all four queues)",
                                            "unknown; the first goal is to measure the current journey"),
                              encoding="utf-8")
        code, out, _ = self.check(GOOD, "--brief", self.brief)
        self.assertEqual(code, 1)
        self.assertIn("brief: baseline is not recorded", out)

    def test_outcome_without_any_record_fails(self):
        report = GOOD.replace("- Claims triaged within one day: 74% against a baseline of 61% (M3; baseline M1).",
                              "- Triage is faster than before, handlers tell us.")
        code, out, _ = self.check(report)
        self.assertEqual(code, 1)
        self.assertIn("outcome: cites no M record", out)

    def test_window_older_than_period_fails(self):
        code, out, _ = self.check(GOOD.replace("74% against a baseline of 61% (M3; baseline M1)",
                                               "70% against a baseline of 61% (M2; baseline M1)"))
        self.assertEqual(code, 1)
        self.assertIn("M2: window ends 2026-08-31, before the report period starts 2026-09-01", out)

    def test_baseline_record_is_exempt_from_the_window_check(self):
        code, out, _ = self.check(GOOD)
        self.assertNotIn("M1: window", out)

    def test_assumption_presented_as_measured_fails(self):
        report = GOOD.replace("- Escalations to a senior handler fell to 212 (M10).",
                              "- Full rollout reaches 160 handlers (M8).")
        code, out, _ = self.check(report)
        self.assertEqual(code, 1)
        self.assertIn("rests on an assumption (M8) but reads as measured", out)

    def test_one_stated_assumption_in_the_estimate_voice_passes(self):
        report = GOOD.replace("- Escalations to a senior handler fell to 212 (M10).",
                              "- Estimate: full rollout reaches 160 handlers (M8).")
        code, out, _ = self.check(report)
        self.assertEqual(code, 0, out)

    def test_stacked_assumptions_fail(self):
        report = GOOD.replace("- Escalations to a senior handler fell to 212 (M10).",
                              "- Estimate: 160 handlers (M8) at a 70% triage share (M9) triage 9,000 claims a month.")
        code, out, _ = self.check(report)
        self.assertEqual(code, 1)
        self.assertIn("stacked assumptions (2)", out)

    def test_cost_per_outcome_needs_numerator_and_denominator(self):
        report = GOOD.replace("£2,540 spend (M5) over 4,100 resolved claims (M6)", "from the bill (M5)")
        code, out, _ = self.check(report)
        self.assertEqual(code, 1)
        self.assertIn("cost per outcome must cite its numerator", out)
        report = GOOD.replace("£2,540 spend (M5) over 4,100 resolved claims (M6)", "over 4,100 resolved claims (M6)")
        code, out, _ = self.check(report)
        self.assertEqual(code, 1)
        self.assertIn("found M6", out)

    def test_unreported_incident_in_period_fails(self):
        report = GOOD.replace("- I1: 2026-09-14, severity 2, 31 replies quoted a withdrawn clause; auto-send paused; "
                              "C4 test added.", "- No incidents recorded in the period.")
        report = report.replace("fix in I1 to hold", "fix to hold")
        code, out, _ = self.check(report)
        self.assertEqual(code, 1)
        self.assertIn("incidents: I1 (2026-09-14) falls in the period but is not reported", out)
        self.assertNotIn("I0", out)

    def test_missing_call_decider_and_section_fail(self):
        report = GOOD.replace("call: continue\n", "").replace("decider: Head of Claims Operations\n", "")
        report = report.replace("## Counter-metric", "## Other figures")
        code, out, _ = self.check(report)
        self.assertEqual(code, 1)
        self.assertIn("no decider", out)
        self.assertIn("call must be one of stop, continue, scale", out)
        self.assertIn("sections: no counter-metric section", out)

    def test_adoption_without_active_definition_warns(self):
        report = GOOD.replace("Active means one accepted triage in the month: 38 of 52 handlers (M7).",
                              "38 of 52 handlers use it (M7).")
        code, out, _ = self.check(report)
        self.assertEqual(code, 0)
        self.assertIn("WARNING adoption: state the definition of an active user", out)

    def test_wrapped_bullet_is_one_logical_line(self):
        report = GOOD.replace("- Escalations to a senior handler fell to 212 (M10).",
                              "- Escalations to a senior handler fell to 212\n  this month (M10), the lowest yet.")
        code, out, _ = self.check(report)
        self.assertEqual(code, 0, out)

    def test_counter_metric_without_baseline_is_an_error_unless_the_line_says_so(self):
        plan = PLAN.replace("baseline 3.0% (brief §4); ", "")
        path = self.root / "plan-no-counter-baseline.md"
        path.write_text(plan, encoding="utf-8")
        code, out, _ = self.check(GOOD, plan=path)
        self.assertEqual(code, 1)
        self.assertIn("counter-metric: M4 has no baseline", out)
        stated = GOOD.replace("- Reopened claims: 3.1% against 3.0% (M4), within the margin on this sample.",
                              "- Reopened claims: 3.1% (M4); no baseline yet, G11 measures one.")
        code, out, _ = self.check(stated, plan=path)
        self.assertEqual(code, 0, out)
        self.assertIn("WARNING counter-metric: M4 has no baseline, as the report says", out)

    def test_last_period_figure_may_be_cited_as_context(self):
        report = GOOD.replace("(M3; baseline M1).", "(M3; baseline M1); last period 70% (M2).")
        code, out, _ = self.check(report)
        self.assertEqual(code, 0, out)

    def test_scale_with_an_open_severity_two_incident_fails(self):
        code, out, _ = self.check(GOOD.replace("call: continue", "call: scale"))
        self.assertEqual(code, 1)
        self.assertIn("call: scale with I1 (severity 2) without a status", out)
        plan = PLAN.replace("fix C4 test", "fix C4 test; status closed 2026-09-20")
        path = self.root / "plan-closed.md"
        path.write_text(plan, encoding="utf-8")
        code, out, _ = self.check(GOOD.replace("call: continue", "call: scale"), plan=path)
        self.assertEqual(code, 0, out)

    def test_no_front_matter_exits_2(self):
        code, _, err = self.check("# Report\n")
        self.assertEqual(code, 2)
        self.assertIn("front matter", err)


if __name__ == "__main__":
    unittest.main()
