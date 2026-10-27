"""Mail assistant agent."""
from __future__ import annotations

from google.adk.agents import LlmAgent

from mailagent.security.gate import capability_gate
from google.adk.tools import FunctionTool

from mailagent.security.taint import label_untrusted, record_user_values
from mailagent.tools.mail_tools import archive_thread, delete_file, search_mail, send_email

INSTRUCTION = """\
You help the user manage their mail and drive: find threads, answer and send emails, tidy up by
archiving threads and deleting files the user no longer needs.
"""


def build_agent() -> LlmAgent:
    return LlmAgent(
        name="mail_assistant",
        model="gemini-3.5-flash",
        instruction=INSTRUCTION,
        tools=[search_mail, send_email, delete_file,
               FunctionTool(archive_thread, require_confirmation=True)],
        before_agent_callback=record_user_values,
        before_tool_callback=capability_gate,
        after_tool_callback=label_untrusted,
    )


root_agent = build_agent()
