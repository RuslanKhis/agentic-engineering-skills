Activation run: backend claude-cli, model claude-haiku-5-5, 154 cases x 1 repeat(s)
catalogue 7871f43e531caf26  corpus 1d43aab454fb0165

| Run | PASS | PARTIAL | FAIL | ERROR |
| --- | --- | --- | --- | --- |
| repeat 1 | 145 | 7 | 2 | 0 |
| all | 145 | 7 | 2 | 0 |

Cases not passing in every repeat:
- api-payment-approval-near-miss [safe-api-tool-calls, near-miss] PARTIAL: primary adk-operational-guardrails; supporting safe-api-tool-calls. Human approval with durable review records and a resume flow across days is guardrails work, and the refund write itself must run once only after approval, which is the write side of confirmation.
- fastapi-backend-cross-user-tool-near-miss [adk-fastapi-backend, near-miss] PARTIAL: primary adk-tool-auth-and-secrets; supporting adk-fastapi-backend. Binding a tool to the verified caller so the model cannot choose another user's ID is cross-user access control at the tool hop, and the FastAPI verified-principal dependency supports it.
- fastapi-backend-plain-crud-near-miss [adk-fastapi-backend, near-miss] FAIL: primary adk-fastapi-backend; supporting -. Building a FastAPI CRUD service for an inventory system is backend routes and data work, but it is not an ADK agent application, so the skill fit is weak and it may be unrelated FastAPI work.
- fastapi-backend-session-endpoints-near-miss [adk-fastapi-backend, near-miss] PARTIAL: primary adk-frontend-integration; supporting adk-fastapi-backend. Session continuation on the run and session endpoints and the chat error state belong to frontend integration, while the verified owner check on the session data is backend work.
- guardrails-approved-payment-replay-near-miss [adk-operational-guardrails, near-miss] PARTIAL: primary safe-api-tool-calls; supporting adk-operational-guardrails. Ensuring an approved payment is submitted exactly once despite a timed-out retry is the write-side idempotency problem this skill covers, and the human-approval resume flow is relevant to the approval record.
- instructions-exemplar-measure-near-miss [adk-agent-instructions, near-miss] PARTIAL: primary adk-agent-evaluation; supporting adk-agent-instructions. Scoring two exemplar versions on a labelled development set and categorising errors is the evaluation loop, with the exemplar design itself informed by the instructions skill.
- memory-ingestion-positive [adk-memory-architecture, positive] FAIL: primary none; supporting -. OCR and vision routing for scanned planning documents is document ingestion, which falls outside the catalogue; the memory and retrieval skill covers RAG rather than document preprocessing.
- model-output-deprecation-near-miss [adk-model-and-output-contracts, near-miss] PARTIAL: primary adk-release-engineering; supporting adk-model-and-output-contracts,adk-agent-evaluation. Migrating a released agent to a replacement model with pinned IDs, re-baselining and rollback is release engineering, while choosing the replacement model and re-measuring quality draw on the other two skills.
- observability-eval-handoff-positive [adk-agent-observability, positive] PARTIAL: primary adk-agent-evaluation; supporting protect-adk-sensitive-data,adk-agent-observability. Building a regression eval set from production samples is evaluation work, while the BigQuery Agent Analytics extraction and the personal-data removal fall under observability and sensitive-data handling.
