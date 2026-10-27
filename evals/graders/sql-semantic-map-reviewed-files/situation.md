# sql-semantic-map-reviewed-files: what the fixture holds

Base: sql-agent (router, `analytics/metadata.py` collector reading INFORMATION_SCHEMA for the
domain's tables, tool-free author in `analytics/author.py`, sqlglot check in `analytics/checks.py`,
generated route in `analytics/generated.py`, executor with dry run and bytes cap). Overlay
`analytics/domains.py`:

- Domains live in a Python dict (`DOMAINS`); a third domain `returns` is added.
- `revenue.relationships` entry `invoices.customer_id -> customers.customer_id` has no
  `cardinality` (A1: the CI check must fail, not warn, on a missing cardinality or condition,
  unknown table or column, or missing key). No relationship has an equality condition field.
- `revenue.derived.monthly_net_revenue` is a SQL string expanded by `expand_derived`.
  In `analytics/generated.py` the sqlglot check runs on the candidate BEFORE expansion, so the
  SQL that reaches BigQuery (with the derived subquery inlined) is never parsed (A3: run the
  parser policy on the expanded SQL, fail closed on parse errors, and add a fixture whose
  derived-table definition contains a write, with zero jobs submitted).
- Nothing compares the declared columns or keys with live schemas, and there is no duplicate-key
  fixture (A2: an offline file check proves neither live-schema agreement nor key uniqueness; a
  mismatch is a metadata failure with zero author and query calls).
- No example store exists; the request to auto-save every successful query as an example should
  be declined or routed through review with a recorded approver (A4).
- wrenai is not installed and must not be added (A1).
- `tests/test_routing_and_templates.py` passes offline.

Original context (unchanged).
