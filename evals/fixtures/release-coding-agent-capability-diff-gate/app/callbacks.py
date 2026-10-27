"""before_tool_callback: tools the current turn may call."""
from __future__ import annotations

READ_ONLY = {"lookup_order", "list_my_orders", "search_help", "get_product", "check_stock"}
WRITE = {"refund_order": "refunds", "send_email": "mail"}


def capability_check(tool, args, tool_context):
    name = getattr(tool, "name", "")
    if name in READ_ONLY:
        return None
    scope = WRITE.get(name)
    granted = set(tool_context.state.get("user:scopes", []))
    if scope and scope in granted:
        return None
    return {"status": "error", "message": f"{name} is not allowed for this conversation."}
