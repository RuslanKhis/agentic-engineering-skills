"""Who is calling: read from the IAP header in front of the portal."""
from __future__ import annotations

import base64
import json


def claims_from_iap_header(headers: dict) -> dict:
    """Return the claims of the IAP JWT assertion (header x-goog-iap-jwt-assertion)."""
    token = headers.get("x-goog-iap-jwt-assertion", "")
    parts = token.split(".")
    if len(parts) != 3:
        return {}
    payload = parts[1] + "=" * (-len(parts[1]) % 4)
    return json.loads(base64.urlsafe_b64decode(payload))


def customer_id_for(claims: dict, directory: dict) -> str | None:
    """Map the signed-in email to the customer account it belongs to."""
    return directory.get(claims.get("email", ""))
