"""Voucher codes."""
from __future__ import annotations

from app import services

VOUCHERS = {"WELCOME10": 10, "HARBOUR15": 15}


def apply_voucher(order_id: str, code: str, tool_context) -> dict:
    """Apply a voucher code to an order that is still processing.

    Args:
        order_id: Order ID such as "HO-10518".
        code: The voucher code exactly as printed, e.g. "WELCOME10".

    Returns:
        {"status": "applied", "percent": ...} or {"status": "error", "message": ...}.
    """
    order = services.get().store.get_order(order_id.strip().upper())
    if order is None or order["customer_id"] != tool_context.user_id:
        return {"status": "error", "message": f"No order {order_id} on this account."}
    percent = VOUCHERS.get(code.strip().upper())
    if percent is None:
        return {"status": "error", "message": "That code is not valid."}
    if order["status"] != "processing":
        return {"status": "error", "message": "Vouchers can only be added before the order ships."}
    return {"status": "applied", "percent": percent}
