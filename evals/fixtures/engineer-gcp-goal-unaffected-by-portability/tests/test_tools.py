import unittest
from types import SimpleNamespace

from claims import tools


class ClaimToolTests(unittest.TestCase):
    def setUp(self):
        tools.use_repository(tools.DictClaims({
            "CL-20931": {"policyholder_id": "ph-1", "stage": "assessment", "next_step": "loss adjuster visit"},
            "CL-20977": {"policyholder_id": "ph-2", "stage": "settled", "next_step": "none"},
        }))

    def test_own_claim(self):
        self.assertEqual(tools.claim_status("CL-20931", SimpleNamespace(user_id="ph-1"))["stage"], "assessment")

    def test_other_policyholders_claim_is_not_found(self):
        self.assertEqual(tools.claim_status("CL-20977", SimpleNamespace(user_id="ph-1"))["status"], "not_found")

    def test_note_is_added(self):
        self.assertEqual(tools.add_claim_note("CL-20931", "Quote attached", SimpleNamespace(user_id="ph-1"))["status"],
                         "noted")


if __name__ == "__main__":
    unittest.main()
