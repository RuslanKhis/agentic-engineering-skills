"""Nightly job: generate memories from yesterday's sessions.

Runs as a Cloud Run job at 02:00 Europe/London. For every session that ended
yesterday it asks Memory Bank to extract and consolidate memories for that
customer. A session whose text addresses the assistant ("SYSTEM NOTE ...") is
quarantined, not generated from. Each generate call carries revision labels so
a bad source can be found and rolled back (see jobs/memory_repair.py).
Exit status is 1 if any session was quarantined or failed.
"""
from __future__ import annotations

import datetime as dt
import os
import sys

from pinecrest.memory_policy import generation_config, looks_injected


def yesterdays_sessions(client, engine):
    since = (dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=1)).isoformat()
    return client.agent_engines.sessions.list(name=engine, config={"filter": f'update_time>="{since}"'})


def session_texts(client, session) -> list[str]:
    # UNVERIFIED against the real SDK (no cloud access when written): event/part attribute names.
    texts = []
    for event in client.agent_engines.sessions.events.list(name=session.name):
        for part in getattr(getattr(event, "content", None), "parts", None) or []:
            if getattr(part, "text", None):
                texts.append(part.text)
    return texts


def run(client, engine: str, run_date: str, sessions=None, texts=session_texts) -> dict:
    report = {"generated": [], "quarantined": [], "failed": []}
    for session in (yesterdays_sessions(client, engine) if sessions is None else sessions):
        try:
            if any(looks_injected(t) for t in texts(client, session)):
                report["quarantined"].append(session.name)
                continue
            client.agent_engines.memories.generate(
                name=engine,
                vertex_session_source={"session": session.name},
                scope={"user_id": session.user_id},
                config=generation_config(session.name, run_date),
            )
            report["generated"].append(session.name)
        except Exception as exc:  # fail closed per session; one bad session must not stop the rest
            report["failed"].append((session.name, type(exc).__name__))
    return report


def main() -> int:
    import vertexai

    client = vertexai.Client(project=os.environ["GOOGLE_CLOUD_PROJECT"],
                             location=os.environ.get("GOOGLE_CLOUD_LOCATION", "europe-west2"))
    report = run(client, os.environ["AGENT_ENGINE_NAME"], dt.date.today().isoformat())
    print(report)
    return 1 if report["quarantined"] or report["failed"] else 0


if __name__ == "__main__":
    sys.exit(main())
