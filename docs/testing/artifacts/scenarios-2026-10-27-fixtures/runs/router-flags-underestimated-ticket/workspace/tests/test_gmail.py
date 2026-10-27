import unittest

from app import connections, services
from app.clients.gmail import GmailClient
from app.clients.http import Response
from app.connections import (GMAIL_READONLY, GmailConnections, InvalidGrant, InvalidTransaction,
                             ScopeMismatch)
from app.tools.gmail import find_order_email
from tests.fakes import FakeToolContext, FakeTransport, configure_fakes


class FakeProvider:
    def __init__(self):
        self.exchanges = []
        self.revoked = []
        self.revoke_error = None
        self.refresh_error = None
        self.scope = GMAIL_READONLY
        self.refresh_token = "rt-1"

    def authorization_url(self, *, state, code_challenge, redirect_uri, scope):
        return f"https://accounts.test/auth?state={state}&scope={scope}"

    def exchange_code(self, *, code, code_verifier, redirect_uri):
        self.exchanges.append(code)
        return {"refresh_token": self.refresh_token, "scope": self.scope, "account": "ana@shop.test"}

    def refresh_access_token(self, refresh_token):
        if self.refresh_error:
            raise self.refresh_error
        return f"access-for-{refresh_token}"

    def revoke(self, token):
        if self.revoke_error:
            raise self.revoke_error
        self.revoked.append(token)


class FakeSecrets:
    def __init__(self):
        self.data, self.disabled = {}, []

    def put(self, user_id, payload):
        ref = f"secret-{user_id}-{len(self.data)}"
        self.data[ref] = payload
        return ref

    def get(self, ref):
        return self.data[ref]

    def disable(self, ref):
        self.disabled.append(ref)


class GmailTestCase(unittest.TestCase):
    def setUp(self):
        self.store, _, _ = configure_fakes()
        self.now = 1_000.0
        self.provider, self.secrets = FakeProvider(), FakeSecrets()
        self.conns = GmailConnections(self.store, self.provider, self.secrets,
                                      "https://app.test/oauth/callback", clock=lambda: self.now)
        self.gmail_transport = FakeTransport()
        services.get().connections = self.conns
        services.get().gmail = GmailClient(self.gmail_transport)

    def connect(self, user="cust-ana"):
        started = self.conns.start(user)
        state = started["authorization_url"].split("state=")[1].split("&")[0]
        return state, started["browser_nonce"]


class ConsentTests(GmailTestCase):
    def test_happy_path_requests_only_read_only_and_stores_a_reference(self):
        state, nonce = self.connect()
        result = self.conns.complete("cust-ana", state, nonce, "code-1")
        self.assertEqual(result["status"], "connected")
        row = self.store.get_gmail_connection("cust-ana")
        self.assertEqual(row["scopes"], GMAIL_READONLY)
        self.assertNotIn("rt-1", str(row))
        self.assertEqual(self.secrets.data[row["secret_ref"]], "rt-1")

    def test_other_principal_cannot_complete_and_no_exchange_happens(self):
        state, nonce = self.connect("cust-ana")
        with self.assertRaises(InvalidTransaction):
            self.conns.complete("cust-ben", state, nonce, "code-1")
        self.assertEqual(self.provider.exchanges, [])

    def test_other_browser_cannot_complete(self):
        state, _ = self.connect()
        with self.assertRaises(InvalidTransaction):
            self.conns.complete("cust-ana", state, "someone-elses-nonce", "code-1")
        self.assertEqual(self.provider.exchanges, [])

    def test_state_is_single_use(self):
        state, nonce = self.connect()
        self.conns.complete("cust-ana", state, nonce, "code-1")
        with self.assertRaises(InvalidTransaction):
            self.conns.complete("cust-ana", state, nonce, "code-1")
        self.assertEqual(len(self.provider.exchanges), 1)

    def test_expired_transaction_is_refused(self):
        state, nonce = self.connect()
        self.now += connections.TRANSACTION_TTL_SECONDS + 1
        with self.assertRaises(InvalidTransaction):
            self.conns.complete("cust-ana", state, nonce, "code-1")

    def test_unknown_state_is_refused(self):
        with self.assertRaises(InvalidTransaction):
            self.conns.complete("cust-ana", "forged", "x", "code-1")

    def test_broader_or_missing_scope_publishes_nothing(self):
        for scope in (GMAIL_READONLY + " https://mail.google.com/", "openid"):
            self.provider.scope = scope
            state, nonce = self.connect()
            with self.assertRaises(ScopeMismatch):
                self.conns.complete("cust-ana", state, nonce, "c")
            self.assertIsNone(self.store.get_gmail_connection("cust-ana"))

    def test_missing_refresh_token_publishes_nothing(self):
        self.provider.refresh_token = None
        state, nonce = self.connect()
        with self.assertRaises(ScopeMismatch):
            self.conns.complete("cust-ana", state, nonce, "c")
        self.assertIsNone(self.store.get_gmail_connection("cust-ana"))

    def test_reconnect_advances_the_revision(self):
        for _ in range(2):
            state, nonce = self.connect()
            self.conns.complete("cust-ana", state, nonce, "c")
        self.assertEqual(self.store.get_gmail_connection("cust-ana")["revision"], 2)


