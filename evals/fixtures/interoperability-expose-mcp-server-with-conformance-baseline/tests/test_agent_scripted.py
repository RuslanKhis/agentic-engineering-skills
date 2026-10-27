import importlib.util
import unittest

try:
    HAVE_ADK = importlib.util.find_spec("google.adk") is not None
except ModuleNotFoundError:
    HAVE_ADK = False


@unittest.skipUnless(HAVE_ADK, "google-adk not installed")
class ScriptedAgentTests(unittest.TestCase):
    def test_search_then_answer(self):
        from google.adk.runners import InMemoryRunner
        from google.genai import types

        from research.agent import root_agent
        from tests.scripted_model import ScriptedModel
        from google.adk.models.llm_response import LlmResponse

        root_agent.model = ScriptedModel(responses=[
            LlmResponse(content=types.Content(role="model", parts=[types.Part(function_call=types.FunctionCall(
                name="search_papers", args={"query": "agents"}))])),
            LlmResponse(content=types.Content(role="model", parts=[types.Part(text="See p-102.")])),
        ])
        runner = InMemoryRunner(agent=root_agent, app_name="t")
        session = runner.session_service.create_session_sync(app_name="t", user_id="u")
        events = list(runner.run(user_id="u", session_id=session.id,
                                 new_message=types.Content(role="user", parts=[types.Part(text="agents?")])))
        self.assertIn("p-102", events[-1].content.parts[0].text)


if __name__ == "__main__":
    unittest.main()
