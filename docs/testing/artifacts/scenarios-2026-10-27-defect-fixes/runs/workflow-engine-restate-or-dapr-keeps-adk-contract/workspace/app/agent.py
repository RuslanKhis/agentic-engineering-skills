"""The refund flow as an ADK App: intake, then refund, with a manager's approval on the refund."""
from __future__ import annotations

import os

from google.adk.agents import LlmAgent, RunConfig, SequentialAgent
from google.adk.apps import App, ResumabilityConfig

from app import budget, services
from app.clients.http import HttpxTransport
from app.clients.mail import MailClient
from app.clients.payments import PaymentsClient
from app.helpdesk import HelpIndex
from app.prompts import INTAKE_INSTRUCTION, REFUND_INSTRUCTION
from app.settings import Settings
from app.store import Store
from app.tools.orders import list_my_orders, lookup_order
from app.tools.refunds import request_refund

RUN_CONFIG = RunConfig(max_llm_calls=8)


def build_app(settings: Settings | None = None) -> App:
    settings = settings or Settings.from_env()
    transport = HttpxTransport()
    services.configure(services.Services(
        store=Store(settings.db_path),
        payments=PaymentsClient(settings.payments_base_url, transport, os.environ.get("PAYMENTS_API_KEY", "")),
        mail=MailClient(settings.mail_base_url, transport),
        help_index=HelpIndex(),
        max_refund_cents=settings.max_refund_cents,
        approval_ttl_days=settings.approval_ttl_days,
    ))
    intake = LlmAgent(
        name="intake", model=settings.model_id, instruction=INTAKE_INSTRUCTION,
        tools=[lookup_order, list_my_orders], output_key="intake",
        before_model_callback=budget.before_model, after_model_callback=budget.after_model)
    refund = LlmAgent(
        name="refund", model=settings.model_id, instruction=REFUND_INSTRUCTION,
        tools=[lookup_order, request_refund],
        before_model_callback=budget.before_model, after_model_callback=budget.after_model)
    root = SequentialAgent(name="refund_flow", sub_agents=[intake, refund])
    return App(name="refunds", root_agent=root, resumability_config=ResumabilityConfig(is_resumable=True))


app = build_app()
