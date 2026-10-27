"""A minimal transport seam: production uses httpx, tests pass a fake."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Protocol


class TransportTimeout(Exception):
    """No response arrived before the deadline; the request may or may not have been processed."""


class TransportError(Exception):
    """The connection failed before the request was sent."""


@dataclass
class Response:
    status_code: int
    body: dict[str, Any] = field(default_factory=dict)


class Transport(Protocol):
    def request(self, method: str, url: str, *, json: dict | None = None,
                headers: dict | None = None, timeout: float = 10.0) -> Response: ...


class HttpxTransport:
    """Production transport. Imported lazily so tests never need httpx."""

    def request(self, method, url, *, json=None, headers=None, timeout=10.0):
        import httpx

        try:
            resp = httpx.request(method, url, json=json, headers=headers, timeout=timeout)
        except httpx.ConnectError as exc:
            raise TransportError(str(exc)) from exc
        except httpx.TimeoutException as exc:
            raise TransportTimeout(str(exc)) from exc
        try:
            body = resp.json()
        except ValueError:
            body = {"raw": resp.text}
        return Response(resp.status_code, body)
