import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("score_recall", ROOT / "eval" / "score_recall.py")
score_recall = importlib.util.module_from_spec(spec)
spec.loader.exec_module(score_recall)


class ScoreRecallTests(unittest.TestCase):
    def test_saved_outputs_pass_the_gold_set(self):
        gold = score_recall.load(ROOT / "eval" / "memory_gold.jsonl")
        outputs = score_recall.load(ROOT / "eval" / "recall_outputs.jsonl")
        self.assertTrue(all(r["pass"] for r in score_recall.score(gold, outputs)))

    def test_forbidden_phrase_fails_a_case(self):
        gold = [{"id": "x", "ability": "information_extraction", "expected": ["porch"], "forbidden": ["garage"]}]
        outputs = [{"id": "x", "recalled": ["porch", "garage"]}]
        self.assertFalse(score_recall.score(gold, outputs)[0]["pass"])


if __name__ == "__main__":
    unittest.main()
