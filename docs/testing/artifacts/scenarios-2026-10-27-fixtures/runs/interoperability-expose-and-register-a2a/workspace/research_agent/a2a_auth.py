"""Inbound auth for the A2A endpoint: pure ASGI, no third-party imports at module level.

Cloud Run IAM is the first gate (--no-allow-unauthenticated). This middleware is the second: it
verifies the Google-signed OIDC token itself and accepts only the listed caller principals,
so a mis-set IAM binding or an internal-network caller does not open the agent.
"""
from __future__ import annotations

import json
from typing import Awaitable, Callable

CARD_PATH = "/.well-known/agent-card.json"
# Verifier: (token, audience) -> claims dict; raises ValueError for an invalid token and
# ConnectionError when keys cannot be fetched.
Verifier = Callable[[str, str], dict]


def google_oidc_verifier(token: str, audience: str) -> dict:
    from google.auth.exceptions import TransportError
    from google.auth.transport import requests as g_requests
    from google.oauth2 import id_token

    try:
        return id_token.verify_oauth2_token(token, g_requests.Request(), audience=audience)
    except TransportError as exc:
        raise ConnectionError(str(exc)) from exc


async def _reply(send, status: int, message: str, www_authenticate: bool = False) -> None:
    headers = [(b"content-type", b"application/json")]
    if www_authenticate:
        headers.append((b"www-authenticate", b'Bearer realm="research-agent"'))
    await send({"type": "http.response.start", "status": status, "headers": headers})
    await send({"type": "http.response.body", "body": json.dumps({"error": message}).encode()})


class CallerAuthMiddleware:
    """401 without a valid token, 403 for a valid token from an unlisted principal, 503 if keys are unreachable."""

    def __init__(self, app, *, audience: str, allowed_emails: set[str], verifier: Verifier = google_oidc_verifier):
        self.app, self.audience, self.verifier = app, audience, verifier
        self.allowed = {e.lower() for e in allowed_emails}

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http" or scope["path"] == CARD_PATH:
            return await self.app(scope, receive, send)
        headers = {k.decode().lower(): v.decode() for k, v in scope["headers"]}
        # Cloud Run documents X-Serverless-Authorization for callers that cannot use Authorization.
        raw = headers.get("x-serverless-authorization") or headers.get("authorization", "")
        scheme, _, token = raw.partition(" ")
        if scheme.lower() != "bearer" or not token:
            return await _reply(send, 401, "missing bearer token", www_authenticate=True)
        try:
            claims = self.verifier(token, self.audience)
        except ConnectionError:
            return await _reply(send, 503, "token verifier unavailable")
        except Exception:  # any verification failure denies; never fall through
            return await _reply(send, 401, "invalid token", www_authenticate=True)
        email = str(claims.get("email", "")).lower()
        if not claims.get("email_verified") or email not in self.allowed:
            return await _reply(send, 403, "caller not allowed")
        scope.setdefault("state", {})["caller"] = email
        return await self.app(scope, receive, send)
