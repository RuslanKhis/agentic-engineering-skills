"""SQLite schema and connection for the expenses database."""
from __future__ import annotations

import sqlite3

SCHEMA = """
CREATE TABLE employees (id TEXT PRIMARY KEY, name TEXT NOT NULL, department_id TEXT NOT NULL, manager_id TEXT);
CREATE TABLE departments (id TEXT PRIMARY KEY, name TEXT NOT NULL, cost_centre TEXT NOT NULL);
CREATE TABLE profiles (employee_id TEXT PRIMARY KEY, approver_id TEXT, bank_last4 TEXT, home_currency TEXT NOT NULL, updated_at TEXT);
CREATE TABLE expense_categories (code TEXT PRIMARY KEY, label TEXT NOT NULL, gl_account TEXT NOT NULL);
CREATE TABLE policy_limits (category_code TEXT NOT NULL, grade TEXT NOT NULL, limit_cents INTEGER NOT NULL, PRIMARY KEY (category_code, grade));
CREATE TABLE expenses (id INTEGER PRIMARY KEY AUTOINCREMENT, employee_id TEXT NOT NULL, category_code TEXT NOT NULL, amount_cents INTEGER NOT NULL, currency TEXT NOT NULL, incurred_on TEXT NOT NULL, receipt_path TEXT, status TEXT NOT NULL, created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP);
CREATE TABLE expense_lines (id INTEGER PRIMARY KEY AUTOINCREMENT, expense_id INTEGER NOT NULL, description TEXT NOT NULL, amount_cents INTEGER NOT NULL);
CREATE TABLE approvals (id INTEGER PRIMARY KEY AUTOINCREMENT, expense_id INTEGER NOT NULL, approver_id TEXT NOT NULL, state TEXT NOT NULL, issue_url TEXT, decided_at TEXT);
CREATE TABLE reimbursements (id INTEGER PRIMARY KEY AUTOINCREMENT, expense_id INTEGER NOT NULL, amount_cents INTEGER NOT NULL, paid_on TEXT);
CREATE TABLE exchange_rates (currency TEXT NOT NULL, day TEXT NOT NULL, rate_to_eur REAL NOT NULL, PRIMARY KEY (currency, day));
CREATE TABLE cards (employee_id TEXT NOT NULL, last4 TEXT NOT NULL, active INTEGER NOT NULL);
CREATE TABLE audit_log (id INTEGER PRIMARY KEY AUTOINCREMENT, actor TEXT NOT NULL, action TEXT NOT NULL, target TEXT NOT NULL, at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP);
CREATE TABLE notifications (id INTEGER PRIMARY KEY AUTOINCREMENT, employee_id TEXT NOT NULL, message TEXT NOT NULL, sent_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP);
CREATE TABLE sync_state (key TEXT PRIMARY KEY, value TEXT NOT NULL, updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP);
"""


def connect(path: str = ":memory:") -> sqlite3.Connection:
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.executescript(SCHEMA)
    return conn
