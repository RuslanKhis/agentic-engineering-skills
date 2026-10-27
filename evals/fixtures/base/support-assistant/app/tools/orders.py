"""Order lookups for the signed-in customer."""
from __future__ import annotations

from app import services


def lookup_order(order_id: str, tool_context) -> dict:
    """Look up one of the signed-in customer's orders by its order ID.

    Use when the customer gives an order ID such as "HO-10442". Do not use it to
    search by name or date; use list_my_orders for that.

    Args:
        order_id: The order ID exactly as the customer wrote it, e.g. "HO-10442".

    Returns:
        {"status": "ok", "order": {...}} or {"status": "not_found", "message": ...}.
    """
    order = services.get().store.get_order(order_id.strip().upper())
    if order is None or order["customer_id"] != tool_context.user_id:
        return {"status": "not_found", "message": f"No order {order_id} on this account."}
    return {"status": "ok", "order": order}


def list_my_orders(tool_context) -> dict:
    """List the signed-in customer's recent orders, newest first.

    Returns:
        {"status": "ok", "orders": [{order_id, status, total_cents, placed_on}, ...]}.
    """
    orders = services.get().store.orders_for(tool_context.user_id)
    return {"status": "ok", "orders": [{k: o[k] for k in ("order_id", "status", "total_cents", "placed_on")}
                                       for o in orders[:10]]}
