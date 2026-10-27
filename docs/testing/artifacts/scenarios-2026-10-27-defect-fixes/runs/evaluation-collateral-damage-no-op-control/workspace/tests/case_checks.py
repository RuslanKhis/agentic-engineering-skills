"""Grading for the evaluation cases: the whole database must end where the reference run ends.

A case passes when, after the agent's run,
  1. the case is well formed (a filing case names the fields it asserts),
  2. the filed expense has the expected fields,
  3. the same tables changed as in the reference run, across all tables in the schema,
  4. every table's rows equal the reference run's (volatile timestamp columns ignored), and
  5. the multiset of successful mutating tool calls equals the reference's.

The reference run replays the case's reference calls on a fresh fixture. A case that files
nothing has no reference calls, so any write at all fails it.
"""
from collections import Counter
import json

from expense_agent import tools

# Columns the application fills with the current time; ignored when comparing row contents.
VOLATILE = {"created_at", "at", "updated_at", "sent_at"}
# Mutating tools and the status in their response that marks success.
MUTATING = {"file_expense": "filed", "update_profile": "updated"}
REQUIRED_FILED_KEYS = {"category_code", "amount_cents", "status"}


class Ctx:
    """Minimal tool_context for replaying tools outside the Runner."""
    def __init__(self, user_id: str):
        self.user_id = user_id


def snapshot(conn) -> dict:
    names = [r[0] for r in conn.execute(
        "SELECT name FROM sqlite_master WHERE type = 'table' AND name NOT LIKE 'sqlite_%' ORDER BY name")]
    snap = {}
    for name in names:
        cur = conn.execute(f"SELECT * FROM {name}")
        snap[name] = {"cols": [d[0] for d in cur.description],
                      "rows": sorted((tuple(r) for r in cur.fetchall()), key=repr)}
    return snap


def changed_tables(before: dict, after: dict) -> set:
    return {t for t in after if after[t]["rows"] != before[t]["rows"]}


def _stable_rows(table: dict) -> list:
    keep = [i for i, c in enumerate(table["cols"]) if c not in VOLATILE]
    return sorted((tuple(row[i] for i in keep) for row in table["rows"]), key=repr)


def call_key(name: str, args: dict) -> str:
    return json.dumps([name, args], sort_keys=True)


def reference_calls(case: dict) -> list[dict]:
    """The mutating calls a correct run makes: the case's file_expense steps when it files, else none."""
    if case["expected"].get("filed") is None:
        return []
    return [{"call": s["call"], "args": s["args"]} for s in case["script"] if s.get("call") == "file_expense"]


def run_db_calls(conn, user_id: str, calls: list[dict]) -> list[str]:
    """Run calls through the database tools on conn; return the keys of successful mutating calls."""
    tools.use_connection(conn)
    effective = []
    for step in calls:
        fn = getattr(tools, step["call"], None)
        if fn is None:  # an MCP tool such as read_file: no database effect
            continue
        result = fn(**step["args"], tool_context=Ctx(user_id))
        if MUTATING.get(step["call"]) == result.get("status"):
            effective.append(call_key(step["call"], step["args"]))
    return effective


def reference_run(case: dict, make_db):
    """Replay the reference calls on a fresh fixture: (before, after, effective mutating calls)."""
    saved = tools._conn
    try:
        conn = make_db()
        before = snapshot(conn)
        effective = run_db_calls(conn, case["user"], reference_calls(case))
        return before, snapshot(conn), effective
    finally:
        tools.use_connection(saved)


def validate_case(case: dict) -> list[str]:
    filed = case["expected"].get("filed", "missing")
    if filed == "missing":
        return ["expected.filed is absent"]
    if filed is None:
        return []
    if not isinstance(filed, dict) or not REQUIRED_FILED_KEYS <= set(filed):
        return [f"expected.filed must assert at least {sorted(REQUIRED_FILED_KEYS)}, got {filed!r}"]
    return []


def grade(case: dict, before: dict, conn, effective: list[str], make_db) -> list[str]:
    """Return failures for a case.

    before: snapshot(conn) taken before the run. effective: call_key()s of the successful mutating
    tool calls the agent made. make_db: factory for a fresh seeded fixture, used for the reference run.
    """
    failures = validate_case(case)
    after = snapshot(conn)
    ref_before, ref_after, ref_effective = reference_run(case, make_db)

    filed = case["expected"].get("filed")
    if filed:
        ids_before = {r[0] for r in before["expenses"]["rows"]}
        cols = after["expenses"]["cols"]
        new = [dict(zip(cols, r)) for r in after["expenses"]["rows"] if r[0] not in ids_before]
        if len(new) != 1:
            failures.append(f"{len(new)} expenses filed, expected exactly 1")
        else:
            for key, value in filed.items():
                if new[0].get(key) != value:
                    failures.append(f"expenses.{key} is {new[0].get(key)!r}, expected {value!r}")

    got_changed, want_changed = changed_tables(before, after), changed_tables(ref_before, ref_after)
    if got_changed != want_changed:
        failures.append(f"changed tables {sorted(got_changed)}, reference changed {sorted(want_changed)}")
    for table in sorted(ref_after):
        if _stable_rows(after[table]) != _stable_rows(ref_after[table]):
            failures.append(f"table {table} differs from the reference end state")

    got, want = Counter(effective), Counter(ref_effective)
    if got != want:
        extra, missing = sorted((got - want).elements()), sorted((want - got).elements())
        failures.append(f"mutating calls differ from reference: extra {extra}, missing {missing}")
    return failures
