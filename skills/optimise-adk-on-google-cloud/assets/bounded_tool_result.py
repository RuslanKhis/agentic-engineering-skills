"""Bound oversized tool results before they enter model context.

Teaching pattern for an ADK ``after_tool_callback``. The module imports no ADK
symbol at the top level so it stays importable in a plain test environment;
``tool_context`` is typed loosely and only ``save_artifact`` is used from it.

Verified against ADK 2.8.0 source (``agents/context.py``), read 6 October 2026:

    async def save_artifact(self, filename: str, artifact: types.Part,
                            custom_metadata: dict[str, Any] | None = None) -> int
    async def load_artifact(self, filename: str, version: int | None = None
                            ) -> types.Part | None

``save_artifact`` returns the new version (the first save is 0) and raises
``ValueError('Artifact service is not initialized.')`` when the Runner has no
artifact service. In 2.8.0 ``after_tool_callback(tool, args, tool_context,
tool_response)`` replaces the function response when it returns a dict and
keeps the original when it returns ``None`` (``flows/llm_flows/functions.py``).
Recheck both against the installed version before adopting this file.

The callback keeps small results untouched, leaves non-dict results to the
framework, preserves an explicit failure status, and for an oversized dict
returns a bounded envelope with a UTF-8 safe preview plus the artifact name and
version when a save succeeded. Limits here are an adaptable example, not ADK
defaults; match them to the target's result contract and model budget.
"""
# Copyright (c) 2026 RuslanKhis. SPDX-License-Identifier: MIT
from __future__ import annotations

import base64
import inspect
import json
import re
from typing import Any, Callable

DEFAULT_MAX_BYTES = 20_000
DEFAULT_PREVIEW_BYTES = 2_000
FAILURE_STATUSES = frozenset({
    "error", "failed", "failure", "blocked", "denied", "cancelled", "incomplete",
})
_SAFE_NAME = re.compile(r"[^A-Za-z0-9_.-]+")


def serialise(value: Any) -> bytes:
    """Deterministic UTF-8 JSON bytes for size measurement and storage."""
    return json.dumps(value, ensure_ascii=False, sort_keys=True, default=str).encode("utf-8")


def utf8_prefix(data: bytes, limit: int) -> str:
    """Return the longest decodable UTF-8 prefix of at most ``limit`` bytes."""
    if limit <= 0:
        return ""
    cut = data[:limit]
    return cut.decode("utf-8", errors="ignore")


def default_part_factory(data: bytes, mime_type: str) -> Any:
    """Build a ``types.Part`` when google-genai is importable, else a plain dict.

    ``BaseArtifactService.save_artifact`` accepts a Part or a dict normalised by
    ``ensure_part`` in ADK 2.8.0; the dict form keeps this module importable
    without the SDK. Replace with ``types.Part.from_bytes`` directly in a target
    that always has the SDK installed.
    """
    try:
        from google.genai import types  # type: ignore[import-not-found]
    except ImportError:
        return {"inline_data": {"mime_type": mime_type,
                                "data": base64.b64encode(data).decode("ascii")}}
    return types.Part.from_bytes(data=data, mime_type=mime_type)


def artifact_name(tool_name: str, call_id: str | None, prefix: str) -> str:
    safe_tool = _SAFE_NAME.sub("_", tool_name or "tool")[:64] or "tool"
    safe_call = _SAFE_NAME.sub("_", call_id or "")[:64]
    suffix = f"-{safe_call}" if safe_call else ""
    return f"{prefix}-{safe_tool}{suffix}.json"


def build_bounded_after_tool_callback(
    *,
    max_bytes: int = DEFAULT_MAX_BYTES,
    preview_bytes: int = DEFAULT_PREVIEW_BYTES,
    artifact_prefix: str = "tool-result",
    part_factory: Callable[[bytes, str], Any] = default_part_factory,
):
    """Return an async ``after_tool_callback`` that bounds oversized dict results."""
    if max_bytes <= 0 or preview_bytes <= 0:
        raise ValueError("max_bytes and preview_bytes must be positive")

    async def bounded_after_tool_callback(tool: Any, args: dict, tool_context: Any,
                                          tool_response: Any) -> dict | None:
        del args  # Arguments do not influence bounding; kept for the ADK signature.
        if not isinstance(tool_response, dict):
            return None
        data = serialise(tool_response)
        if len(data) <= max_bytes:
            return None
        tool_name = getattr(tool, "name", None) or "tool"
        call_id = getattr(tool_context, "function_call_id", None)
        name = artifact_name(str(tool_name), call_id if isinstance(call_id, str) else None,
                             artifact_prefix)
        version = None
        artifact = None
        artifact_state = "unavailable"
        save = getattr(tool_context, "save_artifact", None)
        if callable(save):
            try:
                result = save(name, part_factory(data, "application/json"))
                if inspect.isawaitable(result):
                    result = await result
                if type(result) is int:
                    version, artifact, artifact_state = result, name, "saved"
                else:
                    artifact_state = "save_returned_no_version"
            except Exception:  # noqa: BLE001 - the fixed label avoids leaking payload text
                artifact_state = "save_failed"
        original_status = tool_response.get("status")
        status = "success"
        if isinstance(original_status, str) and original_status.lower() in FAILURE_STATUSES:
            status = original_status
        return {
            "status": status,
            "preview": utf8_prefix(data, preview_bytes),
            "artifact": artifact,
            "version": version,
            "truncated": True,
            "original_bytes": len(data),
            "artifact_state": artifact_state,
        }

    return bounded_after_tool_callback
