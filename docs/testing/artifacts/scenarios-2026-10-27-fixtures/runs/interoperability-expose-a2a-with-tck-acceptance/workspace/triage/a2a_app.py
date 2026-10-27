"""A2A entry point: `uvicorn triage.a2a_app:app --host 127.0.0.1 --port 8001`.

Not executed in this sandbox (google-adk, a2a-sdk and PyJWT are not installed).
The card-parsing call and `to_a2a(agent_card=...)` follow the 2.12.0 signature
documented in the interoperability skill and must be confirmed on the pinned
packages by the acceptance run in docs/partner/a2a-acceptance.md.
"""
import json
import os
from pathlib import Path

from a2a.types import AgentCard  # a2a-sdk 1.x cards are protobuf messages
from google.adk.a2a.utils.agent_to_a2a import to_a2a
from google.protobuf.json_format import ParseDict

from triage.a2a_auth import BearerAuthMiddleware, make_jwt_verifier
from triage.agent import root_agent

CARD_FILE = Path(__file__).resolve().parent.parent / "a2a" / "agent-card.json"
ISSUER = os.environ.get("TRIAGE_OAUTH_ISSUER", "https://auth.service-desk.example")
JWKS_URL = os.environ.get("TRIAGE_OAUTH_JWKS_URL", f"{ISSUER}/.well-known/jwks.json")
AUDIENCE = "warranty-triage"
REQUIRED_SCOPE = "triage:invoke"

card = ParseDict(json.loads(CARD_FILE.read_text()), AgentCard())

# A supplied card is served as is, so its advertised URL is the public one.
# In-memory sessions and tasks: single instance only (see acceptance doc).
app = to_a2a(root_agent, agent_card=card)
app.add_middleware(
    BearerAuthMiddleware,
    verifier=make_jwt_verifier(JWKS_URL, ISSUER, AUDIENCE),
    required_scope=REQUIRED_SCOPE,
)
