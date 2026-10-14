---
goal: G13
title: The DPO and legal have what they need to assess the service
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: protect-adk-sensitive-data
supporting_skills: [adk-agent-security]
blocked_by: []
phase: 1
profile: production
estimate:
  hands_on: 10-16
  review_and_verify: 2-3
  total: 12-19
  calendar_waits: none
owner: Eng E
status: ready
---

# G13 The DPO and legal have what they need to assess the service

## Outcome

Engineering input to the DPIA and the AI Act transparency work, delivered
early so the DPO's review (wait W2, which follows this goal) runs in
parallel with the build. Implements D9 and D16 documentation.

## Scope

- In: `docs/compliance/data-flow.md` (diagram and inventory: fields,
  purposes, lawful basis proposed, retention, processors including Google
  Cloud and Guidewire, regions), disclosure and privacy-notice drafts,
  AI Act classification memo for legal (assumption Q12).
- Out: the DPO's assessment and decision (W2); legal wording.
- Depth: production; updated if G12 changes a retention or region.

## Acceptance

- [ ] A1 The data-flow and inventory cover every store and sink in the design's data table, with regions and retention, and are delivered to the DPO.
- [ ] A2 AI disclosure text (German and English) and privacy-notice changes are drafted and sent to legal.
- [ ] A3 The classification memo states why the service is assumed not to be high-risk under the AI Act, with the open points for legal.

Verification: document review by the DPO and legal; no code.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G13-dpia-input.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
