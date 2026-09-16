"""Optional SDK-shaped integration tests; no credentials or provider calls."""

import asyncio
import importlib
from pathlib import Path
import socket
import sys
import types
import unittest
from unittest.mock import AsyncMock, patch


PACKAGE = "skill_test_sdp_assets"
package = types.ModuleType(PACKAGE)
package.__path__ = [str(Path(__file__).resolve().parents[1] / "assets")]
sys.modules[PACKAGE] = package
adapter = importlib.import_module(f"{PACKAGE}.google_sdp_adapter")
try:
    from google.cloud import dlp_v2 as dlp
except ImportError:
    dlp = None


def config(**changes):
    parent = "projects/fixture-project/locations/us-central1"
    values = dict(
        project="fixture-project", location="us-central1",
        deny_inspect=f"{parent}/inspectTemplates/deny",
        pii_inspect=f"{parent}/inspectTemplates/pii",
        deidentify=f"{parent}/deidentifyTemplates/replace",
    )
    return adapter.SdpTemplates(**(values | changes))


class ConfigTests(unittest.TestCase):
    def test_regional_endpoint_and_templates_are_bound(self):
        self.assertEqual(config().endpoint, "dlp.us-central1.rep.googleapis.com")
        self.assertEqual(config().parent, "projects/fixture-project/locations/us-central1")

    def test_invalid_or_foreign_config_rejected_before_sdk_start(self):
        for values in (
            {"project": ""}, {"project": "PRIVATE_INPUT/invalid"}, {"project": None},
            {"location": "global"}, {"location": "../invalid"},
            {"deny_inspect": "projects/foreign-project/locations/us-central1/inspectTemplates/deny"},
            {"pii_inspect": "projects/fixture-project/locations/europe-west1/inspectTemplates/pii"},
            {"deidentify": "projects/fixture-project/locations/us-central1/inspectTemplates/wrong"},
            {"deny_inspect": config().pii_inspect},
        ):
            with self.subTest(values=values), self.assertRaises(ValueError) as caught:
                config(**values)
            self.assertNotIn("PRIVATE_INPUT", str(caught.exception))

    def test_constructor_limits_and_laziness(self):
        with patch.object(importlib, "import_module", side_effect=AssertionError):
            instance = adapter.GoogleSdpProtector(config())
        self.assertIsNone(instance._client)
        for keyword in ("max_chars", "max_bytes", "max_concurrent"):
            for value in (0, -1, True, 1.5):
                with self.subTest(keyword=keyword, value=value), self.assertRaises(ValueError):
                    adapter.GoogleSdpProtector(config(), **{keyword: value})
        for keyword in ("timeout_s", "rpc_timeout_s"):
            for value in (0, -1, True, float("nan"), float("inf")):
                with self.subTest(keyword=keyword, value=value), self.assertRaises(ValueError):
                    adapter.GoogleSdpProtector(config(), **{keyword: value})


