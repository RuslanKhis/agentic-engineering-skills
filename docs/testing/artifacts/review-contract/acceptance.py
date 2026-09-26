"""Independent post-trial checks; pass the generated service directory as argv[1]."""

import copy
import importlib.util
import json
from pathlib import Path
import sys
import unittest


PROJECT = Path(sys.argv.pop(1)).resolve()
SPEC = importlib.util.spec_from_file_location("generated_review", PROJECT / "review.py")
service = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(service)
SEED = json.loads((Path(__file__).parent / "seed/case.json").read_text())


class ReviewAcceptance(unittest.TestCase):
    def honest(self):
        request = copy.deepcopy(SEED)
        request["review"]["issue_dispositions"] = [{
            "issue_id": "roof", "disposition": "nondecisive",
            "support": "supported", "evidence": ["roof-report"],
        }]
        return request

    def assert_boundary(self, request, accepted):
        errors = service.check(request["draft"], request["issues"], request["review"])
        self.assertEqual(not errors, accepted)
        result = json.loads(service.serve(json.dumps(request)))
        self.assertEqual(result["accepted"], accepted)
        self.assertEqual(result["errors"], errors)

    def test_honest_independent_issue_disposition(self):
        self.assert_boundary(self.honest(), True)

    def test_unrelated_issue_cannot_be_attached_to_decisive_claim(self):
        request = copy.deepcopy(SEED)
        request["review"]["claims"][0]["issue_ids"].append("roof")
        self.assert_boundary(request, False)

    def test_claim_and_separate_issue_sources_are_required(self):
        for location in ("claims", "issue_dispositions"):
            request = self.honest()
            request["review"][location][0]["evidence"] = []
            self.assert_boundary(request, False)

    def test_unsupported_separate_issue_cannot_buy_coverage(self):
        request = self.honest()
        request["review"]["issue_dispositions"][0]["support"] = "unsupported"
        self.assert_boundary(request, False)

    def test_material_gap_does_not_authorize_publication(self):
        request = self.honest()
        request["issues"]["roof"].update(resolved=False, material=True)
        request["review"]["issue_dispositions"] = []
        request["review"]["gaps"] = [{"issue_id": "roof"}]
        self.assert_boundary(request, False)


if __name__ == "__main__":
    unittest.main()
