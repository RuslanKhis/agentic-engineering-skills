"""Deterministic controller checks; these do not validate an SDP detector."""

import asyncio
import dataclasses
import importlib.util
import logging
import pathlib
import sys
import traceback
import unittest
from unittest.mock import patch


ASSET = pathlib.Path(__file__).resolve().parents[1] / "assets" / "sdp_boundary.py"
SPEC = importlib.util.spec_from_file_location("sdp_boundary", ASSET)
boundary = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = boundary
SPEC.loader.exec_module(boundary)
InspectResult = boundary.InspectResult
TextProtectionError = boundary.TextProtectionError
protect_text = boundary.protect_text


class FakeProviders:
    """Only a synthetic fixture transformation, never a production detector."""

    def __init__(self, result=None):
        self.result = result if result is not None else InspectResult(0, False)
        self.events = []

    async def inspect(self, text):
        self.events.append(("inspect", text))
        return self.result

    async def deidentify(self, text):
        self.events.append(("deidentify", text))
        return text.replace("alice@example.test", "[EMAIL]")

    async def deliver(self, text, **options):
        protected = await protect_text(
            text, inspect=self.inspect, deidentify=self.deidentify, **options
        )
        for sink in ("model", "session", "tool"):
            self.events.append((sink, protected))
        return protected


