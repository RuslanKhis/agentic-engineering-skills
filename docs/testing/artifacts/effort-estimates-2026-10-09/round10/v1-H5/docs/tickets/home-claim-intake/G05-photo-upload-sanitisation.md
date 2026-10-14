---
goal: G05
title: A customer's photos are stored safely and a clean copy is ready for the model
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: protect-adk-sensitive-data
supporting_skills: [adk-agent-security]
blocked_by: [G02]
phase: 1
profile: production
estimate:                # human hours, agent-assisted, ×1.5 for a team new to ADK
  hands_on: 18-28
  review_and_verify: 6-10
  total: 24-38
  calendar_waits: none
owner: Eng C
status: blocked
---

# G05 A customer's photos are stored safely and a clean copy is ready for the model

## Outcome

Implements D9's storage half: signed upload URLs to the quarantine bucket,
server-side validation, decode and re-encode, EXIF stripped from the model
copy, original kept for attachment, all keyed by draft and photo ID.

## Scope

- In: `POST /drafts/{id}/photos/upload-url` (owner-checked, ≤ 20 per draft,
  ≤ 15 MB, JPEG/PNG/HEIC); sanitiser with a bounded worker pool; photo
  records on the draft (`received`, `clean`, `rejected`); a local fake for
  GCS in tests; 1 h handoff from Eng A.
- Out: model description (G08); upload UI (G12); retention rules (G13).
- Depth: production; no anti-virus product (A12).

## Acceptance

- [ ] A valid JPEG and a HEIC become clean copies without EXIF; the originals keep theirs.
- [ ] A file with an image extension but other content, a 40 MB file and a 21st photo are each rejected with a customer-readable reason.
- [ ] Uploading to another customer's draft is refused.
- [ ] Re-uploading the same photo ID replaces it without a duplicate record.

Verification: offline tests with fixture files and the GCS fake; a bounded
dev-bucket check once a dev project exists.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G05-photo-upload-sanitisation.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
