"""Checks on the author's candidate SQL before it is executed."""
from __future__ import annotations


class RejectedSQL(Exception):
    pass


def check_candidate(sql: str, allowed_tables: set[str]) -> None:
    import sqlglot
    from sqlglot import exp

    statements = sqlglot.parse(sql, read="bigquery")
    if len(statements) != 1:
        raise RejectedSQL("exactly one statement is allowed")
    tree = statements[0]
    if not isinstance(tree, (exp.Select, exp.Union)):
        raise RejectedSQL("only SELECT is allowed")
    for table in tree.find_all(exp.Table):
        if table.name and table.name not in allowed_tables:
            raise RejectedSQL(f"table {table.name} is not in the domain")
