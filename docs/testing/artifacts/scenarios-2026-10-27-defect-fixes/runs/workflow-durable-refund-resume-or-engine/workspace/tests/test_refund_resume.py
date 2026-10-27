"""Replaying a resumed refund must not pay twice (incident 2026-10-21).

ADK resume re-runs the confirmed tool call. If the worker dies after the provider accepted the
refund but before the invocation's events were written, the next resume runs issue_refund again
with the same function-call id. These tests replay that, against a provider fake that
de-duplicates on Idempotency-Key like the real one. No SDK, no network.
"""
import unittest

from app.clients.http import Response
from app.tools.refunds import issue_refund
from tests.fakes import FakeToolContext, FakeTransport, configure_fakes


class DedupingProvider(FakeTransport):
    """Creates a refund per new Idempotency-Key; a repeated key returns the original."""

    def __init__(self) -> None:
        super().__init__()
        self.by_key: dict[str, str] = {}

    def request(self, method, url, *, json=None, headers=None, timeout=10.0):
        super().request(method, url, json=json, headers=headers, timeout=timeout)
        key = (headers or {}).get("Idempotency-Key")
        if not key:
            return Response(400, {})
        refund = self.by_key.setdefault(key, f"re_{len(self.by_key) + 1}")
        return Response(200, {"id": refund})


def setup():
    store, _, _ = configure_fakes()
    from app import services
    provider = DedupingProvider()
    services.get().payments.transport = provider
    return store, provider


def ctx(call_id="call-1"):
    return FakeToolContext(user_id="cust-ana", function_call_id=call_id)


class RefundReplayTest(unittest.TestCase):
    def test_replayed_resume_pays_once(self):
        store, provider = setup()
        first = issue_refund("HO-10442", 6_400, "damaged", ctx())
        second = issue_refund("HO-10442", 6_400, "damaged", ctx())  # second approval, same call
        self.assertEqual(first, second)
        self.assertEqual(len(provider.by_key), 1)
        self.assertEqual(len(store.refunds_for("HO-10442")), 1)

    def test_crash_after_provider_accepts_pays_once(self):
        store, provider = setup()
        real = store.record_refund
        calls = {"n": 0}

        def die_once(*args, **kwargs):
            calls["n"] += 1
            if calls["n"] == 1:
                raise RuntimeError("pod evicted")
            return real(*args, **kwargs)

        store.record_refund = die_once
        with self.assertRaises(RuntimeError):
            issue_refund("HO-10442", 6_400, "damaged", ctx())
        result = issue_refund("HO-10442", 6_400, "damaged", ctx())
        self.assertEqual(result["status"], "refunded")
        self.assertEqual(len(provider.by_key), 1)  # provider saw the key twice, paid once
        self.assertEqual(len(provider.requests), 2)
        self.assertEqual(len({r["headers"]["Idempotency-Key"] for r in provider.requests}), 1)
        self.assertEqual(len(store.refunds_for("HO-10442")), 1)

    def test_a_separate_request_is_a_separate_refund(self):
        store, provider = setup()
        issue_refund("HO-10442", 3_000, "damaged", ctx("call-1"))
        issue_refund("HO-10442", 3_000, "damaged", ctx("call-2"))
        self.assertEqual(len(provider.by_key), 2)

    def test_without_a_call_id_nothing_is_paid(self):
        _, provider = setup()
        result = issue_refund("HO-10442", 6_400, "damaged", ctx(call_id=None))
        self.assertEqual(result["status"], "error")
        self.assertEqual(provider.requests, [])


if __name__ == "__main__":
    unittest.main()
