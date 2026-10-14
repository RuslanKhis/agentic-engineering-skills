---
goal: G09
title: When Maria presses Submit, exactly one claim registration starts and survives any crash
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: safe-api-tool-calls
supporting_skills: [adk-operational-guardrails]
blocked_by: [G04, G06]
phase: 1
profile: production
estimate:                # human hours, agent-assisted, ×1.5 for a team new to ADK
  hands_on: 36-54
  review_and_verify: 14-20
  total: 50-74
  calendar_waits: none
owner: Eng B
mentions_only: [G12]
status: blocked
---

# G09 When Maria presses Submit, exactly one claim registration starts and survives any crash

## Outcome

Implements D2, D3 and invariants I2 and I3 against a Guidewire contract fake:
the confirm endpoint, approval binding to the draft version hash, the
`submission_ledger` state machine and the executor.

## Scope

- In: `POST /claims/{draft_id}/confirm` with `draft_version_hash`; recheck of
  owner and policy entitlement at confirm; ledger row with unique
  `operation_id` committed before any outbound call; states `PENDING →
  CREATED → DOCS_ATTACHED → SUBMITTED / FAILED / UNCERTAIN`; executor with
  bounded retries for transient errors only; a fake provider with
  configurable lost responses, rejections and delays; status endpoint for the
  customer; 3 h handoff from Eng A and Eng E.
- Out: real adapter and reconciler (G10); UI (G12).
- Depth: production; careful review (write that leads to money).

## Acceptance

- [ ] Happy path reaches `SUBMITTED` with the fake's claim number shown via the status endpoint.
- [ ] Double submit and two concurrent confirms produce one ledger row and one provider create.
- [ ] Changed draft after the summary → 409 and no provider call.
- [ ] Provider commits but the response is lost → `UNCERTAIN`; no second create is sent.
- [ ] Process killed between ledger commit and provider call, then restarted → executor resumes the same `operation_id`.
- [ ] The agent's tool list contains no submission tool.

Verification: offline and local integration tests with Postgres and a real
process restart.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G09-confirmed-submission-ledger.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
