#!/usr/bin/env python3
"""Inventory the tools and resources a live MCP server advertises, then pin them.

Speaks MCP JSON-RPC directly with the standard library: a stdio subprocess
(``--command``) or a Streamable HTTP endpoint (``--url``). Performs the SDK 1.x
``initialize`` handshake and falls back to the 2026-07-28 revision's
``server/discover`` when a server rejects ``initialize``. Lists ``tools/list``
and ``resources/list``, records each tool's name, input-schema hash,
description hash, output-schema presence and annotations, writes an optional
pinned manifest, diffs against a prior manifest (added, removed and changed
definitions are the rug-pull signal), flags name collisions across sources,
tools without an ``outputSchema``, and descriptions carrying imperative phrases
or markers (a labelled heuristic, never a verdict).

Read-only toward the server: it never calls ``tools/call`` or reads a resource.
Non-loopback URLs are refused unless ``--allow-remote`` is given. Exit 0 when
every source was inspected, 1 when at least one source failed (``partial``),
2 for bad arguments.
"""

from __future__ import annotations

import argparse
import hashlib
import ipaddress
import json
import os
from pathlib import Path
import queue
import re
import shlex
import subprocess
import sys
import threading
import time
from urllib import error as urlerror
from urllib import request as urlrequest
from urllib.parse import urlsplit


CLIENT_INFO = {"name": "adk-agent-interoperability-inventory", "version": "1.0"}
DEFAULT_PROTOCOL_VERSION = "2025-06-18"
PROTOCOL_META_PREFIX = "io.modelcontextprotocol/"
RESERVED_ADK_TOOL_NAMES = {"adk_request_credential", "adk_request_confirmation",
                           "adk_request_input", "transfer_to_agent"}
METHOD_NOT_FOUND = -32601
UNSUPPORTED_PROTOCOL_CODES = {-32004, -32022}
MAX_PAGES = 20
NAME_PATTERN = re.compile(r"^[A-Za-z0-9_.-]{1,128}$")
IMPERATIVE_PATTERNS = [
    (re.compile(r"\bignore (all |any )?(previous|prior|above|earlier) (instructions|messages|rules)", re.I),
     "ignore previous instructions"),
    (re.compile(r"\b(you must|you should|always|never) (call|use|invoke|run|read|send|include)\b", re.I),
     "directive aimed at the model"),
    (re.compile(r"\b(before|after) (calling|using|invoking) (this|any|another|other) tools?\b", re.I),
     "cross-tool sequencing instruction"),
    (re.compile(r"\b(also|first|then) (call|read|send|include|pass)\b", re.I), "chained action instruction"),
    (re.compile(r"\b(do not|don't|never) (tell|mention|reveal|show|inform) (the )?user\b", re.I),
     "concealment instruction"),
    (re.compile(r"</?(important|system|instructions?|hidden|secret)>", re.I), "pseudo-markup marker"),
    (re.compile(r"\b(IMPORTANT|SYSTEM|NOTE TO (THE )?(MODEL|ASSISTANT|AI))\s*:", re.I), "attention marker"),
    (re.compile(r"\bsystem prompt\b", re.I), "system prompt reference"),
    (re.compile(r"(~/\.ssh|id_rsa|id_ed25519|\.env\b|\.netrc|credentials\.json|/etc/passwd)", re.I),
     "sensitive file path"),
    (re.compile(r"\b(api[_ -]?key|password|secret|token)s?\b.*\b(pass|send|include|provide|put)\b", re.I),
     "secret exfiltration phrasing"),
    (re.compile(r"[​‌‍⁠﻿­]"), "zero-width or invisible character"),
]
DESCRIPTION_LENGTH_LIMIT = 1500


def canonical_hash(value) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"),
                                     ensure_ascii=False).encode("utf-8")).hexdigest()


def positive(value):
    try:
        number = float(value)
    except ValueError:
        raise argparse.ArgumentTypeError("must be a positive number") from None
    if number <= 0:
        raise argparse.ArgumentTypeError("must be a positive number")
    return number


