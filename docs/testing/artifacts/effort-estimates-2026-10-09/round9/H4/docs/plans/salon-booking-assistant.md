# Implementation plan: salon booking assistant

Status: draft, with ready goals identified. The assumed answers A1–A10 in the design are not yet confirmed.
Architecture: [docs/architecture/salon-booking-assistant.md](../architecture/salon-booking-assistant.md)
Continuation source of truth: this plan's schedule block plus the phase 1 tickets in
[docs/tickets/salon-booking-assistant/](../tickets/salon-booking-assistant/). The tickets are each goal's home.

## Summary for the reader

- **Profile and phase 1:** MVP. Within 10 working days, signed-in customers of
  the **pilot salon** can use a chat widget on the salon website to see
  availability and to book, move and cancel their own appointments. Each change
  is confirmed by the customer's click and carried out through the existing
  booking API. The other four salons follow in the first days of phase 2 (G12),
  once the pilot meets the graduation conditions in design §2.
- **Effort and finish:** phase 1 needs 56–88.5 human hours (agent-assisted)
  against 112.5 hours of capacity after a 25 % reserve. The schedule check gives
  a finish of 6.13–9.87 working days against 10, so it **fits, with little
  slack at the high end**. The longest dependent chain is G01 → G04 → G06 → G11
  (8.27 working days at the high end).
- **Largest risks:** (1) The booking API may lack an idempotency key, so a lost
  write response is uncertain. G01 finds out and the D5 reconciliation covers
  it (Dev A). (2) The existing customer login may not be verifiable by our
  backend (A4). G03 finds out on day 1; the email one-time-code fallback costs
  6–10 h and would push G11 past day 10 (Dev C). (3) The model may misstate
  times or policy. G08 measures this, and G11 gates the pilot on the result
  (Dev B).
- **Decisions needed from you:** confirm or correct A1–A10 in the design,
  especially A4 (login), A5 (no deposits) and A7 (policy window). Confirm the
  cut line below, or choose one extra working day instead.
- **Next prompt:** `/adk-engineer Carry out docs/tickets/salon-booking-assistant/G01-booking-api-contract-and-fake.md.`
  Dev C can start G03 the same day.

## Destination and constraints

Destination, non-goals and decisions: design §1 and D1–D12. No application
code exists yet; the repository holds only the skill packages, so every module
path is **proposed**: `app/` (FastAPI app, agent, tools, operations),
`prompts/booking_agent/`, `web/widget.js`, `eval/`, `tests/`. Every goal
inherits the working pins `google-adk==2.8.0` (the specialists' checked version,
confirmed in G02) and `gemini-3.8-flash` on Vertex AI (D2), plus the prompt
version in `prompts/booking_agent/`. A goal that changes any of these is a
release and records it in `release.json` (D11). No credentials or private
resource identifiers belong in these documents.

Authorization: this session was design only. Goals are ready in design. Local
work needs nothing further. G06's staging check, G09, G10 and G11 need W1's
staging key and GCP project, and the team's approval for each deployment and
for the pilot.

## Delivery profile and capacity

Profile: MVP or pilot (design §2).

| Phase | Delivers | Goals | Human hours, agent-assisted | Capacity and reserve |
| --- | --- | --- | --- | --- |
| 1, ship | Real customers of the pilot salon book, move and cancel their own appointments safely; the team sees failures and cost | G01–G11 | 56–88.5 | 3 people × 5 focused h/day × 10 days = 150 h; 25 % reserve → 112.5 h |
| 2, graduate and harden | All five salons, slot cards, live evaluation gate, adversarial suite, SLOs, erasure, automated reconciliation | G12–G19 | 38–64 (rough, re-estimated after G11) | After the pilot, as time allows |

