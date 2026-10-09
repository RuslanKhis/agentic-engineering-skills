"""Per-customer Gmail connections (delegated OAuth) for the support agent.

Standard library only, so it can be tested without the ADK SDK. Provider HTTP,
token storage and the connection index are injected; the in-memory stores at the
bottom are for tests and local development only.

Boundary: verified customer principal -> their own connection record -> their
own refresh token (held in the vault, never in prompts or ADK state) -> a
short-lived access token for the read-only Gmail scope.
"""
from __future__ import annotations

import base64
import dataclasses
import hashlib
import secrets
import threading
import time
import urllib.parse
from typing import Protocol

GMAIL_READONLY_SCOPE = "https://www.googleapis.com/auth/gmail.readonly"
REQUESTED_SCOPES = ("openid", GMAIL_READONLY_SCOPE)
GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"

CONSENT_TTL_SECONDS = 600
ACCESS_TOKEN_SAFETY_SECONDS = 60


# --- errors -----------------------------------------------------------------

class ConsentRejected(Exception):
    """Callback failed validation; no code exchange or linking happened."""


class NotConnected(Exception):
    """The principal has no usable Gmail connection (connect or reconnect)."""


class TemporarilyUnavailable(Exception):
    """Provider or store outage; the connection is preserved."""


class InvalidGrant(Exception):
    """Token endpoint rejected the refresh token (revoked or expired)."""


class ProviderError(Exception):
    """Any other provider failure (quota, 5xx, timeout, malformed body)."""


# --- records ----------------------------------------------------------------

@dataclasses.dataclass(frozen=True)
class OAuthConfig:
    client_id: str
    redirect_uri: str
    environment: str  # binds records so staging cannot select production tokens


@dataclasses.dataclass(frozen=True)
class ConsentTransaction:
    state: str
    principal: str
    browser_binding_hash: str
    code_verifier: str
    client_id: str
    redirect_uri: str
    scopes: tuple[str, ...]
    expires_at: float


@dataclasses.dataclass(frozen=True)
class Connection:
    principal: str
    environment: str
    client_id: str
    provider_account: str  # Google OIDC `sub` of the mailbox owner
    granted_scopes: tuple[str, ...]
    credential_ref: str | None
    status: str  # "connected" | "reauth_required" | "disconnected"
    revision: int
    pending_cleanup: tuple[str, ...] = ()  # refs whose revoke/destroy failed


@dataclasses.dataclass(frozen=True)
class TokenResponse:
    access_token: str
    expires_in: int
    scopes: tuple[str, ...]
    refresh_token: str | None = None


# --- injected boundaries ----------------------------------------------------

class OAuthProvider(Protocol):
    def exchange_code(self, code: str, code_verifier: str, redirect_uri: str) -> TokenResponse: ...
    def refresh(self, refresh_token: str) -> TokenResponse: ...
    def account_id(self, access_token: str) -> str: ...
    def revoke(self, token: str) -> None: ...


class TokenVault(Protocol):
    """Protected payload store (e.g. Secret Manager); returns opaque references."""
    def put(self, principal: str, payload: str) -> str: ...
    def get(self, ref: str) -> str: ...
    def destroy(self, ref: str) -> None: ...


class ConnectionIndex(Protocol):
    def get(self, principal: str, environment: str) -> Connection | None: ...
    def compare_and_set(self, new: Connection, expected_revision: int | None) -> bool: ...


class ConsentStore(Protocol):
    def put(self, txn: ConsentTransaction) -> None: ...
    def consume(self, state: str) -> ConsentTransaction | None:
        """Atomically remove and return the transaction (single use)."""


# --- service ----------------------------------------------------------------

def _hash(value: str) -> str:
    return hashlib.sha256(value.encode()).hexdigest()


