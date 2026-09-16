"""Accept one complete public answer from a finite, decoded ADK event stream.

Validation and lifecycle patterns adapted from the MIT-licensed
optimise-adk-on-google-cloud/assets/finite_answer_stream.py skill asset.
Copyright (c) 2026 RuslanKhis. See LICENSE.finite-answer-stream.
The application owns authentication, transport decoding and raw-byte admission.
"""

import asyncio
from collections.abc import AsyncIterable, Awaitable, Callable


class AnswerRejected(ValueError):
    """The invocation did not produce an accepted complete answer."""


class _InvalidEvent(ValueError):
    """Internal fixed rejection codes; never raised by a user callback."""


_TOOL_FIELDS = (
    ("function_call", "functionCall"),
    ("function_response", "functionResponse"),
    ("executable_code", "executableCode"),
    ("code_execution_result", "codeExecutionResult"),
    ("tool_call", "toolCall"),
    ("tool_response", "toolResponse"),
)
_PART_FIELDS = frozenset({
    "text", "thought", "thought_signature", "thoughtSignature",
    *(name for aliases in _TOOL_FIELDS for name in aliases),
})


def _alias(value: dict, *names: str):
    present = [value[name] for name in names if name in value]
    if not present:
        return None
    if any(type(item) is not type(present[0]) or item != present[0]
           for item in present[1:]):
        raise _InvalidEvent("invalid_event")
    return present[0]


def _answer_text(event: dict, invocation_id: str, answer_author: str):
    """Check run status before selecting eligible text, including ignored events."""
    if type(event) is not dict:
        raise _InvalidEvent("invalid_event")
    identity = _alias(event, "invocation_id", "invocationId")
    if type(identity) is not str or identity != invocation_id:
        raise _InvalidEvent("invocation_mismatch")
    for names in (("error",), ("error_code", "errorCode"),
                  ("error_message", "errorMessage")):
        if _alias(event, *names) not in (None, ""):
            raise _InvalidEvent("stream_error")
    partial = event.get("partial")
    interrupted = event.get("interrupted")
    if any(value is not None and type(value) is not bool
           for value in (partial, interrupted)):
        raise _InvalidEvent("invalid_event")
    if interrupted:
        raise _InvalidEvent("interrupted")
    reason = _alias(event, "finish_reason", "finishReason")
    if reason is not None and type(reason) is not str:
        raise _InvalidEvent("invalid_event")
    if reason not in (None, "STOP"):
        raise _InvalidEvent("unaccepted_finish")

    content = event.get("content")
    if content is None:
        content = {}
    if type(content) is not dict:
        raise _InvalidEvent("invalid_event")
    parts = content.get("parts")
    if parts is None:
        parts = []
    if type(parts) is not list:
        raise _InvalidEvent("invalid_event")
    text, tool = [], False
    for part in parts:
        if type(part) is not dict:
            raise _InvalidEvent("invalid_event")
        # Unknown payloads need a separate completion contract. Null SDK defaults
        # are harmless; tool envelopes are protocol work, not verified results.
        if any(name not in _PART_FIELDS and value is not None
               for name, value in part.items()):
            raise _InvalidEvent("unsupported_content")
        thought = part.get("thought")
        value = part.get("text")
        if ((thought is not None and type(thought) is not bool)
                or (value is not None and type(value) is not str)):
            raise _InvalidEvent("invalid_event")
        signature = _alias(part, "thought_signature", "thoughtSignature")
        if signature is not None and type(signature) is not str:
            raise _InvalidEvent("invalid_event")
        for names in _TOOL_FIELDS:
            function = _alias(part, *names)
            if function is not None:
                if type(function) is not dict:
                    raise _InvalidEvent("invalid_event")
                tool = True
        if not thought and value is not None:
            text.append(value)
    if (event.get("author") != answer_author or content.get("role") != "model"
            or tool or not text):
        return None, partial is True, reason
    return "".join(text), partial is True, reason


async def _close_iterator(iterator):
    close = getattr(iterator, "aclose", None)
    if close is not None:
        await close()


async def collect_answer(
    events: AsyncIterable[dict],
    *,
    invocation_id: str,
    answer_author: str,
    on_preview: Callable[[str], Awaitable[None]],
) -> str:
    """Await delta previews; return one STOP aggregate after exhaustion and close.

    Only the return value is authoritative and replaces the provisional preview.
    Protocol rejections are retained while draining the finite stream; callback
    or transport exceptions stop consumption. Every acquired iterator is closed
    when it supports aclose. Closure must cooperate and finish even if the caller
    cancels during cleanup. No limits or transport policy are imposed here.
    """
    iterator = None
    candidate = None
    failure = None
    cancellation = None
    task = asyncio.current_task()
    initial_cancel_requests = task.cancelling()
    try:
        iterator = aiter(events)
        preview = ""
        # Use the obtained iterator directly: do not call __aiter__ a second time.
        while True:
            try:
                event = await anext(iterator)
            except StopAsyncIteration:
                break
            if task.cancelling() > initial_cancel_requests:
                raise asyncio.CancelledError()
            try:
                text, partial, reason = _answer_text(event, invocation_id, answer_author)
            except _InvalidEvent as error:
                failure = failure or str(error)
                continue
            if failure is not None or text is None:
                continue
            if candidate is not None:
                failure = "answer_after_completion"
            elif partial:
                preview += text
                await on_preview(preview)
                if task.cancelling() > initial_cancel_requests:
                    raise asyncio.CancelledError()
            elif text.strip():
                if reason != "STOP":
                    failure = "incomplete_answer"
                else:
                    candidate = text
        if candidate is None:
            failure = failure or "incomplete_answer"
    except asyncio.CancelledError as error:
        cancellation = error
    except Exception:
        # Includes external exceptions of our exported AnswerRejected type.
        failure = failure or "stream_failed"

    # An upstream coroutine may have swallowed cancellation before yielding/EOF.
    if cancellation is None and task.cancelling() > initial_cancel_requests:
        cancellation = asyncio.CancelledError()

    cleanup_failed = False
    if iterator is not None:
        # Shield only cleanup, retain its task, and join it before returning or
        # raising. Repeated caller cancellation must not leave it in the background.
        closing = asyncio.create_task(_close_iterator(iterator))
        while True:
            try:
                await asyncio.shield(closing)
            except asyncio.CancelledError as error:
                if cancellation is None and task.cancelling() > initial_cancel_requests:
                    cancellation = error
                if closing.done():
                    # Retrieve a simultaneous close failure as well as cancellation.
                    cleanup_failed = closing.cancelled() or closing.exception() is not None
                    break
            except Exception:
                cleanup_failed = True
                break
            else:
                break

    # Raise outside handlers: provider/callback/close contents must not escape
    # through either the public message or exception chaining.
    if cancellation is not None:
        if cleanup_failed:
            cancellation.add_note("answer_cleanup_failed")
        raise cancellation
    if failure is not None:
        raise AnswerRejected(failure)
    if cleanup_failed:
        raise AnswerRejected("cleanup_failed")
    return candidate
