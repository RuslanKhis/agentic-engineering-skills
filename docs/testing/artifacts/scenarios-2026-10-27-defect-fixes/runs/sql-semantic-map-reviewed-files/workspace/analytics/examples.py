"""Few-shot examples for the author: a pending queue written by code, a reviewed set read by the author.

A successful query is only a candidate. `record_pending` (called by application code, never exposed as
a tool) stores it with literals masked and no question text or user identity. A reviewer promotes it
by adding it, with `reviewed_by` and `reviewed_on`, to `semantic/examples/<domain>.yml`. The author
sees promoted examples for the current domain only, and each is re-checked by `check_candidate`.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import yaml

from analytics.checks import RejectedSQL, check_candidate
from analytics.semantic import ROOT

MAX_EXAMPLES = 5


def mask_literals(sql: str) -> str:
    import sqlglot
    from sqlglot import exp

    tree = sqlglot.parse_one(sql, read="bigquery")
    masked = tree.transform(lambda n: exp.Placeholder(this="value") if isinstance(n, exp.Literal) else n)
    return masked.sql(dialect="bigquery")


def record_pending(domain: str, sql: str, pending_dir: Path) -> Path | None:
    """Queue a successful query for review. Returns the file written, or None if already queued."""
    masked = mask_literals(sql)
    digest = hashlib.sha256(f"{domain}\n{masked}".encode()).hexdigest()[:16]
    path = pending_dir / f"{domain}-{digest}.json"
    if path.exists():
        return None
    pending_dir.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"domain": domain, "sql": masked}, indent=1), encoding="utf-8")
    return path


def promoted(domain: str, allowed_tables: set[str], root: Path = ROOT) -> list[dict]:
    """Reviewed examples for one domain, at most MAX_EXAMPLES; any that fail the policy are dropped."""
    path = root / "examples" / f"{domain}.yml"
    if not path.exists():
        return []
    doc = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    out = []
    for ex in doc.get("examples") or []:
        if not (ex.get("reviewed_by") and ex.get("reviewed_on") and ex.get("question") and ex.get("sql")):
            continue
        try:
            check_candidate(ex["sql"], allowed_tables)
        except RejectedSQL:
            continue
        out.append({"question": ex["question"], "sql": ex["sql"]})
    return out[:MAX_EXAMPLES]
