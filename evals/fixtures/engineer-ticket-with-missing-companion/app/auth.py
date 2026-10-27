"""Verified caller from the IAP assertion."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Mapping


class Unauthenticated(Exception):
    pass


@dataclass(frozen=True)
class Principal:
    user_id: str
    email: str


def principal_from_headers(headers: Mapping[str, str], verify: Callable[[str, str], Mapping[str, str]],
                           audience: str) -> Principal:
    assertion = headers.get("x-goog-iap-jwt-assertion")
    if not assertion:
        raise Unauthenticated("missing assertion")
    try:
        claims = verify(assertion, audience)
    except Exception as exc:
        raise Unauthenticated("invalid assertion") from exc
    if not claims.get("sub"):
        raise Unauthenticated("no subject")
    return Principal(claims["sub"], claims.get("email", ""))
