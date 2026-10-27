"""Consent, review and erasure outside the chat: `python -m fieldline.memory_admin <command> <user_id>`.

This is the deterministic path the app settings screen (or a support runbook acting on the engineer's request)
calls. The model has no tool for it. user_id must come from the authenticated caller, never from free text.
Commands: grant | withdraw (stops memory and erases everything) | list | sweep (retry writes/erases, expire).
"""
from __future__ import annotations

import asyncio
import json
import sys

from fieldline.memory_governor import MemoryGovernor


async def run(governor: MemoryGovernor, command: str, user_id: str | None) -> dict:
    if command == "sweep":
        await governor.sweep_all()
        return {"status": "ok"}
    if not user_id:
        return {"status": "error", "message": "user_id required"}
    if command == "grant":
        ok = governor.grant_consent(user_id)
        return {"status": "granted" if ok else "blocked_erasure_in_progress"}
    if command == "withdraw":
        return {"status": "withdrawn", **await governor.withdraw_consent(user_id)}
    if command == "list":
        return {"status": "ok", "consent": governor.ledger.consent_record(user_id),
                "memories": governor.list_memories(user_id)}
    return {"status": "error", "message": f"unknown command {command}"}


if __name__ == "__main__":
    from fieldline.services import governor

    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    print(json.dumps(asyncio.run(run(governor(), cmd, sys.argv[2] if len(sys.argv) > 2 else None)), indent=2))
