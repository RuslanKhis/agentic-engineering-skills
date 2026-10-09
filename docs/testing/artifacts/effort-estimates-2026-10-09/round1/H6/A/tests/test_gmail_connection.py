"""Offline tests for per-customer Gmail connections (doubles for Google; no ADK)."""
import base64
import types
import unittest
import urllib.parse

from support_agent import gmail_oauth as g
from support_agent import gmail_tool

CONFIG = g.OAuthConfig(client_id="client-1", redirect_uri="https://support.example/oauth/gmail/callback",
                       environment="pilot")


class FakeProvider:
    def __init__(self):
        self.exchanges = 0
        self.refreshes = 0
        self.revoked = []
        self.next_scopes = ("openid", g.GMAIL_READONLY_SCOPE)
        self.next_refresh_token = "rt-alice-1"
        self.account = "google-sub-alice"
        self.refresh_error = None
        self.refresh_rotates_to = None
        self.revoke_error = None

    def exchange_code(self, code, code_verifier, redirect_uri):
        self.exchanges += 1
        return g.TokenResponse(access_token=f"at-{code}", expires_in=3600, scopes=self.next_scopes,
                               refresh_token=self.next_refresh_token)

    def refresh(self, refresh_token):
        self.refreshes += 1
        if self.refresh_error:
            raise self.refresh_error
        return g.TokenResponse(access_token=f"at-refreshed-{self.refreshes}", expires_in=3600,
                               scopes=("openid", g.GMAIL_READONLY_SCOPE), refresh_token=self.refresh_rotates_to)

    def account_id(self, access_token):
        return self.account

    def revoke(self, token):
        if self.revoke_error:
            raise self.revoke_error
        self.revoked.append(token)


class Clock:
    def __init__(self):
        self.now = 1_000_000.0

    def __call__(self):
        return self.now


def make_service():
    provider, vault, index, clock = FakeProvider(), g.InMemoryVault(), g.InMemoryIndex(), Clock()
    service = g.GmailConnectionService(CONFIG, provider, vault, index, g.InMemoryConsentStore(), clock=clock)
    return service, provider, vault, index, clock


def connect(service, principal, code="code-1"):
    url, binding = service.start_consent(principal)
    state = urllib.parse.parse_qs(urllib.parse.urlparse(url).query)["state"][0]
    return service.complete_consent(principal, state, code, binding)


