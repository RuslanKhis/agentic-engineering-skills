"""Operator tool: find and roll back poisoned memories. Read-only unless --apply is given.

  python -m jobs.memory_repair scan     ENGINE                 list memories whose fact claims an entitlement
  python -m jobs.memory_repair rollback MEMORY_NAME [--apply]  restore the last revision before the poisoned one

Rollback restores a revision, so the earlier fact ("Customer prefers paper bags.") comes back; deleting the
memory would lose it. It is a write to production: the default is a dry run that prints the plan.
Revisions are kept 90 days (REVISION_TTL); m-77a1 was changed on 22 Sep 2026, so act before ~21 Dec 2026.
UNVERIFIED against the real SDK: client.agent_engines.memories.{list,rollback,revisions.list} and the
`fact`, `name`, `create_time` attributes were taken from documentation, not executed.
"""
from __future__ import annotations

import argparse
import os
import sys

from pinecrest.memory_policy import is_entitlement_claim


def scan(client, engine: str) -> list[tuple[str, str]]:
    return [(m.name, m.fact) for m in client.agent_engines.memories.list(name=engine)
            if is_entitlement_claim(m.fact)]


def plan_rollback(client, memory_name: str):
    """Return (target revision, revisions) where target is the newest revision that is not an entitlement claim."""
    revisions = sorted(client.agent_engines.memories.revisions.list(name=memory_name),
                       key=lambda r: r.create_time, reverse=True)
    target = next((r for r in revisions if not is_entitlement_claim(r.fact)), None)
    return target, revisions


def rollback(client, memory_name: str, apply: bool = False) -> str:
    target, revisions = plan_rollback(client, memory_name)
    if target is None:
        return f"no clean revision among {len(revisions)}; nothing to roll back to (consider deleting)"
    msg = f"roll back {memory_name} to {target.name} ({target.fact!r})"
    if not apply:
        return "DRY RUN: " + msg
    client.agent_engines.memories.rollback(name=memory_name, target_revision_id=target.name.rsplit("/", 1)[-1])
    return "DONE: " + msg


def main(argv) -> int:
    import vertexai

    p = argparse.ArgumentParser()
    p.add_argument("cmd", choices=["scan", "rollback"])
    p.add_argument("name")
    p.add_argument("--apply", action="store_true")
    a = p.parse_args(argv)
    client = vertexai.Client(project=os.environ["GOOGLE_CLOUD_PROJECT"],
                             location=os.environ.get("GOOGLE_CLOUD_LOCATION", "europe-west2"))
    if a.cmd == "scan":
        hits = scan(client, a.name)
        for name, fact in hits:
            print(name, fact)
        return 1 if hits else 0
    print(rollback(client, a.name, a.apply))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