def is_loopback_host(hostname: str | None) -> bool:
    if not hostname:
        return False
    host = hostname.strip("[]").lower()
    if host == "localhost" or host.endswith(".localhost"):
        return True
    try:
        return ipaddress.ip_address(host).is_loopback
    except ValueError:
        return False


class TransportError(Exception):
    """Raised when the server could not be reached or answered outside the protocol."""


class NoRedirect(urlrequest.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):  # noqa: D401
        raise TransportError(f"refusing to follow redirect ({code}) to {newurl}")


class StdioTransport:
    """Newline-delimited JSON-RPC over a child process's stdin and stdout."""

    def __init__(self, command: str, timeout: float, max_bytes: int):
        self.argv = shlex.split(command)
        if not self.argv:
            raise TransportError("empty command")
        self.timeout = timeout
        self.max_bytes = max_bytes
        self.process = None
        self.lines: queue.Queue = queue.Queue()
        self.stderr_tail: list[str] = []

    def open(self) -> None:
        try:
            self.process = subprocess.Popen(  # noqa: S603 - command supplied by the operator on purpose
                self.argv, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                text=True, encoding="utf-8", errors="replace", bufsize=1)
        except OSError as exc:
            raise TransportError(f"cannot start command: {exc}") from exc
        threading.Thread(target=self._pump, args=(self.process.stdout, self.lines), daemon=True).start()
        threading.Thread(target=self._pump_stderr, daemon=True).start()

    def _pump(self, stream, sink):
        try:
            for line in stream:
                if len(line) > self.max_bytes:
                    sink.put(("oversize", len(line)))
                    continue
                sink.put(("line", line))
        finally:
            sink.put(("eof", None))

    def _pump_stderr(self):
        try:
            for line in self.process.stderr:
                if len(self.stderr_tail) < 20:
                    self.stderr_tail.append(line.rstrip()[:300])
        except ValueError:
            pass

    def send(self, message: dict) -> None:
        try:
            self.process.stdin.write(json.dumps(message, separators=(",", ":")) + "\n")
            self.process.stdin.flush()
        except (OSError, ValueError) as exc:
            raise TransportError(f"cannot write to server: {exc}") from exc

    def receive(self, expect_id):
        """Return the response for ``expect_id``; answers stray server requests with an error."""
        deadline = time.monotonic() + self.timeout
        while True:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise TransportError(f"timed out after {self.timeout}s waiting for response id {expect_id}")
            try:
                kind, payload = self.lines.get(timeout=remaining)
            except queue.Empty:
                raise TransportError(f"timed out after {self.timeout}s waiting for response id {expect_id}") from None
            if kind == "eof":
                raise TransportError("server closed stdout before answering; stderr: " + " | ".join(self.stderr_tail))
            if kind == "oversize":
                raise TransportError(f"server line exceeded {self.max_bytes} bytes")
            text = payload.strip()
            if not text:
                continue
            try:
                message = json.loads(text)
            except ValueError as exc:
                raise TransportError(f"server wrote a line that is not JSON: {text[:120]!r}") from exc
            if not isinstance(message, dict):
                raise TransportError("server wrote a JSON value that is not an object")
            if "method" in message and "id" in message:
                self.send({"jsonrpc": "2.0", "id": message["id"],
                           "error": {"code": METHOD_NOT_FOUND, "message": "inventory client answers no requests"}})
                continue
            if "method" in message:
                continue  # notification
            if message.get("id") == expect_id:
                return message

    def close(self) -> None:
        if self.process is None:
            return
        try:
            self.process.stdin.close()
        except OSError:
            pass
        try:
            self.process.wait(timeout=2)
        except subprocess.TimeoutExpired:
            self.process.kill()
            try:
                self.process.wait(timeout=2)
            except subprocess.TimeoutExpired:
                pass


