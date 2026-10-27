import json
import unittest
from types import SimpleNamespace as NS

from app.streaming import GENERIC_ERROR, stream_frames


def call(name, id="c1"):
    return NS(function_call=NS(id=id, name=name), function_response=None, text=None, thought=False)


def result(name, response, id="c1"):
    return NS(function_response=NS(id=id, name=name, response=response), function_call=None,
              text=None, thought=False)


def text(t, thought=False):
    return NS(text=t, function_call=None, function_response=None, thought=thought)


def event(*parts, error_code=None):
    return NS(content=NS(parts=list(parts)), error_code=error_code, error_message=None)


async def run(events, fail_after=None):
    async def gen():
        for e in events:
            yield e
        if fail_after:
            raise fail_after
    return [json.loads(b) async for b in stream_frames("s1", gen())]


class StreamingTests(unittest.IsolatedAsyncioTestCase):
    async def test_tool_lifecycle_then_text(self):
        frames = await run([
            event(call("lookup_order")),
            event(result("lookup_order", {"status": "ok", "order": {"secret": 1}})),
            event(text("Shipped.")),
        ])
        self.assertEqual([f["type"] for f in frames],
                         ["session", "tool_start", "tool_end", "text", "done"])
        self.assertTrue(frames[2]["ok"])
        self.assertNotIn("secret", json.dumps(frames))  # results are not public

    async def test_tool_error_status_marks_step_failed(self):
        frames = await run([event(call("issue_refund")),
                            event(result("issue_refund", {"status": "error", "message": "x"}))])
        self.assertFalse(frames[2]["ok"])

    async def test_thought_text_is_dropped(self):
        frames = await run([event(text("thinking", thought=True), text("Hi"))])
        self.assertEqual([f.get("text") for f in frames if f["type"] == "text"], ["Hi"])

    async def test_exception_after_text_keeps_text_and_ends_with_error(self):
        frames = await run([event(text("Partial"))], fail_after=RuntimeError("boom: internal detail"))
        self.assertEqual([f["type"] for f in frames], ["session", "text", "error"])
        self.assertEqual(frames[-1]["message"], GENERIC_ERROR)

    async def test_event_error_code_is_terminal_error(self):
        frames = await run([event(text("Partial")), event(error_code="X"), event(text("never"))])
        self.assertEqual([f["type"] for f in frames], ["session", "text", "error"])

    async def test_call_without_result_is_closed_as_failed(self):
        frames = await run([event(call("search_help"))])
        self.assertEqual([f["type"] for f in frames], ["session", "tool_start", "tool_end", "done"])
        self.assertFalse(frames[2]["ok"])


if __name__ == "__main__":
    unittest.main()
