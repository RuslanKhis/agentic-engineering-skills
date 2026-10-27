"""Keep prompt, tool and response content out of the BigQuery analytics plugin. Standard library only."""
from __future__ import annotations

from typing import Any

# Events whose payload is essentially user or tool content. Timings, token counts and
# errors remain on the events that are kept (LLM_RESPONSE, *_COMPLETED, *_ERROR, ...).
CONTENT_EVENTS = ["USER_MESSAGE_RECEIVED", "LLM_REQUEST", "TOOL_STARTING"]

REDACTED = "[content not logged]"


def drop_content(content: Any, event_type: str = "") -> str:
    """content_formatter for BigQueryLoggerConfig: never keep the content body."""
    return REDACTED
