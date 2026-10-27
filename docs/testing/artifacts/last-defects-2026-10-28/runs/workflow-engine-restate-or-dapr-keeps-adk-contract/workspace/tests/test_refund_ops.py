"""Refund operations against fakes: the review record, the decision and the single payment write.

These prove the application's side of the contract. They do not exercise Restate: that the engine
re-runs `execute` after a crash is its documented behaviour, and is checked in the list in
docs/refund-durability.md.
"""
import unittest

from app import refund_ops, services
from app.clients.http import Response
from app.clients.payments import PaymentsError
from tests.fakes import configure_fakes

ANA = ("cust-ana", "ana@example.test")
MIA = ("mgr-mia", "Mia@Harbour.test")  # manager; the allowlist is lower-case
T0 = "2026-10-28T09:00:00.000000Z"
T_LATE = "2026-11-20T09:00:00.000000Z"  # past the 14-day expiry


def submit(amount=2_500, now=T0):
    return refund_ops.submit("cust-ana", "HO-10442", amount, "Jacket arrived torn", now=now)


class RefundOpsTests(unittest.TestCase):
    def setUp(self):
        self.store, self.pay, _ = configure_fakes()
        self.reviews = services.get().reviews

    def op_id(self, result=None):
        return (result or submit())["operation_id"]

    # submit
    def test_submit_is_pending_pays_nothing_and_starts_one_workflow(self):
        result = submit()
        self.assertEqual(result["status"], "pending_approval")
        self.assertFalse(result["payment_processed"])
        self.assertEqual(self.pay.requests, [])
        self.assertEqual(self.reviews.started, [result["operation_id"]])

    def test_repeat_submit_returns_the_same_operation(self):
        first, second = submit(), submit()
        self.assertEqual(first["operation_id"], second["operation_id"])
        self.assertEqual(self.store.conn.execute("SELECT COUNT(*) FROM refund_ops").fetchone()[0], 1)

    def test_invalid_requests_create_nothing(self):
        for args in (("cust-ana", "HO-20001", 100), ("cust-ana", "HO-10442", 9_000),
                     ("cust-ana", "HO-10442", 0), ("cust-ana", "HO-10442", True)):
            self.assertEqual(refund_ops.submit(*args, "x", now=T0)["status"], "error")
        self.assertEqual(self.store.conn.execute("SELECT COUNT(*) FROM refund_ops").fetchone()[0], 0)
        self.assertEqual(self.reviews.started, [])

    def test_a_queueing_failure_leaves_a_saved_request_that_a_repeat_heals(self):
        self.reviews.fail = True
        self.assertEqual(submit()["status"], "error")
        self.reviews.fail = False
        healed = submit()
        self.assertEqual(healed["status"], "pending_approval")
        self.assertEqual(self.reviews.started, [healed["operation_id"]])

    # decision authority
    def test_only_a_listed_manager_may_decide(self):
        op_id = self.op_id()
        with self.assertRaises(refund_ops.ReviewRefused) as ctx:
            refund_ops.review(op_id, True, "cust-ben", "ben@example.test", now=T0)
        self.assertEqual(ctx.exception.code, "forbidden")
        self.assertEqual(self.store.get_refund_op(op_id)["state"], "pending")
        self.assertEqual(self.reviews.woken, [])

    def test_a_manager_cannot_approve_their_own_refund(self):
        op_id = self.op_id()
        with self.assertRaises(refund_ops.ReviewRefused) as ctx:
            refund_ops.review(op_id, True, "cust-ana", "mia@harbour.test", now=T0)
        self.assertEqual(ctx.exception.code, "self_approval")

    def test_unknown_operation_is_not_found(self):
        with self.assertRaises(refund_ops.ReviewRefused) as ctx:
            refund_ops.review("rf-nope-1", True, *MIA, now=T0)
        self.assertEqual(ctx.exception.code, "not_found")

    # approve, pay once
    def test_approval_alone_pays_nothing_then_execute_pays_once_with_the_operation_key(self):
        op_id = self.op_id()
        approved = refund_ops.review(op_id, True, *MIA, now=T0)
        self.assertEqual(approved["status"], "approved")
        self.assertFalse(approved["payment_processed"])
        self.assertEqual(self.pay.requests, [])
        self.assertEqual(self.reviews.woken, [op_id])
        done = refund_ops.execute(op_id)
        self.assertEqual(done["status"], "completed")
        self.assertTrue(done["payment_processed"])
        self.assertEqual(len(self.pay.requests), 1)
        self.assertEqual(self.pay.requests[0]["headers"]["Idempotency-Key"], op_id)
        self.assertEqual(self.pay.requests[0]["json"]["amount_cents"], 2_500)
        self.assertEqual(len(self.store.refunds_for("HO-10442")), 1)

    def test_duplicate_approval_and_repeated_execute_make_one_payment(self):
        op_id = self.op_id()
        refund_ops.review(op_id, True, *MIA, now=T0)
        refund_ops.review(op_id, True, *MIA, now=T0)
        refund_ops.execute(op_id)
        refund_ops.execute(op_id)
        self.assertEqual(len(self.pay.requests), 1)
        self.assertEqual(len(self.store.refunds_for("HO-10442")), 1)

    def test_a_second_conflicting_decision_does_not_overturn_the_first(self):
        op_id = self.op_id()
        refund_ops.review(op_id, False, *MIA, now=T0)
        again = refund_ops.review(op_id, True, *MIA, now=T0)
        self.assertEqual(again["status"], "rejected")
        refund_ops.execute(op_id)
        self.assertEqual(self.pay.requests, [])

    def test_execute_before_any_decision_writes_nothing(self):
        op_id = self.op_id()
        self.assertEqual(refund_ops.execute(op_id)["status"], "pending_approval")
        self.assertEqual(self.pay.requests, [])

    # crash points
    def test_crash_after_the_provider_accepted_reruns_with_the_same_key_and_one_refund_row(self):
        op_id = self.op_id()
        refund_ops.review(op_id, True, *MIA, now=T0)
        real_finish = self.store.finish_refund_op
        calls = []

        def crash_once(*args, **kwargs):
            calls.append(1)
            if len(calls) == 1:
                raise RuntimeError("worker killed after the provider answered")
            return real_finish(*args, **kwargs)

        self.store.finish_refund_op = crash_once
        with self.assertRaises(RuntimeError):
            refund_ops.execute(op_id)
        self.assertEqual(self.store.get_refund_op(op_id)["state"], "executing")  # not assumed failed
        self.assertEqual(refund_ops.execute(op_id)["status"], "completed")  # the engine re-runs the step
        keys = {r["headers"]["Idempotency-Key"] for r in self.pay.requests}
        self.assertEqual(keys, {op_id})  # the provider dedups a repeated key to one refund
        self.assertEqual(len(self.store.refunds_for("HO-10442")), 1)

    def test_transient_provider_error_raises_for_retry_and_then_completes(self):
        self.store, self.pay, _ = configure_fakes(payments_responses=[Response(503, {})])
        op_id = refund_ops.submit("cust-ana", "HO-10442", 1_000, "x", now=T0)["operation_id"]
        refund_ops.review(op_id, True, *MIA, now=T0)
        with self.assertRaises(PaymentsError):
            refund_ops.execute(op_id)
        self.assertEqual(refund_ops.execute(op_id)["status"], "completed")
        self.assertEqual({r["headers"]["Idempotency-Key"] for r in self.pay.requests}, {op_id})

    def test_final_provider_refusal_fails_without_a_refund_row(self):
        self.store, self.pay, _ = configure_fakes(payments_responses=[Response(402, {})])
        op_id = refund_ops.submit("cust-ana", "HO-10442", 1_000, "x", now=T0)["operation_id"]
        refund_ops.review(op_id, True, *MIA, now=T0)
        self.assertEqual(refund_ops.execute(op_id)["status"], "failed")
        self.assertEqual(self.store.refunds_for("HO-10442"), [])

    def test_exhausted_retries_end_as_outcome_unknown_not_failed(self):
        op_id = self.op_id()
        refund_ops.review(op_id, True, *MIA, now=T0)
        self.store.claim_refund_op(op_id)
        self.assertEqual(refund_ops.mark_outcome_unknown(op_id)["status"], "outcome_unknown")
        self.assertEqual(refund_ops.execute(op_id)["status"], "outcome_unknown")  # no further write
        self.assertEqual(self.pay.requests, [])

    # expiry
    def test_approval_after_expiry_cannot_revive_the_operation(self):
        op_id = self.op_id()
        refund_ops.review(op_id, True, *MIA, now=T_LATE)
        self.assertEqual(self.store.get_refund_op(op_id)["state"], "pending")  # decision refused
        self.assertEqual(refund_ops.expire(op_id, now=T_LATE)["status"], "expired")
        refund_ops.review(op_id, True, *MIA, now=T_LATE)
        self.assertEqual(refund_ops.execute(op_id)["status"], "expired")
        self.assertEqual(self.pay.requests, [])

    def test_timer_firing_after_an_approval_leaves_the_approval_standing(self):
        op_id = self.op_id()
        refund_ops.review(op_id, True, *MIA, now=T0)
        self.assertEqual(refund_ops.expire(op_id, now=T_LATE)["status"], "approved")
        self.assertEqual(refund_ops.execute(op_id)["status"], "completed")

    def test_expiry_timer_before_the_deadline_does_nothing(self):
        op_id = self.op_id()
        self.assertEqual(refund_ops.expire(op_id, now=T0)["status"], "pending_approval")
        self.assertGreater(refund_ops.seconds_until_expiry(op_id, now=T0), 13 * 86_400)

    def test_customer_can_ask_again_after_a_rejection_with_a_new_operation_and_key(self):
        first = self.op_id()
        refund_ops.review(first, False, *MIA, now=T0)
        second = self.op_id()
        self.assertNotEqual(first, second)
        refund_ops.review(second, True, *MIA, now=T0)
        refund_ops.execute(second)
        self.assertEqual(self.pay.requests[0]["headers"]["Idempotency-Key"], second)

    # status
    def test_status_is_visible_to_the_requester_and_managers_only(self):
        op_id = self.op_id()
        self.assertEqual(refund_ops.status(op_id, *ANA)["status"], "pending_approval")
        self.assertEqual(refund_ops.status(op_id, *MIA)["status"], "pending_approval")
        self.assertIsNone(refund_ops.status(op_id, "cust-ben", "ben@example.test"))
        self.assertIsNone(refund_ops.status("rf-nope-1", *ANA))


if __name__ == "__main__":
    unittest.main()