Estimates are person-hours of human effort for a developer with a coding
agent: hands-on work plus review and verification. Every figure, hands-on and
review alike, already includes the **×1.5 multiplier for a team new to ADK**
(A2). Handoff hours are included in the receiving goal's hands-on figure.
Review is sized to the change: heavier for identity (G03) and writes (G04),
lighter for the widget and evaluation set. W1 and W2 are calendar waits
requested on day 1 (W1 by Dev C, W2 by Dev A); they consume no hours.

| Person (suggested role) | Goals | Hours | Their capacity after reserve |
| --- | --- | --- | --- |
| Dev A: knows the booking API best | G01, G04, G06, G10 | 19–29.5 | 37.5 |
| Dev B: agent, evaluation and frontend | G02, G07, G08, G11 | 19–31 | 37.5 |
| Dev C: identity and platform | G03, G05, G09 | 18–28 | 37.5 |

Schedule block (the single source of each estimate; tickets copy it):

```yaml
- goal: W1
  phase: 1
  total: 0
  blocked_by: []
  calendar_waits: GCP project with billing and Vertex AI enabled, staging booking-API key and test salon data
  wait_days: 1-2
- goal: W2
  phase: 1
  total: 0
  blocked_by: []
  calendar_waits: salon owner sign-off on assistant wording, cancellation policy text and pilot salon
  wait_days: 2-4
- goal: G01
  phase: 1
  hands_on: 2.5-4
  review: 1-2
  total: 3.5-6
  owner: Dev A
  blocked_by: []
  calendar_waits: none
  wait_days: 0
  handoff: 0
- goal: G02
  phase: 1
  hands_on: 4-6
  review: 1-2
  total: 5-8
  owner: Dev B
  blocked_by: [G01]
  calendar_waits: none
  wait_days: 0
  handoff: 0.5
- goal: G03
  phase: 1
  hands_on: 5-8
  review: 2-3
  total: 7-11
  owner: Dev C
  blocked_by: []
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
  hands_on: 3-4
  review: 1-2
  total: 4-6
  owner: Dev C
  blocked_by: [G03, G04]
  calendar_waits: none
  wait_days: 0
  handoff: 1
- goal: G06
  phase: 1
  hands_on: 3-5
  review: 1-2
  total: 4-7
  owner: Dev A
  blocked_by: [G03, G04, W1]
  calendar_waits: none
  wait_days: 0
  handoff: 0.5
- goal: G07
  phase: 1
  hands_on: 3-5
  review: 1-2
  total: 4-7
  owner: Dev B
  blocked_by: [G02, G03]
  calendar_waits: none
  wait_days: 0
  handoff: 0.5
- goal: G08
  phase: 1
  hands_on: 5-8
  review: 1-2
  total: 6-10
  owner: Dev B
  blocked_by: [G02]
  calendar_waits: none
  wait_days: 0
  handoff: 0
- goal: G09
  phase: 1
  hands_on: 5-8
  review: 2-3
  total: 7-11
  owner: Dev C
  blocked_by: [W1]
  calendar_waits: none
  wait_days: 0
  handoff: 0
- goal: G10
  phase: 1
  hands_on: 2.5-3.5
  review: 1-1
  total: 3.5-4.5
  owner: Dev A
  blocked_by: [G09, W2]
  calendar_waits: none
  wait_days: 0
  handoff: 0.5
- goal: G11
  phase: 1
  hands_on: 3-4
  review: 1-2
  total: 4-6
  owner: Dev B
  blocked_by: [G05, G06, G07, G08, G09, G10]
  calendar_waits: none
  wait_days: 0
  handoff: 1
```

Schedule check, run 2026-10-14:
`python3.12 .claude/skills/adk-system-designer/scripts/check_schedule.py --plan docs/plans/salon-booking-assistant.md --tickets docs/tickets/salon-booking-assistant/ --days 10 --reserve 0.25 --person "Dev A=5" --person "Dev B=5" --person "Dev C=5"`
reported 56–88.5 h against a capacity of 112.5 h (fits). The longest chain is
G01 → G04 → G06 → G11 at 8.27 working days on the high end, and the finish is
6.13–9.87 working days against 10, so the calendar fits. It found no ticket
mismatches and no handoffs without hours.

