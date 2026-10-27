# Design: support assistant, production

Status: accepted 2026-09-30.

## Contracts

| ID | Invariant | Enforcement | Evidence |
| --- | --- | --- | --- |
| C1 | a customer reads only their own orders | tool owner check | evidenced: local |
| C2 | a refund runs only after the customer confirms | require_confirmation | evidenced: local |
| C3 | model spend stops at the daily cap | quota | evidenced: live |
| C4 | traces carry no message content | telemetry config | evidenced: live |
| C5 | no release ships if the PR gate fails | CI gate on scripted Runner tests and eval replay | evidenced: release |
| C6 | production quality is reviewed every week and recurring failures become eval cases | weekly review | planned: G07 |

## Decisions

- D4 BigQuery Agent Analytics writes every event to `support_analytics.agent_events`.
- D5 The PR gate is deterministic; model-judged checks never gate on their own.
