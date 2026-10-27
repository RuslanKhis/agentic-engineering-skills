"""The leak detector itself: it must flag known leaks and stay quiet on ordinary traffic. No ADK."""
from __future__ import annotations

import logging
import unittest

from tests.fakes import FakeTransport
from tests.runner import canaries
from tests.runner.leak_guard import LeakGuard, scan_text

LIVE_KEY = "hpk_live_" + "ab" * 16
RELAY = "hmr-" + "123e4567-e89b-12d3-a456-426614174000"
JWT = "eyJhbGciOiJSUzI1NiJ9." + "eyJzdWIiOiJ1MSJ9." + "c2lnbmF0dXJl"
OTHER_CARD = "4111 1111 1111 1111"  # Luhn-valid, not one of our canaries


def kinds(text, **kw):
    return {f.kind for f in scan_text(text, "t", **kw)}


class DetectorTests(unittest.TestCase):
    def test_each_canary_is_found(self):
        for value in canaries.ALL:
            self.assertTrue(scan_text(f"x {value} y", "t"), value)

    def test_reformatted_digits_are_found(self):
        self.assertIn("canary", kinds("card 4000-0000-0000-0417"))
        self.assertIn("canary", kinds("call 447700900417"))

    def test_credential_formats(self):
        self.assertIn("payments_key", kinds(f"key={LIVE_KEY}"))
        self.assertIn("mail_relay_token", kinds(f"token {RELAY}"))
        self.assertIn("jwt", kinds(f"Bearer {JWT}"))

    def test_shapes_beyond_the_canaries(self):
        self.assertIn("card_number", kinds(f"pay with {OTHER_CARD}"))
        self.assertIn("email", kinds("write to someone.else@example.org"))
        self.assertIn("phone", kinds("ring +44 7700 900123 today"))

    def test_ordinary_traffic_is_clean(self):
        text = ('{"order_id": "HO-10442", "amount_cents": 8900, "timestamp": 1730000000.123456, '
                '"id": "123e4567-e89b-12d3-a456-426614174000", "status": "delivered"}')
        self.assertEqual(scan_text(text, "t"), [])

    def test_findings_never_print_the_value(self):
        for f in scan_text(f"{canaries.EMAIL} {LIVE_KEY}", "t"):
            self.assertNotIn(canaries.EMAIL, str(f))
            self.assertNotIn(LIVE_KEY, str(f))

    def test_shapes_off_allows_recipient_but_not_credentials_or_cards(self):
        self.assertEqual(scan_text('{"to": "a.person@example.org"}', "t", shapes=False), [])
        self.assertIn("payments_key", kinds(LIVE_KEY, shapes=False))
        self.assertIn("card_number", kinds(OTHER_CARD, shapes=False))


class GuardTests(unittest.TestCase):
    def setUp(self):
        self.guard = LeakGuard()
        self.guard.start()
        self.addCleanup(self.guard.stop)

    def test_log_leak_is_caught_including_lazy_args(self):
        logging.getLogger("support.agent").info("reply for %s", canaries.EMAIL)
        self.assertTrue(any(f.sink.startswith("log") for f in self.guard.findings()))

    def test_clean_log_passes(self):
        logging.getLogger("support.agent").info("turn start session %s", "s-1")
        self.assertEqual(self.guard.findings(), [])

    def test_model_request_event_and_session_leaks_are_caught(self):
        self.guard.model_requests.append({"contents": [{"text": canaries.CARD}]})
        self.guard.events.append({"args": {"note": LIVE_KEY}})
        self.guard.sessions.append({"state": {"t": RELAY}})
        sinks = {f.sink.split("[")[0] for f in self.guard.findings()}
        self.assertEqual(sinks, {"model_request", "event", "session"})

    def test_tool_call_body_leak_is_caught_but_auth_header_is_not(self):
        transport = FakeTransport()
        transport.request("POST", "https://payments.test/v1/refunds",
                          json={"note": canaries.CARD}, headers={"Authorization": f"Bearer {LIVE_KEY}"})
        self.guard.provider_transports["payments"] = transport
        found = self.guard.findings()
        self.assertTrue(found)
        self.assertTrue(all(f.kind in ("canary", "card_number") for f in found))

    def test_logging_level_is_restored(self):
        before = logging.getLogger().level
        guard = LeakGuard()
        guard.start()
        guard.stop()
        self.assertEqual(logging.getLogger().level, before)


if __name__ == "__main__":
    unittest.main()
