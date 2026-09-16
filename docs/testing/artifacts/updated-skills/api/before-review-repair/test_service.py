"""Offline tests for ``service.Gateway`` using a local httpx transport double.

Run: python -m unittest -v test_service   (or python -m pytest test_service.py)
"""

import asyncio
import json
import logging
import unittest

import httpx

from service import Gateway

SECRET = "SENSITIVE-MARKER-4242"
REFERENCE = "case-123"


class Provider:
    """Local transport double: records requests and counts applied refunds."""

    def __init__(self, handler):
        self.handler = handler
        self.requests = []
        self.applied_refunds = 0

    async def __call__(self, request):
        if request.url.host != "provider.test":
            raise AssertionError("unexpected destination")
        self.requests.append(request)
        return await self.handler(self, request)


def respond(status, body):
    async def handler(provider, request):
        if isinstance(body, (dict, list, str, int)) and not isinstance(body, bytes):
            return httpx.Response(status, json=body)
        return httpx.Response(status, content=body)
    return handler


def raise_error(error_type):
    async def handler(provider, request):
        raise error_type(f"boom {SECRET}", request=request)
    return handler


def applied_body(**overrides):
    body = {"refund_id": "rf_1", "reference": REFERENCE, "amount": "10.00",
            "status": "applied"}
    body.update(overrides)
    return body


