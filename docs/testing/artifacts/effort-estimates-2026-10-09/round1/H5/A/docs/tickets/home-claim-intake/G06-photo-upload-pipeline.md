---
goal: G06
title: A customer uploads photos that are validated, kept as evidence and minimised before any model sees them
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: protect-adk-sensitive-data
supporting_skills: [adk-tool-auth-and-secrets, adk-agent-security]
blocked_by: [G04]
phase: 1
profile: production
estimate: 48-72 h
status: blocked
---

# G06 A customer uploads photos that are validated, kept as evidence and minimised before any model sees them

## Outcome

Photos go by signed URL to a quarantine location, are validated by magic bytes and size, the original is retained and an EXIF-stripped downscaled model copy is produced; each photo is bound to the customer's draft. Implements D4, I1, I7, I9 (photo cap) in the design.

## Scope

- In: `POST /drafts/{id}/uploads` issuing a signed URL; finalise endpoint; validation and re-encode in `app/photos/`; per-draft cap (20); lifecycle rules (30 days) described for G16; local storage emulation for tests.
- Out: Extraction (G07), attaching to Guidewire (G10/G11), face redaction (P2-04).
- Depth: Build; floor: model copy has no EXIF/GPS; originals never served back to another customer.
- Route: Storage adapter interface with a local filesystem implementation for tests and a GCS implementation configured in G16.
- Prerequisites: G04; DPO answer on EXIF in originals (open decision) — default keeps originals unmodified for evidence.
- Supporting skills:
  - `adk-tool-auth-and-secrets`: owner-bound, short-lived signed upload URLs
  - `adk-agent-security`: hostile file handling (type confusion, decompression bombs)
- Execution scope: Local only: repository files, local Postgres/containers, scripted models and fake Guidewire. No cloud, IAM, Guidewire or paid model calls.

## Acceptance

- [ ] A JPEG with GPS EXIF yields an original identical to the upload and a model copy with no EXIF and longest side ≤ 1,600 px.
- [ ] A renamed non-image, an oversize file and a 21st photo are rejected with a user-facing reason.
- [ ] Forbidden: customer B cannot obtain an upload URL or read a photo of customer A's draft.

Verification: Offline tests with fixture images including a decompression-bomb PNG.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G06-photo-upload-pipeline.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
