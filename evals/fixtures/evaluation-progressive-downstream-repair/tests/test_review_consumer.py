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


if __name__ == "__main__":
    unittest.main()
