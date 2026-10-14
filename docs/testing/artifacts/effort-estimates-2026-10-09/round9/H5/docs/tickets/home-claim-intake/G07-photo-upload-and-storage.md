---
goal: G07
title: Customers upload damage photos safely to their own draft
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: adk-memory-architecture
supporting_skills: [protect-adk-sensitive-data, adk-tool-auth-and-secrets]
blocked_by: [G04, G05]
phase: 1
profile: production
estimate:                # human hours, agent-assisted; copied from the plan's schedule block
  hands_on: 20-34
  review_and_verify: 6-10
  total: 26-44
  calendar_waits: none
owner: Agent
status: blocked
---

# G07 Customers upload damage photos safely to their own draft

## Outcome

Delivers the upload half of D5/D10 with I1 for photos.

## Scope

- In: `/photos` issues short-lived signed upload URLs for an object path derived from verified `customer_id`/`draft_id`. Finalisation validates type (JPEG/PNG/HEIC), size ≤15 MB and count ≤10, stores sha256 and creates an EXIF-stripped model copy. Lifecycle rule on the bucket.
- Out: Analysis (G08). Attachment to Guidewire (G23). Erasure job (G12).
- Depth: Build. The original is kept for the claim file, and only the stripped copy goes to the model.

Supporting skills and why:
- protect-adk-sensitive-data (EXIF stripping, content-type checks)
- adk-tool-auth-and-secrets (ownership-checked signed URLs)

Route and rationale: see the [design](../../architecture/home-claim-intake.md) decisions named above and the
[plan](../../plans/home-claim-intake.md) implementation map.

## Acceptance

- [ ] An upload for one's own draft succeeds, and the stored model copy has no GPS/EXIF tags (asserted).
- [ ] Asking for an upload URL for another customer's draft returns 404, and no URL is issued.
- [ ] An 11th photo, a 16 MB photo, or a PDF renamed .jpg is rejected with an actionable message.

Verification: Offline with a GCS fake. Authorised live: dev bucket only.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G07-photo-upload-and-storage.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
