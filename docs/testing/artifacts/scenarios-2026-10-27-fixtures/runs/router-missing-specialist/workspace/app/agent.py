"""Builds the ADK agent. This is the only module (with server.py) that imports google.adk."""
from __future__ import annotations

import os

from google.adk.agents import LlmAgent

from app import services
from app.clients.http import HttpxTransport
from app.clients.mail import MailClient
from app.clients.payments import PaymentsClient
from app.helpdesk import HelpIndex
from app.prompts import instruction_for
from app.settings import Settings
from app.store import Store
from app.tools.help import search_help
from app.tools.mail import fetch_email, send_email
from app.tools.orders import list_my_orders, lookup_order
from app.tools.preferences import set_language_preference
from app.tools.refunds import issue_refund


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
    return LlmAgent(
        name="support_assistant",
        model=settings.model_id,
        description="Answers Harbour Outfitters customers' order, delivery and refund questions.",
        instruction=lambda ctx: instruction_for(ctx.user_id),
        tools=[lookup_order, list_my_orders, search_help, issue_refund, fetch_email, send_email,
               set_language_preference],
    )


root_agent = build_agent()
