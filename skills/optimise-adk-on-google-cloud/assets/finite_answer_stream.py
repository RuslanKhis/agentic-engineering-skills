"""Optional Python 3.11 acceptance boundary for one finite decoded ADK stream.

The caller supplies a trusted invocation ID and answer author, bounds raw bytes
BEFORE decoding, and owns authentication and the transport. This component is
not an SSE parser, tool-result validator, provider budget/cancellation mechanism,
durable message store, or consumer for bidirectional/multiple-answer protocols.

``send_preview`` receives provisional display snapshots: delta input is appended;
snapshot input replaces the preceding preview. Only the returned AcceptedAnswer
may be committed, replacing any preview. On failure mark the preview incomplete.
Deadlines and iterator closure require cooperative asynchronous implementations.
Limits below are teaching defaults, not ADK or provider defaults.
"""

import asyncio
from collections.abc import AsyncIterable, Awaitable, Callable
from dataclasses import dataclass
import json
import math


class StreamRejected(ValueError):
    """Fixed public code, with a safe flag for a secondary close failure."""

    def __init__(self, code: str, *, cleanup_failed: bool = False):
        super().__init__(code)
        self.cleanup_failed = cleanup_failed


@dataclass(frozen=True)
class StreamLimits:
    max_events: int = 256
    max_event_bytes: int = 64 * 1024
    max_total_bytes: int = 1024 * 1024
    max_visible_bytes: int = 64 * 1024
    overall_seconds: float = 60.0
    close_seconds: float = 2.0

    def __post_init__(self):
        counts = (self.max_events, self.max_event_bytes,
                  self.max_total_bytes, self.max_visible_bytes)
        times = (self.overall_seconds, self.close_seconds)
        if any(type(value) is not int or value < 1 for value in counts):
            raise StreamRejected("invalid_configuration")
        try:
            valid_times = all(type(value) in (int, float) and math.isfinite(value)
                              and value > 0 for value in times)
        except OverflowError:
            valid_times = False
        if not valid_times:
            raise StreamRejected("invalid_configuration")


@dataclass(frozen=True)
class AcceptedAnswer:
    text: str
    event_count: int
    partial_count: int


def _alias(value: dict, *names: str, default=None):
    present = [value[name] for name in names if name in value]
    if not present:
        return default
    if any(type(item) is not type(present[0]) or item != present[0]
           for item in present[1:]):
        raise StreamRejected("invalid_event")
    return present[0]


def _json_bytes(event: object) -> int:
    if type(event) is not dict:
        raise StreamRejected("invalid_event")
    # Encoding rejects cycles, nonfinite numbers and invalid Unicode. The plain
    # value pass also rejects coercions accepted by json.dumps (e.g. integer keys
    # and tuples). Upstream raw-byte limits bound this synchronous work.
    encoded = json.dumps(event, ensure_ascii=False, allow_nan=False,
                         separators=(",", ":")).encode("utf-8")
    pending = [event]
    while pending:
        value = pending.pop()
        if type(value) is dict:
            if any(type(key) is not str for key in value):
                raise StreamRejected("invalid_event")
            pending.extend(value.values())
        elif type(value) is list:
            pending.extend(value)
        elif type(value) not in (str, int, float, bool, type(None)):
            raise StreamRejected("invalid_event")
    return len(encoded)


