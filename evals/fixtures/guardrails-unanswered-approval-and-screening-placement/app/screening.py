"""Model Armor screen on the model's responses, run beside the model call so replies are not delayed."""
from __future__ import annotations

import asyncio
import logging
import os

from google.adk.plugins.base_plugin import BasePlugin
from google.genai import types

log = logging.getLogger(__name__)

BLOCKED_REPLY = "Sorry, I can't help with that here. A colleague will get back to you."


class ModelArmorClientWrapper:
    """Thin wrapper so tests can replace the SDK client."""

    def __init__(self, template: str | None = None) -> None:
        self.template = template or os.environ.get("MODEL_ARMOR_TEMPLATE", "")

    async def sanitize_model_response(self, text: str) -> bool:
        from google.cloud import modelarmor_v1

        client = modelarmor_v1.ModelArmorAsyncClient()
        result = await client.sanitize_model_response(
            request=modelarmor_v1.SanitizeModelResponseRequest(
                name=self.template, model_response_data=modelarmor_v1.DataItem(text=text)))
        return result.sanitization_result.filter_match_state == modelarmor_v1.FilterMatchState.MATCH_FOUND


class OutputScreenPlugin(BasePlugin):
    def __init__(self, client: ModelArmorClientWrapper | None = None) -> None:
        super().__init__(name="output_screen")
        self.client = client or ModelArmorClientWrapper()
        self.flagged: dict[str, bool] = {}

    async def after_model_callback(self, *, callback_context, llm_response):
        text = "".join(p.text or "" for p in (llm_response.content.parts if llm_response.content else []))
        if text:
            # Screen in the background; the response (and any tool calls in it) continues meanwhile.
            asyncio.create_task(self._screen(callback_context.invocation_id, text))
        return None

    async def _screen(self, invocation_id: str, text: str) -> None:
        try:
            self.flagged[invocation_id] = await self.client.sanitize_model_response(text)
        except Exception:
            log.exception("model armor screen failed")

    async def after_run_callback(self, *, invocation_context):
        if self.flagged.pop(invocation_context.invocation_id, False):
            invocation_context.session.state["temp:blocked"] = True
            return types.Content(role="model", parts=[types.Part(text=BLOCKED_REPLY)])
        return None
