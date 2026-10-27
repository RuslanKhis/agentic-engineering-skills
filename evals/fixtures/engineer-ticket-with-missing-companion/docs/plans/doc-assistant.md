# Implementation plan: doc assistant

Status: in progress
Architecture: [docs/architecture/doc-assistant.md](../architecture/doc-assistant.md)

## Delivery profile and capacity

Profile: proof of concept, one developer, 16 h capacity after reserve.

```yaml
- goal: G01
  phase: 1
  total: 2-3
  owner: Lea
  blocked_by: []
  contracts: [C1, C4]
  security: [SB01]
  type: implementation
- goal: G02
  phase: 1
  total: 2-3
  owner: Lea
  blocked_by: [G01]
  contracts: [C2]
  type: implementation
- goal: G03
  phase: 1
  total: 3-4
  owner: Lea
  blocked_by: [G02]
  contracts: [C3]
  security: [SB10]
  type: implementation
- goal: G04
  phase: 1
  total: 1-2
  owner: Lea
  blocked_by: [G03]
  contracts: [C1, C2, C3, C4]
  type: journey
```

## Goals and dependencies

| ID and goal | Type | Human hours | Depends on | Primary skill | State |
| --- | --- | --- | --- | --- | --- |
| [G01 Answers with citations](../tickets/doc-assistant/G01.md) | implementation | 2-3 | none | adk-agent-instructions | see ticket |
| [G02 Streamed answers](../tickets/doc-assistant/G02.md) | implementation | 2-3 | G01 | adk-frontend-integration | see ticket |
| [G03 UI shell](../tickets/doc-assistant/G03.md) | implementation | 3-4 | G02 | adk-frontend-integration | see ticket |
| [G04 Journey check](../tickets/doc-assistant/G04.md) | journey | 1-2 | G03 | adk-agent-evaluation | see ticket |
