"""Grade a booking run by the state it leaves, not by the order of its calls.

A case carries one reference trajectory. It is replayed on a fresh backend to get the target end
state; the agent's run passes when its backend diff and its effective mutations match. Imports
nothing from google.adk, so it runs offline.
"""
from __future__ import annotations

import contextlib
import copy
import inspect
from collections import Counter
from dataclasses import dataclass, field

from booking_agent import tools
from booking_agent.backend import Backend

# tool -> the status its own contract returns on success (see booking_agent/tools.py)
MUTATING = {"book_slot": "booked", "cancel_booking": "cancelled"}


@dataclass
class Ctx:
    user_id: str


@dataclass
class Call:
    name: str
    args: dict
    result: dict = field(default_factory=dict)


def seeded_backend(case: dict) -> Backend:
    """A fresh backend holding the case's seed bookings (session_input.state.seed_bookings)."""
    session = case["session_input"]
    backend = Backend()
    for slot_id in session.get("state", {}).get("seed_bookings", []):
        backend.book(slot_id, session["user_id"])
    return backend


def reference_calls(case: dict) -> list[Call]:
    return [Call(u["name"], dict(u.get("args") or {}))
            for turn in case["conversation"]
            for u in (turn.get("intermediate_data") or {}).get("tool_uses", [])]


@contextlib.contextmanager
def using_backend(backend: Backend):
    previous = tools.backend
    tools.backend = backend
    try:
        yield
    finally:
        tools.backend = previous


def replay(calls: list[Call], user_id: str, backend: Backend) -> list[Call]:
    """Run calls through the real tool functions against `backend`; returns calls with results."""
    done = []
    with using_backend(backend):
        for c in calls:
            fn = getattr(tools, c.name)
            kwargs = dict(c.args)
            if "tool_context" in inspect.signature(fn).parameters:
                kwargs["tool_context"] = Ctx(user_id)
            done.append(Call(c.name, c.args, fn(**kwargs)))
    return done


def diff_snapshots(before: dict, after: dict, ignore_fields: dict[str, set] | None = None) -> dict:
    """Per-table added / removed / changed-field diff over every table in the snapshot.

    `ignore_fields` maps a table to volatile fields; it never hides a table-level change.
    """
    ignore_fields = ignore_fields or {}
    out = {}
    for table in sorted(set(before) | set(after)):
        old, new = before.get(table, {}), after.get(table, {})
        skip = ignore_fields.get(table, set())
        entry = {"added": {k: new[k] for k in new.keys() - old.keys()},
                 "removed": {k: old[k] for k in old.keys() - new.keys()},
                 "changed": {}}
        for key in old.keys() & new.keys():
            fields = {f: (old[key].get(f), new[key].get(f))
                      for f in set(old[key]) | set(new[key])
                      if f not in skip and old[key].get(f) != new[key].get(f)}
            if fields:
                entry["changed"][key] = fields
        if entry["added"] or entry["removed"] or entry["changed"]:
            out[table] = entry
    return out


def effective_mutations(calls: list[Call]) -> Counter:
    """Multiset of mutating calls whose own result marks success."""
    return Counter((c.name, tuple(sorted(c.args.items())))
                   for c in calls
                   if c.name in MUTATING and c.result.get("status") == MUTATING[c.name])


def grade(case: dict, agent_calls: list[Call], agent_after: dict,
          ignore_fields: dict[str, set] | None = None) -> list[str]:
    """Return the list of violated checks; empty means the run reached the reference end state.

    agent_calls need results (captured from the Runner's function responses); agent_after is the
    backend snapshot after the run, taken from a backend seeded by `seeded_backend(case)`.
    """
    user_id = case["session_input"]["user_id"]
    start = seeded_backend(case).snapshot()
    ref_backend = seeded_backend(case)
    ref_done = replay(reference_calls(case), user_id, ref_backend)

    want = diff_snapshots(start, ref_backend.snapshot(), ignore_fields)
    got = diff_snapshots(start, agent_after, ignore_fields)
    problems = []
    if set(got) != set(want):
        problems.append(f"changed tables {sorted(got)} != expected {sorted(want)}")
    elif got != want:
        problems.append("record or field changes differ from the reference end state")
    if effective_mutations(agent_calls) != effective_mutations(ref_done):
        problems.append("effective mutating calls differ from the reference (extra, missing or detour)")
    problems.extend(_path_rules(ref_done, agent_calls))
    return problems


def _path_rules(ref: list[Call], run: list[Call]) -> list[str]:
    """Order that matters for safety. Everything else about order is free.

    A move (reference books and cancels) must not cancel before the new booking succeeded, or a
    failed book_slot leaves the patient with no appointment.
    """
    names = {c.name for c in ref if c.name in MUTATING}
    if names != set(MUTATING):
        return []
    booked_at = next((i for i, c in enumerate(run)
                      if c.name == "book_slot" and c.result.get("status") == "booked"), None)
    cancelled_at = next((i for i, c in enumerate(run)
                         if c.name == "cancel_booking" and c.result.get("status") == "cancelled"), None)
    if cancelled_at is not None and (booked_at is None or cancelled_at < booked_at):
        return ["cancelled the old booking before the new one was booked"]
    return []


def do_nothing_passes(case: dict) -> list[str]:
    """Control: an agent that makes no calls. An action case must fail it; non-action must pass."""
    return grade(case, [], seeded_backend(case).snapshot())


def is_action_case(case: dict) -> bool:
    return bool(effective_mutations(replay(reference_calls(case), case["session_input"]["user_id"],
                                           seeded_backend(case))))
