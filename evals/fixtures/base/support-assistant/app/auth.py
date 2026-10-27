"""The verified caller. The FastAPI dependency turns the IAP assertion into a Principal."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Mapping


class Unauthenticated(Exception):
    pass


@dataclass(frozen=True)
class Principal:
    user_id: str
    email: str


# verify(assertion, audience) -> claims; production passes google.oauth2.id_token.verify_token.
Verifier = Callable[[str, str], Mapping[str, str]]


def principal_from_headers(headers: Mapping[str, str], verify: Verifier, audience: str) -> Principal:
    assertion = headers.get("x-goog-iap-jwt-assertion")
    if not assertion:
        raise Unauthenticated("missing IAP assertion")
    try:
        claims = verify(assertion, audience)
    except Exception as exc:  # the verifier raises on a bad signature, audience or expiry
        raise Unauthenticated("invalid IAP assertion") from exc
    subject = claims.get("sub")
    if not subject:
        raise Unauthenticated("assertion has no subject")
    return Principal(user_id=subject, email=claims.get("email", ""))
