"""Our HTTP front end: standard-library http.server with the ADK Runner in process.

POST /summary   -> {"status": "ok", "summary": "..."}
POST /chat      -> {"session_id": ..., "reply": ...}
The verified principal comes from the IAP assertion (app/auth.py).
"""
from __future__ import annotations

import asyncio
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import os

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from app.agent import root_agent
from app.auth import Unauthenticated, principal_from_headers
from app.summary import build_summary_flow

sessions = InMemorySessionService()
chat_runner = Runner(app_name="support", agent=root_agent, session_service=sessions)
summary_runner = Runner(app_name="summary", agent=build_summary_flow(), session_service=sessions)


def _verify(assertion, audience):
    from google.oauth2 import id_token
    from google.auth.transport import requests as google_requests

    return id_token.verify_token(assertion, google_requests.Request(), audience=audience,
                                 certs_url="https://www.gstatic.com/iap/verify/public_key")


async def run_summary(user_id: str) -> dict:
    session = await sessions.create_session(app_name="summary", user_id=user_id)
    text = []
    async for event in summary_runner.run_async(user_id=user_id, session_id=session.id,
                                                new_message=types.Content(role="user",
                                                                          parts=[types.Part(text="summary")])):
        if event.is_final_response() and event.content and event.content.parts:
            text.extend(p.text for p in event.content.parts if p.text)
    return {"status": "ok", "summary": "".join(text)}


class Handler(BaseHTTPRequestHandler):
    def _send(self, code: int, body: dict) -> None:
        data = json.dumps(body).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_POST(self):
        try:
            principal = principal_from_headers(self.headers, _verify, os.environ.get("IAP_AUDIENCE", ""))
        except Unauthenticated:
            return self._send(401, {"error": "unauthenticated"})
        if self.path == "/summary":
            return self._send(200, asyncio.run(run_summary(principal.user_id)))
        return self._send(404, {"error": "not found"})


if __name__ == "__main__":
    ThreadingHTTPServer(("0.0.0.0", int(os.environ.get("PORT", "8080"))), Handler).serve_forever()
