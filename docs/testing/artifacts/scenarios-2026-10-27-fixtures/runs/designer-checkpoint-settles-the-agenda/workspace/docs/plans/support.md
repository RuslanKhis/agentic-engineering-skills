# Implementation plan: support assistant reply language and streaming

Status: in progress (checkpointed after G01, 2026-10-27; cut line is provisional, see Open questions)
Architecture: [docs/architecture/support.md](../architecture/support.md)
Continuation source of truth: this plan and the tickets under `docs/tickets/support/`

## Summary for the reader

- **Profile and phase 1:** proof of concept. After the G01 overrun, phase 1 is cut to: a signed-in
  customer can save and forget a reply language (done except the hard-delete fix), ending in the
  support team's review. Streaming and honest failures (G02-G04) move to phase 2.
- **Effort and finish:** phase 1 is 9-10 human hours (6 h actual on G01, 1 h G06, 2-3 h G05)
  against 10 h capacity; it fits only at the low end. Phase 2 (G02-G04) is 5-9 h more and does
  not fit in the 10 h.
- **Largest risks:** the soft-delete ruling was rejected on an assumption (D4); SSE through IAP
  buffering (G02) is still unproven, so G02 is re-estimated upward; the review date (D3).
- **Decisions needed from you:** (1) the privacy notice and the 30-day retention (D4); (2) the cut
  line: accept it, or raise capacity to about 15-19 h to keep streaming in the review; (3) the
  review date (D3).
- **Next prompt:** `/adk-engineer Carry out docs/tickets/support/G06.md.`

## Delivery profile and capacity

Profile: proof of concept.

| Phase | Delivers | Goals | Human hours, agent-assisted (range) | Capacity and reserve |
| --- | --- | --- | --- | --- |
| 1, ship | save and forget a language, hard delete, review | G01, G06, G05 | 9-10 (G01 actual 6) | 1 × 14 h × 0.7 = 10 h |
| 2, streaming | streamed replies, honest failures, journey check | G02, G03, G04 | 5-9 | not funded; needs more capacity or the review's go-ahead |
| 3, pilot | spend cap, quota, monitoring | later | not estimated | after the review |

Why the cut: G01 took 6 h against 2-3 h, so 6 h of the 10 h is spent. The old remaining work
(G02 to G05, 6-11 h) plus the 1 h hard-delete rework leaves 7-12 h against 4 h left. Not even
the low end fits. The cut keeps the floor: no streaming means no C3 or C5 promise is made in
this slice. Re-estimates (G02 3-5 h, from 2-4 h) account for the hidden-state surprise in G01 and
the unproven IAP buffering; G03 and G04 are left as estimated.

Schedule block (hand-computed; `check_schedule.py` could not be run in this session, rerun it):

```yaml
- goal: G01
  phase: 1
  hands_on: 5
  review: 1
  total: 6
  owner: Ana
  blocked_by: []
  calendar_waits: none
  wait_days: 0
  handoff: 0
  contracts: [C1, C2]
  security: [SB01]
  mentions_only: []
  type: implementation
- goal: G06
  phase: 1
  hands_on: 0.5
  review: 0.5
  total: 1
  owner: Ana
  blocked_by: [G01]
  calendar_waits: none
  wait_days: 0
  handoff: 0
  contracts: [C2]
  security: []
  mentions_only: []
  type: implementation
- goal: G05
  phase: 1
  hands_on: 1.5-2
  review: 0.5-1
  total: 2-3
  owner: Ana
  blocked_by: [G06, D3]
  calendar_waits: D3 review date
  wait_days: 0-5
  handoff: 0
  contracts: []
  security: []
  mentions_only: [C4]
  type: presentation
- goal: G02
  phase: 2
  hands_on: 2.5-4
  review: 0.5-1
  total: 3-5
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
  phase: 2
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
  phase: 2
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
```

The G01 hands-on and review split (5 and 1) is assumed; only the 6 h total was reported.

## Goals and dependencies

| ID and goal | Phase | Type | Human hours | Depends on | Primary skill | State / blocker |
| --- | --- | --- | --- | --- | --- | --- |
| [G01 Save and forget a reply language](../tickets/support/G01.md) | 1 | implementation | 6 actual (est. 2-3) | none | adk-memory-architecture | verified_local; soft-delete ruling rejected |
| [G06 Forget is a hard delete](../tickets/support/G06.md) | 1 | implementation | 1 | G01 | adk-memory-architecture | ready |
| [G05 Phase-1 review presentation](../tickets/support/G05.md) | 1 | presentation | 2-3 | G06, D3 | adk-presenter | waits for D3 |
| [G02 Streamed replies](../tickets/support/G02.md) | 2 | implementation | 3-5 | G01 | adk-frontend-integration | ready, unfunded |
| [G03 Honest failed replies](../tickets/support/G03.md) | 2 | implementation | 1-2 | G01 | adk-frontend-integration | ready, unfunded |
| [G04 Journey check](../tickets/support/G04.md) | 2 | journey | 1-2 | G02, G03 | adk-agent-evaluation | blocked by G02, G03 |

## Open questions and assumptions

| Question | Assumed answer (non-interactive checkpoint) | Depends on it |
| --- | --- | --- |
| Does the privacy notice allow keeping a forgotten preference 30 days, and does support really need the complaint view? | No; hard delete (D4, provisional) | G06, C2, G01 ruling |
| Is capacity still 10 h, or can Ana add about 3-9 h so streaming makes the review? | Still 10 h | cut line, G02-G04 phase |
| Does the review go ahead on the language slice alone? | Yes, G05 shows streaming as the next slice | G05 outline, D3 |

If capacity grows to about 15-19 h, move G02-G04 back to phase 1 and put G05 after G04 again.

## Later

| Item | Trigger that brings it forward | Risk accepted while it waits | Likely primary skill |
| --- | --- | --- | --- |
| C4 spend cap as a Vertex AI quota | pilot approved | a runaway session costs money during the PoC | adk-operational-guardrails |
| Shared household preference | product asks for group accounts | none for individual accounts | adk-memory-architecture |
| 30-day retention and complaint view | privacy notice allows it and support confirms the need | support cannot see a customer's earlier choice | adk-memory-architecture |

## Change log

| Date | Change | By |
| --- | --- | --- |
| 2026-10-14 | Plan accepted with G01-G05 | Ana |
| 2026-10-16 | Ana's availability cut to 14 h; capacity 10 h after reserve | Ana |
| 2026-10-27 | Checkpoint after G01: C2 revised (forget also clears `user:language` in session state; hard delete); C1, C2 and SB01 evidence updated; G01 soft-delete ruling rejected, D4 added (provisional); G06 added (1 h); G02 re-estimated 2-4 to 3-5 h; G02-G04 moved to phase 2 and G05 now depends on G06, not G04, because phase 1 no longer fits the 10 h. Removed or weakened: the phase-1 promise of streaming and failed-reply display, and G04's journey check before the review (moved, not dropped; C3, C5 stay planned, nothing in the floor removed). | checkpoint |

## Resume here

G01 done (verified_local, 6 h actual). Next: G06. Run `/adk-engineer Carry out docs/tickets/support/G06.md.`
Phase 1 base commit: none recorded (the repository has no git history in this workspace).
