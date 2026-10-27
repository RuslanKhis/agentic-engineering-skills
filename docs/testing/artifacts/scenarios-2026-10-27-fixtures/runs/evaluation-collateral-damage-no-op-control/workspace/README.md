# Expense agent

An ADK 2.12 agent that files employees' expense claims. It reads receipts from the shared
receipts folder through the filesystem MCP server, files the claim in the expenses database and,
for over-limit claims, opens an approval issue in the finance GitHub repository through the GitHub
MCP server.

- `expense_agent/agent.py` builds the agent and its two MCP toolsets.
- `expense_agent/tools.py` are the database tools (no ADK imports).
- `expense_agent/db.py` is the SQLite schema (14 tables).
- `eval_cases/cases.json` holds the 30 evaluation cases; `tests/test_cases.py` runs each through
  the Runner with a scripted model and grades it with `tests/case_checks.py`.
- `docs/nightly-live-run.md` describes the nightly run against the real MCP servers.

Grading (`tests/case_checks.py`) diffs every table before and after a run and requires the changed
tables and audit-log actions to be exactly what filing one expense produces. `tests/test_grader.py`
checks the grader offline: a do-nothing run must fail every action case, and the collateral edit
from the 2026-10-16 incident (case c14) must be caught.

Tests: `python -m unittest discover -s tests -t .` (Runner tests skip when google-adk is not
installed; it is not installed in this environment, so `test_grader.py` is the part that runs here).
