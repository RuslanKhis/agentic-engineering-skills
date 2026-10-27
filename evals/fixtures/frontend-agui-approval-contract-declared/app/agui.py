"""AG-UI endpoint for the CopilotKit chat."""
from __future__ import annotations

from ag_ui_adk import ADKAgent, add_adk_fastapi_endpoint
from fastapi import Depends, FastAPI

from app.agent import root_agent


def mount_agui(app: FastAPI, principal_dependency) -> ADKAgent:
    agent = ADKAgent(
        adk_agent=root_agent,
        app_name="support",
        user_id_extractor=lambda run_input: run_input.forwarded_props.get("userId", "anonymous"),
        use_in_memory_services=True,
    )
    add_adk_fastapi_endpoint(app, agent, path="/api/agent", dependencies=[Depends(principal_dependency)])
    return agent
