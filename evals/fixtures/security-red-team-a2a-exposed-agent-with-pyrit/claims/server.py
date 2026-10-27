"""FastAPI app with the agent exposed over A2A under /a2a/claims."""
from __future__ import annotations

import os

from fastapi import FastAPI
from google.adk.a2a.utils.agent_to_a2a import to_a2a

from claims.agent import root_agent

PUBLIC_HOST = os.environ.get("PUBLIC_HOST", "claims-agent-7f3k2-ew.a.run.app")

a2a_app = to_a2a(root_agent, host=PUBLIC_HOST, port=443, protocol="https")

app = FastAPI(title="Claims agent")
app.mount("/a2a/claims", a2a_app)
# Agent card: https://<host>/a2a/claims/.well-known/agent-card.json


@app.get("/healthz")
def healthz():
    return {"ok": True}
