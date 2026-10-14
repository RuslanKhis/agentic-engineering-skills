---
goal: G14
title: Report damage from the portal page with chat, draft, photos and confirm
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: adk-frontend-integration
supporting_skills: []
blocked_by: [G07, G08]
phase: 1
profile: production
estimate:                # human hours, agent-assisted
  hands_on: 24-42
  review_and_verify: 6-11
  total: 30-53
  calendar_waits: none
  wait_days: 0
owner: Dev C
status: blocked
---

# G14 Report damage from the portal page with chat, draft, photos and confirm

## Outcome

A portal page streams chat, shows the live draft, uploads photos and submits on Confirm with status from receipts. Implements D11, I3, I5; route and rationale in the [plan](../../plans/home-claim-intake.md), entry for this goal ID.

## Scope

- In: SSE chat, draft panel, upload widget, review and Confirm sending version and hash, status view, reconnect.
- Out: Languages, accessibility, AI notice (G22).
- Depth: Production.

## Acceptance

- [ ] Text arrives incrementally over a real socket; tool updates refresh the draft panel.
- [ ] Confirm sends version and hash; the claim number appears only after a receipt; uncertain shows pending.
- [ ] Disconnect and reopen restores the draft and last complete reply.

Verification: Local integration: browser test against the local backend with fake model and fake ClaimCenter.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G14-customer-ui.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
