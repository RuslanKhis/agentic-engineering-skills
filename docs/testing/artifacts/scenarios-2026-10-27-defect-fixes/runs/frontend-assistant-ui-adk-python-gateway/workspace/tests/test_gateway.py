import unittest
from types import SimpleNamespace as NS

from app import gateway
from app.gateway import BadRequest


def fn_call(id, name, args=None):
    return NS(function_call=NS(id=id, name=name, args=args or {}), function_response=None, text=None, thought=False)


def fn_resp(id, name, response):
    return NS(function_call=None, function_response=NS(id=id, name=name, response=response), text=None, thought=False)


def text(t, thought=False):
    return NS(function_call=None, function_response=None, text=t, thought=thought)


def event(inv, author, *parts, rewind_before=None):
    return NS(invocation_id=inv, author=author, content=NS(parts=list(parts)),
              actions=NS(rewind_before_invocation_id=rewind_before))


def body(**kw):
    return dict({"sessionId": "s1", "parts": [{"text": "hi"}]}, **kw)


class ParseRequestTests(unittest.TestCase):
    def test_plain_message(self):
        turn = gateway.parse_request(body())
        self.assertEqual((turn.text, turn.approvals, turn.checkpoint), ("hi", (), None))

    def test_message_shorthand(self):
        self.assertEqual(gateway.parse_request({"sessionId": "s1", "message": "yo"}).text, "yo")

    def test_state_delta_is_refused(self):
        with self.assertRaises(BadRequest) as ctx:
            gateway.parse_request(body(stateDelta={"user:role": "admin"}))
        self.assertEqual(ctx.exception.code, "state_not_accepted")

    def test_user_id_in_body_is_ignored(self):
        turn = gateway.parse_request(body(userId="someone-else"))
        self.assertFalse(hasattr(turn, "user_id"))

    def test_bad_session_id_and_checkpoint(self):
        for bad in (body(sessionId="../x"), body(sessionId=None), body(checkpointId="before:1"), []):
            with self.assertRaises(BadRequest):
                gateway.parse_request(bad)

    def test_unsupported_parts_are_refused(self):
        for part in ({"text": "x", "thought": True}, {"inlineData": {}}, {"functionCall": {"name": "x"}, "text": "y"}):
            with self.assertRaises(BadRequest, msg=part):
                gateway.parse_request(body(parts=[part]))

    def test_oversized_text(self):
        with self.assertRaises(BadRequest):
            gateway.parse_request(body(parts=[{"text": "x" * (gateway.MAX_TEXT_CHARS + 1)}]))

    def test_approval_shape_is_exact(self):
        ok = {"functionResponse": {"id": "c1", "name": gateway.CONFIRMATION_CALL, "response": {"confirmed": True}}}
        turn = gateway.parse_request(body(parts=[ok]))
        self.assertEqual(turn.approvals, (gateway.Approval("c1", True),))
        for resp in ({"confirmed": "yes"}, {"confirmed": True, "payload": 1}, {}):
            bad = {"functionResponse": {"id": "c1", "name": gateway.CONFIRMATION_CALL, "response": resp}}
            with self.assertRaises(BadRequest):
                gateway.parse_request(body(parts=[bad]))
        other = {"functionResponse": {"id": "c1", "name": "issue_refund", "response": {"confirmed": True}}}
        with self.assertRaises(BadRequest):
            gateway.parse_request(body(parts=[other]))

    def test_approval_beside_text_is_accepted(self):
        ok = {"functionResponse": {"id": "c1", "name": gateway.CONFIRMATION_CALL, "response": {"confirmed": False}}}
        turn = gateway.parse_request(body(parts=[ok, {"text": "never mind"}]))
        self.assertEqual((len(turn.approvals), turn.text), (1, "never mind"))

    def test_regenerate_has_empty_text_with_checkpoint(self):
        turn = gateway.parse_request(body(parts=[{"text": ""}], checkpointId="start"))
        self.assertEqual((turn.text, turn.checkpoint), ("", "start"))
        with self.assertRaises(BadRequest):
            gateway.parse_request(body(parts=[{"text": ""}]))


def history():
    return gateway.summarize([
        event("i1", "user", text("where is HO-10442?")),
        event("i1", "support_assistant", text("Shipped.")),
        event("i2", "user", text("refund 500")),
        event("i2", "support_assistant", fn_call("c1", "issue_refund", {"order_id": "HO-10442"}),
              fn_call("q1", gateway.CONFIRMATION_CALL)),
    ])


class ApprovalTests(unittest.TestCase):
    def test_pending_is_accepted_once(self):
        gateway.check_approvals(history(), [gateway.Approval("q1", True)])
        with self.assertRaises(BadRequest):
            gateway.check_approvals(history(), [gateway.Approval("q1", True), gateway.Approval("q1", False)])

    def test_unknown_or_answered_is_refused(self):
        with self.assertRaises(BadRequest):
            gateway.check_approvals(history(), [gateway.Approval("zzz", True)])
        answered = history() + gateway.summarize([event("i2", "user", fn_resp("q1", gateway.CONFIRMATION_CALL, {}))])
        with self.assertRaises(BadRequest):
            gateway.check_approvals(answered, [gateway.Approval("q1", True)])

    def test_rewound_confirmation_is_not_pending(self):
        rewound = history() + gateway.summarize([event("i3", "user", rewind_before="i2")])
        with self.assertRaises(BadRequest):
            gateway.check_approvals(rewound, [gateway.Approval("q1", True)])


