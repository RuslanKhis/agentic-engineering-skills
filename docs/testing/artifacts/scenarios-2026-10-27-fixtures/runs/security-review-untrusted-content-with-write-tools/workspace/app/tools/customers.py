"""Customer contact details from the CRM table."""
from __future__ import annotations

from app import services


def get_customer_profile(tool_context) -> dict:
    """Return the signed-in customer's name, email, phone and saved addresses.

    Returns:
        {"status": "ok", "profile": {...}} or {"status": "not_found"}.
    """
    store = services.get().store
    row = store.conn.execute("SELECT * FROM customers WHERE customer_id = ?",
                             (tool_context.user_id,)).fetchone()
    if row is None:
        return {"status": "not_found"}
    return {"status": "ok", "profile": dict(row)}
