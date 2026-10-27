"""Look up a provider operation by id: reconnects to work already dispatched instead of sending it again."""
from __future__ import annotations

from pipeline.model import Transport, httpx_transport


def operation_status(base_url: str, operation_id: str, api_key: str,
                     transport: Transport = httpx_transport) -> dict:
    """Returns {"state": "running" | "succeeded" | "failed" | "expired", "result": ..., "usage": ...}."""
    status, body = transport(f"{base_url}/operations/{operation_id}", {}, {"Authorization": f"Bearer {api_key}"}, 30.0)
    if status == 404:
        return {"state": "expired"}
    return body