class HttpTransport:
    """Streamable HTTP: JSON-RPC over POST, JSON or SSE responses, optional Mcp-Session-Id."""

    def __init__(self, url: str, headers: dict[str, str], timeout: float, max_bytes: int):
        self.url = url
        self.base_headers = dict(headers)
        self.timeout = timeout
        self.max_bytes = max_bytes
        self.session_id: str | None = None
        self.protocol_version: str | None = None
        self.opener = urlrequest.build_opener(NoRedirect)

    def open(self) -> None:
        return None

    def _headers(self) -> dict[str, str]:
        headers = {"Content-Type": "application/json", "Accept": "application/json, text/event-stream"}
        headers.update(self.base_headers)
        if self.session_id:
            headers["Mcp-Session-Id"] = self.session_id
        if self.protocol_version:
            headers["MCP-Protocol-Version"] = self.protocol_version
        return headers

    def post(self, message: dict):
        body = json.dumps(message, separators=(",", ":")).encode("utf-8")
        req = urlrequest.Request(self.url, data=body, headers=self._headers(), method="POST")
        try:
            with self.opener.open(req, timeout=self.timeout) as response:
                session_id = response.headers.get("Mcp-Session-Id")
                if session_id:
                    self.session_id = session_id
                content_type = (response.headers.get("Content-Type") or "").lower()
                raw = response.read(self.max_bytes + 1)
        except urlerror.HTTPError as exc:
            detail = exc.read(300).decode("utf-8", "replace") if exc.fp else ""
            raise TransportError(f"HTTP {exc.code} from server: {detail.strip()[:200]}") from exc
        except (urlerror.URLError, OSError, ValueError) as exc:
            raise TransportError(f"cannot reach server: {exc}") from exc
        if len(raw) > self.max_bytes:
            raise TransportError(f"response exceeded {self.max_bytes} bytes")
        return content_type, raw.decode("utf-8", "replace")

    def send(self, message: dict) -> None:
        """Send a notification; servers answer 202 (or 200) with no body."""
        self.post(message)

    def request(self, message: dict):
        content_type, text = self.post(message)
        if "text/event-stream" in content_type:
            for data in self._sse_payloads(text):
                try:
                    parsed = json.loads(data)
                except ValueError as exc:
                    raise TransportError(f"SSE data is not JSON: {data[:120]!r}") from exc
                if isinstance(parsed, dict) and parsed.get("id") == message["id"] and "method" not in parsed:
                    return parsed
            raise TransportError(f"SSE stream ended without a response for id {message['id']}")
        if not text.strip():
            raise TransportError("empty body where a JSON-RPC response was expected")
        try:
            parsed = json.loads(text)
        except ValueError as exc:
            raise TransportError(f"response body is not JSON: {text[:120]!r}") from exc
        if not isinstance(parsed, dict) or parsed.get("id") != message["id"]:
            raise TransportError("response is not the JSON-RPC reply to this request")
        return parsed

    @staticmethod
    def _sse_payloads(text: str):
        data_lines: list[str] = []
        for line in text.splitlines() + [""]:
            if line == "":
                if data_lines:
                    yield "\n".join(data_lines)
                    data_lines = []
                continue
            if line.startswith("data:"):
                data_lines.append(line[5:].lstrip())

    def close(self) -> None:
        if self.session_id:
            try:
                req = urlrequest.Request(self.url, headers=self._headers(), method="DELETE")
                self.opener.open(req, timeout=min(self.timeout, 5)).close()
            except Exception:  # noqa: BLE001 - best-effort session termination
                pass


