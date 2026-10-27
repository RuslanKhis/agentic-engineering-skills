Activation run: backend claude-cli, model claude-haiku-5-5, 154 cases x 1 repeat(s), split dev
catalogue 3295a5a6cc395a72  corpus e57980b8cbe62338

| Run | PASS | PARTIAL | FAIL | ERROR |
| --- | --- | --- | --- | --- |
| repeat 1 | 147 | 4 | 3 | 0 |
| all | 147 | 4 | 3 | 0 |

| Split | PASS | PARTIAL | FAIL | ERROR |
| --- | --- | --- | --- | --- |
| dev | 147 | 4 | 3 | 0 |

Cases not passing in every repeat:
- designer-checkpoint-positive [adk-system-designer, positive, dev] FAIL: primary adk-engineer; supporting adk-memory-architecture. The checkpoint covers a multi-ticket ADK build whose scope changed, and redefining forgetting a preference involves memory erasure boundaries.
- evaluation-exemplar-edit-near-miss [adk-agent-evaluation, near-miss, dev] PARTIAL: primary adk-agent-instructions; supporting adk-agent-evaluation. Balancing few-shot exemplars and matching the required output format is exemplar design within prompt wording, and checking the classifier's effect on labelled cases belongs to evaluation.
- fastapi-backend-cross-user-tool-near-miss [adk-fastapi-backend, near-miss, dev] PARTIAL: primary adk-tool-auth-and-secrets; supporting adk-fastapi-backend. Binding a tool's user identity to the verified caller so a model argument cannot read another user's orders is tool-hop ownership, and the FastAPI verified-principal dependency supports it.
- fastapi-backend-session-endpoints-near-miss [adk-fastapi-backend, near-miss, dev] FAIL: primary adk-fastapi-backend; supporting adk-frontend-integration. Rejecting continuation of sessions the caller does not own concerns the agent's run/session endpoints and ownership checks, which the frontend-integration skill owns, while the error state in the chat is UI work for that same skill.
- guardrails-approval-card-near-miss [adk-operational-guardrails, near-miss, dev] PARTIAL: primary adk-frontend-integration; supporting adk-operational-guardrails. Approve and reject buttons and the post-rejection timeline are agent UI states and approval interface design, while the approval policy itself lies with guardrails.
- guardrails-confirmation-tiering-near-miss [adk-operational-guardrails, near-miss, dev] PARTIAL: primary adk-agent-security; supporting adk-operational-guardrails. Assessing which tools an injected page could abuse is whole-agent threat modelling, and deciding which actions need human review is handled by the guardrails skill's approval mechanics.
- portability-migration-build-near-miss [adk-portability-planning, near-miss, dev] FAIL: primary adk-portability-planning; supporting deploy-adk-on-google-cloud. Rewriting an ADK agent in LangGraph and deploying on AWS is building or migrating an application on another platform, which this skill's exclusions rule out, so the closest match is the portability planning skill for assessing it, with deployment noted as a separate concern.