class ConsentTests(unittest.TestCase):
    def setUp(self):
        self.service, self.provider, self.vault, self.index, self.clock = make_service()

    def _start(self, principal="alice"):
        url, binding = self.service.start_consent(principal)
        return urllib.parse.parse_qs(urllib.parse.urlparse(url).query), binding

    def test_authorization_url_requests_readonly_offline_pkce(self):
        q, _ = self._start()
        self.assertEqual(q["scope"][0].split(), ["openid", g.GMAIL_READONLY_SCOPE])
        self.assertEqual(q["code_challenge_method"][0], "S256")
        self.assertEqual(q["access_type"][0], "offline")
        self.assertEqual(q["redirect_uri"][0], CONFIG.redirect_uri)

    def test_connect_stores_token_only_in_vault(self):
        conn = connect(self.service, "alice")
        self.assertEqual(conn.status, "connected")
        self.assertEqual(conn.provider_account, "google-sub-alice")
        self.assertNotIn("rt-alice-1", repr(conn))
        self.assertEqual(self.vault.get(conn.credential_ref), "rt-alice-1")

    def test_rejected_callbacks_never_exchange(self):
        cases = {"other signed-in customer": lambda s, b: ("bob", s, b),
                 "copied URL, other browser": lambda s, b: ("alice", s, "other-browser"),
                 "forged state": lambda s, b: ("alice", "forged-state", b),
                 "empty state": lambda s, b: ("alice", "", b)}
        for name, tamper in cases.items():
            with self.subTest(name):
                q, binding = self._start()
                principal, state, browser = tamper(q["state"][0], binding)
                with self.assertRaises(g.ConsentRejected):
                    self.service.complete_consent(principal, state, "code", browser)
        self.assertEqual(self.provider.exchanges, 0)

    def test_state_is_single_use_and_expires(self):
        q, binding = self._start()
        self.service.complete_consent("alice", q["state"][0], "c1", binding)
        with self.assertRaises(g.ConsentRejected):
            self.service.complete_consent("alice", q["state"][0], "c1", binding)
        q, binding = self._start()
        self.clock.now += g.CONSENT_TTL_SECONDS + 1
        with self.assertRaises(g.ConsentRejected):
            self.service.complete_consent("alice", q["state"][0], "c2", binding)
        self.assertEqual(self.provider.exchanges, 1)

    def test_missing_gmail_scope_is_rejected_and_revoked(self):
        self.provider.next_scopes = ("openid",)
        with self.assertRaises(g.ConsentRejected):
            connect(self.service, "alice")
        self.assertEqual(self.service.status("alice"), "not_connected")
        self.assertEqual(self.provider.revoked, ["rt-alice-1"])

    def test_omitted_refresh_token_reuses_only_same_account(self):
        first = connect(self.service, "alice")
        self.provider.next_refresh_token = None
        again = connect(self.service, "alice", code="c2")
        self.assertEqual(again.credential_ref, first.credential_ref)
        self.provider.account = "google-sub-someone-else"
        with self.assertRaises(g.ConsentRejected):
            connect(self.service, "alice", code="c3")
        self.assertEqual(self.index.get("alice", "pilot").provider_account, "google-sub-alice")

    def test_reconnect_with_new_token_retires_old(self):
        first = connect(self.service, "alice")
        self.provider.next_refresh_token = "rt-alice-2"
        second = connect(self.service, "alice", code="c2")
        self.assertGreater(second.revision, first.revision)
        self.assertIn("rt-alice-1", self.provider.revoked)
        with self.assertRaises(KeyError):
            self.vault.get(first.credential_ref)


class TokenLifecycleTests(unittest.TestCase):
    def setUp(self):
        self.service, self.provider, self.vault, self.index, self.clock = make_service()
        connect(self.service, "alice")
        self.provider.next_refresh_token = "rt-bob-1"
        self.provider.account = "google-sub-bob"
        connect(self.service, "bob")

    def test_each_principal_gets_own_token_and_unknown_is_denied(self):
        self.assertEqual(self.service.access_token("alice"), "at-code-1")
        self.clock.now += 7200
        self.service.access_token("alice")
        self.assertEqual(self.vault.get(self.index.get("bob", "pilot").credential_ref), "rt-bob-1")
        with self.assertRaises(g.NotConnected):
            self.service.access_token("mallory")
        with self.assertRaises(g.NotConnected):
            self.service.access_token("")

    def test_transient_refresh_failure_keeps_connection_and_recovers(self):
        self.clock.now += 7200
        self.provider.refresh_error = g.ProviderError("503")
        with self.assertRaises(g.TemporarilyUnavailable):
            self.service.access_token("alice")
        self.assertEqual(self.service.status("alice"), "connected")
        self.provider.refresh_error = None
        self.assertTrue(self.service.access_token("alice").startswith("at-refreshed"))

    def test_invalid_grant_requires_reauth_for_that_principal_only(self):
        self.clock.now += 7200
        self.provider.refresh_error = g.InvalidGrant()
        with self.assertRaises(g.NotConnected):
            self.service.access_token("alice")
        self.assertEqual(self.service.status("alice"), "reauth_required")
        self.assertEqual(self.service.status("bob"), "connected")

    def test_rotating_refresh_publishes_new_version(self):
        self.clock.now += 7200
        before = self.index.get("alice", "pilot")
        self.provider.refresh_rotates_to = "rt-alice-rotated"
        self.service.access_token("alice")
        after = self.index.get("alice", "pilot")
        self.assertEqual(self.vault.get(after.credential_ref), "rt-alice-rotated")
        with self.assertRaises(KeyError):
            self.vault.get(before.credential_ref)

    def test_disconnect_blocks_locally_even_if_revoke_fails(self):
        self.provider.revoke_error = g.ProviderError("timeout")
        conn = self.service.disconnect("alice")
        self.assertEqual(conn.status, "disconnected")
        self.assertEqual(len(conn.pending_cleanup), 1)
        with self.assertRaises(g.NotConnected):
            self.service.access_token("alice")  # cached access token no longer usable
        self.assertEqual(self.service.disconnect("alice").status, "disconnected")  # repeatable
        self.assertEqual(self.service.status("bob"), "connected")

    def test_disconnect_revokes_and_destroys(self):
        ref = self.index.get("alice", "pilot").credential_ref
        self.service.disconnect("alice")
        self.assertIn("rt-alice-1", self.provider.revoked)
        with self.assertRaises(KeyError):
            self.vault.get(ref)


