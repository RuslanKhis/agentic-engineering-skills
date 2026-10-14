# Implementation plan: salon booking assistant

Status: draft. Ready goals identified.
Architecture: [docs/architecture/salon-booking-assistant.md](../architecture/salon-booking-assistant.md)
Continuation source of truth: this plan, and for phase 1 the tickets in
[`docs/tickets/salon-booking-assistant/`](../tickets/salon-booking-assistant/).

## Summary for the reader

- **Profile and phase 1:** MVP or pilot. Signed-in customers of one pilot
  salon can book, move and cancel appointments in a web chat widget. Every
  change waits for their Confirm and goes through the existing booking API.
- **Effort and finish:** phase 1 is 64–89 human hours against 112.5 h of
  capacity after a 25 % reserve. The hours fit. The finish range is 7.47–10.13
  working days against 10: **the low end fits, and the high end is about one
  hour over.** The gap closes if Dev A protects 6 focused hours a day instead
  of 5, which gives 6.44–9.02 days and fits. The alternative is accepting a
  go-live on day 11.
- **Largest risks:**
  1. The booking API may have no idempotency or no atomic reschedule (A6).
     G01 settles it by day 2, and G03 absorbs the outcome.
  2. The site token may not be verifiable by our service (A5). This is the
     first step of G04, and the fallback is an introspection call.
  3. The salon owner's sign-off (W1) arrives late, which blocks G11 go-live. It
     is requested on day 1.
- **Decisions needed from you:** confirm the assumed answers in the design
  (especially A5, A6, A7 and A9); confirm or move the cut line; decide
  between 6 h a day for Dev A and a day-11 launch; name the pilot salon.
- **Next prompt:** see *Resume here*.

## Destination and constraints

Destination: a kept MVP, so phase 1 code is continued in phase 2. The stack
is Python, ADK (working assumption `google-adk==2.8.0`, which G02 confirms),
`gemini-3.8-flash` on Vertex AI (pinned, D8), FastAPI on Cloud Run, Cloud SQL
Postgres, and the existing booking API and booking website. The repository is
empty apart from `.claude/`, so every module named here is **proposed**:
`app/agent.py`, `app/tools/`, `app/booking_client.py`, `app/operations.py`,
`app/gateway.py`, `app/policy.yaml`, `web/widget/`, `evals/`, `infra/`.

This session authorises design only. Cloud provisioning, IAM and the
production launch each need the team's go-ahead in their own goal.

## Delivery profile and capacity

Profile: MVP or pilot (see the design). Assumptions (A2): three developers at
about 5 focused hours a day for 10 working days, with 25 % held in reserve.
That is 3.75 h a day and 37.5 h each, 112.5 h in total. Every figure already
includes the **×1.5 multiplier for a team new to ADK**. Estimates are whole
person-hours, agent-assisted (hands-on plus review). Calendar waits are their
own entries.

| Phase | Delivers | Goals | Human hours | Capacity |
| --- | --- | --- | --- | --- |
| 1, ship | Pilot salon live: confirmed, idempotent writes, verified identity, a measured evaluation set, runbook | G01–G11, W1 | 64–89 | 112.5 h after reserve |
| 2, graduate to all five salons | CI gate, SLIs, adversarial suite, retention, reconciliation, rollout | G12–G17 | 27–50 | When phase 1 has run |

| Person | Goals | Hours | Capacity |
| --- | --- | --- | --- |
| Dev A: API, writes, infra, launch | G01, G03, G07, G11 | 25–34 | 37.5 |
| Dev B: agent and evaluation | G02, G06, G08, G09 | 19–28 | 37.5 |
| Dev C: identity, frontend, runbook | G04, G05, G10 | 20–27 | 37.5 |

Dev A carries the critical chain and the irreversible-effect code (G03), so
G03's review is done by Dev B. Dev C, with the most slack, is the overflow for
G08 labelling.

