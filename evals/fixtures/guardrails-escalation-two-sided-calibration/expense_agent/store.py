"""Claims store."""
from __future__ import annotations

import json
import sqlite3

SCHEMA = """
CREATE TABLE IF NOT EXISTS claims (
    claim_id TEXT PRIMARY KEY,
    employee_id TEXT NOT NULL,
    payload TEXT NOT NULL,
    lane TEXT,
    decision TEXT,
    reason TEXT
);
"""


class ClaimStore:
    def __init__(self, path: str = ":memory:") -> None:
        self.conn = sqlite3.connect(path)
        self.conn.row_factory = sqlite3.Row
        self.conn.executescript(SCHEMA)

    def add(self, claim: dict) -> None:
        with self.conn:
            self.conn.execute("INSERT INTO claims (claim_id, employee_id, payload) VALUES (?, ?, ?)",
                              (claim["claim_id"], claim["employee_id"], json.dumps(claim)))

    def get(self, claim_id: str) -> dict | None:
        row = self.conn.execute("SELECT * FROM claims WHERE claim_id = ?", (claim_id,)).fetchone()
        if row is None:
            return None
        return {**json.loads(row["payload"]), "lane": row["lane"], "decision": row["decision"],
                "reason": row["reason"]}

    def set_outcome(self, claim_id: str, lane: str, decision: str | None, reason: str) -> None:
        with self.conn:
            self.conn.execute("UPDATE claims SET lane = ?, decision = ?, reason = ? WHERE claim_id = ?",
                              (lane, decision, reason, claim_id))