### What changed after failing runs

| Run | Finish (working days) | Change made | Why it is true of the work |
| --- | --- | --- | --- |
| 1: nine goals, move and cancel in one goal, launch in one goal | 6.93–11.47, low end only | Split move (G06, Dev A) from cancel (G05, Dev C). G04 runs on the G01 fake, and its staging check (1 h) moves to G06, which waits for W1. Launch preparation (G10) splits from go-live (G11) | Cancel and move share G04's machinery but not each other. The fake exists after G01, and only the live check needs staging. A runbook and staff briefing do not need the finished agent |
| 2 | 7.73–12, low end only | G09 (infrastructure) waits only for W1. The "agent served on staging" check (1 h) moves to G11. G10 moves to Dev A, with a 0.5 h handoff | Project, database, service account, secrets and a skeleton service do not need the agent; only its deploy does |
| 3 | 6.53–10.67, low end only | The A4 login discovery (1 h) moves from G01 to G03, so G03 starts on day 1 | The login is the identity owner's question; it does not depend on the booking-API contract |
| 4 (this plan) | 6.13–9.87, fits | Cut: plain widget (G07 −1–2 h) and launch at the pilot salon only (G11 −1 h). Slot cards and the other four salons move to G13 and G12 | Scope cut; no floor item removed |

What-ifs that did not close the gap, all on run 3's plan: G11 owned by Dev A
or Dev C (10.67); the widget cut alone (10.13); pilot-only alone (10.4); the
evaluation set moved to Dev C (13.6); 4.5 instead of 5 focused hours a day
(11.85). **Alternative to the cut:** the full scope (the slot-card widget and
all five salons on launch day) fits in **11** working days: 58–91.5 h, finish
6.53–10.67.

### Cut line

**Ships in phase 1 (G01–G11, 56–88.5 of 112.5 h):** book, move and cancel for
signed-in customers at the pilot salon; plain widget with proposal cards and
Confirm; evaluation before launch; Cloud Run with traces, caps and a kill
switch.
**Waits for phase 2:** the other four salons (G12, the first goal after the
pilot), slot cards (G13), and G14–G19.

If phase 1 runs high anyway, the next cut is move as cancel plus rebook (two
confirmed operations) instead of a single reschedule call, if G01 finds the
API's reschedule endpoint awkward. Identity (G03), confirmation and idempotent
dispatch (G04), caps and the kill switch (G09), and the pre-launch evaluation
(G08) are the floor or its evidence. They are not cut.

If time runs out early, the goals stay useful in this order: G01 + G02 make an
availability demo; G03 + G04 add booking for signed-in customers locally; G05
+ G06 complete the journey; G07 + G09 + G10 + G11 put it in front of
customers, and G08 is the evidence that this is safe.

## Implementation map

| Decision | Component and integration point (proposed) | GCP responsibility | Primary skill | Verification still needed |
| --- | --- | --- | --- | --- |
| D1, D12 | `app/agent.py`: one `LlmAgent` with three read tools and three `propose_*` tools; `app/context.py` injects the date, time zone and hours into session state | Vertex AI model endpoint | `adk-tool-interface-design` | ADK 2.8.0 constructor and `ToolContext` names against the chosen pin |
| D2 | Model ID in `app/config.py` and `release.json` | Vertex AI | `adk-model-and-output-contracts` | Refresh the lifecycle snapshot (checked 2026-10-08) before G02 |
| D3 | `app/auth.py`: token verification dependency; the chat API writes `customer_id` to session state and tools read it from `ToolContext.state` | Secret Manager, if the verification key is not public | `adk-tool-auth-and-secrets` | A4: token format, issuer and key source |
| D4, D5 | `app/operations.py` (state machine and Postgres row claim), `POST /operations/{id}/confirm`, `app/booking_client.py` | Cloud SQL Postgres | `safe-api-tool-calls` | A6: idempotency key and lookup endpoint |
| D6 | `DatabaseSessionService` on Postgres; SQLite locally | Cloud SQL | `deploy-adk-on-google-cloud` | Session service behaviour under the pinned ADK |
| D7, D9, D11 | FastAPI app owning the `Runner`; one Cloud Run service; caps, kill switch and `release.json` | Cloud Run, Secret Manager, billing budget alert | `deploy-adk-on-google-cloud` | Region and prices (not looked up offline) |
| D8 | `web/widget.js` with the JSON contract in design D8 | Static file on the salon site | `adk-frontend-integration` | Embedding on the existing site |
| D10, I6 | Tool projections; telemetry content capture off | Cloud Trace and Logging | `adk-agent-observability` | The span-retention fix noted for ADK 2.10.0 or later in the observability compatibility notes |

