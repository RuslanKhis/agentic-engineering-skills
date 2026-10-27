"""Model Armor screening of customer input. The SDK is imported lazily so tests can pass a double."""
from __future__ import annotations

import base64
import hashlib
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


# Filters the input template enables; a file verdict is only trusted if each reported a result.
REQUIRED_FILTERS = ("rai", "pi_and_jailbreak", "malicious_uris", "sdp")
_MAX_CACHED = 256
_allowed_files: set[tuple[str, str]] = set()  # (template, sha256) of files already allowed


def _screenable_kind(kind: str) -> bool:
    from claims_agent.attachments import SCREENABLE_KINDS

    return kind in SCREENABLE_KINDS


def screen_file(kind: str, data: bytes, client: Any = None, sdk: Any = None) -> Verdict:
    """Screen one file's bytes against the input template. Only ALLOW lets it reach the model.

    Model Armor returns a verdict, not a redacted file, so any match is a block. Nothing is
    sent when the file is outside what the service can screen.
    """
    if not _screenable_kind(kind):
        return Verdict(INDETERMINATE, f"{kind or 'unknown'} files cannot be screened")
    if not config.SCREENABLE_FILE_MIN_BYTES <= len(data) <= config.SCREENABLE_FILE_MAX_BYTES:
        return Verdict(INDETERMINATE, "file size outside the screenable range")
    key = (config.INPUT_TEMPLATE, hashlib.sha256(data).hexdigest())
    if key in _allowed_files:
        return Verdict(ALLOW)
    sdk = sdk or _sdk()
    client = client or get_client()
    payload = base64.b64encode(data) if config.BYTE_DATA_ENCODING == "base64" else data
    item = sdk.DataItem(byte_item=sdk.ByteDataItem(
        byte_data_type=getattr(sdk.ByteDataItem.ByteItemType, kind), byte_data=payload))
    request = sdk.SanitizeUserPromptRequest(name=config.INPUT_TEMPLATE, user_prompt_data=item)
    try:
        response = client.sanitize_user_prompt(request=request, timeout=config.SCREEN_FILE_TIMEOUT_S)
    except Exception as exc:  # network, permission, quota, unsupported file
        return Verdict(INDETERMINATE, f"file screening failed: {type(exc).__name__}")
    result = getattr(response, "sanitization_result", None)
    if result is None:
        return Verdict(INDETERMINATE, "no sanitization result")
    state = getattr(result, "filter_match_state", None)
    if state == sdk.FilterMatchState.MATCH_FOUND:
        return Verdict(BLOCK, "filter matched")
    if state != sdk.FilterMatchState.NO_MATCH_FOUND:
        return Verdict(INDETERMINATE, f"unexpected match state {state!r}")
    if getattr(result, "invocation_result", None) != sdk.InvocationResult.SUCCESS:
        return Verdict(INDETERMINATE, "screening did not fully run")
    ran = getattr(result, "filter_results", None) or {}
    missing = [name for name in REQUIRED_FILTERS if name not in ran]
    if missing:
        return Verdict(INDETERMINATE, f"no result from filters: {', '.join(missing)}")
    if len(_allowed_files) >= _MAX_CACHED:
        _allowed_files.clear()
    _allowed_files.add(key)
    return Verdict(ALLOW)


def screen_attachments(attachments: list, client: Any = None, sdk: Any = None) -> Verdict:
    """Screen every queued upload; the first non-ALLOW verdict stops the turn."""
    for attachment in attachments:
        verdict = screen_file(attachment.kind, attachment.data, client, sdk)
        if verdict.decision != ALLOW:
            return verdict
    return Verdict(ALLOW)


def screen_inline_files(contents: list, client: Any = None, sdk: Any = None) -> Verdict:
    """Screen file parts already in a model request, including ones replayed from history."""
    from claims_agent.attachments import detect_kind

    for content in contents or []:
        for part in getattr(content, "parts", None) or []:
            blob = getattr(part, "inline_data", None)
            if blob is None:
                continue
            data = getattr(blob, "data", None) or b""
            verdict = screen_file(detect_kind(data) or "", data, client, sdk)
            if verdict.decision != ALLOW:
                return verdict
    return Verdict(ALLOW)
