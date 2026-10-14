# Implementation plan: salon booking assistant (MVP)

Status: draft — ready goals identified (G01, and W1 to request on day 1)
Architecture: [../architecture/salon-booking.md](../architecture/salon-booking.md)
Continuation source of truth: this plan and the tickets in
[../tickets/salon-booking/](../tickets/salon-booking/)

## Summary for the reader

- **Profile and phase 1:** MVP/pilot. Phase 1 delivers a website chat in which a
  signed-in customer books, moves or cancels their own appointment after
  pressing Confirm on a card, live at **one pilot salon**, with the other four
  enabled once the go-live criteria in G10 hold (G14, phase 2).
- **Effort and finish:** 62–95 human hours (agent-assisted) against 135 hours
  available after a 25% reserve; fits. Finish 6–9.1 working days against 10;
  **fits** (schedule check, 2026-10-14), assuming 6 focused hours a day each.
  At 5 focused hours a day it finishes in 7.2–10.9 days and needs one more
  working day (tested); see *Cut line*.
- **Largest risks:** (1) the booking API has no safe way to tell whether a
  timed-out write happened — G01 finds out, G03 designs for it; (2) customer
  sign-in on the website cannot be verified by our backend — G01 finds out,
  G04 has a fallback; (3) the operations manager's sign-off (W1) arrives late
  — request it on day 1.
