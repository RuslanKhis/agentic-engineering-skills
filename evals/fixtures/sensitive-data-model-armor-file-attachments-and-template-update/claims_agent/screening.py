"""Model Armor screening of customer input. The SDK is imported lazily so tests can pass a double."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from claims_agent import config

ALLOW, BLOCK, INDETERMINATE = "allow", "block", "indeterminate"


@dataclass
class Verdict:
    decision: str
    reason: str = ""


def _sdk():
    from google.cloud import modelarmor_v1

    return modelarmor_v1


_client = None


def get_client():
    global _client
    if _client is None:
        _client = _sdk().ModelArmorClient()
    return _client


def screen_text(text: str, client: Any = None, sdk: Any = None) -> Verdict:
    """Screen one piece of customer text against the input template."""
    sdk = sdk or _sdk()
    client = client or get_client()
    request = sdk.SanitizeUserPromptRequest(name=config.INPUT_TEMPLATE,
                                            user_prompt_data=sdk.DataItem(text=text))
    try:
        response = client.sanitize_user_prompt(request=request)
    except Exception as exc:  # network, permission, quota
        return Verdict(INDETERMINATE, f"screening failed: {type(exc).__name__}")
    result = getattr(response, "sanitization_result", None)
    if result is None:
        return Verdict(INDETERMINATE, "no sanitization result")
    state = getattr(result, "filter_match_state", None)
    if state == sdk.FilterMatchState.NO_MATCH_FOUND:
        return Verdict(ALLOW)
    if state == sdk.FilterMatchState.MATCH_FOUND:
        return Verdict(BLOCK, "filter matched")
    return Verdict(INDETERMINATE, f"unexpected match state {state!r}")
