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
OLD, NEW = "PA-2026-0165-r1", "PA-2026-0165-r2"
REPLIES = json.loads((ROOT / "tests/fixtures/PA-2026-0165/replies.json").read_text())


class CorrectionTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        shutil.copytree(ROOT / "runs" / "PA-2026-0165-r1", Path(self._tmp.name) / "PA-2026-0165-r1")
        self.store = CheckpointStore(self._tmp.name)
        self.spans = case_spans(load_case(ROOT / "cases/dev/PA-2026-0165"), load_policies())

    def tearDown(self):
        self._tmp.cleanup()

    def _correct(self, index):
        transport = ScriptedTransport([(200, REPLIES["writer_correction"][index])])
        writer = ChatModel("https://gw.test/v1", "m", transport=transport)
        return transport, lambda: correct_warnings(OLD, NEW, self.store, writer, self.spans)

    def test_corrected_draft_has_no_warnings_in_a_new_run(self):
        transport, run = self._correct(2)
        run()
        self.assertEqual(self.store.load(NEW, "writer")["meta"]["warnings"], [])
        self.assertEqual(transport.sends, 1)

    def test_original_run_is_untouched(self):
        before = {p.name: p.read_bytes() for p in (Path(self._tmp.name) / OLD).iterdir()}
        _, run = self._correct(2)
        run()
        repair_review(OLD, NEW, self.store)
        after = {p.name: p.read_bytes() for p in (Path(self._tmp.name) / OLD).iterdir()}
        self.assertEqual(before, after)

    def test_correction_keeps_decision_conditions_and_citations(self):
        old = self.store.load(OLD, "writer")["payload"]
        _, run = self._correct(2)
        new = run()
        for key in ("decision", "reasons", "conditions", "conflicts", "gaps"):
            self.assertEqual(new[key], old[key])
        self.assertEqual({c["span_id"] for c in new["citations"]}, {c["span_id"] for c in old["citations"]})

    def test_corrections_that_change_the_decision_are_refused(self):
        for index in (0, 1):
            _, run = self._correct(index)
            with self.assertRaises(StageFailed):
                run()
            self.assertIsNone(self.store.load(NEW, "writer"))

    def test_same_run_directory_is_refused(self):
        writer = ChatModel("https://gw.test/v1", "m", transport=ScriptedTransport([]))
        with self.assertRaises(ValueError):
            correct_warnings(OLD, OLD, self.store, writer, self.spans)

    def test_review_repair_drops_only_the_quotation_finding(self):
        old = self.store.load(OLD, "review")
        review = repair_review(OLD, NEW, self.store)
        self.assertEqual(review["findings"], old["payload"]["findings"][1:])
        self.assertEqual(review["verdict"], "reject")
        self.assertEqual(review["claims"], old["payload"]["claims"])
        meta = self.store.load(NEW, "review")["meta"]
        self.assertEqual(meta["findings_dropped"], old["payload"]["findings"][:1])
        self.assertFalse(meta["reviewer_rerun"])
        self.assertEqual(meta["usage"], old["meta"]["usage"])


if __name__ == "__main__":
    unittest.main()
