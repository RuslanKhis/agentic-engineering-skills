"""Tools for the support agent."""
import json
import os
import re

import httpx

ORDERS_API = "https://orders.internal.example/api"

# T-201 demo: cancellations go to the staging orders API (fake orders only)
# unless explicitly overridden. Kept separate from ORDERS_API so the demo
# cannot cancel production orders by default.
CANCEL_ORDERS_API = os.environ.get("CANCEL_ORDERS_API", "https://orders.staging.example/api")

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


def _orders_client() -> httpx.Client:
    # No transport retries: the cancel endpoint's replay contract is unknown.
    return httpx.Client(base_url=CANCEL_ORDERS_API, timeout=10, transport=httpx.HTTPTransport(retries=0))


def cancel_order(order_id: str) -> dict:
    """Cancel one customer order by its order ID.

    Call only after the customer has asked to cancel a specific order and you
    know its exact order ID. Never call it again for the same order after a
    result of "unknown"; tell the customer staff will check instead.

    Args:
        order_id: The exact order ID, for example "ORD-1042". Not a customer name.

    Returns:
        status "cancelled" when the orders API confirmed the cancellation,
        "error" when it was refused and nothing was cancelled, or "unknown" when
        the outcome could not be confirmed (the order may or may not be cancelled).
    """
    if not isinstance(order_id, str) or not _ORDER_ID.fullmatch(order_id):
        return {"status": "error", "error": "invalid_order_id", "message": "Order ID is not valid; no cancellation was attempted."}
    # Single attempt: replaying a POST with unknown semantics could cancel twice
    # or mask a lost response, so ambiguity is reported, never retried.
    try:
        with _orders_client() as client:
            resp = client.post(f"/orders/{order_id}/cancel")
    except httpx.TimeoutException:
        return _unknown(order_id, "timeout")
    except httpx.ConnectError:
        # Connection never established, so the request was not sent.
        return {"status": "error", "order_id": order_id, "error": "orders_api_unreachable", "message": "Orders service unreachable; the order was not cancelled."}
    except httpx.TransportError:
        return _unknown(order_id, "transport_error")
    if 200 <= resp.status_code < 300:
        return {"status": "cancelled", "order_id": order_id}
    if resp.status_code in (404, 409, 422):
        reason = {404: "order_not_found", 409: "order_not_cancellable", 422: "order_not_cancellable"}[resp.status_code]
        return {"status": "error", "order_id": order_id, "error": reason, "message": "The order was not cancelled."}
    if 400 <= resp.status_code < 500:
        return {"status": "error", "order_id": order_id, "error": f"http_{resp.status_code}", "message": "The order was not cancelled."}
    return _unknown(order_id, f"http_{resp.status_code}")


def _unknown(order_id: str, reason: str) -> dict:
    return {
        "status": "unknown",
        "order_id": order_id,
        "error": reason,
        "message": "Could not confirm whether the order was cancelled. Do not retry; staff will check the order status.",
    }
