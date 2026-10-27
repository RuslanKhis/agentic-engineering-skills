"""Alignment gate before side-effecting tools.

LlamaFirewall's stock AlignmentCheck is not used: it sends the whole trace, tool results included, to a
remote OpenAI-compatible endpoint (Together AI by default). This gate hands an injected judge only the
user's own message and the proposed call, never a tool result. The judge itself is not wired here.
"""
from __future__ import annotations

import asyncio
import logging
from typing import Any, Awaitable, Callable

logger = logging.getLogger(__name__)

# async (user_goal, tool_name, args) -> True when the call serves the goal
AlignmentJudge = Callable[[str, str, dict], Awaitable[bool]]

GATED_TOOLS = {"send_email"}
REFUSED = {"status": "error", "error_message": "this action was not confirmed as matching the request"}

_judge: AlignmentJudge | None = None
_timeout_s = 20.0


def configure_judge(judge: AlignmentJudge | None, timeout_s: float = 20.0) -> None:
    """With no judge configured the gate does nothing (the allow-list and confirmation still apply)."""
    global _judge, _timeout_s
    _judge, _timeout_s = judge, timeout_s


def _user_goal(tool_context: Any) -> str:
    content = getattr(tool_context, "user_content", None)
    return " ".join(p.text for p in (getattr(content, "parts", None) or []) if getattr(p, "text", None))


async def alignment_gate(tool: Any, args: dict, tool_context: Any) -> dict | None:
    """before_tool_callback. A missing goal, a judge error or a timeout refuses the call."""
    if _judge is None or tool.name not in GATED_TOOLS:
        return None
    goal = _user_goal(tool_context)
    try:
        ok = bool(goal) and await asyncio.wait_for(_judge(goal, tool.name, dict(args)), _timeout_s)
    except Exception as exc:
        logger.warning("alignment_gate tool=%s outcome=unavailable error=%s", tool.name, type(exc).__name__)
        ok = False
    if not ok:
        logger.info("alignment_gate tool=%s outcome=refused", tool.name)
    return None if ok else dict(REFUSED)
