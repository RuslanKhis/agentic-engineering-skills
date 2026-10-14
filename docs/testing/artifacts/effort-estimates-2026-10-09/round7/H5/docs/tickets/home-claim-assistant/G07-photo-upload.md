---
goal: G07
title: Customers upload photos safely
design: ../../architecture/home-claim-assistant.md
plan: ../../plans/home-claim-assistant.md
primary_skill: protect-adk-sensitive-data
supporting_skills: [adk-tool-auth-and-secrets]
blocked_by: [G04, G05]
phase: 1
profile: production
estimate:                # human hours, agent-assisted
  hands_on: 12-18
  review_and_verify: 4-8
  total: 16-26
  calendar_waits: none
owner: Eng A
status: blocked
---

# G07 Customers upload photos safely

## Outcome

Signed-URL upload to the quarantine bucket, server-side validation and a re-encoded metadata-free copy for the model. Implements D6.

## Scope

- In: `app/photos/` routes, magic-byte type check, size ≤ 15 MB, ≤ 20 per draft, re-encode and downscale, owner binding.
- Out: malware scanning product (O5), Guidewire transfer (G09/G11).
- Depth: build; originals never sent to the model.

## Acceptance

- [ ] A JPEG/PNG/HEIC within limits is stored and a derived copy without EXIF exists
- [ ] A renamed executable, an oversized or 21st file is rejected
- [ ] Customer B cannot obtain an upload or read URL for customer A's draft

Verification: Offline with a fake GCS; local integration against a GCS emulator if available.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-assistant/G07-photo-upload.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
