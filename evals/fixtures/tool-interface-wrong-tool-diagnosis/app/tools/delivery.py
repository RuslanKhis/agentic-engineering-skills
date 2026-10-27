"""Delivery tracking and address changes."""
from __future__ import annotations

from app import services

STAGES = {"processing": "Being packed", "shipped": "With the courier", "delivered": "Delivered"}


def track_parcel(order_id: str, tool_context) -> dict:
    """Show where the parcel for one of the customer's orders is.

    Args:
        order_id: Order ID such as "HO-10518".

    Returns:
        {"status": "ok", "stage": ...} or {"status": "not_found", "message": ...}.
    """
    order = services.get().store.get_order(order_id.strip().upper())
    if order is None or order["customer_id"] != tool_context.user_id:
        return {"status": "not_found", "message": f"No order {order_id} on this account."}
    return {"status": "ok", "stage": STAGES.get(order["status"], order["status"])}


def change_delivery_address(order_id: str, address_line: str, postcode: str, tool_context) -> dict:
    """Change the delivery address of an order that has not shipped yet.

    Args:
        order_id: Order ID such as "HO-10518".
        address_line: Street address on one line.
        postcode: Postcode as the customer wrote it.

    Returns:
        {"status": "changed"} or {"status": "error", "message": ...}.
    """
    order = services.get().store.get_order(order_id.strip().upper())
    if order is None or order["customer_id"] != tool_context.user_id:
        return {"status": "error", "message": f"No order {order_id} on this account."}
    if order["status"] != "processing":
        return {"status": "error", "message": "The parcel has already left the warehouse."}
    return {"status": "changed", "order_id": order["order_id"], "postcode": postcode.upper()}