```yaml
- goal: W1
  phase: 1
  total: 0
  blocked_by: []
  calendar_waits: salon owner signs off policy windows, pilot salon and privacy notice
  wait_days: 2-4
- goal: G01
  phase: 1
  hands_on: 3-4
  review: 1
  total: 4-5
  owner: Dev A
  blocked_by: []
  calendar_waits: none
- goal: G02
  phase: 1
  hands_on: 4-6
  review: 2-3
  total: 6-9
  owner: Dev B
  blocked_by: []
  calendar_waits: none
- goal: G03
  phase: 1
  hands_on: 5-7
  review: 3-4
  total: 8-11
  owner: Dev A
  blocked_by: [G01]
  calendar_waits: none
- goal: G04
  phase: 1
  hands_on: 6-8
  review: 3-4
  total: 9-12
  owner: Dev C
  blocked_by: []
  calendar_waits: none
- goal: G05
  phase: 1
  hands_on: 6-8
  review: 2-3
  total: 8-11
  owner: Dev C
  blocked_by: [G04]
  calendar_waits: none
- goal: G06
  phase: 1
  hands_on: 3-4
  review: 1-2
  total: 4-6
  owner: Dev B
  blocked_by: [G02, G03]
  calendar_waits: none
- goal: G07
  phase: 1
  hands_on: 6-8
  review: 2-3
  total: 8-11
  owner: Dev A
  blocked_by: [G02]
  calendar_waits: none
- goal: G08
  phase: 1
  hands_on: 5-7
  review: 1-2
  total: 6-9
  owner: Dev B
  blocked_by: [G02]
  calendar_waits: none
- goal: G09
  phase: 1
  hands_on: 2-3
  review: 1
  total: 3-4
  owner: Dev B
  blocked_by: [G06, G08]
  calendar_waits: none
- goal: G10
  phase: 1
  hands_on: 2-3
  review: 1
  total: 3-4
  owner: Dev C
  blocked_by: [G07]
  calendar_waits: none
- goal: G11
  phase: 1
  hands_on: 4-5
  review: 1-2
  total: 5-7
  owner: Dev A
  blocked_by: [G05, G07, G09, G10, W1]
  calendar_waits: none
- goal: G12
  phase: 2
  total: 5-9
  blocked_by: [G11]
- goal: G13
  phase: 2
  total: 5-9
  blocked_by: [G11]
- goal: G14
  phase: 2
  total: 5-9
  blocked_by: [G11]
- goal: G15
  phase: 2
  total: 3-6
  blocked_by: [G11]
- goal: G16
  phase: 2
  total: 4-8
  blocked_by: [G11]
- goal: G17
  phase: 2
  total: 5-9
  blocked_by: [G12, G13, G14, G15]
```

**Schedule check** (run 2026-10-14 with `python3
.claude/skills/adk-system-designer/scripts/check_schedule.py --plan
docs/plans/salon-booking-assistant.md --tickets
docs/tickets/salon-booking-assistant/ --days 10 --reserve 0.25 --person "Dev
A=5" --person "Dev B=5" --person "Dev C=5"`, on Python 3.9.13 rather than the
3.11+ the skill names). Result: 64–89 h, capacity 112.5 h, hours fit. Longest
dependent chain G01 → G03 → G06 → G09 → G11, 6.4–8.8 days. Finish
7.47–10.13 working days. Calendar: **low end only** (exit 1). Same command
with `"Dev A=6"`: finish 6.44–9.02 days, fits (exit 0).

**Changes after failing runs** (each change is true of the work, and no
review or wait was shortened):

| Run | Finish (days) | Change and reason |
| --- | --- | --- |
| First draft: 8 goals, eval after writes | 10.93–15.73 | — |
| Split eval set into labelling (G08) and measured run (G09) | 10.13–14.13 | Labelling needs only the read agent |
| Gateway built against a stub agent (G04 has no prerequisite); token check moved from G01 into G04 | 8.53–12.27 | Identity and ownership code never calls the real agent |
| Policy cases read `policy.yaml`, so G08 no longer waits for W1 | 8.53–11.73 | The labels compute the expected outcome from config |
| G07 to Dev A, G08 to Dev B | 7.47–10.4 | Dev C was the bottleneck |
| Runbook split from launch (G10, Dev C) | 7.47–10.13 | Runbook needs only the deployed service |
| Infra provisioning (G07) after G02 instead of G04 | 7.47–10.13 | Provisioning is independent of the gateway code. The integrated build is deployed in G11 |

Rejected what-ifs: moving G08 to Dev C or G07 to Dev C gave 10.4–12. Cutting
G08 to 20 cases gave 10.4. Trimming G05 gave 10.13. Only more focused hours
for Dev A closes the gap.

**Cut line (confirm or move it):** G01–G11 ship in phase 1, and G12–G17
follow. If the work runs high, these goals stay useful in this order: G01,
G02, G03, G06 (a working agent with safe writes, demoable locally), then G04,
G07, G05, G11. G08 and G09 are required before go-live. The floor inside G03,
G04 and G06 is never trimmed.

## Implementation map

| Decision | Component and integration point (proposed) | GCP | Primary skill |
| --- | --- | --- | --- |
| D1, D5 | `app/agent.py` `LlmAgent` + `app/tools/*.py` + `app/policy.yaml` | Vertex AI | `adk-tool-interface-design` |
| D2, D4 | `app/operations.py` state machine + `confirm_operation()` → `app/booking_client.py` | Cloud SQL | `safe-api-tool-calls` |
| D3, D9 | `app/gateway.py` middleware: token → `customer_id` in trusted state; allowance; `RunConfig(max_llm_calls=12)` | Secret Manager | `adk-tool-auth-and-secrets` |
| D10 | `web/widget/` ↔ `/chat`, `/confirm/{id}`, `/operations/{id}` | — | `adk-frontend-integration` |
| D6, D7, D11 | `DatabaseSessionService`; Cloud Run staging and prod; telemetry content capture off | Cloud Run, Cloud SQL, Secret Manager, Cloud Trace | `deploy-adk-on-google-cloud` |
| D8 | Pinned model ID in config; side-by-side in G09 | Vertex AI | `adk-model-and-output-contracts` |

