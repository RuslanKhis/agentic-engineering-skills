"""Qualification route offline: run_qualification (what pipeline/adk_qualification.py calls) with a scripted provider."""
import copy
from pathlib import Path
import tempfile
import unittest

from pipeline.checkpoints import CheckpointStore
from pipeline.labels import occurrence_label
from pipeline.model import ChatModel
from pipeline.qualification import MAX_PACK_CHARS, PackTooLarge, load_pack, render_pack, run_qualification
from tests.doubles import ScriptedTransport
from tests.test_correction_probe import CORRECTED, PACK


class QualificationRouteTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.store = CheckpointStore(Path(self._tmp.name) / "runs")
        self.pack = load_pack(PACK)

    def tearDown(self):
        self._tmp.cleanup()

    def route(self, reply, pack=None):
        """Run the route once against a scripted provider; returns (transport, result or raises)."""
        self.transport = ScriptedTransport([reply])
        model = ChatModel("https://gw.test/v1", "m", transport=self.transport)
        return run_qualification(pack or self.pack, model, self.store, "t")

    def test_every_selected_passage_with_text_reaches_the_prompt_untruncated(self):
        rendered = render_pack(self.pack)
        for p in self.pack["passages"]:
            if p["id"] in self.pack["selected_pack"] and p["text"]:
                self.assertIn(f"[{occurrence_label(p)}] {p['text']}", rendered)

    def test_sent_request_asks_for_labels(self):
        self.route(CORRECTED)
        sent = self.transport.sent[0]["payload"]
        self.assertIn('"labels"', sent["messages"][0]["content"])
        item = sent["response_format"]["json_schema"]["schema"]["properties"]["findings"]["items"]
        self.assertIn("labels", item["required"])

    def test_corrected_result_is_accepted_and_saved(self):
        self.assertEqual(self.route(CORRECTED), CORRECTED)
        self.assertEqual(self.transport.sends, 1)
        self.assertEqual(self.store.load("t", "qualification")["meta"]["errors"], [])

    def test_unlabelled_result_is_rejected_and_the_failure_is_kept(self):
        bare = {"findings": [{"statement": "Prior notice applies.", "support": "supported"}]}
        with self.assertRaises(ValueError):
            self.route(bare)
        self.assertTrue(self.store.load("t", "qualification")["meta"]["errors"])

    def test_strict_check_applies_on_the_route(self):
        # Cites the clause head but drops the footnote it requires: only strict mode rejects this.
        weak = copy.deepcopy(CORRECTED)
        weak["findings"][0]["qualifications"] = []
        with self.assertRaisesRegex(ValueError, "omits qualifications"):
            self.route(weak)

    def test_oversize_pack_is_refused_not_cut_and_nothing_is_sent(self):
        pack = copy.deepcopy(self.pack)
        pack["passages"][0]["text"] += "x" * MAX_PACK_CHARS
        with self.assertRaises(PackTooLarge):
            self.route(CORRECTED, pack)
        self.assertEqual(self.transport.sends, 0)

    def test_pack_missing_a_required_footnote_is_refused_before_any_send(self):
        pack = copy.deepcopy(self.pack)
        pack["selected_pack"].remove("d7-fn3")
        with self.assertRaises(ValueError):
            self.route(CORRECTED, pack)
        self.assertEqual(self.transport.sends, 0)


if __name__ == "__main__":
    unittest.main()
