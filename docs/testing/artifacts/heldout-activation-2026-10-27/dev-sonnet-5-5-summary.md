Activation run: backend claude-cli, model claude-sonnet-5-5, 154 cases x 2 repeat(s), split dev
catalogue 3295a5a6cc395a72  corpus e57980b8cbe62338

| Run | PASS | PARTIAL | FAIL | ERROR |
| --- | --- | --- | --- | --- |
| repeat 1 | 151 | 3 | 0 | 0 |
| repeat 2 | 150 | 4 | 0 | 0 |
| all | 301 | 7 | 0 | 0 |

| Split | PASS | PARTIAL | FAIL | ERROR |
| --- | --- | --- | --- | --- |
| dev | 301 | 7 | 0 | 0 |

Cases not passing in every repeat:
- api-payment-approval-near-miss [safe-api-tool-calls, near-miss, dev] PARTIAL PARTIAL: primary adk-operational-guardrails; supporting safe-api-tool-calls. Human approval for refunds over a threshold with durable review records and next-day resume is the approval flow owned by operational guardrails, with the approved write running once handled by safe-api-tool-calls.
- evaluation-ci-gate-near-miss [adk-agent-evaluation, near-miss, dev] PASS PARTIAL: primary adk-release-engineering; supporting adk-agent-evaluation. Wiring eval gates into CI with threshold, repeat and judge cost policy is explicitly release engineering, using the existing eval set.
- guardrails-confirmation-tiering-near-miss [adk-operational-guardrails, near-miss, dev] PASS PARTIAL: primary adk-agent-security; supporting adk-operational-guardrails. Identifying which tools injected content could abuse and tiering them for confirmation is the lethal-trifecta and tool-tiering work of adk-agent-security, with guardrails covering the approval mechanics.
- instructions-exemplar-measure-near-miss [adk-agent-instructions, near-miss, dev] PARTIAL PASS: primary adk-agent-evaluation; supporting adk-agent-instructions. Measuring exemplar versions on a development set with error categorisation is the evaluation loop, with exemplar design from the instructions skill as support.
- instructions-near-miss [adk-agent-instructions, near-miss, dev] PASS PARTIAL: primary adk-agent-evaluation; supporting adk-agent-instructions. Error analysis on a labelled dev set with one change per iteration and holdout reporting is the measured improvement loop, with instructions supporting the prompt changes.
- observability-eval-handoff-positive [adk-agent-observability, positive, dev] PARTIAL PASS: primary adk-agent-evaluation; supporting protect-adk-sensitive-data,adk-agent-observability. Turning production thumbs-down traces into an evaluation set is evaluation work, with PII removal and the Agent Analytics source as supporting concerns.
