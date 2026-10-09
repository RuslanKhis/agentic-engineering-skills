---
goal: G06
title: "A customer can upload photos that are checked and cleaned before anything reads them"
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: protect-adk-sensitive-data
supporting_skills: [adk-tool-auth-and-secrets]
blocked_by: [G04]
phase: 1
profile: production
estimate:                # human hours, agent-assisted, x1.5 included
  hands_on: 12-18
  review_and_verify: 6-9
  total: 18-27
  calendar_waits: none
  wait_days: 0
owner: Frontend eng
status: blocked
---

# G06 A customer can upload photos that are checked and cleaned before anything reads them

## Outcome

Phone photos upload directly to an EU quarantine bucket; only re-encoded, metadata-free copies reach the clean bucket, owned by the customer's draft. Implements D6, I6; route and rationale in the
[plan entry](../../plans/home-claim-intake.md#g06--a-customer-can-upload-photos-that-are-checked-and-cleaned-before-anything-reads-them).

## Scope

- In: Signed upload URL route with type and size limits; sanitiser triggered on finalize; `photo` table with owner, draft, state; 20 photos per draft.
- Out: Photo analysis (G07); attachment to Guidewire (G11).
- Depth: Build.

## Acceptance

- [ ] A JPEG with GPS EXIF arrives in the clean bucket without EXIF.
- [ ] A PDF renamed .jpg, a 40 MB file and a 21st photo are rejected with a clear message.
- [ ] Customer B cannot obtain a URL for or read customer A's photo.

Verification: Local tests with fixtures; dev-project integration test. Execution scope: Dev project only.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G06-photo-upload-and-sanitising.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
