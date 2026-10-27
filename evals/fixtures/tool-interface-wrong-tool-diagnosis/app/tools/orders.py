"""Order lookups for the signed-in customer."""
from __future__ import annotations

from app import services


def search_orders(value: str, tool_context) -> dict:
    """Search orders."""
    needle = value.strip().lower()
    orders = services.get().store.orders_for(tool_context.user_id)
    hits = [o for o in orders if needle in o["order_id"].lower() or needle in o["status"].lower()
            or needle in o["placed_on"]]
    return {"status": "ok", "orders": hits}


def get_order(data: str, tool_context) -> dict:
    """Get an order."""
    order = services.get().store.get_order(data.strip().upper())
    if order is None or order["customer_id"] != tool_context.user_id:
        return {"status": "not_found", "message": f"No order {data} on this account."}
    return {"status": "ok", "order": order}


def list_my_orders(tool_context) -> dict:
    """List the signed-in customer's recent orders, newest first.

    Returns:
        {"status": "ok", "orders": [{order_id, status, total_cents, placed_on}, ...]}.
    """
    orders = services.get().store.orders_for(tool_context.user_id)
    return {"status": "ok", "orders": [{k: o[k] for k in ("order_id", "status", "total_cents", "placed_on")}
                                       for o in orders[:10]]}
