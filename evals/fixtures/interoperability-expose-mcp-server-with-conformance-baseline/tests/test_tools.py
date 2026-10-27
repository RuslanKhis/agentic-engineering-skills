import unittest

from research.tools import get_abstract, search_papers


class ToolTests(unittest.TestCase):
    def test_search(self):
        self.assertEqual(search_papers("agents reliability")["papers"][0]["paper_id"], "p-102")

    def test_unknown_paper(self):
        self.assertEqual(get_abstract("p-999")["status"], "not_found")


if __name__ == "__main__":
    unittest.main()
