import json
from pathlib import Path
import shutil
import tempfile
import unittest

from pipeline.checkpoints import CheckpointStore, StoreLimitExceeded
from pipeline.config import Settings
from pipeline.ledger import AllowanceExceeded, CampaignLedger
from pipeline.model import ChatModel
from pipeline.schemas import CONDITION_TEMPLATES, missing_continuations, validate_draft
from pipeline.sources import case_spans, load_case, load_policies
from pipeline.stages import export
from pipeline.workflow import run_case
from tests.doubles import RejectingTransport, ScriptedTransport, enum_values_with_line_break

ROOT = Path(__file__).resolve().parents[1]
CASE = ROOT / "cases" / "dev" / "PA-2026-0141"

DRAFT = {
    "decision": "approve",
    "reasons": [{"id": "R1", "text": "The 3.6 m projection is within the 4.0 m limit for terraces.",
                 "citations": ["DAS@1:p1:1", "LP-H4@2024:p31:4", "LP-H4@2024:p31:5", "LP-H4@2024:p31:6"]}],
    "conditions": [],
    "citations": [{"span_id": "DAS@1:p1:1", "quote": "The extension projects 3.6 m beyond the original rear wall."}],
    "conflicts": [],
    "gaps": [],
}
REVIEW = {"verdict": "accept", "claims": [{"reason_id": "R1", "support": "supported",
                                           "span_ids": ["DAS@1:p1:1", "LP-H4@2024:p31:4", "LP-H4@2024:p31:5",
                                                        "LP-H4@2024:p31:6"]}], "findings": []}


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

    def test_serialized_requests_pass_the_controlled_rejecting_transport(self):
        # Batch 3: four of six writer calls got a 400 for a line-break enum value in draft-v6.
        transport = RejectingTransport([DRAFT, REVIEW])
        writer = ChatModel("https://gw.test/v1", "m", transport=transport)
        reviewer = ChatModel("https://gw.test/v1", "m", transport=transport)
        run_case(CASE, Settings(), writer, reviewer, CheckpointStore(self.tmp / "runs"),
                 CampaignLedger(self.tmp / "ledger.json"), run_id="t4")
        for sent in transport.sent:
            self.assertEqual(enum_values_with_line_break(sent["payload"]["response_format"]), [])
        self.assertEqual(transport.sends, 2)

    def test_rejecting_transport_still_rejects_the_draft_v6_shape(self):
        # Negative control: the double must fail the request that failed in batch 3.
        v6 = {"type": "object", "properties": {"template": {"type": "string",
              "enum": ["The development shall be carried out.\nReason: for the avoidance of doubt."]}}}
        transport = RejectingTransport([])
        status, _ = transport("https://gw.test/v1/chat/completions",
                              {"response_format": {"json_schema": {"schema": v6}}}, {}, 1)
        self.assertEqual(status, 400)

    def test_citing_one_line_of_a_wrapped_sentence_is_invalid(self):
        # Batch 2, PA-2026-0146: LP-H4@2024:p31:7 cited without :8 ("... non-opening below 1.7 m.").
        spans = case_spans(load_case(CASE), load_policies())
        ids = {s.span_id for s in spans}
        bad = json.loads(json.dumps(DRAFT))
        bad["reasons"][0]["citations"] = ["LP-H4@2024:p31:7"]
        self.assertIn("reason R1 cites a sentence that continues in LP-H4@2024:p31:8",
                      validate_draft(bad, ids, spans))
        bad["reasons"][0]["citations"] = ["LP-H4@2024:p31:7", "LP-H4@2024:p31:8"]
        self.assertEqual(validate_draft(bad, ids, spans), [])

    def test_the_4m_limit_needs_its_unless_clause_cited(self):
        spans = case_spans(load_case(CASE), load_policies())
        self.assertEqual(missing_continuations(["LP-H4@2024:p31:4"], spans),
                         ["LP-H4@2024:p31:5", "LP-H4@2024:p31:6"])

    def test_condition_must_use_a_known_template_id(self):
        spans = case_spans(load_case(CASE), load_policies())
        bad = json.loads(json.dumps(DRAFT))
        bad["conditions"] = [{"id": "C1", "template_id": "COND-NOPE", "reason_id": "R1"}]
        self.assertTrue(validate_draft(bad, {s.span_id for s in spans}, spans))

    def test_export_renders_condition_text_from_the_template_id(self):
        # Latent blocker behind batch 3: export read c["text"], which no draft shape provides.
        draft = json.loads(json.dumps(DRAFT))
        draft["decision"] = "approve_with_conditions"
        draft["conditions"] = [{"id": "C1", "template_id": "COND-PLANS", "reason_id": "R1"}]
        result = export(load_case(CASE), draft, REVIEW)
        self.assertEqual(result["conditions"], [CONDITION_TEMPLATES["COND-PLANS"]])

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
