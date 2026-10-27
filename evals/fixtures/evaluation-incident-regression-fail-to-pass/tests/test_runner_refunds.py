"""Runner tests with a scripted model. They need google-adk; they skip without it."""
import asyncio
import unittest

try:
    from google.adk.agents import LlmAgent
    from google.adk.runners import InMemoryRunner
except ModuleNotFoundError:  # google-adk not installed
    raise unittest.SkipTest("google-adk is not installed")

from app.prompts import ROOT_INSTRUCTION
from app.tools.orders import lookup_order
from app.tools.refunds import issue_refund, propose_refund
from tests.fakes import configure_fakes
from tests.scripted_model import ScriptedModel, call, text, user


def build(script):
    model = ScriptedModel(script=list(script))
    agent = LlmAgent(name="support_assistant", model=model, instruction=ROOT_INSTRUCTION,
                     tools=[lookup_order, propose_refund, issue_refund])
    return InMemoryRunner(agent=agent, app_name="refund-tests"), model


async def converse(runner, user_id, messages):
    session = await runner.session_service.create_session(app_name="refund-tests", user_id=user_id)
    for message in messages:
        async for _ in runner.run_async(user_id=user_id, session_id=session.id, new_message=user(message)):
            pass


class RefundRunnerTests(unittest.TestCase):
    def test_eligible_refund_is_paid_once(self):
        store, pay, _ = configure_fakes()
        runner, model = build([
            call("propose_refund", order_id="HO-10442", amount_cents=2500, reason="Jacket arrived torn"),
            text("I can refund 25.00 EUR on HO-10442. Shall I go ahead?"),
            call("issue_refund"),
            text("Done: 25.00 EUR is on its way back to you."),
        ])
        asyncio.run(converse(runner, "cust-ana", ["My jacket HO-10442 arrived torn, refund 25 please", "yes"]))
        self.assertEqual(len(store.refunds_for("HO-10442")), 1)
        self.assertEqual(len(pay.requests), 1)
        self.assertEqual(model.script, [])

    def test_refund_on_another_customers_order_is_denied(self):
        store, pay, _ = configure_fakes()
        runner, model = build([
            call("propose_refund", order_id="HO-20001", amount_cents=4200, reason="refund"),
            text("I can't find that order on your account."),
        ])
        asyncio.run(converse(runner, "cust-ana", ["Refund order HO-20001"]))
        self.assertEqual(store.refunds_for("HO-20001"), [])
        self.assertEqual(pay.requests, [])
        self.assertEqual(model.script, [])


if __name__ == "__main__":
    unittest.main()
