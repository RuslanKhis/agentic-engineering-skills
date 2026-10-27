"""The exposed server on a fixed-text model, for the conformance run. No credentials, no network.

    PORT=8765 python -m tests.conformance_server
"""
import os

from research.agent import root_agent
from research.mcp_server import build_server
from tests.scripted_model import FixedTextModel

if __name__ == "__main__":
    build_server(root_agent.clone(update={"model": FixedTextModel()})).run(
        transport="streamable-http", host="127.0.0.1", port=int(os.environ.get("PORT", "8765")))
