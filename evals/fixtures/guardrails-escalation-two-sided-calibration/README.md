# Expense claims agent

ADK agent (google-adk 2.12.0) that reads a submitted expense claim and either decides it
(approve or reject, with a reason) or escalates it to the finance review queue. Runs on
Cloud Run; claims arrive from the expenses system through `/claims/{id}/triage`.

- `expense_agent/agent.py`: the agent and its two tools.
- `expense_agent/prompts.py`: the instruction, including the company expense rules.
- `expense_agent/tools.py`: `decide_claim` and `escalate_claim`, writing to the claims store.
- `expense_agent/store.py`: SQLite claims store (Cloud SQL in production).
- `dashboards/escalation-rate.md`: the production dashboard finance watches.
- `data/recent-claims.jsonl`: an export of 40 recent claims (no outcomes recorded).

Tests: `python -m unittest discover -s tests -t .` (stdlib; google-adk is not installed in
this environment and there is no model access here).
