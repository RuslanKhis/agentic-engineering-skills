"""Upload analyst agent."""
from __future__ import annotations

import os

from google.adk.agents import LlmAgent
from google.adk.code_executors import UnsafeLocalCodeExecutor
from google.adk.integrations.daytona import DaytonaEnvironment
from google.adk.tools.environment import EnvironmentToolset

from app.tools.reports import email_report
from app.tools.uploads import download_upload

INSTRUCTION = """\
You help underwriters analyse files customers uploaded. Use download_upload to fetch the file the
underwriter names, then write and run Python (pandas is available) to answer the question.
For longer analyses use the workspace tools to keep intermediate files. When the underwriter asks,
send the findings with email_report.
"""

workspace = EnvironmentToolset(
    environment=DaytonaEnvironment(api_key=os.environ.get("DAYTONA_API_KEY", ""),
                                   target="eu", image="python:3.12-slim"),
)

root_agent = LlmAgent(
    name="upload_analyst",
    model="gemini-3.5-flash",
    instruction=INSTRUCTION,
    tools=[download_upload, email_report, workspace],
    code_executor=UnsafeLocalCodeExecutor(),
)
