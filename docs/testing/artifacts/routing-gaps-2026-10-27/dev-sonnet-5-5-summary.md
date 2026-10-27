Activation run: backend claude-cli, model claude-sonnet-5-5, 163 cases x 2 repeat(s), split dev
catalogue 74e4ed4293f09ed1  corpus df13231d2053304f

| Run | PASS | PARTIAL | FAIL | ERROR |
| --- | --- | --- | --- | --- |
| repeat 1 | 157 | 6 | 0 | 0 |
| repeat 2 | 158 | 5 | 0 | 0 |
| all | 315 | 11 | 0 | 0 |

| Split | PASS | PARTIAL | FAIL | ERROR |
| --- | --- | --- | --- | --- |
| dev | 315 | 11 | 0 | 0 |

Cases not passing in every repeat:
- api-payment-approval-near-miss [safe-api-tool-calls, near-miss, dev] PARTIAL PARTIAL: primary adk-operational-guardrails; supporting safe-api-tool-calls. Human approval with durable review records and delayed resume is guardrails, and the refund write must run only once after approval.
- evaluation-ci-gate-near-miss [adk-agent-evaluation, near-miss, dev] PARTIAL PASS: primary adk-release-engineering; supporting adk-agent-evaluation. Wiring eval gates into CI with threshold, repeat and cost policy is release engineering, with the existing eval set run via the evaluation skill.
- fastapi-backend-cross-user-tool-near-miss [adk-fastapi-backend, near-miss, dev] PARTIAL PASS: primary adk-tool-auth-and-secrets; supporting adk-fastapi-backend. Binding a tool to the verified caller to stop cross-user access through the tool is verified ownership at the tool hop, using the backend's verified principal.
- fastapi-backend-session-endpoints-near-miss [adk-fastapi-backend, near-miss, dev] PASS PARTIAL: primary adk-frontend-integration; supporting adk-fastapi-backend. Ownership of the agent's session and run endpoints and the chat error state belong to adk-frontend-integration, with the verified-principal ownership check supported by the backend skill.
- guardrails-approval-card-near-miss [adk-operational-guardrails, near-miss, dev] PASS PARTIAL: primary adk-frontend-integration; supporting adk-operational-guardrails. Approval buttons and the tool timeline after rejection are agent UI states, with the confirmation flow semantics from guardrails.
- guardrails-confirmation-tiering-near-miss [adk-operational-guardrails, near-miss, dev] PARTIAL PARTIAL: primary adk-agent-security; supporting adk-operational-guardrails. Threat-modelling which tools an injected page could abuse and tiering them for confirmation is the security skill, with guardrails covering the human approval mechanics.
- observability-eval-handoff-positive [adk-agent-observability, positive, dev] PARTIAL PARTIAL: primary adk-agent-evaluation; supporting adk-agent-observability,protect-adk-sensitive-data. Building a regression eval set is evaluation work; turning production traces from BigQuery Agent Analytics into cases is observability territory, and PII removal calls for the sensitive-data skill.
- tool-interface-toolset-positive [adk-tool-interface-design, positive, dev] PARTIAL PASS: primary adk-agent-interoperability; supporting adk-tool-interface-design. Consuming an MCP server with tool_filter and prefixes is interoperability, while naming, consolidation and result shaping to avoid context bloat belong to tool interface design.
