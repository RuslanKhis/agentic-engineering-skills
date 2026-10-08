"""Exercise the MCP inventory through its CLI against fake stdio and loopback HTTP servers."""

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import shlex
import subprocess
import sys
import tempfile
import threading
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "mcp_tool_inventory.py"
FAKE_STDIO = Path(__file__).resolve().parent / "fixtures" / "fake_mcp_stdio_server.py"
HTTP_TOOLS = [
    {"name": "search", "description": "Search the catalogue.",
     "inputSchema": {"type": "object", "properties": {"q": {"type": "string"}}},
     "outputSchema": {"type": "object"}},
    {"name": "read_file", "description": "Read a file from the remote store.",
     "inputSchema": {"type": "object", "properties": {"path": {"type": "string"}}}},
]


def stdio_command(mode="normal"):
    return f"{shlex.quote(sys.executable)} -I {shlex.quote(str(FAKE_STDIO))} {mode}"


def run(*args):
    completed = subprocess.run([sys.executable, "-I", "-B", str(SCRIPT), *args],
                               capture_output=True, text=True, timeout=120)
    payload = json.loads(completed.stdout) if completed.stdout.strip().startswith("{") else None
    return completed.returncode, payload, completed.stderr


class Handler(BaseHTTPRequestHandler):
    mode = "json"
    seen_headers = []

    def log_message(self, *_):
        return

    def _reply(self, status, body, content_type="application/json", extra=None):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        for key, value in (extra or {}).items():
            self.send_header(key, value)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        length = int(self.headers.get("Content-Length") or 0)
        message = json.loads(self.rfile.read(length) or b"{}")
        type(self).seen_headers.append({k.lower(): v for k, v in self.headers.items()})
        method = message.get("method")
        if method == "notifications/initialized":
            self._reply(202, b"")
            return
        if self.mode == "malformed":
            self._reply(200, b"<html>not json</html>", "text/html")
            return
        if method == "initialize":
            result = {"protocolVersion": "2025-06-18", "capabilities": {"tools": {}},
                      "serverInfo": {"name": "fake-http", "version": "1"}}
            extra = {"Mcp-Session-Id": "sess-123"}
        elif method == "tools/list":
            result = {"tools": HTTP_TOOLS, "ttlMs": 60000, "cacheScope": "private"}
            extra = None
        elif method == "resources/list":
            result = {"resources": []}
            extra = None
        else:
            body = json.dumps({"jsonrpc": "2.0", "id": message.get("id"),
                               "error": {"code": -32601, "message": "Method not found"}}).encode()
            self._reply(200, body)
            return
        reply = {"jsonrpc": "2.0", "id": message.get("id"), "result": result}
        if self.mode == "sse":
            body = ("event: message\ndata: " + json.dumps(reply) + "\n\n").encode()
            self._reply(200, body, "text/event-stream", extra)
        else:
            self._reply(200, json.dumps(reply).encode(), extra=extra)

    def do_DELETE(self):
        self._reply(200, b"")


class LoopbackServer:
    def __init__(self, mode):
        handler = type("ModeHandler", (Handler,), {"mode": mode, "seen_headers": []})
        self.handler = handler
        self.server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)

    def __enter__(self):
        self.thread.start()
        return self

    @property
    def url(self):
        return f"http://127.0.0.1:{self.server.server_address[1]}/mcp"

    def __exit__(self, *exc):
        self.server.shutdown()
        self.server.server_close()


