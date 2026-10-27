"""G03: sessions persist in a database and a down store gives 503.

Needs the SDK (google-adk, fastapi, aiosqlite); skipped where it is absent.
"""
import asyncio
import os
import tempfile
import unittest

from app.settings import Settings

try:
    os.environ.setdefault("SESSION_DB_URL", "sqlite+aiosqlite:///" + os.path.join(tempfile.mkdtemp(), "boot.db"))
    from fastapi.testclient import TestClient
    from google.adk.sessions import DatabaseSessionService
    from sqlalchemy.exc import OperationalError

    from app import server
    HAVE_SDK = True
except ImportError:
    HAVE_SDK = False


class SettingsTests(unittest.TestCase):
    def test_session_url_comes_from_env(self):
        os.environ["SESSION_DB_URL"] = "postgresql+asyncpg://u:p@10.0.0.3/sessions"
        try:
            self.assertEqual(Settings.from_env().session_db_url, "postgresql+asyncpg://u:p@10.0.0.3/sessions")
        finally:
            os.environ.pop("SESSION_DB_URL")

    def test_default_is_sqlite(self):
        os.environ.pop("SESSION_DB_URL", None)
        self.assertTrue(Settings.from_env().session_db_url.startswith("sqlite"))


@unittest.skipUnless(HAVE_SDK, "google-adk not installed")
class SessionPersistenceTests(unittest.TestCase):
    def test_session_survives_a_new_service_on_same_database(self):
        # A new service object stands in for a restarted instance (A1, local tier).
        url = "sqlite+aiosqlite:///" + os.path.join(tempfile.mkdtemp(), "s.db")

        async def go():
            first = DatabaseSessionService(db_url=url)
            s = await first.create_session(app_name="support", user_id="cust-ana")
            second = DatabaseSessionService(db_url=url)
            return s.id, await second.get_session(app_name="support", user_id="cust-ana", session_id=s.id)

        sid, again = asyncio.run(go())
        self.assertIsNotNone(again)
        self.assertEqual(again.id, sid)


@unittest.skipUnless(HAVE_SDK, "google-adk not installed")
class UnreachableStoreTests(unittest.TestCase):
    def setUp(self):
        from app.auth import Principal
        server.app.dependency_overrides[server.current_principal] = lambda: Principal(
            user_id="cust-ana", email="ana@example.com")
        self.original = server.session_service

    def tearDown(self):
        server.session_service = self.original
        server.app.dependency_overrides.clear()

    def test_unreachable_database_is_503_and_creates_nothing(self):
        created = []

        class Down:
            async def get_session(self, **kw):
                raise OperationalError("select", {}, OSError("connection refused"))

            async def create_session(self, **kw):
                created.append(kw)

        server.session_service = Down()
        r = TestClient(server.app).post("/api/chat", json={"session_id": "x", "message": "hi"})
        self.assertEqual(r.status_code, 503)
        self.assertNotIn("session_id", r.json())
        self.assertEqual(created, [])


if __name__ == "__main__":
    unittest.main()
