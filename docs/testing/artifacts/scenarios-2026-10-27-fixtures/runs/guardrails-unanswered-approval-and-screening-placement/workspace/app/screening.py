"""Model Armor screen on the model's responses.

The screen runs inline in after_model_callback, before ADK dispatches any tool call in the response.
Running it beside the model call let a flagged response's tool call fire before the verdict arrived.
"""
from __future__ import annotations

import logging
import os

from google.adk.models.llm_response import LlmResponse
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

    async def after_model_callback(self, *, callback_context, llm_response):
        parts = llm_response.content.parts if llm_response.content else []
        text = "".join(p.text or "" for p in parts)
        has_tool_call = any(p.function_call for p in parts)
        if not text:
            return None
        try:
            flagged = await self.client.sanitize_model_response(text)
        except Exception:
            log.exception("model armor screen failed")
            # A response that would act must not go unscreened; plain text keeps the earlier fail-open.
            flagged = has_tool_call
        if flagged:
            callback_context.state["temp:blocked"] = True
            # Replacing the response drops its function calls, so nothing downstream executes.
            return LlmResponse(content=types.Content(role="model", parts=[types.Part(text=BLOCKED_REPLY)]))
        return None
