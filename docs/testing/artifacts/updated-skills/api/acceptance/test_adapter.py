"""Independent oracle; give the candidate only its request and fixture inputs."""

import importlib.util
import json
import logging
from pathlib import Path
import socket
import tempfile
import unittest
from unittest.mock import patch

import httpx

from _support import load_service


service = load_service()
PRIVATE = "SYNTHETIC_PRIVATE_PROVIDER_BODY"


class AdapterAcceptance(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.guard = patch.object(socket.socket, "connect",
                                  side_effect=AssertionError("network forbidden"))
        self.guard.start()
        self.addCleanup(self.guard.stop)

    async def test_valid_read_and_refund_preserve_contract_and_client_ownership(self):
        read = {"reference": "R-1", "state": "ready"}
        paid = {"refund_id": "rf-1", "reference": "R-1", "amount": "12.50",
                "status": "applied"}
        calls = []

        async def handler(request):
            calls.append(request)
            return httpx.Response(200, json=read if request.method == "GET" else paid)

        async with httpx.AsyncClient(base_url="https://fixture.invalid",
                                     transport=httpx.MockTransport(handler)) as client:
            gateway = service.Gateway(client)
            first = await gateway.lookup("R-1")
            second = await gateway.refund("R-1", "12.50")
            for result, data, outcome in ((first, read, "read"), (second, paid, "applied")):
                self.assertEqual(set(result), {"ok", "data", "reason", "outcome"})
                self.assertTrue(result["ok"])
                self.assertEqual(result["data"], data)
                self.assertEqual(result["outcome"], outcome)
            self.assertEqual(len(calls), 2)
            self.assertFalse(client.is_closed)

    async def test_invalid_read_success_never_becomes_business_success(self):
        for payload in ({}, [], {"reference": "wrong", "state": "ready"},
                        {"reference": "R-1", "state": "invented"}):
            with self.subTest(payload=payload):
                async with httpx.AsyncClient(
                    base_url="https://fixture.invalid",
                    transport=httpx.MockTransport(lambda request: httpx.Response(200, json=payload)),
                ) as client:
                    result = await service.Gateway(client).lookup("R-1")
                self.assertFalse(result["ok"])
                self.assertIsNone(result["data"])
                self.assertEqual(result["outcome"], "unavailable")

    async def test_ambiguous_refund_has_one_effect_and_unknown_result(self):
        for variant in ("missing_fields", "wrong_reference", "invalid_json", "lost_response"):
            with self.subTest(variant=variant):
                effects = []

                async def handler(request):
                    effects.append(json.loads(request.content))
                    if variant == "lost_response":
                        raise httpx.ReadTimeout(PRIVATE, request=request)
                    if variant == "invalid_json":
                        return httpx.Response(200, text=PRIVATE)
                    payload = {} if variant == "missing_fields" else {
                        "refund_id": "rf-1", "reference": "wrong", "amount": "12.50",
                        "status": "applied",
                    }
                    return httpx.Response(200, json=payload)

                async with httpx.AsyncClient(base_url="https://fixture.invalid",
                                             transport=httpx.MockTransport(handler)) as client:
                    result = await service.Gateway(client).refund("R-1", "12.50")
                self.assertEqual(len(effects), 1)
                self.assertFalse(result["ok"])
                self.assertIsNone(result["data"])
                self.assertEqual(result["outcome"], "unknown")
                self.assertNotIn(PRIVATE, repr(result))

    async def test_invalid_money_never_dispatches(self):
        calls = []

        def forbidden(request):
            calls.append(request)
            return httpx.Response(200, json={})

        async with httpx.AsyncClient(base_url="https://fixture.invalid",
                                     transport=httpx.MockTransport(forbidden)) as client:
            for amount in ("NaN", "-1.00", "0.00", "1.001", True):
                with self.subTest(amount=amount):
                    result = await service.Gateway(client).refund("R-1", amount)
                    self.assertFalse(result["ok"])
                    self.assertEqual(result["outcome"], "not_attempted")
                    self.assertEqual(calls, [])

    async def test_contract_valid_leading_zero_amount_is_preserved(self):
        calls = []
        paid = {"refund_id": "rf-1", "reference": "R-1", "amount": "01.00",
                "status": "applied"}

        async def handler(request):
            calls.append(json.loads(request.content))
            return httpx.Response(200, json=paid)

        async with httpx.AsyncClient(base_url="https://fixture.invalid",
                                     transport=httpx.MockTransport(handler)) as client:
            result = await service.Gateway(client).refund("R-1", "01.00")
        self.assertTrue(result["ok"])
        self.assertEqual(result["outcome"], "applied")
        self.assertEqual(result["data"], paid)
        self.assertEqual(calls, [{"reference": "R-1", "amount": "01.00"}])

    async def test_literal_exception_source_is_absent_from_structured_logs(self):
        records = []

        class Capture(logging.Handler):
            def emit(self, record):
                records.append(record)

        # Keep the canary literal in a real module: format_tb includes its
        # source line even when exception messages themselves are omitted.
        temp = tempfile.TemporaryDirectory(prefix="provider-exception-")
        self.addCleanup(temp.cleanup)
        source = Path(temp.name) / "local_provider.py"
        source.write_text(
            'async def handler(request):\n'
            '    raise RuntimeError("SYNTHETIC_LITERAL_EXCEPTION_PAYLOAD")\n',
            encoding="utf-8",
        )
        spec = importlib.util.spec_from_file_location("local_provider", source)
        provider = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(provider)

        capture = Capture()
        root_logger = logging.getLogger()
        root_logger.addHandler(capture)
        self.addCleanup(root_logger.removeHandler, capture)
        async with httpx.AsyncClient(base_url="https://fixture.invalid",
                                     transport=httpx.MockTransport(provider.handler)) as client:
            result = await service.Gateway(client).lookup("R-1")
        self.assertFalse(result["ok"])
        self.assertEqual(result["outcome"], "unavailable")
        self.assertTrue(result["reason"])
        self.assertTrue(records, "Unexpected defects must retain safe diagnostics")
        captured = repr(result) + "\n".join(
            record.getMessage() + repr(record.__dict__) for record in records
        )
        self.assertNotIn("SYNTHETIC_LITERAL_EXCEPTION_PAYLOAD", captured)

    async def test_diagnostics_do_not_disclose_provider_body(self):
        messages = []

        class Capture(logging.Handler):
            def emit(self, record):
                messages.append(self.format(record))

        capture = Capture()
        root_logger = logging.getLogger()
        root_logger.addHandler(capture)
        self.addCleanup(root_logger.removeHandler, capture)
        async with httpx.AsyncClient(
            base_url="https://fixture.invalid",
            transport=httpx.MockTransport(lambda request: httpx.Response(400, text=PRIVATE)),
        ) as client:
            result = await service.Gateway(client).lookup("R-1")
        self.assertFalse(result["ok"])
        self.assertTrue(result["reason"])
        self.assertNotIn(PRIVATE, repr(result) + "\n".join(messages))