class ProtectTextTests(unittest.IsolatedAsyncioTestCase):
    async def assert_blocked(self, callback):
        with self.assertRaises(TextProtectionError) as caught:
            await callback()
        self.assertEqual(
            str(caught.exception),
            "Text protection failed; downstream use is blocked.",
        )
        self.assertIsNone(caught.exception.__context__)
        self.assertIsNone(caught.exception.__cause__)
        return caught.exception

    async def test_transform_precedes_every_sink_and_second_run_is_identical(self):
        fake = FakeProviders()
        raw = "Contact alice@example.test"
        expected = "Contact [EMAIL]"
        for _ in range(2):
            fake.events.clear()
            self.assertEqual(await fake.deliver(raw), expected)
            self.assertEqual(
                fake.events,
                [("inspect", raw), ("deidentify", raw)]
                + [(sink, expected) for sink in ("model", "session", "tool")],
            )

    async def test_denied_or_incomplete_inspection_never_reaches_other_calls(self):
        for result in (InspectResult(1, False), InspectResult(0, True), InspectResult(4, True)):
            with self.subTest(result=result):
                fake = FakeProviders(result)
                await self.assert_blocked(lambda: fake.deliver("synthetic secret"))
                self.assertEqual(fake.events, [("inspect", "synthetic secret")])

    async def test_malformed_inspection_fails_closed(self):
        malformed = [
            {}, (0, False), "safe", InspectResult(True, False),
            InspectResult(-1, False), InspectResult(0.0, False),
            InspectResult(0, 0), InspectResult(0, None),
        ]
        for result in malformed:
            with self.subTest(result=result):
                fake = FakeProviders(result)
                await self.assert_blocked(lambda: fake.deliver("synthetic"))
                self.assertEqual(fake.events, [("inspect", "synthetic")])

    async def test_provider_exceptions_do_not_leak_or_reach_sinks(self):
        raw = "alice@example.test"
        for stage in ("inspect", "deidentify"):
            fake = FakeProviders()

            async def fail(text):
                fake.events.append((stage, text))
                raise RuntimeError("provider detail: " + text)

            setattr(fake, stage, fail)
            error = await self.assert_blocked(lambda: fake.deliver(raw))
            rendered = "".join(traceback.format_exception(error))
            self.assertNotIn(raw, rendered)
            self.assertNotIn("provider detail", rendered)
            self.assertNotIn("RuntimeError", rendered)
            self.assertFalse(any(name in ("model", "session", "tool") for name, _ in fake.events))

    async def test_logging_sink_receives_protected_text_without_failure_canaries(self):
        canary = "alice@example.test"
        raw = "Contact " + canary
        logger = logging.getLogger("test_sdp_boundary.downstream")
        good = FakeProviders()
        denied = FakeProviders(InspectResult(1, False))
        failed = FakeProviders()

        async def provider_failure(text):
            raise RuntimeError("provider payload: " + text)

        failed.inspect = provider_failure

        async def deliver_to_log(fake):
            protected = await fake.deliver(raw)
            logger.info("protected=%s", protected)

        # Capture root logging so this also catches accidental controller logs.
        with self.assertLogs(level="DEBUG") as captured:
            await deliver_to_log(good)
            await self.assert_blocked(lambda: deliver_to_log(denied))
            await self.assert_blocked(lambda: deliver_to_log(failed))
        self.assertEqual(
            captured.output,
            ["INFO:test_sdp_boundary.downstream:protected=Contact [EMAIL]"],
        )
        self.assertNotIn(canary, "\n".join(captured.output))
        self.assertNotIn("provider payload", "\n".join(captured.output))

    async def test_invalid_inputs_and_options_do_not_call_providers(self):
        cases = [
            ("", {}), (None, {}), (b"text", {}), ("\ud800", {}),
            ("four", {"max_chars": 3}), ("text", {"max_chars": True}),
            ("text", {"max_chars": 0}), ("text", {"max_chars": -1}),
            ("text", {"max_chars": 4.0}), ("text", {"timeout_s": True}),
            ("text", {"timeout_s": 0}), ("text", {"timeout_s": -1}),
            ("text", {"timeout_s": float("nan")}),
            ("text", {"timeout_s": float("inf")}),
            ("text", {"timeout_s": "1"}),
        ]
        for raw, options in cases:
            with self.subTest(raw=repr(raw), options=options):
                fake = FakeProviders()
                await self.assert_blocked(lambda: fake.deliver(raw, **options))
                self.assertEqual(fake.events, [])

    async def test_invalid_or_overlong_transformed_output_never_reaches_sinks(self):
        for output in ("", None, b"safe", "\udfff", "12345"):
            with self.subTest(output=repr(output)):
                fake = FakeProviders()

                async def transform(text):
                    fake.events.append(("deidentify", text))
                    return output

                fake.deidentify = transform
                await self.assert_blocked(lambda: fake.deliver("text", max_chars=4))
                self.assertEqual([name for name, _ in fake.events], ["inspect", "deidentify"])

    async def test_limit_counts_unicode_characters_and_accepts_exact_limit(self):
        fake = FakeProviders()
        self.assertEqual(await fake.deliver("\U0001f600" * 4, max_chars=4), "\U0001f600" * 4)

    async def test_timeout_during_each_provider_blocks_sinks(self):
        for stage in ("inspect", "deidentify"):
            with self.subTest(stage=stage):
                fake = FakeProviders()
                cancelled = asyncio.Event()

                async def never_finishes(text):
                    fake.events.append((stage, text))
                    try:
                        await asyncio.Event().wait()
                    finally:
                        cancelled.set()

                setattr(fake, stage, never_finishes)
                await self.assert_blocked(lambda: fake.deliver("text", timeout_s=0.01))
                self.assertTrue(cancelled.is_set())
                self.assertFalse(any(name in ("model", "session", "tool") for name, _ in fake.events))

    async def test_one_deadline_covers_both_operations(self):
        fake = FakeProviders()
        loop = asyncio.get_running_loop()
        real_time = loop.time
        base = real_time()
        now = [base]

        async def inspect(text):
            fake.events.append(("inspect", text))
            now[0] = base + 0.6
            return InspectResult(0, False)

        async def deidentify(text):
            fake.events.append(("deidentify", text))
            now[0] = base + 1.1
            return "safe"

        fake.inspect, fake.deidentify = inspect, deidentify
        # Neither provider yields: this tests the explicit deadline guards
        # without depending on scheduling latency or wall-clock sleeps.
        with patch.object(loop, "time", side_effect=lambda: now[0]):
            await self.assert_blocked(lambda: fake.deliver("text", timeout_s=1.0))
        self.assertEqual([name for name, _ in fake.events], ["inspect", "deidentify"])

    async def test_cancelled_provider_is_not_translated_to_boundary_error(self):
        for stage in ("inspect", "deidentify"):
            fake = FakeProviders()
            entered = asyncio.Event()

            async def wait_forever(text):
                fake.events.append((stage, text))
                entered.set()
                await asyncio.Event().wait()

            setattr(fake, stage, wait_forever)
            task = asyncio.create_task(fake.deliver("text"))
            await entered.wait()
            task.cancel()
            with self.assertRaises(asyncio.CancelledError):
                await task
            self.assertFalse(any(name in ("model", "session", "tool") for name, _ in fake.events))

    async def test_concurrent_calls_have_independent_data_and_outcomes(self):
        both_entered = asyncio.Event()
        entered = []
        transformed = []

        async def inspect(text):
            entered.append(text)
            if len(entered) == 2:
                both_entered.set()
            await both_entered.wait()
            return InspectResult(int(text == "deny"), False)

        async def deidentify(text):
            transformed.append(text)
            return text.replace("alice@example.test", "[EMAIL]")

        results = await asyncio.gather(
            *(protect_text(text, inspect=inspect, deidentify=deidentify)
              for text in ("deny", "alice@example.test")),
            return_exceptions=True,
        )
        self.assertIsInstance(results[0], TextProtectionError)
        self.assertEqual(results[1], "[EMAIL]")
        self.assertEqual(transformed, ["alice@example.test"])

    def test_inspection_result_is_immutable(self):
        result = InspectResult(0, False)
        with self.assertRaises(dataclasses.FrozenInstanceError):
            result.findings_count = 1

    def test_import_guard_rejects_simulated_older_python_versions(self):
        # This exercises the guard on the current interpreter, not an actual
        # compatibility run under either of these older interpreters.
        spec = importlib.util.spec_from_file_location("sdp_boundary_unsupported", ASSET)
        for version in ((3, 9, 0), (3, 10, 0)):
            with self.subTest(version=version):
                module = importlib.util.module_from_spec(spec)
                with patch.object(sys, "version_info", version):
                    with self.assertRaisesRegex(
                        RuntimeError, r"^sdp_boundary requires Python 3\.11 or newer\.$"
                    ):
                        spec.loader.exec_module(module)


if __name__ == "__main__":
    unittest.main()
