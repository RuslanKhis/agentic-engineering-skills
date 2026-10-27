import importlib.util
import unittest


@unittest.skipUnless(importlib.util.find_spec("pydantic"), "pydantic not installed")
class SchemaTests(unittest.TestCase):
    def test_minimal_record_validates(self):
        from extractor.schema import ClaimExtraction

        record = ClaimExtraction.model_validate(
            {"claim_reference": "CLM-2026-04411", "claim_type": "glass", "urgency": "routine"})
        self.assertIsNone(record.vehicle)

    def test_unknown_claim_type_is_rejected(self):
        from pydantic import ValidationError

        from extractor.schema import ClaimExtraction

        with self.assertRaises(ValidationError):
            ClaimExtraction.model_validate({"claim_reference": "x", "claim_type": "flood", "urgency": "routine"})


if __name__ == "__main__":
    unittest.main()
