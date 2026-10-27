"""Retry and parsing behaviour with a fake runner; no model and no google.adk needed for most tests."""
import asyncio
import importlib.util
import json
import unittest

HAS_PYDANTIC = importlib.util.find_spec("pydantic") is not None
HAS_ADK = importlib.util.find_spec("google.adk") is not None if importlib.util.find_spec("google") else False

VALID = {"claim_reference": "CLM-2026-04411", "claim_type": "glass", "urgency": "routine"}


class _Session:
    def __init__(self, state=None):
        self.id = "s1"
        self.state = state or {}


class _SessionService:
    def __init__(self, runner):
        self.runner = runner

    async def create_session(self, app_name, user_id):
        return _Session()

    async def get_session(self, app_name, user_id, session_id):
        return _Session(self.runner.next_state())


class FakeRunner:
    """Each run_async call consumes one scripted outcome: a state value, or an exception to raise."""

    def __init__(self, outcomes):
        self.outcomes = list(outcomes)
        self.messages = []
        self.session_service = _SessionService(self)
        self._current = None

    async def run_async(self, user_id, session_id, new_message):
        self.messages.append(new_message.parts[0].text)
        self._current = self.outcomes.pop(0)
        if isinstance(self._current, Exception):
            raise self._current
        return
        yield  # makes this an async generator

    def next_state(self):
        return {} if self._current is None else {"extraction": self._current}


@unittest.skipUnless(HAS_PYDANTIC and HAS_ADK, "pydantic and google-adk needed (types.Content)")
class RetryTests(unittest.TestCase):
    def run_extract(self, outcomes, **kw):
        from extractor.pipeline import extract_with_runner

        runner = FakeRunner(outcomes)
        result = asyncio.run(extract_with_runner(runner, "email body", **kw))
        return result, runner

    def test_first_attempt_dict(self):
        result, _ = self.run_extract([VALID])
        self.assertEqual((result.status, result.attempts), ("ok", 1))

    def test_fenced_string_is_accepted(self):
        result, _ = self.run_extract(["```json\n" + json.dumps(VALID) + "\n```"])
        self.assertEqual(result.status, "ok")

    def test_prose_then_valid_retries_with_error_feedback(self):
        from pydantic import ValidationError

        try:
            from extractor.schema import ClaimExtraction
            ClaimExtraction.model_validate_json("Here is the claim")
        except ValidationError as exc:
            raised = exc
        result, runner = self.run_extract([raised, VALID])
        self.assertEqual((result.status, result.attempts), ("ok", 2))
        self.assertIn("ValidationError", runner.messages[1])

    def test_budget_exhausted_returns_explicit_failure(self):
        result, runner = self.run_extract(["prose", "more prose", "still prose"], max_attempts=3)
        self.assertEqual((result.status, result.attempts, result.extraction), ("failed", 3, None))
        self.assertEqual(len(runner.messages), 3)

    def test_schema_valid_but_wrong_enum_counts_as_failure(self):
        result, _ = self.run_extract([dict(VALID, claim_type="flood")], max_attempts=1)
        self.assertEqual(result.status, "failed")


@unittest.skipUnless(HAS_PYDANTIC and HAS_ADK, "pydantic and google-adk not installed")
class PathCaptureTests(unittest.TestCase):
    """Proves which mechanism carried the schema, with a scripted model (no provider call).

    Run once per backend:  GOOGLE_GENAI_USE_ENTERPRISE=true  and  unset (API key, GOOGLE_API_KEY=dummy).
    Expected on the API-key backend in 2.8.0: gatherer has tools and no schema; formatter has schema,
    JSON mime type and no tools. On either backend the formatter must never carry set_model_response.
    """

    def test_schema_is_on_the_tool_free_agent_only(self):
        from google.adk.models.base_llm import BaseLlm
        from google.adk.models.llm_response import LlmResponse
        from google.adk.runners import InMemoryRunner
        from google.genai import types

        from extractor import agent as agent_module
        from extractor import probe

        class Scripted(BaseLlm):
            async def generate_content_async(self, llm_request, stream=False):
                has_tools = bool(llm_request.config.tools)
                text = "notes: glass claim" if has_tools else json.dumps(VALID)
                yield LlmResponse(content=types.Content(role="model", parts=[types.Part(text=text)]))

        scripted = Scripted(model="scripted")
        agent_module.gather_agent.model = scripted
        agent_module.format_agent.model = scripted
        probe.CAPTURED.clear()

        async def go():
            runner = InMemoryRunner(agent=agent_module.extraction_agent, app_name="t")
            session = await runner.session_service.create_session(app_name="t", user_id="u")
            msg = types.Content(role="user", parts=[types.Part(text="CLM-2026-04411 cracked windscreen")])
            async for _ in runner.run_async(user_id="u", session_id=session.id, new_message=msg):
                pass
            return await runner.session_service.get_session(app_name="t", user_id="u", session_id=session.id)

        session = asyncio.run(go())
        by_agent = {r["agent"]: r for r in probe.CAPTURED}
        gather, fmt = by_agent["claim_gatherer"], by_agent["claim_formatter"]
        self.assertEqual(gather["tool_names"], ["lookup_policy", "lookup_repairer"])
        self.assertFalse(gather["response_schema"])
        self.assertTrue(fmt["response_schema"])  # 2.8.0 carries the schema in response_schema
        self.assertEqual(fmt["response_mime_type"], "application/json")
        self.assertEqual(fmt["tool_names"], [])
        self.assertFalse(fmt["set_model_response"])
        self.assertEqual(session.state["extraction"]["claim_type"], "glass")


if __name__ == "__main__":
    unittest.main()
