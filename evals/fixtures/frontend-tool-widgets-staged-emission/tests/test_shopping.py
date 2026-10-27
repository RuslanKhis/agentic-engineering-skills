import unittest
from unittest import mock

from app import widgets
from app.tools.shopping import compare_products, search_products


class FakeToolContext:
    """Duck-typed stand-in for the attributes the tools use. Not an ADK ToolContext."""

    def __init__(self, state=None):
        self.state = dict(state or {})
        self.rendered = []

    def render_ui_widget(self, widget):
        self.rendered.append(widget)


def plain_widget(widget_id, payload):
    return {"id": widget_id, "payload": payload}


@mock.patch.object(widgets, "to_ui_widget", plain_widget)
class ShoppingToolTests(unittest.TestCase):
    def test_search_returns_skus_and_shows_cards(self):
        ctx = FakeToolContext()
        result = search_products("waterproof jacket", ctx)
        self.assertEqual(result["skus"], ["JK-210", "JK-115"])
        self.assertEqual(ctx.rendered[0]["id"], "product-cards")
        self.assertEqual(ctx.state["last_search"]["skus"], ["JK-210", "JK-115"])

    def test_cards_use_currency(self):
        ctx = FakeToolContext({"user:currency": "EUR"})
        search_products("daypack", ctx)
        self.assertEqual(ctx.rendered[0]["payload"]["components"][0]["price"], "€74.00")

    def test_compare_shows_table(self):
        ctx = FakeToolContext()
        self.assertEqual(compare_products(["JK-210", "JK-340"], ctx)["status"], "ok")
        self.assertEqual(ctx.rendered[0]["id"], "comparison-table")


if __name__ == "__main__":
    unittest.main()
