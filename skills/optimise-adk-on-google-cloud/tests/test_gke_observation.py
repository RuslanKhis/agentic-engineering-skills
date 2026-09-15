"""Real in-memory OpenTelemetry export for the optional session span component.

No application or provider is contacted. These checks establish this custom
span's behaviour, not native ADK, HTTP instrumentation or production privacy.
"""

import asyncio
import importlib.metadata
import importlib.util
from pathlib import Path
import unittest
from unittest.mock import patch


MARKER = "SYNTHETIC_PRIVATE_SESSION_TRACE_91"
IDENTIFIERS = {
    "app_name": f"app-{MARKER}",
    "user_id": f"user-{MARKER}",
    "session_id": f"session-{MARKER}",
}


class SessionServiceDouble:
    def __init__(self, result=None, error=None):
        self.result = result
        self.error = error
        self.calls = []

    async def get_session(self, **identifiers):
        self.calls.append(identifiers)
        if self.error is not None:
            raise self.error
        return self.result


class GkeObservationContract(unittest.TestCase):
    def setUp(self):
        try:
            importlib.metadata.version("opentelemetry-sdk")
        except importlib.metadata.PackageNotFoundError:
            self.skipTest("OpenTelemetry SDK is absent; preserve target dependencies")

        from opentelemetry.sdk.resources import Resource
        from opentelemetry.sdk.trace import TracerProvider
        from opentelemetry.sdk.trace.export import SimpleSpanProcessor
        from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter
        from opentelemetry.sdk.trace.sampling import ALWAYS_ON

        for target in (
            "socket.socket.connect", "socket.socket.connect_ex",
            "socket.create_connection", "socket.getaddrinfo",
        ):
            guard = patch(target, side_effect=AssertionError("Network is prohibited"))
            guard.start()
            self.addCleanup(guard.stop)

        self.exporter = InMemorySpanExporter()
        self.provider = TracerProvider(
            resource=Resource({"service.name": "offline-session-observation"}),
            sampler=ALWAYS_ON,
            shutdown_on_exit=False,
        )
        self.provider.add_span_processor(SimpleSpanProcessor(self.exporter))
        self.addCleanup(self.provider.shutdown)
        self.tracer = self.provider.get_tracer("offline-session-observation")

        path = Path(__file__).resolve().parents[1] / "assets/session_observation.py"
        spec = importlib.util.spec_from_file_location("session_observation_under_test", path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        self.load_session = module.load_session_safely

    def call(self, service, store_kind="managed"):
        return asyncio.run(self.load_session(
            self.tracer, service, **IDENTIFIERS, store_kind=store_kind,
        ))

    def assert_safe_span(self, *, expected_attributes, error=False):
        from opentelemetry.trace import StatusCode

        spans = self.exporter.get_finished_spans()
        self.assertEqual(len(spans), 1)
        span = spans[0]
        self.assertEqual(span.name, "session.load")
        self.assertEqual(dict(span.attributes), expected_attributes)
        self.assertEqual(tuple(span.events), ())
        self.assertEqual(tuple(span.links), ())
        self.assertEqual(span.status.status_code, StatusCode.ERROR if error else StatusCode.UNSET)
        self.assertIsNone(span.status.description)
        self.assertNotIn(MARKER, span.to_json())

    def test_returns_exact_session_and_passes_identifiers_only_to_service(self):
        session = {"private": MARKER}
        service = SessionServiceDouble(result=session)
        self.assertIs(self.call(service), session)
        self.assertEqual(service.calls, [IDENTIFIERS])
        self.assert_safe_span(expected_attributes={
            "session.store": "managed", "session.found": True,
        })

    def test_missing_session_is_observed_without_changing_none(self):
        service = SessionServiceDouble()
        self.assertIsNone(self.call(service, store_kind="postgresql"))
        self.assertEqual(service.calls, [IDENTIFIERS])
        self.assert_safe_span(expected_attributes={
            "session.store": "postgresql", "session.found": False,
        })

    def exercise_error(self, error, category):
        service = SessionServiceDouble(error=error)
        with self.assertRaises(type(error)) as raised:
            self.call(service)
        self.assertIs(raised.exception, error)
        self.assertEqual(service.calls, [IDENTIFIERS])
        self.assert_safe_span(error=True, expected_attributes={
            "session.store": "managed", "error.type": category,
        })

    def test_sensitive_backend_exception_keeps_identity_without_exporting_content(self):
        self.exercise_error(RuntimeError(MARKER), "session_error")

    def test_timeout_keeps_identity_and_uses_fixed_category(self):
        self.exercise_error(TimeoutError(MARKER), "timeout")

    def test_cancellation_keeps_identity_and_uses_fixed_category(self):
        self.exercise_error(asyncio.CancelledError(MARKER), "cancelled")

    def test_invalid_store_labels_fail_before_observation_or_service_read(self):
        service = SessionServiceDouble()
        for label in (MARKER, "", "memory", "MANAGED", None, [], {}, 1):
            with self.subTest(label_type=type(label).__name__):
                with self.assertRaisesRegex(ValueError, "^Unsupported store label$"):
                    self.call(service, store_kind=label)
        self.assertEqual(service.calls, [])
        self.assertEqual(self.exporter.get_finished_spans(), ())

    def test_default_context_manager_records_the_sensitive_exception_control(self):
        from opentelemetry.trace import Status, StatusCode

        with self.assertRaises(RuntimeError):
            with self.tracer.start_as_current_span("unsafe.control") as span:
                span.set_attribute("error.type", "session_error")
                span.set_status(Status(StatusCode.ERROR))
                raise RuntimeError(MARKER)
        exported = self.exporter.get_finished_spans()[0]
        self.assertIn(MARKER, exported.to_json())
        self.assertTrue(any(event.name == "exception" for event in exported.events))

    def test_unfiltered_parent_can_still_record_the_same_sensitive_exception(self):
        service = SessionServiceDouble(error=RuntimeError(MARKER))
        with self.assertRaises(RuntimeError):
            with self.tracer.start_as_current_span("unfiltered.parent"):
                self.call(service)
        spans = {span.name: span for span in self.exporter.get_finished_spans()}
        self.assertEqual(set(spans), {"session.load", "unfiltered.parent"})
        self.assertNotIn(MARKER, spans["session.load"].to_json())
        self.assertIn(MARKER, spans["unfiltered.parent"].to_json())
        self.assertEqual(
            spans["session.load"].parent.span_id,
            spans["unfiltered.parent"].context.span_id,
        )


if __name__ == "__main__":
    unittest.main()
