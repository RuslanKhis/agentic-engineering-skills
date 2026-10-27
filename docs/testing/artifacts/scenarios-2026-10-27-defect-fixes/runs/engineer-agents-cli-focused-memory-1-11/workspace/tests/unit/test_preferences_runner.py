"""Stored effects of the language preference through a real Runner and a scripted model. Offline.

Needs google-adk and aiosqlite (SQLite stands in for Cloud SQL; no network, no model call).
Skipped when either is missing, so a skip is `not run`, not a pass.
"""
import os
import tempfile
import unittest

try:
    import aiosqlite  # noqa: F401
    import google.adk  # noqa: F401
    HAVE_DEPS = True
except ImportError:
    HAVE_DEPS = False


@unittest.skipUnless(HAVE_DEPS, "google-adk and aiosqlite are required")
class LanguageRunnerTest(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self._dir = tempfile.TemporaryDirectory()
        self.url = f"sqlite+aiosqlite:///{os.path.join(self._dir.name, 'sessions.db')}"

    def tearDown(self):
        self._dir.cleanup()

    def _runner(self, script):
        """A Runner over a fresh DatabaseSessionService, as after a process restart."""
        from google.adk.agents import Agent
        from google.adk.apps import App
        from google.adk.models.base_llm import BaseLlm
        from google.adk.models.llm_response import LlmResponse
        from google.adk.runners import Runner
        from google.adk.sessions import DatabaseSessionService
        from google.genai import types

        from app.agent import instruction_provider
        from app.tools import my_tickets, raise_ticket, search_kb, set_response_language

        seen = []

        class Scripted(BaseLlm):
            async def generate_content_async(self, llm_request, stream=False):
                seen.append(str(llm_request.config.system_instruction))
                step = script.pop(0) if script else None
                part = (types.Part.from_function_call(name=step[0], args=step[1]) if step
                        else types.Part(text="ok"))
                yield LlmResponse(content=types.Content(role="model", parts=[part]))

        agent = Agent(name="helpdesk", model=Scripted(model="scripted"), instruction=instruction_provider,
                      tools=[search_kb, my_tickets, raise_ticket, set_response_language])
        runner = Runner(app=App(name="app", root_agent=agent), session_service=DatabaseSessionService(self.url))
        return runner, seen

    async def _turn(self, runner, user_id, text="hello"):
        from google.genai import types
        session = await runner.session_service.create_session(app_name="app", user_id=user_id)
        async for _ in runner.run_async(user_id=user_id, session_id=session.id,
                                        new_message=types.Content(role="user", parts=[types.Part(text=text)])):
            pass
        return session.id

    async def test_saved_persists_across_restart_and_is_not_shared(self):
        runner, _ = self._runner([("set_response_language", {"language": "fr"})])
        await self._turn(runner, "s-100", "reply in French from now on")

        restarted, seen = self._runner([])
        await self._turn(restarted, "s-100")
        self.assertIn("French", seen[-1])

        other, seen_other = self._runner([])
        await self._turn(other, "s-200")
        self.assertNotIn("French", seen_other[-1])

    async def test_rejected_language_stores_nothing(self):
        runner, _ = self._runner([("set_response_language", {"language": "Klingon"})])
        await self._turn(runner, "s-100")
        state = (await runner.session_service.create_session(app_name="app", user_id="s-100")).state
        self.assertNotIn("user:response_language", state)


if __name__ == "__main__":
    unittest.main()
