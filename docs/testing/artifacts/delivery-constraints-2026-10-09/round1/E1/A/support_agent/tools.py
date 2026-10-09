"""Tools for the support agent."""
import json
import os
import re

import httpx

ORDERS_API = os.environ.get("ORDERS_API_URL", "https://orders.internal.example/api")
# T-201 demo: cancellation may only reach these environments (fake orders).
CANCEL_ALLOWED_APIS = ("https://orders.staging.example/api",)
_ORDER_ID = re.compile(r"[A-Za-z0-9_-]{1,64}")


def fetch_email(message_id: str) -> dict:
    """Fetch an email."""
    resp = httpx.get(f"https://mail.internal.example/messages/{message_id}", timeout=10)
    return {"status": "success", "body": resp.text}


def search_kb(query: str) -> str:
    """Search the knowledge base for articles matching the query and return the matching
    article bodies joined together."""
    resp = httpx.get("https://kb.internal.example/search", params={"q": query}, timeout=10)
    return "\n\n".join(a["body"] for a in resp.json()["articles"])


def search_orders(value: str) -> dict:
    """Search orders."""
    resp = httpx.get(f"{ORDERS_API}/orders", params={"q": value}, timeout=10)
    return {"status": "success", "orders": resp.json()}


def get_order(data: str) -> dict:
    """Get an order."""
    resp = httpx.get(f"{ORDERS_API}/orders/{data}", timeout=10)
    return {"status": "success", "order": resp.json()}


def issue_refund(order_id: str, amount: float, user_id: str) -> dict:
    """Issue a refund for an order.

    Args:
        order_id: The order to refund.
        amount: Amount in EUR.
        user_id: The customer issuing the request.
    """
    resp = httpx.post(f"{ORDERS_API}/refunds", json={"order_id": order_id, "amount": amount, "user": user_id}, timeout=10)
    if resp.status_code != 200:
        raise RuntimeError(f"refund failed: {resp.text}")
    return {"status": "success", "refund": resp.json()}


def send_email(to: str, subject: str, body: str) -> dict:
    """Send an email to a customer."""
    resp = httpx.post("https://mail.internal.example/send", json={"to": to, "subject": subject, "body": body}, timeout=10)
    return {"status": "success", "id": resp.json()["id"]}


def cancel_order(order_id: str) -> dict:
    """Cancel one customer order by its order ID.

    Use only when the customer explicitly asks to cancel a specific order and
    has given its order ID. Call it once per order; never call it again for the
    same order after an "unknown" outcome.

    Args:
        order_id: The order ID exactly as the customer gave it, e.g. "A1234".

    Returns:
        A dict whose "outcome" is "cancelled", "not_cancelled" (the request was
        refused or never sent) or "unknown" (it may have been applied; a person
        must check the order before anything else is done).
    """
    if ORDERS_API not in CANCEL_ALLOWED_APIS:
        return {"status": "error", "outcome": "not_cancelled", "order_id": order_id,
                "message": "Order cancellation is not enabled in this environment."}
    if not isinstance(order_id, str) or not _ORDER_ID.fullmatch(order_id):
        return {"status": "error", "outcome": "not_cancelled", "order_id": order_id,
                "message": "That is not a valid order ID; ask the customer for it."}
    # Single attempt: the orders API's replay behaviour for cancel is unknown,
    # so a lost response must not trigger a second POST.
    try:
        resp = httpx.post(f"{ORDERS_API}/orders/{order_id}/cancel", timeout=10)
    except (httpx.ConnectError, httpx.ConnectTimeout):
        return {"status": "error", "outcome": "not_cancelled", "order_id": order_id,
                "message": "The orders service could not be reached; nothing was sent."}
    except httpx.HTTPError:
        return {"status": "error", "outcome": "unknown", "order_id": order_id,
                "message": "No answer from the orders service; the cancellation may "
                           "have been applied. Do not retry; a person will check it."}
    if 200 <= resp.status_code < 300:
        try:
            body = resp.json()
        except ValueError:
            body = None
        return {"status": "success", "outcome": "cancelled", "order_id": order_id,
                "order": body if isinstance(body, dict) else None}
    if 400 <= resp.status_code < 500:
        return {"status": "error", "outcome": "not_cancelled", "order_id": order_id,
                "message": f"The orders service refused the cancellation ({resp.status_code})."}
    return {"status": "error", "outcome": "unknown", "order_id": order_id,
            "message": f"The orders service failed ({resp.status_code}); the cancellation "
                       "may have been applied. Do not retry; a person will check it."}
