"""Existing public adapter for one finite, decoded ADK answer stream.

The caller owns authentication and decoding. The implementation currently accepts
text too early; repair it without changing the public interface.
"""

from collections.abc import AsyncIterable, Awaitable, Callable


class AnswerRejected(ValueError):
    """The invocation did not produce an accepted complete answer."""


async def collect_answer(
    events: AsyncIterable[dict],
    *,
    invocation_id: str,
    answer_author: str,
    on_preview: Callable[[str], Awaitable[None]],
) -> str:
    """Return completed public text, with provisional snapshots via the callback."""
    preview = ""
    async for event in events:
        content = event.get("content") or {}
        text = "".join(part.get("text", "") for part in content.get("parts", []))
        if not text:
            continue
        if event.get("partial"):
            preview += text
            await on_preview(preview)
        else:
            return text
    raise AnswerRejected("incomplete_answer")
