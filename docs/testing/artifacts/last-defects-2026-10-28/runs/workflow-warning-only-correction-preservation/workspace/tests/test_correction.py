import json
from pathlib import Path
import shutil
import tempfile
import unittest

from pipeline.checkpoints import CheckpointStore
from pipeline.correction import correct_warnings, repair_review
from pipeline.model import ChatModel
from pipeline.sources import case_spans, load_case, load_policies
from pipeline.stages import StageFailed
from tests.doubles import ScriptedTransport

ROOT = Path(__file__).resolve().parents[1]
REPLIES = json.loads((ROOT / "tests/fixtures/PA-2026-0165/replies.json").read_text())
R1, R2 = "PA-2026-0165-r1", "PA-2026-0165-r2"


class CorrectionTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        shutil.copytree(ROOT / "runs" / R1, Path(self._tmp.name) / R1)
        self.store = CheckpointStore(self._tmp.name)
        self.spans = case_spans(load_case(ROOT / "cases/dev/PA-2026-0165"), load_policies())

    def tearDown(self):
        self._tmp.cleanup()

    def _correct(self, reply):
        transport = ScriptedTransport([(200, reply)])
        writer = ChatModel("https://gw.test/v1", "m", transport=transport)
        corrected = correct_warnings(R1, R2, self.store, writer, self.spans)
        self.assertEqual(transport.sends, 1)
        return corrected

    def _snapshot(self):
        return {p.name: p.read_bytes() for p in (Path(self._tmp.name) / R1).iterdir()}

    def test_corrected_draft_has_no_warnings_and_original_run_is_untouched(self):
        before = self._snapshot()
        self._correct(REPLIES["writer_correction"][2])
        self.assertEqual(self.store.load(R2, "writer")["meta"]["warnings"], [])
        self.assertEqual(self._snapshot(), before)

    def test_only_the_warned_quote_changes(self):
        old = self.store.load(R1, "writer")["payload"]
        new = self._correct(REPLIES["writer_correction"][2])
        for key in ("decision", "reasons", "conditions", "conflicts", "gaps"):
            self.assertEqual(old[key], new[key])
        changed = [(o["span_id"]) for o, n in zip(old["citations"], new["citations"]) if o != n]
        self.assertEqual(changed, ["DAS@1:p1:1"])

    def test_correction_that_drops_a_citation_or_gap_is_rejected(self):
        with self.assertRaises(StageFailed):
            self._correct(REPLIES["writer_correction"][0])
        self.assertIsNone(self.store.load(R2, "writer"))

    def test_correction_that_changes_the_decision_is_rejected(self):
        with self.assertRaises(StageFailed):
            self._correct(REPLIES["writer_correction"][1])
        self.assertIsNone(self.store.load(R2, "writer"))

    def test_review_is_carried_with_verdict_and_findings_intact(self):
        original = self.store.load(R1, "review")
        self._correct(REPLIES["writer_correction"][2])
        review = repair_review(R1, R2, self.store, self.spans)
        self.assertEqual(review, original["payload"])
        self.assertEqual(review["verdict"], "reject")
        saved = self.store.load(R2, "review")
        self.assertEqual(saved["payload"], original["payload"])
        self.assertEqual(saved["meta"]["frame_sha256"], original["meta"]["frame_sha256"])
        self.assertEqual(saved["meta"]["images"], original["meta"]["images"])
        self.assertEqual(saved["meta"]["resolved_findings"], [original["payload"]["findings"][0]])
        self.assertEqual(saved["meta"]["needs_fresh_review_of"], "r2")
        self.assertEqual(self.store.load(R1, "review"), original)


if __name__ == "__main__":
    unittest.main()
