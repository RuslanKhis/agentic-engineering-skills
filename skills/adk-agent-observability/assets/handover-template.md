# Operations handover: <agent name>

Status: draft / accepted by <client role> on <date>
From: <agency or build team> · To: <client IT or platform team>
Release in production: <build tag> · Hypercare: <start> to <end>
Built from: design <path> (contracts, deferred controls), plan <path>
(resources, cost contract), rollout pack <path> (feedback channel, exit test)

## 1. What the agent must never do, and how that is checked

| Contract | Invariant (one line) | Enforcement | Evidence and how to re-run it |
| --- | --- | --- | --- |
| C<n> | | | <test or eval command; last result and date> |

## 2. System map

Host, region, project ID, services, data stores, model and judge IDs (pinned),
external tools and their owners. Link the design's diagram.

## 3. Support tiers and RACI

| Tier | Who (team, contact route) | Handles | Hours |
| --- | --- | --- | --- |
| 1 | Client service desk | User reports, known issues, triage | |
| 2 | Client IT / platform | Alerts, runbook actions, access, cost alerts | |
| 3 | <agency until <date>, then client ADK engineers> | Code, prompt, tool, model changes; root cause | |

Severity table: <Sev1: wrong or unapproved outside action, data exposure,
outage; Sev2: quality drop past threshold, partial outage, a wrong output
that reached a customer; Sev3: a single wrong answer or draft caught by the
human check, single reports> with response targets per tier.

Model-retirement dates come from the lifecycle table for the serving
platform; mark them `refresh before relying` when read offline.

R = responsible, A = accountable (exactly one), C = consulted, I = informed.

| Activity | Service desk | Client IT | Agency | Client product owner | Client DPO |
| --- | --- | --- | --- | --- | --- |
| Sev1 incident response | | | | | |
| Release and rollback | | | | | |
| Model or judge migration before retirement | | | | | |
| Evaluation-set refresh from production samples | | | | | |
| Monthly cost review against the cost contract | | | | | |
| Quarterly access review | | | | | |
| Feedback triage | | | | | |
| Postmortem and action tracking | | | | | |
| Breach notification decision | | | | | |

## 4. Alerts

| Alert policy | Condition | Severity | Channel | Owning tier | Runbook entry |
| --- | --- | --- | --- | --- | --- |
| Telemetry stopped arriving | | | | | |

## 5. Runbook entries

### <alert or task name>

- Symptom:
- First check:
- Safe actions for tier 2: <rollback, disable tool, fallback model, flag>
- Escalate when:
- Approval needed for: <actions with outside effects>
- Rehearsed by tier 2 on: <date>

## 6. Transfer of access

| Item | From | To | Date | Verified by new owner | Old access removed and verified |
| --- | --- | --- | --- | --- | --- |
| Project IAM roles | | | | | |
| Service accounts (no keys) | | | | | |
| Secret Manager secrets and rotation owner | | | | | |
| OAuth client and consent screen | | | | | |
| Billing account link and budget alerts | | | | | |
| Source repository and CI secrets | | | | | |
| Domain and certificate | | | | | |

## 7. Recurring ownership

| Task | Owner | Cadence or date | Source |
| --- | --- | --- | --- |
| Model retirement: <model ID> retires <date> | | <start migration by date> | adk-model-and-output-contracts lifecycle table, read <date> |
| Judge model retirement: <judge ID> | | | |
| Evaluation-set refresh | | <monthly> | adk-release-engineering production feedback |
| Cost review | | <monthly; first bill> | cost contract C<n> |
| Feedback triage | | <weekly> | feedback table |
| Access review | | <quarterly> | |

## 8. Known limits

From deferred controls and gaps, each with the trigger that brings it forward.

## 9. Incident review

Postmortem triggers (agreed): <list>. Template: the agent postmortem template
in this skill; reviews stored at `docs/operations/<topic>/postmortems/`.

## 10. Hypercare exit (operations)

- [ ] Every RACI row has exactly one accountable owner.
- [ ] Every alert routes to a client channel; the telemetry-stopped alert fired once in a test.
- [ ] Every access row verified by the new owner; agency access removed and verified absent (or kept with expiry under the support contract).
- [ ] Every runbook entry rehearsed by tier 2.
- [ ] Model-retirement calendar, evaluation refresh and cost review have owners and dates.
- [ ] The rollout pack's hypercare exit test passed.
