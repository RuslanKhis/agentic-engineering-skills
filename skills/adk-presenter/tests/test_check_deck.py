"""Exercise the deck checker through its public CLI with hand-written decks."""

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "check_deck.py"

GOOD = """---
stage: poc-approval
audience: business
minutes: 15
title: Guided campaign briefs for small advertisers
sources: docs/discovery/ads.md, docs/architecture/ads.md, docs/plans/ads.md
decider: Director of SMB Sales
date: 2026-10-30
---

## Guided campaign briefs: a four-week proof of concept
Covers: title

---

## Small advertisers abandon the purchase at product choice more than at any other step
Covers: problem
Evidence: docs/discovery/ads.md funnel table; measured
Notes: Open with the funnel. Product choice loses 38% of eligible advertisers; creative upload loses 12%.

- 38% leave at product choice (last quarter, 2,140 advertisers)
- 12% leave at creative upload

---

## A guided brief should recover a share of those advertisers without raising refunds
Covers: hypothesis
Evidence: hypothesis; docs/discovery/ads.md §4
Notes: This is the hypothesis chain, not a result.

Less effort to choose → more completed purchases → more repeat campaigns.
We expect a 5 to 8 percent lift; the proof of concept measures it.

---

## We will call it a success at a measured lift on checkout completion with refunds flat
Covers: success-criteria
Evidence: C1, C4; docs/plans/ads.md summary
Notes: Agree the criteria now so the review is a comparison, not a debate.

---

## Scope: one display product family, existing assets, a human before every purchase
Covers: scope
Evidence: D2, D5
Notes: Everything else waits.

---

## The proof of concept costs about 60 human hours and under $200 of model and cloud spend
Covers: cost
Evidence: docs/plans/ads.md schedule check, run 14 October 2026
Notes: Hours are from the schedule check, not a guess.

---

## Three risks, each with a control already in the design
Covers: risks
Evidence: D3, D7, C6
Notes: Wrong product recommended, licence breach, runaway spend.

---

## The decision: approve four weeks and one developer, review on 14 November
Covers: ask
Evidence: docs/plans/ads.md summary
Notes: Ask for the decision in one sentence and stop talking.
"""


def run(text, *args):
    with tempfile.TemporaryDirectory() as directory:
        deck = Path(directory) / "deck.md"
        deck.write_text(text, encoding="utf-8")
        return subprocess.run([sys.executable, "-I", "-B", str(SCRIPT), "--deck", str(deck), *args],
                              capture_output=True, text=True)


