"""Application-owned identity: the intranet gateway signs each request.

Not generated. The staff ID used as the ADK user_id comes only from here.
"""
from __future__ import annotations

import hashlib
import hmac
import time


class Unauthenticated(Exception):
    pass


def verify_staff_header(header: str | None, secret: bytes, now: float | None = None,
                        max_age_s: int = 300) -> str:
    """Return the staff ID from an `X-Northbridge-Staff: <staff_id>.<unix_ts>.<hex hmac>` header."""
    if not header:
        raise Unauthenticated("missing staff header")
    try:
        staff_id, ts, signature = header.rsplit(".", 2)
        issued = int(ts)
    except ValueError as exc:
        raise Unauthenticated("malformed staff header") from exc
    expected = hmac.new(secret, f"{staff_id}.{ts}".encode(), hashlib.sha256).hexdigest()
    if not hmac.compare_digest(expected, signature):
        raise Unauthenticated("bad signature")
    if abs((now or time.time()) - issued) > max_age_s:
        raise Unauthenticated("expired")
    return staff_id
