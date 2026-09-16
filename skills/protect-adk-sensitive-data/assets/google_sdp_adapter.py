"""Regional, template-based SDP adapter; copy beside sdp_boundary.py in a package.

Copyright (c) 2026 RuslanKhis
SPDX-License-Identifier: MIT
Retain this notice and the accompanying LICENSE when copying.

Requires Python 3.11+. SDK-shaped offline tests use google-cloud-dlp 3.38.0;
this adaptation has not been run against a live provider. Import/construction
does not load ADC or create clients. Explicit start() uses ADC through the SDK
unless an owned client factory is injected. No resource provisioning occurs.

One instance belongs to one event loop/worker and one trusted template set.
The host must stop/drain requests before close(). Protect before all downstream
sinks; the caller supplies authorisation, Model Armor and final-answer release.
Template preflight must verify deny classes, PII coverage, replacement-all,
throw_error and finding-quote policy. This adapter sends no inline overrides.
Regional availability and complete application residency require separate checks.
Errors never log provider data, but exporters must disable traceback-local capture.
"""

from __future__ import annotations

import asyncio
import math
import re
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from .sdp_boundary import InspectResult, TextProtectionError, protect_text


@dataclass(frozen=True)
class SdpTemplates:
    project: str
    location: str
    deny_inspect: str
    pii_inspect: str
    deidentify: str

    def __post_init__(self) -> None:
        if (
            type(self.project) is not str
            or not re.fullmatch(r"(?:[a-z][a-z0-9-]{4,28}[a-z0-9]|[0-9]{6,30})", self.project)
            or type(self.location) is not str
            or not re.fullmatch(r"[a-z][a-z0-9-]{0,62}", self.location)
            or self.location == "global"
        ):
            raise ValueError("Select a valid project and supported regional SDP location.")
        for name, collection in (
            (self.deny_inspect, "inspectTemplates"),
            (self.pii_inspect, "inspectTemplates"),
            (self.deidentify, "deidentifyTemplates"),
        ):
            prefix = f"{self.parent}/{collection}/"
            if (
                type(name) is not str
                or not name.startswith(prefix)
                or not re.fullmatch(r"[A-Za-z0-9_-]{1,256}", name[len(prefix):])
            ):
                raise ValueError("SDP template names must match the configured project/location.")
        if self.deny_inspect == self.pii_inspect:
            raise ValueError("Deny and PII policies require separate inspection templates.")

    @property
    def parent(self) -> str:
        return f"projects/{self.project}/locations/{self.location}"

    @property
    def endpoint(self) -> str:
        return f"dlp.{self.location}.rep.googleapis.com"


