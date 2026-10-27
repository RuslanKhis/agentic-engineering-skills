"""Trust rules for the partner's signed A2A agent card. No google.adk import.

The key set is pinned from a file agreed out of band; the `jku` inside the card
being verified is never followed. a2a-sdk is imported lazily so the unit tests
run without it.
"""
from __future__ import annotations

import json
from urllib.parse import urlsplit

ALLOWED_ALGORITHMS = ["ES256"]


class CardRefused(Exception):
    """The partner card is not trusted; do not delegate to it."""


def _jwt_error_base():
    import jwt  # PyJWT, installed with a2a-sdk[signing]
    return jwt.PyJWTError


def _make_unknown_key_error():
    # The a2a-sdk verifier moves on to the next signature only for PyJWTError
    # subclasses; any other exception aborts verification.
    class UnknownCardKey(_jwt_error_base()):
        pass
    return UnknownCardKey


class PinnedKeyProvider:
    """key_provider(kid, jku) for a2a.utils.signing.create_signature_verifier.

    Only kids in `allowed_kids` that are present in the pinned JWKS are
    accepted, so a rotation (card-2026-10 -> card-2027-01) is a reviewed
    config change, and `jku` is ignored.
    """

    def __init__(self, jwks: dict, allowed_kids: set[str] | frozenset[str]) -> None:
        import jwt
        self._keys = {}
        for entry in jwks.get("keys", []):
            kid = entry.get("kid")
            if kid in allowed_kids and entry.get("kty") == "EC" and "d" not in entry:
                self._keys[kid] = jwt.PyJWK(entry)
        if not self._keys:
            raise CardRefused("pinned JWKS has none of the allowed key ids")
        self._error = _make_unknown_key_error()

    @classmethod
    def from_file(cls, path: str, allowed_kids) -> "PinnedKeyProvider":
        try:
            with open(path, encoding="utf-8") as fh:
                return cls(json.load(fh), frozenset(allowed_kids))
        except (OSError, ValueError) as exc:
            raise CardRefused(f"cannot load pinned partner JWKS {path!r}: {exc}") from exc

    def __call__(self, kid: str | None, jku: str | None = None):
        key = self._keys.get(kid or "")
        if key is None:
            raise self._error(f"key id {kid!r} is not pinned")
        return key


def origin_of(url: str) -> tuple[str, str, int]:
    parts = urlsplit(url)
    port = parts.port or (443 if parts.scheme == "https" else 80)
    return parts.scheme, (parts.hostname or "").lower(), port


def check_interface_origins(urls: list[str], card_url: str) -> None:
    """Every RPC URL must be https on the origin the card was fetched from.

    ADK skips its own same-origin check for a card passed as an object.
    """
    expected = origin_of(card_url)
    if expected[0] != "https":
        raise CardRefused(f"card URL is not https: {card_url}")
    if not urls:
        raise CardRefused("card declares no RPC interface URL")
    for url in urls:
        if origin_of(url) != expected:
            raise CardRefused(f"card RPC URL {url} is not on the card origin {card_url}")


def card_rpc_urls(card) -> list[str]:
    """RPC URLs of an a2a-sdk 1.x AgentCard (supportedInterfaces) or a 0.3 card (url)."""
    interfaces = getattr(card, "supported_interfaces", None) or []
    urls = [i.url for i in interfaces if getattr(i, "url", "")]
    legacy = getattr(card, "url", "")
    if legacy:
        urls.append(legacy)
    return urls


async def fetch_verified_card(card_url: str, key_provider, httpx_client):
    """Fetch the card and verify its signature; raise CardRefused otherwise."""
    from a2a.client.card_resolver import A2ACardResolver
    from a2a.utils.signing import create_signature_verifier

    base, _, path = card_url.partition("/.well-known/")
    resolver = A2ACardResolver(httpx_client=httpx_client, base_url=base,
                               agent_card_path="/.well-known/" + path)
    verifier = create_signature_verifier(key_provider, ALLOWED_ALGORITHMS)
    try:
        card = await resolver.get_agent_card(signature_verifier=verifier)
    except Exception as exc:  # any fetch, parse or signature failure refuses the card
        raise CardRefused(f"partner card rejected: {type(exc).__name__}: {exc}") from exc
    check_interface_origins(card_rpc_urls(card), card_url)
    return card
