---
goal: G09
title: Upload damage photos safely
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: protect-adk-sensitive-data
supporting_skills: [adk-agent-security, adk-tool-auth-and-secrets]
blocked_by: [G07, G08]
phase: 1
profile: production
estimate:                # human hours, agent-assisted
  hands_on: 12-21
  review_and_verify: 5-8
  total: 17-29
  calendar_waits: none
  wait_days: 0
owner: Dev D
status: blocked
---

# G09 Upload damage photos safely

## Outcome

Customers upload photos by signed URL; the pipeline validates, scans, re-encodes without EXIF and records an owner-scoped photo row. Implements D3, D8, D14, I9; route and rationale in the [plan](../../plans/home-claim-intake.md), entry for this goal ID.

## Scope

- In: Signed-URL route, type/size limits (JPEG, PNG, HEIC; ≤ 15 MB; ≤ 20 per draft), malware scan hook, re-encode, photo table.
- Out: Model reading of photos (G10); transfer to ClaimCenter (G13).
- Depth: Production; scanner choice is an assumption to confirm.

## Acceptance

- [ ] A valid photo appears in the draft's photo list.
- [ ] Oversized, wrong-type and polyglot files are rejected with a reason; EXIF GPS is absent from the stored derivative.
- [ ] Another customer cannot fetch the photo; the original is deleted after re-encode.

Verification: Offline with fixture files and a fake bucket.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G09-photo-upload-pipeline.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
