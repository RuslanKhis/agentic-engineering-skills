"""Capability gate for every tool call (before_tool_callback).

Started from the adk-agent-security skill's injection-patterns gate (CaMeL-style capability checks)
and extended: the first copy let any tool that was not an egress tool through, so delete_file and
archive_thread were never checked. Now every tool needs a policy and unknown tools are refused.
"""
from typing import Any

READ_ONLY_TOOLS = {"search_mail"}                   # no side effects: allowed without a plan
EGRESS_TOOLS = {"send_email", "post_webhook"}
EGRESS_ARGS = {"to", "url", "body"}
# Tools whose target must be a value the user typed: tool name -> target argument.
USER_TARGET_TOOLS = {"delete_file": "file_id"}
# Reversible writes: the target may come from a search result, but the callable is wrapped in
# require_confirmation (agent.py) so a person sees it first.
CONFIRMED_WRITE_TOOLS = {"archive_thread": "thread_id"}
MIN_TAINT_LENGTH = 8   # shorter tainted values match exactly only; set it per domain


def _refuse(message: str, hint: str = "none") -> dict:
    return {"status": "error", "error_message": message, "hint": hint}


def _is_tainted(value: str, tainted: set[str]) -> bool:
    return value in tainted or any(len(t) >= MIN_TAINT_LENGTH and t in value for t in tainted)


def capability_gate(tool: Any, args: dict[str, Any], tool_context: Any) -> dict | None:
    try:
        return _decide(tool, args, tool_context.state)
    except Exception:                                # fail closed: a gate error must not allow the call
        return _refuse(f"policy check failed for {getattr(tool, 'name', '?')}")


def _decide(tool: Any, args: dict[str, Any], state: Any) -> dict | None:
    plan = state.get("plan:allowed_tools")          # written by a planner step if one exists; none does yet
    if plan is not None and tool.name not in plan:
        return _refuse(f"{tool.name} is not in the approved plan",
                       "Ask the user to restart with a plan that includes this step.")
    if tool.name in READ_ONLY_TOOLS:
        return None

    tainted = set(state.get("taint:untrusted_fields", []))

    if tool.name in USER_TARGET_TOOLS:
        # Provenance rule: the target must come from the user's own message and never from content.
        target = str(args.get(USER_TARGET_TOOLS[tool.name], ""))
        if not target or _is_tainted(target, tainted) or target not in state.get("provenance:user_values", []):
            return _refuse(f"{tool.name} target was not given by the user",
                           "Ask the user to name the file id themselves.")
        return None

    if tool.name in CONFIRMED_WRITE_TOOLS:
        target = str(args.get(CONFIRMED_WRITE_TOOLS[tool.name], ""))
        # A thread id must at least be one the mailbox returned or the user typed, never invented.
        if not target or (target not in tainted and target not in state.get("provenance:user_values", [])):
            return _refuse(f"{tool.name} target is not a known thread id")
        return None

    if tool.name not in EGRESS_TOOLS:               # deny by default: a new tool needs its own policy
        return _refuse(f"no policy covers {tool.name}",
                       "Ask the owner to classify this tool before the agent may call it.")

    # The labeller stores values extracted from untrusted results (addresses, URLs, account ids),
    # not whole chunks, so a short destination embedded inside a long chunk still matches.
    for key in EGRESS_ARGS & set(args):
        if _is_tainted(str(args[key]), tainted):
            return _refuse("argument derived from untrusted content",
                           "Only values entered by the user may be sent externally.")
    allowed_destinations = state.get("policy:egress_allowlist", [])
    for key in ("to", "url"):
        if key in args and args[key] not in allowed_destinations:
            return _refuse("destination not in allowlist")
    return None
