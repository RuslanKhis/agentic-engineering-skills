"""Builds the ADK app. This is the only module (with server.py) that imports google.adk."""
from __future__ import annotations

import os

from google.adk.agents import LlmAgent
from google.adk.apps import App

from app import services
from app.clients.http import HttpxTransport
from app.clients.mail import MailClient
from app.clients.payments import PaymentsClient
from app.helpdesk import HelpIndex
from app.plugins.screening import ModelArmorInputPlugin
from app.prompts import ROOT_INSTRUCTION
from app.settings import Settings
from app.store import Store
from app.tools.customers import get_customer_profile
from app.tools.docs import search_docs
from app.tools.mail import fetch_email, send_email
from app.tools.orders import list_my_orders, lookup_order
from app.tools.refunds import issue_refund
from app.tools.tickets import add_ticket_note


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
        instruction=ROOT_INSTRUCTION,
        tools=[fetch_email, search_docs, lookup_order, list_my_orders, get_customer_profile,
               issue_refund, send_email, add_ticket_note],
    )


root_agent = build_agent()

app = App(
    name="support",
    root_agent=root_agent,
    plugins=[ModelArmorInputPlugin(template=os.environ.get(
        "MODEL_ARMOR_TEMPLATE", "projects/harbour-support/locations/europe-west4/templates/support-input"))],
)
