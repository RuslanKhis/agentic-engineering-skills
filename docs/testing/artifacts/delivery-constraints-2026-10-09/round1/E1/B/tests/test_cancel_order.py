"""Offline tests for the T-201 cancel_order tool (no network, no ADK)."""
import socket

import httpx
import pytest

from support_agent import tools


@pytest.fixture(autouse=True)
def no_network(monkeypatch):
    def refuse(*args, **kwargs):
        raise AssertionError("unexpected network connection")

    monkeypatch.setattr(socket.socket, "connect", refuse)


@pytest.fixture
def orders_api(monkeypatch):
    """Fake staging orders API; records every request it receives."""
    state = {"requests": [], "cancelled": [], "respond": lambda req: httpx.Response(200, json={"status": "cancelled"})}

    def handler(request):
        state["requests"].append(request)
        return state["respond"](request)

    monkeypatch.setattr(
        tools,
        "_orders_client",
        lambda: httpx.Client(base_url=tools.CANCEL_ORDERS_API, transport=httpx.MockTransport(handler)),
    )
    return state


def test_cancel_defaults_to_staging_not_production():
    assert tools.CANCEL_ORDERS_API.startswith("https://orders.staging.")
    assert tools.CANCEL_ORDERS_API != tools.ORDERS_API


def test_successful_cancel_posts_once_to_order_path(orders_api):
    result = tools.cancel_order("ORD-1042")
    assert result == {"status": "cancelled", "order_id": "ORD-1042"}
    assert len(orders_api["requests"]) == 1
    req = orders_api["requests"][0]
    assert req.method == "POST"
    assert req.url.path == "/api/orders/ORD-1042/cancel"


@pytest.mark.parametrize("bad", ["", "../refunds", "ORD 1", "a" * 65, "Jane Smith", None, 1042])
def test_invalid_order_id_never_reaches_api(orders_api, bad):
    result = tools.cancel_order(bad)
    assert result["status"] == "error" and result["error"] == "invalid_order_id"
    assert orders_api["requests"] == []


@pytest.mark.parametrize("code,error", [(404, "order_not_found"), (409, "order_not_cancellable"), (403, "http_403")])
def test_refusal_is_error_with_one_attempt(orders_api, code, error):
    orders_api["respond"] = lambda req: httpx.Response(code)
    result = tools.cancel_order("ORD-1042")
    assert result["status"] == "error" and result["error"] == error
    assert len(orders_api["requests"]) == 1


def test_lost_response_is_unknown_and_not_retried(orders_api):
    def commit_then_lose(request):
        orders_api["cancelled"].append(request.url.path)
        raise httpx.ReadTimeout("response lost", request=request)

    orders_api["respond"] = commit_then_lose
    result = tools.cancel_order("ORD-1042")
    assert result["status"] == "unknown"
    assert "Do not retry" in result["message"]
    assert len(orders_api["requests"]) == 1
    assert orders_api["cancelled"] == ["/api/orders/ORD-1042/cancel"]


@pytest.mark.parametrize("code", [500, 502, 503])
def test_server_error_is_unknown_and_not_retried(orders_api, code):
    orders_api["respond"] = lambda req: httpx.Response(code)
    result = tools.cancel_order("ORD-1042")
    assert result["status"] == "unknown"
    assert len(orders_api["requests"]) == 1


def test_connect_error_is_not_cancelled(orders_api):
    def refuse(request):
        raise httpx.ConnectError("refused", request=request)

    orders_api["respond"] = refuse
    result = tools.cancel_order("ORD-1042")
    assert result["status"] == "error" and result["error"] == "orders_api_unreachable"
    assert len(orders_api["requests"]) == 1


def test_real_client_has_no_transport_retries():
    client = tools._orders_client()
    try:
        assert client._transport._pool._retries == 0
    finally:
        client.close()