class GoogleSdpProtector:
    """Deny then replace, using one deadline including semaphore queue time.

    client_factory(endpoint) transfers client ownership to this adapter. Production
    normally omits it. SDK dependency/version declaration belongs to the project.
    """

    def __init__(
        self,
        templates: SdpTemplates,
        *,
        max_chars: int = 10_000,
        max_bytes: int = 32_768,
        timeout_s: float = 10.0,
        rpc_timeout_s: float = 5.0,
        max_concurrent: int = 8,
        client_factory: Callable[[str], Any] | None = None,
    ) -> None:
        if type(templates) is not SdpTemplates:
            raise ValueError("Validated SDP templates are required.")
        for value in (max_chars, max_bytes, max_concurrent):
            if type(value) is not int or value <= 0:
                raise ValueError("SDP limits must be positive integers.")
        for value in (timeout_s, rpc_timeout_s):
            if type(value) not in (int, float) or not math.isfinite(value) or value <= 0:
                raise ValueError("SDP timeouts must be finite and positive.")
        if client_factory is not None and not callable(client_factory):
            raise ValueError("Invalid SDP client factory.")
        self.templates = templates
        self.max_chars, self.max_bytes = max_chars, max_bytes
        self.timeout_s, self.rpc_timeout_s = timeout_s, rpc_timeout_s
        self._max_concurrent, self._factory = max_concurrent, client_factory
        self._client = self._sdk = self._slots = self._loop = None
        self._closing = False

    async def start(self) -> None:
        if self._closing:
            raise RuntimeError("Create a new SDP protector after shutdown.")
        loop = asyncio.get_running_loop()
        if self._loop is not None and self._loop is not loop:
            raise RuntimeError("SDP clients cannot be shared across event loops.")
        if self._client is not None:
            return
        try:
            from google.cloud import dlp_v2
        except ImportError:
            raise RuntimeError("Declare and supply a compatible google-cloud-dlp SDK.") from None
        try:
            client = (
                self._factory(self.templates.endpoint)
                if self._factory is not None
                else dlp_v2.DlpServiceAsyncClient(
                    client_options={"api_endpoint": self.templates.endpoint}
                )
            )
        except Exception:
            pass
        else:
            self._client, self._sdk, self._loop = client, dlp_v2, loop
            self._slots = asyncio.Semaphore(self._max_concurrent)
            return
        raise TextProtectionError("SDP startup unavailable; downstream use is blocked.") from None

    async def close(self) -> None:
        self._closing = True
        if self._client is None:
            return
        try:
            # Retain the client if close fails so an explicit retry can finish it.
            await self._client.transport.close()
        except Exception:
            pass
        else:
            self._client = None
            return
        raise TextProtectionError("SDP transport closure failed.") from None

    async def __aenter__(self) -> GoogleSdpProtector:
        await self.start()
        return self

    async def __aexit__(self, exc_type, exc_value, traceback) -> None:
        await self.close()

    def _valid_bytes(self, text: str) -> None:
        if type(text) is not str or not 0 < len(text) <= self.max_chars:
            raise ValueError("Invalid SDP text.")
        if len(text.encode("utf-8")) > self.max_bytes:
            raise ValueError("SDP text exceeds its byte budget.")

    async def protect_text(self, text: str, *, deadline: float | None = None) -> str:
        """Use an optional host monotonic deadline; never extend its budget."""
        try:
            loop = asyncio.get_running_loop()
            if self._client is None or self._closing or self._loop is not loop:
                raise RuntimeError
            self._valid_bytes(text)
            stop = loop.time() + self.timeout_s
            if deadline is not None:
                if type(deadline) not in (int, float) or not math.isfinite(deadline):
                    raise ValueError
                stop = min(stop, deadline)
            if not math.isfinite(stop) or stop <= loop.time():
                raise TimeoutError

            async def call(method, request):
                remaining = stop - loop.time()
                if remaining <= 0:
                    raise TimeoutError
                return await method(
                    request=request, retry=None,
                    timeout=min(self.rpc_timeout_s, remaining),
                )

            async def inspect(value):
                sdk = self._sdk
                response = await call(
                    self._client.inspect_content,
                    sdk.InspectContentRequest(
                        parent=self.templates.parent,
                        inspect_template_name=self.templates.deny_inspect,
                        item=sdk.ContentItem(value=value),
                    ),
                )
                if (
                    type(response) is not sdk.InspectContentResponse
                    or not sdk.InspectContentResponse.pb(response).HasField("result")
                ):
                    raise ValueError
                result = response.result
                return InspectResult(len(result.findings), result.findings_truncated)

            async def deidentify(value):
                sdk = self._sdk
                response = await call(
                    self._client.deidentify_content,
                    sdk.DeidentifyContentRequest(
                        parent=self.templates.parent,
                        inspect_template_name=self.templates.pii_inspect,
                        deidentify_template_name=self.templates.deidentify,
                        item=sdk.ContentItem(value=value),
                    ),
                )
                if type(response) is not sdk.DeidentifyContentResponse:
                    raise ValueError
                pb = sdk.DeidentifyContentResponse.pb(response)
                if not pb.HasField("item") or pb.item.WhichOneof("data_item") != "value":
                    raise ValueError
                if not pb.HasField("overview"):
                    raise ValueError
                overview = response.overview
                if overview.transformed_bytes < 0 or (
                    overview.transformed_bytes > 0 and not overview.transformation_summaries
                ):
                    raise ValueError
                success = sdk.TransformationSummary.TransformationResultCode.SUCCESS
                for summary in overview.transformation_summaries:
                    if not summary.results or any(
                        result.code != success or result.count < 0 for result in summary.results
                    ):
                        raise ValueError
                self._valid_bytes(response.item.value)
                return response.item.value

            async with asyncio.timeout_at(stop):
                async with self._slots:
                    return await protect_text(
                        text, inspect=inspect, deidentify=deidentify,
                        max_chars=self.max_chars, timeout_s=stop - loop.time(),
                    )
        except Exception:
            pass
        raise TextProtectionError("Text protection failed; downstream use is blocked.") from None
