"""The signed-in customer's saved reply language."""
from __future__ import annotations

import re

from app import services

# A BCP 47 style tag such as "en", "fr" or "pt-BR". The value is placed in the instruction,
# so anything else is rejected rather than passed on.
_LANGUAGE_TAG = re.compile(r"^[A-Za-z]{2,3}(-[A-Za-z0-9]{2,8}){0,2}$")


def valid_language(tag: str) -> bool:
    return bool(_LANGUAGE_TAG.fullmatch(tag))


def set_language_preference(language: str, tool_context) -> dict:
    """Save the language the signed-in customer wants replies in, for this and future chats.

    Use when the customer asks to be answered in a language, e.g. "reply in French from now on".
    Do not use it for a one-off translation of a single message.

    Args:
        language: A language tag such as "en", "fr", "de" or "pt-BR".

    Returns:
        {"status": "saved", "language": ...} or {"status": "error", "message": ...}.
    """
    tag = language.strip()
    if not valid_language(tag):
        return {"status": "error", "message": f"{language!r} is not a language tag like 'en' or 'pt-BR'."}
    services.get().store.set_language(tool_context.user_id, tag)
    return {"status": "saved", "language": tag}
