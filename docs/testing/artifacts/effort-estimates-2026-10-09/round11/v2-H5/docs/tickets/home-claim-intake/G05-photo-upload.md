---
goal: G05
title: The customer uploads damage photos and the assistant sees safe copies
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: protect-adk-sensitive-data
supporting_skills: [adk-tool-auth-and-secrets]
blocked_by: [G02, G03, G16]
phase: 1
profile: production
estimate:
  hands_on: 14-20
  review_and_verify: 5-8
  total: 19-28
  calendar_waits: none
owner: Eng C
status: proposed
---

# G05 The customer uploads damage photos and the assistant sees safe copies

## Outcome

Photos go straight from the browser to a private EU bucket; the service
validates them and attaches re-encoded, location-free derivatives to the next
model turn. Implements D5. Handoff: 2 h from Eng A and Eng E.

## Scope

- In: `POST /v1/drafts/{id}/photos` (signed URL, 15 min, path
  `customer/draft/photo_id`), finalize handler (content sniffing, size and
  count limits, re-encode to ≤ 1536 px, EXIF stripped), photo records table,
  derivative attachment as image parts in the Runner call.
- Out: transfer to ClaimCenter (G09), retention jobs (G12), UI (G10).
- Depth: production; originals are never sent to the model.

## Acceptance

- [ ] A1 JPEG, PNG and HEIC up to 20 MB upload by signed URL; at most 20 photos per draft; the URL expires after 15 minutes and only writes its own object path.
- [ ] A2 A file whose content is not an allowed image, over 20 MB, or the 21st photo is rejected with a user message and its object deleted.
- [ ] A3 The derivative is ≤ 1536 px with no EXIF (GPS included); a captured model request contains derivatives only.
- [ ] A4 Customer B cannot obtain an upload URL, record or derivative for customer A's draft (404).
- [ ] A5 A duplicate finalize notification for the same object yields one photo record.
- [ ] A6 A corrupt image is rejected without a model call.
- [ ] A7 Storage unavailable or an expired signed URL shows an upload error; a retry gets a new URL; no photo record exists without its object.

Verification: offline with a storage fake for A2–A6; A1 and A7 (expiry,
path scope, expired URL) against the staging bucket from G16.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G05-photo-upload.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
