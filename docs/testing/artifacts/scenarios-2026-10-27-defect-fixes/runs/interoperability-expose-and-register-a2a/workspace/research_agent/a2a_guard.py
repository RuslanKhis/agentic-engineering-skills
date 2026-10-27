"""Tool-call guard for the A2A-served agent. No google.adk imports."""
from __future__ import annotations

GATED_TOOLS = frozenset({"submit_procurement_request"})


def block_gated_tools(tool, args, tool_context):
    """before_tool_callback: refuse tools that need a human approval on the A2A surface.

    Returning a dict skips the tool call and uses the dict as its result.
    """
    if getattr(tool, "name", None) in GATED_TOOLS:
        return {"status": "error", "message": "This action is not available over A2A."}
    return None
