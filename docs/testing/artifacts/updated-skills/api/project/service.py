"""Synthetic provider adapter for status lookups and refunds.

The caller owns the authenticated ``httpx.AsyncClient`` (base URL, credentials,
finite transport timeouts and closing it) and performs authorisation/approval
before calling ``refund``. See CONTRACT.md.

Refunds are dispatched at most once per call: the provider offers no protected
replay facility, so any failure after dispatch is reported as ``unknown`` and
must be reconciled before another refund is considered.

Reasons and log records contain classification only (reason code, exception
class, HTTP status, failing field name, elapsed time). Provider bodies,
exception messages, references and amounts are never included.
"""

import asyncio
import logging
import os
import re
import time
import traceback
from decimal import Decimal

import httpx

logger = logging.getLogger(__name__)

LOOKUP_STATES = frozenset({"ready", "pending"})
MAX_REFERENCE_LENGTH = 256
# Fixed USD fixture: positive decimal string with an optional "+", ASCII
# digits and exactly two fractional digits. Spelling such as "01.00" is valid
# and sent unchanged. The integer-digit bound limits input size, not business.
_AMOUNT_PATTERN = re.compile(r"\+?[0-9]{1,15}\.[0-9]{2}")


class _Failure(Exception):
    """Expected, classified failure carrying only safe diagnostic fields."""

    def __init__(self, code, *, status=None, field=None, error=None):
        super().__init__(code)
        self.code = code
        self.status = status
        self.field = field
        self.error_class = type(error).__name__ if error is not None else None


def _result(ok, data, reason, outcome):
    return {"ok": ok, "data": data, "reason": reason, "outcome": outcome}


def _valid_reference(reference):
    return (
        isinstance(reference, str)
        and 0 < len(reference) <= MAX_REFERENCE_LENGTH
        and reference.strip() == reference
        and reference.isprintable()
    )


def _valid_amount(amount):
    return (
        isinstance(amount, str)
        and _AMOUNT_PATTERN.fullmatch(amount) is not None
        and Decimal(amount) > 0
    )


async def _send(request):
    """Run one HTTP request, translating transport errors into ``_Failure``."""
    try:
        return await request
    except httpx.TimeoutException as error:
        raise _Failure("transport_timeout", error=error) from None
    except httpx.TransportError as error:
        raise _Failure("transport_error", error=error) from None
    except httpx.HTTPStatusError as error:  # e.g. raise_for_status event hook
        raise _Failure(
            "http_status", status=error.response.status_code, error=error
        ) from None
    except httpx.HTTPError as error:
        raise _Failure("http_error", error=error) from None


def _json_object(response):
    if not 200 <= response.status_code < 300:
        raise _Failure("http_status", status=response.status_code)
    try:
        body = response.json()
    except ValueError as error:  # JSONDecodeError and UnicodeDecodeError
        raise _Failure("invalid_json", status=response.status_code, error=error) from None
    if not isinstance(body, dict):
        raise _Failure("invalid_response", status=response.status_code, field="$")
    return body


def _require(body, field, predicate, status):
    if field not in body or not predicate(body[field]):
        raise _Failure("invalid_response", status=status, field=field)


def _describe(failure):
    parts = [failure.code]
    if failure.status is not None:
        parts.append(str(failure.status))
    if failure.field is not None:
        parts.append(failure.field)
    return ":".join(parts)


def _frame_locations(error):
    """Return "file.py:line:function" per frame.

    Source lines, locals and the exception message are omitted because any of
    them can contain sensitive literals or values.
    """
    return tuple(
        f"{os.path.basename(frame.filename)}:{frame.lineno}:{frame.name}"
        for frame in traceback.extract_tb(error.__traceback__)
    )


def _log(level, operation, outcome, started, failure=None, error=None):
    fields = {
        "operation": operation,
        "outcome": outcome,
        "elapsed_ms": round((time.monotonic() - started) * 1000, 1),
    }
    if failure is not None:
        fields.update(
            reason_code=failure.code,
            http_status=failure.status,
            field=failure.field,
            error_class=failure.error_class,
        )
    if error is not None:
        fields.update(
            reason_code="unexpected_error",
            error_class=type(error).__name__,
            error_frames=_frame_locations(error),
        )
    logger.log(
        level,
        "provider %s %s", operation, outcome,
        extra={"provider_call": fields},
    )


class Gateway:
    def __init__(self, client):
        self.client = client

    async def lookup(self, reference):
        started = time.monotonic()
        if not _valid_reference(reference):
            failure = _Failure("invalid_reference")
            _log(logging.WARNING, "lookup", "unavailable", started, failure)
            return _result(False, None, _describe(failure), "unavailable")
        try:
            response = await _send(
                self.client.get("/status", params={"reference": reference})
            )
            body = _json_object(response)
            status = response.status_code
            _require(body, "reference", lambda v: v == reference, status)
            _require(body, "state", lambda v: isinstance(v, str) and v in LOOKUP_STATES,
                     status)
        except _Failure as failure:
            _log(logging.WARNING, "lookup", "unavailable", started, failure)
            return _result(False, None, _describe(failure), "unavailable")
        except Exception as error:
            # A defect, not a provider failure: keep it visible to monitoring.
            _log(logging.ERROR, "lookup", "unavailable", started, error=error)
            return _result(False, None, "unexpected_error", "unavailable")
        _log(logging.INFO, "lookup", "read", started)
        return _result(True, body, None, "read")

    async def refund(self, reference, amount):
        started = time.monotonic()
        if not _valid_reference(reference):
            failure = _Failure("invalid_reference")
        elif not _valid_amount(amount):
            failure = _Failure("invalid_amount")
        else:
            failure = None
        if failure is not None:
            _log(logging.WARNING, "refund", "not_attempted", started, failure)
            return _result(False, None, _describe(failure), "not_attempted")

        # From here the request may reach the provider. There is no protected
        # replay, so exactly one attempt is made and every failure is unknown.
        try:
            response = await _send(
                self.client.post(
                    "/refunds", json={"reference": reference, "amount": amount}
                )
            )
            body = _json_object(response)
            status = response.status_code
            _require(body, "refund_id", lambda v: isinstance(v, str) and v != "", status)
            _require(body, "reference", lambda v: v == reference, status)
            _require(body, "amount", lambda v: v == amount, status)
            _require(body, "status", lambda v: v == "applied", status)
        except _Failure as failure:
            _log(logging.ERROR, "refund", "unknown", started, failure)
            return _result(False, None, _unknown_reason(_describe(failure)), "unknown")
        except asyncio.CancelledError:
            # Caller cancellation propagates; the refund may still be applied.
            _log(logging.ERROR, "refund", "unknown", started,
                 _Failure("cancelled_after_dispatch"))
            raise
        except Exception as error:
            _log(logging.ERROR, "refund", "unknown", started, error=error)
            return _result(False, None, _unknown_reason("unexpected_error"), "unknown")
        _log(logging.INFO, "refund", "applied", started)
        return _result(True, body, None, "applied")


def _unknown_reason(code):
    return (
        f"refund_outcome_unknown:{code}; the refund may have been applied, "
        "reconcile with the provider before any new refund"
    )
