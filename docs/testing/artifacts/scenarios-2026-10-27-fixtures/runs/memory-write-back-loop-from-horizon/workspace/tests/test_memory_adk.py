import unittest
from types import SimpleNamespace

try:
    import google.adk  # noqa: F401
    HAVE_ADK = True
except ImportError:
    HAVE_ADK = False


def ctx(user_id, text="torque", search=None, add=None):
    parts = [SimpleNamespace(text=text)]
    return SimpleNamespace(user_id=user_id, invocation_id="inv1", function_call_id="fc1",
                           user_content=SimpleNamespace(parts=parts), search_memory=search, add_events_to_memory=add)


class Request:
    def __init__(self):
        self.added = []

    def append_instructions(self, items):
        self.added.extend(items)


@unittest.skipUnless(HAVE_ADK, "google-adk is not installed")
class GlueTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        from fieldline.memory_adk import GovernedRecallTool, make_flush_callback, make_memory_tools
        from fieldline.memory_controls import MemoryControls

        self.mc = MemoryControls(known_sites={"NW-0417"})
        self.recall = GovernedRecallTool(self.mc)
        self.flush = make_flush_callback(self.mc)
        self.tools = {t.__name__: t for t in make_memory_tools(self.mc)}

    async def test_tool_uses_authenticated_user_not_model_arguments(self):
        self.mc.grant_consent("eng-ravi")
        result = self.tools["remember"]("kit", "I carry a splicer.", ctx("eng-ravi"))
        self.assertEqual(result["status"], "recorded")
        self.assertEqual(self.mc.list_facts("eng-mei"), [])
        self.assertEqual(len(self.mc.list_facts("eng-ravi")), 1)

    async def test_tools_cannot_grant_consent(self):
        self.assertNotIn("grant_consent", self.tools)
        result = self.tools["remember"]("kit", "I carry a splicer.", ctx("eng-ravi"))
        self.assertEqual(result["status"], "consent_required")

    async def test_flush_writes_events_through_the_context_and_never_raises(self):
        self.mc.grant_consent("eng-ravi")
        self.tools["remember"]("kit", "I carry a splicer.", ctx("eng-ravi"))
        sent = []

        async def add(*, events):
            sent.append(events)

        await self.flush(ctx("eng-ravi", add=add))
        self.assertEqual(len(sent), 1)
        self.assertEqual(sent[0][0].content.parts[0].text, "I carry a splicer.")

        async def broken(*, events):
            raise RuntimeError("down")

        self.tools["remember"]("kit", "I carry a drill.", SimpleNamespace(
            user_id="eng-ravi", invocation_id="inv2", function_call_id="fc2"))
        self.assertIsNone(await self.flush(ctx("eng-ravi", add=broken)))

    async def test_recall_tool_injects_only_consented_own_facts(self):
        self.mc.grant_consent("eng-ravi")
        self.tools["remember"]("kit", "I carry a splicer.", ctx("eng-ravi"))

        async def add(*, events):
            return None

        await self.flush(ctx("eng-ravi", add=add))
        text = "I carry a splicer."

        async def search(query):
            entry = SimpleNamespace(content=SimpleNamespace(parts=[SimpleNamespace(text=text)]))
            return SimpleNamespace(memories=[entry])

        req = Request()
        await self.recall.process_llm_request(tool_context=ctx("eng-ravi", search=search), llm_request=req)
        self.assertIn("I carry a splicer.", req.added[0])
        req = Request()
        await self.recall.process_llm_request(tool_context=ctx("eng-mei", search=search), llm_request=req)
        self.assertEqual(req.added, [])

    async def test_recall_tool_tells_the_model_when_memory_is_down(self):
        self.mc.grant_consent("eng-ravi")

        async def search(query):
            raise RuntimeError("down")

        req = Request()
        await self.recall.process_llm_request(tool_context=ctx("eng-ravi", search=search), llm_request=req)
        self.assertIn("could not be read", req.added[0])


if __name__ == "__main__":
    unittest.main()
