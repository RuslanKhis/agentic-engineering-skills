---
goal: G02
title: Pin down the Guidewire FNOL contract and build a contract-faithful fake
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: safe-api-tool-calls
supporting_skills: [adk-tool-auth-and-secrets]
blocked_by: []
phase: 1
profile: production
estimate:                # human hours, agent-assisted; copied from the plan's schedule block
  hands_on: 12-20
  review_and_verify: 4-6
  total: 16-26
  calendar_waits: none
owner: Integration
status: ready
---

# G02 Pin down the Guidewire FNOL contract and build a contract-faithful fake

## Outcome

Resolves O1: how a claim is created, submitted and found again, so D4/I3 can be stated as a guarantee or downgraded honestly.

## Scope

- In: Reading the ClaimCenter Cloud API docs (and the company gateway's docs) for: draft claim create, submit, documents upload, an external-reference field and a search by it, idempotency headers, error codes and timeouts. A local fake server (`tests/fakes/guidewire.py`, proposed) reproduces these, including commit-then-timeout. A list of replay questions for sandbox verification in G10.
- Out: The real submission path (G10). Attachment worker (G23).
- Depth: Discovery plus test fixture. Production depth for the fake: it must model failure windows, not just happy paths.

Supporting skills and why:
- adk-tool-auth-and-secrets (OAuth2 client credentials through the API gateway)

Route and rationale: see the [design](../../architecture/home-claim-intake.md) decisions named above and the
[plan](../../plans/home-claim-intake.md) implementation map.

## Acceptance

- [ ] The decision note answers: can a claim be found by our `op_id` reference, and is that search consistent right after create? Each answer is cited, or marked to be verified in the sandbox.
- [ ] The fake supports success, 4xx validation, 5xx, timeout-after-commit and duplicate create. A test shows each.
- [ ] If no reliable lookup exists, the design's D4/I3 are updated to 'at most one, reconciled by an operator' and the change is flagged to the Lead.

Verification: Offline: `pytest tests/fakes` (proposed). No network calls in this goal.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G02-guidewire-contract-and-fake.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
