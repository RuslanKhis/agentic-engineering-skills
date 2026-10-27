import os
import tempfile
import unittest
from unittest import mock

from app.auth import Principal
from app.sessions import SessionStoreUnavailable, store_guard
from app.settings import Settings


class SettingsTests(unittest.TestCase):
    def test_session_url_comes_from_environment(self):
        with mock.patch.dict(os.environ, {"SESSION_DB_URL": "postgresql+asyncpg://u:p@10.0.0.3/sessions"}):
            self.assertEqual(Settings.from_env().session_db_url, "postgresql+asyncpg://u:p@10.0.0.3/sessions")

    def test_default_is_a_local_sqlite_file(self):
        with mock.patch.dict(os.environ, {}, clear=True):
            self.assertTrue(Settings.from_env().session_db_url.startswith("sqlite"))


class StoreGuardTests(unittest.TestCase):
    def test_os_error_becomes_store_unavailable(self):
        with self.assertRaises(SessionStoreUnavailable):
            with store_guard():
                raise ConnectionRefusedError("db down")

    def test_unrelated_error_is_not_hidden(self):
        with self.assertRaises(ValueError):
            with store_guard():
                raise ValueError("bad argument")


class RestartTests(unittest.IsolatedAsyncioTestCase):
    """A second service object over the same database stands in for a restarted instance.

    This is a SQLite file, not Cloud SQL; the live restart check is owed (A1).
    """

    async def test_session_survives_a_new_service_instance(self):
        try:
            from app.sessions import build_session_service
            first = build_session_service(f"sqlite+aiosqlite:///{self._path()}")
        except ImportError as exc:
            self.skipTest(f"SDK or SQLite async driver absent: {exc}")
        session = await first.create_session(app_name="support", user_id="cust-ana", state={"topic": "refund"})
        second = build_session_service(f"sqlite+aiosqlite:///{self._path()}")
        again = await second.get_session(app_name="support", user_id="cust-ana", session_id=session.id)
        self.assertIsNotNone(again)
        self.assertEqual(again.state["topic"], "refund")

    async def test_another_user_does_not_get_the_session(self):
        try:
            from app.sessions import build_session_service
            svc = build_session_service(f"sqlite+aiosqlite:///{self._path()}")
        except ImportError as exc:
            self.skipTest(f"SDK or SQLite async driver absent: {exc}")
        session = await svc.create_session(app_name="support", user_id="cust-ana")
        other = await svc.get_session(app_name="support", user_id="cust-ben", session_id=session.id)
        self.assertIsNone(other)

    def _path(self):
        if not hasattr(self, "_dir"):
            self._dir = tempfile.TemporaryDirectory()
            self.addCleanup(self._dir.cleanup)
        return os.path.join(self._dir.name, "sessions.db")


class ChatRouteOutageTests(unittest.TestCase):
    """A2: the route returns 503 and creates no session when the store is down."""

    def setUp(self):
        try:
            from fastapi.testclient import TestClient
            from app import server
        except ImportError as exc:
            self.skipTest(f"SDK or web dependencies absent: {exc}")
        self.server = server
        self.client = TestClient(server.app)
        server.app.dependency_overrides[server.current_principal] = lambda: Principal(
            user_id="cust-ana", email="ana@example.com")
        self.addCleanup(server.app.dependency_overrides.clear)

    def test_unreachable_store_gives_503_and_no_session(self):
        created = []

        class DownService:
            async def get_session(self, **kw):
                raise ConnectionRefusedError("db down")

            async def create_session(self, **kw):
                created.append(kw)
                raise ConnectionRefusedError("db down")

        with mock.patch.object(self.server, "session_service", DownService()):
            resp = self.client.post("/api/chat", json={"message": "hi"})
        self.assertEqual(resp.status_code, 503)
        self.assertNotIn("session_id", resp.json())
        self.assertEqual(len(created), 1)  # attempted once, nothing stored


if __name__ == "__main__":
    unittest.main()
