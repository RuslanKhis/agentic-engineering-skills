"""How a chat message answers (or does not answer) a pending refund confirmation.

An approval is only ever granted by an explicit, timely "yes". A missing, late or
unclear answer never authorizes the tool: the pending request is rejected instead.
"""
from __future__ import annotations

import time
from dataclasses import dataclass

CONFIRMATION_CALL = "adk_request_confirmation"

# An unanswered request older than this is dead; a later "yes" cannot revive it.
CONFIRMATION_TTL_SECONDS = 15 * 60

APPROVE_WORDS = frozenset({"yes", "y", "yes please", "confirm", "confirmed", "approve", "approved",
                           "go ahead", "yes, go ahead", "yes go ahead", "do it"})
REJECT_PREFIXES = ("no", "cancel", "stop")

EXPIRED_REPLY = ("That refund request was waiting too long and has been cancelled. "
                 "Nothing was refunded. Tell me again if you still want it.")


@dataclass(frozen=True)
class Pending:
    call_id: str
    requested_at: float


@dataclass(frozen=True)
class Resolution:
    """What the server does with a message.

    reject_call_id: if set, first send a rejection for this request (the tool does not run).
    answer: "approve" | "reject" | None. When set, the message is the answer and nothing else runs.
    run_text: if True, the message is then processed as a new message.
    static_reply: if set, returned to the customer without waiting on a new model turn.
    """
    call_id: str | None = None
    answer: str | None = None
    reject_call_id: str | None = None
    run_text: bool = True
    static_reply: str | None = None


def find_pending(session) -> Pending | None:
    """The newest confirmation request that has no answer yet."""
    answered: set[str] = set()
    pending: Pending | None = None
    for event in session.events:
        for call in event.get_function_calls():
            if call.name == CONFIRMATION_CALL:
                pending = Pending(call.id, getattr(event, "timestamp", 0.0) or 0.0)
        for response in event.get_function_responses():
            if response.name == CONFIRMATION_CALL:
                answered.add(response.id)
    if pending and pending.call_id not in answered:
        return pending
    return None


def classify(text: str) -> str | None:
    t = " ".join(text.strip().lower().rstrip(".!").split())
    if t in APPROVE_WORDS:
        return "approve"
    if t.startswith(REJECT_PREFIXES):
        return "reject"
    return None


def resolve(session, text: str, now: float | None = None,
            ttl: float = CONFIRMATION_TTL_SECONDS) -> Resolution:
    pending = find_pending(session)
    if pending is None:
        return Resolution()
    now = time.time() if now is None else now
    verdict = classify(text)
    if now - pending.requested_at > ttl:
        # Late answer: reject the stale request, never execute it.
        if verdict == "approve":
            return Resolution(reject_call_id=pending.call_id, run_text=False, static_reply=EXPIRED_REPLY)
        return Resolution(reject_call_id=pending.call_id)
    if verdict in ("approve", "reject"):
        return Resolution(call_id=pending.call_id, answer=verdict, run_text=False)
    # Anything else is a new message: the unanswered request is closed as rejected first.
    return Resolution(reject_call_id=pending.call_id)
