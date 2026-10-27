"""Builds the ADK agent; warranty questions go to the partner's agent over A2A."""
from __future__ import annotations

import os

from google.adk.agents import LlmAgent
from google.adk.agents.remote_a2a_agent import RemoteA2aAgent

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
    warranty = RemoteA2aAgent(
        name="warranty_partner",
        description="The bike maker's warranty agent: coverage and repair options for a serial number.",
        agent_card="https://partner.example/.well-known/agent-card.json",
    )
    return LlmAgent(
        name="support_assistant",
        model=settings.model_id,
        instruction=ROOT_INSTRUCTION + "\nTransfer warranty questions to warranty_partner.",
        tools=[lookup_order, list_my_orders, search_help],
        sub_agents=[warranty],
    )


root_agent = build_agent()
