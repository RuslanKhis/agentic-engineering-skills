import json
from pathlib import Path
import shutil
import tempfile
import unittest

from pipeline.checkpoints import CheckpointStore
from pipeline.config import Settings
from pipeline.model import ChatModel
from pipeline.resume import resume_case
from pipeline.stages import StageFailed
from tests.doubles import ScriptedTransport

ROOT = Path(__file__).resolve().parents[1]

DRAFT_0147 = {
    "decision": "approve_with_conditions",
    "reasons": [{"id": "R1", "text": "The 4.6 m projection suits a semi-detached house.",
                 "citations": ["DAS@2:p1:1", "LP-H4@2024:p31:4"]}],
    "conditions": [{"id": "C1", "text": "Tree protection fencing before works start.", "reason_id": "R1"}],
    "citations": [{"span_id": "DAS@2:p1:1", "quote": "The extension projects 4.6 m beyond the original rear wall."}],
    "conflicts": [], "gaps": [],
}
REVIEW_0147 = {"verdict": "accept", "findings": [],
               "claims": [{"reason_id": "R1", "support": "supported", "span_ids": ["DAS@2:p1:1"]}]}
REVIEW_0152_R2 = {"verdict": "accept", "findings": [],
                  "claims": [{"reason_id": "R1", "support": "supported", "span_ids": ["DAS@1:p1:1"]},
                             {"reason_id": "R2", "support": "supported", "span_ids": ["DAS@1:p1:3"]}]}


def snapshot(folder: Path) -> dict:
    return {str(p.relative_to(folder)): p.read_bytes() for p in folder.rglob("*") if p.is_file()}


class ResumeTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)
        self.addCleanup(self._tmp.cleanup)

    def copy_run(self, run: str) -> Path:
        shutil.copytree(ROOT / "runs" / run, self.tmp / run)
        return self.tmp / run

    def resume(self, run: str, case: str, replies: list, drafts_dir: Path | None = None):
        transport = ScriptedTransport(replies)
        model = ChatModel("https://gw.test/v1", "m", transport=transport)
        result = resume_case(ROOT / "cases" / "dev" / case, run, Settings(), model, model, CheckpointStore(self.tmp),
                             drafts_dir=drafts_dir or self.tmp / "no-drafts")
        return result, transport

    def test_saved_stages_are_not_paid_for_again(self):
        run = self.copy_run("PA-2026-0141-r3")
        (run / "export.json").unlink()
        result, transport = self.resume("PA-2026-0141-r3", "PA-2026-0141", [])
        self.assertEqual(transport.sends, 0)
        self.assertEqual(result["decision"], "approve")

    def test_complete_run_resumes_without_sends_or_new_files(self):
        run = self.copy_run("PA-2026-0141-r3")
        before = snapshot(self.tmp)
        _, transport = self.resume("PA-2026-0141-r3", "PA-2026-0141", [])
        self.assertEqual(transport.sends, 0)
        self.assertEqual(snapshot(self.tmp), before)

    def test_changed_source_reruns_writer_and_review_but_keeps_constraints(self):
        run = self.copy_run("PA-2026-0147-r1")
        before = snapshot(run)
        result, transport = self.resume("PA-2026-0147-r1", "PA-2026-0147", [DRAFT_0147, REVIEW_0147])
        self.assertEqual(transport.sends, 2)
        self.assertEqual(snapshot(run), before)                      # the saved run is untouched
        new = self.tmp / "PA-2026-0147-r1-c1"
        self.assertTrue((new / "writer.json").exists() and (new / "review.json").exists())
        self.assertFalse((new / "constraints.json").exists())        # reused from the parent
        self.assertFalse((new / "diagnostics").exists())             # the hand-edited response is never used
        manifest = json.loads((new / "manifest.json").read_text())
        self.assertEqual(manifest["reused"]["constraints"], "PA-2026-0147-r1")
        self.assertIn("writer", manifest["invalidated"])
        self.assertEqual(result["constraints"], ["Tree Preservation Order T/2019/07", "Flood Zone 2"])
        # the second resume reconnects to the continuation: nothing is sent again
        _, again = self.resume("PA-2026-0147-r1", "PA-2026-0147", [])
        self.assertEqual(again.sends, 0)
        self.assertFalse((self.tmp / "PA-2026-0147-r1-c2").exists())

    def test_amended_draft_is_reviewed_and_the_stale_review_is_not_exported(self):
        run = self.copy_run("PA-2026-0152-r1")
        before = snapshot(run)
        result, transport = self.resume("PA-2026-0152-r1", "PA-2026-0152", [REVIEW_0152_R2], ROOT / "drafts")
        self.assertEqual(transport.sends, 1)                          # review only; writer and constraints reused
        self.assertIn("approve_with_conditions", transport.sent[0]["payload"]["messages"][0]["content"])
        self.assertEqual(result["decision"], "approve_with_conditions")
        self.assertEqual(snapshot(run), before)
        new = self.tmp / "PA-2026-0152-r1-c1"
        self.assertFalse((new / "writer.json").exists())
        meta = json.loads((new / "review.json").read_text())["meta"]
        self.assertEqual(meta["draft_revision"], "r2")
        _, again = self.resume("PA-2026-0152-r1", "PA-2026-0152", [], ROOT / "drafts")
        self.assertEqual(again.sends, 0)

    def test_amendment_is_not_overwritten_when_the_writer_must_rerun(self):
        run = self.copy_run("PA-2026-0152-r1")
        manifest = json.loads((run / "manifest.json").read_text())
        manifest["writer"]["prompt"] = "writer-v6"
        (run / "manifest.json").write_text(json.dumps(manifest))
        with self.assertRaises(StageFailed):
            _, _ = self.resume("PA-2026-0152-r1", "PA-2026-0152", [], ROOT / "drafts")
        self.assertFalse((self.tmp / "PA-2026-0152-r1-c1" / "writer.json").exists())


if __name__ == "__main__":
    unittest.main()
