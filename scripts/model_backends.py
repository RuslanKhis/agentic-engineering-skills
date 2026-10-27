"""Model calls shared by the evaluation runners. Standard library only.

Two text backends: ``claude-cli`` (headless ``claude -p`` using the local Claude
Code login, run in an empty directory with tools, skills, settings, MCP servers
and project instructions switched off) and ``anthropic`` (the Messages API over
urllib with ``ANTHROPIC_API_KEY``). Both return the same ``ModelReply``.
Nothing here runs at import time and the tests never call either backend.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
import time
import urllib.error
import urllib.request

DEFAULT_MODEL = "claude-sonnet-5-5"
KNOWN_MODELS = ("claude-sonnet-5-5", "claude-opus-5-5", "claude-haiku-5-5")
API_URL = "https://api.anthropic.com/v1/messages"
API_VERSION = "2023-06-01"
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


def call_anthropic(prompt: str, system: str, model: str, timeout: float = 600,
                   api_key: str | None = None, max_tokens: int = 16000,
                   opener=urllib.request.urlopen, attempts: int = 4) -> ModelReply:
    key = api_key or os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        raise BackendError("ANTHROPIC_API_KEY is not set")
    body = json.dumps({"model": model, "max_tokens": max_tokens, "system": system,
                       "messages": [{"role": "user", "content": prompt}]}).encode()
    headers = {"content-type": "application/json", "x-api-key": key,
               "anthropic-version": API_VERSION}
    started = time.monotonic()
    for attempt in range(1, attempts + 1):
        request = urllib.request.Request(API_URL, data=body, headers=headers, method="POST")
        try:
            with opener(request, timeout=timeout) as response:
                data = json.loads(response.read().decode())
            break
        except urllib.error.HTTPError as exc:
            retryable = exc.code == 429 or exc.code >= 500
            if not retryable or attempt == attempts:
                detail = exc.read().decode(errors="replace")[:300] if exc.fp else ""
                raise BackendError(f"Messages API HTTP {exc.code}: {detail}") from exc
            wait = exc.headers.get("retry-after") if exc.headers else None
            time.sleep(min(float(wait), 60) if wait and wait.isdigit() else 2 ** attempt)
        except (urllib.error.URLError, TimeoutError) as exc:
            if attempt == attempts:
                raise BackendError(f"Messages API unreachable: {exc}") from exc
            time.sleep(2 ** attempt)
    if data.get("stop_reason") == "refusal":
        raise BackendError("the model declined the request (stop_reason refusal)")
    text = "".join(block.get("text", "") for block in data.get("content", [])
                   if block.get("type") == "text")
    return ModelReply(text=text, model=data.get("model", model), usage=data.get("usage") or {},
                      duration_s=round(time.monotonic() - started, 1))


def call_model(backend: str, prompt: str, system: str, model: str, timeout: float = 600) -> ModelReply:
    if backend == "claude-cli":
        return call_claude_cli(prompt, system, model, timeout)
    if backend == "anthropic":
        return call_anthropic(prompt, system, model, timeout)
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
