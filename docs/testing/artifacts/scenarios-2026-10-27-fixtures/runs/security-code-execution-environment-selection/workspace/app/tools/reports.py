"""Email an analysis report."""
from __future__ import annotations

import os
import smtplib
from email.message import EmailMessage
from email.utils import parseaddr

SMTP_HOST = os.environ.get("SMTP_HOST", "smtp-relay.example.invalid")
ALLOWED_DOMAINS = frozenset(
    d.strip().lower() for d in os.environ.get("REPORT_ALLOWED_DOMAINS", "fjord.example").split(",")
    if d.strip()
)


def _allowed(to: str) -> bool:
    name, addr = parseaddr(to)
    # One plain address only: no display-name tricks, lists or control characters.
    if not addr or addr != to.strip() or any(c in to for c in ",;\r\n"):
        return False
    return addr.count("@") == 1 and addr.rsplit("@", 1)[1].lower() in ALLOWED_DOMAINS


def email_report(to: str, subject: str, body: str) -> dict:
    """Email the analysis findings to a colleague at the company.

    Args:
        to: One recipient address at an approved company domain.
        subject: Subject line.
        body: Plain-text findings.

    Returns:
        {"status": "sent"} or {"status": "error", "message": ...}.
    """
    if not _allowed(to):
        return {"status": "error", "message": "recipient is not at an approved domain"}
    msg = EmailMessage()
    msg["From"] = "upload-analyst@fjord.example"
    msg["To"] = to
    msg["Subject"] = subject.replace("\r", " ").replace("\n", " ")
    msg.set_content(body)
    with smtplib.SMTP(SMTP_HOST, 587, timeout=10) as smtp:
        smtp.starttls()
        smtp.send_message(msg)
    return {"status": "sent"}
