"""Order lookups for the signed-in customer."""
from __future__ import annotations

from app import services


def search_orders(query: str, tool_context) -> dict:
    """Find the signed-in customer's orders by status or date when the customer
    does NOT have an order ID. If you already have an order ID such as "HO-10518",
    call get_order instead. This does not search by product or customer name.

    Args:
        query: Text to match against order ID, status or placed-on date.
            Examples: "processing", "shipped", "2026-03" (a date prefix).

    Returns:
        {"status": "ok", "orders": [{order_id, customer_id, status, total_cents, placed_on}, ...]};
        the list is empty when nothing matches (try list_my_orders).
    """
    needle = query.strip().lower()
    orders = services.get().store.orders_for(tool_context.user_id)
    hits = [o for o in orders if needle in o["order_id"].lower() or needle in o["status"].lower()
            or needle in o["placed_on"]]
    return {"status": "ok", "orders": hits}


def get_order(order_id: str, tool_context) -> dict:
    """Get the full record of one of the customer's orders from its order ID.
    Use this whenever an order ID is known; if it is not, call list_my_orders or
    search_orders first. Never pass a customer name or product name.

    Args:
        order_id: Order ID such as "HO-10518" (case-insensitive).

    Returns:
        {"status": "ok", "order": {...}} or
        {"status": "not_found", "message": ..., "hint": ...}.
    """
    order = services.get().store.get_order(order_id.strip().upper())
    if order is None or order["customer_id"] != tool_context.user_id:
        return {"status": "not_found", "message": f"No order {order_id} on this account.",
                "hint": "Order IDs look like HO-10518. Call list_my_orders to see this customer's IDs."}
    return {"status": "ok", "order": order}


def list_my_orders(tool_context) -> dict:
    """List the signed-in customer's recent orders, newest first.

    Returns:
        {"status": "ok", "orders": [{order_id, status, total_cents, placed_on}, ...]}.
    """
    orders = services.get().store.orders_for(tool_context.user_id)
    return {"status": "ok", "orders": [{k: o[k] for k in ("order_id", "status", "total_cents", "placed_on")}
                                       for o in orders[:10]]}
