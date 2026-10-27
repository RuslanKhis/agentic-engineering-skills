import asyncio
import unittest
from types import SimpleNamespace

try:
    import google.adk  # noqa: F401
    HAVE_ADK = True
except ImportError:
    HAVE_ADK = False


class FakeMem0Client:
    """Behaves like the Platform where it matters here.

    * ``user_id`` / ``app_id`` passed to ``add`` are entity fields; ``metadata`` is not
      filterable, so a filter on a field only present in metadata matches nothing.
    * A message containing "moved to" supersedes the user's earlier memories; superseded
      records are returned only when ``latest_only`` is not set.
    * Deleted users' records are gone from ``get_all``.
    """

    def __init__(self):
        self.records = []
        self.added = []
        self.search_kwargs = []
        self.fail = None  # method name -> exception to raise
        self.delete_does_nothing = False

    def _maybe_fail(self, name):
        if self.fail and self.fail[0] == name:
            raise self.fail[1]

    def add(self, messages, **kwargs):
        self._maybe_fail("add")
        self.added.append((messages, kwargs))
        text = messages[-1]["content"]
        if "moved to" in text:
            for r in self.records:
                if r["user_id"] == kwargs.get("user_id"):
                    r["superseded"] = True
        self.records.append({
            "id": f"m{len(self.records) + 1}",
            "memory": text,
            "user_id": kwargs.get("user_id"),
            "app_id": kwargs.get("app_id"),  # entity field only if passed as such
            "metadata": kwargs.get("metadata", {}),
            "superseded": False,
            "created_at": "2026-09-01",
        })
        return {"results": [{"event": "ADD"}]}

    @staticmethod
    def _matches(record, filters):
        return all(record.get(k) == v for clause in filters["AND"] for k, v in clause.items())

    def search(self, query, **kwargs):
        self._maybe_fail("search")
        self.search_kwargs.append(kwargs)
        out = [r for r in self.records
               if self._matches(r, kwargs["filters"])
               and not (kwargs.get("latest_only") and r["superseded"])]
        return {"results": out[: kwargs.get("top_k", 10)]}

    def delete_all(self, **kwargs):
        self._maybe_fail("delete_all")
        if not self.delete_does_nothing:
            self.records = [r for r in self.records if r["user_id"] != kwargs["user_id"]]

    def get_all(self, **kwargs):
        return {"results": [r for r in self.records if self._matches(r, kwargs["filters"])]}


def part(text):
    return SimpleNamespace(text=text)


def event(author, text):
    return SimpleNamespace(author=author, content=SimpleNamespace(parts=[part(text)]))


def session(user_id, text, sid="s-1"):
    return SimpleNamespace(app_name="homeline", user_id=user_id, id=sid, events=[event("user", text)])


def run(coro):
    return asyncio.run(coro)


