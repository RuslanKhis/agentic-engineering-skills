"""Hash MCP tool definitions and compare them with the recorded inventory. Standard library only."""
from __future__ import annotations

import hashlib
import json


def tool_hash(definition: dict) -> str:
    core = {k: definition[k] for k in ("name", "description", "inputSchema") if k in definition}
    return hashlib.sha256(json.dumps(core, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def diff_inventory(recorded: dict, listed: list[dict]) -> list[str]:
    want = {t["name"]: t["sha256"] for t in recorded["tools"]}
    have = {t["name"]: tool_hash(t) for t in listed}
    out = [f"added: {n}" for n in sorted(set(have) - set(want))]
    out += [f"removed: {n}" for n in sorted(set(want) - set(have))]
    out += [f"changed: {n}" for n in sorted(set(want) & set(have)) if want[n] != have[n]]
    return out
