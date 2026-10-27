# Implementation plan: support assistant reply language and transcripts

Status: in progress
Architecture: [docs/architecture/support.md](../architecture/support.md)
Continuation source of truth: this plan and the tickets under `docs/tickets/support/`

## Summary for the reader

- **Profile and phase 1:** proof of concept; phase 1 lets a signed-in customer save and forget a
  reply language and keep a transcript in their own Drive, ending in the support team's review (D3).
- **Effort and finish:** 8-13 human hours, agent-assisted, against 14 h capacity; fits.
- **Decisions needed from you:** the review date (D3).

## Delivery profile and capacity

Profile: proof of concept. Phase 1 started from commit `4c1e9a2` on `main` (2026-10-15).

| Phase | Delivers | Goals | Human hours, agent-assisted (range) | Capacity and reserve |
| --- | --- | --- | --- | --- |
| 1, ship | language preference, Drive transcripts, journey | G01 to G04 | 8-13 | 1 × 20 h × 0.7 = 14 h |
| 2, pilot | spend cap, bulk delete of history | later | not estimated | after the review |

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
  hands_on: 2-3
  review: 1-1.5
  total: 3-4.5
  owner: Ana
  blocked_by: [G01]
  calendar_waits: none
  wait_days: 0
  handoff: 0
  contracts: [C3, C5]
  security: []
  mentions_only: []
  type: implementation
- goal: G03
  phase: 1
  hands_on: 1-2
  review: 0.5
  total: 1.5-2.5
  owner: Ana
  blocked_by: [G01]
  calendar_waits: none
  wait_days: 0
  handoff: 0
  contracts: [C1]
  security: []
  mentions_only: []
  type: implementation
- goal: G04
  phase: 1
  hands_on: 1-1.5
  review: 0.5-1.5
  total: 1.5-3
  owner: Ana
  blocked_by: [G02, G03]
  calendar_waits: none
  wait_days: 0
  handoff: 0
  contracts: [C1, C2, C3]
  security: [SB01]
  mentions_only: []
  type: journey
```

## Goals and dependencies

| ID and goal | Phase | Type | Human hours | Depends on | Primary skill | State / blocker |
| --- | --- | --- | --- | --- | --- | --- |
| [G01 Save and forget a reply language](../tickets/support/G01.md) | 1 | implementation | 2-3 | none | adk-memory-architecture | see ticket |
| [G02 Transcripts in the customer's Drive](../tickets/support/G02.md) | 1 | implementation | 3-4.5 | G01 | adk-tool-auth-and-secrets | see ticket |
| [G03 Faster first reply](../tickets/support/G03.md) | 1 | implementation | 1.5-2.5 | G01 | adk-memory-architecture | see ticket |
| [G04 Journey check](../tickets/support/G04.md) | 1 | journey | 1.5-3 | G02, G03 | adk-agent-evaluation | see ticket |

The phase-1 review itself (D3) is a meeting with the support lead; its deck is prepared after
this check.

## Later

| Item | Trigger that brings it forward | Risk accepted while it waits | Likely primary skill |
| --- | --- | --- | --- |
| C4 spend cap as a Vertex AI quota | pilot approved | a runaway session costs money during the PoC | adk-operational-guardrails |
| C5 bulk delete of conversation history | pilot approved | customers delete conversations one by one through support | adk-memory-architecture |

## Change log

| Date | Change | By |
| --- | --- | --- |
| 2026-10-14 | Plan accepted with G01-G04 | Ana |
| 2026-10-19 | C2 revised after G01 (session copy cleared on forget) | Ana |
| 2026-10-22 | C5 withdrawn from phase 1 after G02; moved to Later | Ana |

## Resume here

All phase-1 tickets are verified_local. Next: the phase-1 check before the review (D3).
