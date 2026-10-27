"""Order cancellation through the orders API."""
from __future__ import annotations

from app import services
from app.clients.orders import OrderAlreadyShipped, OrderOutcomeUnknown, OrdersError

_NOT_CANCELLABLE = {"shipped", "delivered", "cancelled"}


def cancel_order(order_id: str, tool_context) -> dict:
    """Cancel one of the signed-in customer's orders that has not shipped yet.

    Use when the customer asks to cancel an order and gives its ID, e.g. "HO-10518".
    Ask the customer to confirm first. Never retry after an "unknown" result; tell the
    customer the outcome is unconfirmed and offer to pass it to a person.

    Args:
        order_id: The order ID exactly as the customer wrote it.

    Returns:
        {"status": "cancelled", "order_id": ..., "cancellation_id": ...},
        {"status": "error", "message": ...} (nothing was cancelled) or
        {"status": "unknown", "message": ...} (the cancellation may have been applied).
    """
    svc = services.get()
    order = svc.store.get_order(order_id.strip().upper())
    if order is None or order["customer_id"] != tool_context.user_id:
        return {"status": "error", "message": f"No order {order_id} on this account."}
    if order["status"] in _NOT_CANCELLABLE:
        return {"status": "error", "message": f"Order {order['order_id']} is {order['status']} "
                                              "and can no longer be cancelled."}
    try:
        result = svc.orders.cancel_order(order["order_id"])
    except OrderAlreadyShipped:
        return {"status": "error", "message": f"Order {order['order_id']} has already shipped."}
    except OrderOutcomeUnknown as exc:
        return {"status": "unknown", "message": f"{exc}; the cancellation may have gone through."}
    except OrdersError as exc:
        return {"status": "error", "message": str(exc)}
    svc.store.set_order_status(order["order_id"], "cancelled")
    return {"status": "cancelled", "order_id": order["order_id"],
            "cancellation_id": result["cancellation_id"]}
