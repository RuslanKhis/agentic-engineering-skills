"""Offline ADK session storage, lifecycle and native tracing contracts.

SQLite exercises real database behaviour; the managed-service API is doubled at
its client boundary. No PostgreSQL server, provider, GKE workload or external
exporter is contacted. These checks do not establish production persistence,
pool sizing, migrations, complete-turn ordering or whole-application privacy.
"""

import asyncio
from contextlib import asynccontextmanager
from datetime import datetime, timezone
import importlib.metadata
import json
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import AsyncMock, patch


class GkeSessionContract(unittest.TestCase):
    def setUp(self):
        try:
            version = importlib.metadata.version("google-adk")
        except importlib.metadata.PackageNotFoundError:
            self.skipTest("ADK is absent; this real-framework contract was not run")
        if version != "2.8.0":
            self.skipTest("This contract requires ADK 2.8.0; preserve target pins")
        for target in (
            "socket.socket.connect", "socket.socket.connect_ex",
            "socket.socket.sendto", "socket.create_connection",
            "socket.getaddrinfo", "socket.gethostbyname",
            "socket.gethostbyname_ex", "socket.gethostbyaddr",
        ):
            guard = patch(target, side_effect=AssertionError("Network is prohibited"))
            guard.start()
            self.addCleanup(guard.stop)

    def require_distribution(self, name):
        try:
            importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError:
            self.skipTest(f"{name} is absent; preserve target dependencies")

    def require_database_dependencies(self):
        # Core ADK includes aiosqlite but keeps SQLAlchemy in its optional db
        # extra. Its async engine also needs greenlet, which may require the
        # SQLAlchemy asyncio extra on this platform.
        self.require_distribution("sqlalchemy")
        self.require_distribution("aiosqlite")
        self.require_distribution("greenlet")

    def database_run(self, exercise):
        from google.adk.sessions import DatabaseSessionService

        async def run():
            with tempfile.TemporaryDirectory(prefix="offline-gke-session-") as directory:
                service = DatabaseSessionService(
                    db_url=f"sqlite+aiosqlite:///{Path(directory) / 'sessions.db'}"
                )
                try:
                    return await exercise(service)
                finally:
                    await service.close()

        return asyncio.run(run())

    async def seed_database(self, service):
        from google.adk.events import Event
        from google.genai import types

        session = await service.create_session(
            app_name="offline_gke_contract", user_id="synthetic-owner",
            session_id="s-history", state={"retained_fact": "old synthetic fact"},
        )
        parts = [
            types.Part(text="OLD_HISTORY_MARKER"),
            types.Part(function_call=types.FunctionCall(
                name="lookup", id="call-1", args={"key": "synthetic"},
            )),
            types.Part(function_response=types.FunctionResponse(
                name="lookup", id="call-1", response={"status": "success"},
            )),
            types.Part(text="The synthetic lookup completed."),
        ]
        for index, part in enumerate(parts):
            await service.append_event(session=session, event=Event(
                id=f"event-{index}", invocation_id="invocation-1",
                author="user" if index == 0 else "offline_agent",
                timestamp=session.last_update_time + 1,
                content=types.Content(
                    role="user" if index in (0, 2) else "model", parts=[part],
                ),
            ))
        return {
            "app_name": session.app_name, "user_id": session.user_id,
            "session_id": session.id,
        }

    def test_database_limits_events_in_sql_without_deleting_history_or_state(self):
        self.require_database_dependencies()
        from google.adk.sessions.base_session_service import GetSessionConfig
        from sqlalchemy import event as sqlalchemy_event

        async def exercise(service):
            identifiers = await self.seed_database(service)
            statements = []

            def capture(connection, cursor, statement, parameters, context, executemany):
                if "from events" in statement.lower():
                    statements.append((statement, parameters))

            sqlalchemy_event.listen(service.db_engine.sync_engine, "before_cursor_execute", capture)
            try:
                recent = await service.get_session(
                    **identifiers, config=GetSessionConfig(num_recent_events=2),
                )
                self.assertEqual([item.id for item in recent.events], ["event-2", "event-3"])
                self.assertEqual(len(statements), 1)
                self.assertIn("limit", statements[0][0].lower())
                self.assertEqual(statements[0][1][-2:], (2, 0))
                # An event window can retain a tool result without its call. It
                # does not promise complete turns or semantically safe context.
                self.assertEqual(recent.events[0].get_function_responses()[0].id, "call-1")
                self.assertFalse(any(item.get_function_calls() for item in recent.events))
                self.assertEqual(recent.state["retained_fact"], "old synthetic fact")
                full = await service.get_session(**identifiers)
                self.assertEqual([item.id for item in full.events], [f"event-{i}" for i in range(4)])
                self.assertEqual(full.events[0].content.parts[0].text, "OLD_HISTORY_MARKER")
                self.assertFalse(any(item.actions.compaction for item in full.events))
            finally:
                sqlalchemy_event.remove(service.db_engine.sync_engine, "before_cursor_execute", capture)

        self.database_run(exercise)

    def test_database_zero_event_window_skips_event_query_but_keeps_metadata(self):
        self.require_database_dependencies()
        from google.adk.sessions.base_session_service import GetSessionConfig
        from sqlalchemy import event as sqlalchemy_event

        async def exercise(service):
            identifiers = await self.seed_database(service)
            event_queries = []

            def capture(connection, cursor, statement, parameters, context, executemany):
                if "from events" in statement.lower():
                    event_queries.append(statement)

            sqlalchemy_event.listen(service.db_engine.sync_engine, "before_cursor_execute", capture)
            try:
                metadata = await service.get_session(
                    **identifiers, config=GetSessionConfig(num_recent_events=0),
                )
                self.assertEqual(metadata.events, [])
                self.assertEqual(metadata.id, identifiers["session_id"])
                self.assertEqual(metadata.state["retained_fact"], "old synthetic fact")
                self.assertEqual(event_queries, [])
            finally:
                sqlalchemy_event.remove(service.db_engine.sync_engine, "before_cursor_execute", capture)

        self.database_run(exercise)

    def test_runner_close_flushes_and_service_close_disposes_owned_engine(self):
        self.require_database_dependencies()
        from google.adk import Agent, Runner
        from google.adk.apps import App
        from google.adk.sessions import DatabaseSessionService
        from sqlalchemy import event as sqlalchemy_event

        async def run():
            with tempfile.TemporaryDirectory(prefix="offline-gke-close-") as directory:
                disposals = []
                async with DatabaseSessionService(
                    db_url=f"sqlite+aiosqlite:///{Path(directory) / 'sessions.db'}"
                ) as service:
                    await service.prepare_tables()
                    sqlalchemy_event.listen(
                        service.db_engine.sync_engine, "engine_disposed", disposals.append,
                    )
                    runner = Runner(
                        app=App(name="offline_gke_contract", root_agent=Agent(
                            name="offline_agent", model="unused-offline-model",
                        )),
                        session_service=service,
                    )
                    with patch.object(service, "flush", new=AsyncMock(wraps=service.flush)) as flush:
                        await runner.close()
                        flush.assert_awaited_once_with()
                    self.assertEqual(disposals, [])
                self.assertEqual(disposals, [service.db_engine.sync_engine])

        asyncio.run(run())

    def test_managed_positive_limit_reads_full_api_iterator_then_slices(self):
        self.exercise_managed_history(limit=2, expected_ids=["event-2", "event-3"])

    def test_managed_zero_limit_skips_event_listing(self):
        self.exercise_managed_history(limit=0, expected_ids=[])

    def exercise_managed_history(self, *, limit, expected_ids):
        self.require_distribution("google-cloud-aiplatform")
        from google.adk.events import Event
        from google.adk.sessions.base_session_service import GetSessionConfig
        from google.adk.sessions.vertex_ai_session_service import VertexAiSessionService
        from google.genai import types

        iterated = []

        async def events():
            for index in range(4):
                iterated.append(index)
                item = Event(
                    id=f"event-{index}", author="offline_agent",
                    invocation_id="invocation-1", timestamp=1000 + index,
                    content=types.Content(role="model", parts=[types.Part(text=f"fact-{index}")]),
                )
                yield SimpleNamespace(
                    name=f"reasoningEngines/123/sessions/s-history/events/{item.id}",
                    author=item.author, invocation_id=item.invocation_id,
                    timestamp=datetime.fromtimestamp(item.timestamp, tz=timezone.utc),
                    raw_event=item.model_dump(mode="json", exclude_none=True),
                )

        sessions = SimpleNamespace(
            get=AsyncMock(return_value=SimpleNamespace(
                user_id="synthetic-owner", update_time=datetime.fromtimestamp(1004, tz=timezone.utc),
                session_state={"retained_fact": "old synthetic fact"},
            )),
            events=SimpleNamespace(list=AsyncMock(return_value=events())),
        )

        @asynccontextmanager
        async def fake_client():
            yield SimpleNamespace(agent_engines=SimpleNamespace(sessions=sessions))

        service = VertexAiSessionService(
            project="synthetic-project", location="us-central1", agent_engine_id="123",
        )

        async def run():
            with patch.object(service, "_get_api_client", side_effect=fake_client):
                return await service.get_session(
                    app_name="offline_gke_contract", user_id="synthetic-owner",
                    session_id="s-history", config=GetSessionConfig(num_recent_events=limit),
                )

        result = asyncio.run(run())
        target = "reasoningEngines/123/sessions/s-history"
        sessions.get.assert_awaited_once_with(name=target)
        self.assertEqual([item.id for item in result.events], expected_ids)
        self.assertEqual(result.state["retained_fact"], "old synthetic fact")
        if limit:
            sessions.events.list.assert_awaited_once_with(name=target)
            self.assertEqual(iterated, [0, 1, 2, 3])
        else:
            sessions.events.list.assert_not_awaited()
            self.assertEqual(iterated, [])

    def test_native_adk_capture_flags_still_export_raw_conversation_id(self):
        self.require_distribution("opentelemetry-sdk")
        from google.adk.telemetry.tracing import trace_agent_invocation
        from opentelemetry.sdk.resources import Resource
        from opentelemetry.sdk.trace import TracerProvider
        from opentelemetry.sdk.trace.export import SimpleSpanProcessor
        from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter
        from opentelemetry.sdk.trace.sampling import ALWAYS_ON

        marker = "SYNTHETIC_PRIVATE_NATIVE_SESSION_91"
        exporter = InMemorySpanExporter()
        provider = TracerProvider(
            resource=Resource({"service.name": "offline-native-adk-contract"}),
            sampler=ALWAYS_ON, shutdown_on_exit=False,
        )
        provider.add_span_processor(SimpleSpanProcessor(exporter))
        try:
            with patch.dict("os.environ", {
                "ADK_CAPTURE_MESSAGE_CONTENT_IN_SPANS": "false",
                "OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT": "false",
            }):
                with provider.get_tracer("offline-native-adk-contract").start_as_current_span("invoke_agent") as span:
                    trace_agent_invocation(
                        span,
                        SimpleNamespace(name="offline_agent", description="Synthetic contract"),
                        SimpleNamespace(session=SimpleNamespace(id=marker)),
                    )
            spans = exporter.get_finished_spans()
            self.assertEqual(len(spans), 1)
            exported = json.loads(spans[0].to_json())
            self.assertEqual(exported["attributes"]["gen_ai.conversation.id"], marker)
            # This is a negative control using the actual native ADK helper. It
            # proves flags alone are insufficient, not that a filter exists.
            self.assertIn(marker, spans[0].to_json())
        finally:
            provider.shutdown()


if __name__ == "__main__":
    unittest.main()
