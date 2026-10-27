import json
from pathlib import Path
import shutil
import tempfile
import unittest

from pipeline.checkpoints import CheckpointStore
from pipeline.correction import correct_warnings, repair_review
from pipeline.model import ChatModel
from pipeline.sources import case_spans, load_case, load_policies
from tests.doubles import ScriptedTransport

ROOT = Path(__file__).resolve().parents[1]
REPLIES = json.loads((ROOT / "tests/fixtures/PA-2026-0165/replies.json").read_text())


class CorrectionTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        shutil.copytree(ROOT / "runs" / "PA-2026-0165-r1", Path(self._tmp.name) / "PA-2026-0165-r1")
        self.store = CheckpointStore(self._tmp.name)
        self.spans = case_spans(load_case(ROOT / "cases/dev/PA-2026-0165"), load_policies())

    def tearDown(self):
        self._tmp.cleanup()

    def test_corrected_draft_has_no_warnings(self):
        transport = ScriptedTransport([(200, REPLIES["writer_correction"][2])])
        writer = ChatModel("https://gw.test/v1", "m", transport=transport)
        correct_warnings("PA-2026-0165-r1", self.store, writer, self.spans)
        self.assertEqual(self.store.load("PA-2026-0165-r1", "writer")["meta"]["warnings"], [])
        self.assertEqual(transport.sends, 1)

    def test_review_repair_drops_the_quotation_finding(self):
        review = repair_review("PA-2026-0165-r1", self.store)
        self.assertFalse(any("verbatim" in f for f in review["findings"]))


if __name__ == "__main__":
    unittest.main()
