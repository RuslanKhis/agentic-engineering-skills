import asyncio
import socket

import pytest

from provider import MockProvider
from refund_tool import refund


@pytest.fixture(autouse=True)
def block_network(monkeypatch):
    def forbidden(*args, **kwargs):
        pytest.fail("Network access is outside the fixture scope")

    monkeypatch.setattr(socket, "create_connection", forbidden)
    monkeypatch.setattr(socket.socket, "connect", forbidden)
    monkeypatch.setattr(socket.socket, "connect_ex", forbidden)


def check_status(result, expected):
    assert isinstance(result, dict)
    assert result["status"] == expected
    assert isinstance(result["message"], str) and result["message"]


def test_lost_reply_recovers_receipt_with_one_effect():
    provider = MockProvider(["commit_then_lose", "success"])

    result = refund(provider, "refund-order-1", 1250, True)

    check_status(result, "succeeded")
    assert result["receipt"] == {"refund_id": "refund-1", "amount_cents": 1250}
    assert provider.calls == [("refund-order-1", 1250)] * 2
    assert provider.effects == 1


def test_successful_operation_replays_across_tool_invocations():
    provider = MockProvider()

    first = refund(provider, "refund-order-1", 1250, True)
    replay = refund(provider, "refund-order-1", 1250, True)
    distinct = refund(provider, "refund-order-2", 1250, True)

    for result in (first, replay, distinct):
        check_status(result, "succeeded")
    assert first["receipt"] == replay["receipt"]
    assert distinct["receipt"]["refund_id"] != first["receipt"]["refund_id"]
    assert provider.calls == [
        ("refund-order-1", 1250),
        ("refund-order-1", 1250),
        ("refund-order-2", 1250),
    ]
    assert provider.effects == 2


def test_exhausted_lost_reply_recovers_on_next_invocation():
    provider = MockProvider(["commit_then_lose"])

    lost = refund(provider, "refund-order-1", 1250, True, max_attempts=1)
    recovered = refund(provider, "refund-order-1", 1250, True, max_attempts=1)

    check_status(lost, "unknown")
    assert lost["operation_id"] == "refund-order-1"
    check_status(recovered, "succeeded")
    assert recovered["receipt"] == provider.receipts["refund-order-1"]
    assert provider.calls == [("refund-order-1", 1250)] * 2
    assert provider.effects == 1


@pytest.mark.parametrize("initial_action", ["success", "commit_then_lose", "unavailable"])
def test_changed_amount_keeps_key_and_is_rejected(initial_action):
    provider = MockProvider([initial_action])
    refund(provider, "refund-order-1", 1250, True, max_attempts=1)
    effects_before = provider.effects

    result = refund(provider, "refund-order-1", 1300, True)

    check_status(result, "rejected")
    assert result["error_type"] == "PayloadMismatch"
    assert provider.calls == [("refund-order-1", 1250), ("refund-order-1", 1300)]
    assert provider.payloads == {"refund-order-1": 1250}
    assert provider.effects == effects_before


def test_transient_failure_recovers_with_same_payload():
    provider = MockProvider(["unavailable", "success"])

    result = refund(provider, "refund-order-1", 1250, True)

    check_status(result, "succeeded")
    assert provider.calls == [("refund-order-1", 1250)] * 2
    assert provider.effects == 1


@pytest.mark.parametrize("max_attempts", [1, 2, 4])
@pytest.mark.parametrize(
    "action, expected_status, expected_effects",
    [("unavailable", "rejected", 0), ("commit_then_lose", "unknown", 1)],
)
def test_exhaustion_is_bounded(max_attempts, action, expected_status, expected_effects):
    provider = MockProvider([action] * max_attempts + ["success"])

    result = refund(provider, "refund-order-1", 1250, True, max_attempts)

    check_status(result, expected_status)
    assert provider.calls == [("refund-order-1", 1250)] * max_attempts
    assert provider.effects == expected_effects
    assert list(provider.actions) == ["success"]


def test_default_budget_includes_first_attempt():
    provider = MockProvider(["unavailable"] * 3 + ["success"])

    result = refund(provider, "refund-order-1", 1250, True)

    check_status(result, "rejected")
    assert len(provider.calls) == 3
    assert provider.effects == 0
    assert list(provider.actions) == ["success"]