class McpClient:
    """Minimal JSON-RPC client that knows the initialize and server/discover handshakes."""

    def __init__(self, transport, protocol_version: str):
        self.transport = transport
        self.requested_version = protocol_version
        self.negotiated_version: str | None = None
        self.handshake: str | None = None
        self.server_info = None
        self.server_capabilities = None
        self._next_id = 0

    def _call(self, method: str, params: dict | None = None):
        self._next_id += 1
        message = {"jsonrpc": "2.0", "id": self._next_id, "method": method, "params": params or {}}
        if self.handshake == "server/discover":
            meta = message["params"].setdefault("_meta", {})
            meta[PROTOCOL_META_PREFIX + "protocolVersion"] = self.negotiated_version or self.requested_version
            meta[PROTOCOL_META_PREFIX + "clientInfo"] = CLIENT_INFO
            meta[PROTOCOL_META_PREFIX + "clientCapabilities"] = {}
        if isinstance(self.transport, HttpTransport):
            response = self.transport.request(message)
        else:
            self.transport.send(message)
            response = self.transport.receive(self._next_id)
        return response

    def _result(self, response: dict, method: str) -> dict:
        if "error" in response:
            err = response["error"] if isinstance(response["error"], dict) else {"message": str(response["error"])}
            raise ProtocolError(method, err.get("code"), str(err.get("message", "")))
        result = response.get("result")
        if not isinstance(result, dict):
            raise TransportError(f"{method} returned no result object")
        return result

    def connect(self) -> None:
        params = {"protocolVersion": self.requested_version, "capabilities": {}, "clientInfo": CLIENT_INFO}
        try:
            result = self._result(self._call("initialize", params), "initialize")
        except ProtocolError as exc:
            if exc.code == METHOD_NOT_FOUND or exc.code in UNSUPPORTED_PROTOCOL_CODES:
                self._discover()
                return
            raise
        self.handshake = "initialize"
        self.negotiated_version = result.get("protocolVersion")
        self.server_info = result.get("serverInfo")
        self.server_capabilities = result.get("capabilities")
        if isinstance(self.transport, HttpTransport) and isinstance(self.negotiated_version, str):
            self.transport.protocol_version = self.negotiated_version
        notification = {"jsonrpc": "2.0", "method": "notifications/initialized"}
        self.transport.send(notification)

    def _discover(self) -> None:
        self.handshake = "server/discover"
        result = self._result(self._call("server/discover"), "server/discover")
        versions = result.get("protocolVersions") or result.get("supportedProtocolVersions") or []
        if isinstance(versions, list) and versions:
            self.negotiated_version = str(sorted(str(v) for v in versions)[-1])
        self.server_info = result.get("serverInfo")
        self.server_capabilities = result.get("capabilities")
        if isinstance(self.transport, HttpTransport) and self.negotiated_version:
            self.transport.protocol_version = self.negotiated_version

    def list_all(self, method: str, key: str):
        items: list = []
        cursor = None
        last_result: dict = {}
        for _ in range(MAX_PAGES):
            params = {"cursor": cursor} if cursor else {}
            last_result = self._result(self._call(method, params), method)
            page = last_result.get(key)
            if not isinstance(page, list):
                raise TransportError(f"{method} result has no {key!r} list")
            items.extend(page)
            cursor = last_result.get("nextCursor")
            if not cursor:
                break
        return items, last_result


class ProtocolError(Exception):
    def __init__(self, method: str, code, message: str):
        super().__init__(f"{method} failed with JSON-RPC error {code}: {message}")
        self.method = method
        self.code = code


def field(mapping: dict, *names, default=None):
    for name in names:
        if name in mapping:
            return mapping[name]
    return default


def describe_tool(raw: dict) -> dict:
    name = raw.get("name")
    description = raw.get("description") or ""
    input_schema = field(raw, "inputSchema", "input_schema", default={})
    output_schema = field(raw, "outputSchema", "output_schema")
    annotations = raw.get("annotations") if isinstance(raw.get("annotations"), dict) else {}
    meta = field(raw, "_meta", "meta", default=None)
    return {
        "name": name if isinstance(name, str) else str(name),
        "title": raw.get("title") if isinstance(raw.get("title"), str) else None,
        "description_sha256": canonical_hash(description),
        "description_length": len(description),
        "input_schema_sha256": canonical_hash(input_schema if input_schema is not None else {}),
        "output_schema_sha256": canonical_hash(output_schema) if output_schema is not None else None,
        "has_output_schema": output_schema is not None,
        "annotations": {k: annotations[k] for k in sorted(annotations)},
        "has_meta": meta is not None,
        "ui_resource_uri": (meta.get("ui", {}) or {}).get("resourceUri") if isinstance(meta, dict)
        and isinstance(meta.get("ui"), dict) else None,
    }


