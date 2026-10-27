"""Builds the production support agent."""
from __future__ import annotations

import os

from google.adk.agents import LlmAgent
from google.adk.tools import FunctionTool
from google.adk.tools.mcp_tool.mcp_toolset import McpToolset, StreamableHTTPConnectionParams

from app import services
from app.callbacks import capability_check
from app.clients.http import HttpxTransport
from app.clients.mail import MailClient
from app.clients.payments import PaymentsClient
from app.helpdesk import HelpIndex
from app.prompts import ROOT_INSTRUCTION
from app.reporting import reporting_agent
from app.settings import Settings
from app.store import Store
from app.tools.help import search_help
from app.tools.mail import fetch_email, send_email
from app.tools.orders import list_my_orders, lookup_order
from app.tools.refunds import issue_refund as refund_order


def build_agent(settings: Settings | None = None) -> LlmAgent:
    settings = settings or Settings.from_env()
    transport = HttpxTransport()
    services.configure(services.Services(
        store=Store(settings.db_path),
        payments=PaymentsClient(settings.payments_base_url, transport, os.environ.get("PAYMENTS_API_KEY", "")),
        mail=MailClient(settings.mail_base_url, transport),
        help_index=HelpIndex(),
        max_refund_cents=settings.max_refund_cents,
    ))
    catalogue = McpToolset(
        connection_params=StreamableHTTPConnectionParams(url="https://catalogue-mcp.internal.example/mcp"),
        tool_filter=["get_product", "check_stock"],
    )
    returns_agent = LlmAgent(
        name="returns_agent",
        model=settings.model_id,
        description="Explains the returns policy and books return labels.",
        instruction="Explain the returns policy from search_help. Do not issue refunds.",
        tools=[search_help],
    )
    mail_agent = LlmAgent(
        name="mail_agent",
        model=settings.model_id,
        description="Reads inbound support emails that staff paste by message ID.",
        instruction="Read the email with fetch_email and summarise what the customer wants.",
        tools=[fetch_email],
    )
    return LlmAgent(
        name="support_assistant",
        model=settings.model_id,
        description="Answers Harbour Outfitters customers' order, delivery and refund questions.",
        instruction=ROOT_INSTRUCTION,
        tools=[lookup_order, list_my_orders, search_help, FunctionTool(refund_order, require_confirmation=True),
               send_email, catalogue],
        sub_agents=[returns_agent, mail_agent, reporting_agent],
        before_tool_callback=capability_check,
    )


root_agent = build_agent()
