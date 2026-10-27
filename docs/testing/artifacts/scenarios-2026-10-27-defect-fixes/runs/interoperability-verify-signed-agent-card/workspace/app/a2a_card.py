"""Fetch the partner's A2A agent card and refuse it unless its JWS signature verifies.

The trust anchor is the key set agreed out of band (settings.partner_jwks_url), never the
`jku` inside the card being checked. Anything that fails raises CardRefused; the caller then
does not build the remote agent.
"""
from __future__ import annotations

from typing import Any, Callable, Iterable, Mapping
from urllib.parse import urlsplit

ALGORITHMS = ["ES256"]  # asymmetric only; the partner signs with ES256


class CardRefused(Exception):
    """The card is not trusted; do not delegate to it."""


def _origin(url: str) -> tuple[str, str, int | None]:
    parts = urlsplit(url)
    return parts.scheme, (parts.hostname or "").lower(), parts.port or (443 if parts.scheme == "https" else None)


def check_rpc_origins(rpc_urls: Iterable[str], card_url: str) -> None:
    """Every RPC target must be https on the origin the card came from.

    ADK skips this check for a card handed in as an object, so we do it here.
    """
    urls = list(rpc_urls)
    if not urls:
        raise CardRefused("card declares no RPC interface")
    expected = _origin(card_url)
    if expected[0] != "https":
        raise CardRefused(f"card URL is not https: {card_url}")
    for url in urls:
        if _origin(url) != expected:
            raise CardRefused(f"RPC URL {url} is not on the card's origin {expected[1]}")


def pinned_key_provider(jwks: Mapping[str, Any], allowed_kids: Iterable[str]) -> Callable[..., Any]:
    """Key provider for a2a.utils.signing.create_signature_verifier.

    Looks keys up in the pinned JWKS by `kid` only and ignores `jku`. An unknown or
    non-allowlisted kid raises a jwt.PyJWTError subclass so the verifier can move on to the
    next signature (any other exception type aborts verification).
    """
    import jwt  # PyJWT, from a2a-sdk[signing]
    from jwt.algorithms import ECAlgorithm

    class UnknownKeyId(jwt.PyJWTError):
        pass

    allowed = set(allowed_kids)
    keys = {}
    for jwk in jwks.get("keys", []):
        kid = jwk.get("kid")
        if kid in allowed and jwk.get("kty") == "EC":
            keys[kid] = ECAlgorithm.from_jwk(jwk)

    def provider(kid: str | None, jku: str | None = None):
        if kid not in keys:
            raise UnknownKeyId(f"key id {kid!r} is not in the pinned key set")
        return keys[kid]

    return provider


async def fetch_pinned_jwks(jwks_url: str, httpx_client) -> dict:
    if urlsplit(jwks_url).scheme != "https":
        raise CardRefused("partner JWKS URL must be https")
    response = await httpx_client.get(jwks_url)
    response.raise_for_status()
    return response.json()


async def fetch_verified_card(card_url: str, jwks_url: str, allowed_kids: Iterable[str], httpx_client):
    """Return an AgentCard whose signature verified against the pinned key set, or raise CardRefused."""
    from a2a.client import A2ACardResolver
    from a2a.utils.signing import create_signature_verifier

    jwks = await fetch_pinned_jwks(jwks_url, httpx_client)
    verifier = create_signature_verifier(pinned_key_provider(jwks, allowed_kids), ALGORITHMS)
    parts = urlsplit(card_url)
    resolver = A2ACardResolver(httpx_client=httpx_client, base_url=f"{parts.scheme}://{parts.netloc}",
                               agent_card_path=parts.path)
    try:
        card = await resolver.get_agent_card(signature_verifier=verifier)
    except Exception as exc:  # bad or missing signature, unknown kid, HTTP or parse failure
        raise CardRefused(f"card not verified: {exc}") from exc
    check_rpc_origins([i.url for i in card.supported_interfaces], card_url)
    return card
