"""Invoices for the signed-in customer's orders."""
from __future__ import annotations

from app import services


def get_invoice(order_id: str, tool_context) -> dict:
    """Show the invoice lines for one of the customer's orders.

    Args:
        order_id: Order ID such as "HO-10442".

    Returns:
        {"status": "ok", "lines": [{"label", "amount_cents"}], "total_cents": ...}
        or {"status": "not_found", "message": ...}.
    """
    order = services.get().store.get_order(order_id.strip().upper())
    if order is None or order["customer_id"] != tool_context.user_id:
        return {"status": "not_found", "message": f"No order {order_id} on this account."}
    total = order["total_cents"]
    shipping = 495 if total < 10_000 else 0
    return {"status": "ok", "total_cents": total,
            "lines": [{"label": "Items", "amount_cents": total - shipping},
                      {"label": "Delivery", "amount_cents": shipping}]}
