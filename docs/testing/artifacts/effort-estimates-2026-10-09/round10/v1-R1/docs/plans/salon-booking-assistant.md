# Implementation plan: salon booking assistant

Status: draft, revision 2 (2026-10-14), with ready goals identified. The launch
date (8 working days) is the salon owners' decision; the assumed answers A1–A15
in the design, including the cut package A11–A15, are not yet confirmed.
Architecture: [docs/architecture/salon-booking-assistant.md](../architecture/salon-booking-assistant.md)
Continuation source of truth: this plan's schedule block plus the phase 1 tickets in
[docs/tickets/salon-booking-assistant/](../tickets/salon-booking-assistant/). The tickets are each goal's home.

## Summary for the reader

- **Profile and phase 1:** MVP. On working day 8, signed-in customers of the
  **pilot salon** can use a chat widget on the salon website to see
  availability, book and cancel their own appointments, and move one as two
  confirmed steps (book the new time, then cancel the old one). Each change is
  confirmed by the customer's click and carried out through the existing
  booking API. The single-step move (G06), anonymous chat (G22) and the other
  four salons (G12) follow in phase 2.
- **Effort and finish:** phase 1 needs 48.5–74.5 human hours (agent-assisted)
  against 90 hours of capacity after a 25 % reserve. The schedule check gives
  a finish of 5.47–8 working days against 8, so it **fits, with no calendar
  slack at the high end beyond the reserve**: all three developers finish
  their last pre-launch goal on day 6.67 at the high end, and G11 takes the
  rest. A 1–2 h overrun on a goal near the end (tested on G05) gives
  5.73–8.53, which spends reserve.
