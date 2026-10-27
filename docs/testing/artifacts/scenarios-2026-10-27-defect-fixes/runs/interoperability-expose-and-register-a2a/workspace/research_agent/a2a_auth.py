"""Bearer-token authentication in front of the A2A app. Pure ASGI, no google.adk imports."""
from __future__ import annotations

import json
from typing import Awaitable, Callable

CARD_PATH = "/.well-known/agent-card.json"


class VerifierUnavailable(Exception):
    """The verifier could not reach its keys; the request is denied with 503."""


class Principal:
    """Authenticated user object for request.scope["user"] (Starlette's contract)."""

    is_authenticated = True

    def __init__(self, name: str, scopes: frozenset[str] = frozenset()):
        self.identity = name
        self.display_name = name
        self.scopes = scopes


# verify(token) -> Principal for a valid token, None for an invalid one,
# raises VerifierUnavailable when keys cannot be fetched.
Verifier = Callable[[str], Awaitable[Principal | None]]


async def _respond(send, status: int, detail: str, headers: list[tuple[bytes, bytes]] | None = None):
    body = json.dumps({"error": detail}).encode()
    await send({"type": "http.response.start", "status": status,
                "headers": [(b"content-type", b"application/json"), *(headers or [])]})
    await send({"type": "http.response.body", "body": body})


class BearerAuthMiddleware:
    """Everything except the public card needs a verified bearer token (fail closed)."""

    def __init__(self, app, verify: Verifier, required_scope: str | None = None):
        self.app, self.verify, self.required_scope = app, verify, required_scope

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http" or scope["path"].endswith(CARD_PATH):
            return await self.app(scope, receive, send)
        auth = dict(scope["headers"]).get(b"authorization", b"").decode()
        scheme, _, token = auth.partition(" ")
        challenge = [(b"www-authenticate", b'Bearer realm="research-agent"')]
        if scheme.lower() != "bearer" or not token:
            return await _respond(send, 401, "missing bearer token", challenge)
        try:
            principal = await self.verify(token)
        except VerifierUnavailable:
            return await _respond(send, 503, "token verifier unavailable")
        if principal is None:
            return await _respond(send, 401, "invalid token", challenge)
        if self.required_scope and self.required_scope not in principal.scopes:
            return await _respond(send, 403, "insufficient scope")
        scope["user"] = principal
        return await self.app(scope, receive, send)
