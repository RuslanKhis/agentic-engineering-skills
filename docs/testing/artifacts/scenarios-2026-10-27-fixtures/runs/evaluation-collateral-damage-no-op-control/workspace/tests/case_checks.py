"""Checks for the evaluation cases: the whole database is diffed, not just the expense row."""

# Tables the tools write as a side effect of any write. They may change only as far as the audit
# actions below account for; they never stand in for a business-table change.
BOOKKEEPING = {"audit_log", "sync_state"}
# Volatile fields, ignored per (table, column) so the table itself is still compared.
VOLATILE = {("expenses", "created_at"), ("audit_log", "at"), ("sync_state", "updated_at")}
FILED_TABLES = {"expenses", "expense_lines"}


def snapshot(conn) -> dict:
    """Every table -> {rowid: row dict}, read from sqlite_master so a 15th table is covered too."""
    names = [r[0] for r in conn.execute(
        "SELECT name FROM sqlite_master WHERE type = 'table' AND name NOT LIKE 'sqlite_%' ORDER BY name")]
    snap = {}
    for name in names:
        cur = conn.execute(f"SELECT rowid AS _rowid, * FROM {name}")
        cols = [c[0] for c in cur.description]
        snap[name] = {r[0]: {c: v for c, v in zip(cols[1:], tuple(r)[1:]) if (name, c) not in VOLATILE}
                      for r in cur.fetchall()}
    return snap


def diff(before: dict, after: dict) -> dict:
    """Changed tables only: {table: {"added": {rowid: row}, "removed": {...}, "changed": {rowid: {col: (old, new)}}}}."""
    out = {}
    for table in after:
        b, a = before.get(table, {}), after[table]
        added = {k: v for k, v in a.items() if k not in b}
        removed = {k: v for k, v in b.items() if k not in a}
        changed = {k: {c: (b[k][c], a[k][c]) for c in a[k] if a[k][c] != b[k][c]} for k in a if k in b and a[k] != b[k]}
        if added or removed or changed:
            out[table] = {"added": added, "removed": removed, "changed": changed}
    return out


def validate_case(case: dict) -> list[str]:
    """A case must say what it expects; an empty `filed` is vacuous, so it is rejected, not graded."""
    expected = case.get("expected", {})
    if "filed" not in expected:
        return ["expected.filed is missing (use null for 'nothing is filed')"]
    filed = expected["filed"]
    if filed is not None and not {"category_code", "amount_cents", "status"} <= set(filed):
        return ["expected.filed must name at least category_code, amount_cents and status, or be null"]
    return []


def grade(case: dict, before: dict, conn) -> list[str]:
    """Return failures for a case. `before` is snapshot(conn) taken before the run."""
    bad = validate_case(case)
    if bad:
        return bad
    changes = diff(before, snapshot(conn))
    filed = case["expected"]["filed"]
    failures = []

    if filed is None:
        # Nothing should be written at all, bookkeeping included.
        return [f"{t} changed although nothing should be written" for t in sorted(changes)]

    stray = sorted(set(changes) - FILED_TABLES - BOOKKEEPING)
    failures += [f"{t} changed but only {sorted(FILED_TABLES)} may change: {_brief(changes[t])}" for t in stray]
    for t in sorted(FILED_TABLES - set(changes)):
        failures.append(f"{t} did not change: nothing was filed")

    actions = [r["action"] for r in changes.get("audit_log", {}).get("added", {}).values()]
    if actions != ["file_expense"]:
        failures.append(f"audit_log actions are {actions!r}, expected ['file_expense']")
    for t in sorted(BOOKKEEPING & set(changes)):
        if changes[t]["removed"] or (t == "audit_log" and changes[t]["changed"]):
            failures.append(f"{t} rows were removed or rewritten")

    exp = changes.get("expenses", {})
    if exp.get("removed") or exp.get("changed") or len(exp.get("added", {})) != 1:
        failures.append(f"expenses must gain exactly one row and change none: {_brief(exp)}")
    else:
        (rowid, row), = exp["added"].items()
        if row["employee_id"] != case["user"]:
            failures.append(f"expense filed for {row['employee_id']!r}, expected {case['user']!r}")
        for key, value in filed.items():
            if row[key] != value:
                failures.append(f"expenses.{key} is {row[key]!r}, expected {value!r}")
        lines = changes.get("expense_lines", {})
        added = list(lines.get("added", {}).values())
        if lines.get("removed") or lines.get("changed") or len(added) != 1:
            failures.append(f"expense_lines must gain exactly one row: {_brief(lines)}")
        elif added[0]["expense_id"] != rowid or added[0]["amount_cents"] != row["amount_cents"]:
            failures.append("expense_lines row does not match the filed expense")
    return failures


def _brief(change: dict) -> str:
    return f"added={list(change.get('added', {}).values())} removed={list(change.get('removed', {}).values())} " \
           f"changed={change.get('changed', {})}"
