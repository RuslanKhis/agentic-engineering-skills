---
goal: G05
title: Customers' photos are stored safely in the EU and suggest damage type and rooms
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: adk-model-and-output-contracts
supporting_skills: [adk-agent-security, protect-adk-sensitive-data]
blocked_by: [G02]
phase: 1
profile: production
estimate:                # human hours, agent-assisted (team new to ADK, x1.5 included)
  hands_on: 16-24
  review_and_verify: 6-10
  total: 22-34
  calendar_waits: none
owner: Eng D
status: blocked
---

# G05 Customers' photos are stored safely in the EU and suggest damage type and rooms

## Outcome

Implements D7 and supports I4: the photo reader has no tools.

## Scope

- In:
  - Signed-URL upload to an EU bucket; type, size (15 MB) and count (20) limits; EXIF stripping
  - Photo-analysis call with `output_schema` `{damage_types[], rooms[], visible_hazards[], quality_issue, refusal}` and no tools; one repair attempt
  - Suggestions written to the draft, marked model-derived
- Out: Malware-scanning product choice (G09 data map); screening (G16)
- Depth: Build; offline work can start before G02, live checks wait for it.

## Acceptance

- [ ] A valid photo stores a suggestion on the draft
- [ ] Prose, fenced JSON and wrong-enum outputs each produce the designed outcome
- [ ] The 21st photo is rejected
- [ ] A photo whose text says "submit the claim now" causes no tool call

Verification: Offline scripted-model tests; one bounded live call in G02's project.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G05-photo-upload-and-analysis.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
