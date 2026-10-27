"""after_tool_callback: record values from untrusted tool results so the gate can refuse them."""
from __future__ import annotations

import re
from typing import Any

UNTRUSTED_TOOLS = {"search_mail"}
EMAIL = re.compile(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+")
URL = re.compile(r"https?://\S+")
ID = re.compile(r"\b(?:file|thr)-[0-9a-f]{6,}\b")


def record_user_values(callback_context: Any) -> None:
    """before_agent_callback: remember ids, addresses and URLs the user typed (the provenance the gate checks).

    Union only, never replace: on resume after a confirmation this runs again with the confirmation
    as user_content, and must not drop what the original request recorded.
    """
    content = getattr(callback_context, "user_content", None)
    text = " ".join(p.text for p in (getattr(content, "parts", None) or []) if getattr(p, "text", None))
    found = set(EMAIL.findall(text)) | set(URL.findall(text)) | set(ID.findall(text))
    if found:
        known = set(callback_context.state.get("provenance:user_values", []))
        callback_context.state["provenance:user_values"] = sorted(known | found)
    return None


def label_untrusted(tool: Any, args: dict, tool_context: Any, tool_response: Any) -> None:
    if tool.name not in UNTRUSTED_TOOLS:
        return None
    text = str(tool_response)
    found = set(EMAIL.findall(text)) | set(URL.findall(text)) | set(ID.findall(text))
    known = set(tool_context.state.get("taint:untrusted_fields", []))
    tool_context.state["taint:untrusted_fields"] = sorted(known | found)
    return None
