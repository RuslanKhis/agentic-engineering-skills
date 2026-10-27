Activation run: backend claude-cli, model claude-sonnet-5-5, 178 cases x 2 repeat(s), split dev
catalogue 1156bd511cea6af7  corpus 1b1176c4e0116a18

| Run | PASS | PARTIAL | FAIL | ERROR |
| --- | --- | --- | --- | --- |
| repeat 1 | 172 | 5 | 1 | 0 |
| repeat 2 | 172 | 5 | 1 | 0 |
| all | 344 | 10 | 2 | 0 |

| Split | PASS | PARTIAL | FAIL | ERROR |
| --- | --- | --- | --- | --- |
| dev | 344 | 10 | 2 | 0 |

Cases not passing in every repeat:
- api-payment-approval-near-miss [safe-api-tool-calls, near-miss, dev] PARTIAL PARTIAL: primary adk-operational-guardrails; supporting safe-api-tool-calls. Human approval for refunds with durable review and resume after a day is guardrails work, and the write must run only once after approval.
- designer-checkpoint-positive [adk-system-designer, positive, dev] FAIL PASS: primary adk-engineer; supporting -. A mid-build checkpoint of a plan with a scope change in an existing ADK project is a cross-cutting engineering and planning request, starting from the general engineer skill.
- evaluation-ci-gate-near-miss [adk-agent-evaluation, near-miss, dev] PARTIAL PARTIAL: primary adk-release-engineering; supporting adk-agent-evaluation. Wiring an existing eval set into CI with repeat, cost cap and threshold policy is release engineering; evaluation skill helps with eval reliability.
- fastapi-backend-session-endpoints-near-miss [adk-fastapi-backend, near-miss, dev] PASS PARTIAL: primary adk-frontend-integration; supporting adk-fastapi-backend. The agent's run/stream/session endpoints and their ownership, plus the chat error state, belong to adk-frontend-integration, with the verified-principal ownership check supported by the FastAPI backend skill.
- guardrails-confirmation-tiering-near-miss [adk-operational-guardrails, near-miss, dev] PARTIAL PARTIAL: primary adk-agent-security; supporting adk-operational-guardrails. Identifying which tools an injected page could abuse and tiering which need confirmation is security tool tiering; approval mechanics are a guardrails concern.
- guardrails-review-dashboard-near-miss [adk-operational-guardrails, near-miss, dev] PARTIAL PARTIAL: primary adk-agent-observability; supporting adk-operational-guardrails. A dashboard and alert on escalations and review-queue depth is monitoring and alert design, with the review-queue semantics informed by the guardrails skill.
- observability-eval-handoff-positive [adk-agent-observability, positive, dev] PARTIAL FAIL: primary adk-agent-evaluation; supporting protect-adk-sensitive-data,adk-agent-observability. Turning production negative-feedback traces into a regression eval set is evaluation work, with PII removal and the analytics source as supporting concerns.
