"""Scripted-model Runner tests of stored effects. Need google-adk; skipped (not run) where it is absent.

Written against the 2.8.0 surfaces named in the memory reference and never executed in the session that wrote them:
expect to adjust import paths or the scripted model on first run.
"""
import unittest

try:
    import google.adk  # noqa: F401
    HAVE_ADK = True
except ImportError:
    HAVE_ADK = False


@unittest.skipUnless(HAVE_ADK, "google-adk is not installed")
class RunnerMemoryTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        from google.adk.agents import LlmAgent
        from google.adk.memory import InMemoryMemoryService
        from google.adk.models.base_llm import BaseLlm
        from google.adk.models.llm_response import LlmResponse
        from google.adk.runners import Runner
        from google.adk.sessions import InMemorySessionService
        from google.genai import types

        from fieldline import memory_tools as T
        from fieldline.memory_adk import AdkMemoryBackend, in_memory_eraser_for, recall_instruction, save_memories_callback
        from fieldline.memory_governor import MemoryGovernor
        from fieldline.memory_ledger import MemoryLedger

        outer = self
        outer.seen_instructions = []

        class Scripted(BaseLlm):
            """Calls the tool named in the user's message prefix 'remember:', otherwise answers in text."""
            model: str = "scripted"

            async def generate_content_async(self, llm_request, stream=False):
                outer.seen_instructions.append(str(llm_request.config.system_instruction))
                last = llm_request.contents[-1]
                part = last.parts[0]
                if part.function_response is not None:
                    yield LlmResponse(content=types.Content(role="model", parts=[types.Part(text="done")]))
                elif (part.text or "").startswith("remember:"):
                    args = {"topic": "answer_style", "text": part.text.split(":", 1)[1].strip()}
                    yield LlmResponse(content=types.Content(role="model", parts=[
                        types.Part(function_call=types.FunctionCall(name="remember", args=args))]))
                else:
                    yield LlmResponse(content=types.Content(role="model", parts=[types.Part(text="ok")]))

        raw = InMemoryMemoryService()
        self.gov = MemoryGovernor(MemoryLedger(":memory:"),
                                  AdkMemoryBackend(raw, "fieldline", in_memory_eraser_for(raw, "fieldline")))
        T.set_governor(self.gov)
        self.addCleanup(T.set_governor, None)
        agent = LlmAgent(name="fieldline", model=Scripted(), instruction=recall_instruction("base", self.gov),
                         tools=[T.remember, T.list_my_memories, T.forget_memory],
                         after_agent_callback=save_memories_callback(self.gov))
        self.sessions = InMemorySessionService()
        self.runner = Runner(app_name="fieldline", agent=agent, session_service=self.sessions)
        self.types = types

    async def say(self, user, text):
        s = await self.sessions.create_session(app_name="fieldline", user_id=user)
        msg = self.types.Content(role="user", parts=[self.types.Part(text=text)])
        async for _ in self.runner.run_async(user_id=user, session_id=s.id, new_message=msg):
            pass

    async def test_saved_then_recalled_for_owner_only_then_forgotten(self):
        self.gov.grant_consent("eng-ravi")
        self.gov.grant_consent("eng-mia")
        await self.say("eng-ravi", "remember: metric torque values")
        mem = self.gov.list_memories("eng-ravi")
        self.assertEqual([m["status"] for m in mem], ["accepted"])
        await self.say("eng-ravi", "hello")
        self.assertIn("metric torque values", self.seen_instructions[-1])
        await self.say("eng-mia", "hello")
        self.assertNotIn("metric torque values", self.seen_instructions[-1])
        await self.gov.forget("eng-ravi", mem[0]["memory_id"])
        await self.say("eng-ravi", "hello")
        self.assertNotIn("metric torque values", self.seen_instructions[-1])

    async def test_no_consent_no_write(self):
        await self.say("eng-ravi", "remember: metric torque values")
        self.assertEqual(self.gov.ledger.list_live("eng-ravi"), [])


if __name__ == "__main__":
    unittest.main()
