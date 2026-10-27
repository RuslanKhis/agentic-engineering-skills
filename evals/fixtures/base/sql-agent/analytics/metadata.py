"""Collects column metadata for a domain's tables and the derived-table definitions."""
from __future__ import annotations

from analytics.domains import DATASET, DOMAINS, PROJECT

COLUMNS_SQL = (
    f"SELECT table_name, column_name, data_type FROM `{PROJECT}.{DATASET}.INFORMATION_SCHEMA.COLUMNS` "
    "WHERE table_name IN UNNEST(@tables) ORDER BY table_name, ordinal_position"
)


def collect(domain_name: str, run_query) -> dict:
    """run_query(sql, params) -> list of dict rows. Returns the author's context for one domain."""
    domain = DOMAINS[domain_name]
    rows = run_query(COLUMNS_SQL, {"tables": list(domain["tables"])})
    exposed = {t: set(spec["columns"]) for t, spec in domain["tables"].items()}
    columns: dict[str, list[dict]] = {t: [] for t in domain["tables"]}
    for row in rows:
        if row["column_name"] in exposed.get(row["table_name"], ()):
            columns[row["table_name"]].append({"name": row["column_name"], "type": row["data_type"]})
    return {
        "domain": domain_name,
        "tables": {t: {"key": domain["tables"][t]["key"], "columns": cols} for t, cols in columns.items()},
        "relationships": domain["relationships"],
        "derived": domain["derived"],
    }


def expand_derived(sql: str, derived: dict) -> str:
    """Replace references to derived tables with their defining SQL as subqueries."""
    for name, definition in derived.items():
        sql = sql.replace(f"`{name}`", f"({definition})").replace(f" {name} ", f" ({definition}) ")
    return sql
