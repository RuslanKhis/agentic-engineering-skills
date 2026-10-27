"""Builds the process-wide services from settings. Shared by the web service and the review worker."""
from __future__ import annotations

import os

from app import services
from app.clients.http import HttpxTransport
from app.clients.mail import MailClient
from app.clients.payments import PaymentsClient
from app.clients.restate import RestateReviews, UnconfiguredReviews
from app.helpdesk import HelpIndex
from app.settings import Settings
from app.store import Store


def configure_services(settings: Settings) -> None:
    transport = HttpxTransport()
    reviews = (RestateReviews(settings.restate_ingress_url, transport)
               if settings.restate_ingress_url else UnconfiguredReviews())
    services.configure(services.Services(
        store=Store(settings.db_path),
        payments=PaymentsClient(settings.payments_base_url, transport, os.environ.get("PAYMENTS_API_KEY", "")),
        mail=MailClient(settings.mail_base_url, transport),
        help_index=HelpIndex(),
        max_refund_cents=settings.max_refund_cents,
        reviews=reviews,
        manager_emails=settings.manager_emails,
        approval_days=settings.approval_days,
    ))
