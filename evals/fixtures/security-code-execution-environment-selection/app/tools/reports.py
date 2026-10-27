"""Email an analysis report."""
from __future__ import annotations

import os
import smtplib
from email.message import EmailMessage

SMTP_HOST = os.environ.get("SMTP_HOST", "smtp-relay.example.invalid")


def email_report(to: str, subject: str, body: str) -> dict:
    """Email the analysis findings.

    Args:
        to: Recipient address.
        subject: Subject line.
        body: Plain-text findings.

    Returns:
        {"status": "sent"}.
    """
    msg = EmailMessage()
    msg["From"] = "upload-analyst@fjord.example"
    msg["To"] = to
    msg["Subject"] = subject
    msg.set_content(body)
    with smtplib.SMTP(SMTP_HOST, 587, timeout=10) as smtp:
        smtp.starttls()
        smtp.send_message(msg)
    return {"status": "sent"}
