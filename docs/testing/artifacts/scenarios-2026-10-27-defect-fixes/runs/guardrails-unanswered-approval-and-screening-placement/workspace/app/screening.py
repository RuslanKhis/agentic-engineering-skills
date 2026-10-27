"""Model Armor screen on the model's responses.

The screen blocks: it runs inside after_model_callback and the verdict is known before
ADK dispatches any tool call in that response. Running it beside the model call let a
tool fire before the verdict, and a verdict that arrives after the effect cannot undo it.
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
        if getattr(llm_response, "partial", False) or not llm_response.content:
            return None
        text = "".join(p.text or "" for p in llm_response.content.parts or [])
        if not text:
            return None
        try:
            flagged = await self.client.sanitize_model_response(text)
        except Exception:
            # Fail closed: an unscreened response must not carry a tool call to the dispatcher.
            log.exception("model armor screen failed")
            flagged = True
        if not flagged:
            return None
        callback_context.state["temp:blocked"] = True
        # The replacement has no function_call parts, so no tool runs for this response.
        return LlmResponse(content=types.Content(role="model", parts=[types.Part(text=BLOCKED_REPLY)]))
