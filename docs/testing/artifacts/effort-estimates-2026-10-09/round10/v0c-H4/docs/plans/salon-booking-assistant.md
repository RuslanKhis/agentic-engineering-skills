# Implementation plan: salon booking assistant (MVP)

Status: draft — ready goals identified (assumptions unconfirmed)
Architecture: [../architecture/salon-booking-assistant.md](../architecture/salon-booking-assistant.md)
Continuation source of truth: this plan; phase 1 goal detail lives in
[the tickets](../tickets/salon-booking-assistant/)

## Summary for the reader

- **Profile and phase 1:** MVP. Signed-in customers of all five salons book,
  move and cancel their own appointments in a chat widget in the existing web
  app, each change confirmed by the customer's click and committed once (G01–G11).
- **Effort and finish:** phase 1 is 66–101 human hours against 135 h of
  capacity after a 25 % reserve (fits). Finish 7.2–11.6 working days against
  10 (fits at the low end only). The pilot salon goes live by day 9.6 even at
  the high end; what slips when work runs high is enabling the other four
  salons after the 1–2 day soak, to day 11–12. Two remedies close the gap
  (what-ifs below): launch all five at once, or allow two more working days.
- **Largest risks:** (1) the booking API lacks idempotency keys, so
  at-most-once (I3) needs API work — G01 finds out on day 1, Dev A; (2) the
  chain owner's sign-off on policy, privacy notice and pilot salon (wait W1)
  arrives late — requested on day 1; (3) the team is new to ADK, already
  priced in at ×1.5, and the evaluation (G08) may show the model mishandling
  dates or ambiguity — the reserve and G07's cases cover it; Dev A carries
  the heaviest load (27–41 of 45 h).
- **Decisions needed from you:** confirm the assumed answers A1–A10 in the
  design, especially A5 (no payments), A6 and A7; confirm the cut line
  (pilot salon by day 10, other four after a soak) or choose a remedy below;
  name the pilot salon.
