"""Tool-result screening and alignment gate. Nothing here imports google.adk or llamafirewall at import time.

Documents must not leave the project, so every scanner runs in-process or against an endpoint inside
the project. Anything other than an explicit ALLOW (block, human-in-the-loop, error, timeout,
missing scanner) withholds the result or the call.
"""
from __future__ import annotations

import asyncio
import logging
from typing import Any, Awaitable, Callable
from urllib.parse import urlparse

logger = logging.getLogger(__name__)

ALLOW = "allow"
BLOCKED_RESULT = {"status": "blocked", "message": "This tool result was withheld by a safety screen."}
BLOCKED_CALL = {"status": "error", "error_message": "This action was withheld by a safety screen."}
MAX_SCREENED_CHARS = 100_000
SCAN_TIMEOUT_S = 10.0

# An async scanner takes text and returns True only for an explicit allow.
Scanner = Callable[[str], Awaitable[bool]]
# A judge takes a trace (list of {"role", "content"}) and returns True only for an explicit allow.
Judge = Callable[[list[dict]], Awaitable[bool]]


def _strings(value: Any, depth: int = 0) -> list[str] | None:
    """All string leaves of a JSON-like value, or None if it is too deep or has an unknown type."""
    if depth > 8:
        return None
    if isinstance(value, str):
        return [value]
    if value is None or isinstance(value, (bool, int, float)):
        return []
    if isinstance(value, dict):
        out: list[str] = []
        for k, v in value.items():
            sub = _strings(v, depth + 1)
            if not isinstance(k, str) or sub is None:
                return None
            out += [k, *sub]
        return out
    if isinstance(value, (list, tuple)):
        out = []
        for v in value:
            sub = _strings(v, depth + 1)
            if sub is None:
                return None
            out += sub
        return out
    return None


async def _allowed(scanner: Scanner, text: str) -> bool:
    try:
        return await asyncio.wait_for(scanner(text), SCAN_TIMEOUT_S) is True
    except Exception as exc:  # fail closed; log the type only, never the content
        logger.warning("screen unavailable: %s", type(exc).__name__)
        return False


def tool_result_screen(scanners: list[Scanner]) -> Callable[..., Awaitable[dict | None]]:
    """Build an ADK after_tool_callback: replace a result any scanner does not allow.

    The returned dict replaces the tool response, so the model and the stored event only see it.
    """
    if not scanners:
        raise ValueError("at least one scanner is required; refusing to run unscreened")

    async def after_tool(tool: Any, args: dict, tool_context: Any, tool_response: Any) -> dict | None:
        texts = _strings(tool_response)
        if texts is None or sum(map(len, texts)) > MAX_SCREENED_CHARS:
            return dict(BLOCKED_RESULT)
        joined = "\n".join(texts)  # one string, so a payload split across fields is still seen whole
        for scanner in scanners:
            if not await _allowed(scanner, joined):
                return dict(BLOCKED_RESULT)
        return None

    return after_tool


# ---- LlamaFirewall adapters (the package must already be in the image; not installed here) ----

def llamafirewall_scanner(prompt_guard_weights_dir: str | None = None) -> Scanner:
    """Local scanner: LlamaFirewall REGEX, plus PROMPT_GUARD when weights are baked into the image.

    PROMPT_GUARD loads Meta's model from the Hugging Face cache. In production set HF_HUB_OFFLINE=1
    and ship the weights in the image; a missing model then raises and the screen fails closed.
    """
    from llamafirewall import LlamaFirewall, Role, ScanDecision, ScannerType, ToolMessage

    kinds = [ScannerType.REGEX]
    if prompt_guard_weights_dir:
        kinds.append(ScannerType.PROMPT_GUARD)
    firewall = LlamaFirewall(scanners={Role.TOOL: kinds})

    async def scan(text: str) -> bool:
        result = await asyncio.to_thread(firewall.scan, ToolMessage(content=text))
        return result.decision == ScanDecision.ALLOW

    return scan


def alignment_gate(judge: Judge, guarded_tools: frozenset[str] = frozenset({"send_email"})):
    """Build an ADK before_tool_callback that asks `judge` whether a side-effecting call fits the user's goal.

    The trace is the first user message plus the session's function calls and responses and the
    proposed call. It contains documents, so `judge` must run inside the project.
    """

    async def before_tool(tool: Any, args: dict, tool_context: Any) -> dict | None:
        if tool.name not in guarded_tools:
            return None
        try:
            trace = _trace(tool_context, tool.name, args)
        except Exception as exc:
            logger.warning("alignment trace unavailable: %s", type(exc).__name__)
            return dict(BLOCKED_CALL)
        try:
            allowed = await asyncio.wait_for(judge(trace), SCAN_TIMEOUT_S) is True
        except Exception as exc:
            logger.warning("alignment judge unavailable: %s", type(exc).__name__)
            allowed = False
        return None if allowed else dict(BLOCKED_CALL)

    return before_tool


def _trace(tool_context: Any, name: str, args: dict) -> list[dict]:
    trace: list[dict] = []
    for event in tool_context.session.events:
        parts = (event.content.parts or []) if event.content else []
        for part in parts:
            if part.text and event.author == "user":
                trace.append({"role": "user", "content": part.text})
            elif part.function_call:
                trace.append({"role": "assistant", "content": f"{part.function_call.name}({part.function_call.args})"})
            elif part.function_response:
                trace.append({"role": "tool", "content": str(part.function_response.response)})
    if not any(m["role"] == "user" for m in trace):
        raise ValueError("no user message in trace")  # AlignmentCheck would ALLOW this; we do not
    trace.append({"role": "assistant", "content": f"{name}({args})"})
    return trace


ALIGNMENT_HOST_SUFFIXES = ("-aiplatform.googleapis.com",)  # regional Vertex AI, inside the project


def llamafirewall_alignment_judge(api_base_url: str, model_name: str, api_key_env_var: str) -> Judge:
    """Endpoint guard for an AlignmentCheck judge. NOT WIRED: always raises after validating the endpoint.

    The stock AlignmentCheckScanner sends the whole trace, documents included, to Together AI. The
    only acceptable variant is a CustomCheckScanner subclass (model_name, api_base_url,
    api_key_env_var, temperature) aimed at a regional Vertex AI host in this project. It needs the
    package installed to write and test, so it is left undone rather than guessed. Until then
    `alignment_gate` takes any in-project judge callable.
    """
    parsed = urlparse(api_base_url)
    if parsed.scheme != "https" or not (parsed.hostname or "").endswith(ALIGNMENT_HOST_SUFFIXES):
        raise ValueError("alignment endpoint must be an https regional Vertex AI host in this project")
    raise NotImplementedError("in-project AlignmentCheck subclass is not wired")


__all__ = ["tool_result_screen", "alignment_gate", "llamafirewall_scanner", "llamafirewall_alignment_judge"]
