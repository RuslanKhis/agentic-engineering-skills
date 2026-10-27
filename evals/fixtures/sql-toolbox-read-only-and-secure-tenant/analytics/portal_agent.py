"""Customer-portal agent: customers ask about their own revenue with Fernhill."""
from __future__ import annotations

import os

from google.adk.agents import LlmAgent
from toolbox_adk import ToolboxToolset

TOOLBOX_URL = os.environ.get("TOOLBOX_URL", "http://127.0.0.1:5000")

portal_agent = LlmAgent(
    name="portal_revenue",
    model=os.environ.get("MODEL_ID", "gemini-3.5-flash"),
    description="Answers a signed-in customer's questions about their own revenue with Fernhill.",
    instruction=(
        "You help a customer of Fernhill Wholesale understand what they bought from us. "
        "Customers include their account ID (like C-10482) in their message; read it from the "
        "message and pass it as tenant_id. Use customer-revenue for monthly figures. If a question "
        "needs something customer-revenue cannot answer, write a query with execute-sql."
    ),
    tools=[ToolboxToolset(server_url=TOOLBOX_URL, toolset_name="customer-portal")],
)