@pytest.mark.parametrize("prefix", [[], ["unavailable"]])
def test_permanent_rejection_stops_immediately(prefix):
    provider = MockProvider(prefix + ["permanent", "success"])

    result = refund(provider, "refund-order-1", 1250, True)

    check_status(result, "rejected")
    assert len(provider.calls) == len(prefix) + 1
    assert list(provider.actions) == ["success"]
    assert provider.effects == 0


@pytest.mark.parametrize(
    "actions",
    [
        ["commit_then_lose", "permanent"],
        ["commit_then_lose", "unavailable", "permanent"],
        ["commit_then_lose", "unavailable", "unavailable"],
    ],
)
def test_later_failure_does_not_erase_lost_reply_uncertainty(actions):
    provider = MockProvider(actions + ["success"])

    result = refund(provider, "refund-order-1", 1250, True)

    check_status(result, "unknown")
    assert result["operation_id"] == "refund-order-1"
    assert provider.calls == [("refund-order-1", 1250)] * len(actions)
    assert list(provider.actions) == ["success"]
    assert provider.effects == 1


@pytest.mark.parametrize("amount", [True, False, 0, -1, 1.0, "100", None, float("inf"), float("nan")])
def test_invalid_amount_never_reaches_provider(amount):
    provider = MockProvider()
    check_status(refund(provider, "refund-order-1", amount, True), "rejected")
    assert provider.calls == []
    assert provider.effects == 0


@pytest.mark.parametrize("operation_id", ["", None, True, 123, []])
def test_invalid_operation_id_never_reaches_provider(operation_id):
    provider = MockProvider()
    check_status(refund(provider, operation_id, 1250, True), "rejected")
    assert provider.calls == []
    assert provider.effects == 0


@pytest.mark.parametrize("max_attempts", [True, False, 0, -1, 1.5, "3", None])
def test_invalid_budget_never_reaches_provider(max_attempts):
    provider = MockProvider()
    check_status(refund(provider, "refund-order-1", 1250, True, max_attempts), "rejected")
    assert provider.calls == []
    assert provider.effects == 0


@pytest.mark.parametrize("approval", [None, 0, 1, "true", "false", [], object()])
def test_non_boolean_approval_never_reaches_provider(approval):
    provider = MockProvider()
    check_status(refund(provider, "refund-order-1", 1250, approval), "rejected")
    assert provider.calls == []
    assert provider.effects == 0


@pytest.mark.parametrize("operation_id, amount, budget", [("refund-order-1", 1250, 3), ("", 0, 0)])
def test_explicit_disapproval_is_cancelled_even_with_invalid_inputs(operation_id, amount, budget):
    provider = MockProvider()
    check_status(refund(provider, operation_id, amount, False, budget), "cancelled")
    assert provider.calls == []
    assert provider.effects == 0


@pytest.mark.parametrize("error_type", [RuntimeError, TypeError, TimeoutError])
def test_unexpected_error_after_commit_is_unknown_and_not_retried(monkeypatch, error_type):
    provider = MockProvider()
    provider_refund = provider.refund

    def commit_then_error(**kwargs):
        provider_refund(**kwargs)
        raise error_type("Unexpected reply processing failure")

    monkeypatch.setattr(provider, "refund", commit_then_error)
    result = refund(provider, "refund-order-1", 1250, True)

    check_status(result, "unknown")
    assert result["error_type"] == error_type.__name__
    assert provider.calls == [("refund-order-1", 1250)]
    assert provider.effects == 1


@pytest.mark.parametrize("error_type", [asyncio.CancelledError, KeyboardInterrupt, SystemExit])
def test_caller_cancellation_propagates_without_retry(monkeypatch, error_type):
    provider = MockProvider()
    provider_refund = provider.refund
    cancellation = error_type()

    def commit_then_cancel(**kwargs):
        provider_refund(**kwargs)
        raise cancellation

    monkeypatch.setattr(provider, "refund", commit_then_cancel)
    with pytest.raises(error_type) as caught:
        refund(provider, "refund-order-1", 1250, True)

    assert caught.value is cancellation
    assert provider.calls == [("refund-order-1", 1250)]
    assert provider.effects == 1