def description_findings(source: str, tool_name: str, description: str, where: str) -> list[dict]:
    findings = []
    for pattern, label in IMPERATIVE_PATTERNS:
        match = pattern.search(description)
        if match:
            findings.append({"source": source, "tool": tool_name, "code": "description_imperative_phrase",
                             "level": "review", "heuristic": True,
                             "message": f"{where} contains {label}: {match.group(0)[:60]!r}; read it as an attacker would"})
    if len(description) > DESCRIPTION_LENGTH_LIMIT:
        findings.append({"source": source, "tool": tool_name, "code": "description_long", "level": "review",
                         "heuristic": True,
                         "message": f"{where} is {len(description)} characters; long descriptions hide instructions and cost context"})
    return findings


def inspect_source(kind: str, target: str, args, headers: dict[str, str]) -> dict:
    entry = {"kind": kind, "target": target, "status": "inspected", "handshake": None,
             "protocol_version": None, "server_info": None, "server_capabilities": None,
             "session_id_issued": False, "tools": [], "resources": [], "list_result_ttl_ms": None,
             "list_result_cache_scope": None, "error": None}
    if kind == "stdio":
        transport = StdioTransport(target, args.timeout, args.max_bytes)
    else:
        transport = HttpTransport(target, headers, args.timeout, args.max_bytes)
    client = McpClient(transport, args.protocol_version)
    findings: list[dict] = []
    try:
        transport.open()
        client.connect()
        entry["handshake"] = client.handshake
        entry["protocol_version"] = client.negotiated_version
        entry["server_info"] = client.server_info
        entry["server_capabilities"] = client.server_capabilities
        if isinstance(transport, HttpTransport):
            entry["session_id_issued"] = transport.session_id is not None
        capabilities = client.server_capabilities if isinstance(client.server_capabilities, dict) else {}
        tools_capability = capabilities.get("tools") if isinstance(capabilities.get("tools"), dict) else {}
        if tools_capability.get("listChanged"):
            findings.append({"source": target, "tool": "-", "code": "server_list_changed_unsubscribed",
                             "level": "info", "heuristic": False,
                             "message": "server advertises notifications/tools/list_changed; ADK 2.8.0 McpToolset does not subscribe,"
                                        " so a changed tool list is seen only when tool_list_cache_ttl_seconds expires or on the next get_tools()"})
        raw_tools, last = client.list_all("tools/list", "tools")
        entry["list_result_ttl_ms"] = last.get("ttlMs")
        entry["list_result_cache_scope"] = last.get("cacheScope")
        for raw in raw_tools:
            if not isinstance(raw, dict) or not isinstance(raw.get("name"), str):
                raise TransportError("tools/list returned a tool without a string name")
            tool = describe_tool(raw)
            entry["tools"].append(tool)
            findings.extend(tool_findings(target, raw, tool))
        if not args.no_resources:
            try:
                raw_resources, _ = client.list_all("resources/list", "resources")
                for raw in raw_resources:
                    if isinstance(raw, dict):
                        entry["resources"].append({"name": raw.get("name"), "uri": raw.get("uri"),
                                                   "mime_type": field(raw, "mimeType", "mime_type")})
            except ProtocolError as exc:
                entry["resources_error"] = str(exc)
        entry["tools"].sort(key=lambda t: t["name"])
        entry["resources"].sort(key=lambda r: (str(r.get("name")), str(r.get("uri"))))
    except (TransportError, ProtocolError) as exc:
        entry["status"] = "failed"
        entry["error"] = str(exc)
    finally:
        transport.close()
    entry["findings"] = findings
    return entry


