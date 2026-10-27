"""Hash MCP tool definitions and compare them with the recorded manifest. Standard library only."""
from __future__ import annotations

import hashlib
import json


def tool_hash(definition: dict) -> str:
    core = {k: definition[k] for k in ("name", "description", "inputSchema") if k in definition}
    return hashlib.sha256(json.dumps(core, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def diff_manifest(recorded: dict, listed: list[dict]) -> list[str]:
    """Differences between the recorded manifest and the tools a server lists now."""
    want = {t["name"]: t["sha256"] for t in recorded["tools"]}
    have = {t["name"]: tool_hash(t) for t in listed}
    problems = [f"added: {n}" for n in sorted(set(have) - set(want))]
    problems += [f"removed: {n}" for n in sorted(set(want) - set(have))]
    problems += [f"changed: {n}" for n in sorted(set(want) & set(have)) if want[n] != have[n]]
    return problems
