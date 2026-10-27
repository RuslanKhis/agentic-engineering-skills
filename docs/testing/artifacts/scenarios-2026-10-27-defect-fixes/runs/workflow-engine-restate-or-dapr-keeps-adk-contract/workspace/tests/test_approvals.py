"""The approval workflow driven without Dapr: a scripted context stands in for the engine.

The driver replays what the engine does: it resolves each when_any as scripted, runs the payment
activity for real against the provider double, and re-runs a failed activity as the retry policy would.
It proves the workflow body and activity; it does not prove Dapr's own replay, timers or events.
"""
import json
import os
import unittest
from datetime import datetime
from unittest import mock

from app import approvals, services
from app.approvals import RefundRequest, check_decision, refund_approval_workflow, refund_key
from app.settings import Settings
from tests.fakes import DedupingTransport, configure_fakes


class FakeTask:
    def __init__(self, kind, **fields):
        self.kind, self.result = kind, None
        self.__dict__.update(fields)

    def get_result(self):
        return self.result


class FakeCtx:
    current_utc_datetime = datetime(2026, 10, 28, 9, 0)

    def __init__(self):
        self.retry_policies = []

    def create_timer(self, due):
        return FakeTask("timer", due=due)

    def wait_for_external_event(self, name):
        return FakeTask("event", name=name)

    def when_any(self, tasks):
        return FakeTask("any", children=list(tasks))

    def call_activity(self, fn, *, input=None, retry_policy=None):
        self.retry_policies.append(retry_policy)
        return FakeTask("activity", fn=fn, input=input)


def drive(payload, script, attempts=3):
    """Run the workflow. script: one step per wait, ("decision", dict) or ("expire",)."""
    ctx, steps, value = FakeCtx(), iter(script), None
    gen = refund_approval_workflow(ctx, json.loads(json.dumps(payload)))  # input survives serialisation
    try:
        while True:
            task = gen.send(value)
            if task.kind == "any":
                step = next(steps)
                if step[0] == "expire":
                    value = next(c for c in task.children if c.kind == "timer")
                else:
                    value = next(c for c in task.children if c.kind == "event")
                    value.result = step[1]
            else:
                for attempt in range(attempts):
                    try:
                        value = task.fn(None, task.input)
                        break
                    except Exception:
                        if attempt == attempts - 1:
                            raise
    except StopIteration as stop:
        return stop.value


def make_request(user="cust-ana", order="HO-10442", cents=2_500, reason="Jacket arrived torn"):
    return RefundRequest(refund_key(user, order, cents), user, order, cents, reason)


def decision(req, reviewer="mgr-1", approved=True, digest=None):
    return ("decision", {"reviewer_id": reviewer, "approved": approved, "digest": digest or req.digest})


class CheckDecisionTests(unittest.TestCase):
    def test_valid_decision_stands(self):
        req = make_request()
        self.assertIsNone(check_decision(req, decision(req)[1]))

    def test_each_defect_is_named(self):
        req = make_request()
        good = decision(req)[1]
        self.assertEqual(check_decision(req, {**good, "digest": "stale"}), "digest_mismatch")
        self.assertEqual(check_decision(req, {**good, "reviewer_id": req.user_id}), "self_approval")
        self.assertEqual(check_decision(req, {**good, "reviewer_id": ""}), "no_reviewer")
        self.assertEqual(check_decision(req, {**good, "approved": "yes"}), "malformed")

    def test_digest_changes_with_amount(self):
        self.assertNotEqual(make_request(cents=2_500).digest, make_request(cents=2_600).digest)


