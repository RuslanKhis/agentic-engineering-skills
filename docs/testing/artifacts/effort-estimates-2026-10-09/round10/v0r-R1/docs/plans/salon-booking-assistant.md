# Implementation plan: salon booking assistant

Status: draft, with ready goals identified. The assumed answers A1–A10 in the design are not yet confirmed.
Architecture: [docs/architecture/salon-booking-assistant.md](../architecture/salon-booking-assistant.md)
Continuation source of truth: this plan's schedule block plus the phase 1 tickets in
[docs/tickets/salon-booking-assistant/](../tickets/salon-booking-assistant/). The tickets are each goal's home.

## Summary for the reader

- **Revision 2026-10-14:** the salon owners moved the launch from 10 to 8
  working days; the same three developers. Nothing has been built yet (every
  ticket's Evidence is empty), so the 8 days start at day 1 of this plan (A11).
- **Profile and phase 1:** MVP. Within 8 working days, signed-in customers of
  the **pilot salon** can use a chat widget on the salon website to see
  availability, list their own appointments and **book** with one confirmed
  click through the existing booking API. Moving and cancelling stay on the
  phone for the pilot: the assistant gives the salon's number. Cancel (G05)
  and move (G06) are the first goals of phase 2; the other four salons follow
  (G12) once the pilot meets the graduation conditions in design §2.
- **Effort and finish:** phase 1 needs 48–74 human hours (agent-assisted)
  against 90 hours of capacity after a 25 % reserve. The schedule check gives
  a finish of 5.2–8 working days against 8: it **fits, with no slack at the
  high end**. The calendar, not the hours, is the limit: the longest
  dependent chain is G01 → G02 → G08 → G11 (7.87 working days at the high
  end), and Dev C's G03 → G09 → G10 feeds G11 as well.
- **Largest risks:** (1) The existing customer login may not be verifiable by
  our backend (A4). G03 finds out on day 1; the email one-time-code fallback
  costs 6–10 h and does **not** fit 8 days (Dev C). (2) The booking API may
  lack an idempotency key, so a lost write response is uncertain. G01 finds
  out and the D5 reconciliation covers it (Dev A). (3) The model may misstate
  times or offer changes it cannot make. G08 measures this and G11 gates the
  pilot on the result (Dev B).
- **Decisions needed from you:** confirm the new cut line below (booking only
  at launch). Launching with booking **and** cancel needs the original 10
  working days; 9 is not enough. Confirm A12 (chat requires sign-in) and A1–A10, especially A4.
- **Next prompt:** `/adk-engineer Carry out docs/tickets/salon-booking-assistant/G01-booking-api-contract-and-fake.md.`
  Dev C starts G03 the same day.

## Destination and constraints

Destination, non-goals and decisions: design §1 and D1–D12. No application
code exists yet; the repository holds only the skill packages, so every module
path is **proposed**: `app/` (FastAPI app, agent, tools, operations),
`prompts/booking_agent/`, `web/widget.js`, `eval/`, `tests/`. Every goal
inherits the working pins `google-adk==2.8.0` (the specialists' checked version,
confirmed in G02) and `gemini-3.8-flash` on Vertex AI (D2), plus the prompt
version in `prompts/booking_agent/`. A goal that changes any of these is a
release and records it in `release.json` (D11); adding `propose_cancellation`
(G05) or `propose_move` (G06) after launch is such a release. No credentials
or private resource identifiers belong in these documents.

Authorization: this session was design only. Goals are ready in design. Local
work needs nothing further. G09, G10, G11 and G22's deletion job need W1's GCP
project and staging key, and the team's approval for each deployment and for
the pilot.

## Delivery profile and capacity

Profile: MVP or pilot (design §2).

| Phase | Delivers | Goals | Human hours, agent-assisted | Capacity and reserve |
| --- | --- | --- | --- | --- |
| 1, ship | Signed-in customers of the pilot salon see availability and book safely; the team sees failures and cost | G01–G04, G07–G11, G22 | 48–74 | 3 people × 5 focused h/day × 8 days = 120 h; 25 % reserve → 90 h |
| 2, graduate and harden | Cancel and move, all five salons, slot cards, live evaluation gate, adversarial suite, SLOs, erasure, automated reconciliation | G05, G06, G12–G19 | 46–76 (rough, re-estimated after G11) | After the pilot, as time allows |

Estimates are person-hours of human effort for a developer with a coding
agent: hands-on work plus review and verification. Every figure, hands-on and
review alike, already includes the **×1.5 multiplier for a team new to ADK**
(A2). Handoff hours are included in the receiving goal's hands-on figure.
Review is sized to the change: heavier for identity (G03) and writes (G04),
lighter for the widget, evaluation set and CI. W1 and W2 are calendar waits
requested on day 1 (W1 by Dev C, W2 by Dev A); they consume no hours.

| Person (suggested role) | Goals | Hours | Their capacity after reserve |
| --- | --- | --- | --- |
| Dev A: booking API, writes, chat API | G01, G04, G07, G22 | 18–28 | 30 |
| Dev B: agent and evaluation | G02, G08, G11 | 15–23.5 | 30 |
| Dev C: identity and platform | G03, G09, G10 | 15–22.5 | 30 |

Spare hours are not a phase 2 budget: the calendar, not the hours, binds, and
Dev B owns G11, the last goal. If G02 and G08 finish at the low end, Dev B
may start G05 (cancel) on the G04 code, but G05 ships in its own release
after G11 and never joins G11's release candidate.

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
  calendar_waits: salon owner sign-off on assistant wording, the "call the salon to move or cancel" text and pilot salon
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
  hands_on: 4.5-7
  review: 2-3
  total: 6.5-10
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
- goal: G07
  phase: 1
  hands_on: 3-4.5
  review: 1-2
  total: 4-6.5
  owner: Dev A
  blocked_by: [G02, G03]
  calendar_waits: none
  wait_days: 0
  handoff: 1
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
  hands_on: 4-6
  review: 1.5-2.5
  total: 5.5-8.5
  owner: Dev C
  blocked_by: [W1]
  calendar_waits: none
  wait_days: 0
  handoff: 0
- goal: G10
  phase: 1
  hands_on: 2-3
  review: 1-1
  total: 3-4
  owner: Dev C
  blocked_by: [G09, W2]
  calendar_waits: none
  wait_days: 0
  handoff: 0
- goal: G11
  phase: 1
  hands_on: 3-4
  review: 1-1.5
  total: 4-5.5
  owner: Dev B
  blocked_by: [G03, G04, G07, G08, G09, G10]
  calendar_waits: none
  wait_days: 0
  handoff: 1
- goal: G22
  phase: 1
  hands_on: 2-2.5
  review: 0.5-1
  total: 2.5-3.5
  owner: Dev A
  blocked_by: [G08, G09]
  calendar_waits: none
  wait_days: 0
  handoff: 0.5
- goal: G05
  phase: 2
  hands_on: 3-4
  review: 1-2
  total: 4-6
  owner: Dev B
  blocked_by: [G03, G04]
  calendar_waits: none
  wait_days: 0
  handoff: 1
- goal: G06
  phase: 2
  hands_on: 3-5
  review: 1-2
  total: 4-7
  owner: Dev A
  blocked_by: [G03, G04, G05, W1]
  calendar_waits: none
  wait_days: 0
  handoff: 0.5
```

Schedule check, run 2026-10-14:
`python3.12 .claude/skills/adk-system-designer/scripts/check_schedule.py --plan docs/plans/salon-booking-assistant.md --tickets docs/tickets/salon-booking-assistant/ --days 8 --reserve 0.25 --person "Dev A=5" --person "Dev B=5" --person "Dev C=5"`
reported 48–74 h against a capacity of 90 h (fits). The longest chain is
G01 → G02 → G08 → G11 at 7.87 working days on the high end, and the finish is
5.2–8 working days against 8, so the calendar fits with no slack at the high
end. It found no ticket mismatches and no handoffs without hours; the same
check with `--phase 2` reads G05 and G06 (8–13 h) without mismatches.

### What changed for 8 days

The 10-day plan, checked against 8 days, finished in 6.13–9.87 working days
(low end only). Each row below is one change, with the helper's finish after it.

| Change | Finish after it (working days) | Why it is true of the work |
| --- | --- | --- |
| Move (G06) to phase 2; its staging check is covered by G10's drill (forced uncertain booking on staging) and G11's staging journey | 6.27–10.13 | Move is a separate operation on G04's machinery; nothing else waits for it |
| Cancel (G05) to phase 2 as well; G04 creates bookings only | 6–9.87 | Cancel shares G04's machinery but nothing in the booking journey needs it. The A7 policy window no longer applies at launch |
| G11 slimmed: −0.5 h. The staging journey is one booking, not three operations; the first days' monitoring and baseline move to G12 | 6–9.73 | Watching the pilot happens after customers have access, and G12 already waits for 3 pilot days |
| CI and the 30-day session-deletion job split out of G09 into G22 (Dev A, after G08 and G09), which does not gate G11 | 6–9.73 | The first session is 30 days from deletion; G11 runs the same tests and scripted evaluation by hand before deploying (G10 runbook) |
| Owners: G07 to Dev A (handoff 1 h), G10 to Dev C (no handoff; was 0.5 h) | 5.33–8.27 | Dev C built G09's platform; Dev A owns the confirm endpoint the widget calls, and Dev B owns the end of the chain |
| Chat requires sign-in (A12): no anonymous sessions or per-IP caps. G03 −0.5 to −1 h, G07 −0.5 to −1 h | **5.2–8, fits** | Unauthenticated requests are refused before any session or model call, so the abuse floor holds with fewer controls |

G08 was **not** cut: it keeps 30 cases and its hours; the move, cancel and
policy-window cases become booking, reading and "call the salon" cases.

What-ifs that did not close the gap (high-end finish, working days): G11 to
Dev A with only move cut (10.13); G04 split into an operations core and a
booking tool, with book and cancel kept (9.6–9.87); on the final plan, G22
owned by Dev B (8.93), G22 gating G11 (8.93), G11 not slimmed (8.13), or
anonymous browsing kept (8.27). **Alternative to the cut:** booking and
cancel at launch (G05 in phase 1, gating G11) needs **10** working days:
52.5–80.5 h, finish 6.13–9.6 with Dev B on G05. At 9 days the best placement
(Dev C) finishes 6.27–9.2, so 9 days does not fit.

### Cut line

**Ships in phase 1 (G01–G04, G07–G11, G22; 48–74 of 90 h):** availability,
own appointments and click-confirmed booking for signed-in customers at the
pilot salon; plain widget with proposal cards and Confirm; evaluation before
launch; Cloud Run with traces, caps and a kill switch; CI and session
deletion.
**Waits for phase 2:** cancel (G05) and move (G06), the first goals after
launch; the other four salons (G12); slot cards (G13); and G14–G19.

There is no slack at the high end. If phase 1 runs high anyway, nothing more
comes out of the floor: identity (G03), confirmation and idempotent dispatch
(G04), caps and the kill switch (G09), the runbook drill (G10) and the
pre-launch evaluation (G08) stay. The order of what gives is: G22 slips past
launch day (CI runs by hand meanwhile; the deletion job must land before the
first session is 30 days old); then launch moves to day 9.

If time runs out early, the goals stay useful in this order: G01 + G02 make an
availability demo; G03 + G04 add booking for signed-in customers locally; G07
puts it in a browser; G09 + G10 + G11 put it in front of customers, and G08 is
the evidence that this is safe.

### The 10-day plan's run history

The structure above still rests on the 10-day plan's changes: move split from
cancel; G09 waits only for W1, with the agent's deploy in G11; the A4 login
discovery sits in G03 on day 1; slot cards and the other four salons in phase
2. Its detail is in this file's git history.

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
| [G03 Signed-in customer is identified from the existing login](../tickets/salon-booking-assistant/G03-customer-identity.md) | 1 | discovery + implementation | 6.5–10 | — | Dev C | `adk-tool-auth-and-secrets` | ready |
| [G04 Customer books with one confirmed click](../tickets/salon-booking-assistant/G04-book-with-confirmation.md) | 1 | implementation | 8–12 | G01 | Dev A | `safe-api-tool-calls` | blocked on G01 |
| [G07 Chat API and plain widget](../tickets/salon-booking-assistant/G07-chat-api-and-widget.md) | 1 | implementation | 4–6.5 | G02, G03 | Dev A | `adk-frontend-integration` | blocked |
| [G08 Evaluation set of 30 conversations](../tickets/salon-booking-assistant/G08-evaluation-set.md) | 1 | implementation | 6–10 | G02 | Dev B | `adk-agent-evaluation` | blocked on G02 |
| [G09 Staging and production on Cloud Run](../tickets/salon-booking-assistant/G09-cloud-run-platform.md) | 1 | implementation (cloud) | 5.5–8.5 | W1 | Dev C | `deploy-adk-on-google-cloud` | blocked on W1 |
| [G10 Launch readiness: runbook, drills, staff briefing](../tickets/salon-booking-assistant/G10-launch-readiness.md) | 1 | implementation (cloud) | 3–4 | G09, W2 | Dev C | `deploy-adk-on-google-cloud` | blocked |
| [G11 Pilot go-live at one salon](../tickets/salon-booking-assistant/G11-pilot-go-live.md) | 1 | implementation (cloud) | 4–5.5 | G03, G04, G07–G10 | Dev B | `adk-agent-evaluation` | blocked |
| [G22 CI and session deletion job](../tickets/salon-booking-assistant/G22-ci-and-session-retention.md) | 1 | implementation (cloud) | 2.5–3.5 | G08, G09 | Dev A | `adk-release-engineering` | blocked |
| [G05 Customer cancels their own appointment](../tickets/salon-booking-assistant/G05-cancel-appointment.md) | 2 | implementation | 4–6 | G03, G04; released after G11 | Dev B | `safe-api-tool-calls` | phase 2 |
| [G06 Customer moves their own appointment](../tickets/salon-booking-assistant/G06-move-appointment.md) | 2 | implementation + bounded live check | 4–7 | G03, G04, G05, W1 | Dev A | `safe-api-tool-calls` | phase 2 |

### Phase 2, graduate and harden (re-estimate after G11)

G05 and G06 keep their full tickets because they were ready before the
launch moved; the rest stay as short entries. Each of G05 and G06 is its own
release (D11): the new `propose_*` tool, its G08 cases and the W2 policy text
ship together.

- **G12 Watch the pilot, then extend to all five salons.** Primary
  `deploy-adk-on-google-cloud`. 3–5 h (1 h added for the first days'
  monitoring and baseline moved out of G11). Acceptance: baseline numbers
  (completion, latency, cost per completed booking) recorded in
  `eval/README.md` and design §6; graduation conditions (design §2) recorded
  as met; a booking at each salon succeeds on production with the staging
  test account.
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
| Anonymous availability browsing (cut by A12) | Salon owners want visitors without an account to see free slots | Visitors without an account sign up or phone | `adk-operational-guardrails` (per-IP caps), `adk-tool-auth-and-secrets` |
| Latency and cost tuning | Measured cost per completed operation or p95 latency above target | Spend above the minimum | `optimise-adk-on-google-cloud` |

## What the reviewer reads

| Document | Establishes |
| --- | --- |
| [Design](../architecture/salon-booking-assistant.md) | Decisions, guarantees, failure handling |
| `eval/README.md` (written in G08, updated in G11) | Latest result per evaluation case |
| This plan | Schedule, cut line, remaining limits and deferred controls |

## Open decisions for further planning

These are kept in design §9. A4 blocks G03 and, through it, G07 and G11. A6
shapes G04 (and G06 in phase 2). A7 no longer blocks phase 1; it shapes G05
and G06.

## Resume here

- **Next goal:** G01, the booking API contract and fake. It is ready, and its
  answers settle A6 and A7. G03 is ready as well and starts in parallel on
  day 1; with no slack at the high end, both start on day 1.
- **Read first:** the design, then the G01 ticket.
- **Next action:** send W1 and W2 on day 1 (W2 now asks for the "call the
  salon to move or cancel" wording instead of the cancellation policy text).
  Then list the booking API's endpoints for
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
