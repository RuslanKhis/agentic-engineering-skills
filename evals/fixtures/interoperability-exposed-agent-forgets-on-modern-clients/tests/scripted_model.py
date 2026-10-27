"""A scripted model for Runner tests: returns queued LlmResponses in order. Needs google-adk."""
from __future__ import annotations

from google.adk.models.base_llm import BaseLlm


class ScriptedModel(BaseLlm):
    model: str = "scripted"
    responses: list = []

    async def generate_content_async(self, llm_request, stream: bool = False):
        yield self.responses.pop(0)
