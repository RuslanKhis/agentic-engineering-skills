"""Trusted-side rules for what the portal agent may call and with which customer."""
from __future__ import annotations

ALLOWED_TOOLS = frozenset({"customer-revenue"})
TENANT_PARAM = "tenant_id"


def check_tool_call(tool_name: str, args: dict) -> str | None:
    """Return a refusal message, or None when the call may go ahead.

    The customer ID is bound by the portal when the agent is built; a model-supplied one is
    refused rather than overwritten so an injection attempt is visible.
    """
    if tool_name not in ALLOWED_TOOLS:
        return f"tool {tool_name!r} is not available in the portal"
    if TENANT_PARAM in args:
        return "the customer account is set by the portal and cannot be chosen"
    return None
