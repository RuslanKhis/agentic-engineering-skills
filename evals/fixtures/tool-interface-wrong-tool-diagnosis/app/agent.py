"""Builds the ADK agent. This is the only module (with server.py) that imports google.adk."""
from __future__ import annotations

import os

from google.adk.agents import LlmAgent

from app import services
from app.clients.http import HttpxTransport
from app.clients.mail import MailClient
from app.clients.payments import PaymentsClient
from app.helpdesk import HelpIndex
from app.prompts import ROOT_INSTRUCTION
from app.settings import Settings
from app.store import Store
from app.tools.delivery import change_delivery_address, track_parcel
from app.tools.help import search_help
from app.tools.mail import fetch_email, send_email
from app.tools.orders import get_order, list_my_orders, search_orders
from app.tools.refunds import issue_refund
from app.tools.returns import return_status, start_return
from app.tools.vouchers import apply_voucher

TOOLS = [
    search_orders, get_order, list_my_orders, track_parcel, change_delivery_address,
    start_return, return_status, issue_refund, apply_voucher, search_help, fetch_email, send_email,
]


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
        tools=TOOLS,
    )


root_agent = build_agent()