def _checked_text(event: dict, invocation_id: str):
    identity = _alias(event, "invocation_id", "invocationId")
    if type(identity) is not str or identity != invocation_id:
        raise StreamRejected("invocation_mismatch")
    for names in (("error",), ("error_code", "errorCode"),
                  ("error_message", "errorMessage")):
        if _alias(event, *names) not in (None, ""):
            raise StreamRejected("stream_error")
    interrupted = event.get("interrupted")
    partial = event.get("partial")
    if any(value is not None and type(value) is not bool
           for value in (interrupted, partial)):
        raise StreamRejected("invalid_event")
    if interrupted:
        raise StreamRejected("interrupted")
    reason = _alias(event, "finish_reason", "finishReason")
    if reason is not None and type(reason) is not str:
        raise StreamRejected("invalid_event")
    if reason not in (None, "STOP"):
        raise StreamRejected("unaccepted_finish")
    author = event.get("author")
    if type(author) is not str or not author:
        raise StreamRejected("invalid_event")
    content = event.get("content")
    if content is None:
        content = {}
    if type(content) is not dict:
        raise StreamRejected("invalid_event")
    role = content.get("role")
    if role is not None and type(role) is not str:
        raise StreamRejected("invalid_event")
    parts = content.get("parts")
    if parts is None:
        parts = []
    if type(parts) is not list:
        raise StreamRejected("invalid_event")
    text, tool = [], False
    for part in parts:
        if type(part) is not dict:
            raise StreamRejected("invalid_event")
        # This finite text-answer boundary deliberately rejects other payloads
        # (including media and future SDK fields) rather than accepting their
        # accompanying narration as a complete answer. Null SDK defaults carry
        # no payload and remain compatible with exclude_none=False dumps.
        if any(name not in _PART_FIELDS and value is not None
               for name, value in part.items()):
            raise StreamRejected("unsupported_content")
        thought = part.get("thought")
        if thought is not None and type(thought) is not bool:
            raise StreamRejected("invalid_event")
        value = part.get("text")
        if value is not None and type(value) is not str:
            raise StreamRejected("invalid_event")
        signature = _alias(part, "thought_signature", "thoughtSignature")
        if signature is not None and type(signature) is not str:
            raise StreamRejected("invalid_event")
        for names in _TOOL_FIELDS:
            function = _alias(part, *names)
            if function is not None:
                if type(function) is not dict:
                    raise StreamRejected("invalid_event")
                tool = True
        if not thought and value is not None:
            text.append(value)
    return author, role, "".join(text) if text else None, tool, partial is True, reason


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


def _deadline_elapsed(deadline: asyncio.Timeout) -> bool:
    # An adapter can suppress timeout cancellation or return without yielding
    # long enough to starve the scheduled timeout callback. Neither permits a
    # late answer to be accepted after control returns to this consumer.
    return (deadline.expired()
            or asyncio.get_running_loop().time() >= deadline.when())


def _suppressed_cancellation() -> asyncio.CancelledError:
    error = asyncio.CancelledError()
    # The adapter already swallowed the original exception, so its identity and
    # message cannot be recovered. Do not invent either or return success.
    error.add_note("stream_cancellation_was_suppressed")
    return error