def tool_findings(source: str, raw: dict, tool: dict) -> list[dict]:
    findings = []
    name = tool["name"]
    if not NAME_PATTERN.match(name):
        findings.append({"source": source, "tool": name, "code": "tool_name_not_identifier", "level": "review",
                         "heuristic": False, "message": "tool name has characters outside [A-Za-z0-9_.-]"})
    if name in RESERVED_ADK_TOOL_NAMES:
        findings.append({"source": source, "tool": name, "code": "reserved_adk_tool_name", "level": "error",
                         "heuristic": False,
                         "message": "ADK 2.8.0 McpToolset skips this name (collides with a framework tool)"})
    if not tool["has_output_schema"]:
        findings.append({"source": source, "tool": name, "code": "tool_without_output_schema", "level": "info",
                         "heuristic": False,
                         "message": "no outputSchema; the client cannot validate structured results against a contract"})
    annotations = tool["annotations"]
    if annotations:
        hints = ", ".join(f"{k}={annotations[k]}" for k in sorted(annotations))
        findings.append({"source": source, "tool": name, "code": "annotations_are_hints", "level": "info",
                         "heuristic": False,
                         "message": f"annotations ({hints}) are server-supplied hints; do not derive tool tier or confirmation policy from them"})
    findings.extend(description_findings(source, name, raw.get("description") or "", "tool description"))
    schema = field(raw, "inputSchema", "input_schema", default={})
    if isinstance(schema, dict):
        for prop_name, prop in (schema.get("properties") or {}).items():
            if isinstance(prop, dict) and isinstance(prop.get("description"), str):
                findings.extend(description_findings(source, name, prop["description"],
                                                     f"parameter {prop_name!r} description"))
    if tool["ui_resource_uri"]:
        findings.append({"source": source, "tool": name, "code": "mcp_app_ui_resource", "level": "info",
                         "heuristic": False,
                         "message": f"declares an MCP App UI resource {tool['ui_resource_uri']}; ADK 2.8.0 renders it as a UiWidget"})
    return findings


def build_manifest(sources: list[dict]) -> dict:
    tools = {}
    for source in sources:
        if source["status"] != "inspected":
            continue
        for tool in source["tools"]:
            key = f"{source['target']}::{tool['name']}"
            tools[key] = {"source": source["target"], "name": tool["name"],
                          "description_sha256": tool["description_sha256"],
                          "input_schema_sha256": tool["input_schema_sha256"],
                          "output_schema_sha256": tool["output_schema_sha256"],
                          "annotations": tool["annotations"]}
    return {"manifest_version": 1, "tools": dict(sorted(tools.items()))}


def diff_manifests(prior: dict, current: dict) -> dict:
    prior_tools = prior.get("tools") if isinstance(prior.get("tools"), dict) else {}
    current_tools = current["tools"]
    added = sorted(set(current_tools) - set(prior_tools))
    removed = sorted(set(prior_tools) - set(current_tools))
    changed = []
    for key in sorted(set(current_tools) & set(prior_tools)):
        before, after = prior_tools[key], current_tools[key]
        fields = [f for f in ("description_sha256", "input_schema_sha256", "output_schema_sha256", "annotations")
                  if before.get(f) != after.get(f)]
        if fields:
            changed.append({"tool": key, "fields": fields})
    return {"added": added, "removed": removed, "changed": changed,
            "rug_pull_signal": bool(added or removed or changed)}


def collision_findings(sources: list[dict]) -> list[dict]:
    seen: dict[str, list[str]] = {}
    for source in sources:
        for tool in source["tools"]:
            seen.setdefault(tool["name"], []).append(source["target"])
    findings = []
    for name, targets in sorted(seen.items()):
        if len(targets) > 1:
            findings.append({"source": " | ".join(targets), "tool": name, "code": "tool_name_collision",
                             "level": "review", "heuristic": False,
                             "message": "same tool name from several servers; set tool_name_prefix on each McpToolset"})
    return findings


