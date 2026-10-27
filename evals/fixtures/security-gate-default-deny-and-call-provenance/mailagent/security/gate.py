"""Capability gate for every tool call (before_tool_callback).

Copied from the adk-agent-security skill's injection-patterns reference (CaMeL-style capability
checks) in September 2026; only the tool names were changed for this project.
"""
from typing import Any

EGRESS_TOOLS = {"send_email", "post_webhook"}
EGRESS_ARGS = {"to", "url", "body"}
MIN_TAINT_LENGTH = 8   # shorter tainted values match exactly only; set it per domain


def capability_gate(tool: Any, args: dict[str, Any], tool_context: Any) -> dict | None:
    state = tool_context.state
    plan = state.get("plan:allowed_tools")          # written by the planner step, not by the model turn
    if plan is not None and tool.name not in plan:
        return {"status": "error", "error_message": f"{tool.name} is not in the approved plan",
                "hint": "Ask the user to restart with a plan that includes this step."}
    if tool.name not in EGRESS_TOOLS:
        return None
    # The labeller stores values extracted from untrusted results (addresses, URLs, account ids),
    # not whole chunks, so a short destination embedded inside a long chunk still matches.
    tainted = set(state.get("taint:untrusted_fields", []))
    for key in EGRESS_ARGS & set(args):
        value = str(args[key])
        if value in tainted or any(len(t) >= MIN_TAINT_LENGTH and t in value for t in tainted):
            return {"status": "error", "error_message": "argument derived from untrusted content",
                    "hint": "Only values entered by the user may be sent externally."}
    allowed_destinations = state.get("policy:egress_allowlist", [])
    for key in ("to", "url"):
        if key in args and args[key] not in allowed_destinations:
            return {"status": "error", "error_message": "destination not in allowlist", "hint": "none"}
    return None
