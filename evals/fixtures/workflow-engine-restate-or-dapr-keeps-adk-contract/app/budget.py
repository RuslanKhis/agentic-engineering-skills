"""Token budget for one invocation, enforced in model callbacks.

before_model refuses the call once the invocation has used TOKEN_BUDGET tokens; after_model
adds each response's usage. The count lives in invocation-scoped state (temp:), so a new
invocation starts from zero. ADK types are imported inside the callbacks so this module (and
its tests) load without the SDK.
"""
from __future__ import annotations

TOKEN_BUDGET = 40_000
USED = "temp:tokens_used"
CALLS = "temp:model_calls"


def before_model(callback_context, llm_request):
    state = callback_context.state
    state[CALLS] = state.get(CALLS, 0) + 1
    if state.get(USED, 0) >= TOKEN_BUDGET:
        from google.adk.models import LlmResponse
        from google.genai import types

        return LlmResponse(content=types.Content(role="model", parts=[types.Part(
            text="I've reached the limit for this conversation. A colleague will pick it up.")]))
    return None


def after_model(callback_context, llm_response):
    usage = getattr(llm_response, "usage_metadata", None)
    if usage is not None:
        state = callback_context.state
        state[USED] = state.get(USED, 0) + (getattr(usage, "total_token_count", 0) or 0)
    return None
