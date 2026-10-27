"""In-process protocol tests for the exposed MCP server, under both protocol eras.

Skipped where google-adk or mcp is not installed (same convention as test_agent_scripted).
"""
import importlib.metadata
import importlib.util
import os
import pathlib
import unittest

try:
    HAVE_STACK = all(importlib.util.find_spec(m) is not None for m in ("google.adk", "mcp"))
except ModuleNotFoundError:
    HAVE_STACK = False

ERAS = {"modern (2026-07-28)": {}, "legacy (handshake)": {"mode": "legacy"}}


def _field(obj, *names):
    for n in names:
        if hasattr(obj, n):
            return getattr(obj, n)
    raise AttributeError(names)


def _text(result) -> str:
    return "".join(getattr(b, "text", "") for b in _field(result, "content"))


@unittest.skipUnless(HAVE_STACK, "google-adk and mcp not installed")
class McpServerTests(unittest.IsolatedAsyncioTestCase):
    def _server(self, model):
        from research.agent import root_agent
        from research.mcp_server import build_server
        return root_agent, build_server(root_agent.clone(update={"model": model}))

    async def test_lists_one_tool_that_describes_capability(self):
        import mcp
        from tests.scripted_model import FixedTextModel
        agent, server = self._server(FixedTextModel())
        for era, kw in ERAS.items():
            with self.subTest(era):
                async with mcp.Client(server, **kw) as client:
                    tools = _field(await client.list_tools(), "tools")
                self.assertEqual([t.name for t in tools], ["paper_research"])
                self.assertEqual(tools[0].description, agent.description)
                schema = _field(tools[0], "inputSchema", "input_schema")
                self.assertEqual(set(schema["properties"]), {"request"})
                self.assertEqual(schema["required"], ["request"])
                # The agent instruction must not leak into what hosts see.
                self.assertNotIn("Never invent", tools[0].description)

    async def test_call_returns_text_answer(self):
        import mcp
        from tests.scripted_model import FixedTextModel
        _, server = self._server(FixedTextModel(text="See p-102."))
        for era, kw in ERAS.items():
            with self.subTest(era):
                async with mcp.Client(server, **kw) as client:
                    result = await client.call_tool("paper_research", {"request": "agents?"})
                self.assertFalse(_field(result, "isError", "is_error"))
                self.assertIn("p-102", _text(result))

    async def test_agent_exception_is_a_tool_error_not_a_crash(self):
        import mcp
        from tests.scripted_model import FailingModel
        _, server = self._server(FailingModel())
        for era, kw in ERAS.items():
            with self.subTest(era):
                async with mcp.Client(server, **kw) as client:
                    result = await client.call_tool("paper_research", {"request": "agents?"})
                    self.assertTrue(_field(result, "isError", "is_error"))
                    # The server is still usable after the failure.
                    self.assertTrue(_field(await client.list_tools(), "tools"))

    async def test_unknown_tool_is_refused(self):
        import mcp
        from tests.scripted_model import FixedTextModel
        _, server = self._server(FixedTextModel())
        async with mcp.Client(server) as client:
            try:
                result = await client.call_tool("no_such_tool", {})
            except Exception:  # a JSON-RPC error is an acceptable refusal
                return
            self.assertTrue(_field(result, "isError", "is_error"))


@unittest.skipUnless(HAVE_STACK and not os.environ.get("MCP_DRIFT_RUN"), "stack missing or drift run")
class PinTests(unittest.TestCase):
    def test_installed_mcp_matches_ci_constraint(self):
        constraints = pathlib.Path(__file__).parent.parent / "ci" / "constraints.txt"
        pins = dict(l.strip().split("==") for l in constraints.read_text().splitlines() if "==" in l)
        self.assertEqual(importlib.metadata.version("mcp"), pins["mcp"],
                         "installed mcp differs from ci/constraints.txt: bump the pin deliberately")


if __name__ == "__main__":
    unittest.main()