- **Next prompt:** `/adk-engineer Carry out docs/tickets/salon-booking-assistant/G01-booking-api-readiness.md.`
  (G02 and G05 can start the same day; see [Resume here](#resume-here).)

## Destination and constraints

Destination: D1–D12 of the design running on Cloud Run for five salons. Non-goals
and assumptions: design §Purpose and §Assumed answers. Authorization: design
only in this session; no code, cloud resources or dependencies were created.
Repository inspected: empty apart from `.claude/skills/` (no application code,
manifests or tests). All module paths below are **proposed**.

Pinned release artefacts every goal inherits: `google-adk==2.8.0` (to confirm in
G02), model `gemini-3.8-flash` on Vertex AI, prompt version `v1` in
`app/agent/instruction.md`. Changing any of them is a release (G10), not a side
effect.

## Delivery profile and capacity

Profile: MVP or pilot (design §Delivery constraints).

| Phase | Delivers | Goals | Human hours, agent-assisted (range) | Capacity and reserve |
| --- | --- | --- | --- | --- |
| 1, ship | Live for signed-in customers at the pilot salon, then all five | G01–G10 | 66–101 (G01–G11) | 3 people × 6 focused h/day × 10 days = 180 h; 25 % reserve → 135 h |
| 2, harden | Measured outcome, SLO alerts, reconciler, eval growth, preferences | G12–G16 | 26–41 | When phase 1 has run for two weeks |

Estimates are person-hours of human effort with a coding agent (hands-on plus
review and verify), assuming developers new to ADK: the starting points in the
designer's delivery-profiles reference were multiplied by **1.5** for every goal.
Calendar waits are separate entries.

Roles (names unknown; assign each to one developer):

- **Dev A — booking API owner:** knows the existing API; owns the write path.
- **Dev B — agent:** ADK agent, tools, evaluation, CI gate.
- **Dev C — web and platform:** gateway, widget, Cloud Run.

| Person or role | Goals | Hours | Their capacity (6 h/day × 10 days, 25 % reserve) |
| --- | --- | --- | --- |
| Dev A | G01, G04, G07, G11; sends W1 request | 27–41 | 45 |
| Dev B | G02, G03, G08, G10 | 19–30 | 45 |
| Dev C | G05, G06, G09 | 20–30 | 45 |

Handoff hours are inside the receiving goal's hands-on figure and recorded as
`handoff:` in the schedule.

```yaml
- goal: W1
  phase: 1
  total: 0
  calendar_waits: chain owner signs off change policy, privacy notice wording and pilot salon; Dev A sends the request on day 1
  wait_days: 3-5
  blocked_by: []
- goal: G01
  phase: 1
  hands_on: 5-8
  review: 2-3
  total: 7-11
  owner: Dev A
  blocked_by: []
  calendar_waits: none
  wait_days: 0
  handoff: 0
- goal: G02
  phase: 1
  hands_on: 3-5
  review: 2-3
  total: 5-8
  owner: Dev B
  blocked_by: []
  calendar_waits: none
  wait_days: 0
  handoff: 0
- goal: G03
  phase: 1
  hands_on: 3-5
  review: 2-3
  total: 5-8
  owner: Dev B
  blocked_by: [G02]
  calendar_waits: none
  wait_days: 0
  handoff: 0
- goal: G04
  phase: 1
  hands_on: 5-8
  review: 3-4
  total: 8-12
  owner: Dev A
  blocked_by: [G01]
  calendar_waits: none
  wait_days: 0
  handoff: 0
- goal: G05
  phase: 1
  hands_on: 4-6
  review: 2-3
  total: 6-9
  owner: Dev C
  blocked_by: []
  calendar_waits: none
  wait_days: 0
  handoff: 0
- goal: G06
  phase: 1
  hands_on: 4-6
  review: 2-3
  total: 6-9
  owner: Dev C
  blocked_by: [G05]
  calendar_waits: none
  wait_days: 0
  handoff: 0
- goal: G07
  phase: 1
  hands_on: 4-6        # includes 1 h handoff from Dev B (tool names, case format)
  review: 1-2
  total: 5-8
  owner: Dev A
  blocked_by: [G02]
  calendar_waits: none
  wait_days: 0
  handoff: 1
- goal: G08
  phase: 1
  hands_on: 3-4        # includes 1 h handoff from Dev A (labelled cases)
  review: 1-2
  total: 4-6
  owner: Dev B
  blocked_by: [G03, G07]
  calendar_waits: none
  wait_days: 0
  handoff: 1
- goal: G09
  phase: 1
  hands_on: 6-9        # includes 1 h handoff from Dev B (agent factory)
  review: 2-3
  total: 8-12
  owner: Dev C
  blocked_by: [G02, G05]
  calendar_waits: none
  wait_days: 0
  handoff: 1
- goal: G10
  phase: 1
  hands_on: 4-6        # includes 1 h handoff from Dev C (deploy pipeline)
  review: 1-2
  total: 5-8
  owner: Dev B
  blocked_by: [G08, G09]
  calendar_waits: none
  wait_days: 0
  handoff: 1
- goal: G11
  phase: 1
  hands_on: 5-7        # includes 1 h handoff (release candidate, widget, executor)
  review: 2-3
  total: 7-10
  owner: Dev A
  blocked_by: [G03, G04, G06, G10, W1]
  calendar_waits: pilot-salon soak of 1-2 working days before enabling all five
  wait_days: 1-2
  handoff: 1
```

Schedule check, run 2026-10-14 with
`python3.11 -I .claude/skills/adk-system-designer/scripts/check_schedule.py --plan docs/plans/salon-booking-assistant.md --tickets docs/tickets/salon-booking-assistant/ --days 10 --reserve 0.25 --person "Dev A=6" --person "Dev B=6" --person "Dev C=6"`:
phase 1 66–101 h of 135 h (fits); longest chain G02 → G03 → G08 → G10 → G11,
6.8–10.9 working days; finish 7.2–11.6 working days against 10 — **fits at the
low end only** (exit status 1 for that reason alone; tickets agree with the plan).

Changes made after failing runs (each true of the work, none removing a
dependency, wait or review):

| Run | Result | Change and why |
| --- | --- | --- |
| First draft | 61–95 h; finish 7.4–12 days | Handoff hours were recorded but not counted; added 1 h to each receiving goal |
| + handoffs | 65–99 h; finish 7.9–12.4 days | G04 only needs the operations-record shape fixed in D3, not G03's tools: dependency changed to G01 only |
| + G04 decoupled | finish 9–14 days | Staging deploy had wrongly been made to wait for G03/G04; it only needs a servable app (G02 + G05), later goals redeploy through it |
| + staging fixed | finish 7.4–12 days | Chain sat entirely on Dev B; labelling the eval cases (now G07) needs tool names only, so it moved to Dev A after G02, leaving the run (G08) with Dev B |
| Adopted plan | finish 7.2–11.6 days | — |

What-ifs on the adopted plan (helper figures):

| Remedy | Finish (working days) | Closes the gap? |
| --- | --- | --- |
| R1 Launch all five salons at once, no soak (changes A10; risk: an early fault reaches all five) | 6.2–9.6 | Yes |
| R2 Launch without waiting for the CI gate G10 (G08's manual run on the candidate instead) | 7.0–11.1 | No |
| R3 One more working day (11) | 7.2–11.6 | No |
| R4 Two more working days (12) | 7.2–11.6 | Yes |
| R5 Labelling G07 by Dev C instead of Dev A | 8.1–12.7 | No (worse) |
| R6 Dev A gives 7 h/day instead of 6 | 7.3–11.6 | No |

Splitting other chain goals was tried in the runs above; moving goals between
people did not help (R5, and in drafts moving G06, G08 or G09). The figures
assume dedicated developers at 6 focused hours a day (A2).

## Implementation map

| Decision | Component and integration point (proposed) | GCP responsibility | Primary skill | Verification still needed |
| --- | --- | --- | --- | --- |
| D1, D5, D10 (G02, G03) | `app/agent/agent.py` (`LlmAgent` factory), `app/agent/tools/read.py`; booking client `app/booking/client.py` with read scope | Vertex AI model endpoint | `adk-tool-interface-design` | ADK pin; tool declarations as sent |
| D2, D3, D11 (G03, G04) | `app/agent/tools/propose.py` writes `operations` rows; `app/api/confirm.py` executor with write client | Cloud SQL Postgres | `safe-api-tool-calls` | Booking API idempotency (G01) |
| D4, D8 (G05) | `app/api/gateway.py` (FastAPI around `Runner`): JWT/JWKS verification, session ownership, allowance, `RunConfig(max_llm_calls=8)`, kill switch | Secret Manager for API credentials | `adk-tool-auth-and-secrets` | JWT audience/JWKS facts (A7) |
| D7 (G06) | Widget in existing web app; JSON schema `app/api/schema.py` | — | `adk-frontend-integration` | Browser walkthrough |
| D6, D9 (G09) | Dockerfile, Cloud Run service, `DatabaseSessionService` on Cloud SQL, telemetry with content capture off | Cloud Run, Cloud SQL, Secret Manager, Cloud Trace/Logging, budget alert | `deploy-adk-on-google-cloud` | Region prices/quotas recorded |
| D12 (G07, G08, G10) | `evals/cases/*.json`, `evals/run.py`, CI workflow, `release-manifest.json` | CI runner with staging credentials | `adk-agent-evaluation`, `adk-release-engineering` | CI model cost per run |

## Goals and dependencies

| ID and goal | Phase | Type | Human hours | Depends on | Owner | Primary skill | State |
| --- | --- | --- | --- | --- | --- | --- | --- |
| W1 Chain owner sign-off (policy, privacy notice, pilot salon) | 1 | wait, 3–5 days | 0 | — | request: Dev A | — | request day 1 |
| [G01 Booking API ready for safe writes](../tickets/salon-booking-assistant/G01-booking-api-readiness.md) | 1 | discovery + implementation | 7–11 | — | Dev A | `safe-api-tool-calls` | ready |
| [G02 Agent answers read questions locally](../tickets/salon-booking-assistant/G02-agent-read-tools.md) | 1 | implementation | 5–8 | — | Dev B | `adk-tool-interface-design` | ready |
| [G03 Agent proposes bookings, moves and cancellations](../tickets/salon-booking-assistant/G03-proposal-tools.md) | 1 | implementation | 5–8 | G02 | Dev B | `adk-tool-interface-design` | blocked by G02 |
| [G04 Confirmed proposal commits exactly once](../tickets/salon-booking-assistant/G04-confirm-executor.md) | 1 | implementation | 8–12 | G01 | Dev A | `safe-api-tool-calls` | blocked by G01 |
| [G05 Signed-in customer reaches only their own chat](../tickets/salon-booking-assistant/G05-gateway-identity-limits.md) | 1 | implementation | 6–9 | — | Dev C | `adk-tool-auth-and-secrets` | ready |
| [G06 Chat widget with cards and receipts](../tickets/salon-booking-assistant/G06-chat-widget.md) | 1 | implementation | 6–9 | G05 | Dev C | `adk-frontend-integration` | blocked by G05 |
| [G07 Labelled evaluation conversations](../tickets/salon-booking-assistant/G07-eval-cases.md) | 1 | implementation (labelling) | 5–8 | G02 | Dev A | `adk-agent-evaluation` | blocked by G02 |
| [G08 Measured evaluation run](../tickets/salon-booking-assistant/G08-eval-run.md) | 1 | implementation | 4–6 | G03, G07 | Dev B | `adk-agent-evaluation` | blocked |
| [G09 Staging deployment on Cloud Run](../tickets/salon-booking-assistant/G09-staging-deploy.md) | 1 | implementation | 8–12 | G02, G05 | Dev C | `deploy-adk-on-google-cloud` | blocked |
| [G10 Release gate and manifest](../tickets/salon-booking-assistant/G10-release-gate.md) | 1 | implementation | 5–8 | G08, G09 | Dev B | `adk-release-engineering` | blocked |
| [G11 Pilot launch, then all five salons](../tickets/salon-booking-assistant/G11-pilot-launch.md) | 1 | implementation + operation | 7–10 + 1–2 day soak | G03, G04, G06, G10, W1 | Dev A (all three at the walkthrough) | `deploy-adk-on-google-cloud` | blocked |

If a developer is away or time runs out early, the goals stay useful in this
order: G02 → G03 → G01 → G04 gives a locally demonstrable, safe
book/move/cancel; G05 → G09 makes it reachable; G06, G07 and G08 make it usable
and measured; G10 and G11 launch.

### Phase 2 — harden (goals written briefly; detail follows phase 1 results)

- **G12 Grow the eval set from production.** Redact and label 30 reviewed pilot
  sessions into cases; the CI gate runs them. Primary `adk-agent-evaluation`;
  6–9 h. Acceptance: gate fails on a seeded regression from a real case.
- **G13 SLOs and alerts.** SLIs: completed operations / proposals, tool error
  rate by tool, p90 reply time, cost per completed operation; burn-rate alerts
  from the first baseline week. Primary `adk-agent-observability`; 5–8 h.
  Acceptance: a forced booking-API failure pages the owner and links to the session.
- **G14 Background reconciler for uncertain operations.** Scheduled job resolves
  `uncertain` rows by idempotency-key lookup and notifies the customer.
  Primary `safe-api-tool-calls`; 5–8 h. Acceptance: an injected lost reply is
  resolved without a second write.
- **G15 Outcome measurement.** Baseline of phone versus self-service changes per
  salon and the share of chat conversations ending in a receipt. Primary
  `adk-agent-observability`; 4–6 h. Acceptance: weekly report for all five salons.
- **G16 "My usual stylist".** Owner-scoped preference profile loaded at
  invocation; forget command. Primary `adk-memory-architecture`; 6–10 h.
  Acceptance: preference survives a new session, is denied to another customer
  and is deleted on request.

## Later

| Item | Trigger that brings it forward | Risk accepted while it waits | Likely primary skill |
| --- | --- | --- | --- |
| Guest booking (no account) | Chain asks for it; needs phone OTP and abuse limits | Customers without accounts use the web app or phone | `adk-tool-auth-and-secrets` |
| SMS / WhatsApp channel | Chain asks for it | — | `adk-frontend-integration` |
| Deposits or payments | Chain introduces deposits | — (none taken in MVP) | `safe-api-tool-calls` |
| Model Armor / SDP screening | Free-text notes or a new channel | Customer text reaches the model unscreened (own data only) | `protect-adk-sensitive-data` |
| Canary releases | >1,000 conversations/day or a second chain | Rollback is whole-revision | `adk-release-engineering` |
| Streaming replies | Measured time to first content hurts completion | Replies arrive whole | `adk-frontend-integration` |
| Cost and latency tuning | Cost per completed operation or p90 above target | — | `optimise-adk-on-google-cloud` |
| Model migration | Lifecycle table announces a `gemini-3.8-flash` retirement | — | `adk-release-engineering` |

## What the reviewer reads

| Document | Establishes |
| --- | --- |
| [Design](../architecture/salon-booking-assistant.md) | Decisions D1–D12, invariants I1–I6, assumptions |
| `evals/REPORT.md` (written by G08, refreshed by G10) | Latest quality result per case |
| This plan | Schedule, remaining limits and deferred controls |

## Open decisions for further planning

See the design's [Open decisions](../architecture/salon-booking-assistant.md#open-decisions);
they block G04 (A6), G05 (A7) and G11 (A8, A10, privacy notice).

## Resume here

- **Next goal:** G01, because idempotency support decides G04's design; G02
  (Dev B, the start of the longest chain) and G05 (Dev C) are ready and start
  the same day in parallel sessions.
  Dev A also sends the W1 request to the chain owner on day 1.
- **Read first:** the design, then the G01 ticket.
- **Next action:** inspect the booking API's create/reschedule/cancel handlers
  for idempotency-key support.
- **Continuation prompt:**

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G01-booking-api-readiness.md.
```

After that goal, `/adk-engineer Continue the next ready goal in docs/plans/salon-booking-assistant.md.`