## Goals and dependencies

The tickets are each phase 1 goal's home. Estimates live in the schedule
block.

| ID and goal | Type | Owner | Depends on | Primary skill |
| --- | --- | --- | --- | --- |
| [G01 Booking API write contract and policy facts](../tickets/salon-booking-assistant/G01-booking-api-contract.md) | discovery | Dev A | — | `safe-api-tool-calls` |
| [G02 Local agent answers availability and "my appointments"](../tickets/salon-booking-assistant/G02-local-agent-read-tools.md) | impl. | Dev B | — | `adk-tool-interface-design` |
| [G03 A confirmed operation changes the booking exactly once](../tickets/salon-booking-assistant/G03-operations-and-confirm.md) | impl. | Dev A | G01 | `safe-api-tool-calls` |
| [G04 Signed-in customer reaches only their own data](../tickets/salon-booking-assistant/G04-identity-gateway.md) | impl. | Dev C | — | `adk-tool-auth-and-secrets` |
| [G05 Chat widget with confirmation card](../tickets/salon-booking-assistant/G05-chat-widget.md) | impl. | Dev C | G04 | `adk-frontend-integration` |
| [G06 Agent proposes book, move and cancel](../tickets/salon-booking-assistant/G06-propose-tools.md) | impl. | Dev B | G02, G03 | `adk-tool-interface-design` |
| [G07 Staging and prod infrastructure on Cloud Run](../tickets/salon-booking-assistant/G07-cloud-run-infra.md) | impl. | Dev A | G02 | `deploy-adk-on-google-cloud` |
| [G08 Labelled evaluation set and runner](../tickets/salon-booking-assistant/G08-evaluation-set.md) | impl. | Dev B | G02 | `adk-agent-evaluation` |
| [G09 Measured run and model freeze](../tickets/salon-booking-assistant/G09-measured-run.md) | impl. | Dev B | G06, G08 | `adk-agent-evaluation` |
| [G10 Runbook, kill switch drill, staff briefing](../tickets/salon-booking-assistant/G10-runbook.md) | impl. | Dev C | G07 | `deploy-adk-on-google-cloud` |
| [G11 Pilot salon goes live](../tickets/salon-booking-assistant/G11-pilot-go-live.md) | impl. | Dev A | G05, G07, G09, G10, W1 | `deploy-adk-on-google-cloud` |

### Phase 2: graduate to all five salons (outline, refined after the pilot)

- **G12 Evaluation gate in CI and release manifest.** Primary
  `adk-release-engineering`. 5–9 h. Acceptance: a PR that lowers the G09
  score below the frozen threshold fails CI, and the manifest records the
  model ID and its lifecycle date.
- **G13 SLIs and alerts.** Primary `adk-agent-observability`. 5–9 h.
  Acceptance: the SLIs are completed changes over proposals, tool error rate
  and tokens per completed change, and an alert fires when uncertain
  operations exceed 1 an hour.
- **G14 Adversarial suite.** Primary `adk-agent-security`. 5–9 h. Acceptance:
  scripted attacks (other customers' IDs, "confirm it for me", instructions
  in notes) produce no write and no disclosure.
- **G15 Retention job.** Primary `protect-adk-sensitive-data`. 3–6 h.
  Acceptance: sessions older than 30 days are gone, and sampled logs contain
  no message text.
- **G16 Automatic reconciliation.** Primary `safe-api-tool-calls`. 4–8 h.
  Acceptance: a simulated lost response is resolved with no human and no
  second booking.
- **G17 Roll out to all five salons.** Primary `adk-agent-instructions`,
  supporting `deploy-adk-on-google-cloud`. 5–9 h. Acceptance: the "which
  salon?" evaluation cases pass, and a customer of salon 3 books there.

## Later

| Item | Trigger | Risk accepted meanwhile | Skill |
| --- | --- | --- | --- |
| SMS or WhatsApp channel | Customers ask for it | Web only | `adk-frontend-integration` |
| Preferred-stylist memory | Repeated "my usual" requests | Customers re-state preferences | `adk-memory-architecture` |
| Streaming replies | Measured p95 above 8 s | Slower feel | `optimise-adk-on-google-cloud` |
| Canary releases | All five salons live | Rollback is manual | `adk-release-engineering` |
| Model migration | Retirement date announced for `gemini-3.8-flash` | — | `adk-model-and-output-contracts` |

## Open decisions for further planning

See the design's *Open decisions*. A6 blocks G03 until G01 is done. A5 is the
first step of G04. W1 blocks G11.

## Resume here

- **Next goal:** G01, owned by Dev A. It is ready and starts the critical
  chain. G02 (Dev B), G04 (Dev C) and the W1 request to the salon owner start
  the same day.
- **Read first:** the design, then the ticket.

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G01-booking-api-contract.md. Read its design and plan, use its primary and supporting skills, run its verification locally, fill in the Evidence section and set status. Leave changes uncommitted.
```

Afterwards: `/adk-engineer Continue the next ready goal in docs/plans/salon-booking-assistant.md.`
