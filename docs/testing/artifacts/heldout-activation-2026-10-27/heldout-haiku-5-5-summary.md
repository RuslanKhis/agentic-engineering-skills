Activation run: backend claude-cli, model claude-haiku-5-5, 78 cases x 1 repeat(s), split heldout
catalogue 3295a5a6cc395a72  corpus e57980b8cbe62338

| Run | PASS | PARTIAL | FAIL | ERROR |
| --- | --- | --- | --- | --- |
| repeat 1 | 74 | 3 | 1 | 0 |
| all | 74 | 3 | 1 | 0 |

| Split | PASS | PARTIAL | FAIL | ERROR |
| --- | --- | --- | --- | --- |
| heldout | 74 | 3 | 1 | 0 |

Cases not passing in every repeat:
- api-heldout-3 [safe-api-tool-calls, near-miss, heldout] FAIL: primary safe-api-tool-calls; supporting adk-model-and-output-contracts. Retry and backoff policy for failing API calls belongs to safe-api-tool-calls, and model failover for Gemini 429s falls under the model-and-output skill.
- frontend-heldout-3 [adk-frontend-integration, near-miss, heldout] PARTIAL: primary adk-memory-architecture; supporting adk-frontend-integration. Forgetting earlier turns in a long VertexAiSessionService session is a conversation session and state question, and the user's frontend question is a supporting check on session continuation.
- model-output-heldout-3 [adk-model-and-output-contracts, near-miss, heldout] PARTIAL: primary adk-frontend-integration; supporting adk-model-and-output-contracts. The browser cannot read fields from the event-wrapped response returned by the deployed agent, which is an agent-to-browser contract problem, with output_schema handling as a secondary check.
- workflow-heldout-1 [adk-workflow-design, positive, heldout] PARTIAL: primary adk-agent-instructions; supporting adk-workflow-design. The literal {research_notes} template and the state KeyError are session-state templating problems, and the output_key handoff timing between sequential sub-agents is a workflow concern.
