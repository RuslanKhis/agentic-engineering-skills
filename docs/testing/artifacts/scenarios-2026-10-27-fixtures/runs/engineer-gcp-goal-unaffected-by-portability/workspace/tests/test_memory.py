import unittest

from google.adk.events import Event
from google.adk.memory import InMemoryMemoryService
from google.adk.sessions import Session
from google.genai import types

from claims import memory

APP = "coastline_claims"


def session(user_id, text, sid="s1"):
    event = Event(author="user", content=types.Content(role="user", parts=[types.Part(text=text)]))
    return Session(id=sid, app_name=APP, user_id=user_id, events=[event])


class FakeCallbackContext:
    """Stands in for the ADK callback context; writes through a real InMemoryMemoryService."""

    def __init__(self, service, user_id, text):
        self.service, self.user_id, self.session = service, user_id, session(user_id, text)

    async def add_session_to_memory(self):
        await self.service.add_session_to_memory(self.session)


class MemoryWriteBackTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.service = InMemoryMemoryService()
        memory.use_memory_settings(memory.DictMemorySettings(declined={"ph-3"}))

    def tearDown(self):
        memory.use_memory_settings(None)

    async def recall(self, user_id, query):
        response = await self.service.search_memory(app_name=APP, user_id=user_id, query=query)
        return response.memories

    async def test_a1_returning_policyholder_gets_earlier_facts(self):
        await memory.write_session_to_memory(FakeCallbackContext(self.service, "ph-1", "kitchen ceiling collapsed"))
        self.assertTrue(await self.recall("ph-1", "kitchen ceiling"))

    async def test_a2_other_policyholder_gets_nothing(self):
        await memory.write_session_to_memory(FakeCallbackContext(self.service, "ph-1", "kitchen ceiling collapsed"))
        self.assertEqual(await self.recall("ph-2", "kitchen ceiling"), [])

    async def test_a3_declined_policyholder_writes_nothing(self):
        await memory.write_session_to_memory(FakeCallbackContext(self.service, "ph-3", "kitchen ceiling collapsed"))
        self.assertEqual(await self.recall("ph-3", "kitchen ceiling"), [])
        self.assertEqual(self.service._session_events, {})

    async def test_unconfigured_settings_write_nothing(self):
        memory.use_memory_settings(None)
        await memory.write_session_to_memory(FakeCallbackContext(self.service, "ph-1", "kitchen ceiling collapsed"))
        self.assertEqual(await self.recall("ph-1", "kitchen ceiling"), [])

    async def test_failed_setting_lookup_writes_nothing_and_does_not_raise(self):
        class Broken:
            def memory_declined(self, user_id):
                raise RuntimeError("firestore down")

        memory.use_memory_settings(Broken())
        await memory.write_session_to_memory(FakeCallbackContext(self.service, "ph-1", "kitchen ceiling collapsed"))
        self.assertEqual(await self.recall("ph-1", "kitchen ceiling"), [])


if __name__ == "__main__":
    unittest.main()
