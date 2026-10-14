---
goal: G07
title: The team can score the agent and the photo reader with one command
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: adk-agent-evaluation
supporting_skills: [adk-model-and-output-contracts]
blocked_by: [G02]
phase: 1
profile: production
estimate:                # human hours, agent-assisted, ×1.5 for a team new to ADK
  hands_on: 22-34
  review_and_verify: 4-6
  total: 26-40
  calendar_waits: none
owner: ML
status: blocked
---

# G07 The team can score the agent and the photo reader with one command

## Outcome

An evaluation harness and a labelled photo development set: 150 staged and
consented photos (A9) labelled with room, damage types and quality issue, a
runner that scores any agent build, thresholds in a file, and
`evals/SUMMARY.md` with the latest result per case.

## Scope

- In: label schema matching `PhotoObservation`; double labelling of 30
  photos to measure agreement; runner with repeats and cost cap; judge
  pinned separately (D7) for free-text fields only; offline mode replaying
  recorded responses; 1 h handoff from Eng A.
- Out: conversation cases (G24); CI wiring (G17).
- Depth: production; no real customer photos.

## Acceptance

- [ ] `python -m evals.run --suite photos` produces per-case results and a summary with a run ID.
- [ ] Label agreement on the double-labelled 30 is reported; disagreements resolved and recorded.
- [ ] A run with a missing result is reported as missing, not as a pass.
- [ ] No personal data in the repository; consent records kept outside it.

Verification: offline replay run; one bounded live run (≤ 300 model calls).

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G07-eval-harness-photo-set.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
