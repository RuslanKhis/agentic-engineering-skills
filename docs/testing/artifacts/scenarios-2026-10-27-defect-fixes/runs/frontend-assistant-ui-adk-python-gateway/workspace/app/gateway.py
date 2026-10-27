"""Gateway rules for the assistant-ui proxy route: request parsing, the public event filter,
approval checks and edit checkpoints. Pure functions; no google.adk import, so unit tests run
without the SDK. app/server.py wires them to the Runner."""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any, Iterable, Mapping

CONFIRMATION_CALL = "adk_request_confirmation"
MAX_TEXT_CHARS = 8000
MAX_PARTS = 16
SESSION_ID_RE = re.compile(r"^[A-Za-z0-9_-]{1,128}$")
FIXED_ERROR = {"errorCode": "run_failed", "errorMessage": "Something went wrong. Please try again."}

# Tool results the browser may see, by tool; any other tool exposes status and message only.
PUBLIC_RESULT_KEYS = {
    "issue_refund": ("status", "refund_id", "amount_cents", "message"),
}
DEFAULT_RESULT_KEYS = ("status", "message")
# A refund that went through cannot be undone by rewinding the conversation.
WRITE_TOOLS = {"issue_refund": "refunded", "send_email": "sent"}


class BadRequest(Exception):
    """Carries an HTTP status and a controlled public code."""

    def __init__(self, status: int, code: str):
        super().__init__(code)
        self.status = status
        self.code = code


@dataclass(frozen=True)
class Approval:
    call_id: str
    confirmed: bool


@dataclass(frozen=True)
class Turn:
    session_id: str
    approvals: tuple[Approval, ...] = ()
    text: str = ""
    checkpoint: str | None = None


def _text_of(part: Mapping[str, Any]) -> str | None:
    value = part.get("text")
    return value if isinstance(value, str) else None


def parse_request(body: Any) -> Turn:
    """Validate the proxy body. Refuses stateDelta, ignores runConfig and the browser's ids."""
    if not isinstance(body, dict):
        raise BadRequest(422, "invalid_request")
    session_id = body.get("sessionId")
    if not isinstance(session_id, str) or not SESSION_ID_RE.match(session_id):
        raise BadRequest(422, "invalid_request")
    if body.get("stateDelta"):
        raise BadRequest(422, "state_not_accepted")
    checkpoint = body.get("checkpointId")
    if checkpoint is not None and not (
            isinstance(checkpoint, str) and (checkpoint == "start" or re.fullmatch(r"after:[\w-]{1,128}", checkpoint))):
        raise BadRequest(422, "invalid_checkpoint")

    parts = body.get("parts")
    if parts is None:
        parts = [{"text": body["message"]}] if "message" in body else []
    if not isinstance(parts, list) or len(parts) > MAX_PARTS:
        raise BadRequest(422, "invalid_request")

    texts: list[str] = []
    approvals: list[Approval] = []
    for part in parts:
        if not isinstance(part, dict):
            raise BadRequest(422, "invalid_request")
        response = part.get("functionResponse")
        if response is not None:
            approvals.append(_parse_approval(response))
            continue
        text = _text_of(part)
        # Calls, thoughts, code and anything else a client could smuggle into a new message.
        if text is None or set(part) - {"text"}:
            if part.get("functionCall") is not None and set(part) == {"functionCall"}:
                continue  # assistant-ui echoes cancellation stubs; the gateway ignores them
            raise BadRequest(422, "unsupported_part")
        texts.append(text)
    text = "".join(texts).strip()
    if len(text) > MAX_TEXT_CHARS:
        raise BadRequest(422, "message_too_long")
    if not text and not approvals and checkpoint is None:
        raise BadRequest(422, "empty_message")
    if approvals and checkpoint is not None:
        raise BadRequest(422, "invalid_request")
    return Turn(session_id=session_id, approvals=tuple(approvals), text=text, checkpoint=checkpoint)


def _parse_approval(response: Any) -> Approval:
    if not isinstance(response, dict):
        raise BadRequest(422, "invalid_approval")
    call_id = response.get("id")
    body = response.get("response")
    if (response.get("name") != CONFIRMATION_CALL or not isinstance(call_id, str) or not call_id
            or not isinstance(body, dict) or set(body) != {"confirmed"} or not isinstance(body["confirmed"], bool)):
        raise BadRequest(422, "invalid_approval")
    return Approval(call_id=call_id, confirmed=body["confirmed"])


# ---- session history, summarised from ADK events (duck-typed) ----

@dataclass
class Step:
    invocation_id: str
    author: str = ""
    user_text: str = ""
    rewind_before: str | None = None
    calls: list[tuple[str, str]] = field(default_factory=list)  # (id, name)
    responses: list[tuple[str, str, Any]] = field(default_factory=list)  # (id, name, response)


def summarize(events: Iterable[Any]) -> list[Step]:
    steps = []
    for e in events:
        step = Step(invocation_id=getattr(e, "invocation_id", "") or "", author=getattr(e, "author", "") or "")
        actions = getattr(e, "actions", None)
        step.rewind_before = getattr(actions, "rewind_before_invocation_id", None) if actions else None
        for p in getattr(getattr(e, "content", None), "parts", None) or []:
            if getattr(p, "function_call", None):
                step.calls.append((p.function_call.id, p.function_call.name))
            elif getattr(p, "function_response", None):
                fr = p.function_response
                step.responses.append((fr.id, fr.name, fr.response))
            elif getattr(p, "text", None) and step.author == "user" and not getattr(p, "thought", False):
                step.user_text += p.text
        steps.append(step)
    return steps


