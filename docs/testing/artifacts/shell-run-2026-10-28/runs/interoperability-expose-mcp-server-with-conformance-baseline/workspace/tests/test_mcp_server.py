"""In-process MCP protocol tests: the same exchange under the handshake and 2026-07-28 revisions.

Needs google-adk and mcp 2.x; skipped otherwise. Scripted model, no network.
"""
import importlib.util
import unittest

try:
    HAVE = all(importlib.util.find_spec(m) for m in ("google.adk", "mcp"))
except ModuleNotFoundError:
    HAVE = False


@unittest.skipUnless(HAVE, "google-adk and mcp not installed")
class McpServerTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        from google.adk.models.llm_response import LlmResponse
        from google.genai import types

        from research.agent import root_agent
        from tests.scripted_model import ScriptedModel

        self._orig_model = root_agent.model
        root_agent.model = ScriptedModel(responses=[
            LlmResponse(content=types.Content(role="model", parts=[types.Part(function_call=types.FunctionCall(
                name="search_papers", args={"query": "agents"}))])),
            LlmResponse(content=types.Content(role="model", parts=[types.Part(text="See p-102.")])),
        ])

    def tearDown(self):
        from research.agent import root_agent
        root_agent.model = self._orig_model

    async def _each_mode(self):
        import mcp
        from research.mcp_server import build_server
        for kwargs in ({}, {"mode": "legacy"}):   # default negotiates 2026-07-28
            yield kwargs, mcp.Client(build_server(), **kwargs)

    async def test_tools_list_contract(self):
        from research.agent import root_agent
        async for kwargs, client in self._each_mode():
            async with client:
                tools = (await client.list_tools()).tools
            with self.subTest(kwargs=kwargs):
                self.assertEqual([t.name for t in tools], ["paper_research"])
                self.assertEqual(tools[0].description, root_agent.description)
                self.assertEqual(tools[0].inputSchema.get("required"), ["request"])
                self.assertNotIn("search_papers", tools[0].description)  # instruction/tools stay private

    async def test_call_returns_final_answer(self):
        from research.agent import root_agent
        from google.adk.models.llm_response import LlmResponse
        from google.genai import types
        async for kwargs, client in self._each_mode():
            root_agent.model.responses[:] = [
                LlmResponse(content=types.Content(role="model", parts=[types.Part(text="See p-102.")]))]
            async with client:
                result = await client.call_tool("paper_research", {"request": "agents?"})
            with self.subTest(kwargs=kwargs):
                self.assertFalse(result.is_error)
                self.assertIn("p-102", "".join(getattr(c, "text", "") for c in result.content))

    async def test_unknown_tool_is_error_result(self):
        async for kwargs, client in self._each_mode():
            async with client:
                try:
                    result = await client.call_tool("nope", {})
                except Exception:  # a JSON-RPC error is also an acceptable rejection
                    continue
            with self.subTest(kwargs=kwargs):
                self.assertTrue(result.is_error)


if __name__ == "__main__":
    unittest.main()