class EditTests(unittest.TestCase):
    def test_edit_first_message_rewinds_before_first_invocation(self):
        plan = gateway.plan_edit(history(), "start")
        self.assertEqual((plan.before_invocation_id, plan.user_text), ("i1", "where is HO-10442?"))

    def test_edit_later_message(self):
        plan = gateway.plan_edit(history(), "after:i1")
        self.assertEqual((plan.before_invocation_id, plan.user_text), ("i2", "refund 500"))

    def test_checkpoint_at_tail_means_append(self):
        self.assertIsNone(gateway.plan_edit(history(), "after:i2").before_invocation_id)

    def test_unknown_checkpoint(self):
        with self.assertRaises(BadRequest) as ctx:
            gateway.plan_edit(history(), "after:nope")
        self.assertEqual(ctx.exception.code, "checkpoint_unknown")

    def test_rewind_past_completed_refund_is_blocked(self):
        done = history() + gateway.summarize([
            event("i2", "support_assistant", fn_resp("c1", "issue_refund", {"status": "refunded"}))])
        with self.assertRaises(BadRequest) as ctx:
            gateway.plan_edit(done, "after:i1")
        self.assertEqual(ctx.exception.code, "rewind_blocked")

    def test_rewind_past_failed_refund_is_allowed(self):
        failed = history() + gateway.summarize([
            event("i2", "support_assistant", fn_resp("c1", "issue_refund", {"status": "error", "message": "x"}))])
        self.assertEqual(gateway.plan_edit(failed, "after:i1").before_invocation_id, "i2")

    def test_second_edit_sees_only_live_history(self):
        steps = history() + gateway.summarize([event("i3", "user", rewind_before="i2"),
                                               event("i4", "user", text("refund 200"))])
        self.assertEqual([s.invocation_id for s in gateway.live_steps(steps)], ["i1", "i1", "i4"])
        self.assertEqual(gateway.plan_edit(steps, "after:i1").before_invocation_id, "i4")


class PublicEventTests(unittest.TestCase):
    AGENT = "support_assistant"

    def test_thoughts_state_and_metadata_are_dropped(self):
        ev = {"id": "e1", "invocationId": "i1", "author": self.AGENT,
              "content": {"role": "model", "parts": [{"text": "secret plan", "thought": True}, {"text": "Hello"}]},
              "actions": {"stateDelta": {"user:token": "SECRET"}}, "usageMetadata": {"totalTokenCount": 9},
              "groundingMetadata": {"x": 1}}
        out = gateway.public_event(ev, self.AGENT)
        self.assertEqual(out["content"]["parts"], [{"text": "Hello"}])
        self.assertNotIn("SECRET", repr(out))
        self.assertNotIn("actions", out)
        self.assertNotIn("usageMetadata", out)

    def test_thought_only_and_foreign_author_events_vanish(self):
        thought = {"author": self.AGENT, "content": {"parts": [{"text": "x", "thought": True}]}}
        self.assertIsNone(gateway.public_event(thought, self.AGENT))
        other = {"author": "other_agent", "content": {"parts": [{"text": "x"}]}}
        self.assertIsNone(gateway.public_event(other, self.AGENT))

    def test_error_text_is_replaced(self):
        out = gateway.public_event({"errorCode": "500", "errorMessage": "Traceback /srv/db password=hunter2",
                                    "invocationId": "i1"}, self.AGENT)
        self.assertEqual(out["errorMessage"], gateway.FIXED_ERROR["errorMessage"])
        self.assertNotIn("hunter2", repr(out))

    def test_confirmation_keeps_original_call_and_long_running_ids(self):
        ev = {"id": "e2", "invocationId": "i2", "author": self.AGENT, "longRunningToolIds": ["q1"],
              "content": {"role": "model", "parts": [{"functionCall": {
                  "id": "q1", "name": gateway.CONFIRMATION_CALL,
                  "args": {"originalFunctionCall": {"id": "c1", "name": "issue_refund",
                                                    "args": {"order_id": "HO-1", "amount_cents": 500}},
                           "toolConfirmation": {"hint": "Refund 5.00", "payload": {"internal": "x"}}}}}]}}
        out = gateway.public_event(ev, self.AGENT)
        args = out["content"]["parts"][0]["functionCall"]["args"]
        self.assertEqual(args["originalFunctionCall"]["id"], "c1")
        self.assertEqual(args["toolConfirmation"], {"hint": "Refund 5.00"})
        self.assertEqual(out["longRunningToolIds"], ["q1"])

    def test_tool_results_are_allowlisted(self):
        def result(name, response):
            ev = {"author": self.AGENT, "content": {"parts": [{"functionResponse": {
                "id": "x", "name": name, "response": response}}]}}
            return gateway.public_event(ev, self.AGENT)["content"]["parts"][0]["functionResponse"]["response"]
        self.assertEqual(result("issue_refund", {"status": "refunded", "refund_id": "rf_1", "amount_cents": 500,
                                                 "provider_id": "pay_9"}),
                         {"status": "refunded", "refund_id": "rf_1", "amount_cents": 500})
        self.assertEqual(result("lookup_order", {"status": "ok", "customer_email": "a@b.c"}), {"status": "ok"})


if __name__ == "__main__":
    unittest.main()
