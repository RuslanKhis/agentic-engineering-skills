"""Checks the tool bodies run themselves. The model cannot reach them. No google.adk imports.

Session state keys are written by the server (principal_email) or by the tools (the rest), never
taken from tool arguments.
"""
from __future__ import annotations

import re
from email.utils import getaddresses

PRINCIPAL_EMAIL = "principal_email"
UNTRUSTED_SEEN = "untrusted_seen"
FETCHED_IDS = "fetched_message_ids"
REFUNDS_THIS_SESSION = "refunds_this_session"

MAX_REFUNDS_PER_SESSION = 3
MAX_EMAIL_BODY_CHARS = 4_000
MAX_DOC_BODY_CHARS = 1_500
MAX_NOTE_CHARS = 500

_MESSAGE_ID = re.compile(r"^[A-Za-z0-9_-]{1,64}$")


def valid_message_id(message_id: str) -> bool:
    """Message IDs go into a URL path; anything but a plain token could reach another endpoint."""
    return bool(_MESSAGE_ID.fullmatch(message_id or ""))


def single_address(value: str) -> str | None:
    """The lower-cased address if `value` holds exactly one and no header-breaking characters."""
    if not value or any(c in value for c in "\r\n"):
        return None
    found = [addr for _, addr in getaddresses([value]) if addr]
    if len(found) != 1 or "@" not in found[0]:
        return None
    return found[0].strip().lower()


def principal_email(state) -> str | None:
    return single_address(state.get(PRINCIPAL_EMAIL, ""))


def mark_untrusted(state) -> None:
    state[UNTRUSTED_SEEN] = True
