"""before_tool_callback for the contract assistant."""
from __future__ import annotations

from typing import Any


def tool_policy(tool: Any, args: dict, tool_context: Any) -> dict | None:
    if tool.name == "send_email":
        allowed = tool_context.state.get("matter:email_allowlist", [])
        if args.get("to") not in allowed:
            return {"status": "error", "error_message": "recipient is not on this matter's allow-list"}
    if tool.name == "fetch_url" and not str(args.get("url", "")).startswith("https://"):
        return {"status": "error", "error_message": "only https pages can be fetched"}
    return None