class GmailConnectionService:
    def __init__(self, config: OAuthConfig, provider: OAuthProvider, vault: TokenVault,
                 index: ConnectionIndex, consents: ConsentStore, clock=time.time):
        self._config = config
        self._provider = provider
        self._vault = vault
        self._index = index
        self._consents = consents
        self._clock = clock
        self._access_cache: dict[tuple[str, int], tuple[str, float]] = {}
        self._locks: dict[str, threading.Lock] = {}
        self._locks_guard = threading.Lock()

    # Consent ---------------------------------------------------------------

    def start_consent(self, principal: str) -> tuple[str, str]:
        """Begin consent for an authenticated customer.

        Returns (authorization_url, browser_binding). The caller stores the
        browser binding in a Secure, HttpOnly, SameSite=Lax cookie and
        redirects the browser to the URL.
        """
        if not principal:
            raise NotConnected("missing principal")
        state = secrets.token_urlsafe(32)
        browser_binding = secrets.token_urlsafe(32)
        verifier = secrets.token_urlsafe(64)
        challenge = base64.urlsafe_b64encode(hashlib.sha256(verifier.encode()).digest()).rstrip(b"=").decode()
        self._consents.put(ConsentTransaction(
            state=state, principal=principal, browser_binding_hash=_hash(browser_binding),
            code_verifier=verifier, client_id=self._config.client_id,
            redirect_uri=self._config.redirect_uri, scopes=REQUESTED_SCOPES,
            expires_at=self._clock() + CONSENT_TTL_SECONDS,
        ))
        query = urllib.parse.urlencode({
            "client_id": self._config.client_id,
            "redirect_uri": self._config.redirect_uri,
            "response_type": "code",
            "scope": " ".join(REQUESTED_SCOPES),
            "state": state,
            "code_challenge": challenge,
            "code_challenge_method": "S256",
            "access_type": "offline",
            "prompt": "consent",
        })
        return f"{GOOGLE_AUTH_URL}?{query}", browser_binding

    def complete_consent(self, principal: str, state: str, code: str, browser_binding: str) -> Connection:
        """Handle the OAuth callback for the currently signed-in customer."""
        txn = self._consents.consume(state) if state else None
        if (txn is None
                or txn.expires_at < self._clock()
                or txn.principal != principal
                or not browser_binding
                or not secrets.compare_digest(txn.browser_binding_hash, _hash(browser_binding))
                or txn.client_id != self._config.client_id
                or txn.redirect_uri != self._config.redirect_uri):
            raise ConsentRejected("invalid consent transaction")

        try:
            tokens = self._provider.exchange_code(code, txn.code_verifier, txn.redirect_uri)
            if GMAIL_READONLY_SCOPE not in tokens.scopes:
                # Google lets the customer untick the Gmail box; do not keep a useless grant.
                try:
                    self._provider.revoke(tokens.refresh_token or tokens.access_token)
                except Exception:  # noqa: BLE001
                    pass
                raise ConsentRejected("gmail.readonly not granted")
            account = self._provider.account_id(tokens.access_token)
        except InvalidGrant:
            raise ConsentRejected("code exchange failed") from None
        except ProviderError:
            # The code is single use; the customer starts a fresh consent.
            raise TemporarilyUnavailable("provider unavailable") from None

        existing = self._index.get(principal, self._config.environment)
        refresh_token = tokens.refresh_token
        reuse_ref = None
        if refresh_token is None:
            # Keep the stored token only for the same account and client on an active connection.
            if (existing and existing.status == "connected" and existing.credential_ref
                    and existing.provider_account == account and existing.client_id == self._config.client_id):
                reuse_ref = existing.credential_ref
            else:
                raise ConsentRejected("no refresh token issued")

        new_ref = reuse_ref or self._vault.put(principal, refresh_token)
        new = Connection(
            principal=principal, environment=self._config.environment,
            client_id=self._config.client_id, provider_account=account,
            granted_scopes=tuple(sorted(tokens.scopes)), credential_ref=new_ref,
            status="connected", revision=(existing.revision + 1) if existing else 1,
            pending_cleanup=existing.pending_cleanup if existing else (),
        )
        if not self._index.compare_and_set(new, existing.revision if existing else None):
            if reuse_ref is None:
                self._vault.destroy(new_ref)
            raise ConsentRejected("connection changed concurrently; retry")
        if existing and existing.credential_ref and existing.credential_ref != new_ref:
            self._retire(new, existing.credential_ref)
        self._access_cache[(principal, new.revision)] = (tokens.access_token, self._clock() + tokens.expires_in)
        return new

    # Use -------------------------------------------------------------------

    def status(self, principal: str) -> str:
        conn = self._index.get(principal, self._config.environment)
        return conn.status if conn else "not_connected"

    def access_token(self, principal: str) -> str:
        """Short-lived Gmail access token for this principal's own connection."""
        if not principal:
            raise NotConnected("missing principal")
        with self._lock_for(principal):
            conn = self._index.get(principal, self._config.environment)
            if (conn is None or conn.status != "connected" or not conn.credential_ref
                    or conn.client_id != self._config.client_id
                    or GMAIL_READONLY_SCOPE not in conn.granted_scopes):
                raise NotConnected(conn.status if conn else "not_connected")
            cached = self._access_cache.get((principal, conn.revision))
            if cached and cached[1] - ACCESS_TOKEN_SAFETY_SECONDS > self._clock():
                return cached[0]
            refresh_token = self._vault.get(conn.credential_ref)
            try:
                tokens = self._provider.refresh(refresh_token)
            except InvalidGrant:
                # Only the revision that failed moves to reauth_required.
                self._index.compare_and_set(dataclasses.replace(conn, status="reauth_required", revision=conn.revision + 1), conn.revision)
                raise NotConnected("reauth_required") from None
            except ProviderError:
                raise TemporarilyUnavailable("token refresh unavailable") from None
            current = conn
            if tokens.refresh_token and tokens.refresh_token != refresh_token:
                new_ref = self._vault.put(principal, tokens.refresh_token)
                current = dataclasses.replace(conn, credential_ref=new_ref, revision=conn.revision + 1)
                if not self._index.compare_and_set(current, conn.revision):
                    self._vault.destroy(new_ref)
                    raise TemporarilyUnavailable("connection changed during refresh")
                self._retire(current, conn.credential_ref, revoke=False)
            elif self._index.get(principal, self._config.environment) != conn:
                raise TemporarilyUnavailable("connection changed during refresh")
            self._access_cache[(principal, current.revision)] = (tokens.access_token, self._clock() + tokens.expires_in)
            return tokens.access_token

    def invalidate_access_token(self, principal: str) -> None:
        """Drop cached access tokens after a resource-server 401 (consent is kept)."""
        for key in [k for k in self._access_cache if k[0] == principal]:
            self._access_cache.pop(key, None)

    # Disconnect ------------------------------------------------------------

    def disconnect(self, principal: str) -> Connection | None:
        """Block new use locally first, then revoke at Google and destroy the token."""
        with self._lock_for(principal):
            conn = self._index.get(principal, self._config.environment)
            if conn is None:
                return None
            if conn.status != "disconnected":
                disconnected = dataclasses.replace(conn, status="disconnected", credential_ref=None, revision=conn.revision + 1)
                if not self._index.compare_and_set(disconnected, conn.revision):
                    raise TemporarilyUnavailable("connection changed; retry disconnect")
                self.invalidate_access_token(principal)
                conn = disconnected if not conn.credential_ref else self._retire(disconnected, conn.credential_ref)
            return conn

    # Internals -------------------------------------------------------------

    def _lock_for(self, principal: str) -> threading.Lock:
        with self._locks_guard:
            return self._locks.setdefault(principal, threading.Lock())

    def _retire(self, current: Connection, ref: str, revoke: bool = True) -> Connection:
        """Revoke and destroy an old credential; record failures for reconciliation."""
        try:
            if revoke:
                self._provider.revoke(self._vault.get(ref))
            self._vault.destroy(ref)
            return current
        except Exception:  # noqa: BLE001 - recorded, never reconnects
            pending = dataclasses.replace(current, pending_cleanup=current.pending_cleanup + (ref,))
            return pending if self._index.compare_and_set(pending, current.revision) else current


