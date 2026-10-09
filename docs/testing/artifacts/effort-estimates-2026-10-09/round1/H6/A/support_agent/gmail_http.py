"""HTTP adapters for Google OAuth and the Gmail API (httpx).

Not exercised against Google yet; see tickets/T-202.md Evidence. Errors carry
no response bodies so tokens and email content stay out of logs.
"""
from __future__ import annotations

import httpx

from .gmail_oauth import InvalidGrant, ProviderError, TokenResponse
from .gmail_tool import GmailUnavailable, ResourceUnauthorized

TOKEN_URL = "https://oauth2.googleapis.com/token"
REVOKE_URL = "https://oauth2.googleapis.com/revoke"
USERINFO_URL = "https://openidconnect.googleapis.com/v1/userinfo"
GMAIL_API = "https://gmail.googleapis.com/gmail/v1/users/me"
TIMEOUT = httpx.Timeout(5.0, connect=3.0)


class GoogleOAuthProvider:
    def __init__(self, client_id: str, client_secret: str, http: httpx.Client | None = None):
        self._client_id = client_id
        self._client_secret = client_secret  # loaded from Secret Manager at start-up, never from code
        self._http = http or httpx.Client(timeout=TIMEOUT)

    def _token(self, form: dict) -> TokenResponse:
        try:
            resp = self._http.post(TOKEN_URL, data={**form, "client_id": self._client_id,
                                                    "client_secret": self._client_secret})
        except httpx.HTTPError:
            raise ProviderError("token endpoint unreachable") from None
        if resp.status_code == 400 and _json(resp).get("error") == "invalid_grant":
            raise InvalidGrant("invalid_grant")
        if resp.status_code != 200:
            raise ProviderError(f"token endpoint HTTP {resp.status_code}")
        body = _json(resp)
        if not isinstance(body.get("access_token"), str):
            raise ProviderError("malformed token response")
        return TokenResponse(access_token=body["access_token"], expires_in=int(body.get("expires_in", 0)),
                             scopes=tuple(str(body.get("scope", "")).split()),
                             refresh_token=body.get("refresh_token"))

    def exchange_code(self, code: str, code_verifier: str, redirect_uri: str) -> TokenResponse:
        return self._token({"grant_type": "authorization_code", "code": code,
                            "code_verifier": code_verifier, "redirect_uri": redirect_uri})

    def refresh(self, refresh_token: str) -> TokenResponse:
        return self._token({"grant_type": "refresh_token", "refresh_token": refresh_token})

    def account_id(self, access_token: str) -> str:
        try:
            resp = self._http.get(USERINFO_URL, headers={"Authorization": f"Bearer {access_token}"})
        except httpx.HTTPError:
            raise ProviderError("userinfo unreachable") from None
        sub = _json(resp).get("sub") if resp.status_code == 200 else None
        if not isinstance(sub, str) or not sub:
            raise ProviderError("userinfo failed")
        return sub

    def revoke(self, token: str) -> None:
        try:
            resp = self._http.post(REVOKE_URL, data={"token": token})
        except httpx.HTTPError:
            raise ProviderError("revoke unreachable") from None
        if resp.status_code not in (200, 400):  # 400: already invalid
            raise ProviderError(f"revoke HTTP {resp.status_code}")


class HttpxGmailClient:
    def __init__(self, http: httpx.Client | None = None):
        self._http = http or httpx.Client(timeout=TIMEOUT)

    def _get(self, access_token: str, path: str, params: dict) -> dict:
        try:
            resp = self._http.get(f"{GMAIL_API}/{path}", params=params,
                                  headers={"Authorization": f"Bearer {access_token}"})
        except httpx.HTTPError:
            raise GmailUnavailable("gmail unreachable") from None
        if resp.status_code == 401:
            raise ResourceUnauthorized()
        if resp.status_code != 200:
            raise GmailUnavailable(f"gmail HTTP {resp.status_code}")
        return _json(resp)

    def list_message_ids(self, access_token: str, query: str, max_results: int) -> list[str]:
        body = self._get(access_token, "messages", {"q": query, "maxResults": max_results})
        return [m["id"] for m in body.get("messages", []) if isinstance(m.get("id"), str)]

    def get_message(self, access_token: str, message_id: str) -> dict:
        return self._get(access_token, f"messages/{message_id}", {"format": "full"})


def _json(resp: httpx.Response) -> dict:
    try:
        body = resp.json()
    except ValueError:
        return {}
    return body if isinstance(body, dict) else {}