class DeckTests(unittest.TestCase):
    def test_good_deck_passes(self):
        result = run(GOOD, "--json")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report["errors"], [])
        self.assertEqual(len(report["slides"]), 8)
        self.assertEqual(report["slides"][1]["evidence"], "cited")
        self.assertIn("38%", report["slides"][1]["numbers"])
        self.assertEqual(report["slides"][2]["evidence"], "cited")
        self.assertIn("problem", report["covered"])

    def test_numbers_without_evidence_fail(self):
        text = GOOD.replace("Evidence: docs/discovery/ads.md funnel table; measured", "Evidence: n/a: context only")
        result = run(text)
        self.assertEqual(result.returncode, 1)
        self.assertIn("numbers without evidence: 38%", result.stdout)

    def test_missing_evidence_line_fails(self):
        text = GOOD.replace("Evidence: D2, D5\n", "")
        result = run(text)
        self.assertEqual(result.returncode, 1)
        self.assertIn("slide 5", result.stdout)
        self.assertIn("no Evidence line", result.stdout)

    def test_evidence_that_cites_nothing_fails(self):
        text = GOOD.replace("Evidence: D3, D7, C6", "Evidence: we discussed this with the team")
        result = run(text)
        self.assertEqual(result.returncode, 1)
        self.assertIn("Evidence cites nothing", result.stdout)

    def test_missing_coverage_fails_and_names_tags(self):
        text = GOOD.replace("Covers: ask\n", "")
        result = run(text)
        self.assertEqual(result.returncode, 1)
        self.assertIn("no slide Covers ask", result.stdout)

    def test_technical_audience_needs_more_coverage(self):
        text = GOOD.replace("audience: business", "audience: technical")
        result = run(text, "--json")
        self.assertEqual(result.returncode, 1)
        report = json.loads(result.stdout)
        self.assertTrue(any("architecture, contracts, evidence-plan, dependencies" in message
                            for message in report["errors"]))

    def test_hypothesis_numbers_only_warn(self):
        report = json.loads(run(GOOD, "--json").stdout)
        # The hypothesis slide cites a path as well, so it is 'cited'; make it label-only.
        text = GOOD.replace("Evidence: hypothesis; docs/discovery/ads.md §4", "Evidence: hypothesis")
        result = run(text, "--json")
        self.assertEqual(result.returncode, 0)
        report = json.loads(result.stdout)
        self.assertEqual(report["slides"][2]["evidence"], "labelled")
        self.assertTrue(any("hypothesis or assumption slide" in message for message in report["warnings"]))

    def test_label_titles_and_missing_notes_warn(self):
        text = GOOD.replace("## Scope: one display product family, existing assets, a human before every purchase",
                            "## Scope").replace("Notes: Everything else waits.\n", "")
        result = run(text, "--json")
        self.assertEqual(result.returncode, 0)
        report = json.loads(result.stdout)
        self.assertTrue(any("label, not a claim" in message for message in report["warnings"]))
        self.assertTrue(any("slide 5" in message and "no speaker Notes" in message for message in report["warnings"]))

    def test_timing_warning(self):
        text = GOOD.replace("minutes: 15", "minutes: 5")
        report = json.loads(run(text, "--json").stdout)
        self.assertTrue(any("more than one a minute" in message for message in report["warnings"]))
        text = GOOD.replace("minutes: 15", "minutes: 60")
        report = json.loads(run(text, "--json").stdout)
        self.assertTrue(any("over three minutes a slide" in message for message in report["warnings"]))

    def test_appendix_slides_are_not_timed_and_notes_length_is_estimated(self):
        appendix = "\n---\n\n## Appendix: the baseline and who measured it\nCovers: questions\nEvidence: docs/discovery/ads.md\nNotes: Only if asked.\n"
        text = GOOD.replace("minutes: 15", "minutes: 7") + appendix * 3
        report = json.loads(run(text, "--json").stdout)
        self.assertEqual(report["timed_slides"], 7)
        self.assertFalse(any("more than one a minute" in message for message in report["warnings"]))
        self.assertGreater(report["spoken_words"], 0)
        self.assertTrue(any("unscripted" in message for message in report["warnings"]))
        long_notes = GOOD.replace("Notes: Everything else waits.", "Notes: " + "word " * 2600)
        report = json.loads(run(long_notes, "--json").stdout)
        self.assertTrue(any("for a 15-minute slot" in message and "unscripted" not in message
                            for message in report["warnings"]))

    def test_missing_decider_and_date_warn(self):
        text = GOOD.replace("decider: Director of SMB Sales\n", "").replace("date: 2026-10-30\n", "")
        report = json.loads(run(text, "--json").stdout)
        self.assertTrue(any("no decider" in message for message in report["warnings"]))
        self.assertTrue(any("no date" in message for message in report["warnings"]))

    def test_counts_and_full_currency_are_numeric_claims(self):
        text = GOOD.replace("Evidence: D2, D5\nNotes: Everything else waits.",
                            "Evidence: n/a: scope\nNotes: Everything else waits.\n\n- 8 of 10 cases passed; it costs $1,500 a month")
        result = run(text)
        self.assertEqual(result.returncode, 1)
        self.assertIn("8 of 10", result.stdout)
        self.assertIn("$1,500", result.stdout)

    def test_bad_front_matter(self):
        text = GOOD.replace("stage: poc-approval", "stage: kickoff").replace("minutes: 15", "minutes: lots")
        result = run(text)
        self.assertEqual(result.returncode, 1)
        self.assertIn("stage must be one of", result.stdout)
        self.assertIn("minutes must be a positive whole number", result.stdout)
        result = run("# No front matter\n\n## A slide\n")
        self.assertEqual(result.returncode, 2)

    def test_rules_inside_code_fences_do_not_split_slides(self):
        text = GOOD.replace("Less effort to choose → more completed purchases → more repeat campaigns.",
                            "```text\nless effort\n---\nmore purchases\n```")
        report = json.loads(run(text, "--json").stdout)
        self.assertEqual(len(report["slides"]), 8)

    def test_case_study_wording_lint(self):
        deck = (GOOD.replace("stage: poc-approval", "stage: case-study")
                    .replace("audience: business", "audience: public")
                    .replace("Covers: problem", "Covers: challenge")
                    .replace("Covers: hypothesis", "Covers: solution")
                    .replace("Covers: success-criteria", "Covers: results")
                    .replace("Covers: ask", "Covers: next"))
        result = run(deck)
        self.assertEqual(result.returncode, 0, result.stdout)
        bad = deck.replace("Everything else waits.", "Everything else waits. Our GCP stack is powered by Google.")
        result = run(bad)
        self.assertEqual(result.returncode, 1)
        self.assertIn("GCP (write Google Cloud in full)", result.stdout)
        self.assertIn("powered by Google", result.stdout)
        # The same wording on an internal deck is not the public story's concern.
        internal = GOOD.replace("Everything else waits.", "Everything else waits. Our GCP stack.")
        self.assertEqual(run(internal).returncode, 0)

    def test_identifiers_are_not_numeric_claims(self):
        text = GOOD.replace("Evidence: D2, D5\nNotes: Everything else waits.",
                            "Evidence: n/a: scope statement\nNotes: Everything else waits. See G03/A2 and C12.")
        result = run(text)
        self.assertEqual(result.returncode, 0, result.stdout)


if __name__ == "__main__":
    unittest.main()
