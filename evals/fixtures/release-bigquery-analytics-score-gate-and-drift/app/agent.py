"""Builds the ADK app; every event is written to BigQuery Agent Analytics."""
from __future__ import annotations

import os

from google.adk.agents import LlmAgent
from google.adk.apps import App
from google.adk.plugins.bigquery_agent_analytics_plugin import BigQueryAgentAnalyticsPlugin
from google.adk.tools import FunctionTool

from app import services
from app.clients.http import HttpxTransport
from app.clients.mail import MailClient
from app.clients.payments import PaymentsClient
from app.helpdesk import HelpIndex
from app.prompts import ROOT_INSTRUCTION
from app.settings import Settings
from app.store import Store
from app.tools.help import search_help
from app.tools.orders import list_my_orders, lookup_order
from app.tools.refunds import issue_refund


def build_app(settings: Settings | None = None) -> App:
    settings = settings or Settings.from_env()
    transport = HttpxTransport()
    services.configure(services.Services(
        store=Store(settings.db_path),
        payments=PaymentsClient(settings.payments_base_url, transport, os.environ.get("PAYMENTS_API_KEY", "")),
        mail=MailClient(settings.mail_base_url, transport),
        help_index=HelpIndex(),
        max_refund_cents=settings.max_refund_cents,
    ))
    agent = LlmAgent(
        name="support_assistant",
        model=settings.model_id,
        instruction=ROOT_INSTRUCTION,
        tools=[lookup_order, list_my_orders, search_help, FunctionTool(issue_refund, require_confirmation=True)],
    )
    analytics = BigQueryAgentAnalyticsPlugin(project_id=os.environ.get("GOOGLE_CLOUD_PROJECT", ""),
                                             dataset_id="support_analytics", table_id="agent_events")
    return App(name="support", root_agent=agent, plugins=[analytics])


app = build_app()
