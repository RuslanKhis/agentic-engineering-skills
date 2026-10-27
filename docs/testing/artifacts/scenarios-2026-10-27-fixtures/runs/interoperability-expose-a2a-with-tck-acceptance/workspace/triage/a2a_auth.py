"""Bearer-token gate for the A2A app. No google.adk or a2a imports.

The middleware only decides; token verification is injected so tests need no
keys or network. `make_jwt_verifier` is the production verifier (PyJWT).
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field

CARD_PATH = "/.well-known/agent-card.json"


class TokenInvalid(Exception):
    """Signature, issuer, audience, expiry or format check failed."""


class VerifierUnavailable(Exception):
    """The key set could not be fetched; deny, but do not ask for a new sign-in."""


@dataclass(frozen=True)
class Principal:
    """Duck-types starlette's BaseUser, which a2a-sdk reads from scope["user"]."""

    subject: str
    scopes: frozenset[str] = field(default_factory=frozenset)

    @property
    def is_authenticated(self) -> bool:
        return True

    @property
    def display_name(self) -> str:
        return self.subject

    @property
    def identity(self) -> str:
        return self.subject


def principal_from_claims(claims: dict) -> Principal:
    subject = claims.get("sub")
    if not isinstance(subject, str) or not subject:
        raise TokenInvalid("no subject")
    raw = claims.get("scope", claims.get("scp", ""))
    scopes = raw.split() if isinstance(raw, str) else list(raw)
    return Principal(subject, frozenset(scopes))


class BearerAuthMiddleware:
    """401 missing/invalid token, 403 missing scope, 503 verifier outage.

    Only GET of the agent card is unauthenticated.
    """

    def __init__(self, app, verifier, required_scope: str):
        self.app = app
        self.verifier = verifier
        self.required_scope = required_scope

    async def __call__(self, scope, receive, send):
        if scope["type"] not in ("http", "websocket"):
            return await self.app(scope, receive, send)
        if scope["type"] == "http" and scope["method"] == "GET" and scope["path"] == CARD_PATH:
            return await self.app(scope, receive, send)
        if scope["type"] == "websocket":
            return await self._deny(send, 403, "websocket not supported")

        token = self._bearer(scope)
        if token is None:
            return await self._deny(send, 401, "missing bearer token", challenge='Bearer')
        try:
            principal = principal_from_claims(self.verifier(token))
        except VerifierUnavailable:
            return await self._deny(send, 503, "cannot verify token")
        except TokenInvalid:
            return await self._deny(send, 401, "invalid token", challenge='Bearer error="invalid_token"')
        if self.required_scope not in principal.scopes:
            return await self._deny(
                send, 403, "insufficient scope",
                challenge=f'Bearer error="insufficient_scope", scope="{self.required_scope}"',
            )
        scope["user"] = principal
        return await self.app(scope, receive, send)

    @staticmethod
    def _bearer(scope) -> str | None:
        for name, value in scope["headers"]:
            if name.lower() == b"authorization":
                scheme, _, token = value.decode("latin-1").partition(" ")
                if scheme.lower() == "bearer" and token.strip():
                    return token.strip()
                return None
        return None

    @staticmethod
    async def _deny(send, status: int, message: str, challenge: str | None = None):
        headers = [(b"content-type", b"application/json")]
        if challenge and status in (401, 403):
            headers.append((b"www-authenticate", challenge.encode()))
        await send({"type": "http.response.start", "status": status, "headers": headers})
        await send({"type": "http.response.body", "body": json.dumps({"error": message}).encode()})


def make_jwt_verifier(jwks_url: str, issuer: str, audience: str, leeway: int = 30):
    """Production verifier. Needs PyJWT[crypto], which pyproject does not pin yet."""
    import jwt  # lazy: not installed in the dev sandbox

    client = jwt.PyJWKClient(jwks_url)

    def verify(token: str) -> dict:
        try:
            key = client.get_signing_key_from_jwt(token).key
            return jwt.decode(
                token, key, algorithms=["RS256", "ES256"], issuer=issuer, audience=audience,
                leeway=leeway, options={"require": ["exp", "iss", "aud", "sub"]},
            )
        except jwt.PyJWKClientConnectionError as exc:
            raise VerifierUnavailable(str(exc)) from exc
        except jwt.PyJWTError as exc:
            raise TokenInvalid(str(exc)) from exc

    return verify
