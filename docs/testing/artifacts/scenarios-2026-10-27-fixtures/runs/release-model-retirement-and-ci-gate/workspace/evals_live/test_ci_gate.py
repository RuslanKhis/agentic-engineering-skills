"""Tier 2 live eval gate. Calls the real model, so it is NOT part of `unittest discover -s tests`.

Run: RUN_LIVE_EVAL=1 EVAL_OUTPUT_CSV=results/ci.csv python -m unittest evals_live.test_ci_gate
AgentEvaluator writes the CSV and then asserts, so a failure still leaves the CSV for
scripts/check_eval_results.py. Unverified against ADK 2.8.0 in this session (no install, no network).
"""
import os
import unittest

EVAL_SET = os.environ.get("EVAL_SET", "eval/support.evalset.json")
NUM_RUNS = int(os.environ.get("EVAL_NUM_RUNS", "3"))
MAX_CASES = int(os.environ.get("EVAL_MAX_CASES", "40"))
MAX_RUNS = int(os.environ.get("EVAL_MAX_RUNS", "3"))
CASES = 40  # keep equal to eval/ci-expectations.json; the checker fails on any mismatch


@unittest.skipUnless(os.environ.get("RUN_LIVE_EVAL") == "1", "NOT RUN: RUN_LIVE_EVAL is not 1")
class LiveGate(unittest.IsolatedAsyncioTestCase):
    async def test_support_evalset(self):
        # Cost ceiling: fail (not skip) so an oversized cohort is never read as a pass.
        self.assertLessEqual(CASES, MAX_CASES, "NOT RUN: case count above EVAL_MAX_CASES")
        self.assertLessEqual(NUM_RUNS, MAX_RUNS, "NOT RUN: runs above EVAL_MAX_RUNS")
        from google.adk.evaluation.agent_evaluator import AgentEvaluator

        await AgentEvaluator.evaluate(
            agent_module="app",
            eval_dataset_file_path_or_dir=EVAL_SET,
            num_runs=NUM_RUNS,
            output_file=os.environ["EVAL_OUTPUT_CSV"],
        )


if __name__ == "__main__":
    unittest.main()
