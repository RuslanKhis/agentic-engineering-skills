# Implementation plan: Coastline claims assistant

Status: in progress
Architecture: [docs/architecture/claims.md](../architecture/claims.md)

## Goals and dependencies

| ID and goal | Phase | Type | Human hours | Depends on | Primary skill | State |
| --- | --- | --- | --- | --- | --- | --- |
| G01 Claim status and notes with owner checks | 1 | implementation | 3-4 | none | adk-tool-auth-and-secrets | complete |
| G02 Recall what the policyholder said before | 1 | implementation | 4-6 | G01 | adk-memory-architecture | ready |
| G03 Streamed chat in the customer portal | 1 | implementation | 3-5 | G01 | adk-frontend-integration | ready |
| G04 No payout promises | 1 | implementation | 2-3 | G01 | adk-agent-security | ready |
| G05 Pilot journey check | 1 | journey | 2-3 | G02, G03, G04 | adk-agent-evaluation | planned |
| G06 Pilot review presentation | 1 | presentation | 2-3 | G05 | adk-presenter | planned |
| G07 Portability assessment for the CTO | 1 | portability | 3-5 | none | adk-portability-planning | not started |

### G02 — Recall what the policyholder said before

- **Phase and estimate:** 1; hands-on 3-4.5, review and verify 1-1.5, total 4-6; calendar waits none; owner Dev A
- **Outcome, contracts and decisions:** a returning policyholder is reminded of what they told the assistant about an open claim; C2, C3; D1, D2.
- **Scope:** recall through `PreloadMemoryTool` and write-back of the session to Memory Bank after each conversation, for policyholders who have not declined. Out: correcting or deleting memories from the portal (G08, later).
- **Depth:** pilot.
- **Implementation route:** `VertexAiMemoryBankService` on the existing Agent Engine (`AGENT_ENGINE_ID`), passed to the Runner in `claims/server.py`; an `after_agent_callback` that writes the session with the verified user ID as scope when the account setting allows; `InMemoryMemoryService` in tests.
- **Resources created:** none (the Agent Engine exists).
- **Primary skill:** adk-memory-architecture
- **Supporting skills:** adk-agent-evaluation (scripted-model Runner tests)
- **Acceptance:**
  - A1 WHEN a policyholder returns to an open claim THE agent SHALL be given the facts they stated in an earlier session (C2)
  - A2 IF another policyholder asks about the same claim number THEN THE agent SHALL be given none of those memories (C2)
  - A3 IF the policyholder declined memory THEN THE app SHALL write nothing to Memory Bank (C3)
- **Verification:** scripted-model Runner tests with `InMemoryMemoryService`, offline; a live recall check on the dev Agent Engine after approval.
- **Execution scope:** local changes only; the live check needs approval.
- **Status and evidence:** ready.

### G07 — Portability assessment for the CTO

- **Primary skill:** adk-portability-planning
- **Outcome:** `docs/portability/claims.md`: what moving to AWS or Azure, or to another agent framework, would involve. Changes no code.
- **Status and evidence:** not started.
