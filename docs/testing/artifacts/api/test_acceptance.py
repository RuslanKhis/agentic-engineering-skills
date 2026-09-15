import pytest
from provider import MockProvider
from refund_tool import refund


def call(p, **kw):
    args = dict(operation_id="refund-order-42", amount_cents=1900, approved=True)
    args.update(kw)
    result = refund(p, **args)
    assert isinstance(result, dict)
    assert result["status"] in {"succeeded", "rejected", "cancelled", "unknown"}
    assert isinstance(result["message"], str) and result["message"]
    return result

@pytest.mark.parametrize("approval", [False, None, 1, "yes"])
def test_unapproved_never_calls_provider(approval):
    p=MockProvider()
    result=call(p, approved=approval)
    assert result["status"] in {"cancelled", "rejected"}
    assert p.calls == []

@pytest.mark.parametrize("amount", [0, -1, 1.5, True, "1900"])
def test_invalid_money_never_calls_provider(amount):
    p=MockProvider()
    assert call(p, amount_cents=amount)["status"] == "rejected"
    assert p.calls == []

def test_retry_and_reinvocation_share_identity():
    p=MockProvider(["commit_then_lose", "success"])
    assert call(p)["status"] == "succeeded"
    assert call(p)["status"] == "succeeded"
    assert p.effects == 1
    assert len({key for key, _ in p.calls}) == 1
    assert 2 <= len(p.calls) <= 3

def test_transient_attempts_are_bounded():
    p=MockProvider(["unavailable"]*20)
    assert call(p, max_attempts=3)["status"] == "rejected"
    assert len(p.calls) == 3
    assert p.effects == 0

def test_permanent_failure_is_not_retried():
    p=MockProvider(["permanent", "success"])
    assert call(p)["status"] == "rejected"
    assert len(p.calls) == 1
    assert p.effects == 0

def test_ambiguous_exhaustion_is_unknown():
    p=MockProvider(["commit_then_lose"]*20)
    assert call(p, max_attempts=2)["status"] == "unknown"
    assert len(p.calls) == 2
    assert p.effects == 1

def test_later_rejection_does_not_erase_uncertainty():
    p=MockProvider(["commit_then_lose", "permanent", "success"])
    assert call(p)["status"] == "unknown"
    assert len(p.calls) == 2
    assert p.effects == 1

def test_payload_mismatch_cannot_create_second_refund():
    p=MockProvider()
    assert call(p)["status"] == "succeeded"
    assert call(p, amount_cents=2500)["status"] == "rejected"
    assert p.effects == 1
    assert len(p.calls) <= 2

def test_distinct_operations_stay_distinct():
    p=MockProvider()
    assert call(p)["status"] == "succeeded"
    assert call(p, operation_id="refund-order-43")["status"] == "succeeded"
    assert p.effects == 2
