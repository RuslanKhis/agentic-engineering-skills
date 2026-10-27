import asyncio
import unittest
from types import SimpleNamespace as NS

try:
    from google.genai import types
    from app.screening import BLOCKED_REPLY, OutputScreenPlugin
except ImportError:  # SDK not installed: AGENTS.md keeps it out of the plain unit-test path
    OutputScreenPlugin = None


class FakeArmor:
    def __init__(self, flagged=False, error=False):
        self.flagged, self.error, self.calls = flagged, error, 0

    async def sanitize_model_response(self, text):
        self.calls += 1
        if self.error:
            raise RuntimeError("armor down")
        return self.flagged


def response_with_tool_call():
    return NS(partial=False, content=types.Content(role="model", parts=[
        types.Part(text="Refunding now."),
        types.Part(function_call=types.FunctionCall(name="issue_refund", args={"order_id": "HO-1"}))]))


@unittest.skipIf(OutputScreenPlugin is None, "google-adk not installed")
class OutputScreenTests(unittest.TestCase):
    def run_cb(self, armor, resp):
        plugin = OutputScreenPlugin(client=armor)
        ctx = NS(state={})
        return asyncio.run(plugin.after_model_callback(callback_context=ctx, llm_response=resp)), ctx

    def test_flagged_response_loses_its_tool_call_before_dispatch(self):
        out, ctx = self.run_cb(FakeArmor(flagged=True), response_with_tool_call())
        self.assertEqual([p.text for p in out.content.parts], [BLOCKED_REPLY])
        self.assertFalse(any(p.function_call for p in out.content.parts))
        self.assertTrue(ctx.state["temp:blocked"])

    def test_screen_error_fails_closed(self):
        out, _ = self.run_cb(FakeArmor(error=True), response_with_tool_call())
        self.assertFalse(any(p.function_call for p in out.content.parts))

    def test_clean_response_passes_through(self):
        out, _ = self.run_cb(FakeArmor(), response_with_tool_call())
        self.assertIsNone(out)


if __name__ == "__main__":
    unittest.main()
