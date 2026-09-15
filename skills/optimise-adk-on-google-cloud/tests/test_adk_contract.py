"""Offline wire-shape integration; constructs ADK objects without model clients."""
import importlib.metadata
import unittest

from test_check_run import checker, example


class AdkWireContract(unittest.TestCase):
    def test_pinned_adk_serialisation_reaches_checker(self):
        try:
            version = importlib.metadata.version("google-adk")
        except importlib.metadata.PackageNotFoundError:
            self.skipTest("ADK is absent; standard-library tests remain available")
        if version != "2.8.0":
            self.skipTest("This recorded ADK wire integration requires 2.8.0; preserve target pins")
        from google.adk.events import Event
        from google.genai import types

        _, expected = example()
        common = {"author": "catalogue_agent", "invocation_id": "wire-test"}
        events = [
            Event(**common, content=types.Content(role="model", parts=[types.Part(
                function_call=types.FunctionCall(id="c1", name="get_schema", args={}))])),
            Event(**common, content=types.Content(role="user", parts=[types.Part(
                function_response=types.FunctionResponse(id="c1", name="get_schema", response={
                    "status": "success", "result": "user_id, revenue"}))])),
            Event(**common, partial=True, content=types.Content(role="model", parts=[types.Part(text="user_id")])),
            Event(**common, partial=True, content=types.Content(role="model", parts=[types.Part(text="revenue")])),
            Event(**common, finish_reason=types.FinishReason.STOP, content=types.Content(
                role="model", parts=[types.Part(text="user_id, revenue")])),
        ]
        for aliases in (False, True):
            wire = [event.model_dump(mode="json", by_alias=aliases, exclude_none=True) for event in events]
            self.assertEqual(checker.check_events(wire, expected)["verdict"], "PASS")


if __name__ == "__main__":
    unittest.main()
