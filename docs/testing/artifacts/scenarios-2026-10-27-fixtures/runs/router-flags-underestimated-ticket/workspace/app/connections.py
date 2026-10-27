"""Per-customer Gmail connection: consent transaction, credential custody and disconnect.

The user ID is always the verified principal's. Tokens live in a SecretStore; the SQLite index
holds only a reference. The Google provider and the Secret Manager store are injected, so this
module imports neither and tests run offline.
"""
from __future__ import annotations

import base64
import hashlib
import secrets
import time
from dataclasses import dataclass
from typing import Callable, Protocol

from app.store import Store

GMAIL_READONLY = "https://www.googleapis.com/auth/gmail.readonly"
TRANSACTION_TTL_SECONDS = 600


class ConnectionError_(Exception):
    """Base for outcomes the caller maps to a safe message."""


class InvalidTransaction(ConnectionError_):
    pass


class ScopeMismatch(ConnectionError_):
    pass


class NotConnected(ConnectionError_):
    pass


class ReconnectRequired(ConnectionError_):
    pass


class InvalidGrant(Exception):
    """Raised by a provider when the token endpoint rejects the refresh grant."""


class OAuthProvider(Protocol):
    def authorization_url(self, *, state: str, code_challenge: str, redirect_uri: str, scope: str) -> str: ...

    def exchange_code(self, *, code: str, code_verifier: str, redirect_uri: str) -> dict:
        """-> {"refresh_token", "scope", "account"}; `account` must come from a validated ID token."""

    def refresh_access_token(self, refresh_token: str) -> str: ...

    def revoke(self, token: str) -> None: ...


class SecretStore(Protocol):
    def put(self, user_id: str, payload: str) -> str: ...
    def get(self, ref: str) -> str: ...
    def disable(self, ref: str) -> None: ...


def _sha256(value: str) -> str:
    return hashlib.sha256(value.encode()).hexdigest()


@dataclass
class GmailConnections:
    store: Store
    provider: OAuthProvider
    secrets: SecretStore
    redirect_uri: str
    clock: Callable[[], float] = time.time

    def start(self, user_id: str) -> dict:
        """Begin consent. Returns the URL to open and the browser nonce to set as a protected cookie."""
        state = secrets.token_urlsafe(32)
        browser_nonce = secrets.token_urlsafe(32)
        verifier = secrets.token_urlsafe(64)
        challenge = base64.urlsafe_b64encode(hashlib.sha256(verifier.encode()).digest()).rstrip(b"=").decode()
        self.store.add_oauth_transaction(_sha256(state), user_id, _sha256(browser_nonce), verifier,
                                         self.redirect_uri, GMAIL_READONLY,
                                         int(self.clock()) + TRANSACTION_TTL_SECONDS)
        url = self.provider.authorization_url(state=state, code_challenge=challenge,
                                              redirect_uri=self.redirect_uri, scope=GMAIL_READONLY)
        return {"authorization_url": url, "browser_nonce": browser_nonce}

    def complete(self, user_id: str, state: str, browser_nonce: str, code: str) -> dict:
        """Finish consent. Nothing is exchanged unless state, principal, browser and expiry all check out."""
        tx = self.store.consume_oauth_transaction(_sha256(state), user_id, _sha256(browser_nonce),
                                                  int(self.clock()))
        if tx is None:
            raise InvalidTransaction("consent transaction is invalid, expired or already used")
        grant = self.provider.exchange_code(code=code, code_verifier=tx["code_verifier"],
                                            redirect_uri=tx["redirect_uri"])
        granted = set(grant.get("scope", "").split())
        if GMAIL_READONLY not in granted:
            raise ScopeMismatch("the read-only Gmail permission was not granted")
        if granted - {GMAIL_READONLY, "openid", "email"}:
            raise ScopeMismatch("broader permissions than requested were granted")
        refresh_token = grant.get("refresh_token")
        if not refresh_token:
            raise ScopeMismatch("no durable grant was returned; start the connection again")
        ref = self.secrets.put(user_id, refresh_token)
        revision = self.store.publish_gmail_connection(user_id, grant["account"], GMAIL_READONLY, ref)
        return {"status": "connected", "account": grant["account"], "revision": revision}

    def status(self, user_id: str) -> dict:
        conn = self.store.get_gmail_connection(user_id)
        if conn is None or conn["status"] != "connected":
            return {"status": "not_connected"}
        return {"status": "connected", "account": conn["provider_account"]}

    def disconnect(self, user_id: str) -> dict:
        """Local access is removed first; remote revocation and secret retirement follow and are reported."""
        before = self.store.disconnect_gmail_connection(user_id)
        if before is None:
            return {"status": "not_connected"}
        remote = "revoked"
        try:
            self.provider.revoke(self.secrets.get(before["secret_ref"]))
        except Exception:  # local removal already holds; reconciliation is a follow-up job
            remote = "revocation_pending"
        try:
            self.secrets.disable(before["secret_ref"])
        except Exception:
            remote = "revocation_pending"
        return {"status": "disconnected", "remote": remote}

    def access_token(self, user_id: str) -> str:
        """A short-lived access token for this user's own mailbox only."""
        conn = self.store.get_gmail_connection(user_id)
        if conn is None or conn["status"] != "connected":
            raise NotConnected("Gmail is not connected")
        try:
            return self.provider.refresh_access_token(self.secrets.get(conn["secret_ref"]))
        except InvalidGrant as exc:
            raise ReconnectRequired("Gmail access was withdrawn; connect again") from exc
