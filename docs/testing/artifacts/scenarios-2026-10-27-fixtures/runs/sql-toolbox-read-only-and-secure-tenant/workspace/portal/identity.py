"""Who is calling: the verified IAP assertion in front of the portal."""
from __future__ import annotations

import os
from typing import Callable

IAP_HEADER = "x-goog-iap-jwt-assertion"
IAP_ISSUER = "https://cloud.google.com/iap"
IAP_CERTS_URL = "https://www.gstatic.com/iap/verify/public_key"


class IdentityError(Exception):
    """The caller could not be authenticated."""


def _google_verifier(token: str, audience: str) -> dict:
    # Imported lazily: checks the ES256 signature, expiry and audience against Google's IAP keys.
    from google.auth.transport import requests
    from google.oauth2 import id_token

    return id_token.verify_token(token, requests.Request(), audience=audience, certs_url=IAP_CERTS_URL)


def claims_from_iap_header(headers: dict, audience: str | None = None,
                           verifier: Callable[[str, str], dict] = _google_verifier) -> dict:
    """Return the verified claims of the IAP assertion, or raise IdentityError (fail closed)."""
    audience = audience or os.environ.get("IAP_AUDIENCE", "")
    if not audience:
        raise IdentityError("IAP_AUDIENCE is not configured")
    token = headers.get(IAP_HEADER, "")
    if not token:
        raise IdentityError("missing IAP assertion")
    try:
        claims = verifier(token, audience)
    except Exception as exc:  # any verification failure is a refusal
        raise IdentityError("IAP assertion failed verification") from exc
    if claims.get("iss") != IAP_ISSUER or claims.get("aud") != audience or not claims.get("email"):
        raise IdentityError("IAP assertion has unexpected issuer, audience or subject")
    return claims


def customer_id_for(claims: dict, directory: dict) -> str | None:
    """Map the signed-in email to the customer account it belongs to."""
    return directory.get(claims.get("email", ""))
