import json
from pathlib import Path
import unittest

from pipeline.review_consumer import ReviewRejected, accept_review

DRAFT = {"reasons": [{"id": "R1", "text": "Within the 4.0 m limit.", "citations": ["DAS@1:p1:1"]}],
         "citations": [{"span_id": "DAS@1:p1:1", "quote": "The extension projects 3.6 m"}]}


class ReviewConsumerTests(unittest.TestCase):
    def test_accepted_review_passes(self):
        accept_review({"verdict": "accept", "findings": [],
                       "claims": [{"reason_id": "R1", "support": "supported", "span_ids": ["DAS@1:p1:1"]}]}, DRAFT)

    def test_rejected_review_is_refused(self):
        with self.assertRaises(ReviewRejected):
            accept_review({"verdict": "reject", "claims": [], "findings": ["R1 unsupported"]}, DRAFT)

    def test_unsupported_claim_is_refused(self):
        with self.assertRaises(ReviewRejected):
            accept_review({"verdict": "accept", "findings": [],
                           "claims": [{"reason_id": "R1", "support": "unsupported", "span_ids": []}]}, DRAFT)

    def test_span_cited_by_another_reason_is_refused(self):
        draft = {"reasons": [{"id": "R1", "text": "a", "citations": ["A@1:p1:1"]},
                             {"id": "R2", "text": "b", "citations": ["B@1:p1:1"]}],
                 "citations": [{"span_id": "A@1:p1:1", "quote": "q"}, {"span_id": "B@1:p1:1", "quote": "q"}]}
        review = {"verdict": "accept", "findings": [],
                  "claims": [{"reason_id": "R1", "support": "supported", "span_ids": ["B@1:p1:1"]},
                             {"reason_id": "R2", "support": "supported", "span_ids": ["B@1:p1:1"]}]}
        with self.assertRaises(ReviewRejected):
            accept_review(review, draft)

    def test_span_outside_every_reason_is_refused_even_if_quoted(self):
        draft = {"reasons": [{"id": "R1", "text": "a", "citations": ["A@1:p1:1"]}],
                 "citations": [{"span_id": "A@1:p1:1", "quote": "q"}, {"span_id": "C@1:p1:1", "quote": "q"}]}
        review = {"verdict": "accept", "findings": [],
                  "claims": [{"reason_id": "R1", "support": "supported", "span_ids": ["C@1:p1:1"]}]}
        with self.assertRaises(ReviewRejected):
            accept_review(review, draft)


class SavedRunReproducerTests(unittest.TestCase):
    """Reads the saved PA-2026-0158-r1 checkpoints (read-only); no provider, no writes."""

    def test_saved_review_is_consumable_against_saved_draft(self):
        base = Path(__file__).resolve().parents[1] / "runs" / "PA-2026-0158-r1"
        draft = json.loads((base / "writer.json").read_text(encoding="utf-8"))["payload"]
        review = json.loads((base / "review.json").read_text(encoding="utf-8"))["payload"]
        accept_review(review, draft)


if __name__ == "__main__":
    unittest.main()