@unittest.skipIf(dlp is None, "Optional google-cloud-dlp SDK is not installed; adapter not verified.")
class AdapterTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        for name in ("connect", "connect_ex"):
            guard = patch.object(socket.socket, name, side_effect=AssertionError("network forbidden"))
            guard.start()
            self.addCleanup(guard.stop)
        guard = patch.object(socket, "create_connection", side_effect=AssertionError("network forbidden"))
        guard.start()
        self.addCleanup(guard.stop)
        self.calls = []
        self.inspect_response = dlp.InspectContentResponse(result=dlp.InspectResult())
        self.deidentify_response = dlp.DeidentifyContentResponse(
            item=dlp.ContentItem(value="Contact [EMAIL_ADDRESS]"),
            overview=dlp.TransformationOverview(),
        )

        async def inspect(**kwargs):
            self.calls.append(("inspect", kwargs))
            return self.inspect_response

        async def deidentify(**kwargs):
            self.calls.append(("deidentify", kwargs))
            return self.deidentify_response

        self.client = types.SimpleNamespace(
            inspect_content=inspect, deidentify_content=deidentify,
            transport=types.SimpleNamespace(close=AsyncMock()),
        )
        self.endpoints = []

        def factory(endpoint):
            self.endpoints.append(endpoint)
            return self.client

        self.factory = factory
        self.protector = adapter.GoogleSdpProtector(config(), client_factory=factory)
        await self.protector.start()
        self.addAsyncCleanup(self.protector.close)

    async def assert_blocked(self, protector=None, **options):
        with self.assertRaises(adapter.TextProtectionError) as caught:
            await (protector or self.protector).protect_text("Contact canary@example.test", **options)
        self.assertIsNone(caught.exception.__context__)
        self.assertIsNone(caught.exception.__cause__)
        self.assertNotIn("canary", str(caught.exception))

    async def test_request_types_routing_no_overrides_and_safe_handoff(self):
        text = await self.protector.protect_text("Contact canary@example.test")
        sinks = {name: text for name in ("history", "model", "tool")}
        self.assertNotIn("canary", repr(sinks))
        self.assertEqual(text, "Contact [EMAIL_ADDRESS]")
        self.assertEqual(self.endpoints, [config().endpoint])
        first, second = (entry[1] for entry in self.calls)
        self.assertIs(type(first["request"]), dlp.InspectContentRequest)
        self.assertIs(type(second["request"]), dlp.DeidentifyContentRequest)
        self.assertEqual(first["request"].inspect_template_name, config().deny_inspect)
        self.assertEqual(second["request"].inspect_template_name, config().pii_inspect)
        self.assertEqual(second["request"].deidentify_template_name, config().deidentify)
        self.assertEqual(first["request"].parent, config().parent)
        for entry in (first, second):
            self.assertIsNone(entry["retry"])
            self.assertTrue(0 < entry["timeout"] <= 5)
            self.assertFalse(type(entry["request"]).pb(entry["request"]).HasField("inspect_config"))
        self.assertFalse(dlp.DeidentifyContentRequest.pb(second["request"]).HasField("deidentify_config"))

    async def test_forbidden_truncated_missing_or_wrong_inspection_withholds(self):
        for response in (
            dlp.InspectContentResponse(result=dlp.InspectResult(findings=[dlp.Finding()])),
            dlp.InspectContentResponse(result=dlp.InspectResult(findings_truncated=True)),
            dlp.InspectContentResponse(result=dlp.InspectResult(findings=[dlp.Finding()], findings_truncated=True)),
            dlp.InspectContentResponse(), None, {},
        ):
            self.calls.clear()
            self.inspect_response = response
            await self.assert_blocked()
            self.assertEqual([kind for kind, _ in self.calls], ["inspect"])

    async def test_malformed_or_partial_transform_withholds(self):
        for response in (
            None, {}, dlp.DeidentifyContentResponse(),
            dlp.DeidentifyContentResponse(item=dlp.ContentItem(value="safe")),
            dlp.DeidentifyContentResponse(item=dlp.ContentItem(table=dlp.Table()), overview=dlp.TransformationOverview()),
            dlp.DeidentifyContentResponse(item=dlp.ContentItem(value="safe"), overview=dlp.TransformationOverview(transformed_bytes=1)),
            dlp.DeidentifyContentResponse(item=dlp.ContentItem(value="safe"), overview=dlp.TransformationOverview(transformation_summaries=[dlp.TransformationSummary()])),
            dlp.DeidentifyContentResponse(item=dlp.ContentItem(value="safe"), overview=dlp.TransformationOverview(transformation_summaries=[dlp.TransformationSummary(results=[dlp.TransformationSummary.SummaryResult(code=dlp.TransformationSummary.TransformationResultCode.ERROR)])])),
        ):
            self.deidentify_response = response
            await self.assert_blocked()

    async def test_complete_success_and_no_transform_are_accepted(self):
        self.deidentify_response.overview = dlp.TransformationOverview(
            transformed_bytes=1,
            transformation_summaries=[dlp.TransformationSummary(results=[
                dlp.TransformationSummary.SummaryResult(
                    code=dlp.TransformationSummary.TransformationResultCode.SUCCESS, count=1
                )
            ])],
        )
        self.assertEqual(await self.protector.protect_text("synthetic"), "Contact [EMAIL_ADDRESS]")
        self.deidentify_response = dlp.DeidentifyContentResponse(
            item=dlp.ContentItem(value="benign"), overview=dlp.TransformationOverview()
        )
        self.assertEqual(await self.protector.protect_text("benign"), "benign")

    async def test_utf8_input_and_output_byte_limits(self):
        limited = adapter.GoogleSdpProtector(config(), max_bytes=8, client_factory=self.factory)
        async with limited:
            with self.assertRaises(adapter.TextProtectionError):
                await limited.protect_text("é" * 5)
            self.assertEqual(self.calls, [])
            self.deidentify_response.item.value = "é" * 5
            with self.assertRaises(adapter.TextProtectionError):
                await limited.protect_text("safe")
            self.assertEqual(len(self.calls), 2)

    async def test_expired_invalid_or_shorter_host_deadline(self):
        for deadline in (-1, True, float("nan"), float("inf")):
            await self.assert_blocked(deadline=deadline)
        self.assertEqual(self.calls, [])
        await self.protector.protect_text("safe", deadline=asyncio.get_running_loop().time() + 0.5)
        self.assertTrue(all(0 < entry[1]["timeout"] <= 0.5 for entry in self.calls))
        self.assertLessEqual(self.calls[1][1]["timeout"], self.calls[0][1]["timeout"])

    async def test_queue_wait_consumes_budget_without_starting_rpc(self):
        await self.protector._slots.acquire()
        # Occupy every remaining slot as well; release only after this check.
        for _ in range(7):
            await self.protector._slots.acquire()
        try:
            await self.assert_blocked(deadline=asyncio.get_running_loop().time() + 0.005)
            self.assertEqual(self.calls, [])
        finally:
            for _ in range(8):
                self.protector._slots.release()

    async def test_provider_failure_is_generic_and_no_transform(self):
        async def fail(**kwargs):
            raise RuntimeError("PRIVATE_PROVIDER_DETAIL canary@example.test")
        self.client.inspect_content = fail
        await self.assert_blocked()
        self.assertEqual(self.calls, [])

    async def test_cancellation_propagates_and_releases_slot(self):
        entered = asyncio.Event()
        async def hold(**kwargs):
            entered.set()
            await asyncio.Future()
        self.client.inspect_content = hold
        task = asyncio.create_task(self.protector.protect_text("synthetic"))
        await entered.wait()
        task.cancel()
        with self.assertRaises(asyncio.CancelledError):
            await task
        self.assertEqual(self.protector._slots._value, 8)

    async def test_client_reuse_close_and_closed_guard(self):
        for _ in range(3):
            await self.protector.start()
            await self.protector.protect_text("synthetic")
        self.assertEqual(len(self.endpoints), 1)
        await self.protector.close()
        await self.protector.close()
        self.client.transport.close.assert_awaited_once()
        await self.assert_blocked()
        with self.assertRaises(RuntimeError):
            await self.protector.start()

    async def test_missing_start_and_close_failure(self):
        unused = adapter.GoogleSdpProtector(config(), client_factory=self.factory)
        await self.assert_blocked(unused)
        self.client.transport.close.side_effect = [RuntimeError("PRIVATE_CLOSE_DETAIL"), None]
        with self.assertRaises(adapter.TextProtectionError) as caught:
            await self.protector.close()
        self.assertNotIn("PRIVATE_CLOSE", str(caught.exception))
        await self.assert_blocked()
        await self.protector.close()
        self.assertEqual(self.client.transport.close.await_count, 2)

    async def test_startup_failure_is_generic_and_does_not_log(self):
        def unavailable(endpoint):
            raise RuntimeError("PRIVATE_ADC_DETAIL")
        failed = adapter.GoogleSdpProtector(config(), client_factory=unavailable)
        with self.assertRaises(adapter.TextProtectionError) as caught:
            await failed.start()
        self.assertNotIn("PRIVATE_ADC", str(caught.exception))
        self.assertIsNone(caught.exception.__context__)

    async def test_default_factory_uses_regional_endpoint_without_inline_policy(self):
        with patch.object(dlp, "DlpServiceAsyncClient", return_value=self.client) as create:
            async with adapter.GoogleSdpProtector(config()) as protector:
                await protector.protect_text("synthetic")
            create.assert_called_once_with(client_options={"api_endpoint": config().endpoint})


if __name__ == "__main__":
    unittest.main()
