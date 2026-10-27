"""Scripted-model Runner harness: drives the real ADK Runner with a model that replays a script.

Needs google-adk; test modules that use it skip when the SDK is not installed.
"""
from __future__ import annotations

try:
    from google.adk.models.base_llm import BaseLlm
    from google.adk.models.llm_response import LlmResponse
    from google.adk.runners import InMemoryRunner
    from google.genai import types
    HAVE_ADK = True
except ImportError:  # the SDK is not installed: unit tests still run, Runner tests skip
    HAVE_ADK = False


if HAVE_ADK:
    class ScriptedModel(BaseLlm):
        """Returns one scripted step per model call: {"function_call": name, "args": {...}} or {"text": ...}."""
        script: list = []
        calls: int = 0
        requests: list = []  # text of every request the model received, for "never reached the model" checks

        async def generate_content_async(self, llm_request, stream: bool = False):
            self.requests.append("\n".join(str(c) for c in llm_request.contents))
            step = self.script[min(self.calls, len(self.script) - 1)]
            self.calls += 1
            if "function_call" in step:
                part = types.Part(function_call=types.FunctionCall(name=step["function_call"],
                                                                   args=step.get("args", {})))
            else:
                part = types.Part(text=step["text"])
            yield LlmResponse(content=types.Content(role="model", parts=[part]))

    async def run_script(agent, script, user_text, user_id="user-1", state=None):
        """Run one user turn with the agent's model replaced by the script; return all events."""
        agent.model = ScriptedModel(model="scripted", script=list(script), requests=[])
        model = agent.model
        runner = InMemoryRunner(agent=agent, app_name="test")
        session = await runner.session_service.create_session(app_name="test", user_id=user_id,
                                                              state=state or {})
        events = []
        async for event in runner.run_async(user_id=user_id, session_id=session.id,
                                            new_message=types.Content(role="user",
                                                                      parts=[types.Part(text=user_text)])):
            events.append(event)
        run_script.last_requests = model.requests
        return events
