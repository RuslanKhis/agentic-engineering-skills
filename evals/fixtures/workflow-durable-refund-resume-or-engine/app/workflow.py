"""Refund workflow: the agent proposes a refund, a manager approves it, the refund is paid.

The refund tool asks for confirmation, so the invocation pauses at the tool call. The paused
session is stored in Postgres (DatabaseSessionService) and the App is resumable; when the
manager answers in the back office, app/approvals.py resumes the same invocation.
"""
from __future__ import annotations

import os

from google.adk.agents import LlmAgent
from google.adk.apps import App, ResumabilityConfig
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
        name="refund_desk", model=settings.model_id, instruction=ROOT_INSTRUCTION,
        tools=[lookup_order, list_my_orders, search_help, FunctionTool(issue_refund, require_confirmation=True)])
    return App(name="refunds", root_agent=agent, resumability_config=ResumabilityConfig(is_resumable=True))


app = build_app()
