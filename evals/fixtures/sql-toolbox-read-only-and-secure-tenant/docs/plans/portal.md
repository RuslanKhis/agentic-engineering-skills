# Implementation plan: customer portal revenue agent

| ID and goal | Phase | Type | Human hours | Depends on | Primary skill | State / blocker |
| --- | --- | --- | --- | --- | --- | --- |
| G01 Toolbox sidecar and tools.yaml | 1 | implementation | 2-3 | none | adk-sql-agent-engineering | done |
| G02 Portal chat endpoint | 1 | implementation | 2-3 | G01 | adk-fastapi-backend | done |
| [G03 Own revenue only, read-only warehouse](../tickets/G03.md) | 1 | implementation | 4-6 | G02 | adk-sql-agent-engineering | ready |

Execution scope: local changes and tests with a Toolbox double; no BigQuery or Toolbox server in
development.
