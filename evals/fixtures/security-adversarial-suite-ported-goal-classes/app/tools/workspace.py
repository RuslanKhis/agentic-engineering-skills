"""Mail, calendar, Drive and payment tools."""
from __future__ import annotations

from app import backends


def search_mail(query: str) -> dict:
    """Search the user's mailbox. Returns {"status": "ok", "messages": [{id, from, subject}]}."""
    return {"status": "ok", "messages": backends.get().mail.search(query)}


def read_mail(message_id: str) -> dict:
    """Read one message. Returns {"status": "ok", "from", "subject", "body"}."""
    return {"status": "ok", **backends.get().mail.read(message_id)}


def send_mail(to: str, subject: str, body: str) -> dict:
    """Send an email from the user's mailbox. Returns {"status": "sent", "id"}."""
    return {"status": "sent", "id": backends.get().mail.send(to, subject, body)}


def delete_mail(message_id: str) -> dict:
    """Move a message to the bin. Returns {"status": "deleted"}."""
    backends.get().mail.delete(message_id)
    return {"status": "deleted"}


def list_events(day: str) -> dict:
    """List calendar events on a day (YYYY-MM-DD). Returns {"status": "ok", "events": [...]}."""
    return {"status": "ok", "events": backends.get().calendar.list_events(day)}


def create_event(title: str, start: str, attendees: list[str]) -> dict:
    """Create a calendar event and invite attendees. Returns {"status": "created", "id"}."""
    return {"status": "created", "id": backends.get().calendar.create_event(title, start, attendees)}


def search_files(query: str) -> dict:
    """Search Drive. Returns {"status": "ok", "files": [{id, name}]}."""
    return {"status": "ok", "files": backends.get().drive.search(query)}


def read_file(file_id: str) -> dict:
    """Read a Drive file's text. Returns {"status": "ok", "text"}."""
    return {"status": "ok", "text": backends.get().drive.read(file_id)}


def share_file(file_id: str, email: str) -> dict:
    """Share a Drive file with someone. Returns {"status": "shared"}."""
    backends.get().drive.share(file_id, email)
    return {"status": "shared"}


def pay_invoice(payee_id: str, amount_cents: int, reference: str) -> dict:
    """Pay a supplier from the operating account.

    Args:
        payee_id: A payee already set up in the bank, e.g. "pay-0042".
        amount_cents: Amount in cents.
        reference: The invoice number.
    """
    return {"status": "paid", "payment_id": backends.get().bank.pay(payee_id, amount_cents, reference)}
