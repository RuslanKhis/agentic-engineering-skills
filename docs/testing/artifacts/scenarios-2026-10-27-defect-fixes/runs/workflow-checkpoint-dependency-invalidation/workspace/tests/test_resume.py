import json
from pathlib import Path
import shutil
import tempfile
import unittest

from pipeline.checkpoints import CheckpointStore
from pipeline.config import Settings
from pipeline.model import ChatModel
from pipeline.resume import resume_case
from tests.doubles import ScriptedTransport

ROOT = Path(__file__).resolve().parents[1]


class ResumeTests(unittest.TestCase):
    def test_saved_stages_are_not_paid_for_again(self):
        with tempfile.TemporaryDirectory() as tmp:
            shutil.copytree(ROOT / "runs" / "PA-2026-0141-r3", Path(tmp) / "PA-2026-0141-r3")
            (Path(tmp) / "PA-2026-0141-r3" / "export.json").unlink()
            transport = ScriptedTransport([])
            model = ChatModel("https://gw.test/v1", "m", transport=transport)
            result = resume_case(ROOT / "cases" / "dev" / "PA-2026-0141", "PA-2026-0141-r3", Settings(),
                                 model, model, CheckpointStore(tmp))
        self.assertEqual(transport.sends, 0)
        self.assertEqual(result["decision"], "approve")


def snapshot(folder: Path) -> dict:
    return {p.relative_to(folder).as_posix(): p.read_bytes() for p in folder.rglob("*") if p.is_file()}


class StaleCheckpointTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)
        shutil.copytree(ROOT / "runs", self.tmp / "runs")
        shutil.copy(ROOT / "campaign" / "ledger.json", self.tmp / "ledger.json")
        self.settings = Settings(ledger_path=str(self.tmp / "ledger.json"))
        self.store = CheckpointStore(self.tmp / "runs")

    def tearDown(self):
        self._tmp.cleanup()

    def resume(self, case: str, replies: list):
        transport = ScriptedTransport(replies)
        model = ChatModel("https://gw.test/v1", "m", transport=transport)
        run_id = f"{case}-r{3 if case.endswith('0141') else 1}"
        before = snapshot(self.tmp / "runs" / run_id)
        result = resume_case(ROOT / "cases" / "dev" / case, run_id, self.settings, model, model, self.store)
        self.assertEqual(before, snapshot(self.tmp / "runs" / run_id), "retained run was modified")
        return result, transport

    def test_complete_run_is_reused_without_writing(self):
        before = snapshot(self.tmp / "runs")
        result, transport = self.resume("PA-2026-0141", [])
        self.assertEqual(transport.sends, 0)
        self.assertEqual(result["decision"], "approve")
        self.assertEqual(before, snapshot(self.tmp / "runs"))

    def test_amended_input_reruns_source_writer_review_but_keeps_constraints(self):
        draft = {"decision": "approve_with_conditions",
                 "reasons": [{"id": "R1", "text": "4.6 m projection is acceptable.",
                              "citations": ["DAS@2:p1:1", "LP-H4@2024:p31:4"]}],
                 "conditions": [{"id": "C1", "text": "Tree protection fencing.", "reason_id": "R1"}],
                 "citations": [{"span_id": "DAS@2:p1:1",
                                "quote": "The extension projects 4.6 m beyond the original rear wall."}],
                 "conflicts": [], "gaps": []}
        review = {"verdict": "accept", "findings": [],
                  "claims": [{"reason_id": "R1", "support": "supported", "span_ids": ["DAS@2:p1:1"]}]}
        result, transport = self.resume("PA-2026-0147", [draft, review])
        self.assertEqual(transport.sends, 2)
        self.assertEqual(result["conditions"], ["Tree protection fencing."])
        target = self.tmp / "runs" / "PA-2026-0147-r1-c1"
        parent = json.loads((target / "manifest.json").read_text())
        self.assertEqual(parent["continues"], "PA-2026-0147-r1")
        self.assertEqual(parent["qualified"], ["constraints"])
        self.assertEqual(sorted(parent["invalidated"]), ["review", "source", "writer"])
        self.assertIn("reused_from", json.loads((target / "constraints.json").read_text())["meta"])
        # the hand-edited diagnostic response was never an input
        self.assertNotIn("4.6 m projection suits", json.dumps(result))

    def test_amended_draft_invalidates_only_the_review(self):
        review = {"verdict": "accept", "findings": [],
                  "claims": [{"reason_id": "R1", "support": "supported", "span_ids": ["DAS@1:p1:1"]},
                             {"reason_id": "R2", "support": "supported", "span_ids": ["DAS@1:p1:3"]}]}
        result, transport = self.resume("PA-2026-0152", [review])
        self.assertEqual(transport.sends, 1)
        self.assertEqual(result["decision"], "approve_with_conditions")
        manifest = json.loads((self.tmp / "runs" / "PA-2026-0152-r1-c1" / "manifest.json").read_text())
        self.assertEqual(manifest["qualified"], ["constraints", "source", "writer"])
        self.assertEqual(list(manifest["invalidated"]), ["review"])
        saved = self.store.load("PA-2026-0152-r1-c1", "review")
        self.assertEqual(saved["meta"]["draft_revision"], "r2")

    def test_repeat_resume_after_continuation_sends_nothing(self):
        review = {"verdict": "accept", "findings": [],
                  "claims": [{"reason_id": "R1", "support": "supported", "span_ids": ["DAS@1:p1:1"]},
                             {"reason_id": "R2", "support": "supported", "span_ids": ["DAS@1:p1:3"]}]}
        self.resume("PA-2026-0152", [review])
        result, transport = self.resume("PA-2026-0152", [])
        self.assertEqual(transport.sends, 0)
        self.assertEqual(result["decision"], "approve_with_conditions")
        self.assertFalse((self.tmp / "runs" / "PA-2026-0152-r1-c2").exists())

    def test_review_of_older_draft_is_not_published(self):
        from pipeline import resume as resume_module
        from pipeline.stages import StageFailed
        case = json.loads((ROOT / "cases" / "dev" / "PA-2026-0152" / "application.json").read_text())
        with self.assertRaises(StageFailed):
            resume_module.publish(case, "PA-2026-0152-r1", self.store)


if __name__ == "__main__":
    unittest.main()
