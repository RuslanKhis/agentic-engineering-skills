"""An async, fail-closed text boundary with injected SDP provider adapters.

Copyright (c) 2026 RuslanKhis
SPDX-License-Identifier: MIT
Retain this notice and the accompanying skill-root LICENSE when copying.

Requires Python 3.11+ for ``asyncio.timeout_at``; tested on Python 3.11.4.

This controller does not detect PII or implement a Google Cloud SDK adapter.
Production wiring must supply an ``inspect`` adapter configured for the
credential/secret deny policy and a ``deidentify`` adapter configured for the
approved PII replacement policy. The inspection adapter must faithfully report
finding counts and incomplete/truncated inspection, including empty findings
with truncation. Treat every other incomplete or failed provider response as an
adapter error; never substitute a successful empty result or the original text.

Callers MUST await ``protect_text`` before writing content to a model, session,
tool, log, or other sink, and use only its returned text. Apply it to every
untrusted text path, including inbound requests, tool results, and replayed
content. This module is a controller, not a complete gateway: structured payload
traversal, authentication, retries, and sink enforcement belong to the caller.
It performs no logging. Do not log raw text or provider exceptions in adapters.
Generic errors do not erase raw text from traceback frame locals. Callers must
disable or sanitize local-variable capture and payload capture in exception
exporters, tracing, debugging, and other observability integrations.

Both provider calls share one deadline. Adapters must remain asynchronous, avoid
blocking the event loop, and propagate cancellation; Python cannot forcibly
terminate blocking provider work. Inputs and outputs must be non-empty, valid
UTF-8 strings within ``max_chars`` Unicode characters. Provider byte limits and
request/response schema validation are additional adapter responsibilities.
Full redaction must return a non-empty approved replacement placeholder.
"""

from __future__ import annotations

import asyncio
import math
import sys
from collections.abc import Awaitable, Callable
from dataclasses import dataclass


if sys.version_info < (3, 11):
    raise RuntimeError("sdp_boundary requires Python 3.11 or newer.")


@dataclass(frozen=True, slots=True)
class InspectResult:
    """Normalized deny-policy inspection; truncation means incomplete coverage."""

    findings_count: int
    findings_truncated: bool


class TextProtectionError(Exception):
    """Text was not proven safe for downstream use; do not continue to sinks."""


def _valid_text(value: object, max_chars: int) -> bool:
    if type(value) is not str or not 0 < len(value) <= max_chars:
        return False
    try:
        value.encode("utf-8")
    except UnicodeEncodeError:
        return False
    return True


async def protect_text(
    text: str,
    *,
    inspect: Callable[[str], Awaitable[InspectResult]],
    deidentify: Callable[[str], Awaitable[str]],
    max_chars: int = 10_000,
    timeout_s: float = 10.0,
) -> str:
    """Inspect for denied data, require complete coverage, then deidentify PII.

    Any denied finding, incomplete inspection, invalid value, provider failure,
    or expired deadline raises a generic ``TextProtectionError``. Cancellation
    propagates unchanged. Each invocation has independent state and no cache.
    """
    try:
        if (
            type(max_chars) is not int
            or max_chars <= 0
            or type(timeout_s) not in (int, float)
            or not math.isfinite(timeout_s)
            or timeout_s <= 0
            or not _valid_text(text, max_chars)
        ):
            raise ValueError

        loop = asyncio.get_running_loop()
        deadline = loop.time() + timeout_s
        if not math.isfinite(deadline):
            raise ValueError
        async with asyncio.timeout_at(deadline):
            result = await inspect(text)
            if (
                type(result) is not InspectResult
                or type(result.findings_count) is not int
                or result.findings_count < 0
                or type(result.findings_truncated) is not bool
                or result.findings_count > 0
                or result.findings_truncated
            ):
                raise ValueError
            if loop.time() >= deadline:
                raise TimeoutError

            protected = await deidentify(text)
            if not _valid_text(protected, max_chars):
                raise ValueError
            if loop.time() >= deadline:
                raise TimeoutError
        return protected
    except Exception:
        # Raise outside the handler so the provider exception is not retained
        # as __context__. CancelledError inherits BaseException and propagates.
        pass
    raise TextProtectionError("Text protection failed; downstream use is blocked.") from None
