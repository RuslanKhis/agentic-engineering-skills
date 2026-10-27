Activation run: backend claude-cli, model claude-haiku-5-5, 163 cases x 1 repeat(s), split dev
catalogue 74e4ed4293f09ed1  corpus df13231d2053304f

| Run | PASS | PARTIAL | FAIL | ERROR |
| --- | --- | --- | --- | --- |
| repeat 1 | 151 | 11 | 1 | 0 |
| all | 151 | 11 | 1 | 0 |

| Split | PASS | PARTIAL | FAIL | ERROR |
| --- | --- | --- | --- | --- |
| dev | 151 | 11 | 1 | 0 |

Cases not passing in every repeat:
- api-payment-approval-near-miss [safe-api-tool-calls, near-miss, dev] PARTIAL: primary adk-operational-guardrails; supporting safe-api-tool-calls. Human approval of risky actions with durable review records and a confirm-then-resume flow is guardrail work, and the refund write must run exactly once after approval.
- auth-pasted-secret-near-miss [adk-tool-auth-and-secrets, near-miss, dev] PARTIAL: primary protect-adk-sensitive-data; supporting adk-tool-auth-and-secrets. Detecting and masking API keys and card numbers before the model, history and logs see them is sensitive-data screening, and key handling touches credential custody.
- designer-checkpoint-positive [adk-system-designer, positive, dev] FAIL: primary none; supporting -. Checkpointing a plan document after a scope change and hour overrun does not match any catalogue skill's design, evaluation, or presentation purpose.
- evaluation-ci-gate-near-miss [adk-agent-evaluation, near-miss, dev] PARTIAL: primary adk-release-engineering; supporting adk-agent-evaluation. Wiring evaluation gates into CI with repeat, judge-cost and threshold policy is release-engineering, while the existing eval set and its flaky-case repeats draw on the evaluation skill.
- fastapi-backend-cross-user-tool-near-miss [adk-fastapi-backend, near-miss, dev] PARTIAL: primary adk-tool-auth-and-secrets; supporting adk-fastapi-backend. Binding a tool to the verified caller so it cannot act for another user is tool-hop ownership enforcement, with the verified-principal dependency in the FastAPI backend as a supporting concern.
- fastapi-backend-session-endpoints-near-miss [adk-fastapi-backend, near-miss, dev] PARTIAL: primary adk-frontend-integration; supporting adk-fastapi-backend. Owning the run/stream endpoint's session continuation and its error state in the chat is frontend-integration work, and the caller ownership check relies on the verified-principal dependency from the backend skill.
- frontend-heldout-3 [adk-frontend-integration, near-miss, dev] PARTIAL: primary optimise-adk-on-google-cloud; supporting adk-frontend-integration. Forgetting earlier turns in a long session is in-session history and context growth, which this skill covers, and the frontend skill is needed to check whether the session endpoints are part of the problem.
- guardrails-confirmation-tiering-near-miss [adk-operational-guardrails, near-miss, dev] PARTIAL: primary adk-agent-security; supporting adk-operational-guardrails. Threat-modelling which tools an injected page could abuse and which need a human in the loop is a whole-agent security review, with approval policy as a supporting concern.
- model-output-deprecation-near-miss [adk-model-and-output-contracts, near-miss, dev] PARTIAL: primary adk-release-engineering; supporting adk-model-and-output-contracts,adk-agent-evaluation. A model-version migration with re-baselining, pinned model IDs in the release manifest and rollback is release lifecycle work, with model selection and eval re-baselining as supporting concerns.
- observability-eval-handoff-positive [adk-agent-observability, positive, dev] PARTIAL: primary adk-agent-evaluation; supporting protect-adk-sensitive-data,adk-agent-observability. Building a regression eval set from production conversations is evaluation work, the PII removal needs sensitive-data controls, and the source is a BigQuery Agent Analytics table.
- system-designer-scope-gate-positive [adk-system-designer, positive, dev] PARTIAL: primary adk-discovery; supporting adk-system-designer. Deciding what to build first and what to leave out under a tight time budget is scoping a proof of concept, which the system designer skill covers, and discovery picks the first use case.
- tool-interface-toolset-positive [adk-tool-interface-design, positive, dev] PARTIAL: primary adk-agent-interoperability; supporting adk-tool-interface-design. Exposing a 40-tool MCP server calls for MCP tool_filter and prefix decisions, and tool-count budgets and result shaping to limit context use come from the interface design skill.
