"""Order lookups for the signed-in customer."""
from __future__ import annotations

from app import services


def search_orders(query: str, tool_context) -> dict:
    """Find the signed-in customer's orders by a fragment of order ID, status or date.

    Use this only when the customer has NOT given a full order ID and describes
    orders by status or date. If you already have an order ID such as "HO-10442",
    call get_order instead. To see all recent orders, call list_my_orders.
    This does not search by product name, customer name or address.

    Args:
        query: Case-insensitive text matched against the order ID, the status
            (for example "processing" or "shipped") or the placed-on date in
            YYYY-MM-DD form (for example "2025-03"). Never a person's name.

    Returns:
        {"status": "ok", "orders": [full order records]}; the list is empty when
        nothing matches.
    """
    needle = query.strip().lower()
    orders = services.get().store.orders_for(tool_context.user_id)
    hits = [o for o in orders if needle in o["order_id"].lower() or needle in o["status"].lower()
            or needle in o["placed_on"]]
    return {"status": "ok", "orders": hits}


def get_order(order_id: str, tool_context) -> dict:
    """Get the full record of one order of the signed-in customer by its order ID.

    Use this whenever the customer gives an order ID like "HO-10442". If they
    gave no ID, call list_my_orders or search_orders first to find it; do not
    guess an ID.

    Args:
        order_id: The order ID, "HO-" followed by digits (for example
            "HO-10442"). Case-insensitive. Not a customer name or product name.

    Returns:
        {"status": "ok", "order": {order record}} or, when the ID does not exist
        on this account, {"status": "not_found", "message": ..., "hint": ...}.
    """
    order = services.get().store.get_order(order_id.strip().upper())
    if order is None or order["customer_id"] != tool_context.user_id:
        return {"status": "not_found", "message": f"No order {order_id} on this account.",
                "hint": "Call list_my_orders to see this customer's order IDs."}
    return {"status": "ok", "order": order}


def list_my_orders(tool_context) -> dict:
    """List the signed-in customer's recent orders, newest first.

    Returns:
        {"status": "ok", "orders": [{order_id, status, total_cents, placed_on}, ...]}.
    """
    orders = services.get().store.orders_for(tool_context.user_id)
    return {"status": "ok", "orders": [{k: o[k] for k in ("order_id", "status", "total_cents", "placed_on")}
                                       for o in orders[:10]]}
