# Implementation plan: support assistant pilot

Status: in progress
Architecture: [docs/architecture/support.md](../architecture/support.md)

## Goals and dependencies

| ID and goal | Phase | Type | Human hours | Depends on | Primary skill | State |
| --- | --- | --- | --- | --- | --- | --- |
| G01 Owner checks on order and refund tools | 1 | implementation | 2-3 | none | adk-tool-auth-and-secrets | verified_local |
| G02 Deploy to Cloud Run dev behind IAP | 1 | implementation | 2-4 | G01 | deploy-adk-on-google-cloud | verified_live |
| [G03 Sessions on Cloud SQL](../tickets/support/G03.md) | 1 | implementation | 3-5 | G02 | adk-memory-architecture | ready |
| G04 Pilot journey check | 1 | journey | 1-2 | G03 | adk-agent-evaluation | planned |
| G05 Pilot review presentation | 1 | presentation | 2-3 | G04 | adk-presenter | planned |
| [G06 Pilot teardown](../tickets/support/G06.md) | 1 | teardown | 1-2 | G05 | deploy-adk-on-google-cloud | planned |

```yaml
- goal: G03
  phase: 1
  hands_on: 2-3.5
  review: 1-1.5
  total: 3-5
  owner: Priya
  blocked_by: [G02]
  calendar_waits: none
  contracts: [C2]
  type: implementation
- goal: G06
  phase: 1
  hands_on: 0.5-1
  review: 0.5-1
  total: 1-2
  owner: Priya
  blocked_by: [G05]
  calendar_waits: none
  contracts: [C3]
  type: teardown
```
