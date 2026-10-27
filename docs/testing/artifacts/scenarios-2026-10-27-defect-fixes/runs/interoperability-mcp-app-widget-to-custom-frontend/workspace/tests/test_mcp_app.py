"""Run: python -I -m unittest tests.test_mcp_app (stdlib only; mcp_app imports mcp lazily)."""
import json
import pathlib
import unittest

from insights import mcp_app

PARTNER = pathlib.Path(__file__).parent.parent / "partner" / "tools-list-with-ui-capability.json"


class VisibilityGuard(unittest.TestCase):
    def tools(self):
        return {t["name"]: t.get("_meta") for t in json.loads(PARTNER.read_text())["tools"]}

    def test_refresh_chart_is_app_only(self):
        meta = self.tools()["refresh_chart"]
        self.assertTrue(mcp_app.app_may_call(meta))
        self.assertNotIn("model", mcp_app.ui_meta(meta)[1])

    def test_get_chart_resource(self):
        self.assertEqual(mcp_app.ui_meta(self.tools()["get_chart"])[0], "ui://charts/trend.html")

    def test_model_only_tool_refused_for_app(self):
        self.assertFalse(mcp_app.app_may_call({"ui": {"visibility": ["model"]}}))


if __name__ == "__main__":
    unittest.main()
