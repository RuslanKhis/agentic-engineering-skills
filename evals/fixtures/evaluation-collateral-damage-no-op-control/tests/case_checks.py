"""Checks for the evaluation cases: did the expected row get filed?"""
import hashlib


def table_hash(conn, table: str) -> str:
    rows = conn.execute(f"SELECT * FROM {table} ORDER BY 1").fetchall()
    return hashlib.sha256(repr([tuple(r) for r in rows]).encode()).hexdigest()


def grade(case: dict, before: dict, conn) -> list[str]:
    """Return failures for a case. before maps table name -> hash taken before the run."""
    failures = []
    expected = case["expected"]
    if expected.get("filed"):
        row = conn.execute("SELECT * FROM expenses WHERE employee_id = ? ORDER BY id DESC LIMIT 1",
                           (case["user"],)).fetchone()
        if row is None:
            failures.append("no expense filed")
        else:
            for key, value in expected["filed"].items():
                if row[key] != value:
                    failures.append(f"expenses.{key} is {row[key]!r}, expected {value!r}")
    else:
        if table_hash(conn, "expenses") != before["expenses"]:
            failures.append("expenses changed although nothing should be filed")
    return failures
