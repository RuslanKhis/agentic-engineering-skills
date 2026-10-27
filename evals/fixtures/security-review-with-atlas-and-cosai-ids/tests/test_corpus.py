import unittest

from corpus.index import CorpusIndex


class CorpusTests(unittest.TestCase):
    def test_search_finds_procedure(self):
        hits = CorpusIndex.load().search("lost pallet carrier")
        self.assertEqual(hits[0]["doc"], "carrier-escalations.md")


if __name__ == "__main__":
    unittest.main()
