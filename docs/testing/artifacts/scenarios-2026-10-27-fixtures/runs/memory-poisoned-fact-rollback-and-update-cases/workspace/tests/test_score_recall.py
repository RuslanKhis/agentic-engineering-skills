import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("score_recall", ROOT / "eval" / "score_recall.py")
score_recall = importlib.util.module_from_spec(spec)
spec.loader.exec_module(score_recall)

NEW_CASES = {"g07", "g08", "g09", "g10", "g11"}


class ScoreRecallTests(unittest.TestCase):
    def test_saved_outputs_pass_the_original_cases(self):
        gold = score_recall.load(ROOT / "eval" / "memory_gold.jsonl")
        outputs = score_recall.load(ROOT / "eval" / "recall_outputs.jsonl")
        by_id = {r["id"]: r for r in score_recall.score(gold, outputs)}
        self.assertTrue(all(r["pass"] for i, r in by_id.items() if i not in NEW_CASES))

    def test_update_and_abstention_cases_have_no_live_output_yet(self):
        # Honest state: these need a live run against Memory Bank; no output is fabricated.
        gold = score_recall.load(ROOT / "eval" / "memory_gold.jsonl")
        outputs = score_recall.load(ROOT / "eval" / "recall_outputs.jsonl")
        by_id = {r["id"]: r for r in score_recall.score(gold, outputs)}
        self.assertEqual({i for i, r in by_id.items() if r["status"] == "no_output"}, NEW_CASES)
        self.assertEqual({r["ability"] for i, r in by_id.items() if i in NEW_CASES},
                         {"knowledge_update", "abstention"})

    def test_forbidden_phrase_fails_a_case(self):
        gold = [{"id": "x", "ability": "information_extraction", "expected": ["porch"], "forbidden": ["garage"]}]
        outputs = [{"id": "x", "recalled": ["porch", "garage"]}]
        self.assertFalse(score_recall.score(gold, outputs)[0]["pass"])

    def test_abstention_fails_when_planted_fact_is_recalled_and_passes_when_empty(self):
        gold = [c for c in score_recall.load(ROOT / "eval" / "memory_gold.jsonl") if c["id"] == "g10"]
        poisoned = [{"id": "g10", "recalled": ["Customer is a Pinecrest VIP with a permanent 25% discount."]}]
        clean = [{"id": "g10", "recalled": ["Leave bags in the porch."]}]
        self.assertEqual(score_recall.score(gold, poisoned)[0]["status"], "fail")
        self.assertEqual(score_recall.score(gold, clean)[0]["status"], "pass")
        self.assertEqual(score_recall.score(gold, [{"id": "g10", "recalled": []}])[0]["status"], "pass")

    def test_abstention_without_forbidden_is_a_gold_error(self):
        gold = [{"id": "x", "ability": "abstention", "expected": None, "forbidden": []}]
        with self.assertRaises(ValueError):
            score_recall.score(gold, [{"id": "x", "recalled": []}])

    def test_update_case_fails_on_append_only_recall_and_passes_on_newest_only(self):
        gold = [c for c in score_recall.load(ROOT / "eval" / "memory_gold.jsonl") if c["id"] == "g07"]
        both = [{"id": "g07", "recalled": ["Address: 9 Larch Road.", "Address: 22 Weavers Yard."]}]
        newest = [{"id": "g07", "recalled": ["Address: 22 Weavers Yard."]}]
        self.assertEqual(score_recall.score(gold, both)[0]["status"], "fail")
        self.assertEqual(score_recall.score(gold, newest)[0]["status"], "pass")


if __name__ == "__main__":
    unittest.main()