## Goals and dependencies

Each ticket is the home of its goal's scope, route and acceptance.

| ID and goal | Phase | Type | Human hours | Depends on | Owner | Primary skill | State |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [G01 Booking API contract and fake](../tickets/salon-booking-assistant/G01-booking-api-contract-and-fake.md) | 1 | discovery + implementation | 3.5–6 | — | Dev A | `safe-api-tool-calls` | ready |
| [G02 Customer asks about services, free slots and their appointments](../tickets/salon-booking-assistant/G02-read-only-agent.md) | 1 | implementation | 5–8 | G01 | Dev B | `adk-tool-interface-design` | blocked on G01 |
| [G03 Signed-in customer is identified from the existing login](../tickets/salon-booking-assistant/G03-customer-identity.md) | 1 | discovery + implementation | 7–11 | — | Dev C | `adk-tool-auth-and-secrets` | ready |
| [G04 Customer books with one confirmed click](../tickets/salon-booking-assistant/G04-book-with-confirmation.md) | 1 | implementation | 8–12 | G01 | Dev A | `safe-api-tool-calls` | blocked on G01 |
| [G05 Customer cancels their own appointment](../tickets/salon-booking-assistant/G05-cancel-appointment.md) | 1 | implementation | 4–6 | G03, G04 | Dev C | `safe-api-tool-calls` | blocked |
| [G06 Customer moves their own appointment](../tickets/salon-booking-assistant/G06-move-appointment.md) | 1 | implementation + bounded live check | 4–7 | G03, G04, W1 | Dev A | `safe-api-tool-calls` | blocked |
| [G07 Chat API and plain widget](../tickets/salon-booking-assistant/G07-chat-api-and-widget.md) | 1 | implementation | 4–7 | G02, G03 | Dev B | `adk-frontend-integration` | blocked |
| [G08 Evaluation set of 30 conversations](../tickets/salon-booking-assistant/G08-evaluation-set.md) | 1 | implementation | 6–10 | G02 | Dev B | `adk-agent-evaluation` | blocked on G02 |
| [G09 Staging and production on Cloud Run](../tickets/salon-booking-assistant/G09-cloud-run-platform.md) | 1 | implementation (cloud) | 7–11 | W1 | Dev C | `deploy-adk-on-google-cloud` | blocked on W1 |
| [G10 Launch readiness: runbook, drills, staff briefing](../tickets/salon-booking-assistant/G10-launch-readiness.md) | 1 | implementation (cloud) | 3.5–4.5 | G09, W2 | Dev A | `deploy-adk-on-google-cloud` | blocked |
| [G11 Pilot go-live at one salon](../tickets/salon-booking-assistant/G11-pilot-go-live.md) | 1 | implementation (cloud) | 4–6 | G05–G10 | Dev B | `adk-agent-evaluation` | blocked |

### Phase 2, graduate and harden (re-estimate after G11)

- **G12 Extend to all five salons.** Primary `deploy-adk-on-google-cloud`.
  2–4 h. Acceptance: graduation conditions (design §2) recorded as met; a
  booking at each salon succeeds on production with the staging test account.
