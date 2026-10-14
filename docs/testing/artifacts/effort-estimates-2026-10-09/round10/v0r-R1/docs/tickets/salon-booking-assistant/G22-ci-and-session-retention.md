---
goal: G22
title: CI and the 30-day session deletion job
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: adk-release-engineering
supporting_skills: [deploy-adk-on-google-cloud, protect-adk-sensitive-data]
blocked_by: [G08, G09]
phase: 1
profile: MVP or pilot
estimate:                # human hours, agent-assisted
  hands_on: 2-2.5
  review_and_verify: 0.5-1
  total: 2.5-3.5
  calendar_waits: none
owner: Dev A
status: blocked
---

# G22 CI and the 30-day session deletion job

## Outcome

Every push runs the deterministic tests and the scripted evaluation, and conversation sessions older than 30 days are deleted automatically. Implements the CI half of D11 and the session lifetime in design §5. Split out of G09 in the 8-day revision so that it does not gate go-live (G11).

## Scope

- In: CI workflow running `pytest` and `python eval/run.py --scripted` on every push, failing on any failed or missing case; a scheduled job (Cloud Scheduler calling a Cloud Run job, or the team's equivalent) deleting ADK sessions and their events older than 30 days from the G09 Postgres, using the G09 service account; the runbook's "run by hand before deploy" step (G10) marked as replaced by CI.
- Out: Live evaluation gate (G14); erasure on request and operation-record retention (G17).
- Depth: Build (MVP). Floor: the deletion job's credential comes from workload identity, not a key file; the job logs counts and IDs, never message content.
- Notes: Pick up G09's project and database from Dev C and G08's runner from Dev B; handoff 0.5 h included. Not on G11's path: if it slips, deploys keep using the G10 runbook's manual step, and the job must land before the first pilot session is 30 days old.
- Execution scope: CI is local to the repository. The deletion job needs W1's project and the team's approval for the scheduled job and its IAM grant.

## Acceptance

- [ ] A push with a deliberately failing unit test, and one with a scripted evaluation case removed, both fail CI by exit code; the second reports the case as missing.
- [ ] On staging, a session back-dated to 31 days is deleted with its events by one run of the job, and a 29-day session is kept.
- [ ] The job's log lines for that run contain counts and session IDs only, with no message text or fixture names.

Verification: Offline: CI run on a branch. Authorised cloud: one run of the deletion job on staging.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G22-ci-and-session-retention.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
