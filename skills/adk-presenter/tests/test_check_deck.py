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

- 38% leave at product choice (last quarter, 2,140 advertisers)
- 12% leave at creative upload

Notes: Open with the funnel. Product choice loses 38% of eligible advertisers; creative upload loses 12%.

---

## A guided brief should recover a share of those advertisers without raising refunds
Covers: hypothesis
Evidence: hypothesis; docs/discovery/ads.md §4

Less effort to choose → more completed purchases → more repeat campaigns.
We expect a 5 to 8 percent lift; the proof of concept measures it.

Notes: This is the hypothesis chain, not a result.

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

    def test_tables_are_visuals_and_decimals_are_one_word(self):
        table = GOOD.replace("Less effort to choose → more completed purchases → more repeat campaigns.",
                             "\n".join("| criterion %d | threshold | measured | method | sample |" % i for i in range(12)))
        self.assertFalse(any("word budget" in m for m in json.loads(run(table, "--json").stdout)["warnings"]))
        title = GOOD.replace("## Small advertisers abandon the purchase at product choice more than at any other step",
                             "## Median handling time fell from 4.4 minutes to 1.7 minutes on 331 orders, 9 to 22 November 2026, measured")
        report = json.loads(run(title, "--json").stdout)
        self.assertFalse(any("title runs over" in m and "slide 2" in m for m in report["warnings"]))

    def test_technical_budgets_are_wider(self):
        long_title = ("## Scope: one display product family, existing assets, a human before every purchase, "
                      "no agencies, no video, no bespoke sponsorships, no autonomous spend changes at all")
        business = GOOD.replace("## Scope: one display product family, existing assets, a human before every purchase", long_title)
        self.assertTrue(any("title runs over 20 words" in m for m in json.loads(run(business, "--json").stdout)["warnings"]))
        technical = business.replace("audience: business", "audience: technical")
        self.assertFalse(any("title runs over" in m for m in json.loads(run(technical, "--json").stdout)["warnings"]))
        body = GOOD.replace("Less effort to choose → more completed purchases → more repeat campaigns.", "word " * 60)
        self.assertTrue(any("40-word budget" in m for m in json.loads(run(body, "--json").stdout)["warnings"]))
        self.assertFalse(any("word budget" in m for m in json.loads(run(body.replace("audience: business", "audience: technical"), "--json").stdout)["warnings"]))

    def test_word_budgets_warn(self):
        long_title = GOOD.replace("## Scope: one display product family, existing assets, a human before every purchase",
                                  "## Scope: one display product family, existing assets, a human before every purchase, "
                                  "no agencies, no video, no bespoke sponsorships, no autonomous spend changes at all")
        report = json.loads(run(long_title, "--json").stdout)
        self.assertTrue(any("title runs over 20 words" in message for message in report["warnings"]))
        long_body = GOOD.replace("Less effort to choose → more completed purchases → more repeat campaigns.",
                                 "word " * 45).replace("Notes: This is the hypothesis chain, not a result.",
                                                       "Notes: the notes do not count " + "word " * 100)
        report = json.loads(run(long_body, "--json").stdout)
        self.assertTrue(any("over the 40-word budget" in message for message in report["warnings"]))
        self.assertFalse(any("over the 40-word budget" in message for message in json.loads(run(GOOD, "--json").stdout)["warnings"]))
        ask_body = GOOD.replace("Notes: Ask for the decision in one sentence and stop talking.",
                                "word " * 60 + "\n\nNotes: Ask for the decision in one sentence and stop talking.")
        self.assertFalse(any("word budget" in message for message in json.loads(run(ask_body, "--json").stdout)["warnings"]))
        appendix = GOOD + "\n---\n\n## Appendix: answers to the questions this room will ask\nCovers: questions\nEvidence: docs/plans/ads.md\n\n" + "word " * 80 + "\nNotes: Only if asked.\n"
        self.assertFalse(any("word budget" in message for message in json.loads(run(appendix, "--json").stdout)["warnings"]))

    def test_hype_words_warn(self):
        text = GOOD.replace("Notes: Everything else waits.", "Notes: This revolutionary agent understands every brief and eliminates rework.")
        report = json.loads(run(text, "--json").stdout)
        self.assertTrue(any("hype words" in message and "revolutionary" in message and "eliminates" in message
                            for message in report["warnings"]))
        self.assertEqual(run(GOOD).returncode, 0)

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

    def test_measurement_ids_cite_and_code_spans_are_not_hype(self):
        text = GOOD.replace("Evidence: D2, D5", "Evidence: M3, I1").replace(
            "Notes: Everything else waits.", "Notes: the `arm` field holds `always treatment`; everything else waits.")
        report = json.loads(run(text, "--json").stdout)
        self.assertEqual(report["slides"][4]["evidence"], "cited")
        self.assertFalse(any("hype" in m for m in report["warnings"]))

    def test_prose_mode_lints_wording_only(self):
        with tempfile.TemporaryDirectory() as directory:
            prose = Path(directory) / "case-study.md"
            prose.write_text("# Acme cuts handling time\n\nBuilt with Google Gemini on Google Cloud.\n", encoding="utf-8")
            clean = subprocess.run([sys.executable, "-I", "-B", str(SCRIPT), "--prose", str(prose)], capture_output=True, text=True)
            self.assertEqual(clean.returncode, 0, clean.stdout)
            prose.write_text("Our GCP stack, powered by Google.\n", encoding="utf-8")
            bad = subprocess.run([sys.executable, "-I", "-B", str(SCRIPT), "--prose", str(prose)], capture_output=True, text=True)
            self.assertEqual(bad.returncode, 1)
            self.assertIn("GCP", bad.stdout)
            both = subprocess.run([sys.executable, "-I", "-B", str(SCRIPT), "--prose", str(prose), "--deck", str(prose)], capture_output=True, text=True)
            self.assertEqual(both.returncode, 2)

    def test_identifiers_are_not_numeric_claims(self):
        text = GOOD.replace("Evidence: D2, D5\nNotes: Everything else waits.",
                            "Evidence: n/a: scope statement\nNotes: Everything else waits. See G03/A2 and C12.")
        result = run(text)
        self.assertEqual(result.returncode, 0, result.stdout)


if __name__ == "__main__":
    unittest.main()