def live_steps(steps: list[Step]) -> list[Step]:
    """Drop events that a rewind marker removed from the conversation."""
    live: list[Step] = []
    for s in steps:
        if s.rewind_before:
            cut = next((i for i, x in enumerate(live) if x.invocation_id == s.rewind_before), None)
            if cut is not None:
                live = live[:cut]
            continue
        live.append(s)
    return live


def pending_confirmations(steps: list[Step]) -> set[str]:
    """Ids of confirmation calls in the live history that have no response yet."""
    live = live_steps(steps)
    pending = {c for s in live for c, n in s.calls if n == CONFIRMATION_CALL}
    for s in live:
        for rid, _, _ in s.responses:
            pending.discard(rid)
    return pending


def check_approvals(steps: list[Step], approvals: Iterable[Approval]) -> None:
    pending = pending_confirmations(steps)
    seen: set[str] = set()
    for a in approvals:
        if a.call_id not in pending or a.call_id in seen:
            raise BadRequest(409, "approval_not_pending")
        seen.add(a.call_id)


@dataclass(frozen=True)
class Rewind:
    before_invocation_id: str | None  # None: nothing to rewind, append normally
    user_text: str  # text of the first removed user message, for a regenerate


def plan_edit(steps: list[Step], checkpoint: str) -> Rewind:
    """Resolve `start` / `after:<invocation id>` to the invocation to rewind before."""
    live = live_steps(steps)
    order: list[str] = []
    for s in live:
        if s.invocation_id and s.invocation_id not in order:
            order.append(s.invocation_id)
    if checkpoint == "start":
        index = 0
    else:
        anchor = checkpoint.removeprefix("after:")
        if anchor not in order:
            raise BadRequest(409, "checkpoint_unknown")
        index = order.index(anchor) + 1
    if index >= len(order):
        return Rewind(None, "")
    removed = set(order[index:])
    for s in live:
        if s.invocation_id in removed:
            for _, name, response in s.responses:
                if name in WRITE_TOOLS and isinstance(response, dict) and response.get("status") == WRITE_TOOLS[name]:
                    raise BadRequest(409, "rewind_blocked")
    target = order[index]
    first = next((s.user_text for s in live if s.invocation_id == target and s.author == "user" and s.user_text), "")
    return Rewind(target, first)


# ---- public event filter ----

def _public_result(name: str, response: Any) -> dict:
    keys = PUBLIC_RESULT_KEYS.get(name, DEFAULT_RESULT_KEYS)
    if not isinstance(response, dict):
        return {"status": "error"}
    return {k: response[k] for k in keys if k in response and isinstance(response[k], (str, int, bool))}


def _public_confirmation_args(args: Any) -> dict:
    args = args if isinstance(args, dict) else {}
    original = args.get("originalFunctionCall") or {}
    out: dict[str, Any] = {"originalFunctionCall": {
        "id": original.get("id"), "name": original.get("name"),
        "args": original.get("args") if isinstance(original.get("args"), dict) else {}}}
    hint = (args.get("toolConfirmation") or {}).get("hint")
    if isinstance(hint, str):
        out["toolConfirmation"] = {"hint": hint}
    return out


def public_event(event: Mapping[str, Any], agent_name: str) -> dict | None:
    """Reduce one ADK event (camelCase JSON) to the public allowlist; None drops it.

    Dropped: thought parts, state deltas, usage and grounding metadata, auth requests, raw error
    text and every author but the user and the agent."""
    if event.get("errorCode") or event.get("errorMessage"):
        return dict(FIXED_ERROR, invocationId=event.get("invocationId"))
    if event.get("author") not in ("user", agent_name):
        return None
    parts = []
    for p in (event.get("content") or {}).get("parts") or []:
        if p.get("thought"):
            continue
        if isinstance(p.get("text"), str):
            parts.append({"text": p["text"]})
        elif p.get("functionCall"):
            fc = p["functionCall"]
            args = _public_confirmation_args(fc.get("args")) if fc.get("name") == CONFIRMATION_CALL else (
                fc.get("args") if isinstance(fc.get("args"), dict) else {})
            parts.append({"functionCall": {"id": fc.get("id"), "name": fc.get("name"), "args": args}})
        elif p.get("functionResponse"):
            fr = p["functionResponse"]
            parts.append({"functionResponse": {"id": fr.get("id"), "name": fr.get("name"),
                                               "response": _public_result(fr.get("name") or "", fr.get("response"))}})
    if not parts:
        return None
    out = {"id": event.get("id"), "invocationId": event.get("invocationId"), "author": event.get("author"),
           "content": {"role": (event.get("content") or {}).get("role"), "parts": parts}}
    if event.get("partial"):
        out["partial"] = True
    if event.get("longRunningToolIds"):
        out["longRunningToolIds"] = list(event["longRunningToolIds"])
    return out
