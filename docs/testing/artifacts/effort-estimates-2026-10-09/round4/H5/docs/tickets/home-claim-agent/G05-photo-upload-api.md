---
goal: G05
title: A customer can attach up to ten photos safely to their draft
design: ../../architecture/home-claim-agent.md
plan: ../../plans/home-claim-agent.md
primary_skill: protect-adk-sensitive-data
supporting_skills: []
blocked_by: [G03]
phase: 1
profile: production
estimate:                # human hours, agent-assisted (×1.5 new-to-ADK multiplier included)
  hands_on: 18-30
  review_and_verify: 8-14
  total: 26-44
  calendar_waits: none
  wait_days: 0
owner: Eng C
status: proposed
---

# G05 A customer can attach up to ten photos safely to their draft

## Outcome

Implements the ingest half of D9: only real images, bounded size and count, metadata removed, stored under the owner's draft.

## Scope

- In: `POST /drafts/{id}/photos` in `app/photos/`: magic-byte check (JPEG, PNG, HEIC), ≤ 15 MB, ≤ 10 per draft, re-encode to JPEG without EXIF, write to `drafts/{draft_id}/`, record on the draft; 30-day lifecycle rule (in `infra/`).
- Out: Photo description (G06), UI (G11), live bucket check (G16).
- Depth: Production depth. Floor: objects not public; owner check; no photo content in logs.

## Acceptance

- [ ] After upload, a test photo's EXIF including GPS is absent
- [ ] A polyglot file, a 16 MB file and an 11th photo are each rejected with an actionable message
- [ ] Another customer cannot read or list the object; the object is not publicly readable
- [ ] No photo bytes or EXIF values appear in logs

Verification: Offline against a GCS fake: `pytest tests/photos` (proposed).

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-agent/G05-photo-upload-api.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
