# Implementation plan: salon booking assistant

Status: draft, ready goals identified (design decisions provisional, see the design's Assumed answers)
Architecture: [docs/architecture/salon-booking-assistant.md](../architecture/salon-booking-assistant.md)
Continuation source of truth: this plan; phase 1 goal detail lives in the tickets under
[docs/tickets/salon-booking-assistant/](../tickets/salon-booking-assistant/)

## Summary for the reader

- **Profile and phase 1:** MVP / pilot. Phase 1 lets signed-in customers book,
  move and cancel appointments by chat on the booking website. Each change is
  confirmed and ledgered. It goes live at one salon, then all five.
- **Effort and finish:** phase 1 is 56.5–88.5 human hours against 112.5 hours of capacity after a 25 % reserve. It finishes in **6.4–10 working days** of the 10 available, so it **fits, with the high end exactly on the deadline**. Figures from `check_schedule.py`, run on 2026-10-14. The cut line: phase 1 ends live at **the first salon**. The other four follow in G10 after 3 clean pilot days, about 3 working days after the deadline.
- **Largest risks:** (1) The booking API may lack idempotency keys or an atomic
  reschedule, which makes D4 weaker. G01 settles this on day 1. (2) ADK tool
  confirmation is experimental at the assumed pin. G01 chooses between it and
  the propose/commit fallback (D3). (3) The salon chain's sign-off (W1) slips
  and pushes the launch. Request it on day 1.
- **Decisions needed from you:** confirm or correct the Assumed answers A1–A11
  in the design. In particular A5 (site JWT), A7 (API capabilities), O1 (real
  customer emails on confirmed changes) and O4 (allowance numbers). Then
  confirm or move the cut line below.
- **Next prompt:** `/adk-engineer Carry out docs/tickets/salon-booking-assistant/G01-api-contract-and-pins.md. Read its design and plan, use its primary and supporting skills, run its verification locally, fill in the Evidence section and set status. Leave changes uncommitted.`

## Destination and constraints

The destination is a kept MVP that is improved after launch, so phase 1 code
uses configuration where phase 2 will change things. The repository holds no
application code yet; every module path below is **proposed**. The accepted
stack is assumed: Python, google-adk 2.8.0 (to be confirmed in G01), FastAPI,
Cloud Run, Vertex AI and the existing Postgres. The model is pinned to
`gemini-3.8-flash` (D7). The prompt is versioned in code. A goal that changes
the model or prompt after launch is a release. Authorisation so far covers
design only; staging access, deployments and the pilot each need the team's
go-ahead when their goal runs.

Proposed layout: `assistant/agent.py` (App, agent, instruction),
`assistant/tools/` (read and write tools), `assistant/booking/` (client,
ledger, reconciliation), `assistant/api/` (FastAPI, JWT, allowance),
`widget/` (chat widget), `eval/` (cases and runner), `deploy/`.

## Delivery profile and capacity

Profile: MVP or pilot (design, "Delivery constraints").

| Phase | Delivers | Goals | Human hours, agent-assisted (range) | Capacity and reserve |
| --- | --- | --- | --- | --- |
| 1, ship | Customers of the first salon complete book, move and cancel safely; the team sees failures and cost | G01–G09 (and wait W1) | 56.5–88.5 | 3 people × 5 h/day × 10 days, 25 % reserve = 112.5 h after reserve |
| 2, graduate and harden | All five salons, CI gate, retention purge, SLOs and alerts, automated reconciliation, staff handoff | G10–G15 | 27.5–47 | When the team has time after launch |

Estimates are person-hours of human effort with a coding agent, covering
hands-on work plus review and verification. Each one already includes the
×1.5 multiplier for a team new to ADK (A2), applied to every goal. Review is
sized to the change. It is heavier for G03 and G04, which handle writes and
authority, and lighter for G06 configuration. Handoff hours are inside the
receiving goal's hands-on figure and also recorded as `handoff:`.

Suggested owners. Assign them by who knows what; the letters are placeholders.

| Person or role | Goals | Hours | Their capacity |
| --- | --- | --- | --- |
| Dev A: agent and evaluation (the one most curious about ADK/LLMs) | G01, G02, G07, G08 | 19–29.5 | 37.5 |
| Dev B: booking backend (whoever knows the booking API best) | G03, G04 | 17.5–27.5 | 37.5 |
| Dev C: web and infrastructure (whoever owns the site and GCP) | G06, G05, G09 | 20–31.5 | 37.5 |

Schedule block, the single machine-readable source of each estimate:

```yaml
- goal: W1
  phase: 1
  total: 0
  calendar_waits: salon chain owner sign-off on wording, policies and privacy-notice update (A11)
  wait_days: 3-5
  blocked_by: []
- goal: G01
  phase: 1
  hands_on: 2-3
  review: 0.5-1
  total: 2.5-4
  owner: Dev A
  blocked_by: []
  calendar_waits: none
  wait_days: 0
  handoff: 0
  mentions_only: [G06]
- goal: G02
  phase: 1
  hands_on: 4-6
  review: 1.5-3
  total: 5.5-9
  owner: Dev A
  blocked_by: [G01]
  calendar_waits: none
  wait_days: 0
  handoff: 0
- goal: G03
  phase: 1
  hands_on: 6.5-9.5
  review: 3-5
  total: 9.5-14.5
  owner: Dev B
  blocked_by: [G01]
  calendar_waits: none
  wait_days: 0
  handoff: 0.5
  mentions_only: [G14]
- goal: G04
  phase: 1
  hands_on: 5-8
  review: 3-5
  total: 8-13
  owner: Dev B
  blocked_by: [G02, G03]
  calendar_waits: none
  wait_days: 0
  handoff: 1
- goal: G06
  phase: 1
  hands_on: 6-9
  review: 1.5-3
  total: 7.5-12
  owner: Dev C
  blocked_by: []
  calendar_waits: none
  wait_days: 0
  handoff: 0
  mentions_only: [G01, G13]
- goal: G05
  phase: 1
  hands_on: 6-9
  review: 2-4
  total: 8-13
  owner: Dev C
  blocked_by: [G02, G06]
  calendar_waits: none
  wait_days: 0
  handoff: 1
- goal: G07
  phase: 1
  hands_on: 6-9
  review: 1.5-2.5
  total: 7.5-11.5
  owner: Dev A
  blocked_by: [G02]
  calendar_waits: none
  wait_days: 0
  handoff: 0
  mentions_only: [G04, G11]
- goal: G09
  phase: 1
  hands_on: 3.5-5
  review: 1-1.5
  total: 4.5-6.5
  owner: Dev C
  blocked_by: [G06]
  calendar_waits: none
  wait_days: 0
  handoff: 0
  mentions_only: [G03, G14]
- goal: G08
  phase: 1
  hands_on: 2.5-3.5
  review: 1-1.5
  total: 3.5-5
  owner: Dev A
  blocked_by: [G04, G05, G07, G09, W1]
  calendar_waits: W1 sign-off before go-live
  wait_days: 0
  handoff: 1
  mentions_only: [G10]
- goal: G10
  phase: 2
  total: 0.5-1
  owner: Dev A
  blocked_by: [G08]
  calendar_waits: 3 clean pilot days at the first salon
  wait_days: 3
- goal: G11
  phase: 2
  total: 4-8
  blocked_by: [G07]
- goal: G12
  phase: 2
  total: 4-6
  blocked_by: [G08]
- goal: G13
  phase: 2
  total: 6-10
  blocked_by: [G08]
- goal: G14
  phase: 2
  total: 5-9
  blocked_by: [G08]
- goal: G15
  phase: 2
  total: 8-13
  blocked_by: [G08]
```

Schedule check, run on 2026-10-14 with
`python3.11 .claude/skills/adk-system-designer/scripts/check_schedule.py --plan docs/plans/salon-booking-assistant.md --tickets docs/tickets/salon-booking-assistant/ --days 10 --reserve 0.25 --person "Dev A=5" --person "Dev B=5" --person "Dev C=5"`.
It exits 0. Phase 1 is 56.5–88.5 h against a capacity of 112.5 h. The longest
chain is G01 → G03 → G04 → G08, 6.27–9.73 working days. The finish is
6.4–10 working days. **The high end has no slack beyond the daily 25 %
reserve.** If G03 or G04 runs high, the first thing to move is the
create-then-cancel move fallback, if G01 finds no atomic reschedule. "Move"
would then launch a few days later, behind its own tool flag, while book and
cancel go live. The floor is never cut: confirmation, ledger and adversarial
cases stay in.

Changes after failing runs, each tried as a what-if with the helper:

| Run | Result | Change and reason |
| --- | --- | --- |
| First draft (G08 included production setup; G06 waited for G01) | Fits in hours, but finish 7.2–11.07 days against 10 (low end only) | — |
| Split launch into G09 production readiness (Dev C) and a smaller G08 go-live | 7.07–10.93 days; the chain moved to Dev C's G06 → G05 path | Production setup does not need the write tools, so it can run earlier on another person |
| Also split in-turn reconciliation out of G03 to Dev A | No better (7.07–10.93) | Rejected; G03 left whole |
| Original plan with Dev B on 6 h/day | 6.8–10.53, low end only | Rejected; extra hours alone do not close the gap |
| Split launch, and G06 starts day 1 without G01 | 6.4–10, fits | Adopted. G06 needs only the assumed pin; G01's pin is adopted by a rebuild. One-salon watch moved to G10 (phase 2), since it is a 3-day calendar wait that cannot fit |

## Implementation map

| Decision / requirement | Component and integration point (proposed) | GCP responsibility | Primary skill | Verification still needed |
| --- | --- | --- | --- | --- |
| D1, D7 | `assistant/agent.py`: `App` with one `LlmAgent`, instruction module, pinned model constant | Vertex AI model access | `adk-workflow-design` | ADK 2.8.0 constructor names (G01) |
| D2, I1 | `assistant/api/auth.py`: JWT and JWKS verification, sets `customer_id` in session state before `Runner.run_async`; owner check on `session_id` | — | `adk-tool-auth-and-secrets` | Site JWT format (O3) |
| D3, I2 | `assistant/tools/write.py`: tools with ADK tool confirmation, or propose/commit; recheck before dispatch | — | `safe-api-tool-calls` | Confirmation support on `DatabaseSessionService` at the pin (G01) |
| D4, I3, I4 | `assistant/booking/ledger.py`, `client.py`, `reconcile.py` | Postgres `assistant` schema | `safe-api-tool-calls` | API idempotency and reschedule (O2) |
| D5 | `DatabaseSessionService` on Postgres | Existing instance, new schema and user | `adk-memory-architecture` | Driver and schema compatibility (G06) |
| D6, D10 | `deploy/` (G06, G09): Cloud Run service, service account, Secret Manager, telemetry with content capture off, `release.json` | Cloud Run, Secret Manager, Cloud Trace, billing alert | `deploy-adk-on-google-cloud` | Region and quota (G06) |
| D8, D9, I6 | `assistant/api/chat.py`, `widget/`: `/chat`, `/confirm`, allowance, kill switch, per-salon flags | — | `adk-frontend-integration` | Widget embedding in the site (G05) |
| Quality, injection | `eval/cases/*.json` and runner; adversarial cases | Vertex AI (bounded) | `adk-agent-evaluation` | Live run cost (G07) |

## Goals and dependencies

Phase 1 goals have tickets. **Each ticket is the home** of its scope, route and
acceptance, and this table links to it.

| ID and goal | Phase | Type | Human hours | Depends on | Primary skill | State / blocker |
| --- | --- | --- | --- | --- | --- | --- |
| W1 Salon chain sign-off (request day 1) | 1 | wait | 0 (3–5 days) | — | — | to request |
| [G01 Booking API contract and pins](../tickets/salon-booking-assistant/G01-api-contract-and-pins.md) | 1 | discovery | 2.5–4 | — | `safe-api-tool-calls` | ready |
| [G02 Read-only assistant answers availability and "my appointments"](../tickets/salon-booking-assistant/G02-read-only-assistant.md) | 1 | implementation | 5.5–9 | G01 | `adk-workflow-design` | blocked by G01 |
| [G03 Booking write service with ledger and idempotency](../tickets/salon-booking-assistant/G03-booking-write-service.md) | 1 | implementation | 9.5–14.5 | G01 | `safe-api-tool-calls` | blocked by G01 |
| [G04 Book, move and cancel by chat with confirmation](../tickets/salon-booking-assistant/G04-confirmed-write-tools.md) | 1 | implementation | 8–13 | G02, G03 | `safe-api-tool-calls` | blocked |
| [G05 Chat API and widget on the booking site](../tickets/salon-booking-assistant/G05-chat-api-and-widget.md) | 1 | implementation | 8–13 | G02, G06 | `adk-frontend-integration` | blocked |
| [G06 Staging environment on Cloud Run](../tickets/salon-booking-assistant/G06-staging-on-cloud-run.md) | 1 | implementation | 7.5–12 | — | `deploy-adk-on-google-cloud` | ready |
| [G07 Evaluation and adversarial set](../tickets/salon-booking-assistant/G07-evaluation-set.md) | 1 | implementation | 7.5–11.5 | G02 | `adk-agent-evaluation` | blocked by G02 |
| [G09 Production readiness and rollback drill](../tickets/salon-booking-assistant/G09-production-readiness.md) | 1 | implementation | 4.5–6.5 | G06 | `deploy-adk-on-google-cloud` | blocked by G06 |
| [G08 Pilot go-live at the first salon](../tickets/salon-booking-assistant/G08-pilot-go-live.md) | 1 | implementation | 3.5–5 | G04, G05, G07, G09, W1 | `deploy-adk-on-google-cloud` | blocked |

**If time runs out early**, the goals stay useful in this order. G01 and G02
make a read-only assistant, which could launch alone as "find a slot and see my
appointments" through G06, G05 and G09. Adding G03 and G04 gives writes. G07 is
the quality evidence. Writes must not launch without G07's adversarial cases.

### Phase 2: graduate and harden

Estimates are in the schedule block and include the ×1.5 multiplier
for a team new to ADK.

- **G10 All five salons.** Switch on the other four salons' flags after 3
  clean pilot days, meeting the design's graduation conditions. Primary
  skill: `deploy-adk-on-google-cloud`. Acceptance: no `uncertain` or
  `partial` row is left unreconciled at salon 1, and all five flags are on.
- **G11 Evaluation gate in CI.** The G07 set runs on every prompt, model or
  tool change, with a threshold and a cost cap. Primary skill:
  `adk-release-engineering`. Acceptance: a PR that breaks confirmation
  behaviour fails CI.
- **G12 Session retention purge and erasure.** **Due before pilot day 30.**
  Primary skill: `adk-memory-architecture`. Acceptance: a seeded session
  31 days old is gone after the job runs, and customer deletion cascades.
- **G13 SLIs, dashboard and alerts.** Tracks the completed-operation rate,
  the tool-error rate per tool, tokens per completed operation, and the age of
  `uncertain` ledger rows. Primary skill: `adk-agent-observability`.
  Acceptance: an injected uncertain row older than 15 min pages the on-call
  developer.
- **G14 Automated reconciliation of uncertain operations.** Replaces the
  manual daily query in the runbook. Primary skill: `safe-api-tool-calls`.
  Acceptance: a commit with a lost response is reconciled without staff
  action.
- **G15 Handoff to salon staff.** "Talk to a person" creates a callback
  request for the right salon. Primary skill: `adk-tool-interface-design`.
  Acceptance: the request reaches the right salon with the conversation
  summary and no other customer's data.

## Later

| Item | Trigger that brings it forward | Risk accepted while it waits | Likely primary skill |
| --- | --- | --- | --- |
| Streaming replies | Measured p50 above 4 s (measured at go-live) | Slower-feeling replies | `adk-frontend-integration` |
| Model failover | One outage longer than 30 min, or the model's retirement date announced | The assistant is down during model outages | `adk-model-and-output-contracts` |
| Canary releases and joint rollback | More than one release a week | Whole-traffic releases | `adk-release-engineering` |
| SDP and Model Armor screening | Free-text notes start being stored or sent to staff | Customer-typed personal data reaches the model | `protect-adk-sensitive-data` |
| SMS / WhatsApp channel | Customer demand after the pilot | — | `adk-frontend-integration` |
| Remembered preferences ("my usual") | Repeated requests in the logs | — | `adk-memory-architecture` |
| Deposits or payments | Business decision | Redesign D3/D4 for money first | `safe-api-tool-calls` |
| Cost and latency tuning | Spend above A3 or p95 above 10 s | — | `optimise-adk-on-google-cloud` |

## What the reviewer reads

| Document | Establishes |
| --- | --- |
| [Design](../architecture/salon-booking-assistant.md) | Method, decisions and assumptions |
| `eval/SUMMARY.md` (created in G07) | Latest result per case |
| This plan | Remaining limits and deferred controls |

## Open decisions for further planning

The open decisions are O1–O6 in the design. G01 settles O2 and O3 as evidence.
O1 and O4 need the founders before G08.

## Resume here

- **Next goals:** G01, booking API contract and pins (Dev A), and G06,
  staging on Cloud Run (Dev C). Both are ready on day 1. G01 settles O2, O3
  and the D3 mechanism. On day 1, also send the W1 request to the salon chain
  owner.
- **Read first:** the design, then this plan, then the G01 ticket.
- **Continuation prompt:**

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G01-api-contract-and-pins.md. Read its design and plan, use its primary and supporting skills, run its verification locally, fill in the Evidence section and set status. Leave changes uncommitted.
```

After that goal, continue with: `/adk-engineer Continue the next ready goal in docs/plans/salon-booking-assistant.md.`
Dev C can start G06 at the same time with its ticket's run prompt. After G01, G02 (Dev A) and G03 (Dev B) run in parallel.
