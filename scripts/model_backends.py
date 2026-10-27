"""Model calls shared by the evaluation runners. Standard library only.

One model backend: ``claude-cli`` (headless ``claude -p`` using the local Claude
Code login, run in an empty directory with tools, skills, settings, MCP servers
and project instructions switched off). No API key is used anywhere; the
runners' other backend, ``files``, hands prompts to a person or another agent
and calls no model. Nothing here runs at import time and the tests never call
the model.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile
import time

DEFAULT_MODEL = "claude-sonnet-5-5"
KNOWN_MODELS = ("claude-sonnet-5-5", "claude-opus-5-5", "claude-haiku-5-5")
FENCE = re.compile(r"```(?:json)?\s*(.*?)```", re.DOTALL)


class BackendError(Exception):
    """A model call failed or returned nothing usable."""


@dataclass
class ModelReply:
    text: str
    model: str
    usage: dict = field(default_factory=dict)
    cost_usd: float | None = None
    duration_s: float = 0.0


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_json(value) -> bytes:
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode()


def extract_json(text: str):
    """Return the first JSON object in a model reply, tolerating fences and prose."""
    candidates = [m.group(1) for m in FENCE.finditer(text or "")] + [text or ""]
    for candidate in candidates:
        candidate = candidate.strip()
        try:
            return json.loads(candidate)
        except ValueError:
            pass
        start, end = candidate.find("{"), candidate.rfind("}")
        if 0 <= start < end:
            try:
                return json.loads(candidate[start:end + 1])
            except ValueError:
                pass
    raise BackendError("reply contained no parsable JSON object")


def claude_cli_command(model: str, system: str) -> list[str]:
    """Headless Claude Code with every source of extra context switched off."""
    return ["claude", "-p", "--model", model, "--output-format", "json",
            "--system-prompt", system, "--tools", "", "--safe-mode",
            "--disable-slash-commands", "--no-session-persistence",
            "--strict-mcp-config", "--setting-sources", ""]


def call_claude_cli(prompt: str, system: str, model: str, timeout: float = 600,
                    runner=subprocess.run) -> ModelReply:
    started = time.monotonic()
    with tempfile.TemporaryDirectory(prefix="aes-selector-") as empty:
        try:
            proc = runner(claude_cli_command(model, system), input=prompt, cwd=empty,
                          capture_output=True, text=True, timeout=timeout)
        except FileNotFoundError as exc:
            raise BackendError("the claude command is not on PATH") from exc
        except subprocess.TimeoutExpired as exc:
            raise BackendError(f"claude -p exceeded {timeout:.0f} seconds") from exc
    try:
        data = json.loads(proc.stdout)
    except ValueError as exc:
        raise BackendError(f"claude -p exit {proc.returncode}: {proc.stderr.strip()[:300]}") from exc
    if data.get("is_error") or proc.returncode != 0:
        raise BackendError(f"claude -p reported an error: {str(data.get('result'))[:300]}")
    used = sorted(data.get("modelUsage") or {}) or [model]
    return ModelReply(text=data.get("result") or "", model=",".join(used),
                      usage=data.get("usage") or {}, cost_usd=data.get("total_cost_usd"),
                      duration_s=round(time.monotonic() - started, 1))


def call_model(backend: str, prompt: str, system: str, model: str, timeout: float = 600) -> ModelReply:
    if backend == "claude-cli":
        return call_claude_cli(prompt, system, model, timeout)
    raise BackendError(f"backend {backend!r} does not call a model")


def git_commit(root: Path) -> str | None:
    try:
        proc = subprocess.run(["git", "rev-parse", "HEAD"], cwd=root, capture_output=True,
                              text=True, timeout=10)
    except (OSError, subprocess.TimeoutExpired):
        return None
    if proc.returncode != 0:
        return None
    return proc.stdout.strip() or None
