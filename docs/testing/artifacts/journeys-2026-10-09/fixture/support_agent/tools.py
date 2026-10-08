"""Tools for the support agent."""
import json
import httpx

ORDERS_API = "https://orders.internal.example/api"


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
