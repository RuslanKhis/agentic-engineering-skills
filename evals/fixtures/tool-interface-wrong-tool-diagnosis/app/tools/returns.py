"""Returns: start one, check its status."""
from __future__ import annotations

import uuid

from app import services

_SCHEMA = ("CREATE TABLE IF NOT EXISTS returns (return_id TEXT PRIMARY KEY, order_id TEXT NOT NULL, "
           "sku TEXT NOT NULL, reason TEXT NOT NULL, state TEXT NOT NULL DEFAULT 'label_sent')")


def _conn():
    conn = services.get().store.conn
    conn.execute(_SCHEMA)
    return conn


def start_return(order_id: str, item_sku: str, reason: str, tool_context) -> dict:
    """Start a return for one item of a delivered order and email the customer a label.

    Args:
        order_id: Order ID such as "HO-10442".
        item_sku: The item's SKU from the order, e.g. "JKT-TIDE-M".
        reason: The customer's reason in a few words.

    Returns:
        {"status": "started", "return_id": ...} or {"status": "error", "message": ...}.
    """
    order = services.get().store.get_order(order_id.strip().upper())
    if order is None or order["customer_id"] != tool_context.user_id:
        return {"status": "error", "message": f"No order {order_id} on this account."}
    if order["status"] != "delivered":
        return {"status": "error", "message": "Only delivered orders can be returned."}
    return_id = f"RT-{uuid.uuid4().hex[:6].upper()}"
    with _conn() as conn:
        conn.execute("INSERT INTO returns (return_id, order_id, sku, reason) VALUES (?, ?, ?, ?)",
                     (return_id, order["order_id"], item_sku, reason))
    return {"status": "started", "return_id": return_id}


def return_status(return_id: str) -> dict:
    """Check the state of a return by its return ID ("RT-" followed by six characters).

    Returns:
        {"status": "ok", "state": "label_sent" | "received" | "refunded"} or {"status": "not_found"}.
    """
    row = _conn().execute("SELECT state FROM returns WHERE return_id = ?", (return_id.strip().upper(),)).fetchone()
    return {"status": "ok", "state": row["state"]} if row else {"status": "not_found"}