- **Decisions needed from you:** confirm assumptions A2, A3, A6, A8 and A10 in
  the [design](../architecture/salon-booking.md#assumed-answers); confirm or
  move the cut line below.
- **Next prompt:** `/adk-engineer Carry out docs/tickets/salon-booking/G01-booking-api-contract.md.`

## Destination and constraints

Destination and non-goals: design, *Purpose and constraints*. Stack (proposed,
nothing installed yet): Python 3.11, google-adk 2.8.0 as working assumption
(confirm in G02), FastAPI, PostgreSQL, Cloud Run, Vertex AI with the pinned
model in D6. The repository holds no application code yet; every module path
in the tickets is a **proposed** layout:

```text
app/agent.py          LlmAgent factory and instruction loading
app/tools/            read and propose tools
app/booking_client.py booking-API adapter (real + fake)
app/operations.py     operation record and confirm/execute
app/gateway.py        FastAPI: auth, allowance, /chat, /operations
prompts/booking_agent/instruction.md
widget/               embeddable chat widget
evals/                labelled cases and runner
```

Authorization: design only so far. Each ticket authorizes local work; cloud
steps in G08 and G10 need the GCP project, the booking-API sandbox credential and,
for G10, the operations manager's go-ahead.

## Delivery profile and capacity

Profile: MVP or pilot (design, *Delivery constraints*).

| Phase | Delivers | Goals | Human hours, agent-assisted | Capacity and reserve |
| --- | --- | --- | --- | --- |
| 1, ship | Pilot salon live with safe book/move/cancel | G01–G10, W1 | 62–95 | 3 people × 6 focused h/day × 10 days, 25% reserve → 135 h |
| 2, harden and graduate | All five salons; eval gate, traces, reconciliation, staff handoff | G11–G15 | 23–41 (not schedule-checked) | When phase 1 is live |

Estimates are human hours (hands-on plus review and verify), already
**multiplied by 1.5 for a team new to ADK**, applied to every goal. Handoff hours
for picking up another person's work are inside the receiving goal's hands-on
figure and repeated as `handoff:` for the checker.

Owners are roles; map them to the three developers:

| Person | Strength assumed | Goals | Hours | Capacity after reserve |
| --- | --- | --- | --- | --- |
| Dev A, agent lead | Prompting, evaluation, Python | G02, G07, G08 | 20–31 | 45 |
| Dev B, backend | Knows the booking API | G01, G03, G05 | 20–29 | 45 |
| Dev C, web and platform | Website auth, frontend | G04, G06, G09, G10 | 22–35 | 45 |

```yaml
- goal: W1
  phase: 1
  total: 0
  blocked_by: []
  calendar_waits: operations manager approves privacy notice, pilot salon and staff briefing slot
  wait_days: 2-4
- goal: G01
  phase: 1
  hands_on: 2-3
  review: 1
  total: 3-4
  owner: Dev B
  blocked_by: []
  calendar_waits: none
  wait_days: 0
  handoff: 0
- goal: G02
  phase: 1
  hands_on: 3-5
  review: 1-2
  total: 4-7
  owner: Dev A
  blocked_by: [G01]
  calendar_waits: none
  wait_days: 0
  handoff: 1
- goal: G03
  phase: 1
  hands_on: 6-9
  review: 3-5
  total: 9-14
  owner: Dev B
  blocked_by: [G01]
  calendar_waits: none
  wait_days: 0
  handoff: 0
- goal: G04
  phase: 1
  hands_on: 4-6
  review: 2-4
  total: 6-10
  owner: Dev C
  blocked_by: [G01]
  calendar_waits: none
  wait_days: 0
  handoff: 1
- goal: G05
  phase: 1
  hands_on: 5-7
  review: 3-4
  total: 8-11
  owner: Dev B
  blocked_by: [G02, G03, G04]
  calendar_waits: none
  wait_days: 0
  handoff: 1
- goal: G06
  phase: 1
  hands_on: 6-9
  review: 2-3
  total: 8-12
  owner: Dev C
  blocked_by: [G02, G04]
  calendar_waits: none
  wait_days: 0
  handoff: 1
- goal: G07
  phase: 1
  hands_on: 6-9
  review: 2-3
  total: 8-12
  owner: Dev A
  blocked_by: [G02]
  calendar_waits: none
  wait_days: 0
  handoff: 0
- goal: G08
  phase: 1
  hands_on: 6-9
  review: 2-3
  total: 8-12
  owner: Dev A
  blocked_by: [G02]
  calendar_waits: none
  wait_days: 0
  handoff: 0
- goal: G09
  phase: 1
  hands_on: 3-5
  review: 1-2
  total: 4-7
  owner: Dev C
  blocked_by: [G02, G04]
  calendar_waits: none
  wait_days: 0
  handoff: 1
- goal: G10
  phase: 1
  hands_on: 3-4
  review: 1-2
  total: 4-6
  owner: Dev C
  blocked_by: [G05, G06, G07, G08, G09, W1]
  calendar_waits: none
  wait_days: 0
  handoff: 1
```

Schedule check, run 2026-10-14 with
`python3.11 .claude/skills/adk-system-designer/scripts/check_schedule.py --plan docs/plans/salon-booking.md --tickets docs/tickets/salon-booking/ --days 10 --reserve 0.25 --person "Dev A=6" --person "Dev B=6" --person "Dev C=6"`:

| Figure | Result |
| --- | --- |
| Phase 1 hours | 62–95 of 135 after reserve; fits |
| Load | Dev A 20–31, Dev B 20–29, Dev C 22–35, each of 45 |
| Longest dependent chain | G01 → G03 → G05 → G10: 5.3 (low) – 7.8 (high) working days |
| Finish with these people | 6–9.1 working days against 10; fits |

| Change after a failing run | Why |
| --- | --- |
| First run (go-live and security tests as one goal, 7–11 h) finished in 6.7–10.2 days: high end over 10 | — |
| Split it into G09 (adversarial and privacy tests, needs only G02 and G04) and G10 (pilot go-live, at the end of the chain); one extra handoff hour | True of the work: the tests are written against the booking fake and need neither the confirm flow nor staging; only the final run and go-live wait for G05 |

| What-if at 5 focused h/day each | Finish (working days) | Closes the gap? |
| --- | --- | --- |
| Plan as written, 10 days | 7.2–10.9 | No |
| Plan as written, 11 days | 7.2–10.9 | Yes: one more working day |
| Move G08 (staging) from Dev A to Dev B, +1 h handoff | 8.8–12.8 | No: Dev B becomes the bottleneck |
| Split the operation store out of G03 to Dev A | 8.5–13.1 | No: Dev A becomes the bottleneck |

**Cut line.** Ships in phase 1: G01–G10 (pilot salon live). Waits: G11–G15,
including the four-salon rollout (G14). If the team has nearer 5 focused hours
a day, keep the scope and plan the pilot for day 11. If time runs out anyway,
the goals stay useful in this order: G01–G05 give a working, safe agent behind
a test page; G06 and G08 make it reachable; G07, G09 and G10 make it
trustworthy enough for real customers. **Do not** cut G05's confirm step, the
cross-customer tests in G04 or the adversarial cases in G09 to save time — they
are the floor; move the pilot date instead.

## Implementation map

| Decision | Component and integration point (proposed) | GCP responsibility | Primary skill | Verification still needed |
| --- | --- | --- | --- | --- |
| D1, D6, D7 | `app/agent.py` LlmAgent; read tools in `app/tools/`; Runner owned by `app/gateway.py` | Vertex AI model endpoint | `adk-workflow-design` (G02) | Pin and model ID in region |
| D4 | `app/booking_client.py`, `app/operations.py` | Cloud SQL Postgres | `safe-api-tool-calls` (G03) | Booking API write semantics (G01) |
| D3 | `app/gateway.py` token verification → session state | Secret Manager for verification key | `adk-tool-auth-and-secrets` (G04) | Site auth (G01) |
| D2 | `propose_*` tools + `POST /operations/{id}/confirm` | — | `adk-operational-guardrails` (G05) | ADK confirmation limits not used |
| D10 | `widget/` + `/chat` JSON contract | Static hosting on the existing site | `adk-frontend-integration` (G06) | Embedding on the real site |
| D5, D8, D9 | Cloud Run service, allowances, deletion sweep, logs | Cloud Run, Cloud SQL, Secret Manager, Billing budget | `deploy-adk-on-google-cloud` (G08) | Region, prices |
| Eval, instruction | `prompts/`, `evals/` | — | `adk-agent-evaluation` (G07) | Labelled cases |
| Security posture | Adversarial and privacy tests against the fake | — | `adk-agent-security` (G09) | — |
| D11, go-live | Staging run on the booking sandbox, runbook, checklist, pilot flag | Cloud Run release | `deploy-adk-on-google-cloud` (G10) | Sandbox end to end |

## Goals and dependencies

Phase 1 goals live in their tickets (scope, route, acceptance, run prompt);
estimates and owners live in the schedule block above.

| ID and goal | Phase | Type | Depends on | Primary skill | State |
| --- | --- | --- | --- | --- | --- |
| W1 Request go-live sign-off | 1 | wait (no hours) | — | — | request on day 1 |
| [G01 Booking API and sign-in contract](../tickets/salon-booking/G01-booking-api-contract.md) | 1 | discovery | — | `safe-api-tool-calls` | ready |
| [G02 Agent answers availability questions](../tickets/salon-booking/G02-agent-skeleton-read-tools.md) | 1 | implementation | G01 | `adk-workflow-design` | blocked by G01 |
| [G03 Safe booking writes](../tickets/salon-booking/G03-booking-writes-operation-record.md) | 1 | implementation | G01 | `safe-api-tool-calls` | blocked by G01 |
| [G04 Customer sees only their own appointments](../tickets/salon-booking/G04-customer-identity-scope.md) | 1 | implementation | G01 | `adk-tool-auth-and-secrets` | blocked by G01 |
| [G05 Customer confirms a proposed change](../tickets/salon-booking/G05-propose-confirm-flow.md) | 1 | implementation | G02, G03, G04 | `adk-operational-guardrails` | blocked |
| [G06 Chat widget with confirm cards](../tickets/salon-booking/G06-chat-api-and-widget.md) | 1 | implementation | G02, G04 | `adk-frontend-integration` | blocked |
| [G07 Instruction and evaluation set](../tickets/salon-booking/G07-instruction-and-eval-set.md) | 1 | implementation | G02 | `adk-agent-evaluation` | blocked by G02 |
| [G08 Staging on Cloud Run with limits](../tickets/salon-booking/G08-cloud-run-staging-limits.md) | 1 | implementation | G02 | `deploy-adk-on-google-cloud` | blocked by G02 |
| [G09 Adversarial and privacy tests](../tickets/salon-booking/G09-adversarial-privacy-tests.md) | 1 | implementation | G02, G04 | `adk-agent-security` | blocked |
| [G10 Pilot salon goes live](../tickets/salon-booking/G10-pilot-go-live.md) | 1 | implementation | G05–G09, W1 | `deploy-adk-on-google-cloud` | blocked |

**W1** is a request, not work: on day 1 the tech lead sends the operations
manager the privacy-notice draft (D9), asks them to pick the pilot
salon and a staff-briefing slot, and asks for two weeks of reception call
counts as the baseline.

### Phase 2 — harden and graduate (not ticketed; write tickets after the pilot)

- **G11 Eval gate in CI.** Primary `adk-release-engineering`, supporting
  `adk-agent-evaluation`. 5–9 h. Acceptance: a pull request that breaks a
  labelled case fails CI by exit code; manifest records model ID, prompt
  version and eval-set hash.
- **G12 Traces, cost per completed booking and alerts.** Primary
  `adk-agent-observability`. 6–10 h. Acceptance: one span per agent, tool and
  model call with the session ID; alert on confirm-endpoint error rate and on
  `uncertain` operations; no message content in spans.
- **G13 Uncertain-operation sweep.** Primary `safe-api-tool-calls`. 5–9 h.
  Acceptance: a scheduled job reconciles `executing` rows older than 5 minutes
  by lookup and pages staff for the rest; a fake that committed is marked
  `succeeded` without a second write.
- **G14 Enable the remaining four salons.** Primary `deploy-adk-on-google-cloud`.
  2–4 h. Acceptance: the G10 go-live criteria hold for the pilot salon;
  enabling a salon is a config change with a recorded release.
- **G15 Hand off to salon staff.** Primary `adk-tool-interface-design`,
  supporting `adk-agent-instructions`. 5–9 h. Acceptance: "I want to talk to
  someone" produces a callback request in the salon's existing inbox, with no
  conversation content beyond what the customer approved.

## Later

| Item | Trigger that brings it forward | Risk accepted while it waits | Likely primary skill |
| --- | --- | --- | --- |
| Streaming replies | p50 complete reply > 6 s in G10/G12 measurements | Customers wait with a typing indicator | `adk-frontend-integration` |
| SMS or WhatsApp channel | Operations manager asks; > 30% of moves still by phone | Phone-only customers unserved | `adk-frontend-integration` |
| Preferences memory ("my usual with Priya") | Repeated requests seen in sampled sessions | Customer restates preferences | `adk-memory-architecture` |
| Model Armor / SDP screening | A second channel or staff-written free text enters the context | Minimisation only (D9) | `protect-adk-sensitive-data` |
| Canary releases and joint rollback | All five salons live and weekly releases | Whole-revision rollback only | `adk-release-engineering` |
| Model migration to the next Flash | Lifecycle table shows a retirement for the pinned model | — | `adk-model-and-output-contracts` |
| Cost and latency tuning | Cost > USD 0.05 per conversation or budget alert at 90% | — | `optimise-adk-on-google-cloud` |
| Deposits or cancellation fees | Salon policy introduces them | Not supported; would be a money effect needing idempotent payment design | `safe-api-tool-calls` |
| Languages beyond English | Customer requests in sampled sessions | English only | `adk-agent-instructions` |

## What the reviewer reads

| Document | Establishes |
| --- | --- |
| [Design](../architecture/salon-booking.md) | Decisions, invariants, failure handling |
| `evals/README.md` (created in G07) | Latest result per case, linked to run records |
| This plan | Schedule, cut line, deferred controls |

## Open decisions for further planning

| Decision / question | Known facts and alternatives | Evidence or user decision needed | Blocks which goals? |
| --- | --- | --- | --- |
| A2 verifiable website sign-in | Assumed yes; fallback one-time code | G01 reading the site's auth | G04 scope and estimate |
| A3 booking API write semantics | Assumed no idempotency keys, reschedule exists | G01 | G03 route |
| A6 cancellation policy | Assumed free until 24 h, no fees | Operations manager | G05 policy rule |
| A8/A10 pilot salon and sign-off | Assumed one salon, 2–4 days | W1 | G10 |
| Cut line | G01–G10 in phase 1 | You | Whether G14 moves into phase 1, or the pilot moves to day 11 |

## Resume here

- **Next goal:** G01, booking API and sign-in contract — it has no
  prerequisites and decides G03 and G04. Send the W1 request the same day.
- **Read first:** the design, then G01's ticket.
- **Next action:** Dev B reads the booking API's write endpoints and the
  website's sign-in, and fills G01's decision record.
- **Continuation prompt:**

```text
/adk-engineer Carry out docs/tickets/salon-booking/G01-booking-api-contract.md.
Read docs/architecture/salon-booking.md and preserve its accepted decisions.
Use safe-api-tool-calls with adk-tool-auth-and-secrets.
Work locally, read only the booking API and website code or docs, record the
decision in the ticket's Evidence section, and update A2/A3 in the design.
```

After that goal, the same request without a goal ID continues with the next
ready one: `/adk-engineer Continue the next ready goal in docs/plans/salon-booking.md.`
