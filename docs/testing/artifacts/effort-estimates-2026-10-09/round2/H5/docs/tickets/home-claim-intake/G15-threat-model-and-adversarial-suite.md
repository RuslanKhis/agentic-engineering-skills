---
goal: G15
title: Security review and pentest find no open critical or high issues
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: adk-agent-security
supporting_skills: [adk-agent-evaluation]
blocked_by: [G07, G08, G09]
phase: 1
profile: production
estimate:                # human hours, agent-assisted (x1.5 ADK multiplier included)
  hands_on: 26–48
  review_and_verify: 14–24
  total: 40–72
  calendar_waits: External pentest booking 2–3 weeks plus a 1-week test window (book in week 6)
owner: SEC + E5
status: blocked
---

# G15 Security review and pentest find no open critical or high issues

## Outcome

Threat model per agent, adversarial suite in CI, pentest done and critical/high findings fixed or accepted by the owner. I1, I3, I5.

## Scope

- In: `docs/security/threat-model.md`; adversarial cases from the design's Security posture; pentest scope letter; remediation PRs.
- Out: Ongoing red-team (later).
- Depth: Production: threat model and adversarial suite. Floor: forbidden actions asserted in code tests.
- Route: Scripted-model tests asserting no forbidden tool call or mutation; OWASP LLM and agentic mapping.
- Supporting skills: `adk-agent-evaluation` (adversarial cases run as deterministic forbidden-action assertions)
- Execution scope: Staging only, within the pentest scope letter.

## Acceptance

- [ ] Every adversarial case asserts the forbidden effect is absent and passes in CI
- [ ] Pentest report received; critical/high findings closed or formally accepted with owner
- [ ] Threat model reviewed by the security reviewer

Verification: Offline suite; authorised pentest against staging.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G15-threat-model-and-adversarial-suite.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
