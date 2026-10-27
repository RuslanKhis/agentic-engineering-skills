import asyncio
import unittest
from types import SimpleNamespace

try:
    import google.adk  # noqa: F401
    HAVE_ADK = True
except ImportError:
    HAVE_ADK = False


class FakeMem0Client:
    def __init__(self):
        self.added = []

    def add(self, messages, **kwargs):
        self.added.append((messages, kwargs))
        return {"results": [{"id": "m1", "event": "ADD"}]}

    def search(self, query, **kwargs):
        return {"results": [{"id": "m1", "memory": "Lives at 12 Alder Close", "created_at": "2026-09-01"}]}


def part(text):
    return SimpleNamespace(text=text)


def event(author, text):
    return SimpleNamespace(author=author, content=SimpleNamespace(parts=[part(text)]))


@unittest.skipUnless(HAVE_ADK, "google-adk is not installed")
class Mem0ServiceTests(unittest.TestCase):
    def test_session_is_written_with_user_id(self):
        from homeline.memory.mem0_service import Mem0MemoryService

        client = FakeMem0Client()
        service = Mem0MemoryService(api_key="test", client=client)
        session = SimpleNamespace(app_name="homeline", user_id="u-1", id="s-1",
                                  events=[event("user", "I live at 12 Alder Close")])
        asyncio.run(service.add_session_to_memory(session))
        self.assertEqual(client.added[0][1]["user_id"], "u-1")

    def test_search_returns_memories(self):
        from homeline.memory.mem0_service import Mem0MemoryService

        service = Mem0MemoryService(api_key="test", client=FakeMem0Client())
        response = asyncio.run(service.search_memory(app_name="homeline", user_id="u-1", query="address"))
        self.assertEqual(len(response.memories), 1)


if __name__ == "__main__":
    unittest.main()