class GatewayTestCase(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.clients = []

    async def asyncTearDown(self):
        for client in self.clients:
            await client.aclose()

    def gateway(self, handler):
        provider = Provider(handler)
        client = httpx.AsyncClient(
            transport=httpx.MockTransport(provider),
            base_url="https://provider.test",
            timeout=httpx.Timeout(5.0),
        )
        self.clients.append(client)
        return Gateway(client), provider, client

    def assert_schema(self, result, ok, outcome):
        self.assertEqual(set(result), {"ok", "data", "reason", "outcome"})
        self.assertIs(result["ok"], ok)
        self.assertEqual(result["outcome"], outcome)
        if ok:
            self.assertIsNone(result["reason"])
        else:
            self.assertIsNone(result["data"])
            self.assertIsInstance(result["reason"], str)

    def assert_no_leak(self, result, logs):
        text = json.dumps(result, default=str) + "\n".join(
            f"{record.getMessage()} {record.__dict__.get('provider_call')}"
            for record in logs.records
        )
        self.assertNotIn(SECRET, text)


class LookupTests(GatewayTestCase):
    async def test_valid_states_are_read(self):
        for state in ("ready", "pending"):
            body = {"reference": REFERENCE, "state": state}
            gateway, provider, _ = self.gateway(respond(200, body))
            result = await gateway.lookup(REFERENCE)
            self.assert_schema(result, True, "read")
            self.assertEqual(result["data"], body)
            [request] = provider.requests
            self.assertEqual(request.method, "GET")
            self.assertEqual(request.url.path, "/status")
            self.assertEqual(request.url.params["reference"], REFERENCE)

    async def test_invalid_success_bodies_are_unavailable(self):
        cases = {
            "wrong state": ({"reference": REFERENCE, "state": "done"}, "state"),
            "other reference": ({"reference": "case-999", "state": "ready"},
                                "reference"),
            "missing state": ({"reference": REFERENCE}, "state"),
            "non-string state": ({"reference": REFERENCE, "state": ["ready"]},
                                 "state"),
            "array body": ([{"reference": REFERENCE, "state": "ready"}], "$"),
        }
        for name, (body, field) in cases.items():
            with self.subTest(name):
                gateway, provider, _ = self.gateway(respond(200, body))
                result = await gateway.lookup(REFERENCE)
                self.assert_schema(result, False, "unavailable")
                self.assertEqual(result["reason"], f"invalid_response:200:{field}")
                self.assertEqual(len(provider.requests), 1)

    async def test_http_errors_are_single_attempt_and_do_not_leak_body(self):
        for status in (400, 401, 404, 429, 500, 503):
            with self.subTest(status=status), self.assertLogs("service") as logs:
                gateway, provider, _ = self.gateway(
                    respond(status, {"error": SECRET, "reference": REFERENCE,
                                     "state": "ready"}))
                result = await gateway.lookup(REFERENCE)
                self.assert_schema(result, False, "unavailable")
                self.assertEqual(result["reason"], f"http_status:{status}")
                self.assertEqual(len(provider.requests), 1)
                self.assert_no_leak(result, logs)
                self.assertEqual(logs.records[0].provider_call["http_status"], status)

    async def test_malformed_json_is_unavailable(self):
        gateway, _, _ = self.gateway(respond(200, f"{{not json {SECRET}".encode()))
        with self.assertLogs("service") as logs:
            result = await gateway.lookup(REFERENCE)
        self.assert_schema(result, False, "unavailable")
        self.assertEqual(result["reason"], "invalid_json:200")
        self.assert_no_leak(result, logs)

    async def test_transport_errors_are_classified_without_messages(self):
        cases = {httpx.ReadTimeout: "transport_timeout",
                 httpx.ConnectTimeout: "transport_timeout",
                 httpx.ConnectError: "transport_error",
                 httpx.RemoteProtocolError: "transport_error"}
        for error_type, code in cases.items():
            with self.subTest(error_type.__name__), self.assertLogs("service") as logs:
                gateway, provider, _ = self.gateway(raise_error(error_type))
                result = await gateway.lookup(REFERENCE)
                self.assert_schema(result, False, "unavailable")
                self.assertEqual(result["reason"], code)
                self.assertEqual(len(provider.requests), 1)
                fields = logs.records[0].provider_call
                self.assertEqual(fields["error_class"], error_type.__name__)
                self.assert_no_leak(result, logs)

    async def test_unexpected_defect_is_logged_as_error_without_message(self):
        async def broken(provider, request):
            raise RuntimeError(SECRET)
        gateway, _, _ = self.gateway(broken)
        with self.assertLogs("service", logging.ERROR) as logs:
            result = await gateway.lookup(REFERENCE)
        self.assert_schema(result, False, "unavailable")
        self.assertEqual(result["reason"], "unexpected_error")
        fields = logs.records[0].provider_call
        self.assertEqual(fields["error_class"], "RuntimeError")
        self.assertIn("broken", fields["error_frames"])
        self.assert_no_leak(result, logs)

    async def test_invalid_reference_makes_no_request(self):
        for reference in (None, 123, "", " case", "a\nb", "x" * 257):
            with self.subTest(reference=reference), self.assertLogs("service", logging.WARNING):
                gateway, provider, _ = self.gateway(respond(200, {}))
                result = await gateway.lookup(reference)
                self.assert_schema(result, False, "unavailable")
                self.assertEqual(result["reason"], "invalid_reference")
                self.assertEqual(provider.requests, [])

    async def test_caller_cancellation_propagates(self):
        started = asyncio.Event()

        async def stall(provider, request):
            started.set()
            await asyncio.Event().wait()
        gateway, provider, _ = self.gateway(stall)
        task = asyncio.create_task(gateway.lookup(REFERENCE))
        await started.wait()
        task.cancel()
        with self.assertRaises(asyncio.CancelledError):
            await task
        self.assertEqual(len(provider.requests), 1)

    async def test_gateway_does_not_close_caller_client(self):
        gateway, _, client = self.gateway(raise_error(httpx.ConnectError))
        await gateway.lookup(REFERENCE)
        self.assertFalse(client.is_closed)


class RefundTests(GatewayTestCase):
    async def test_confirmed_refund_is_applied_once(self):
        async def apply(provider, request):
            provider.applied_refunds += 1
            return httpx.Response(201, json=applied_body())
        gateway, provider, _ = self.gateway(apply)
        result = await gateway.refund(REFERENCE, "10.00")
        self.assert_schema(result, True, "applied")
        self.assertEqual(result["data"], applied_body())
        [request] = provider.requests
        self.assertEqual((request.method, request.url.path), ("POST", "/refunds"))
        self.assertEqual(json.loads(request.content),
                         {"reference": REFERENCE, "amount": "10.00"})

    async def test_lost_response_after_commit_is_unknown_and_not_replayed(self):
        for error_type in (httpx.ReadTimeout, httpx.RemoteProtocolError,
                           httpx.ReadError):
            with self.subTest(error_type.__name__), self.assertLogs("service") as logs:
                async def commit_then_lose(provider, request):
                    provider.applied_refunds += 1
                    raise error_type(f"lost {SECRET}", request=request)
                gateway, provider, _ = self.gateway(commit_then_lose)
                result = await gateway.refund(REFERENCE, "10.00")
                self.assert_schema(result, False, "unknown")
                self.assertTrue(result["reason"].startswith("refund_outcome_unknown:"))
                self.assertIn("reconcile", result["reason"])
                self.assertEqual(len(provider.requests), 1)
                self.assertEqual(provider.applied_refunds, 1)
                self.assertEqual(logs.records[0].levelno, logging.ERROR)
                self.assert_no_leak(result, logs)

    async def test_connect_failure_is_still_unknown(self):
        # httpx cannot prove that no bytes reached the provider.
        gateway, provider, _ = self.gateway(raise_error(httpx.ConnectError))
        with self.assertLogs("service"):
            result = await gateway.refund(REFERENCE, "10.00")
        self.assert_schema(result, False, "unknown")
        self.assertIn("transport_error", result["reason"])
        self.assertEqual(len(provider.requests), 1)

    async def test_http_error_statuses_are_unknown_single_attempt(self):
        for status in (400, 409, 422, 429, 500, 502, 503):
            with self.subTest(status=status), self.assertLogs("service") as logs:
                gateway, provider, _ = self.gateway(
                    respond(status, {"detail": SECRET}))
                result = await gateway.refund(REFERENCE, "10.00")
                self.assert_schema(result, False, "unknown")
                self.assertIn(f"http_status:{status}", result["reason"])
                self.assertEqual(len(provider.requests), 1)
                self.assert_no_leak(result, logs)

    async def test_unconfirmed_2xx_bodies_are_unknown(self):
        cases = {
            "pending status": (applied_body(status="pending"), "status"),
            "missing refund_id": ({k: v for k, v in applied_body().items()
                                   if k != "refund_id"}, "refund_id"),
            "empty refund_id": (applied_body(refund_id=""), "refund_id"),
            "numeric refund_id": (applied_body(refund_id=7), "refund_id"),
            "other reference": (applied_body(reference="case-999"), "reference"),
            "numeric amount": (applied_body(amount=10.0), "amount"),
            "different amount": (applied_body(amount="1000.00"), "amount"),
            "reformatted amount": (applied_body(amount="10.0"), "amount"),
            "array body": ([applied_body()], "$"),
        }
        for name, (body, field) in cases.items():
            with self.subTest(name), self.assertLogs("service"):
                gateway, provider, _ = self.gateway(respond(200, body))
                result = await gateway.refund(REFERENCE, "10.00")
                self.assert_schema(result, False, "unknown")
                self.assertIn(f"invalid_response:200:{field}", result["reason"])
                self.assertEqual(len(provider.requests), 1)

    async def test_empty_or_malformed_2xx_body_is_unknown(self):
        for content in (b"", f"<html>{SECRET}</html>".encode(), b"\xff\xfe"):
            with self.subTest(content=content), self.assertLogs("service") as logs:
                gateway, provider, _ = self.gateway(respond(200, content))
                result = await gateway.refund(REFERENCE, "10.00")
                self.assert_schema(result, False, "unknown")
                self.assertIn("invalid_json:200", result["reason"])
                self.assertEqual(len(provider.requests), 1)
                self.assert_no_leak(result, logs)

    async def test_unexpected_defect_after_dispatch_is_unknown_and_logged(self):
        async def broken(provider, request):
            raise RuntimeError(SECRET)
        gateway, _, _ = self.gateway(broken)
        with self.assertLogs("service", logging.ERROR) as logs:
            result = await gateway.refund(REFERENCE, "10.00")
        self.assert_schema(result, False, "unknown")
        self.assertIn("unexpected_error", result["reason"])
        self.assertEqual(logs.records[0].provider_call["error_class"], "RuntimeError")
        self.assert_no_leak(result, logs)

    async def test_invalid_amounts_make_no_request(self):
        from decimal import Decimal
        amounts = [10, 10.0, Decimal("10.00"), True, None, "10", "10.0", "10.001",
                   "0.00", "-1.00", "+1.00", "01.00", "1e3", "NaN", "Infinity",
                   " 10.00", "10.00 ", "1,000.00", "١٠.٠٠", "9" * 16 + ".00",
                   "9" * 10_000 + ".00"]
        for amount in amounts:
            with self.subTest(amount=str(amount)[:20]), self.assertLogs("service", logging.WARNING):
                gateway, provider, _ = self.gateway(respond(200, applied_body()))
                result = await gateway.refund(REFERENCE, amount)
                self.assert_schema(result, False, "not_attempted")
                self.assertEqual(result["reason"], "invalid_amount")
                self.assertEqual(provider.requests, [])

    async def test_boundary_amounts_are_accepted(self):
        for amount in ("0.01", "999999999999999.99"):
            with self.subTest(amount=amount):
                gateway, provider, _ = self.gateway(
                    respond(200, applied_body(amount=amount)))
                result = await gateway.refund(REFERENCE, amount)
                self.assert_schema(result, True, "applied")
                self.assertEqual(len(provider.requests), 1)

    async def test_invalid_reference_makes_no_request(self):
        for reference in (None, "", "a\tb", "x" * 257):
            with self.subTest(reference=reference), self.assertLogs("service", logging.WARNING):
                gateway, provider, _ = self.gateway(respond(200, applied_body()))
                result = await gateway.refund(reference, "10.00")
                self.assert_schema(result, False, "not_attempted")
                self.assertEqual(result["reason"], "invalid_reference")
                self.assertEqual(provider.requests, [])

    async def test_cancellation_after_dispatch_propagates_and_logs_unknown(self):
        started = asyncio.Event()

        async def commit_then_stall(provider, request):
            provider.applied_refunds += 1
            started.set()
            await asyncio.Event().wait()
        gateway, provider, _ = self.gateway(commit_then_stall)
        with self.assertLogs("service", logging.ERROR) as logs:
            task = asyncio.create_task(gateway.refund(REFERENCE, "10.00"))
            await started.wait()
            task.cancel()
            with self.assertRaises(asyncio.CancelledError):
                await task
        self.assertEqual(len(provider.requests), 1)
        self.assertEqual(provider.applied_refunds, 1)
        fields = logs.records[0].provider_call
        self.assertEqual((fields["outcome"], fields["reason_code"]),
                         ("unknown", "cancelled_after_dispatch"))

    async def test_logs_exclude_reference_and_amount(self):
        gateway, _, _ = self.gateway(respond(500, {}))
        with self.assertLogs("service") as logs:
            await gateway.refund("case-PRIVATE", "12345.67")
        rendered = str([(r.getMessage(), r.provider_call) for r in logs.records])
        self.assertNotIn("case-PRIVATE", rendered)
        self.assertNotIn("12345.67", rendered)


if __name__ == "__main__":
    unittest.main()