async def consume_answer(
    events: AsyncIterable[dict], *, answer_author: str, invocation_id: str,
    preview_mode: str, send_preview: Callable[[str], Awaitable[None]],
    limits: StreamLimits = StreamLimits(), min_partials: int = 0,
) -> AcceptedAnswer:
    """Consume, close and accept exactly one complete answer, or fail safely.

    Every event must carry the expected invocation identity. Snake/camel field
    aliases may coexist only when identical. Byte limits count compact UTF-8
    re-encoding, not original wire bytes; visible bytes count all eligible text,
    including every cumulative snapshot and the final answer. Limits are inclusive.
    The callback receives provisional snapshots, including whitespace or clearing
    updates. Only nonblank input partials count toward ``min_partials``. No final callback
    is made. After a candidate, any nonthought model text or tool activity rejects.

    This call owns the iterator it obtains and calls its ``aclose`` when provided,
    even after exhaustion. Exceptions from inputs/callbacks/closure are sanitised.
    A primary rejection survives closure failure via ``cleanup_failed=True``;
    caller cancellation is re-raised with a fixed note if closure also fails.
    Text, thought signatures and function/code/server-side tool parts are supported;
    other nonnull part fields reject. Detected swallowed cancellation prevents
    acceptance, but its original exception cannot be recovered. Deadlines cannot
    force an uncooperative adapter to return control.
    """
    iterator = None
    failure = None
    cancellation = None
    result = None
    deadline = None
    task = asyncio.current_task()
    initial_cancel_requests = task.cancelling()
    try:
        if (type(answer_author) is not str or not answer_author
                or type(invocation_id) is not str or not invocation_id
                or preview_mode not in ("delta", "snapshot")
                or type(preview_mode) is not str or not callable(send_preview)
                or type(limits) is not StreamLimits
                or type(min_partials) is not int
                or not 0 <= min_partials <= limits.max_events):
            raise StreamRejected("invalid_configuration")
        candidate, preview = None, ""
        count = total_bytes = visible_bytes = partials = 0
        deadline = asyncio.timeout(limits.overall_seconds)
        async with deadline:
            iterator = aiter(events)
            if _deadline_elapsed(deadline):
                raise StreamRejected("deadline_exceeded")
            async for event in iterator:
                if _deadline_elapsed(deadline):
                    raise StreamRejected("deadline_exceeded")
                if task.cancelling() > initial_cancel_requests:
                    raise _suppressed_cancellation()
                count += 1
                if count > limits.max_events:
                    raise StreamRejected("event_limit")
                size = _json_bytes(event)
                total_bytes += size
                if size > limits.max_event_bytes or total_bytes > limits.max_total_bytes:
                    raise StreamRejected("event_bytes_limit")
                author, role, text, tool, partial, reason = _checked_text(event, invocation_id)
                if candidate is not None and (tool or (role == "model" and text)):
                    raise StreamRejected("activity_after_answer")
                if author != answer_author or role != "model" or tool or text is None:
                    continue
                visible_bytes += len(text.encode("utf-8"))
                if visible_bytes > limits.max_visible_bytes:
                    raise StreamRejected("visible_bytes_limit")
                if partial:
                    partials += bool(text.strip())
                    preview = preview + text if preview_mode == "delta" else text
                    await send_preview(preview)
                    if _deadline_elapsed(deadline):
                        raise StreamRejected("deadline_exceeded")
                    if task.cancelling() > initial_cancel_requests:
                        raise _suppressed_cancellation()
                elif text.strip():
                    if reason != "STOP":
                        raise StreamRejected("missing_completion")
                    candidate = text
            if _deadline_elapsed(deadline):
                raise StreamRejected("deadline_exceeded")
            if candidate is None or partials < min_partials:
                raise StreamRejected("missing_completion")
            result = AcceptedAnswer(candidate, count, partials)
    except asyncio.CancelledError as error:
        cancellation = error
    except TimeoutError:
        failure = "deadline_exceeded" if deadline is not None and deadline.expired() else "stream_failed"
    except StreamRejected as error:
        # Only internally raised codes reach this public boundary: callbacks and
        # iterators could raise our exception class with their own payload.
        failure = str(error) if str(error) in _PUBLIC_CODES else "stream_failed"
    except Exception:
        failure = "stream_failed"

    # Timeout.__aexit__ has now removed its own cancellation request. Any new
    # remaining request belongs to a caller, even if an adapter swallowed it.
    if cancellation is None and task.cancelling() > initial_cancel_requests:
        cancellation = _suppressed_cancellation()

    cleanup_failed = False
    if iterator is not None:
        closing_task = asyncio.current_task()
        prior_cancel_requests = closing_task.cancelling()
        try:
            close_deadline = asyncio.timeout(limits.close_seconds)
            async with close_deadline:
                close = getattr(iterator, "aclose", None)
                if close is not None:
                    await close()
            if _deadline_elapsed(close_deadline):
                cleanup_failed = True
        except asyncio.CancelledError as error:
            cleanup_failed = True
            # An iterator can raise CancelledError itself. Only a new task
            # cancellation request during close supersedes an earlier rejection;
            # otherwise it is a secondary close failure. An original caller
            # cancellation retains its identity even if another request arrives.
            if cancellation is None and closing_task.cancelling() > prior_cancel_requests:
                cancellation = error
        except Exception:
            cleanup_failed = True
        if closing_task.cancelling() > prior_cancel_requests:
            cleanup_failed = True
            if cancellation is None:
                cancellation = _suppressed_cancellation()
    # Raise outside exception handlers so diagnostic chaining cannot expose raw
    # provider/callback/decoder errors or their payloads.
    if cancellation is not None:
        if cleanup_failed:
            cancellation.add_note("stream_cleanup_failed")
        if failure is not None:
            cancellation.add_note("stream_rejected_before_cancellation")
        raise cancellation
    if failure is not None:
        raise StreamRejected(failure, cleanup_failed=cleanup_failed)
    if cleanup_failed:
        raise StreamRejected("cleanup_failed", cleanup_failed=True)
    return result


_PUBLIC_CODES = frozenset({
    "invalid_configuration", "invalid_event", "invocation_mismatch",
    "stream_error", "interrupted", "unaccepted_finish", "event_limit",
    "event_bytes_limit", "activity_after_answer", "visible_bytes_limit",
    "missing_completion", "unsupported_content", "deadline_exceeded",
})
