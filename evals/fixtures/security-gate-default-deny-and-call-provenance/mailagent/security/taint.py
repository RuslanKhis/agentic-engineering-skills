"""after_tool_callback: record values from untrusted tool results so the gate can refuse them."""
from __future__ import annotations

import re
from typing import Any

UNTRUSTED_TOOLS = {"search_mail"}
EMAIL = re.compile(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+")
URL = re.compile(r"https?://\S+")
ID = re.compile(r"\b(?:file|thr)-[0-9a-f]{6,}\b")


def label_untrusted(tool: Any, args: dict, tool_context: Any, tool_response: Any) -> None:
    if tool.name not in UNTRUSTED_TOOLS:
        return None
    text = str(tool_response)
    found = set(EMAIL.findall(text)) | set(URL.findall(text)) | set(ID.findall(text))
    known = set(tool_context.state.get("taint:untrusted_fields", []))
    tool_context.state["taint:untrusted_fields"] = sorted(known | found)
    return None
