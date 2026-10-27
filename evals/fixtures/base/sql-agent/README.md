# Fernhill revenue analytics agent

An ADK agent that answers account managers' questions about Fernhill Wholesale's sales from the
BigQuery dataset `fernhill-analytics.sales`.

- `analytics/router.py` decides between a reviewed template, a generated query or a
  clarification.
- `analytics/templates.py` holds the reviewed SQL templates.
- `analytics/domains.py` holds the semantic domains (tables, columns, relationships, derived
  tables) the generated-query route may use.
- `analytics/metadata.py` collects column metadata from `INFORMATION_SCHEMA` for a domain's tables.
- `analytics/author.py` builds the tool-free SQL author (ADK `LlmAgent`).
- `analytics/checks.py` parses the author's candidate with sqlglot before execution.
- `analytics/executor.py` runs SQL on BigQuery with a dry run first and a bytes cap.
- `analytics/generated.py` is the generated-query route end to end.
- `analytics/agent.py` wires the route into the ADK agent the app serves.

Tests: `python -m unittest discover -s tests -t .` (no BigQuery, no model; sqlglot-dependent tests
skip when sqlglot is absent).
