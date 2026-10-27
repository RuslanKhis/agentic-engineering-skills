Activation run: backend claude-cli, model claude-sonnet-5-5, 78 cases x 2 repeat(s), split heldout
catalogue 3295a5a6cc395a72  corpus e57980b8cbe62338

| Run | PASS | PARTIAL | FAIL | ERROR |
| --- | --- | --- | --- | --- |
| repeat 1 | 75 | 1 | 2 | 0 |
| repeat 2 | 77 | 1 | 0 | 0 |
| all | 152 | 2 | 2 | 0 |

| Split | PASS | PARTIAL | FAIL | ERROR |
| --- | --- | --- | --- | --- |
| heldout | 152 | 2 | 2 | 0 |

Cases not passing in every repeat:
- api-heldout-3 [safe-api-tool-calls, near-miss, heldout] FAIL PASS: primary safe-api-tool-calls; supporting adk-operational-guardrails. Handling 429 errors from Gemini with retries and backoff is selective retry policy, with loop-protection concerns as secondary.
- engineer-heldout-1 [adk-engineer, positive, heldout] FAIL PASS: primary adk-system-designer; supporting adk-frontend-integration,adk-memory-architecture. The user wants the feature mapped across UI, backend, persistence and Cloud Run to scope work and ownership, which is a cross-cutting design task.
- guardrails-heldout-3 [adk-operational-guardrails, near-miss, heldout] PARTIAL PASS: primary adk-agent-observability; supporting adk-operational-guardrails. Per-agent token/cost accounting and alerting on spend is observability; enforcing staged cost controls is only secondary, and general billing administration is excluded.
- model-output-heldout-3 [adk-model-and-output-contracts, near-miss, heldout] PASS PARTIAL: primary adk-frontend-integration; supporting adk-model-and-output-contracts. The frontend must consume the remote Agent Runtime's event-wrapped responses, an agent-to-browser contract issue, with output schema handling as secondary.
