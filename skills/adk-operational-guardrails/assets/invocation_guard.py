# SPDX-License-Identifier: MIT
# Copyright (c) 2026 RuslanKhis
"""Local, invocation-only pre-execution guard; Python 3.11+, standard library.

Create one instance per invocation and share it across every tool dispatch on
one event loop. Call run() around the actual effect, or pair admit()/finish()
in try/finally. An admission consumes a call even when the operation fails.
Arguments must be JSON dictionaries; signatures include action, effect and
canonical arguments. Identical concurrent calls are rejected, not queued.

Successful reads can repeat. Terminal failures cannot repeat. Identical writes
cannot repeat after success or an ambiguous outcome; reconcile externally.
These are local signatures, NOT durable business-operation idempotency keys.
The absolute deadline includes idle time between calls. Async cancellation is
cooperative: blocking code can overrun it, but late results are rejected. A
timeout/cancellation never proves that an external effect was rolled back.
There is no durable store, authentication, budget reservation or remote cancel.
Guard-generated errors contain fixed codes, never action names or arguments.
"""

from __future__ import annotations

import asyncio
import json
import math
import time
from collections.abc import Awaitable, Callable
from typing import Any, Literal, TypeVar

T = TypeVar("T")
Outcome = Literal["success", "terminal_failure", "ambiguous"]
Effect = Literal["read", "write"]


class GuardStopped(RuntimeError):
    """A guard decision with a fixed, safe-to-log reason code."""

    def __init__(self, code: str) -> None:
        self.code = code
        super().__init__(code)


def _signature(action: str, arguments: dict[str, Any], effect: Effect) -> str:
    def check(value: Any) -> None:
        if type(value) is dict:
            if any(type(key) is not str for key in value):
                raise ValueError
            for item in value.values():
                check(item)
        elif type(value) is list:
            for item in value:
                check(item)
        elif type(value) is float:
            if not math.isfinite(value):
                raise ValueError
        elif type(value) not in (str, int, bool, type(None)):
            raise ValueError

    if type(action) is not str or not action.strip():
        raise ValueError("invalid_action")
    if type(arguments) is not dict:
        raise ValueError("invalid_arguments")
    try:
        check(arguments)
        return json.dumps(
            [action, effect, arguments], sort_keys=True, allow_nan=False,
            ensure_ascii=True, separators=(",", ":"),
        )
    except (TypeError, ValueError, RecursionError):
        raise ValueError("invalid_arguments") from None


class InvocationGuard:
    """One-event-loop guard; do not share across threads or invocations."""

    def __init__(self, *, max_tool_calls: int, timeout_seconds: float) -> None:
        if type(max_tool_calls) is not int or max_tool_calls <= 0:
            raise ValueError("invalid_max_tool_calls")
        try:
            valid_timeout = (
                type(timeout_seconds) in (int, float)
                and math.isfinite(timeout_seconds) and timeout_seconds > 0
            )
        except OverflowError:
            valid_timeout = False
        if not valid_timeout:
            raise ValueError("invalid_timeout_seconds")
        self._limit = max_tool_calls
        self._deadline = time.monotonic() + timeout_seconds
        if not math.isfinite(self._deadline):
            raise ValueError("invalid_timeout_seconds")
        self._calls = 0
        self._pending: dict[object, tuple[str, Effect]] = {}
        self._in_flight: set[str] = set()
        self._blocked: dict[str, str] = {}

    @property
    def tool_calls(self) -> int:
        return self._calls

    def _check_deadline(self) -> None:
        if time.monotonic() >= self._deadline:
            raise GuardStopped("deadline_exceeded")

    def admit(
        self, action: str, arguments: dict[str, Any], *, effect: Effect = "read",
    ) -> object:
        """Admit immediately before execution; always finish the returned token."""
        if type(effect) is not str or effect not in ("read", "write"):
            raise ValueError("invalid_effect")
        signature = _signature(action, arguments, effect)
        self._check_deadline()
        if signature in self._blocked:
            raise GuardStopped(self._blocked[signature])
        if signature in self._in_flight:
            raise GuardStopped("identical_call_in_flight")
        if self._calls >= self._limit:
            raise GuardStopped("tool_call_limit")
        token = object()
        self._calls += 1
        self._pending[token] = (signature, effect)
        self._in_flight.add(signature)
        return token

    def finish(self, token: object, outcome: Outcome) -> None:
        """Report a trusted classification; uncertainty is 'ambiguous'."""
        if type(outcome) is not str or outcome not in ("success", "terminal_failure", "ambiguous"):
            raise ValueError("invalid_outcome")
        try:
            signature, effect = self._pending.pop(token)
        except (KeyError, TypeError):
            raise ValueError("invalid_admission") from None
        self._in_flight.remove(signature)
        if outcome == "terminal_failure":
            self._blocked[signature] = "repeated_terminal_failure"
        elif effect == "write":
            self._blocked[signature] = (
                "write_already_completed" if outcome == "success"
                else "write_requires_reconciliation"
            )

    async def run(
        self, action: str, arguments: dict[str, Any],
        operation: Callable[[], Awaitable[T]], *, effect: Effect = "read",
        classify: Callable[[T], Outcome] | None = None,
    ) -> T:
        """Execute once; never retry. Supply a classifier for structured failures.

        With no classifier, a normal return means success. Any exception or
        cancellation means ambiguous; the original exception is propagated.
        Only this guard's deadline is translated into deadline_exceeded.
        """
        if not callable(operation) or (classify is not None and not callable(classify)):
            raise ValueError("invalid_callable")
        token = self.admit(action, arguments, effect=effect)
        timer = asyncio.timeout(max(0.0, self._deadline - time.monotonic()))
        try:
            async with timer:
                result = await operation()
            self._check_deadline()  # Also catches blocking/suppressed cancellation.
            outcome = "success" if classify is None else classify(result)
            if type(outcome) is not str or outcome not in ("success", "terminal_failure", "ambiguous"):
                raise ValueError("invalid_outcome")
            self._check_deadline()
        except BaseException as error:
            self.finish(token, "ambiguous")
            if isinstance(error, TimeoutError) and timer.expired():
                raise GuardStopped("deadline_exceeded") from None
            raise
        self.finish(token, outcome)
        return result
