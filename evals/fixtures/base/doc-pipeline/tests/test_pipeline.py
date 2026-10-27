import json
from pathlib import Path
import shutil
import tempfile
import unittest

from pipeline.checkpoints import CheckpointStore, StoreLimitExceeded
from pipeline.config import Settings
from pipeline.ledger import AllowanceExceeded, CampaignLedger
from pipeline.model import ChatModel
from pipeline.schemas import validate_draft
from pipeline.sources import case_spans, load_case, load_policies
from pipeline.workflow import run_case
from tests.doubles import ScriptedTransport

ROOT = Path(__file__).resolve().parents[1]
CASE = ROOT / "cases" / "dev" / "PA-2026-0141"

DRAFT = {
    "decision": "approve",
    "reasons": [{"id": "R1", "text": "The 3.6 m projection is within the 4.0 m limit for terraces.",
                 "citations": ["DAS@1:p1:1", "LP-H4@2024:p31:4"]}],
    "conditions": [],
    "citations": [{"span_id": "DAS@1:p1:1", "quote": "The extension projects 3.6 m beyond the original rear wall."}],
    "conflicts": [],
    "gaps": [],
}
REVIEW = {"verdict": "accept", "claims": [{"reason_id": "R1", "support": "supported",
                                           "span_ids": ["DAS@1:p1:1", "LP-H4@2024:p31:4"]}], "findings": []}


class PipelineTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)
        shutil.copy(ROOT / "campaign" / "ledger.json", self.tmp / "ledger.json")

    def tearDown(self):
        self._tmp.cleanup()

    def test_spans_are_numbered_by_document_version_page_and_line(self):
        spans = case_spans(load_case(CASE), load_policies())
        ids = {s.span_id for s in spans}
        self.assertIn("DAS@1:p1:1", ids)
        self.assertIn("LP-H4@2024:p31:4", ids)

    def test_draft_citing_unknown_span_is_invalid(self):
        bad = json.loads(json.dumps(DRAFT))
        bad["reasons"][0]["citations"] = ["DAS@1:p9:9"]
        self.assertTrue(validate_draft(bad, {"DAS@1:p1:1"}))

    def test_case_runs_end_to_end_with_scripted_provider(self):
        transport = ScriptedTransport([DRAFT, REVIEW])
        writer = ChatModel("https://gw.test/v1", "m", transport=transport)
        reviewer = ChatModel("https://gw.test/v1", "m", transport=transport)
        store = CheckpointStore(self.tmp / "runs")
        result = run_case(CASE, Settings(), writer, reviewer, store, CampaignLedger(self.tmp / "ledger.json"),
                          run_id="t1")
        self.assertEqual(result["decision"], "approve")
        self.assertEqual(transport.sends, 2)
        for stage in ("source", "writer", "review", "export"):
            self.assertIsNotNone(store.load("t1", stage), stage)

    def test_checkpoint_over_limit_is_refused(self):
        store = CheckpointStore(self.tmp / "runs", limit_bytes=200)
        with self.assertRaises(StoreLimitExceeded):
            store.save("t2", "writer", {"text": "x" * 500}, {})

    def test_ledger_refuses_reservation_beyond_allowance(self):
        ledger = CampaignLedger(self.tmp / "ledger.json")
        with self.assertRaises(AllowanceExceeded):
            ledger.reserve("t3", "writer", 1000.0)


if __name__ == "__main__":
    unittest.main()
