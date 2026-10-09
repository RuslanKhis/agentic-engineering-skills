import httpx
import pytest

from support_agent import tools

STAGING = "https://orders.staging.example/api"


class Provider(list):
    """Stand-in for the staging orders API: records URLs, returns or raises `reply`."""

    reply = httpx.Response(200, json={"id": "A1234", "state": "cancelled"})

    def post(self, url, **kwargs):
        self.append(url)
        if isinstance(self.reply, Exception):
            raise self.reply
        return self.reply


@pytest.fixture
def calls(monkeypatch):
    provider = Provider()
    monkeypatch.setattr(tools, "ORDERS_API", STAGING)
    monkeypatch.setattr(tools.httpx, "post", provider.post)
    return provider


def test_success_posts_once_to_staging(calls):
    result = tools.cancel_order("A1234")
    assert calls == [f"{STAGING}/orders/A1234/cancel"]
    assert result["outcome"] == "cancelled"
    assert result["order"] == {"id": "A1234", "state": "cancelled"}


def test_non_staging_api_never_dispatches(calls, monkeypatch):
    monkeypatch.setattr(tools, "ORDERS_API", "https://orders.internal.example/api")
    result = tools.cancel_order("A1234")
    assert calls == []
    assert result["outcome"] == "not_cancelled"


@pytest.mark.parametrize("bad", ["", "../refunds", "A1234/cancel", "x" * 65, 1234])
def test_invalid_order_id_never_dispatches(calls, bad):
    assert tools.cancel_order(bad)["outcome"] == "not_cancelled"
    assert calls == []


def test_provider_refusal_is_not_cancelled(calls):
    calls.reply = httpx.Response(409, json={"error": "already shipped"})
    result = tools.cancel_order("A1234")
    assert len(calls) == 1
    assert result["outcome"] == "not_cancelled"


@pytest.mark.parametrize("reply", [
    httpx.ReadTimeout("lost response"),
    httpx.RemoteProtocolError("connection dropped"),
    httpx.Response(503),
])
def test_ambiguous_outcome_is_unknown_and_not_retried(calls, reply):
    calls.reply = reply
    result = tools.cancel_order("A1234")
    assert len(calls) == 1
    assert result["outcome"] == "unknown"
    assert "Do not retry" in result["message"]


def test_connection_failure_is_not_cancelled(calls):
    calls.reply = httpx.ConnectError("refused")
    result = tools.cancel_order("A1234")
    assert len(calls) == 1
    assert result["outcome"] == "not_cancelled"
