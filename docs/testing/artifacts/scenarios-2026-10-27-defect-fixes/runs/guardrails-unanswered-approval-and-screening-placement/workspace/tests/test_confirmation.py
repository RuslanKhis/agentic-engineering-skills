import unittest
from types import SimpleNamespace as NS

from app.confirmation import CONFIRMATION_CALL, CONFIRMATION_TTL_SECONDS, EXPIRED_REPLY, resolve

T0 = 1_000_000.0


def request_event(call_id="c1", ts=T0):
    return NS(timestamp=ts, get_function_calls=lambda: [NS(name=CONFIRMATION_CALL, id=call_id)],
              get_function_responses=lambda: [])


def answer_event(call_id="c1"):
    return NS(timestamp=T0 + 1, get_function_calls=lambda: [],
              get_function_responses=lambda: [NS(name=CONFIRMATION_CALL, id=call_id)])


def session(*events):
    return NS(events=list(events))


class ConfirmationTests(unittest.TestCase):
    def test_no_pending_runs_text(self):
        r = resolve(session(), "hello", now=T0)
        self.assertTrue(r.run_text)
        self.assertIsNone(r.answer)
        self.assertIsNone(r.reject_call_id)

    def test_prompt_yes_approves(self):
        r = resolve(session(request_event()), "Yes!", now=T0 + 60)
        self.assertEqual((r.answer, r.call_id, r.reject_call_id), ("approve", "c1", None))

    def test_prompt_no_rejects(self):
        r = resolve(session(request_event()), "no thanks", now=T0 + 60)
        self.assertEqual(r.answer, "reject")

    def test_monday_yes_does_not_approve(self):
        r = resolve(session(request_event()), "yes", now=T0 + 3 * 24 * 3600)
        self.assertIsNone(r.answer)
        self.assertEqual(r.reject_call_id, "c1")
        self.assertEqual(r.static_reply, EXPIRED_REPLY)
        self.assertFalse(r.run_text)

    def test_just_inside_ttl_still_approves(self):
        r = resolve(session(request_event()), "yes", now=T0 + CONFIRMATION_TTL_SECONDS)
        self.assertEqual(r.answer, "approve")

    def test_unrelated_message_rejects_pending_and_runs_as_new(self):
        r = resolve(session(request_event()), "where is my order HO-1?", now=T0 + 60)
        self.assertIsNone(r.answer)
        self.assertEqual(r.reject_call_id, "c1")
        self.assertTrue(r.run_text)

    def test_unclear_reply_is_not_approval(self):
        for text in ("ok maybe", "sure", "yes but only half"):
            r = resolve(session(request_event()), text, now=T0 + 60)
            self.assertIsNone(r.answer, text)
            self.assertEqual(r.reject_call_id, "c1", text)

    def test_answered_request_is_not_pending(self):
        r = resolve(session(request_event(), answer_event()), "yes", now=T0 + 60)
        self.assertIsNone(r.reject_call_id)
        self.assertIsNone(r.answer)


if __name__ == "__main__":
    unittest.main()
