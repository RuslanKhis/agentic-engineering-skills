"""ASGI entrypoint for the A2A surface: `uvicorn research_agent.a2a_app:app --host 0.0.0.0 --port $PORT`.

Config (environment): SERVICE_URL, the public https URL the card advertises (no trailing slash);
ALLOWED_CALLERS, comma-separated emails of principals allowed to call (the Discovery Engine
service agent). Both are required; startup fails without them.
"""
from __future__ import annotations

import asyncio
import json
import os
from pathlib import Path

from research_agent.a2a_auth import BearerAuthMiddleware, Principal, VerifierUnavailable

CARD_FILE = Path(__file__).resolve().parent.parent / "deploy" / "agent-card.json"
SCOPE = "a2a.invoke"


def load_card_dict(service_url: str) -> dict:
    if not service_url.startswith("https://") or service_url.endswith("/"):
        raise ValueError("SERVICE_URL must be an https URL without a trailing slash")
    card = json.loads(CARD_FILE.read_text())
    card["url"] = service_url
    return card


def make_verifier(audience: str, allowed: frozenset[str]):
    from google.auth.exceptions import TransportError
    from google.auth.transport import requests as g_requests
    from google.oauth2 import id_token

    async def verify(token: str) -> Principal | None:
        try:
            claims = await asyncio.to_thread(
                id_token.verify_oauth2_token, token, g_requests.Request(), audience)
        except TransportError as exc:
            raise VerifierUnavailable from exc
        except ValueError:
            return None
        email = claims.get("email")
        if not claims.get("email_verified") or email not in allowed:
            return None
        return Principal(email, frozenset({SCOPE}))

    return verify


def build_app():
    from a2a.types import AgentCard
    from google.adk.a2a.utils.agent_to_a2a import to_a2a

    from research_agent.agent import a2a_root_agent

    service_url = os.environ["SERVICE_URL"]
    allowed = frozenset(e.strip() for e in os.environ["ALLOWED_CALLERS"].split(",") if e.strip())
    if not allowed:
        raise ValueError("ALLOWED_CALLERS is empty")
    card = AgentCard.model_validate(load_card_dict(service_url))
    # In-memory task store and sessions: keep max-instances=1 until a DatabaseTaskStore and a
    # shared session service are configured (see docs/a2a-exposure.md).
    inner = to_a2a(a2a_root_agent, agent_card=card)
    return BearerAuthMiddleware(inner, make_verifier(service_url, allowed), required_scope=SCOPE)


app = build_app() if "SERVICE_URL" in os.environ else None
