"""Records which mechanism carried the schema on each model request, to prove the path that ran."""
from __future__ import annotations

import logging

logger = logging.getLogger("extractor.probe")

# Appended to on every model request; tests clear it, production reads it through the log line.
CAPTURED: list[dict] = []


def describe_request(agent_name: str, llm_request) -> dict:
    config = llm_request.config
    tool_names = sorted(
        decl.name for tool in (config.tools or []) for decl in (tool.function_declarations or []))
    return {
        "agent": agent_name,
        "response_schema": config.response_schema is not None,
        "response_mime_type": config.response_mime_type,
        "tool_names": tool_names,
        "set_model_response": "set_model_response" in tool_names,
    }


def request_probe(callback_context, llm_request):
    record = describe_request(callback_context.agent_name, llm_request)
    CAPTURED.append(record)
    logger.info("model request %s", record)
    return None
