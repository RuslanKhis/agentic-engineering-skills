"""Workspace assistant agent."""
from __future__ import annotations

from google.adk.agents import LlmAgent
from google.adk.tools import FunctionTool

from app.policy import gate
from app.tools import workspace as ws

INSTRUCTION = """\
You help Larch & Pine finance and operations staff with their mail, calendar and Drive files, and
pay supplier invoices. Use the tools; ask before doing anything the user did not ask for.
"""


def build_agent() -> LlmAgent:
    return LlmAgent(
        name="workspace_assistant",
        model="gemini-3.5-flash",
        instruction=INSTRUCTION,
        tools=[ws.search_mail, ws.read_mail, ws.send_mail, ws.delete_mail, ws.list_events, ws.create_event,
               ws.search_files, ws.read_file, ws.share_file,
               FunctionTool(ws.pay_invoice, require_confirmation=True)],
        before_tool_callback=gate,
    )


root_agent = build_agent()
