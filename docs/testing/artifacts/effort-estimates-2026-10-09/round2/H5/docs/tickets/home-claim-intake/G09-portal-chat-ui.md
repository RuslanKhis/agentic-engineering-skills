---
goal: G09
title: Customer completes the journey in the portal: chat, photos, summary, confirm, receipt
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: adk-frontend-integration
supporting_skills: [protect-adk-sensitive-data]
blocked_by: [G06, G07]
phase: 1
profile: production
estimate:                # human hours, agent-assisted (x1.5 ADK multiplier included)
  hands_on: 44–72
  review_and_verify: 20–32
  total: 64–104
  calendar_waits: Portal team review of the embedded component, 1 week
owner: E4
status: blocked
---

# G09 Customer completes the journey in the portal: chat, photos, summary, confirm, receipt

## Outcome

The portal hosts the assistant with the AI disclosure, per-turn JSON replies, photo upload, the code-rendered summary card with Submit, and status from the operation record. D8, D14, I9.

## Scope

- In: Application-owned JSON contract (`/turns`, `/photos`, `/drafts/{id}`, `/submit`, `/operations/{id}`); portal component; disclosure banner; status rendering for confirmed/pending/uncertain/rejected; fallback link to the classic form with prefill.
- Out: Localisation and accessibility audit (G19).
- Depth: Production. Floor: card content comes from the stored draft, never model text.
- Route: Custom JSON API (no AG-UI) behind the portal's session; turn IDs and operation IDs as stable identities.
- Supporting skills: `protect-adk-sensitive-data` (guarded release: only screened, completed replies are rendered)
- Execution scope: Dev and staging only.

## Acceptance

- [ ] Browser run of Maria's journey ends with a claim number from the sandbox
- [ ] Uncertain operation shows 'confirming' and later the number; never a retry button
- [ ] Disclosure shown before the first turn; reply HTML-escaped (script in model text renders inert)

Verification: Local integration in a browser against dev; component tests offline.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G09-portal-chat-ui.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
