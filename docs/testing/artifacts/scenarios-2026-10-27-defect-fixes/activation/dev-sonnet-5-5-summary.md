Activation run: backend claude-cli, model claude-sonnet-5-5, 172 cases x 2 repeat(s), split dev
catalogue c00a4e0ff95b99ad  corpus ac2f0e7cb0d08f3e

| Run | PASS | PARTIAL | FAIL | ERROR |
| --- | --- | --- | --- | --- |
| repeat 1 | 167 | 5 | 0 | 0 |
| repeat 2 | 164 | 7 | 1 | 0 |
| all | 331 | 12 | 1 | 0 |

| Split | PASS | PARTIAL | FAIL | ERROR |
| --- | --- | --- | --- | --- |
| dev | 331 | 12 | 1 | 0 |

Cases not passing in every repeat:
- api-payment-approval-near-miss [safe-api-tool-calls, near-miss, dev] PASS PARTIAL: primary adk-operational-guardrails; supporting safe-api-tool-calls. Human approval with durable review records and resume after a next-day decision is guardrails, with the write side ensuring the approved refund runs once.
- designer-checkpoint-positive [adk-system-designer, positive, dev] PARTIAL FAIL: primary adk-engineer; supporting adk-system-designer. A mid-build checkpoint of a plan doc with a changed requirement and schedule overrun spans several ADK concerns on an existing application, so the engineer starting point fits, with system-designer for re-scoping the plan.
- evaluation-ci-gate-near-miss [adk-agent-evaluation, near-miss, dev] PASS PARTIAL: primary adk-release-engineering; supporting adk-agent-evaluation. Wiring eval gates into CI with thresholds, repeats and cost caps is release engineering, with eval reliability knowledge supporting.
- fastapi-backend-session-endpoints-near-miss [adk-fastapi-backend, near-miss, dev] PARTIAL PARTIAL: primary adk-frontend-integration; supporting adk-fastapi-backend. Ownership of the agent's run/session endpoints and the chat error state belong to frontend integration, with backend verified-principal support.
- guardrails-approval-card-near-miss [adk-operational-guardrails, near-miss, dev] PASS PARTIAL: primary adk-frontend-integration; supporting adk-operational-guardrails. Approve/reject buttons and the timeline after rejection are agent UI states, while the approval and resume flow comes from guardrails.
- guardrails-confirmation-tiering-near-miss [adk-operational-guardrails, near-miss, dev] PARTIAL PARTIAL: primary adk-agent-security; supporting adk-operational-guardrails. Threat-modelling an agent that reads untrusted content and can act, with tool tiering for confirmation, is adk-agent-security, with approval mechanics in guardrails.
- guardrails-heldout-3 [adk-operational-guardrails, near-miss, dev] PASS PARTIAL: primary adk-agent-observability; supporting adk-operational-guardrails. Attributing Vertex AI spend per agent and alerting on cost is token and cost accounting and monitoring, with staged cost controls as a possible follow-up.
- guardrails-review-dashboard-near-miss [adk-operational-guardrails, near-miss, dev] PASS PARTIAL: primary adk-agent-observability; supporting adk-operational-guardrails. Dashboards and alerts on escalations and queue depth are monitoring work, with guardrails covering the review-queue and escalation-rate concepts.
- observability-eval-handoff-positive [adk-agent-observability, positive, dev] PARTIAL PASS: primary adk-agent-evaluation; supporting protect-adk-sensitive-data,adk-agent-observability. Turning production negative-feedback traces into regression eval cases is evaluation work, needing PII removal and the analytics/trace source knowledge.
- sensitive-data-oauth-token-near-miss [protect-adk-sensitive-data, near-miss, dev] PARTIAL PASS: primary adk-tool-auth-and-secrets; supporting protect-adk-sensitive-data. Keeping delegated OAuth tokens out of state and events is credential lifecycle work, with possible exposure screening as support.