- **What the shorter date cost:** five scope and depth cuts (A11–A15), listed
  with their what-if cost in [the cut line](#cut-line). No floor item was
  removed. Restoring the 20 → 30 evaluation cases, trace export and the
  pre-launch deletion job needs 9 working days (finish 7.67–8.67); the full
  revision-1 scope needed 10.
- **Largest risks:** (1) The existing customer login may not be verifiable by
  our backend (A4). G03 finds out on day 1. The email one-time-code fallback
  (+6–10 h on Dev C) gives 6.8–10.67 days with these owners, so it would
  force a re-plan (Dev C). (2) The booking API may lack an idempotency key, so
  a lost write response is uncertain; G01 finds out and D5 reconciliation
  covers it (Dev A). (3) The model may misstate times or policy or propose a
  move's steps in the wrong order. G08 measures this on 20 cases, and G11
  gates the pilot on the result (Dev B).
- **Decisions needed from you:** confirm or correct A11–A15 (the cut package)
  or choose 9 working days instead; confirm A4 (login), A5 (no deposits) and
  A7 (policy window).
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
work needs nothing further. G09, G10 and G11 need W1's staging key and GCP
project, and the team's approval for each deployment and for the pilot.

## Delivery profile and capacity

Profile: MVP or pilot (design §2).

| Phase | Delivers | Goals | Human hours, agent-assisted | Capacity and reserve |
| --- | --- | --- | --- | --- |
| 1, ship | Signed-in customers of the pilot salon book and cancel their own appointments, and move one in two confirmed steps, safely; the team sees failures and cost in logs | G01–G05, G04a, G07–G11 | 48.5–74.5 | 3 people × 5 focused h/day × 8 days = 120 h; 25 % reserve → 90 h |
| 2, graduate and harden | Baselines, deletion job, all five salons, single-step move, slot cards, anonymous chat, live evaluation gate, adversarial suite, traces and SLOs, erasure, automated reconciliation | G20, G21, G12, G06, G13, G22, G14–G19 | 48–79.5 (rough, re-estimated after G11) | After the launch, as time allows; G21 has a hard date |

Estimates are person-hours of human effort for a developer with a coding
agent: hands-on work plus review and verification. Every figure, hands-on and
review alike, already includes the **×1.5 multiplier for a team new to ADK**
(A2). Handoff hours are included in the receiving goal's hands-on figure.
Review is sized to the change: heavier for identity (G03) and the operations
core (G04a), lighter for the booking tool, widget and evaluation set. W1 and
W2 are calendar waits requested on day 1 (W1 by Dev C, W2 by Dev A); they
consume no hours.

| Person (suggested role) | Goals | Hours | Their capacity after reserve |
| --- | --- | --- | --- |
| Dev A: knows the booking API best | G01, G04a, G05, G10 | 17–25 | 30 |
| Dev B: agent, evaluation and launch | G02, G04, G08, G11 | 15.5–24.5 | 30 |
| Dev C: identity, platform and chat API | G03, G09, G07 | 16–25 | 30 |

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
  hands_on: 2-3.5
  review: 1-2
  total: 3-5.5
  owner: Dev A
  blocked_by: []
  calendar_waits: none
  wait_days: 0
  handoff: 0
  mentions_only: [G10, W2]
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
  mentions_only: [W1]
- goal: G03
  phase: 1
  hands_on: 4.5-7
  review: 2-3
  total: 6.5-10
  owner: Dev C
  blocked_by: []
  calendar_waits: none
  wait_days: 0
  handoff: 0
  mentions_only: [W1]
- goal: G04a
  phase: 1
  hands_on: 3.5-5.5
  review: 2.5-3
  total: 6-8.5
  owner: Dev A
  blocked_by: [G01]
  calendar_waits: none
  wait_days: 0
  handoff: 0
  mentions_only: [G03, G10]
- goal: G04
  phase: 1
  hands_on: 2-3
  review: 0.5-1
  total: 2.5-4
  owner: Dev B
  blocked_by: [G04a]
  calendar_waits: none
  wait_days: 0
  handoff: 0.5
  mentions_only: [G05, G07]
- goal: G05
  phase: 1
  hands_on: 3-4
  review: 1-2
  total: 4-6
  owner: Dev A
  blocked_by: [G03, G04a]
  calendar_waits: none
  wait_days: 0
  handoff: 0.5
  mentions_only: [G08, W2, wait]
- goal: G07
  phase: 1
  hands_on: 3-4.5
  review: 1-2
  total: 4-6.5
  owner: Dev C
  blocked_by: [G02, G03, G04a]
  calendar_waits: none
  wait_days: 0
  handoff: 1
- goal: G08
  phase: 1
  hands_on: 3.5-6
  review: 1-1.5
  total: 4.5-7.5
  owner: Dev B
  blocked_by: [G02, W1]
  calendar_waits: none
  wait_days: 0
  handoff: 0
- goal: G09
  phase: 1
  hands_on: 3.5-6
  review: 2-2.5
  total: 5.5-8.5
  owner: Dev C
  blocked_by: [W1]
  calendar_waits: none
  wait_days: 0
  handoff: 0
- goal: G10
  phase: 1
  hands_on: 3-4
  review: 1-1
  total: 4-5
  owner: Dev A
  blocked_by: [G09, W2]
  calendar_waits: none
  wait_days: 0
  handoff: 0.5
- goal: G11
  phase: 1
  hands_on: 2.5-3
  review: 1-2
  total: 3.5-5
  owner: Dev B
  blocked_by: [G04, G05, G07, G08, G09, G10]
  calendar_waits: none
  wait_days: 0
  handoff: 1
- goal: G06
  phase: 2
  hands_on: 2.5-4.5
  review: 1-2
  total: 3.5-6.5
  owner: Dev A
  blocked_by: [G11]
  calendar_waits: none
  wait_days: 0
  handoff: 0
```

Schedule check, run 2026-10-14:
`python3.12 .claude/skills/adk-system-designer/scripts/check_schedule.py --plan docs/plans/salon-booking-assistant.md --tickets docs/tickets/salon-booking-assistant/ --days 8 --reserve 0.25 --person "Dev A=5" --person "Dev B=5" --person "Dev C=5"`
reported 48.5–74.5 h against a capacity of 90 h (fits). The longest chain is
G01 → G02 → G08 → G11 at 6.93 working days on the high end, and the finish is
5.47–8 working days against 8, so the calendar fits. It found no ticket mismatches and no handoffs without
hours. Settled as mention only: G01 (G10, W2), G02 (W1), G03 (W1), G04a (G03,
G10), G04 (G05, G07), G05 (G08, W2, wait). Each is a pointer to out-of-scope
work, a request the goal sends, an optional live smoke, or placeholder text, not
a dependency.

### What revision 2 removed or weakened

Compared with revision 1 (10 days). Nothing else in the failure rows, tests,
acceptance cases, waits or floor was removed; the floor is unchanged.

| Item (revision 1) | Revision 2 | Reason |
| --- | --- | --- |
| G06 single-step move in phase 1: `propose_move`, offline acceptance "exactly one reschedule" | Moved to phase 2 (ticket kept, status deferred). Phase 1 moves as book-then-cancel (A11); covered by G05's `changeable` rule, G08's 4 move cases (book-first order asserted) and G11's staging journey | Removes 4–7 h from Dev A and a goal from the end of the chain. A two-step move is not atomic: new §7 row and residual risk recorded |
| G06 acceptance "moving into a taken slot returns fresh slots; moving another customer's appointment is refused" | Covered by G04 (`slot_taken` with fresh slots) and G05 (another customer's appointment refused); returns with G06 | Same checks, on the tools phase 1 uses |
| G06 bounded staging check (book, move, cancel, forced timeout) | Forced timeout and create on staging: G10 drill. Cancel and the two-step move on staging: G11. A move by reschedule on staging: G06 (phase 2) | Every step still runs on staging before go-live, but cancel is first seen there on day 7–8 instead of day 6–7 |
| Anonymous browsing with read tools; G03 "anonymous request → read-only rights"; G07 "21st anonymous turn per IP per hour refused" | Removed with the path: chat needs sign-in (A12). Replaced by "no token → 401, no session, no model call" (G03, G07). Anonymous chat is G22 | Saves 1–2 h; also removes unauthenticated model spend |
| G08: 30 cases (8 book, 6 move, 5 cancel, 4 dates, 3 policy, 2 other customer, 2 out of scope); live cap 300 calls | 20 cases (5, 4, 3, 3, 2, 1, 2), every category kept; live cap 200 calls; G14 grows it to 30 or more (A13) | Weakened evidence. Another-customer attempts are also deterministic tests (I1) |
| G09: Cloud Trace export with content capture off; "exported span … contains no fixture name" (I6) | Structured logs with IDs and token counts; I6 checked on the log export; span check moves to G16 with the export (A14) | Saves 0.5–1 h; pinned ADK 2.8.0 lacks the span-retention fix. Attribution relies on log IDs during the pilot week |
| G09: 30-day session deletion job | G21, due before launch day + 30, and a graduation condition (A15) | No session reaches 30 days before then; personal data stays out of logs meanwhile |
| G11: record baselines (completion, latency, cost) on launch day | G20 in the first pilot week; G11 keeps the launch-day watch of errors and uncertain operations | Baselines need traffic, which does not exist before go-live |
| G01: fake fixtures for 5 salons | Pilot salon plus one other (enough for "not available at this salon"); G12 adds the rest | Pilot is one salon |
| Old G04 (8–12 h, one goal) | Split into G04a (operations core, Dev A) and G04 (`propose_booking`, Dev B), same total plus a 0.5 h handoff | Lets the cancel goal and the chat API start after the core instead of after the booking tool |
| G07 depended on G02 and G03 only, but its acceptance used confirmed operations | G07 now depends on G04a too, with 1 h of handoff | Revision 1 had a hidden dependency; the acceptance needs the confirm endpoint |
| Billing budget alert in G09 | In G10, verified with the drill | Same control, owned by the launch-readiness goal; balances Dev C |
| Waits W1 and W2 | Unchanged (1–2 and 2–4 working days, requested on day 1) | — |

### What changed after failing runs

| Run (8 days) | Finish (working days) | Change made | Why it is true of the work |
| --- | --- | --- | --- |
| 1: revision-1 plan unchanged | 6.13–9.87, low end only | Searched every owner assignment of the full scope with G04 split, using the helper's own scheduler: best 9.6 | The full scope does not fit 8 days with these people; scope must go |
| 2: single-step move to phase 2, move as two steps | 9.33 at best | Also chat requires sign-in, deletion job and trace export after launch, eval at 20 cases, baselines after launch, fixtures for two salons | Each is a scope or depth cut listed above; no floor item |
| 3: all of the above | 8.13 | G07 gained its true dependency on G04a (+0.5 h handoff), which revision 1 lacked | Correctness of the schedule, not a fit change |
| 4: widget split out of G07 for Dev B's idle first day; price lookup split out of G09 | 8.8 and 9.33 | Reverted both: the helper schedules by longest remaining path, so the small goals ran late | Kept the plan as it would actually be scheduled |
| 5 (this plan) | 5.47–8, fits | Budget alert moved from G09 to G10 | Moves 0.5 h from Dev C, the last to finish, to Dev A |

### What-ifs, all on this plan

| What-if | Finish (working days) | Fits |
| --- | --- | --- |
| Keep 30 evaluation cases (A13 "no") | 5.47–8.67 | 8 days: low end only; 9 days: yes |
| Keep Cloud Trace export (A14 "no") | 5.47–8.27 | low end only |
| Keep the deletion job before launch (A15 "no") | 5.47–8.27 | low end only |
| Keep anonymous chat (A12 "no") | 5.47–8.53 | low end only |
| Keep single-step move in phase 1, Dev A (A11 "no") | 6.53–9.87 | 8 and 9 days: low end only (Dev A 32 h) |
| Restore A13, A14 and A15 together | 7.67–8.67 | 9 days: yes |
| A4 fails: email one-time code in G03 (+6–10 h, Dev C) | 6.8–10.67 | low end only even at 10 days with these owners; would need a re-plan |
| G05 overruns by 1–2 h | 5.73–8.53 | spends reserve |

### Cut line

**Ships in phase 1 (48.5–74.5 of 90 h, finish 5.47–8 of 8 days):** book and
cancel for signed-in customers at the pilot salon, and move as two confirmed
steps; plain widget with proposal cards and Confirm; a 20-case evaluation
before launch; Cloud Run with structured logs, caps, a kill switch and a
budget alert.
**Waits for phase 2:** baselines (G20), the deletion job (G21, hard date),
the other four salons (G12), single-step move (G06), slot cards (G13),
anonymous chat (G22), and G14–G19.
**Alternative to the cut:** 9 working days restores 30 evaluation cases, trace
export and the pre-launch deletion job (finish 7.67–8.67). The single-step
move does not fit 9 days with Dev A owning it.

If phase 1 runs high anyway, Dev A has 5 h free after G10 at the high end and
can take over a late goal's verification; beyond that the remedy is a day,
not a floor item. Identity (G03), confirmation and idempotent dispatch (G04a),
caps and the kill switch (G07, G09), the budget alert (G10) and the
pre-launch evaluation (G08) are the floor or its evidence. They are not cut.

If time runs out early, the goals stay useful in this order: G01 + G02 make an
availability demo; G03 + G04a + G04 add booking for signed-in customers
locally; G05 completes cancel and the two-step move; G07 + G09 + G10 + G11 put
it in front of customers, and G08 is the evidence that this is safe.

## Implementation map

| Decision | Component and integration point (proposed) | GCP responsibility | Primary skill | Verification still needed |
| --- | --- | --- | --- | --- |
| D1, D12 | `app/agent.py`: one `LlmAgent` with three read tools and two `propose_*` tools in phase 1; `app/context.py` injects the date, time zone and hours into session state | Vertex AI model endpoint | `adk-tool-interface-design` | ADK 2.8.0 constructor and `ToolContext` names against the chosen pin |
| D2 | Model ID in `app/config.py` and `release.json` | Vertex AI | `adk-model-and-output-contracts` | Refresh the lifecycle snapshot (checked 2026-10-08) before G02 |
| D3 | `app/auth.py`: token verification dependency (401 without a valid token); the chat API writes `customer_id` to session state and tools read it from `ToolContext.state` | Secret Manager, if the verification key is not public | `adk-tool-auth-and-secrets` | A4: token format, issuer and key source |
| D4, D5 | `app/operations.py` (state machine and Postgres row claim), `POST /operations/{id}/confirm`, `app/booking_client.py` (G04a); propose tools on top (G04, G05) | Cloud SQL Postgres | `safe-api-tool-calls` | A6: idempotency key and lookup endpoint |
| D6 | `DatabaseSessionService` on Postgres; SQLite locally | Cloud SQL | `deploy-adk-on-google-cloud` | Session service behaviour under the pinned ADK |
| D7, D9, D11 | FastAPI app owning the `Runner`; one Cloud Run service per environment; caps, kill switch and `release.json` (G07, G09); budget alert (G10) | Cloud Run, Secret Manager, billing budget alert | `deploy-adk-on-google-cloud` | Region and prices (not looked up offline) |
| D8 | `web/widget.js` with the JSON contract in design D8 | Static file on the salon site | `adk-frontend-integration` | Embedding on the existing site |
| D10, I6 | Tool projections; structured logs with IDs and token counts; content capture off | Cloud Logging (Cloud Trace from G16) | `adk-agent-observability` | The span-retention fix noted for ADK 2.10.0 or later, before G16 enables export |

## Goals and dependencies

Each ticket is the home of its goal's scope, route and acceptance.

| ID and goal | Phase | Type | Human hours | Depends on | Owner | Primary skill | State |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [G01 Booking API contract and fake](../tickets/salon-booking-assistant/G01-booking-api-contract-and-fake.md) | 1 | discovery + implementation | 3–5.5 | — | Dev A | `safe-api-tool-calls` | ready |
| [G02 Customer asks about services, free slots and their appointments](../tickets/salon-booking-assistant/G02-read-only-agent.md) | 1 | implementation | 5–8 | G01 | Dev B | `adk-tool-interface-design` | blocked on G01 |
| [G03 Signed-in customer is identified from the existing login](../tickets/salon-booking-assistant/G03-customer-identity.md) | 1 | discovery + implementation | 6.5–10 | — | Dev C | `adk-tool-auth-and-secrets` | ready |
| [G04a Confirmed operations core](../tickets/salon-booking-assistant/G04a-operations-core.md) | 1 | implementation | 6–8.5 | G01 | Dev A | `safe-api-tool-calls` | blocked on G01 |
| [G04 Customer books with one confirmed click](../tickets/salon-booking-assistant/G04-book-with-confirmation.md) | 1 | implementation | 2.5–4 | G04a | Dev B | `adk-tool-interface-design` | blocked |
| [G05 Customer cancels, and moves in two steps](../tickets/salon-booking-assistant/G05-cancel-appointment.md) | 1 | implementation | 4–6 | G03, G04a | Dev A | `safe-api-tool-calls` | blocked |
| [G07 Chat API and plain widget](../tickets/salon-booking-assistant/G07-chat-api-and-widget.md) | 1 | implementation | 4–6.5 | G02, G03, G04a | Dev C | `adk-frontend-integration` | blocked |
| [G08 Evaluation set of 20 conversations](../tickets/salon-booking-assistant/G08-evaluation-set.md) | 1 | implementation | 4.5–7.5 | G02, W1 | Dev B | `adk-agent-evaluation` | blocked on G02 |
| [G09 Staging and production on Cloud Run](../tickets/salon-booking-assistant/G09-cloud-run-platform.md) | 1 | implementation (cloud) | 5.5–8.5 | W1 | Dev C | `deploy-adk-on-google-cloud` | blocked on W1 |
| [G10 Launch readiness: runbook, drills, budget alert, staff briefing](../tickets/salon-booking-assistant/G10-launch-readiness.md) | 1 | implementation (cloud) | 4–5 | G09, W2 | Dev A | `deploy-adk-on-google-cloud` | blocked |
| [G11 Pilot go-live at one salon](../tickets/salon-booking-assistant/G11-pilot-go-live.md) | 1 | implementation (cloud) | 3.5–5 | G04, G05, G07–G10 | Dev B | `adk-agent-evaluation` | blocked |
| [G06 Single-step move](../tickets/salon-booking-assistant/G06-move-appointment.md) | 2 | implementation + bounded live check | 3.5–6.5 (rough) | G11 | Dev A | `safe-api-tool-calls` | deferred |

### Phase 2, graduate and harden (re-estimate after G11)

In this order; G20 and G21 come first because graduation needs them.

- **G20 Pilot week: baselines.** Primary `adk-agent-observability`. 2–3 h.
  Acceptance: completion share, p50/p95 reply time and cost per completed
  operation from the logs are recorded in design §6 and `eval/README.md`,
  with the salon's phone-change baseline.
- **G21 Session deletion job.** Primary `protect-adk-sensitive-data`. 1.5–2 h.
  **Due before launch day + 30 calendar days.** Acceptance: a session older
  than 30 days in staging is gone after the scheduled run, and newer ones
  remain.
- **G12 Extend to all five salons.** Primary `deploy-adk-on-google-cloud`.
  2–4 h. Acceptance: graduation conditions (design §2) recorded as met; a
  booking at each salon succeeds on production with the staging test account.
- **G06 Single-step move.** See its ticket.
- **G13 Slot cards in the widget.** Primary `adk-frontend-integration`.
  2–4 h. Acceptance: tapping a slot card produces the same proposal as typing
  the time.
- **G22 Anonymous availability chat.** Primary `adk-tool-auth-and-secrets`.
  2–3 h. Acceptance: an anonymous session gets read tools only, proposal
  tools return `sign_in_required`, and the 21st anonymous turn from one IP in
  an hour is refused with no model call.
- **G14 Live evaluation gate in CI, 30+ cases.** Primary
  `adk-release-engineering`. 7–12 h. Acceptance: the set has at least 30
  cases; a deliberately broken instruction fails the gate by exit code; a run
  that did not happen is reported as missing.
- **G15 Adversarial suite.** Primary `adk-agent-security`. 5–8 h. Acceptance:
  scripted attempts on another customer's booking, skipping confirmation and
  injected service-description text never produce a write, asserted by test.
- **G16 Trace export, SLOs, dashboard and alerts.** Primary
  `adk-agent-observability`. 7–11 h. Acceptance: with the span-retention fix
  confirmed for the pin, an exported span contains no fixture name or message
  text, and an injected booking-API outage raises an alert that leads to the
  stored session.
- **G17 Retention and erasure.** Primary `protect-adk-sensitive-data`. 5–8 h.
  Acceptance: after an erase request no session, operation or log line for
  the test customer remains.
- **G18 Automated reconciliation.** Primary `safe-api-tool-calls`. 5–8 h.
  Acceptance: a forced lost response ends `succeeded` with one booking and no
  human step.
- **G19 Streaming replies.** Primary `adk-frontend-integration`. 6–10 h,
  only if G20 measures slow replies. Acceptance: first text in under 1.5 s at
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
| `eval/README.md` (written in G08, updated in G11 and G20) | Latest result per evaluation case |
| This plan | Schedule, cut line, what revision 2 removed, remaining limits and deferred controls |

## Open decisions for further planning

These are kept in design §9. A4 blocks G03 and, through it, G05 and G07. A6
shapes G04a (and G06 in phase 2), and A7 shapes G05. The cut package A11–A15
versus 9 working days is the salon owners' call.

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
