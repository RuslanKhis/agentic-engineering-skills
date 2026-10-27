"""Database tools for the expense agent. The connection is set by agent.py or the tests."""
from __future__ import annotations

import datetime as dt

_conn = None


def use_connection(conn) -> None:
    global _conn
    _conn = conn


def _log(actor: str, action: str, target: str) -> None:
    _conn.execute("INSERT INTO audit_log (actor, action, target) VALUES (?, ?, ?)", (actor, action, target))
    _conn.execute("INSERT OR REPLACE INTO sync_state (key, value, updated_at) VALUES ('last_write', ?, ?)",
                  (target, dt.datetime.now(dt.timezone.utc).isoformat()))


def get_policy_limit(category_code: str, tool_context) -> dict:
    """Return the employee's limit in cents for an expense category such as "MEAL" or "TRAVEL"."""
    grade = _conn.execute("SELECT 'G' || substr(id, -1) FROM employees WHERE id = ?",
                          (tool_context.user_id,)).fetchone()
    row = _conn.execute("SELECT limit_cents FROM policy_limits WHERE category_code = ? AND grade = ?",
                        (category_code, grade[0] if grade else "G1")).fetchone()
    return {"status": "ok", "limit_cents": row[0] if row else None}


def file_expense(category_code: str, amount_cents: int, currency: str, incurred_on: str,
                 description: str, receipt_path: str, tool_context) -> dict:
    """File an expense claim for the signed-in employee.

    Args:
        category_code: "MEAL", "TRAVEL", "HOTEL" or "OFFICE".
        amount_cents: Total in cents in the receipt's currency.
        currency: ISO code, e.g. "EUR".
        incurred_on: Date on the receipt, YYYY-MM-DD.
        description: What was bought.
        receipt_path: Path of the receipt in the receipts folder.
    """
    with _conn:
        cur = _conn.execute(
            "INSERT INTO expenses (employee_id, category_code, amount_cents, currency, incurred_on, receipt_path, status) "
            "VALUES (?, ?, ?, ?, ?, ?, 'submitted')",
            (tool_context.user_id, category_code, amount_cents, currency, incurred_on, receipt_path))
        _conn.execute("INSERT INTO expense_lines (expense_id, description, amount_cents) VALUES (?, ?, ?)",
                      (cur.lastrowid, description, amount_cents))
        _log(tool_context.user_id, "file_expense", f"expenses/{cur.lastrowid}")
    return {"status": "filed", "expense_id": cur.lastrowid}


def get_my_profile(tool_context) -> dict:
    """Return the signed-in employee's expense profile (approver, bank account ending, currency)."""
    row = _conn.execute("SELECT * FROM profiles WHERE employee_id = ?", (tool_context.user_id,)).fetchone()
    return {"status": "ok", "profile": dict(row) if row else None}


def update_profile(employee_id: str, approver_id: str | None = None, home_currency: str | None = None,
                   tool_context=None) -> dict:
    """Update an expense profile's approver or home currency."""
    with _conn:
        if approver_id is not None:
            _conn.execute("UPDATE profiles SET approver_id = ?, updated_at = CURRENT_TIMESTAMP WHERE employee_id = ?",
                          (approver_id, employee_id))
        if home_currency is not None:
            _conn.execute("UPDATE profiles SET home_currency = ?, updated_at = CURRENT_TIMESTAMP WHERE employee_id = ?",
                          (home_currency, employee_id))
        _log(getattr(tool_context, "user_id", "agent"), "update_profile", f"profiles/{employee_id}")
    return {"status": "updated"}


def list_my_expenses(tool_context) -> dict:
    """List the signed-in employee's last ten claims."""
    rows = _conn.execute("SELECT id, category_code, amount_cents, currency, status FROM expenses "
                         "WHERE employee_id = ? ORDER BY id DESC LIMIT 10", (tool_context.user_id,)).fetchall()
    return {"status": "ok", "expenses": [dict(r) for r in rows]}
