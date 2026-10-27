"""Nightly job: generate memories from yesterday's sessions.

Runs as a Cloud Run job at 02:00 Europe/London. For every session that ended
yesterday it asks Memory Bank to extract and consolidate memories for that
customer.
"""
from __future__ import annotations

import datetime as dt
import os

import vertexai

PROJECT = os.environ["GOOGLE_CLOUD_PROJECT"]
LOCATION = os.environ.get("GOOGLE_CLOUD_LOCATION", "europe-west2")
ENGINE = os.environ["AGENT_ENGINE_NAME"]  # projects/.../reasoningEngines/...


def yesterdays_sessions(client):
    since = (dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=1)).isoformat()
    return client.agent_engines.sessions.list(name=ENGINE, config={"filter": f'update_time>="{since}"'})


def main() -> None:
    client = vertexai.Client(project=PROJECT, location=LOCATION)
    for session in yesterdays_sessions(client):
        client.agent_engines.memories.generate(
            name=ENGINE,
            vertex_session_source={"session": session.name},
            scope={"user_id": session.user_id},
            config={"wait_for_completion": False},
        )


if __name__ == "__main__":
    main()
