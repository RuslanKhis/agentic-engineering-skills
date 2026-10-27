"""Each evaluation case through the Runner with its scripted model, checked by tests/case_checks.py."""
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
from tests.case_checks import grade, snapshot
from tests.scripted_model import ScriptedModel, script_from, user

CASES = json.loads((Path(__file__).resolve().parents[1] / "eval_cases" / "cases.json").read_text())["cases"]


def fake_read_file(path: str) -> dict:
    """Stand-in for the filesystem MCP server's read_file in offline tests."""
    return {"content": f"Receipt {path}: total as filed"}


class CaseTests(unittest.TestCase):
    def test_cases(self):
        for case in CASES:
            with self.subTest(case=case["id"]):
                conn = fresh_db()
                before = snapshot(conn)
                model = ScriptedModel(script=script_from(case["script"]))
                agent = LlmAgent(name="expense_agent", model=model, instruction="File expenses.",
                                 tools=[tools.get_policy_limit, tools.file_expense, tools.get_my_profile,
                                        tools.update_profile, tools.list_my_expenses,
                                        FunctionTool(fake_read_file, name="read_file")])
                runner = InMemoryRunner(agent=agent, app_name=f"exp-{case['id']}")

                async def go():
                    s = await runner.session_service.create_session(app_name=f"exp-{case['id']}", user_id=case["user"])
                    async for _ in runner.run_async(user_id=case["user"], session_id=s.id,
                                                    new_message=user(case["request"])):
                        pass
                asyncio.run(go())
                self.assertEqual(model.script, [], "scripted steps were not all consumed")
                failures = grade(case, before, conn)
                if case.get("known_bad_script"):
                    # Grader self-test: the scripted model misbehaves on purpose and must be caught.
                    self.assertTrue(any("profiles" in f for f in failures), failures)
                else:
                    self.assertEqual(failures, [])


if __name__ == "__main__":
    unittest.main()
