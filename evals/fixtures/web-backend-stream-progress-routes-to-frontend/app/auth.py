"""The verified caller: an Identity Platform ID token sent as a bearer token."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Mapping


class Unauthenticated(Exception):
    pass


@dataclass(frozen=True)
class Principal:
    user_id: str
    email: str


# verify(token, audience) -> claims; production passes google.oauth2.id_token.verify_firebase_token.
Verifier = Callable[[str, str], Mapping[str, str]]


def principal_from_headers(headers: Mapping[str, str], verify: Verifier, audience: str) -> Principal:
    header = headers.get("authorization", "")
    scheme, _, token = header.partition(" ")
    if scheme.lower() != "bearer" or not token:
        raise Unauthenticated("missing bearer token")
    try:
        claims = verify(token, audience)
    except Exception as exc:  # bad signature, audience or expiry
        raise Unauthenticated("invalid token") from exc
    subject = claims.get("sub")
    if not subject:
        raise Unauthenticated("token has no subject")
    return Principal(user_id=subject, email=claims.get("email", ""))
