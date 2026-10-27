"""Correction probe: bind the spans the model selected instead of trusting its regenerated quote."""
from pathlib import Path
import unittest

from pipeline.citations import bind, quote_matches
from pipeline.sources import case_spans, load_case, load_policies

CASE = Path(__file__).resolve().parents[1] / "cases" / "dev" / "PA-2026-0163"


class CorrectionProbeTests(unittest.TestCase):
    def setUp(self):
        self.spans = case_spans(load_case(CASE), load_policies())

    def test_bound_text_is_the_source_text(self):
        bound = bind({"span_ids": ["DAS@2:p1:2", "DAS@2:p1:3"],
                      "explanation": "States the projection beyond No. 14's building line."}, self.spans)
        self.assertIn("rear build-\ning line of No. 14", bound["text"])
        self.assertTrue(quote_matches(bound["text"], bound["span_ids"], self.spans))

    def test_quote_rejoining_a_line_break_hyphen_matches(self):
        # PA-2026-0163-r3: the model wrote "building"; the source line ends "build-" and the next starts "ing".
        quote = "The rear extension projects 3.0 m beyond the rear building line of No. 14"
        ids = ["DAS@2:p1:2", "DAS@2:p1:3"]
        self.assertNotIn(quote, "\n".join(s.text for s in self.spans if s.span_id in ids))  # the old failure
        self.assertTrue(quote_matches(quote, ids, self.spans))

    def test_hyphen_rejoin_does_not_loosen_other_checks(self):
        ids = ["DAS@2:p1:2", "DAS@2:p1:3"]
        for quote in ("The rear extension projects 3.0 m beyond the rear building line of No. 15",
                      "The rear extension projects 4.0 m beyond the rear building line of No. 14",
                      "rear building line of No. 14 and 4.6 m beyond the original rear wall of No. 16 and more"):
            self.assertFalse(quote_matches(quote, ids, self.spans), quote)
        # only the first span: the rejoined word is not in it
        self.assertFalse(quote_matches("rear building line", ["DAS@2:p1:2"], self.spans))
        # a different document's span is never rejoined to the hyphenated line
        self.assertFalse(quote_matches("rear building line", ["DAS@2:p1:2", "DLS@1:p1:1"], self.spans))
        self.assertFalse(quote_matches("anything", [], self.spans))

    def test_unknown_span_is_refused(self):
        with self.assertRaises(KeyError):
            bind({"span_ids": ["DAS@2:p1:9"]}, self.spans)


if __name__ == "__main__":
    unittest.main()
