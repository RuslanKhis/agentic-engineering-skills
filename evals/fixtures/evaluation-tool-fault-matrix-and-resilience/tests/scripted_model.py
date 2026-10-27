"""A model double for Runner tests: replays queued responses and records requests."""
from __future__ import annotations

import copy

from google.adk.models import BaseLlm, LlmResponse
from google.genai import types


class ScriptedModel(BaseLlm):
    model: str = "scripted"
    script: list = []
    requests: list = []

    async def generate_content_async(self, llm_request, stream: bool = False):
        self.requests.append(copy.deepcopy(llm_request))
        if not self.script:
            raise AssertionError("scripted model: no response left for this request")
        yield self.script.pop(0)


def call(name, **args):
    return LlmResponse(content=types.Content(role="model", parts=[
        types.Part(function_call=types.FunctionCall(name=name, args=args))]))


def text(value):
    return LlmResponse(content=types.Content(role="model", parts=[types.Part(text=value)]))


def user(value):
    return types.Content(role="user", parts=[types.Part(text=value)])
