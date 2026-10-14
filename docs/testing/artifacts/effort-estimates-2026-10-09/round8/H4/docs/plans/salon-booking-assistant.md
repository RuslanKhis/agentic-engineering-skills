# Implementation plan: salon booking assistant (MVP)

Status: draft. Ready goals have been identified, but every scope answer is assumed.
Architecture: [docs/architecture/salon-booking-assistant.md](../architecture/salon-booking-assistant.md)
Continuation source of truth: this plan; phase 1 goal detail is in [the tickets](../tickets/salon-booking-assistant/)

## Summary for the reader

- **Profile and phase 1:** MVP or pilot. Signed-in customers of one pilot salon
  book, move and cancel their own appointments by chat in the existing booking
  web app. Every change goes through a confirmation card they click.
- **Effort and finish:** 67–98 human hours against 135 available after a 25%
  reserve. Finish in 7.1–10 working days against 10, so it **fits, with no
  slack at the high end**. The figures come from `check_schedule.py` (run
  below).
- **Largest risks:** (1) The booking API contract (idempotency key, reschedule
  endpoint) is unknown; G01 settles it on day 1. (2) The chain's sign-off (W1)
  takes longer than 5 days: each extra day moves go-live, not the build (what-if
  below). (3) An uncertain write in the pilot needs manual reconciliation until
  G10; covered by the G09 runbook.
- **Decisions needed from you:** confirm A2 (full-time, about 6 focused h/day
  each) and A3 (about $150/month). Name the pilot salon and the sign-off person
  (A7, A12). Confirm or move the cut line: phase 1 is G01–G09. Automatic
  reconciliation (G10), the CI evaluation gate (G11), the retention purge (G12),
  rollout to all five salons (G13) and the slot-picker UI (G14) wait for phase 2.
- **Next prompt:** `/adk-engineer Carry out docs/tickets/salon-booking-assistant/G01-booking-api-contract-and-fake.md.`

## Destination and constraints

Destination: the design's journey works for real customers of one salon, and
the team can see every operation's outcome and the model cost. Accepted stack
(proposed, D5–D7): Python, FastAPI gateway and ADK Runner on Cloud Run, Cloud
SQL for PostgreSQL, Vertex AI `gemini-3.8-flash`, and `google-adk==2.8.0` as a
working assumption that G01 confirms. The repository holds no application code
yet; every module path in the tickets is a proposed layout. Authorization: this
session was design only. Implementing the goals is a separate request, and
cloud work (G08, G09) needs a named GCP project and someone who may create
resources in it.

## Delivery profile and capacity

| Phase | Delivers | Goals | Human hours, agent-assisted | Capacity and reserve |
| --- | --- | --- | --- | --- |
| 1, ship | Pilot salon live; outcomes and cost visible | G01–G09 (+ wait W1) | 67–98 | 3 people × 6 h × 10 days = 180; 25% reserve → 135 |
| 2, harden and graduate | All five salons; automatic reconciliation; CI gate; retention | G10–G15 | 27–46 (sum of ranges below) | When the team has time after go-live |

Estimates are person-hours of human effort with a coding agent (hands-on plus
review and verify). They already include the ×1.5 multiplier for a team new to
ADK (A2) and one hour of handoff on each goal that picks up another person's
work. Review is heavier on the write path (G03) and the identity boundary (G05)
than on the widget or the evaluation runner.

| Person | Role in phase 1 | Goals | Hours | Their capacity after reserve |
| --- | --- | --- | --- | --- |
| Dev A | Contract, identity, quality | G01, G05, G07 | 23–34 | 45 |
| Dev B | Agent and customer experience | G02, G04, G06 | 22–32 | 45 |
| Dev C | Write path, platform, release | G03, G08, G09 | 22–32 | 45 |

The assignment follows the work, not the people's skills, which were not
known. Swap names freely, but keep each column together, because the finish
range depends on it.

```yaml
- goal: W1
  phase: 1
  total: 0
  blocked_by: []
  calendar_waits: chain owner signs off policies, assistant wording and pilot salon
  wait_days: 3-5
- goal: G01
  phase: 1
  hands_on: 3-4
  review: 1-2
  total: 4-6
  owner: Dev A
  blocked_by: []
  calendar_waits: none
  wait_days: 0
  handoff: 0
- goal: G02
  phase: 1
  hands_on: 6-9
  review: 2-3
  total: 8-12
  owner: Dev B
  blocked_by: [G01]
  calendar_waits: none
  wait_days: 0
  handoff: 1
- goal: G03
  phase: 1
  hands_on: 6-8
  review: 3-4
  total: 9-12
  owner: Dev C
  blocked_by: [G01]
  calendar_waits: none
  wait_days: 0
  handoff: 1
- goal: G04
  phase: 1
  hands_on: 5-7
  review: 2-3
  total: 7-10
  owner: Dev B
  blocked_by: [G02, G03]
  calendar_waits: none
  wait_days: 0
  handoff: 1
- goal: G05
  phase: 1
  hands_on: 6-9
  review: 3-5
  total: 9-14
  owner: Dev A
  blocked_by: [G01]
  calendar_waits: none
  wait_days: 0
  handoff: 0
- goal: G06
  phase: 1
  hands_on: 5-7
  review: 2-3
  total: 7-10
  owner: Dev B
  blocked_by: [G05]
  calendar_waits: none
  wait_days: 0
  handoff: 1
- goal: G07
  phase: 1
  hands_on: 8-11
  review: 2-3
  total: 10-14
  owner: Dev A
  blocked_by: [G02]
  calendar_waits: none
  wait_days: 0
  handoff: 1
- goal: G08
  phase: 1
  hands_on: 6-9
  review: 2-4
  total: 8-13
  owner: Dev C
  blocked_by: []
  calendar_waits: none
  wait_days: 0
  handoff: 0
- goal: G09
  phase: 1
  hands_on: 4-5
  review: 1-2
  total: 5-7
  owner: Dev C
  blocked_by: [G04, G06, G07, G08, W1]
  calendar_waits: W1 sign-off before go-live
  wait_days: 0
  handoff: 1
```

