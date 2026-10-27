import asyncio
import unittest

try:
    from google.genai import types
    from app.screening import BLOCKED_REPLY, OutputScreenPlugin
except ImportError:  # the SDK is not needed for the other unit tests
    types = None


class FakeArmor:
    def __init__(self, verdict=False, error=None):
        self.verdict, self.error, self.seen = verdict, error, []

    async def sanitize_model_response(self, text):
        self.seen.append(text)
        if self.error:
            raise self.error
        return self.verdict


class FakeContext:
    def __init__(self):
        self.state = {}


def _response(with_call=True):
    parts = [types.Part(text="Sending that now.")]
    if with_call:
        parts.append(types.Part(function_call=types.FunctionCall(name="send_email", args={"to": "x@example.test"})))
    return types.Content(role="model", parts=parts), parts


@unittest.skipIf(types is None, "google-adk is not installed")
class OutputScreenTests(unittest.TestCase):
    def _run(self, armor, content):
        from google.adk.models.llm_response import LlmResponse
        plugin = OutputScreenPlugin(client=armor)
        return asyncio.run(plugin.after_model_callback(
            callback_context=FakeContext(), llm_response=LlmResponse(content=content)))

    def test_flagged_response_is_replaced_before_tool_calls_can_dispatch(self):
        content, _ = _response()
        result = self._run(FakeArmor(verdict=True), content)
        self.assertEqual([p.text for p in result.content.parts], [BLOCKED_REPLY])
        self.assertFalse(any(p.function_call for p in result.content.parts))

    def test_unavailable_screen_withholds(self):
        content, _ = _response()
        result = self._run(FakeArmor(error=RuntimeError("down")), content)
        self.assertEqual([p.text for p in result.content.parts], [BLOCKED_REPLY])

    def test_clean_response_passes_unchanged(self):
        content, _ = _response()
        self.assertIsNone(self._run(FakeArmor(verdict=False), content))

    def test_tool_call_arguments_are_screened(self):
        armor = FakeArmor()
        content, _ = _response()
        self._run(armor, content)
        self.assertIn("x@example.test", armor.seen[0])


if __name__ == "__main__":
    unittest.main()
