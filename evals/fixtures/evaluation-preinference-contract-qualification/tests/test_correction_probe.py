"""Correction probe: a hand-corrected qualification result passes the contract check."""
from pathlib import Path
import unittest

from pipeline.contract import check_findings
from pipeline.qualification import load_pack

PACK = Path(__file__).resolve().parents[1] / "cases" / "qualification" / "basement-pack.json"

CORRECTED = {"findings": [
    {"statement": "A basement under the dwelling's own footprint may use the prior-notice route only if the "
                  "excavation stays at least 1.0 m from the party wall; otherwise a structural method "
                  "statement is required before work starts.",
     "support": "supported",
     "labels": ["D7-2024/p12/4.3(b)(ii)", "D7-2024/p13/continuation"],
     "qualifications": ["D7-2024/p13/footnote"]},
    {"statement": "The party-wall distance applies on both routes.", "support": "supported",
     "labels": ["D7-2024/p13/footnote"]},
    {"statement": "Table D7.1 lists the route by ground type.", "support": "supported",
     "labels": ["D7-2024/p14/table-header", "D7-2024/p14/table-D7.1/c2"],
     "qualifications": ["D7-2024/p13/footnote"]},
]}


class CorrectionProbeTests(unittest.TestCase):
    def test_corrected_result_passes_the_strict_contract(self):
        self.assertEqual(check_findings(CORRECTED, load_pack(PACK), strict=True), [])

    def test_result_without_labels_fails(self):
        bare = {"findings": [{"statement": "Prior notice applies.", "support": "supported"}]}
        self.assertTrue(check_findings(bare, load_pack(PACK), strict=True))


if __name__ == "__main__":
    unittest.main()