@unittest.skipUnless(HAVE_ADK, "google-adk is not installed")
class Mem0ServiceTests(unittest.TestCase):
    def setUp(self):
        from homeline.memory.mem0_service import Mem0MemoryService, Tombstones

        self.client = FakeMem0Client()
        self.service = Mem0MemoryService(api_key="test", client=self.client, tombstones=Tombstones())

    def texts(self, user="u-1", app="homeline", query="address"):
        response = run(self.service.search_memory(app_name=app, user_id=user, query=query))
        return [m.content.parts[0].text for m in response.memories]

    def test_write_then_read_under_one_scope(self):
        run(self.service.add_session_to_memory(session("u-1", "My door code is 4411")))
        self.assertEqual(self.texts(), ["My door code is 4411"])

    def test_app_id_is_an_entity_field_not_only_metadata(self):
        run(self.service.add_session_to_memory(session("u-1", "hello")))
        self.assertEqual(self.client.added[0][1]["app_id"], "homeline")
        self.assertEqual(self.client.added[0][1]["user_id"], "u-1")

    def test_other_user_and_other_app_see_nothing(self):
        run(self.service.add_session_to_memory(session("u-1", "My door code is 4411")))
        self.assertEqual(self.texts(user="u-2"), [])
        self.assertEqual(self.texts(app="other-app"), [])

    def test_moved_address_returns_only_the_new_one(self):
        run(self.service.add_session_to_memory(session("u-1", "I live at 12 Alder Close")))
        run(self.service.add_session_to_memory(session("u-1", "I moved to 7 Quarry Lane", "s-2")))
        self.assertEqual(self.texts(), ["I moved to 7 Quarry Lane"])
        self.assertTrue(self.client.search_kwargs[-1]["latest_only"])

    def test_search_failure_raises_not_empty(self):
        from homeline.memory.mem0_service import Mem0MemoryError

        self.client.fail = ("search", RuntimeError("401"))
        with self.assertRaises(Mem0MemoryError):
            self.texts()
        self.assertEqual(self.service.search_failures, 1)

    def test_malformed_search_response_raises_not_empty(self):
        from homeline.memory.mem0_service import Mem0MemoryError

        self.client.search = lambda *a, **k: {"detail": "bad"}
        with self.assertRaises(Mem0MemoryError):
            self.texts()

    def test_write_failure_raises_and_is_counted(self):
        from homeline.memory.mem0_service import Mem0MemoryError

        self.client.fail = ("add", RuntimeError("503"))
        with self.assertRaises(Mem0MemoryError):
            run(self.service.add_session_to_memory(session("u-1", "hi")))
        self.assertEqual(self.service.write_failures, 1)

    def test_erase_removes_user_only_and_blocks_new_writes_and_reads(self):
        run(self.service.add_session_to_memory(session("u-1", "door code 4411")))
        run(self.service.add_session_to_memory(session("u-2", "door code 9999")))
        self.service.erase_user("u-1")
        self.assertEqual([r["user_id"] for r in self.client.records], ["u-2"])
        run(self.service.add_session_to_memory(session("u-1", "new fact", "s-3")))
        self.assertEqual([r["user_id"] for r in self.client.records], ["u-2"])
        self.assertEqual(self.texts(user="u-1"), [])
        self.assertEqual(self.texts(user="u-2"), ["door code 9999"])

    def test_erase_not_confirmed_raises_and_keeps_tombstone(self):
        from homeline.memory.mem0_service import Mem0MemoryError

        run(self.service.add_session_to_memory(session("u-1", "door code 4411")))
        self.client.delete_does_nothing = True
        with self.assertRaises(Mem0MemoryError):
            self.service.erase_user("u-1")
        self.assertIn("u-1", self.service.tombstones)

    def test_erase_provider_failure_raises(self):
        from homeline.memory.mem0_service import Mem0MemoryError

        self.client.fail = ("delete_all", RuntimeError("500"))
        with self.assertRaises(Mem0MemoryError):
            self.service.erase_user("u-1")
        self.assertIn("u-1", self.service.tombstones)

    def test_tombstone_survives_restart(self):
        import os
        import tempfile

        from homeline.memory.mem0_service import Tombstones

        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "t.json")
            Tombstones(path).add("u-1")
            self.assertIn("u-1", Tombstones(path))
            self.assertNotIn("u-2", Tombstones(path))


@unittest.skipUnless(HAVE_ADK, "google-adk is not installed")
class ErasureTests(unittest.TestCase):
    def test_erases_memories_and_sessions(self):
        from homeline.memory.erasure import erase_user_data
        from homeline.memory.mem0_service import Mem0MemoryService, Tombstones

        class Sessions:
            def __init__(self):
                self.rows = {("homeline", "u-1"): ["a", "b"], ("homeline", "u-2"): ["c"]}

            async def list_sessions(self, *, app_name, user_id):
                return SimpleNamespace(sessions=[SimpleNamespace(id=i) for i in self.rows[(app_name, user_id)]])

            async def delete_session(self, *, app_name, user_id, session_id):
                self.rows[(app_name, user_id)].remove(session_id)

        client = FakeMem0Client()
        service = Mem0MemoryService(api_key="t", client=client, tombstones=Tombstones())
        run(service.add_session_to_memory(session("u-1", "door code 4411")))
        sessions = Sessions()
        result = run(erase_user_data(memory_service=service, session_service=sessions,
                                     app_name="homeline", user_id="u-1"))
        self.assertEqual(result, {"memories": "deleted", "sessions": "deleted", "sessions_deleted": 2})
        self.assertEqual(sessions.rows[("homeline", "u-2")], ["c"])

    def test_memory_failure_is_reported_not_hidden(self):
        from homeline.memory.erasure import erase_user_data
        from homeline.memory.mem0_service import Mem0MemoryService, Tombstones

        class Sessions:
            async def list_sessions(self, *, app_name, user_id):
                return SimpleNamespace(sessions=[])

        client = FakeMem0Client()
        client.fail = ("delete_all", RuntimeError("500"))
        service = Mem0MemoryService(api_key="t", client=client, tombstones=Tombstones())
        result = run(erase_user_data(memory_service=service, session_service=Sessions(),
                                     app_name="homeline", user_id="u-1"))
        self.assertEqual(result["memories"], "failed")


if __name__ == "__main__":
    unittest.main()
