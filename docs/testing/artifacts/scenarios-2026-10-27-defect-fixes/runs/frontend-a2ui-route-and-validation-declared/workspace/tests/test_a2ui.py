import unittest

from app.tools.a2ui import A2uiValidationError, check_messages, for_tool_result
from app.tools.catalog import compare_products, search_products


class A2uiTests(unittest.TestCase):
    def test_product_cards_from_search(self):
        msgs = for_tool_result("search_products", search_products("waterproof jacket"))
        self.assertEqual(msgs[0]["createSurface"]["surfaceId"], "products")
        kinds = {c["component"] for c in msgs[1]["updateComponents"]["components"]}
        self.assertEqual(kinds, {"Row", "Card", "Column", "Image", "Text"})

    def test_comparison_table(self):
        msgs = for_tool_result("compare_products", compare_products(["JK-210", "JK-115"]))
        texts = [c["text"] for c in msgs[1]["updateComponents"]["components"] if c["component"] == "Text"]
        self.assertIn("Price", texts)
        self.assertTrue(any(t.startswith("$") for t in texts))

    def test_errors_and_empty_results_render_nothing(self):
        self.assertEqual(for_tool_result("compare_products", compare_products(["JK-210"])), [])
        self.assertEqual(for_tool_result("search_products", {"status": "ok", "products": []}), [])
        self.assertEqual(for_tool_result("lookup_order", {"status": "ok"}), [])

    def test_unknown_component_is_refused(self):
        msgs = for_tool_result("compare_products", compare_products(["JK-210", "JK-115"]))
        msgs[1]["updateComponents"]["components"][1]["component"] = "Carousel"
        with self.assertRaises(A2uiValidationError):
            check_messages(msgs)

    def test_missing_root_and_dangling_reference_are_refused(self):
        update = {"surfaceId": "s", "components": [{"id": "a", "component": "Text", "text": "x"}]}
        with self.assertRaises(A2uiValidationError):
            check_messages([{"updateComponents": update}])
        update = {"surfaceId": "s", "components": [{"id": "root", "component": "Column", "children": ["gone"]}]}
        with self.assertRaises(A2uiValidationError):
            check_messages([{"updateComponents": update}])


if __name__ == "__main__":
    unittest.main()
