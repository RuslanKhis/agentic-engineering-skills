"""Local, standard-library-only fixture; NEVER use its demo auth in production.

The HTTP, ownership, SQLite profile and browser stream are real. The model/ADK
event source is an explicit deterministic double, not a live model invocation.
"""
from __future__ import annotations

import argparse
import json
import sqlite3
import threading
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).parent
UPDATE_PREFERENCE = (
    "INSERT INTO preferences VALUES (?, ?) "
    "ON CONFLICT(owner) DO UPDATE SET language=excluded.language"
)


class Rejected(Exception):
    def __init__(self, status, message):
        self.status, self.message = status, message


class DemoRunner:
    """Deterministic provider double with private/partial/aggregate events."""
    def __init__(self):
        self.calls = 0

    def run(self, *, user_id, session_id, message, language):
        self.calls += 1
        yield {"kind": "thought", "text": "Private reasoning never leaves the server."}
        yield {"kind": "tool", "name": "lookup_order", "status": "complete"}
        answer = ("Tu pedido llega el viernes." if language == "Spanish"
                  else "Your order arrives on Friday.")
        for word in answer.split(" "):
            yield {"kind": "text", "text": word + " "}
        yield {"kind": "aggregate", "text": answer}


class App:
    def __init__(self, database=":memory:", runner=None):
        self.runner = runner or DemoRunner()
        self.db = sqlite3.connect(database, check_same_thread=False)
        self.db.execute("CREATE TABLE IF NOT EXISTS preferences "
                        "(owner TEXT PRIMARY KEY, language TEXT NOT NULL)")
        self.lock = threading.RLock()
        self.sessions = {}
        # Deliberately fake, offline identities. Production supplies its verifier.
        self.tokens = {"demo-alice": "alice", "demo-bob": "bob"}

    def authenticate(self, authorization):
        owner = self.tokens.get(authorization.removeprefix("Bearer "))
        if not authorization.startswith("Bearer ") or owner is None:
            raise Rejected(401, "Sign in to continue.")
        return owner

    def language_for(self, owner):
        with self.lock:
            row = self.db.execute(
                "SELECT language FROM preferences "
                "WHERE owner = ?", (owner,)
            ).fetchone()
        return row[0] if row else "English"

    def remember(self, owner, language, consent):
        if consent is not True:
            raise Rejected(422, "Consent required.")
        with self.lock, self.db:
            self.db.execute(
                UPDATE_PREFERENCE, (owner, language)
            )

    def save_preference(self, owner, body):
        if set(body) != {"language", "consent"}:
            raise Rejected(422, "Provide a language and explicit consent.")
        if body["language"] not in ("English", "Spanish"):
            raise Rejected(422, "Choose English or Spanish.")
        self.remember(owner, body["language"], body["consent"])
        return {"saved": True, "language": body["language"]}

    def forget_preference(self, owner):
        with self.lock, self.db:
            self.db.execute("DELETE FROM preferences WHERE owner = ?", (owner,))
        return {"forgotten": True}

    def prepare_chat(self, owner, body):
        if set(body) - {"message", "session_id"}:
            raise Rejected(422, "Unsupported message fields.")
        message = body.get("message")
        if not isinstance(message, str) or not 1 <= len(message.strip()) <= 2000:
            raise Rejected(422, "Enter a message of 1–2000 characters.")
        session_id = body.get("session_id")
        with self.lock:
            if session_id is None:
                session_id = uuid.uuid4().hex
                self.sessions[session_id] = owner
            elif (not isinstance(session_id, str)
                  or self.sessions.get(session_id) != owner):
                raise Rejected(404, "Conversation not found.")
        return session_id, self.public_events(owner, session_id, message)

    def run_agent(self, owner, session_id, message):
        return self.runner.run(
            user_id=owner,
            session_id=session_id,
            message=message,
            language=self.language_for(owner),
        )

    def public_events(self, owner, session_id, message):
        yield {"type": "session", "session_id": session_id}
        source = self.run_agent(owner, session_id, message)
        has_text = False
        try:
            for event in source:
                if event.get("kind") == "error":
                    raise RuntimeError("Provider reported an error")
                if event.get("kind") == "text" and isinstance(event.get("text"), str):
                    has_text = True
                    yield {"type": "text", "text": event["text"]}
                elif (event.get("kind") == "tool" and
                      event.get("name") == "lookup_order" and
                      event.get("status") == "complete"):
                    yield {"type": "tool", "label": "Order checked"}
            if not has_text:
                raise RuntimeError("No public response")
        except Exception:
            yield {"type": "error", "message": "The reply could not finish. Try again later."}
        else:
            yield {"type": "done"}
        finally:
            source.close()


def make_server(app, port=0):
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *args):
            pass

        def json_reply(self, status, body):
            payload = json.dumps(body).encode()
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)

        def body(self):
            try:
                length = int(self.headers.get("Content-Length", "0"))
                if not 0 < length <= 8192:
                    raise ValueError()
                value = json.loads(self.rfile.read(length))
                if not isinstance(value, dict):
                    raise ValueError()
                return value
            except (ValueError, json.JSONDecodeError):
                raise Rejected(422, "Invalid JSON request.")

        def do_GET(self):
            path = urlsplit(self.path).path
            assets = {"/": ("index.html", "text/html"),
                      "/client.js": ("client.js", "text/javascript")}
            if path not in assets:
                self.json_reply(404, {"error": "Not found."})
                return
            name, content_type = assets[path]
            data = (ROOT / name).read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

        def mutate(self):
            try:
                owner = app.authenticate(self.headers.get("Authorization", ""))
                if self.command == "PUT" and self.path == "/api/preference":
                    self.json_reply(200, app.save_preference(owner, self.body()))
                elif self.command == "DELETE" and self.path == "/api/preference":
                    self.json_reply(200, app.forget_preference(owner))
                elif self.command == "POST" and self.path == "/api/chat":
                    _, events = app.prepare_chat(owner, self.body())
                    self.send_response(200)
                    self.send_header("Content-Type", "application/x-ndjson")
                    self.send_header("Cache-Control", "no-store")
                    self.end_headers()
                    try:
                        for event in events:
                            self.wfile.write((json.dumps(event) + "\n").encode())
                            self.wfile.flush()
                    except (BrokenPipeError, ConnectionResetError):
                        pass
                    finally:
                        events.close()
                else:
                    self.json_reply(404, {"error": "Not found."})
            except Rejected as error:
                self.json_reply(error.status, {"error": error.message})

        do_POST = do_PUT = do_DELETE = mutate

    return ThreadingHTTPServer(("127.0.0.1", port), Handler)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--demo", action="store_true", required=True,
                        help="Acknowledge fake localhost-only authentication/model")
    parser.add_argument("--port", type=int, default=8766)
    args = parser.parse_args()
    app = App(ROOT / "demo.sqlite")
    server = make_server(app, args.port)
    print(f"Offline demo: http://127.0.0.1:{server.server_port}", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
        app.db.close()
