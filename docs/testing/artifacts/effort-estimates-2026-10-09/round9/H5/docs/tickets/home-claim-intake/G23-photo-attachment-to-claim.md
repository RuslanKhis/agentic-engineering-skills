---
goal: G23
title: Every photo reaches the claim exactly once, or the adjuster is told
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: safe-api-tool-calls
supporting_skills: []
blocked_by: [G07, G10]
phase: 1
profile: production
estimate:                # human hours, agent-assisted; copied from the plan's schedule block
  hands_on: 16-26
  review_and_verify: 6-10
  total: 22-36
  calendar_waits: none
owner: Agent
status: blocked
---

# G23 Every photo reaches the claim exactly once, or the adjuster is told

## Outcome

Implements I8.

## Scope

- In: `PhotoAttachment` rows keyed `(op_id, photo_sha256)`, attachment tasks after CREATED, lookup of existing documents before upload where the G02 contract allows, retry budget, adjuster note listing failed photos.
- Out: Video (Later).
- Depth: Production depth.

Supporting skills and why:
- none

Route and rationale: see the [design](../../architecture/home-claim-intake.md) decisions named above and the
[plan](../../plans/home-claim-intake.md) implementation map.

## Acceptance

- [ ] 4 photos → 4 documents on the claim in the fake and the Guidewire sandbox.
- [ ] A failure after 2 of 4, followed by a worker restart, still ends with 4 documents and no duplicates.
- [ ] A permanent failure of one photo produces an adjuster note naming it. The customer sees 'photos still uploading', then the final state.

Verification: Offline with the G02 fake. Authorised live: Guidewire sandbox.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G23-photo-attachment-to-claim.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