Schedule check, run 2026-10-14 with Python 3.11:

```text
$ python3.11 .claude/skills/adk-system-designer/scripts/check_schedule.py \
    --plan docs/plans/salon-booking-assistant.md \
    --tickets docs/tickets/salon-booking-assistant/ --days 10 --reserve 0.25 \
    --person "Dev A=6" --person "Dev B=6" --person "Dev C=6"
Phase 1: 10 goals, 67-98 human hours
Capacity after reserve: 135 h; fits: yes
  Dev A: 23-34 h of 45 h available
  Dev B: 22-32 h of 45 h available
  Dev C: 22-32 h of 45 h available
Longest dependent chain (low): G01 -> G02 -> G07 -> G09, 6 working days
Longest dependent chain (high): G01 -> G02 -> G07 -> G09, 8.67 working days
Finish with these people and dependencies, 25% of each day held in reserve: 7.11-10 working days
Calendar: 10 working days; fits: yes
(exit status 0)
```

How the plan reached this (each earlier run failed the calendar at the high end):

| Run | Change | Finish (working days) |
| --- | --- | --- |
| 1 | First draft: G01 included the skeleton, G03 included automatic reconciliation, G08 depended on G01 and was owned by Dev B | 8.4–12.7 |
| 2 | G08 moved to Dev C (what-if) | 8.2–12.7, no gain |
| 3 | G08 no longer depends on G01: its infrastructure needs no application code, and it deploys a placeholder until G09. Adversarial cases moved from G09 to G07 with their hour. The widget's slot-picker moved to phase 2 (G14) | 7.6–11.6 |
| 4 | Automatic reconciliation cut from G03 to phase 2 (G10). Phase 1 keeps the floor: uncertain outcomes are recorded, never re-sent, and reconciled by hand. Every owner layout was tried with the helper's analyser; the best was 10.2 | 10.2 at best |
| 5 | Project skeleton and CI moved from G01 to G02 with their hours, so G01 (the shared gate) is shorter. Owners regrouped by role; handoff hours added | 7.1–10, fits |

What-ifs for the sign-off wait W1: at 7–9 days the finish is 8.1–10.6 (low end
only); at 9–10 days it is 10.1–11.6 (does not fit). In both cases the build
finishes on time and only the go-live step in G09 moves. Because the high end
lands exactly on day 10, if time runs out keep this order. After G04, the
assistant books, moves and cancels against the fake API. After G05 and G06, it
does so in the browser. After G08, it runs on staging. The pilot go-live in G09
comes last and is the step that slips.

## Implementation map

| Decision | Component and integration point (proposed) | GCP | Primary skill | Still to verify |
| --- | --- | --- | --- | --- |
| D1, D7 | `assistant/agent.py` agent factory; `assistant/tools/read.py` | Vertex AI | `adk-workflow-design` | ADK pin; model in region |
| D2, D4 | `assistant/tools/propose.py`, `assistant/operations/{store,executor}.py`; `POST /operations/{id}/confirm` | Cloud SQL | `safe-api-tool-calls` | Idempotency key and reschedule in the API (G01) |
| D3, D5, D6, D10 | `gateway/app.py` (FastAPI), token verification, `DatabaseSessionService` | Cloud SQL, Cloud Run | `adk-tool-auth-and-secrets` | Token verification endpoint (G01) |
| D8 | Chat panel in the booking web app | — | `adk-frontend-integration` | Web app framework |
| D9, D11 | Telemetry settings, `release.json` | Cloud Trace, Cloud Logging | `deploy-adk-on-google-cloud` | Current prices |

## Goals and dependencies

Phase 1 goal detail lives in each ticket. This table and the schedule block
above are the only other places that hold a goal's figures.

