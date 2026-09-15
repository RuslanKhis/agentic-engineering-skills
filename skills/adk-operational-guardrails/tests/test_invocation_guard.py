"""Offline checks for the reusable local guard; no ADK or provider calls."""

import asyncio
import importlib.util
from pathlib import Path
import time
import unittest

ASSET = Path(__file__).resolve().parents[1] / "assets" / "invocation_guard.py"
SPEC = importlib.util.spec_from_file_location("invocation_guard", ASSET)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)
InvocationGuard = MODULE.InvocationGuard
GuardStopped = MODULE.GuardStopped


class GuardTests(unittest.IsolatedAsyncioTestCase):
    def guard(self, calls=4, seconds=2):
        return InvocationGuard(max_tool_calls=calls, timeout_seconds=seconds)

    async def test_over_limit_never_executes(self):
        guard = self.guard(calls=1)
        effects = []

        async def operation():
            effects.append("executed")
            return 42

        self.assertEqual(await guard.run("lookup", {"id": 1}, operation), 42)
        with self.assertRaisesRegex(GuardStopped, "^tool_call_limit$"):
            await guard.run("lookup", {"id": 2}, operation)
        self.assertEqual(effects, ["executed"])
        self.assertEqual(guard.tool_calls, 1)

    async def test_canonical_terminal_failure_executes_once(self):
        guard = self.guard()
        effects = []

        async def operation():
            effects.append(1)
            return {"status": "failed"}

        await guard.run(
            "lookup", {"z": 2, "nested": {"b": 3, "a": 1}}, operation,
            classify=lambda result: "terminal_failure",
        )
        with self.assertRaisesRegex(GuardStopped, "^repeated_terminal_failure$"):
            await guard.run(
                "lookup", {"nested": {"a": 1, "b": 3}, "z": 2}, operation,
            )
        self.assertEqual(effects, [1])

    async def test_successful_read_can_repeat(self):
        guard = self.guard()
        count = 0

        async def operation():
            nonlocal count
            count += 1
            return count

        self.assertEqual(await guard.run("lookup", {}, operation), 1)
        self.assertEqual(await guard.run("lookup", {}, operation), 2)

    async def test_identical_in_flight_call_never_executes(self):
        guard = self.guard()
        entered, release = asyncio.Event(), asyncio.Event()
        effects = []

        async def operation():
            effects.append(1)
            entered.set()
            await release.wait()

        first = asyncio.create_task(guard.run("lookup", {}, operation))
        await entered.wait()
        try:
            with self.assertRaisesRegex(GuardStopped, "^identical_call_in_flight$"):
                await guard.run("lookup", {}, operation)
        finally:
            release.set()
            await first
        self.assertEqual(effects, [1])
        self.assertEqual(guard.tool_calls, 1)

    async def test_ambiguous_write_requires_reconciliation(self):
        guard = self.guard()
        effects = []

        async def operation():
            effects.append("remote_may_have_committed")
            return {"status": "unknown"}

        await guard.run("pay", {}, operation, effect="write", classify=lambda _: "ambiguous")
        with self.assertRaisesRegex(GuardStopped, "^write_requires_reconciliation$"):
            await guard.run("pay", {}, operation, effect="write")
        self.assertEqual(effects, ["remote_may_have_committed"])

    async def test_successful_write_is_not_executed_twice(self):
        guard = self.guard()

        async def operation():
            return "paid"

        await guard.run("pay", {}, operation, effect="write")
        with self.assertRaisesRegex(GuardStopped, "^write_already_completed$"):
            await guard.run("pay", {}, operation, effect="write")

    async def test_deadline_is_shared_and_expires_before_next_dispatch(self):
        guard = self.guard(seconds=0.01)
        await asyncio.sleep(0.02)
        called = False

        async def operation():
            nonlocal called
            called = True

        with self.assertRaisesRegex(GuardStopped, "^deadline_exceeded$"):
            await guard.run("lookup", {}, operation)
        self.assertFalse(called)
        self.assertEqual(guard.tool_calls, 0)

    async def test_cooperative_timeout_preserves_prior_effect(self):
        guard = self.guard(seconds=0.01)
        effects = []
        cancelled = asyncio.Event()

        async def operation():
            effects.append("already_applied")
            try:
                await asyncio.Event().wait()
            finally:
                cancelled.set()

        with self.assertRaisesRegex(GuardStopped, "^deadline_exceeded$"):
            await guard.run("pay", {}, operation, effect="write")
        self.assertTrue(cancelled.is_set())
        self.assertEqual(effects, ["already_applied"])

    async def test_tool_calls_do_not_receive_separate_time_windows(self):
        guard = self.guard(seconds=0.06)

        async def first():
            await asyncio.sleep(0.01)

        async def second():
            await asyncio.sleep(0.055)

        await guard.run("first", {}, first)
        with self.assertRaisesRegex(GuardStopped, "^deadline_exceeded$"):
            await guard.run("second", {}, second)
        self.assertEqual(guard.tool_calls, 2)

    async def test_suppressed_cancellation_cannot_return_late_success(self):
        guard = self.guard(seconds=0.01)

        async def operation():
            try:
                await asyncio.Event().wait()
            except asyncio.CancelledError:
                return "late_success"

        with self.assertRaisesRegex(GuardStopped, "^deadline_exceeded$"):
            await guard.run("lookup", {}, operation)

    async def test_no_yield_operation_rejects_late_result_without_rollback(self):
        guard = self.guard(seconds=0.01)
        effects = []

        async def operation():
            effects.append("already_applied")
            time.sleep(0.02)  # Deliberately blocks: cancellation cannot preempt it.
            return "late_success"

        with self.assertRaisesRegex(GuardStopped, "^deadline_exceeded$"):
            await guard.run("pay", {}, operation, effect="write")
        self.assertEqual(effects, ["already_applied"])

    async def test_external_cancellation_blocks_ambiguous_write(self):
        guard = self.guard()
        entered = asyncio.Event()
        effects = []

        async def operation():
            effects.append("already_applied")
            entered.set()
            await asyncio.Event().wait()

        task = asyncio.create_task(guard.run("pay", {}, operation, effect="write"))
        await entered.wait()
        task.cancel()
        with self.assertRaises(asyncio.CancelledError):
            await task
        with self.assertRaisesRegex(GuardStopped, "^write_requires_reconciliation$"):
            await guard.run("pay", {}, operation, effect="write")
        self.assertEqual(effects, ["already_applied"])

    async def test_operation_timeout_is_not_misreported_as_guard_deadline(self):
        async def operation():
            raise TimeoutError("provider_timeout")

        with self.assertRaisesRegex(TimeoutError, "^provider_timeout$"):
            await self.guard().run("lookup", {}, operation)

    async def test_invalid_configuration_and_json_are_rejected(self):
        for calls in (0, -1, True, 1.5):
            with self.subTest(calls=calls), self.assertRaises(ValueError):
                self.guard(calls=calls)
        for seconds in (0, -1, True, float("nan"), float("inf"), "1", 10 ** 400):
            with self.subTest(seconds=seconds), self.assertRaises(ValueError):
                self.guard(seconds=seconds)
        cycle = {}
        cycle["cycle"] = cycle
        for arguments in ({"x": float("nan")}, {"x": float("inf")},
                          {1: "key"}, {"x": object()}, {"x": (1, 2)}, cycle, []):
            with self.subTest(arguments=type(arguments)), self.assertRaisesRegex(
                ValueError, "^invalid_arguments$"
            ):
                self.guard().admit("lookup", arguments)
        guard = self.guard()
        with self.assertRaisesRegex(ValueError, "^invalid_action$"):
            guard.admit("", {})
        with self.assertRaisesRegex(ValueError, "^invalid_effect$"):
            guard.admit("lookup", {}, effect="invalid")
        self.assertEqual(guard.tool_calls, 0)

    async def test_manual_admissions_validate_outcome_and_instance_ownership(self):
        first, second = self.guard(), self.guard()
        token = first.admit("lookup", {})
        with self.assertRaisesRegex(ValueError, "^invalid_admission$"):
            second.finish(token, "success")
        with self.assertRaisesRegex(ValueError, "^invalid_outcome$"):
            first.finish(token, "unknown")
        first.finish(token, "terminal_failure")
        second_token = second.admit("lookup", {})
        second.finish(second_token, "success")
        with self.assertRaisesRegex(GuardStopped, "^repeated_terminal_failure$"):
            first.admit("lookup", {})
        with self.assertRaisesRegex(ValueError, "^invalid_admission$"):
            first.finish(token, "success")

    async def test_guard_error_does_not_expose_arguments(self):
        guard = self.guard()
        token = guard.admit("private-action", {"secret": "private-value"})
        guard.finish(token, "terminal_failure")
        with self.assertRaises(GuardStopped) as caught:
            guard.admit("private-action", {"secret": "private-value"})
        self.assertEqual(str(caught.exception), "repeated_terminal_failure")
        self.assertNotIn("private", repr(caught.exception))


if __name__ == "__main__":
    unittest.main()
