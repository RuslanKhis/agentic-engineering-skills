"""Loads the signed-in customer's profile into session state for the coordinator and colleagues."""
from __future__ import annotations

from app import services


def load_profile(tool_context) -> dict:
    """Load the signed-in customer's name and order count into the conversation.

    Returns:
        {"status": "ok", "name": ..., "orders": <count>} or {"status": "not_found"}.
    """
    svc = services.get()
    profile = svc.store.get_profile(tool_context.user_id)
    if profile is None:
        return {"status": "not_found"}
    summary = {"name": profile["display_name"], "orders": len(svc.store.orders_for(tool_context.user_id))}
    tool_context.state["customer_profile"] = summary
    return {"status": "ok", **summary}
