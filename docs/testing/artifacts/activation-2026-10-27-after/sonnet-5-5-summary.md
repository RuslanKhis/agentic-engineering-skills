Activation run: backend claude-cli, model claude-sonnet-5-5, 154 cases x 2 repeat(s)
catalogue 7871f43e531caf26  corpus 1d43aab454fb0165

| Run | PASS | PARTIAL | FAIL | ERROR |
| --- | --- | --- | --- | --- |
| repeat 1 | 150 | 3 | 1 | 0 |
| repeat 2 | 148 | 6 | 0 | 0 |
| all | 298 | 9 | 1 | 0 |

Cases not passing in every repeat:
- api-payment-approval-near-miss [safe-api-tool-calls, near-miss] PARTIAL PARTIAL: primary adk-operational-guardrails; supporting safe-api-tool-calls. Human approval of risky actions with durable review records and delayed resume is owned by operational guardrails, and the write must run once only after approval.
- evaluation-ci-gate-near-miss [adk-agent-evaluation, near-miss] PARTIAL PARTIAL: primary adk-release-engineering; supporting adk-agent-evaluation. Wiring an existing eval set into CI with repeat, cost cap and threshold is an evaluation gate in release engineering.
- fastapi-backend-session-endpoints-near-miss [adk-fastapi-backend, near-miss] PASS PARTIAL: primary adk-frontend-integration; supporting adk-fastapi-backend. Session continuation on the agent's run endpoint with ownership checks and a chat error state belongs to the frontend integration skill, with the backend principal dependency supporting.
- guardrails-confirmation-tiering-near-miss [adk-operational-guardrails, near-miss] PARTIAL PARTIAL: primary adk-agent-security; supporting adk-operational-guardrails. This is a lethal-trifecta threat model with tool tiering for which actions need confirmation, and approval mechanics fall to guardrails.
- memory-ingestion-positive [adk-memory-architecture, positive] FAIL PASS: primary none; supporting -. Per-page document ingestion triage for OCR or vision routing is not covered by any catalogue skill.
- observability-eval-handoff-positive [adk-agent-observability, positive] PASS PARTIAL: primary adk-agent-evaluation; supporting adk-agent-observability,protect-adk-sensitive-data. Building a regression eval set from production feedback is evaluation work, with observability for the traces and sensitive-data handling for removing personal data.
- tool-interface-toolset-positive [adk-tool-interface-design, positive] PASS PARTIAL: primary adk-agent-interoperability; supporting adk-tool-interface-design. Consuming an MCP server with tool_filter and prefixes is interoperability, while result shaping and tool-count budgeting belong to tool interface design.
