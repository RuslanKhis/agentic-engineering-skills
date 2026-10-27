"""Builds the ADK support agent. This is the only module (with server.py) that imports google.adk."""
from __future__ import annotations

import os

from google.adk.agents import LlmAgent
from google.adk.tools import FunctionTool

from app import services
from app.clients.http import HttpxTransport
from app.clients.mail import MailClient
from app.clients.payments import PaymentsClient
from app.helpdesk import HelpIndex
from app.prompts import ROOT_INSTRUCTION
from app.settings import Settings
from app.store import Store
from app.tools.mail import send_email
from app.tools.refunds import issue_refund
from app.tools.tickets import read_ticket


def build_agent(settings: Settings | None = None, configure_services: bool = True) -> LlmAgent:
    settings = settings or Settings.from_env()
    if configure_services:
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
        description="Works Harbour Outfitters support tickets: refunds and replies.",
        instruction=ROOT_INSTRUCTION,
        tools=[read_ticket, FunctionTool(issue_refund, require_confirmation=True), send_email],
    )


root_agent = build_agent()