| ID and goal | Type | Depends on | Primary skill | State |
| --- | --- | --- | --- | --- |
| W1 Chain sign-off on policies, wording, pilot salon | Wait (request on day 1) | — | — | proposed |
| [G01 Booking API contract and fake](../tickets/salon-booking-assistant/G01-booking-api-contract-and-fake.md) | Discovery + implementation | — | `safe-api-tool-calls` | ready |
| [G02 Read-only assistant answers availability and "my appointments"](../tickets/salon-booking-assistant/G02-read-only-assistant.md) | Implementation | G01 | `adk-workflow-design` | blocked by G01 |
| [G03 Operation store and confirm executor](../tickets/salon-booking-assistant/G03-operation-store-and-executor.md) | Implementation | G01 | `safe-api-tool-calls` | blocked by G01 |
| [G04 Book, move and cancel through proposals](../tickets/salon-booking-assistant/G04-proposal-tools.md) | Implementation | G02, G03 | `adk-tool-interface-design` | blocked |
| [G05 Gateway: identity, sessions, allowances](../tickets/salon-booking-assistant/G05-gateway-identity-sessions.md) | Implementation | G01 | `adk-tool-auth-and-secrets` | blocked by G01 |
| [G06 Chat panel with confirmation cards](../tickets/salon-booking-assistant/G06-chat-panel.md) | Implementation | G05 | `adk-frontend-integration` | blocked |
| [G07 Evaluation set with adversarial cases](../tickets/salon-booking-assistant/G07-evaluation-set.md) | Implementation | G02 | `adk-agent-evaluation` | blocked |
| [G08 Staging environment on Cloud Run](../tickets/salon-booking-assistant/G08-staging-environment.md) | Implementation (cloud) | — | `deploy-adk-on-google-cloud` | ready in design; needs a GCP project and authorization |
| [G09 Pilot release and go-live](../tickets/salon-booking-assistant/G09-pilot-release.md) | Implementation (cloud) | G04, G06, G07, G08, W1 | `adk-release-engineering` | blocked |

### Phase 2 (harden and graduate)

- **G10 Automatic reconciliation of uncertain writes.** `safe-api-tool-calls`;
  6–10 h. Accept: a dispatched-then-timed-out booking ends `succeeded` or
  `failed` from the API's own appointment list, with no second dispatch.
- **G11 Evaluation gate in CI.** `adk-release-engineering` with
  `adk-agent-evaluation`; 5–9 h. Accept: a prompt change that breaks a G07 case
  fails CI by exit code.
- **G12 Retention purge and customer deletion.** `protect-adk-sensitive-data`;
  4–7 h. Due before day 30 after launch. Accept: sessions older than 30 days and
  a deleted customer's sessions are gone; the purge is logged.
- **G13 Roll out to all five salons with outcome SLIs.** `adk-agent-observability`;
  5–9 h. Accept: a per-salon flag; dashboards of operations completed versus
  failed or uncertain per salon; an alert on any `uncertain`.
- **G14 Slot-picker buttons.** `adk-frontend-integration`; 3–5 h. Accept: a
  click on a slot sends its `slot_id` and the proposal card follows.
- **G15 Pilot transcripts into evaluation cases.** `adk-agent-observability`
  with `adk-agent-evaluation`; 4–6 h. Accept: 10 reviewed, redacted pilot
  conversations are added to the G07 set.

## Later

| Item | Trigger | Risk accepted while it waits | Likely primary skill |
| --- | --- | --- | --- |
| SMS or WhatsApp channel | The chain asks for it | — | `adk-frontend-integration` |
| Deposits or payments | The chain introduces them | Payments are out of scope until then | `safe-api-tool-calls` |
| Stylist and service preferences across conversations | Repeated "same as last time" requests in transcripts | The customer restates them | `adk-memory-architecture` |
| Model Armor or SDP screening | Free-text notes or a new channel | Customer messages reach the model unscreened (own data only) | `protect-adk-sensitive-data` |
| Streaming replies | Median reply above 6 s | Slower perceived replies | `adk-frontend-integration` |
| Canary releases with comparable samples | More than about 200 conversations a day | Rollback is revision-level only | `adk-release-engineering` |
| Model migration | A shutdown or retirement date appears for `gemini-3.8-flash` | — | `adk-model-and-output-contracts` |
| Load test and tuning | Five salons live, or a holiday peak | Unknown headroom | `optimise-adk-on-google-cloud` |

## What the reviewer reads

| Document | Establishes |
| --- | --- |
| The design | Method and decisions |
| G07's evaluation summary (created by G07) | Latest result per case |
| This plan | Remaining limits and deferred controls |

## Open decisions for further planning

See the design's Open decisions. Of those, the A6 answers change only G03 and
G04 detail; A2 and A3 change this plan's figures and should be confirmed first.

## Resume here

- **Next goal:** G01, booking API contract and fake. It has no prerequisites, and every build goal waits on it.
- **Read first:** the design, then the G01 ticket.
- **Next action:** request W1 from the chain today. In parallel, start G08 if a
  GCP project is available.
- **Continuation prompt:**

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G01-booking-api-contract-and-fake.md.
```

After that: `/adk-engineer Continue the next ready goal in docs/plans/salon-booking-assistant.md.`
