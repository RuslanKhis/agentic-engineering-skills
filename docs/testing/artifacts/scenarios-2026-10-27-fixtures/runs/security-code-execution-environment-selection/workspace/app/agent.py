"""Upload analyst agent."""
from __future__ import annotations

from google.adk.agents import LlmAgent
from google.adk.code_executors import AgentEngineSandboxCodeExecutor
from google.adk.tools import FunctionTool

from app.sandbox import sandbox_resource_name
from app.tools.reports import email_report
from app.tools.uploads import download_upload

INSTRUCTION = """\
You help underwriters analyse files customers uploaded. Use download_upload to fetch the file the
underwriter names; it becomes available to your code under the file name the tool returns. Then write
and run Python (pandas is available) to answer the question. The code sandbox has no network access
and does not keep files between runs. When the underwriter asks, send the findings with email_report;
the underwriter confirms the recipient and text before it is sent.
"""

root_agent = LlmAgent(
    name="upload_analyst",
    model="gemini-3.5-flash",
    instruction=INSTRUCTION,
    tools=[download_upload, FunctionTool(email_report, require_confirmation=True)],
    code_executor=AgentEngineSandboxCodeExecutor(sandbox_resource_name=sandbox_resource_name()),
)