class WorkflowTests(unittest.TestCase):
    def setUp(self):
        self.provider = DedupingTransport()
        self.store, _, _ = configure_fakes(payments_transport=self.provider)
        self.req = make_request()

    def test_approval_pays_once_with_the_operation_key(self):
        out = drive(self.req.to_dict(), [decision(self.req)])
        self.assertEqual(out["status"], "refunded")
        self.assertEqual(out["reviewer_id"], "mgr-1")
        self.assertEqual(list(self.provider.effects), [self.req.operation_id])
        self.assertEqual(len(self.store.refunds_for("HO-10442")), 1)

    def test_decline_pays_nothing(self):
        out = drive(self.req.to_dict(), [decision(self.req, approved=False)])
        self.assertEqual(out["status"], "declined")
        self.assertEqual(self.provider.requests, [])

    def test_expiry_pays_nothing(self):
        out = drive(self.req.to_dict(), [("expire",)])
        self.assertEqual(out["status"], "expired")
        self.assertEqual(self.provider.requests, [])

    def test_self_approval_and_stale_digest_are_ignored_until_a_manager_decides(self):
        script = [decision(self.req, reviewer=self.req.user_id), decision(self.req, digest="old"),
                  decision(self.req)]
        out = drive(self.req.to_dict(), script)
        self.assertEqual(out["status"], "refunded")
        self.assertEqual(len(self.provider.effects), 1)

    def test_ignored_decisions_do_not_cancel_expiry(self):
        out = drive(self.req.to_dict(), [decision(self.req, digest="old"), ("expire",)])
        self.assertEqual(out["status"], "expired")
        self.assertEqual(self.provider.requests, [])

    def test_preconditions_are_rechecked_at_payment_time(self):
        services.get().max_refund_cents = 1_000  # limit lowered while the request waited
        out = drive(self.req.to_dict(), [decision(self.req)])
        self.assertEqual(out["status"], "invalid")
        self.assertEqual(self.provider.requests, [])

    def test_payment_activity_gets_the_retry_policy_slot(self):
        approvals.ACTIVITY_RETRY = "policy"
        self.addCleanup(setattr, approvals, "ACTIVITY_RETRY", None)
        ctx = FakeCtx()
        gen = refund_approval_workflow(ctx, self.req.to_dict())
        task = gen.send(None)
        task.children[0].result = decision(self.req)[1]
        gen.send(task.children[0])
        self.assertEqual(ctx.retry_policies, ["policy"])


class PaymentActivityTests(unittest.TestCase):
    def test_crash_after_provider_accepted_gives_one_effect(self):
        """The pod dies after the provider took the write; the retry carries the same key."""
        provider = DedupingTransport(lose_response_first_n=1)
        store, _, _ = configure_fakes(payments_transport=provider)
        req = make_request()
        out = drive(req.to_dict(), [decision(req)])
        self.assertEqual(out["status"], "refunded")
        self.assertEqual(len(provider.requests), 2)  # the retry happened
        self.assertEqual({r["headers"]["Idempotency-Key"] for r in provider.requests}, {req.operation_id})
        self.assertEqual(len(provider.effects), 1)
        self.assertEqual(len(store.refunds_for("HO-10442")), 1)

    def test_crash_after_payment_before_the_checkpoint_does_not_duplicate_the_record(self):
        provider = DedupingTransport()
        store, _, _ = configure_fakes(payments_transport=provider)
        req = make_request()
        approvals.execute_refund(req)
        approvals.execute_refund(req)  # the engine re-ran the activity
        self.assertEqual(len(provider.effects), 1)
        self.assertEqual(len(store.refunds_for("HO-10442")), 1)

    def test_terminal_provider_rejection_is_an_outcome_not_a_retry(self):
        provider = DedupingTransport(fail_status=402)
        store, _, _ = configure_fakes(payments_transport=provider)
        req = make_request()
        out = drive(req.to_dict(), [decision(req)])
        self.assertEqual(out["status"], "rejected")
        self.assertEqual(len(provider.requests), 1)
        self.assertEqual(store.refunds_for("HO-10442"), [])

    def test_provider_5xx_propagates_so_the_engine_retries(self):
        configure_fakes(payments_transport=DedupingTransport(fail_status=503))
        with self.assertRaises(approvals.PaymentsError):
            approvals.execute_refund(make_request())


class SettingsTests(unittest.TestCase):
    def test_approvers_are_parsed_and_default_empty(self):
        with mock.patch.dict(os.environ, {"REFUND_APPROVER_EMAILS": " A@x.com, b@x.com ,"}):
            self.assertEqual(Settings.from_env().approver_emails, frozenset({"a@x.com", "b@x.com"}))
        with mock.patch.dict(os.environ, {}, clear=True):
            self.assertEqual(Settings.from_env().approver_emails, frozenset())


if __name__ == "__main__":
    unittest.main()
