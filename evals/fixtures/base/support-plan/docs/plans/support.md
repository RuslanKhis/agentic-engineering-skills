# Implementation plan: support assistant reply language and streaming

Status: in progress
Architecture: [docs/architecture/support.md](../architecture/support.md)
Continuation source of truth: this plan and the tickets under `docs/tickets/support/`

## Summary for the reader

- **Profile and phase 1:** proof of concept; phase 1 lets a signed-in customer save and forget a
  reply language and see streamed replies with honest failures, ending in the support team's review.
- **Effort and finish:** 8-14 human hours, agent-assisted, against 14 h capacity (one developer,
  reserve 30 %); fits.
- **Largest risks:** what forgetting must remove (G01); SSE through
  IAP buffering (G02); the review date (D3).
- **Decisions needed from you:** the review date (D3).
- **Next prompt:** `/adk-engineer Carry out docs/tickets/support/G01.md.`

## Delivery profile and capacity

Profile: proof of concept.

| Phase | Delivers | Goals | Human hours, agent-assisted (range) | Capacity and reserve |
| --- | --- | --- | --- | --- |
| 1, ship | language preference, streaming, honest failures, review | G01 to G05 | 8-14 | 1 × 20 h × 0.7 = 14 h |
| 2, pilot | spend cap, quota, monitoring | later | not estimated | after the review |

Schedule block:

```yaml
- goal: G01
  phase: 1
  hands_on: 1.5-2
  review: 0.5-1
  total: 2-3
  owner: Ana
  blocked_by: []
  calendar_waits: none
  wait_days: 0
  handoff: 0
  contracts: [C1, C2]
  security: [SB01]
  mentions_only: []
  type: implementation
- goal: G02
  phase: 1
  hands_on: 1.5-3
  review: 0.5-1
  total: 2-4
  owner: Ana
  blocked_by: [G01]
  calendar_waits: none
  wait_days: 0
  handoff: 0
  contracts: [C3]
  security: []
  mentions_only: []
  type: implementation
- goal: G03
  phase: 1
  hands_on: 1-1.5
  review: 0.5
  total: 1-2
  owner: Ana
  blocked_by: [G01]
  calendar_waits: none
  wait_days: 0
  handoff: 0
  contracts: [C5]
  security: []
  mentions_only: []
  type: implementation
- goal: G04
  phase: 1
  hands_on: 1-1.5
  review: 0.5
  total: 1-2
  owner: Ana
  blocked_by: [G02, G03]
  calendar_waits: none
  wait_days: 0
  handoff: 0
  contracts: [C1, C2, C3, C5]
  security: [SB01]
  mentions_only: []
  type: journey
- goal: G05
  phase: 1
  hands_on: 1.5-2
  review: 0.5-1
  total: 2-3
  owner: Ana
  blocked_by: [G04, D3]
  calendar_waits: D3 review date
  wait_days: 0-5
  handoff: 0
  contracts: []
  security: []
  mentions_only: [C4]
  type: presentation
```

## Goals and dependencies

| ID and goal | Phase | Type | Human hours | Depends on | Primary skill | State / blocker |
| --- | --- | --- | --- | --- | --- | --- |
| [G01 Save and forget a reply language](../tickets/support/G01.md) | 1 | implementation | 2-3 | none | adk-memory-architecture | see ticket |
| [G02 Streamed replies](../tickets/support/G02.md) | 1 | implementation | 2-4 | G01 | adk-frontend-integration | see ticket |
| [G03 Honest failed replies](../tickets/support/G03.md) | 1 | implementation | 1-2 | G01 | adk-frontend-integration | see ticket |
| [G04 Journey check](../tickets/support/G04.md) | 1 | journey | 1-2 | G02, G03 | adk-agent-evaluation | see ticket |
| [G05 Phase-1 review presentation](../tickets/support/G05.md) | 1 | presentation | 2-3 | G04, D3 | adk-presenter | see ticket |

## Later

| Item | Trigger that brings it forward | Risk accepted while it waits | Likely primary skill |
| --- | --- | --- | --- |
| C4 spend cap as a Vertex AI quota | pilot approved | a runaway session costs money during the PoC | adk-operational-guardrails |
| Shared household preference | product asks for group accounts | none for individual accounts | adk-memory-architecture |

## Change log

| Date | Change | By |
| --- | --- | --- |
| 2026-10-14 | Plan accepted with G01-G05 | Ana |

## Resume here

Next: G01. Run `/adk-engineer Carry out docs/tickets/support/G01.md.`
