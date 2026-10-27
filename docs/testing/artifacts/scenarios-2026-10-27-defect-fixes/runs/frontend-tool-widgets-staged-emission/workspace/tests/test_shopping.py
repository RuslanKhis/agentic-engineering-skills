import re
import unittest
from pathlib import Path
from unittest import mock

from app import callbacks, staging, widgets
from app.tools.shopping import (compare_products, recommend_products, search_products,
                                show_last_results)


class FakeContext:
    """Duck-typed stand-in for the tool and callback contexts. Not an ADK context."""

    def __init__(self, state=None):
        self.state = dict(state or {})
        self.rendered = []

    def render_ui_widget(self, widget):
        self.rendered.append(widget)


def plain_widget(widget_id, payload):
    return {"id": widget_id, "payload": payload}


@mock.patch.object(widgets, "to_ui_widget", plain_widget)
class StagedWidgetTests(unittest.TestCase):
    def test_tools_stage_and_never_render(self):
        ctx = FakeContext()
        result = search_products("waterproof jacket", ctx)
        self.assertEqual(result["skus"], ["JK-210", "JK-115"])
        self.assertEqual(ctx.state["last_search"]["skus"], ["JK-210", "JK-115"])
        self.assertEqual(ctx.rendered, [])
        self.assertFalse(ctx.state[staging.STATE_KEY][widgets.CARDS_ID]["emitted"])

    def test_callback_emits_cards_with_currency(self):
        ctx = FakeContext({"user:currency": "EUR"})
        search_products("daypack", ctx)
        callbacks.refresh_cards_after_preference_change(ctx)
        self.assertEqual(ctx.rendered[0]["payload"]["components"][0]["price"], "€74.00")

    def test_two_tools_same_id_emit_once_and_second_run_emits_nothing(self):
        ctx = FakeContext()
        search_products("jacket", ctx)
        recommend_products("hiking", ctx)
        callbacks.refresh_cards_after_preference_change(ctx)
        self.assertEqual([w["id"] for w in ctx.rendered], ["product-cards"])
        callbacks.refresh_cards_after_preference_change(ctx)
        self.assertEqual(len(ctx.rendered), 1)

    def test_cards_then_table_in_declared_order(self):
        ctx = FakeContext()
        compare_products(["JK-210", "JK-340"], ctx)
        search_products("jacket", ctx)
        callbacks.refresh_cards_after_preference_change(ctx)
        self.assertEqual([w["id"] for w in ctx.rendered], ["product-cards", "comparison-table"])

    def test_emission_writes_state_so_an_event_is_produced(self):
        ctx = FakeContext()
        search_products("jacket", ctx)
        callbacks.refresh_cards_after_preference_change(ctx)
        self.assertTrue(ctx.state[staging.STATE_KEY][widgets.CARDS_ID]["emitted"])

    def test_currency_change_rerenders_last_cards(self):
        ctx = FakeContext()
        search_products("daypack", ctx)
        callbacks.refresh_cards_after_preference_change(ctx)
        ctx.state["user:currency"] = "EUR"
        callbacks.refresh_cards_after_preference_change(ctx)
        self.assertEqual(len(ctx.rendered), 2)
        self.assertEqual(ctx.rendered[1]["payload"]["components"][0]["price"], "€74.00")
        callbacks.refresh_cards_after_preference_change(ctx)
        self.assertEqual(len(ctx.rendered), 2)

    def test_no_cards_no_refresh(self):
        ctx = FakeContext({"user:currency": "EUR"})
        callbacks.refresh_cards_after_preference_change(ctx)
        self.assertEqual(ctx.rendered, [])

    def test_show_last_results_restages_without_searching(self):
        ctx = FakeContext()
        search_products("jacket", ctx)
        callbacks.refresh_cards_after_preference_change(ctx)
        self.assertEqual(show_last_results(ctx)["skus"], ctx.state["last_search"]["skus"])
        callbacks.refresh_cards_after_preference_change(ctx)
        self.assertEqual(len(ctx.rendered), 2)
        self.assertEqual(ctx.rendered[0], ctx.rendered[1])

    def test_show_last_results_without_search_is_error(self):
        self.assertEqual(show_last_results(FakeContext())["status"], "error")

    def test_compare_errors_stage_nothing(self):
        ctx = FakeContext()
        self.assertEqual(compare_products(["JK-210"], ctx)["status"], "error")
        self.assertNotIn(staging.STATE_KEY, ctx.state)

    def test_render_ui_widget_has_one_call_site(self):
        root = Path(__file__).resolve().parents[1] / "app"
        sites = [str(p) for p in root.rglob("*.py")
                 if re.search(r"\.render_ui_widget\(", p.read_text(encoding="utf-8"))]
        self.assertEqual([Path(s).name for s in sites], ["staging.py"])


if __name__ == "__main__":
    unittest.main()
