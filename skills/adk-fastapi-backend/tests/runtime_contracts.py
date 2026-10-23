"""Optional real-SDK contract tests for the facts this skill's recipe depends on; no provider access.

Run explicitly, from the skill directory, in an environment with the versions
recorded in references/compatibility.md:

    python -m unittest discover -s tests -p runtime_contracts.py -v

Nothing is installed or upgraded. The model is replaced by a scripted BaseLlm,
so no test calls Gemini.
"""

import asyncio
from importlib import metadata
from pathlib import Path
import sys
import tempfile
import unittest

EXPECTED = {"google-adk": "2.12.0", "fastapi": "0.141.1"}
for package, version in EXPECTED.items():
    if metadata.version(package) != version:
        raise RuntimeError(f"These contracts were recorded on {package}=={version}; adapt and re-run for other pins.")

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.testclient import TestClient
from google.adk.agents import LlmAgent
from google.adk.models.base_llm import BaseLlm
from google.adk.models.llm_response import LlmResponse
from google.adk.runners import Runner
from google.adk.sessions import DatabaseSessionService, InMemorySessionService
from google.genai import types

ADK_TABLES = {"sessions", "events", "app_states", "user_states", "adk_internal_metadata"}
BROWSER = {"accept": "text/html,application/xhtml+xml"}


class ScriptedModel(BaseLlm):
    model: str = "scripted"
    calls: int = 0

    async def generate_content_async(self, llm_request, stream=False):
        self.calls += 1
        yield LlmResponse(content=types.Content(role="model", parts=[types.Part(text="scripted")]))


class FrontendFallback(unittest.TestCase):
    """app.frontend() is low priority and answers browser navigation with the HTML shell."""

    def app(self, root, extra=None):
        Path(root, "index.html").write_text("<!doctype html><title>shell</title>")
        for name, text in (extra or {}).items():
            Path(root, name).write_text(text)
        app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)

        @app.get("/api/items")
        def items() -> list[str]:
            return []
        app.frontend("/", directory=root)
        return TestClient(app)

    def test_shell_for_navigation_including_api_and_docs_paths(self):
        with tempfile.TemporaryDirectory() as root:
            client = self.app(root)
            for path in ("/chat/1", "/api/unknown", "/docs", "/openapi.json"):
                response = client.get(path, headers=BROWSER)
                self.assertEqual((response.status_code, response.text[:15]), (200, "<!doctype html>"), path)
                self.assertEqual(client.get(path, headers={"accept": "application/json"}).status_code, 404, path)
            self.assertEqual(client.post("/chat/1").status_code, 404)
            self.assertEqual(client.get("/api/items").json(), [])

    def test_a_404_page_disables_the_shell_fallback(self):
        with tempfile.TemporaryDirectory() as root:
            client = self.app(root, {"404.html": "missing"})
            self.assertEqual(client.get("/chat/1", headers=BROWSER).status_code, 404)

    def test_frontend_has_no_dependencies_parameter(self):
        import inspect
        self.assertNotIn("dependencies", inspect.signature(FastAPI.frontend).parameters)


class AdkServerIsOpen(unittest.TestCase):
    """ADK's own API server authenticates no caller: user_id is whatever the client sends."""

    def test_any_client_reads_and_creates_any_users_sessions(self):
        from google.adk.cli.fast_api import get_fast_api_app
        with tempfile.TemporaryDirectory() as agents:
            package = Path(agents, "helper")
            package.mkdir()
            (package / "__init__.py").write_text("from . import agent\n")
            (package / "agent.py").write_text("from google.adk.agents import LlmAgent\n"
                                              "root_agent = LlmAgent(name='helper', model='gemini-2.5-flash')\n")
            sys.path.insert(0, agents)
            try:
                app = get_fast_api_app(agents_dir=agents, web=False)
                with TestClient(app) as client:
                    created = client.post("/apps/helper/users/bob/sessions", json={})
                    self.assertEqual(created.status_code, 200)
                    listed = client.get("/apps/helper/users/bob/sessions")
                    self.assertEqual([s["id"] for s in listed.json()], [created.json()["id"]])
            finally:
                sys.path.remove(agents)


