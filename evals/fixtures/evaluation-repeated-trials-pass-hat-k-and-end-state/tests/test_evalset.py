"""Runs the evalset through ADK's AgentEvaluator. Needs google-adk and model access."""
import os
import unittest

try:
    from google.adk.evaluation.agent_evaluator import AgentEvaluator
except ModuleNotFoundError:  # google-adk not installed
    raise unittest.SkipTest("google-adk is not installed")


@unittest.skipUnless(os.environ.get("GOOGLE_CLOUD_PROJECT"), "no model access")
class EvalsetTests(unittest.IsolatedAsyncioTestCase):
    async def test_booking_evalset(self):
        await AgentEvaluator.evaluate("booking_agent", "eval_cases/booking.evalset.json", num_runs=1)


if __name__ == "__main__":
    unittest.main()