def parse_headers(values: list[str], parser) -> dict[str, str]:
    headers = {}
    for item in values:
        if "=" not in item:
            parser.error(f"--header expects KEY=VALUE, got {item!r}")
        key, value = item.split("=", 1)
        if not key.strip():
            parser.error("--header key must not be empty")
        headers[key.strip()] = value
    return headers


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Lists only; never calls a tool or reads a resource. Description findings are heuristics.")
    parser.add_argument("--command", action="append", default=[], metavar="CMD",
                        help="stdio MCP server command line (repeatable); runs the command you give it")
    parser.add_argument("--url", action="append", default=[], metavar="URL",
                        help="Streamable HTTP MCP endpoint (repeatable); loopback only unless --allow-remote")
    parser.add_argument("--header", action="append", default=[], metavar="K=V",
                        help="HTTP header for every --url source (repeatable); values are not printed")
    parser.add_argument("--out", type=Path, metavar="MANIFEST", help="write the pinned manifest JSON here")
    parser.add_argument("--diff", type=Path, metavar="PRIOR_MANIFEST", help="compare against a prior manifest")
    parser.add_argument("--allow-remote", action="store_true", help="permit non-loopback --url hosts")
    parser.add_argument("--timeout", type=positive, default=20.0, help="seconds per request (default: 20)")
    parser.add_argument("--max-bytes", type=int, default=4_000_000, help="maximum response size (default: 4000000)")
    parser.add_argument("--protocol-version", default=DEFAULT_PROTOCOL_VERSION,
                        help=f"protocolVersion offered in initialize (default: {DEFAULT_PROTOCOL_VERSION})")
    parser.add_argument("--no-resources", action="store_true", help="skip resources/list")
    args = parser.parse_args(argv)

    if not args.command and not args.url:
        parser.error("give at least one --command or --url")
    if args.max_bytes < 1024:
        parser.error("--max-bytes must be at least 1024")
    headers = parse_headers(args.header, parser)
    for url in args.url:
        parts = urlsplit(url)
        if parts.scheme not in {"http", "https"} or not parts.hostname:
            parser.error(f"--url must be an http(s) URL with a host: {url!r}")
        if not is_loopback_host(parts.hostname) and not args.allow_remote:
            parser.error(f"{url!r} is not a loopback host; pass --allow-remote after the owner approves the connection")
    prior = None
    if args.diff is not None:
        try:
            prior = json.loads(args.diff.read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            parser.error(f"cannot read prior manifest {args.diff}: {exc}")
        if not isinstance(prior, dict):
            parser.error("prior manifest must be a JSON object")

    sources = [inspect_source("stdio", command, args, {}) for command in args.command]
    sources += [inspect_source("http", url, args, headers) for url in args.url]
    findings = [f for source in sources for f in source.pop("findings")]
    findings.extend(collision_findings(sources))
    manifest = build_manifest(sources)
    manifest_written = None
    if args.out is not None:
        try:
            args.out.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
            manifest_written = str(args.out)
        except OSError as exc:
            findings.append({"source": "-", "tool": "-", "code": "manifest_write_failed", "level": "error",
                             "heuristic": False, "message": str(exc)})
    codes = sorted({f["code"] for f in findings})
    result = {
        "sources": sources,
        "findings": findings,
        "diff": diff_manifests(prior, manifest) if prior is not None else None,
        "manifest_written": manifest_written,
        "counts": {"sources": len(sources), "inspected": sum(s["status"] == "inspected" for s in sources),
                   "tools": sum(len(s["tools"]) for s in sources),
                   "resources": sum(len(s["resources"]) for s in sources),
                   "findings": len(findings),
                   "by_code": {code: sum(1 for f in findings if f["code"] == code) for code in codes}},
        "partial": any(s["status"] != "inspected" for s in sources)
        or (args.out is not None and manifest_written is None),
        "notes": ["Hashes are SHA-256 of canonical JSON; compare manifests across time to detect changed definitions.",
                  "description_imperative_phrase and description_long are heuristics; a clean result is not a clearance.",
                  "ADK 2.8.0 pins mcp>=1.24,<2 (SDK 1.x); the initialize handshake is its contract. server/discover support here is best effort."],
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 1 if result["partial"] else 0


if __name__ == "__main__":
    os.environ.setdefault("PYTHONDONTWRITEBYTECODE", "1")
    raise SystemExit(main())
