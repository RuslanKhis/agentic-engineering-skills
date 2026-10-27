"""before_tool_callback: the gates every tool call passes. Imports nothing from ADK."""
from __future__ import annotations

from typing import Any

READ_ONLY = {"search_mail", "read_mail", "list_events", "search_files", "read_file"}


def gate(tool: Any, args: dict, tool_context: Any) -> dict | None:
    state = tool_context.state
    name = tool.name
    if name in READ_ONLY:
        return None
    if name == "send_mail":
        allowed = set(state.get("policy:mail_allowlist", []))
        if args.get("to") not in allowed:
            return {"status": "error", "error_message": "recipient is not on the allow-list"}
        return None
    if name == "share_file":
        domain = str(args.get("email", "")).rsplit("@", 1)[-1]
        if domain not in state.get("policy:share_domains", []):
            return {"status": "error", "error_message": "files can only be shared inside the company"}
        return None
    if name == "create_event":
        return None
    if name == "delete_mail":
        return None
    if name == "pay_invoice":
        if args.get("payee_id") not in state.get("policy:known_payees", []):
            return {"status": "error", "error_message": "unknown payee"}
        paid_today = int(state.get("payments:today_cents", 0))
        cap = int(state.get("policy:daily_payment_cap_cents", 0))
        if paid_today + int(args.get("amount_cents", 0)) > cap:
            return {"status": "error", "error_message": "daily payment cap reached"}
        return None
    return {"status": "error", "error_message": f"no policy covers {name}"}
