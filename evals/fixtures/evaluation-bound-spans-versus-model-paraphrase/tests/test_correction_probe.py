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

    def test_unknown_span_is_refused(self):
        with self.assertRaises(KeyError):
            bind({"span_ids": ["DAS@2:p1:9"]}, self.spans)


if __name__ == "__main__":
    unittest.main()
