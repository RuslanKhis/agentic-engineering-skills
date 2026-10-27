"""Local screen for tool results: a prompt-injection classifier run in-process over bounded windows.

Nothing here leaves the project. The scanner is injected (see contracts/prompt_guard.py for the
LlamaFirewall Prompt Guard 2 adapter); an unknown verdict withholds the result.
"""
from __future__ import annotations

import asyncio
import inspect
import logging
from types import SimpleNamespace
from typing import Any, Callable

logger = logging.getLogger(__name__)

WITHHELD = {"status": "withheld", "message": "This tool result was withheld by the safety screen."}

# Prompt Guard 2 scores only the first 512 tokens: stay well under it and overlap the windows.
WINDOW_TOKENS = 384
OVERLAP_TOKENS = 128
MAX_CHARS = 200_000
MAX_DEPTH = 8


class ScreenUnavailable(Exception):
    """The result could not be screened (too large, too deep, scanner error): treated as unknown."""


def windows(text: str, tokenizer: Any, size: int = WINDOW_TOKENS, overlap: int = OVERLAP_TOKENS) -> list[str]:
    """Split text into overlapping windows of at most `size` tokens using the classifier's tokenizer."""
    ids = tokenizer.encode(text, add_special_tokens=False)
    step = size - overlap
    out = []
    for start in range(0, len(ids), step):
        out.append(tokenizer.decode(ids[start:start + size]))
        if start + size >= len(ids):
            break
    return out


def _strings(value: Any, out: list[str], depth: int = 0) -> None:
    if depth > MAX_DEPTH:
        raise ScreenUnavailable("result nested too deeply")
    if isinstance(value, str):
        out.append(value)
    elif isinstance(value, dict):
        for key, item in value.items():
            out.append(str(key))
            _strings(item, out, depth + 1)
    elif isinstance(value, (list, tuple)):
        for item in value:
            _strings(item, out, depth + 1)


def _val(x: Any) -> str:
    return str(getattr(x, "value", x)).lower()


def _scan_blocking(scanner: Any, message: Any) -> Any:
    """Run scanner.scan (a coroutine that computes synchronously, or a plain function) off the loop."""
    result = scanner.scan(message)
    if inspect.isawaitable(result):
        async def _await() -> Any:
            return await result
        result = asyncio.run(_await())
    return result


class ResultScreen:
    def __init__(self, scanner: Any, tokenizer: Any, make_message: Callable[[str], Any] | None = None,
                 timeout_s: float = 30.0):
        self.scanner = scanner
        self.tokenizer = tokenizer
        self.make_message = make_message or (lambda text: SimpleNamespace(content=text))
        self.timeout_s = timeout_s

    async def _scan_all(self, result: Any) -> tuple[str, Any]:
        parts: list[str] = []
        _strings(result, parts)
        text = "\n".join(parts)
        if len(text) > MAX_CHARS:
            raise ScreenUnavailable("result too large")
        score = None
        for window in windows(text, self.tokenizer):
            scan = await asyncio.to_thread(_scan_blocking, self.scanner, self.make_message(window))
            if _val(scan.status) != "success":
                raise ScreenUnavailable("scanner did not return success")
            score = getattr(scan, "score", None)
            # a block and a human-review hold both withhold; only an explicit allow passes
            if _val(scan.decision) != "allow":
                return "block", score
        return "allow", score

    async def allows(self, result: Any, tool_name: str = "") -> bool:
        """True only on an explicit allow for every window. Never logs the scanned text or the reason."""
        try:
            outcome, score = await asyncio.wait_for(self._scan_all(result), self.timeout_s)
        except Exception as exc:  # unknown verdict: withhold, record the type only
            logger.warning("tool_result_screen tool=%s outcome=unavailable error=%s", tool_name, type(exc).__name__)
            return False
        logger.info("tool_result_screen tool=%s outcome=%s score=%s", tool_name, outcome, score)
        return outcome == "allow"


_screen: ResultScreen | None = None


def configure_screen(screen: ResultScreen | None) -> None:
    """Call once at startup. With no screen configured every tool result is withheld."""
    global _screen
    _screen = screen


async def screen_tool_result(tool: Any, args: dict, tool_context: Any, tool_response: Any) -> dict | None:
    """after_tool_callback: replace a result the screen does not explicitly allow."""
    if _screen is None:
        logger.warning("tool_result_screen tool=%s outcome=unconfigured", tool.name)
        return dict(WITHHELD)
    if await _screen.allows(tool_response, tool_name=tool.name):
        return None
    return dict(WITHHELD)
