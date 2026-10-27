"""Operations assistant agent."""
from __future__ import annotations

import os

from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool import McpToolset, StreamableHTTPConnectionParams

from app.tools.knowledge import search_corpus
from app.tools.workspace import read_drive_file, search_mail, send_mail, share_drive_file

deskline = McpToolset(
    connection_params=StreamableHTTPConnectionParams(
        url="https://mcp.deskline.example/mcp",
        headers={"Authorization": f"Bearer {os.environ.get('DESKLINE_TOKEN', '')}"},
    ),
)

root_agent = LlmAgent(
    name="ops_assistant",
    model="gemini-3.5-flash",
    instruction=("You help Tamsin Logistics operations staff. Look things up in the shared corpus first, "
                 "use mail and Drive for the staff member's own work, and open or update tickets in "
                 "Deskline. Keep going until the task is done."),
    tools=[search_corpus, search_mail, send_mail, read_drive_file, share_drive_file, deskline],
)
