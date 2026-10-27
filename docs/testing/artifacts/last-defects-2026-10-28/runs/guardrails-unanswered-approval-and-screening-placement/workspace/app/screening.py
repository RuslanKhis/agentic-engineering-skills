"""Model Armor screen on the model's responses.

It runs blocking, inside after_model_callback: ADK dispatches a response's tool calls only after
this callback returns, so a flagged (or unscreenable) response is replaced before any tool fires.
"""
from __future__ import annotations

import json
import logging
import os

from google.adk.models.llm_response import LlmResponse
from google.adk.plugins.base_plugin import BasePlugin
from google.genai import types

log = logging.getLogger(__name__)

BLOCKED_REPLY = "Sorry, I can't help with that here. A colleague will get back to you."


def screenable_text(content) -> str:
    """Model text plus the arguments of any tool calls, which are also model output."""
    parts = content.parts if content else []
    chunks = [p.text for p in parts if p.text]
    chunks += [json.dumps({"tool": p.function_call.name, "args": dict(p.function_call.args or {})}, default=str)
               for p in parts if p.function_call]
    return "\n".join(chunks)


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
        text = screenable_text(llm_response.content)
        if not text:
            return None
        try:
            flagged = await self.client.sanitize_model_response(text)
        except Exception:
            # Unknown verdict: withhold rather than let the response (and its tool calls) through.
            log.exception("model armor screen failed; withholding response")
            flagged = True
        if not flagged:
            return None
        callback_context.state["temp:blocked"] = True
        return LlmResponse(content=types.Content(role="model", parts=[types.Part(text=BLOCKED_REPLY)]))