def _gmail_message(text):
    return {"payload": {"mimeType": "multipart/alternative",
                        "headers": [{"name": "From", "value": "orders@acme.example"},
                                    {"name": "Subject", "value": "Your order A-10293"}],
                        "parts": [{"mimeType": "text/plain",
                                   "body": {"data": base64.urlsafe_b64encode(text.encode()).decode().rstrip("=")}}]}}


class FakeGmail:
    def __init__(self):
        self.calls = []
        self.unauthorized_once = False

    def list_message_ids(self, access_token, query, max_results):
        self.calls.append((access_token, query, max_results))
        if self.unauthorized_once:
            self.unauthorized_once = False
            raise gmail_tool.ResourceUnauthorized()
        return ["m1", "m2", "m3", "m4"]

    def get_message(self, access_token, message_id):
        return _gmail_message("Order A-10293: 2 x widget, EUR 40.00. " + "x" * 3000)


def ctx(user_id):
    return types.SimpleNamespace(session=types.SimpleNamespace(user_id=user_id))


class ToolTests(unittest.TestCase):
    def setUp(self):
        self.service, self.provider, *_ = make_service()
        connect(self.service, "alice")
        self.gmail = FakeGmail()
        gmail_tool.configure(self.service, self.gmail, ("orders@acme.example",))

    def tearDown(self):
        gmail_tool._service = gmail_tool._gmail = None

    def test_reads_own_mailbox_with_fixed_query_and_bounded_result(self):
        result = gmail_tool.read_order_confirmations("A-10293", ctx("alice"))
        self.assertEqual(result["status"], "success")
        self.assertEqual(len(result["emails"]), gmail_tool.MAX_MESSAGES)
        self.assertTrue(result["emails"][0]["truncated"])
        self.assertLessEqual(len(result["emails"][0]["text"]), gmail_tool.MAX_CHARS_PER_MESSAGE)
        self.assertEqual(self.gmail.calls, [("at-code-1", 'from:(orders@acme.example) "A-10293"', 3)])

    def test_not_connected_customer_gets_status_and_no_gmail_call(self):
        self.assertEqual(gmail_tool.read_order_confirmations("A-10293", ctx("bob"))["status"], "not_connected")
        self.assertEqual(self.gmail.calls, [])

    def test_query_injection_and_missing_identity_rejected_before_gmail(self):
        for bad in ['A-1" OR from:*', "in:anywhere", "", 42]:
            self.assertEqual(gmail_tool.read_order_confirmations(bad, ctx("alice"))["status"], "invalid_order_id")
        self.assertEqual(gmail_tool.read_order_confirmations("A-10293", ctx(None))["status"], "unavailable")
        self.assertEqual(self.gmail.calls, [])

    def test_resource_401_refreshes_once_and_keeps_consent(self):
        self.gmail.unauthorized_once = True
        result = gmail_tool.read_order_confirmations("A-10293", ctx("alice"))
        self.assertEqual(result["status"], "success")
        self.assertEqual(self.provider.refreshes, 1)
        self.assertEqual(self.service.status("alice"), "connected")

    def test_tool_signature_exposes_no_identity_argument(self):
        import inspect
        params = list(inspect.signature(gmail_tool.read_order_confirmations).parameters)
        self.assertEqual(params, ["order_id", "tool_context"])  # ADK injects tool_context

    def test_unconfigured_tool_fails_closed(self):
        gmail_tool._service = None
        self.assertEqual(gmail_tool.read_order_confirmations("A-10293", ctx("alice"))["status"], "unavailable")


if __name__ == "__main__":
    unittest.main()
