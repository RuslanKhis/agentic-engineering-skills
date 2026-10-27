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


def build_agent(settings: Settings | None = None, warranty_card=None) -> LlmAgent:
    """`warranty_card` is a signature-verified AgentCard; without one there is no warranty agent."""
    settings = settings or Settings.from_env()
    transport = HttpxTransport()
    services.configure(services.Services(
        store=Store(settings.db_path),
        payments=PaymentsClient(settings.payments_base_url, transport, os.environ.get("PAYMENTS_API_KEY", "")),
        mail=MailClient(settings.mail_base_url, transport),
        help_index=HelpIndex(),
        max_refund_cents=settings.max_refund_cents,
    ))
    instruction = ROOT_INSTRUCTION
    sub_agents = []
    if warranty_card is not None:
        sub_agents.append(RemoteA2aAgent(
            name="warranty_partner",
            description="The bike maker's warranty agent: coverage and repair options for a serial number.",
            agent_card=warranty_card,
        ))
        instruction += "\nTransfer warranty questions to warranty_partner."
    else:
        instruction += "\nWarranty lookups are unavailable; tell the customer a human will follow up."
    return LlmAgent(
        name="support_assistant",
        model=settings.model_id,
        instruction=instruction,
        tools=[lookup_order, list_my_orders, search_help],
        sub_agents=sub_agents,
    )


async def build_verified_agent(settings: Settings | None = None) -> LlmAgent:
    """Fetch the partner card, verify its signature, and build the agent.

    A refused card yields an agent without the warranty sub-agent (fail closed).
    """
    import logging
    import httpx
    from app.card_trust import CardRefused, PinnedKeyProvider, fetch_verified_card

    settings = settings or Settings.from_env()
    try:
        provider = PinnedKeyProvider.from_file(settings.partner_jwks_path, settings.partner_card_kids)
        async with httpx.AsyncClient(timeout=10.0, follow_redirects=False) as client:
            card = await fetch_verified_card(settings.partner_card_url, provider, client)
    except CardRefused as exc:
        logging.getLogger(__name__).error("warranty partner disabled: %s", exc)
        card = None
    return build_agent(settings, warranty_card=card)