- **G13 Slot cards in the widget.** Primary `adk-frontend-integration`.
  2–4 h. Acceptance: tapping a slot card produces the same proposal as typing
  the time.
- **G14 Live evaluation gate in CI.** Primary `adk-release-engineering`.
  6–10 h. Acceptance: a deliberately broken instruction fails the gate by exit
  code; a run that did not happen is reported as missing.
- **G15 Adversarial suite.** Primary `adk-agent-security`. 5–8 h. Acceptance:
  scripted attempts on another customer's booking, skipping confirmation and
  injected service-description text never produce a write, asserted by test.
- **G16 SLOs, dashboard and alerts.** Primary `adk-agent-observability`.
  6–10 h. Acceptance: an injected booking-API outage raises an alert that
  leads to the stored session.
- **G17 Retention and erasure.** Primary `protect-adk-sensitive-data`. 5–8 h.
  Acceptance: after an erase request no session, operation or log line for
  the test customer remains.
- **G18 Automated reconciliation.** Primary `safe-api-tool-calls`. 5–8 h.
  Acceptance: a forced lost response ends `succeeded` with one booking and no
  human step.
- **G19 Streaming replies.** Primary `adk-frontend-integration`. 6–10 h,
  only if G11 measures slow replies. Acceptance: first text in under 1.5 s at
  p50 on pilot traffic.

## Later

| Item | Trigger that brings it forward | Risk accepted while it waits | Likely primary skill |
| --- | --- | --- | --- |
| SMS or WhatsApp channel | Customers ask for it, or web chat use stays low | Customers without the website keep phoning | `adk-agent-interoperability` |
| Deposits or payments | The salons start taking deposits (A5) | None; no money moves | `safe-api-tool-calls` |
| Remembered preferences | Repeat customers restating "my usual stylist" | Customers repeat themselves | `adk-memory-architecture` |
| Staff-facing assistant | Front desk asks for it | None | `adk-system-designer` (new design) |
| Languages beyond English (A9) | A salon reports non-English demand | Those customers keep phoning | `adk-agent-instructions` |
| Canary releases | Traffic large enough for comparable samples within a day | Releases go all at once, with a one-command rollback (G10) | `adk-release-engineering` |
| Model migration | Deprecation notice for `gemini-3.8-flash` | None announced at 2026-10-08 | `adk-model-and-output-contracts` |
| Latency and cost tuning | Measured cost per completed operation or p95 latency above target | Spend above the minimum | `optimise-adk-on-google-cloud` |

## What the reviewer reads

| Document | Establishes |
| --- | --- |
| [Design](../architecture/salon-booking-assistant.md) | Decisions, guarantees, failure handling |
| `eval/README.md` (written in G08, updated in G11) | Latest result per evaluation case |
| This plan | Schedule, cut line, remaining limits and deferred controls |

## Open decisions for further planning

These are kept in design §9. A4 blocks G03 and, through it, G05–G07. A6
shapes G04 and G06, and A7 shapes G05 and G06.

## Resume here

- **Next goal:** G01, the booking API contract and fake. It is ready, and its
  answers settle A6 and A7. G03 is ready as well and can start in parallel.
- **Read first:** the design, then the G01 ticket.
- **Next action:** send W1 and W2. Then list the booking API's endpoints for
  availability, create, reschedule, cancel and list-by-customer, and record
  whether it accepts an idempotency key.
- **Continuation prompt:**

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G01-booking-api-contract-and-fake.md.
Read docs/architecture/salon-booking-assistant.md and preserve its accepted decisions.
Use safe-api-tool-calls with adk-tool-interface-design.
Work locally only, verify the ticket's acceptance cases, and record evidence and
remaining blockers in the ticket.
```

After that goal, the same request without an ID continues:
`/adk-engineer Continue the next ready goal in docs/plans/salon-booking-assistant.md.`