# --- in-memory stores (tests / local development only) ----------------------

class InMemoryVault:
    def __init__(self):
        self._data: dict[str, str] = {}

    def put(self, principal: str, payload: str) -> str:
        ref = f"vault/{_hash(principal)[:12]}/{secrets.token_hex(8)}"
        self._data[ref] = payload
        return ref

    def get(self, ref: str) -> str:
        return self._data[ref]

    def destroy(self, ref: str) -> None:
        self._data.pop(ref, None)


class InMemoryIndex:
    def __init__(self):
        self._rows: dict[tuple[str, str], Connection] = {}
        self._lock = threading.Lock()

    def get(self, principal: str, environment: str) -> Connection | None:
        return self._rows.get((principal, environment))

    def compare_and_set(self, new: Connection, expected_revision: int | None) -> bool:
        with self._lock:
            key = (new.principal, new.environment)
            current = self._rows.get(key)
            if (current.revision if current else None) != expected_revision:
                return False
            self._rows[key] = new
            return True


class InMemoryConsentStore:
    def __init__(self):
        self._rows: dict[str, ConsentTransaction] = {}
        self._lock = threading.Lock()

    def put(self, txn: ConsentTransaction) -> None:
        with self._lock:
            self._rows[txn.state] = txn

    def consume(self, state: str) -> ConsentTransaction | None:
        with self._lock:
            return self._rows.pop(state, None)
