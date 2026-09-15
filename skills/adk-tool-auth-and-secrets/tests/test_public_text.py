"""Offline boundary assertions, independent of the book and any credentials."""
from __future__ import annotations

import asyncio
import importlib.util
from pathlib import Path
from types import SimpleNamespace
import unittest

SPEC = importlib.util.spec_from_file_location(
    "public_text", Path(__file__).resolve().parents[1] / "assets/public_text.py"
)
adapter = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(adapter)
CANARY = "SYNTHETIC_NONPUBLIC_CREDENTIAL_CANARY"


def part(text=None, thought=None):
    return SimpleNamespace(text=text, thought=thought)


class Event:
    def __init__(self, parts, final=True):
        self.content = SimpleNamespace(parts=parts)
        self.final = final
        self.raw_auth_credential = CANARY
        self.actions = {"state_delta": {"access_token": CANARY}}
        self.headers = {"Authorization": CANARY}

    def is_final_response(self):
        return self.final

    def model_dump(self):
        raise AssertionError("Full event serialisation must never be used")


class ProjectionTests(unittest.TestCase):
    def test_nonpublic_canaries_excluded_and_public_text_preserved(self):
        event = Event([part(CANARY, True), part("Public "), part("answer.")])
        self.assertEqual(adapter.project_final_text(event), "Public answer.")

    def test_nonfinal_function_or_auth_event_not_forwarded(self):
        self.assertIsNone(adapter.project_final_text(Event([part(CANARY)], False)))

    def test_malformed_part_fails_without_object_dump(self):
        class Bad:
            def __repr__(self):
                raise AssertionError("Must not represent rejected data")
        with self.assertRaises(adapter.PublicProjectionError) as error:
            adapter.project_final_text(Event([Bad()]))
        self.assertNotIn(CANARY, str(error.exception))

    def test_size_and_type_limits_fail_closed(self):
        for kwargs in [{"max_chars": 2}, {"max_chars": True}, {"max_parts": 0}]:
            with self.assertRaises(adapter.PublicProjectionError):
                adapter.project_final_text(Event([part("answer")]), **kwargs)
        with self.assertRaises(adapter.PublicProjectionError):
            adapter.project_final_text(Event([part("a"), part("b")]), max_parts=1)
        for p in [part(123), part("a", "false")]:
            with self.assertRaises(adapter.PublicProjectionError):
                adapter.project_final_text(Event([p]))

    def test_allowed_text_is_not_a_secret_detection_boundary(self):
        # Explicit limit: upstream exclusion/content policy is still required.
        self.assertEqual(adapter.project_final_text(Event([part(CANARY)])), CANARY)

    def test_current_adk_event_shape_when_sdk_available(self):
        try:
            from google.adk.events import Event as AdkEvent, EventActions
            from google.genai import types
        except ImportError:
            self.skipTest("Optional ADK shape check; SDK is not a package dependency")
        event = AdkEvent(
            author="agent", content=types.Content(role="model", parts=[
                types.Part(text=CANARY, thought=True), types.Part(text="Visible")]),
            actions=EventActions(state_delta={"refresh_token": CANARY}),
        )
        self.assertEqual(adapter.project_final_text(event), "Visible")


class CollectionTests(unittest.IsolatedAsyncioTestCase):
    async def test_later_events_consumed_and_second_invocation_is_independent(self):
        visited = []
        async def stream():
            for i, event in enumerate([Event([part("first")]),
                                       Event([part(CANARY)], False),
                                       Event([part("last")])]):
                visited.append(i)
                yield event
        self.assertEqual(await adapter.collect_final_text(stream()), "last")
        self.assertEqual(visited, [0, 1, 2])
        self.assertEqual(await adapter.collect_final_text(stream()), "last")
        self.assertEqual(visited, [0, 1, 2, 0, 1, 2])

    async def test_event_budget_stops_consumption(self):
        seen = []
        async def stream():
            for i in range(10):
                seen.append(i)
                yield Event([part("answer")])
        with self.assertRaises(adapter.PublicProjectionError):
            await adapter.collect_final_text(stream(), max_events=2)
        self.assertEqual(seen, [0, 1, 2])

    async def test_stalled_stream_has_safe_timeout(self):
        async def stream():
            await asyncio.sleep(1)
            yield Event([part(CANARY)])
        with self.assertRaises(adapter.PublicProjectionError) as error:
            await adapter.collect_final_text(stream(), timeout_seconds=0.01)
        self.assertEqual(str(error.exception), "Public event collection failed.")

    async def test_invalid_collection_limits(self):
        async def stream():
            yield Event([part("a")])
        for kwargs in [{"max_events": 0}, {"timeout_seconds": float("nan")},
                       {"timeout_seconds": float("inf")}, {"timeout_seconds": True}]:
            with self.assertRaises(adapter.PublicProjectionError):
                await adapter.collect_final_text(stream(), **kwargs)


if __name__ == "__main__":
    unittest.main()