class StdioTests(unittest.TestCase):
    def test_lists_tools_across_pages_and_resources(self):
        code, payload, stderr = run("--command", stdio_command())
        self.assertEqual(code, 0, stderr)
        source = payload["sources"][0]
        self.assertEqual(source["status"], "inspected")
        self.assertEqual(source["handshake"], "initialize")
        self.assertEqual([t["name"] for t in source["tools"]], ["read_file", "write_file"])
        self.assertEqual(source["resources"][0]["uri"], "file:///readme")
        self.assertTrue(source["tools"][0]["has_output_schema"])
        self.assertFalse(source["tools"][1]["has_output_schema"])
        codes = payload["counts"]["by_code"]
        self.assertEqual(codes.get("tool_without_output_schema"), 1)
        self.assertEqual(codes.get("annotations_are_hints"), 1)
        self.assertEqual(codes.get("server_list_changed_unsubscribed"), 1)
        self.assertNotIn("description_imperative_phrase", codes)
        self.assertFalse(payload["partial"])

    def test_poisoned_description_and_reserved_name_are_flagged(self):
        code, payload, _ = run("--command", stdio_command("poisoned"), "--no-resources")
        self.assertEqual(code, 0)
        codes = payload["counts"]["by_code"]
        self.assertGreaterEqual(codes.get("description_imperative_phrase", 0), 2)
        self.assertEqual(codes.get("reserved_adk_tool_name"), 1)
        flagged = [f for f in payload["findings"] if f["code"] == "description_imperative_phrase"]
        self.assertTrue(all(f["heuristic"] for f in flagged))
        self.assertTrue(any("id_rsa" in f["message"] or "sensitive" in f["message"] for f in flagged))

    def test_server_discover_fallback(self):
        code, payload, stderr = run("--command", stdio_command("discover"), "--no-resources")
        self.assertEqual(code, 0, stderr)
        source = payload["sources"][0]
        self.assertEqual(source["handshake"], "server/discover")
        self.assertEqual(source["protocol_version"], "2026-07-28")
        self.assertEqual(len(source["tools"]), 2)

    def test_server_initiated_request_is_refused_and_listing_continues(self):
        code, payload, stderr = run("--command", stdio_command("request"), "--no-resources")
        self.assertEqual(code, 0, stderr)
        self.assertEqual(len(payload["sources"][0]["tools"]), 2)

    def test_malformed_response_is_partial(self):
        code, payload, _ = run("--command", stdio_command("malformed"), "--timeout", "5")
        self.assertEqual(code, 1)
        self.assertTrue(payload["partial"])
        self.assertEqual(payload["sources"][0]["status"], "failed")
        self.assertIn("not JSON", payload["sources"][0]["error"])

    def test_manifest_written_and_diff_reports_rug_pull(self):
        with tempfile.TemporaryDirectory() as tmp:
            manifest = Path(tmp) / "pinned.json"
            code, payload, _ = run("--command", stdio_command(), "--out", str(manifest), "--no-resources")
            self.assertEqual(code, 0)
            self.assertEqual(payload["manifest_written"], str(manifest))
            pinned = json.loads(manifest.read_text())
            self.assertEqual(pinned["manifest_version"], 1)
            self.assertEqual(len(pinned["tools"]), 2)
            # Same server again: no change.
            code, payload, _ = run("--command", stdio_command(), "--diff", str(manifest), "--no-resources")
            self.assertEqual(code, 0)
            self.assertFalse(payload["diff"]["rug_pull_signal"])
            # Poisoned server under the same key: description changed, tool added and removed.
            key = next(iter(pinned["tools"]))
            pinned["tools"][key]["source"] = stdio_command("poisoned")
            rekeyed = {k.replace(stdio_command(), stdio_command("poisoned")): v for k, v in pinned["tools"].items()}
            manifest.write_text(json.dumps({"manifest_version": 1, "tools": rekeyed}))
            code, payload, _ = run("--command", stdio_command("poisoned"), "--diff", str(manifest), "--no-resources")
            self.assertEqual(code, 0)
            diff = payload["diff"]
            self.assertTrue(diff["rug_pull_signal"])
            self.assertEqual(len(diff["changed"]), 1)
            self.assertIn("description_sha256", diff["changed"][0]["fields"])
            self.assertEqual(len(diff["added"]), 1)
            self.assertEqual(len(diff["removed"]), 1)

    def test_output_is_deterministic(self):
        _, first, _ = run("--command", stdio_command(), "--no-resources")
        _, second, _ = run("--command", stdio_command(), "--no-resources")
        self.assertEqual(first, second)


class HttpTests(unittest.TestCase):
    def test_json_transport_with_session_header(self):
        with LoopbackServer("json") as server:
            code, payload, stderr = run("--url", server.url, "--header", "Authorization=Bearer t", "--no-resources")
            self.assertEqual(code, 0, stderr)
            source = payload["sources"][0]
            self.assertEqual(source["status"], "inspected")
            self.assertTrue(source["session_id_issued"])
            self.assertEqual(source["list_result_ttl_ms"], 60000)
            self.assertEqual([t["name"] for t in source["tools"]], ["read_file", "search"])
            later = server.handler.seen_headers[-1]
            self.assertEqual(later.get("mcp-session-id"), "sess-123")
            self.assertEqual(later.get("mcp-protocol-version"), "2025-06-18")
            self.assertEqual(later.get("authorization"), "Bearer t")
            self.assertNotIn("Bearer t", json.dumps(payload))

    def test_sse_transport(self):
        with LoopbackServer("sse") as server:
            code, payload, stderr = run("--url", server.url, "--no-resources")
            self.assertEqual(code, 0, stderr)
            self.assertEqual(len(payload["sources"][0]["tools"]), 2)

    def test_malformed_http_body_is_partial(self):
        with LoopbackServer("malformed") as server:
            code, payload, _ = run("--url", server.url)
            self.assertEqual(code, 1)
            self.assertEqual(payload["sources"][0]["status"], "failed")

    def test_collision_across_sources(self):
        with LoopbackServer("json") as server:
            code, payload, _ = run("--command", stdio_command(), "--url", server.url, "--no-resources")
            self.assertEqual(code, 0)
            collisions = [f for f in payload["findings"] if f["code"] == "tool_name_collision"]
            self.assertEqual([f["tool"] for f in collisions], ["read_file"])

    def test_unreachable_port_is_partial(self):
        code, payload, _ = run("--url", "http://127.0.0.1:9/mcp", "--timeout", "3")
        self.assertEqual(code, 1)
        self.assertTrue(payload["partial"])


class ArgumentTests(unittest.TestCase):
    def test_no_sources_is_bad_args(self):
        code, _, stderr = run()
        self.assertEqual(code, 2)
        self.assertIn("--command or --url", stderr)

    def test_remote_url_refused_without_flag(self):
        code, _, stderr = run("--url", "https://mcp.example.com/mcp")
        self.assertEqual(code, 2)
        self.assertIn("--allow-remote", stderr)

    def test_bad_header_and_scheme(self):
        self.assertEqual(run("--url", "http://127.0.0.1:1/mcp", "--header", "novalue")[0], 2)
        self.assertEqual(run("--url", "ftp://127.0.0.1/mcp")[0], 2)
        self.assertEqual(run("--command", "true", "--diff", "/nonexistent/prior.json")[0], 2)


if __name__ == "__main__":
    unittest.main()
