"""Per-user response-language preference. No google.adk imports so the unit tests run without the SDK.

Exact, user-controlled setting: a deterministic row keyed by the verified staff ID, read at each
invocation. Stored in SQLite so it survives restarts; set LANGUAGE_PREFS_DB to a durable path.
"""
from __future__ import annotations

import os
import sqlite3
from contextlib import closing

# Closed list: the value is placed in the instruction, so free text is never accepted.
LANGUAGES = {
    "en": "English",
    "fr": "French",
    "de": "German",
    "es": "Spanish",
    "pl": "Polish",
}


def _db_path() -> str:
    return os.environ.get("LANGUAGE_PREFS_DB", "language_prefs.sqlite3")


def _connect() -> sqlite3.Connection:
    conn = sqlite3.connect(_db_path())
    conn.execute("CREATE TABLE IF NOT EXISTS language_pref (staff_id TEXT PRIMARY KEY, code TEXT NOT NULL)")
    return conn


def set_language(staff_id: str, code: str) -> str:
    code = code.strip().lower()
    if code not in LANGUAGES:
        raise ValueError(f"unsupported language; choose one of {', '.join(sorted(LANGUAGES))}")
    with closing(_connect()) as conn, conn:
        conn.execute("INSERT INTO language_pref (staff_id, code) VALUES (?, ?) "
                     "ON CONFLICT(staff_id) DO UPDATE SET code = excluded.code", (staff_id, code))
    return code


def get_language(staff_id: str) -> str | None:
    with closing(_connect()) as conn:
        row = conn.execute("SELECT code FROM language_pref WHERE staff_id = ?", (staff_id,)).fetchone()
    return row[0] if row and row[0] in LANGUAGES else None


def delete_language(staff_id: str) -> bool:
    """Remove the caller's row. Returns whether one existed."""
    with closing(_connect()) as conn, conn:
        return conn.execute("DELETE FROM language_pref WHERE staff_id = ?", (staff_id,)).rowcount > 0
