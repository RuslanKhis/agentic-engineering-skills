"""Hash MCP tool definitions and compare them with the recorded inventory. Standard library only."""
from __future__ import annotations

import hashlib
import json


def tool_hash(definition: dict) -> str:
    core = {k: definition[k] for k in ("name", "description", "inputSchema") if k in definition}
    return hashlib.sha256(json.dumps(core, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def pinned_tool_filter(recorded: dict, allowed: list[str], log=None):
    """McpToolset tool_filter predicate: admit a tool only if allowlisted and its live definition matches the manifest.

    McpToolset calls the predicate on every get_tools(), so a description changed after deploy is withheld
    from the model until the manifest is re-approved. Fails closed per tool.
    """
    want = {t["name"]: t["sha256"] for t in recorded["tools"]}

    def predicate(tool, readonly_context=None) -> bool:
        if tool.name not in allowed:
            return False
        live = tool.raw_mcp_tool.model_dump(by_alias=True, mode="json", exclude_none=True)
        if want.get(tool.name) != tool_hash(live):
            if log is not None:
                log.warning("MCP tool %r withheld: definition differs from the committed manifest", tool.name)
            return False
        return True

    return predicate


def diff_inventory(recorded: dict, listed: list[dict]) -> list[str]:
    want = {t["name"]: t["sha256"] for t in recorded["tools"]}
    have = {t["name"]: tool_hash(t) for t in listed}
    out = [f"added: {n}" for n in sorted(set(have) - set(want))]
    out += [f"removed: {n}" for n in sorted(set(want) - set(have))]
    out += [f"changed: {n}" for n in sorted(set(want) & set(have)) if want[n] != have[n]]
    return out