class PrincipalAroundRunner(unittest.TestCase):
    """A fail-closed dependency in front of an in-process Runner: rejected calls never reach the model."""

    def test_fail_closed_and_principal_scoped_sessions(self):
        model = ScriptedModel()
        service = InMemorySessionService()
        runner = Runner(app_name="a", agent=LlmAgent(name="a", model=model), session_service=service)
        app = FastAPI()
        app.state.verifier = None

        async def principal(request: Request) -> str:
            if app.state.verifier is None:
                raise HTTPException(401)
            return app.state.verifier(request)

        @app.post("/api/runs/{session_id}")
        async def run(session_id: str, body: dict, user: str = Depends(principal)) -> dict:
            if await service.get_session(app_name="a", user_id=user, session_id=session_id) is None:
                raise HTTPException(404, "not found")
            async for _ in runner.run_async(user_id=user, session_id=session_id,
                                            new_message=types.Content(role="user", parts=[types.Part(text="hi")])):
                pass
            return {}

        with TestClient(app) as client:
            self.assertEqual(client.post("/api/runs/x", json={"user_id": "bob"}).status_code, 401)
            app.state.verifier = lambda request: request.headers["x-user"]
            session = asyncio.run(service.create_session(app_name="a", user_id="alice"))
            other = client.post(f"/api/runs/{session.id}", headers={"x-user": "bob"}, json={"user_id": "alice"})
            self.assertEqual(other.status_code, 404)
            self.assertEqual(model.calls, 0)
            self.assertEqual(client.post(f"/api/runs/{session.id}", headers={"x-user": "alice"}, json={}).status_code, 200)
            self.assertEqual(model.calls, 1)


class AdkTablesBesideAppTables(unittest.TestCase):
    def test_database_session_service_creates_five_tables_that_autogenerate_would_drop(self):
        try:
            from alembic.autogenerate import compare_metadata
            from alembic.migration import MigrationContext
            import sqlalchemy as sa
        except ImportError as exc:
            self.skipTest(f"alembic or sqlalchemy absent: {exc}")
        with tempfile.TemporaryDirectory() as root:
            path = Path(root, "shared.db")

            async def create():
                service = DatabaseSessionService(f"sqlite+aiosqlite:///{path}")
                await service.create_session(app_name="a", user_id="u")
            asyncio.run(create())
            engine = sa.create_engine(f"sqlite:///{path}")
            self.assertEqual(set(sa.inspect(engine).get_table_names()), ADK_TABLES)
            app_metadata = sa.MetaData()
            sa.Table("app_documents", app_metadata, sa.Column("id", sa.String(36), primary_key=True))

            def keep(obj, name, type_, reflected, compare_to):
                return not (type_ == "table" and name in ADK_TABLES)
            with engine.connect() as conn:
                bare = compare_metadata(MigrationContext.configure(conn), app_metadata)
                filtered = compare_metadata(MigrationContext.configure(conn, opts={"include_object": keep}),
                                            app_metadata)
            self.assertEqual({d[1].name for d in bare if d[0] == "remove_table"}, ADK_TABLES)
            self.assertEqual([d[0] for d in filtered], ["add_table"])


class FirebaseErrorOrder(unittest.TestCase):
    def test_expired_and_revoked_are_invalid_token_subclasses(self):
        try:
            from firebase_admin import auth
        except ImportError as exc:
            self.skipTest(f"firebase-admin absent: {exc}")
        self.assertTrue(issubclass(auth.ExpiredIdTokenError, auth.InvalidIdTokenError))
        self.assertTrue(issubclass(auth.RevokedIdTokenError, auth.InvalidIdTokenError))
        self.assertFalse(issubclass(auth.CertificateFetchError, auth.InvalidIdTokenError))


class OpenTelemetryCap(unittest.TestCase):
    def test_adk_caps_opentelemetry_below_what_fastapi_0_142_needs(self):
        requirement = [r for r in metadata.requires("google-adk") if r.startswith("opentelemetry-api")]
        self.assertEqual(requirement, ["opentelemetry-api>=1.39,<=1.42.1"])


if __name__ == "__main__":
    unittest.main()
