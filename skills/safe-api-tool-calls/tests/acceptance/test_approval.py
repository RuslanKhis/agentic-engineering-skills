"""Independent oracle for confirmation freshness and dispatch effects."""

import asyncio
import socket
import unittest
from unittest.mock import patch

from _support import load_service


service = load_service()
APPROVAL = {"operation_id": "op-1", "actor": "operator-1", "reference": "R-1",
            "revision": 3, "amount": "12.50", "currency": "USD", "confirmed": True}


class Store:
    def __init__(self, **changes):
        self.action = {**APPROVAL, "authorised": True, "refundable": True, **changes}

    async def current(self, operation_id):
        return dict(self.action)


class Provider:
    def __init__(self):
        self.effects = []

    async def refund(self, action):
        self.effects.append(dict(action))
        return {"refund_id": "fixture-refund"}


class ApprovalAcceptance(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        guard = patch.object(socket.socket, "connect",
                             side_effect=AssertionError("network forbidden"))
        guard.start()
        self.addCleanup(guard.stop)

    async def test_matching_current_approval_dispatches_once(self):
        provider = Provider()
        result = await service.execute_refund(Store(), provider, dict(APPROVAL))
        self.assertEqual(set(result), {"ok", "reason", "data"})
        self.assertTrue(result["ok"])
        self.assertEqual(result["data"], {"refund_id": "fixture-refund"})
        self.assertEqual(len(provider.effects), 1)

    async def test_changed_action_or_authority_never_dispatches(self):
        variants = ({"revision": 4}, {"amount": "25.00"}, {"currency": "EUR"},
                    {"reference": "R-2"}, {"actor": "operator-2"},
                    {"operation_id": "op-2"}, {"authorised": False}, {"refundable": False})
        for changes in variants:
            with self.subTest(changes=changes):
                provider = Provider()
                result = await service.execute_refund(Store(**changes), provider, dict(APPROVAL))
                self.assertFalse(result["ok"])
                self.assertIsNone(result["data"])
                self.assertTrue(result["reason"])
                self.assertEqual(provider.effects, [])

    async def test_declined_confirmation_never_dispatches(self):
        provider = Provider()
        result = await service.execute_refund(Store(), provider, {**APPROVAL, "confirmed": False})
        self.assertFalse(result["ok"])
        self.assertEqual(provider.effects, [])

    async def test_cancellation_propagates_without_another_effect(self):
        started = asyncio.Event()

        class Stalled(Provider):
            async def refund(self, action):
                self.effects.append(dict(action))
                started.set()
                await asyncio.Event().wait()

        provider = Stalled()
        task = asyncio.create_task(service.execute_refund(Store(), provider, dict(APPROVAL)))
        await asyncio.wait_for(started.wait(), 1)
        task.cancel()
        with self.assertRaises(asyncio.CancelledError):
            await task
        self.assertEqual(len(provider.effects), 1)
