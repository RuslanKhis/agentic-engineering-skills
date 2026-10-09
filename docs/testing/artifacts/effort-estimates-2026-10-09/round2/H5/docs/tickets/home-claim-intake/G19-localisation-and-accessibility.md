---
goal: G19
title: The assistant works in the local language and meets WCAG 2.1 AA
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: adk-frontend-integration
supporting_skills: [adk-agent-instructions, adk-agent-evaluation]
blocked_by: [G09, G10]
phase: 1
profile: production
estimate:                # human hours, agent-assisted (x1.5 ADK multiplier included)
  hands_on: 32–54
  review_and_verify: 16–26
  total: 48–80
  calendar_waits: Translation of UI copy and disclosure, 1–2 weeks
owner: E4
status: blocked
---

# G19 The assistant works in the local language and meets WCAG 2.1 AA

## Outcome

Customers can complete the journey in the local language and with a screen reader or keyboard only.

## Scope

- In: UI copy localisation, language selection rules, accessibility fixes and audit, local-language eval subset results.
- Out: Second market (G24).
- Depth: Production. Floor: disclosure available in both languages.
- Route: Portal i18n framework; instruction reads the customer's language from trusted state.
- Supporting skills: `adk-agent-instructions` (language handling in the instruction); `adk-agent-evaluation` (local-language subset of the eval set)
- Execution scope: Dev and staging.

## Acceptance

- [ ] Local-language eval subset meets the G16 thresholds
- [ ] Accessibility audit shows no WCAG 2.1 AA failures on the journey
- [ ] Keyboard-only run completes the journey

Verification: Audit tool plus manual check; eval run in dev.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G19-localisation-and-accessibility.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