class DisconnectTests(GmailTestCase):
    def setUp(self):
        super().setUp()
        state, nonce = self.connect()
        self.conns.complete("cust-ana", state, nonce, "c")

    def test_disconnect_blocks_the_tool_revokes_and_retires_the_secret(self):
        result = self.conns.disconnect("cust-ana")
        self.assertEqual(result, {"status": "disconnected", "remote": "revoked"})
        self.assertEqual(self.provider.revoked, ["rt-1"])
        self.assertEqual(len(self.secrets.disabled), 1)
        self.assertEqual(find_order_email("HO-10442", FakeToolContext("cust-ana"))["status"], "not_connected")
        self.assertEqual(self.gmail_transport.requests, [])

    def test_failed_revocation_still_removes_local_access(self):
        self.provider.revoke_error = TimeoutError()
        result = self.conns.disconnect("cust-ana")
        self.assertEqual(result["remote"], "revocation_pending")
        self.assertEqual(self.conns.status("cust-ana")["status"], "not_connected")

    def test_repeated_disconnect_is_harmless(self):
        self.conns.disconnect("cust-ana")
        self.assertEqual(self.conns.disconnect("cust-ana")["status"], "not_connected")
        self.assertEqual(len(self.provider.revoked), 1)

    def test_disconnect_does_not_touch_another_customer(self):
        state, nonce = self.connect("cust-ben")
        self.conns.complete("cust-ben", state, nonce, "c")
        self.conns.disconnect("cust-ana")
        self.assertEqual(self.conns.status("cust-ben")["status"], "connected")


class FindOrderEmailTests(GmailTestCase):
    def setUp(self):
        super().setUp()
        state, nonce = self.connect("cust-ana")
        self.conns.complete("cust-ana", state, nonce, "c")
        self.gmail_transport.responses = [
            Response(200, {"messages": [{"id": "m1"}]}),
            Response(200, {"snippet": "Order HO-10442 confirmed, ships 3 Nov",
                           "payload": {"headers": [{"name": "From", "value": "sales@supplier.test"},
                                                   {"name": "Subject", "value": "Confirmation HO-10442"},
                                                   {"name": "Date", "value": "Mon, 2 Nov 2026"}]}}),
        ]

    def test_uses_the_signed_in_customers_token_and_returns_an_allowlist(self):
        result = find_order_email("HO-10442", FakeToolContext("cust-ana"))
        self.assertEqual(result["status"], "ok")
        self.assertEqual(set(result["emails"][0]), {"from", "subject", "date", "snippet"})
        for req in self.gmail_transport.requests:
            self.assertEqual(req["method"], "GET")
            self.assertEqual(req["headers"]["Authorization"], "Bearer access-for-rt-1")

    def test_customer_without_a_connection_never_reaches_gmail(self):
        result = find_order_email("HO-20001", FakeToolContext("cust-ben"))
        self.assertEqual(result["status"], "not_connected")
        self.assertEqual(self.gmail_transport.requests, [])

    def test_withdrawn_grant_asks_to_reconnect_and_keeps_the_connection(self):
        self.provider.refresh_error = InvalidGrant()
        result = find_order_email("HO-10442", FakeToolContext("cust-ana"))
        self.assertEqual(result["status"], "reconnect_required")
        self.assertEqual(self.conns.status("cust-ana")["status"], "connected")

    def test_provider_failure_is_unavailable_and_leaks_nothing(self):
        self.gmail_transport.responses = [Response(500, {"error": "boom rt-1"})]
        result = find_order_email("HO-10442", FakeToolContext("cust-ana"))
        self.assertEqual(result, {"status": "unavailable"})

    def test_quotes_in_the_order_id_cannot_widen_the_query(self):
        find_order_email('HO-1" OR in:anywhere', FakeToolContext("cust-ana"))
        self.assertNotIn("%22%20OR", self.gmail_transport.requests[0]["url"])


if __name__ == "__main__":
    unittest.main()
