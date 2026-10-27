"""Contract assistant agent."""
from __future__ import annotations

from google.adk.agents import LlmAgent
from google.adk.tools import FunctionTool

from contracts.policy import tool_policy
from contracts.screening import alignment_gate, llamafirewall_scanner, tool_result_screen
from contracts.tools.contract_tools import fetch_url, read_contract, send_email

INSTRUCTION = """\
You help Rowan Legal paralegals review supplier contracts. Read the contract with read_contract,
check the supplier's published terms with fetch_url when asked, and summarise differences.
Send a summary with send_email only when the paralegal asks.
"""


def build_agent(scanners=None, judge=None) -> LlmAgent:
    """scanners screen every tool result (default: local LlamaFirewall; startup fails if it is missing).

    judge, when given, must run inside the project; it gates send_email on goal alignment.
    """
    if scanners is None:
        scanners = [llamafirewall_scanner()]
    before = [tool_policy] + ([alignment_gate(judge)] if judge is not None else [])
    return LlmAgent(
        name="contract_assistant",
        model="gemini-3.5-flash",
        instruction=INSTRUCTION,
        tools=[fetch_url, read_contract, FunctionTool(send_email, require_confirmation=True)],
        before_tool_callback=before,
        after_tool_callback=tool_result_screen(scanners),
    )


root_agent = build_agent()
