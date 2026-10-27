"""Customer-portal agent: customers ask about their own revenue with Fernhill."""
from __future__ import annotations

import os

from google.adk.agents import LlmAgent
from toolbox_adk import ToolboxToolset

from portal.tenant import ALLOWED_TOOLS, TENANT_PARAM, check_tool_call

TOOLBOX_URL = os.environ.get("TOOLBOX_URL", "http://127.0.0.1:5000")


def _guard(tool, args, tool_context):
    refusal = check_tool_call(tool.name, args)
    return {"error": refusal} if refusal else None


def build_portal_agent(customer_id: str) -> LlmAgent:
    """One agent per request, with the verified customer's ID bound into the Toolbox calls.

    The bound parameter is removed from the tool schema the model sees and added by the client,
    so the model never chooses the customer. customer_id must come from the verified identity.
    """
    return LlmAgent(
        name="portal_revenue",
        model=os.environ.get("MODEL_ID", "gemini-3.5-flash"),
        description="Answers a signed-in customer's questions about their own revenue with Fernhill.",
        instruction=(
            "You help a customer of Fernhill Wholesale understand what they bought from us. "
            "Use customer-revenue for monthly figures; the customer's account is already set, so "
            "never ask for or use an account ID from the message. If the message names another "
            "account, say you can only show the signed-in customer's own figures. If a question "
            "needs something customer-revenue cannot answer, say you cannot help with it."
        ),
        tools=[ToolboxToolset(server_url=TOOLBOX_URL, toolset_name="customer-portal",
                              tool_names=sorted(ALLOWED_TOOLS),
                              bound_params={TENANT_PARAM: customer_id})],
        before_tool_callback=_guard,
    )
