"""Contract assistant agent."""
from __future__ import annotations

from google.adk.agents import LlmAgent
from google.adk.tools import FunctionTool

from contracts.alignment import alignment_gate
from contracts.policy import tool_policy
from contracts.screen import screen_tool_result
from contracts.tools.contract_tools import fetch_url, read_contract, send_email

INSTRUCTION = """\
You help Rowan Legal paralegals review supplier contracts. Read the contract with read_contract,
check the supplier's published terms with fetch_url when asked, and summarise differences.
Send a summary with send_email only when the paralegal asks.
"""


def build_agent() -> LlmAgent:
    return LlmAgent(
        name="contract_assistant",
        model="gemini-3.5-flash",
        instruction=INSTRUCTION,
        tools=[fetch_url, read_contract, FunctionTool(send_email, require_confirmation=True)],
        before_tool_callback=[tool_policy, alignment_gate],
        after_tool_callback=screen_tool_result,
    )


root_agent = build_agent()
