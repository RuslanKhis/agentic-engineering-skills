---
goal: G09
title: The customer's photos appear on their filed claim, once each
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: safe-api-tool-calls
supporting_skills: []
blocked_by: [G05, G08]
phase: 1
profile: production
estimate:
  hands_on: 14-20
  review_and_verify: 6-9
  total: 20-29
  calendar_waits: none
owner: Eng B
status: proposed
---

# G09 The customer's photos appear on their filed claim, once each

## Outcome

After the claim number exists, each original photo is attached as a
ClaimCenter document through per-photo steps of the submission operation.
Implements D7 (attach steps). Handoff: 1 h from Eng C on photo records.

## Scope

- In: `attach_photo[i]` steps in `app/submission/` using the documents
  calls of the G34 adapter (upload with our document reference, lookup of
  the claim's documents), per-photo state in the status API.
- Out: deleting originals after transfer (G33).
- Depth: production; the claim stays filed whatever happens to photos.

## Acceptance

- [ ] A1 After filing, all photos of the confirmed draft are attached; each has a per-photo state `attached` with the document ID.
- [ ] A2 Three of ten uploads fail with 5xx: the claim stays filed; status shows "7 of 10 photos attached, retrying"; retries complete or end in `needs_ops`; the final count is accurate.
- [ ] A3 An upload whose response is lost or malformed is followed by a lookup of the claim's documents by our reference before any re-upload; two workers on the same photo step attach it once; no duplicate document.
- [ ] A4 A photo ClaimCenter rejects (size or type) is marked `rejected` and the customer is told to send it another way; other photos and the claim are unaffected.
- [ ] A5 The worker attaches only photos linked to this operation's confirmed draft version; a photo from another draft cannot be attached (test).
- [ ] A6 401 and 429 go through the shared Guidewire client (G34) with the operation's retry owner and deadline from G08.

Verification: offline — `pytest tests/submission/test_photos.py` with the
G01 fake.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G09-photo-transfer.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
