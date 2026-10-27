"""Each evaluation case through the Runner with its scripted model, graded against the reference end state.

Two runs per case: the case's own script, and a do-nothing control (a model that answers with
text at once). The control must fail every case that expects a filing.
"""
import asyncio
import json
from pathlib import Path
import unittest

try:
    from google.adk.agents import LlmAgent
    from google.adk.runners import InMemoryRunner
    from google.adk.tools import FunctionTool
except ModuleNotFoundError:  # google-adk not installed
    raise unittest.SkipTest("google-adk is not installed")

from expense_agent import tools
from tests.fixture_db import fresh_db
from tests.case_checks import MUTATING, call_key, grade, snapshot
from tests.scripted_model import ScriptedModel, script_from, user

CASES = json.loads((Path(__file__).resolve().parents[1] / "eval_cases" / "cases.json").read_text())["cases"]
DO_NOTHING = [{"text": "Nothing to do."}]


def fake_read_file(path: str) -> dict:
    """Stand-in for the filesystem MCP server's read_file in offline tests."""
    return {"content": f"Receipt {path}: total as filed"}


def run_case(case: dict, steps: list[dict]) -> list[str]:
    """Run the case's request with a model scripted to steps; return the grading failures."""
    conn = fresh_db()
    before = snapshot(conn)
    effective = []

    def record(tool, args, tool_context, tool_response):
        # Successful mutating calls only; an error status is not an effect.
        if tool.name in MUTATING and tool_response.get("status") == MUTATING[tool.name]:
            effective.append(call_key(tool.name, args))
        return None

    agent = LlmAgent(name="expense_agent", model=ScriptedModel(script=script_from(steps)),
                     instruction="File expenses.", after_tool_callback=record,
                     tools=[tools.get_policy_limit, tools.file_expense, tools.get_my_profile,
                            tools.update_profile, tools.list_my_expenses,
                            FunctionTool(fake_read_file, name="read_file")])
    app = f"exp-{case['id']}"
    runner = InMemoryRunner(agent=agent, app_name=app)

    async def go():
        s = await runner.session_service.create_session(app_name=app, user_id=case["user"])
        async for _ in runner.run_async(user_id=case["user"], session_id=s.id,
                                        new_message=user(case["request"])):
            pass
    asyncio.run(go())
    return grade(case, before, conn, effective, fresh_db)


class CaseTests(unittest.TestCase):
    def test_cases(self):
        for case in CASES:
            with self.subTest(case=case["id"]):
                self.assertEqual(run_case(case, case["script"]), [])

    def test_do_nothing_control_fails_every_filing_case(self):
        for case in CASES:
            with self.subTest(case=case["id"]):
                failures = run_case(case, DO_NOTHING)
                if case["expected"].get("filed") is None:
                    self.assertEqual(failures, [])
                else:
                    self.assertNotEqual(failures, [], "a run that does nothing passed this filing case")


if __name__ == "__main__":
    unittest.main()
