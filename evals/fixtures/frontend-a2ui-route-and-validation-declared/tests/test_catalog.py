import unittest

from app.tools.catalog import compare_products, search_products


class CatalogTests(unittest.TestCase):
    def test_search_matches_all_terms(self):
        skus = [p["sku"] for p in search_products("waterproof jacket")["products"]]
        self.assertEqual(skus, ["JK-210", "JK-115"])

    def test_search_price_limit(self):
        skus = [p["sku"] for p in search_products("jacket", max_price_cents=10000)["products"]]
        self.assertEqual(skus, ["JK-115"])

    def test_compare_needs_two_to_four(self):
        self.assertEqual(compare_products(["JK-210"])["status"], "error")
        table = compare_products(["JK-210", "JK-115"])
        self.assertEqual([r["sku"] for r in table["rows"]], ["JK-210", "JK-115"])

    def test_compare_unknown_sku(self):
        self.assertIn("XX-1", compare_products(["JK-210", "XX-1"])["message"])


if __name__ == "__main__":
    unittest.main()
