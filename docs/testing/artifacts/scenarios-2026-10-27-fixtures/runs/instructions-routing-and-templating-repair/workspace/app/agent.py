"""Builds the coordinator and its sub-agents. Only this module (and server.py) imports google.adk."""
from __future__ import annotations

import os

from google.adk.agents import LlmAgent

from app import services
from app.clients.http import HttpxTransport
from app.clients.mail import MailClient
from app.clients.payments import PaymentsClient
from app.helpdesk import HelpIndex
from app.prompts import (BILLING_DESCRIPTION, BILLING_INSTRUCTION, COORDINATOR_INSTRUCTION,
                         ORDERS_DESCRIPTION, ORDERS_INSTRUCTION, REFUNDS_DESCRIPTION,
                         REFUNDS_INSTRUCTION)
from app.settings import Settings
from app.store import Store
from app.tools.billing import get_invoice
from app.tools.help import search_help
from app.tools.orders import list_my_orders, lookup_order
from app.tools.profile import load_profile
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
    billing_agent = LlmAgent(name="billing_agent", model=settings.model_id, description=BILLING_DESCRIPTION,
                             instruction=BILLING_INSTRUCTION, tools=[get_invoice])
    refunds_agent = LlmAgent(name="refunds_agent", model=settings.model_id, description=REFUNDS_DESCRIPTION,
                             instruction=REFUNDS_INSTRUCTION, tools=[lookup_order, search_help, issue_refund])
    orders_agent = LlmAgent(name="orders_agent", model=settings.model_id, description=ORDERS_DESCRIPTION,
                            instruction=ORDERS_INSTRUCTION, tools=[lookup_order, list_my_orders])
    return LlmAgent(
        name="support_coordinator",
        model=settings.model_id,
        description="Front desk for Harbour Outfitters customer support.",
        instruction=COORDINATOR_INSTRUCTION,
        tools=[load_profile],
        sub_agents=[billing_agent, refunds_agent, orders_agent],
    )


root_agent = build_agent()
