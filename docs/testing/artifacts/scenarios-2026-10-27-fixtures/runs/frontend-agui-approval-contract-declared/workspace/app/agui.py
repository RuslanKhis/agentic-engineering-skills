"""AG-UI endpoint for the CopilotKit chat."""
from __future__ import annotations

from ag_ui_adk import ADKAgent, add_adk_fastapi_endpoint
from fastapi import Depends, FastAPI

from app.agent import root_agent


# Approval contract (G06): the frontend answers with a plain `role: "tool"` message
# (CopilotKit useHumanInTheLoop), so the middleware must not end runs with an
# interrupt outcome. Switching to interrupt/resume means moving the web app to
# useInterrupt in the same change.
EMIT_INTERRUPT_OUTCOME = False


def mount_agui(app: FastAPI, principal_dependency) -> ADKAgent:
    agent = ADKAgent(
        adk_agent=root_agent,
        app_name="support",
        emit_interrupt_outcome=EMIT_INTERRUPT_OUTCOME,
        user_id_extractor=lambda run_input: run_input.forwarded_props.get("userId", "anonymous"),
        use_in_memory_services=True,
    )
    add_adk_fastapi_endpoint(app, agent, path="/api/agent", dependencies=[Depends(principal_dependency)])
    return agent
