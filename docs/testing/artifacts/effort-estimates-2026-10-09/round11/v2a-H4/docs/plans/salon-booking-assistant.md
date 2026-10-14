# Implementation plan: salon booking assistant (MVP)

Status: draft, ready goals identified; assumptions unconfirmed; reviewed once
by an independent reviewer (findings settled below)
Architecture: [design](../architecture/salon-booking-assistant.md)
Continuation source of truth: this plan; each phase 1 goal's scope and
acceptance live in its [ticket](../tickets/salon-booking-assistant/)

## Summary for the reader

- **Profile and phase 1:** MVP. Signed-in customers of all five salons book,
  move and cancel their own appointments through a chat widget on the existing
  site. Every change needs the customer's click on a card and happens at most
  once (design I1–I6).
- **Effort:** phase 1 is 53.5–77.5 human hours. Capacity is 81 hours after a
  25 % reserve (3 developers × 3.6 focused h/day × 10 days), so **it fits the
  hours**, but only just at the high end. Dev A is loaded 19–27 h of 27.
- **Finish:** **9.2–13.7 working days, against 10. Two weeks fits at the low
  end only.** The tail cannot be compressed: a staging run, then the salon
  chain's approval wait, then go-live.
- **Recommended cut line:** keep the full scope, because confirmed writes are
  the product. Plan go-live for **14 working days, Thu 5 Nov 2026** (fits at
  the high end), with a staging demo for the salon chain at about day 9–10.
  The alternative is 11 working days if all three developers give 4.8 focused
  h/day (finish 7.1–10.8). No scope cut that I tested fits 10 days at the high
  end: not the move operation, not the evaluation set, not even a read-only
  assistant with deep links (7.3–11.6). See the what-if table.
- **Largest risks:**
  1. The existing login cannot issue a verifiable token (OD1). This adds about
     8–14 h to G02 and moves the finish to 11.4–18.1 days.
  2. The booking API has no atomic reschedule or idempotency key (OD2).
     G01 settles this on days 1–2.
  3. The salon chain is slow with its policies (W1) or its approval (W2).
     Both are on or near the critical path. Dev A asks for both on day 1.
- **Decisions needed from you:**
  - The cut line (OD3).
  - Confirm Q2, Q3, Q6 and Q11 in the design's Assumed answers.
  - Name the GCP project, region and monthly budget (W0).
- **Next prompt:** start G01, G02 and G03 on day 1 (no prerequisites). G04
  follows G01:
  `/adk-engineer Carry out docs/tickets/salon-booking-assistant/G01-booking-api-write-contract.md. Read its design and plan, use its primary and supporting skills, run its verification locally, fill in the Evidence section and set status. Leave changes uncommitted.`

## Destination and constraints

Destination, non-goals and accepted stack: see the design's Purpose and D1–D12.
Nothing has been inspected yet. The repository holds no application code, so
every module path in the design is proposed.

Pinned versions the goals inherit:
- model `gemini-3.5-flash` on Vertex AI (D8);
- `google-adk==2.8.0` as a working assumption, confirmed in G03/A10;
- the prompt version, recorded in G08/A1.

After launch, a goal that changes the model or the prompt is a release, and
G13 comes first.

Authorisation: this session is design only. G06, G08, G10, G11 and G12 each
need the user's authorisation when they run, for the staging booking API, the
GCP project or production.

## Delivery profile and capacity

Profile: MVP or pilot (design, Delivery constraints).

| Phase | Delivers | Goals | Human hours, agent-assisted | Capacity and reserve |
| --- | --- | --- | --- | --- |
| 1, ship | Live booking, moving and cancelling for signed-in customers of five salons | G01 to G12 | 53.5–77.5 | 3 × 3.6 h/day × 10 days = 108 h; 25 % reserve → 81 h |
| 2, harden | CI evaluation gate, first-week figures and alerts, threat model, learning from production, guest booking, preferences | G13 to G18 | 33–58 | When the team has time after launch |

**How to read the hours.**
- Estimates are person-hours of human effort with a coding agent: hands-on
  plus review and verify.
- The team is new to ADK, so **every figure includes a ×1.5 multiplier** on
  the starting points of the delivery-profile reference.
- Handoff hours are included in the receiving goal's total (`handoff:` in the
  schedule).
- Review is heavier on the authorisation boundary (G02) and the write path
  (G04, G06) than on the widget, deployment and evaluation goals.
- Calendar waits are separate entries (W0, W1, W2) and carry no hours.

| Person | Goals | Hours (helper) | Their capacity after reserve, 10 days |
| --- | --- | --- | --- |
| Dev A (knows the booking API) | G01, G04, G06, G11 | 19–27 | 27 |
| Dev B (front end, prompting) | G03, G07, G09 | 17.5–24.5 | 27 |
| Dev C (backend, GCP) | G02, G05, G08, G10, G12 | 17–26 | 27 |

Waits. All three are requested on day 1 (Mon 19 Oct):

- **W0**, from the user: the GCP project, region, monthly budget figure and
  authorisation for cloud work. Assumed 0–1 working days.
- **W1**, from the salon chain: policies and wording (notice window, bookable
  services, refusal wording, phone numbers, opening hours). Assumed 2–4
  working days. Dev A sends the request.
- **W2**, from the salon chain: go-live approval after the staging demo.
  Assumed 1–2 working days.

Schedule block. This is the single machine-readable source of each estimate:

```yaml
- goal: W0
  phase: 1
  total: 0
  blocked_by: []
  calendar_waits: GCP project, region, monthly budget figure and cloud authorisation from the user
  wait_days: 0-1
- goal: W1
  phase: 1
  total: 0
  blocked_by: []
  calendar_waits: salon policies and wording from the salon chain
  wait_days: 2-4
- goal: G01
  phase: 1
  hands_on: 2-4
  review: 1-1
  total: 3-5
  owner: Dev A
  blocked_by: []
  calendar_waits: none
- goal: G02
  phase: 1
  hands_on: 3-5
  review: 2-3
  total: 5-8
  owner: Dev C
  blocked_by: []
  calendar_waits: none
- goal: G03
  phase: 1
  hands_on: 5-7
  review: 2-3
  total: 7-10
  owner: Dev B
  blocked_by: []
  calendar_waits: none
  mentions_only: [W1]
- goal: G04
  phase: 1
  hands_on: 5-7
  review: 3-4
  total: 8-11
  owner: Dev A
  blocked_by: [G01]
  calendar_waits: none
  mentions_only: [W1]
- goal: G05
  phase: 1
  hands_on: 2.5-3.5
  review: 1-1.5
  total: 3.5-5
  owner: Dev C
  blocked_by: [G02]
  calendar_waits: none
- goal: G06
  phase: 1
  hands_on: 4.5-5.5
  review: 1.5-2.5
  total: 6-8
  owner: Dev A
  blocked_by: [G01, G02, G04]
  calendar_waits: none
  handoff: 0.5
- goal: G07
  phase: 1
  hands_on: 4.5-5.5
  review: 1-2
  total: 5.5-7.5
  owner: Dev B
  blocked_by: [G02]
  calendar_waits: none
  handoff: 0.5
- goal: G08
  phase: 1
  hands_on: 3-5
  review: 1-1
  total: 4-6
  owner: Dev C
  blocked_by: [G02, W0]
  calendar_waits: none
- goal: G09
  phase: 1
  hands_on: 4-6
  review: 1-1
  total: 5-7
  owner: Dev B
  blocked_by: [G03, W0, W1]
  calendar_waits: none
  handoff: 0.5
- goal: G10
  phase: 1
  hands_on: 2-3
  review: 0.5-1
  total: 2.5-4
  owner: Dev C
  blocked_by: [G03, G05, G06, G07, G08, G09]
  calendar_waits: none
  handoff: 1.5
- goal: G12
  phase: 1
  hands_on: 1.5-2
  review: 0.5-1
  total: 2-3
  owner: Dev C
  blocked_by: [G10]
  calendar_waits: none
- goal: W2
  phase: 1
  total: 0
  blocked_by: [G10]
  calendar_waits: salon chain go-live approval after the staging demo
  wait_days: 1-2
- goal: G11
  phase: 1
  hands_on: 2-2
  review: 0-1
  total: 2-3
  owner: Dev A
  blocked_by: [G10, G12, W2]
  calendar_waits: none
  handoff: 0.5
- goal: G13
  phase: 2
  total: 6-10
  blocked_by: [G11]
- goal: G14
  phase: 2
  total: 5-8
  blocked_by: [G11]
- goal: G15
  phase: 2
  total: 4-8
  blocked_by: [G11]
- goal: G16
  phase: 2
  total: 6-10
  blocked_by: [G13]
- goal: G17
  phase: 2
  total: 8-14
  blocked_by: [G15]
- goal: G18
  phase: 2
  total: 4-8
  blocked_by: [G11]
```

**Schedule check**, run 2026-10-15 with Python 3.12:

```bash
python3 .claude/skills/adk-system-designer/scripts/check_schedule.py --plan docs/plans/salon-booking-assistant.md --tickets docs/tickets/salon-booking-assistant/ --design docs/architecture/salon-booking-assistant.md --days 10 --reserve 0.25 --person "Dev A=3.6" --person "Dev B=3.6" --person "Dev C=3.6"
```

Result:
- 53.5–77.5 h against a capacity of 81 h: fits.
- Longest chain at the high end: G01 → G04 → G06 → G10 → W2 → G11, 13.48 days.
- Finish: 9.15–13.67 working days.
- Calendar: fits at the low end only. Exit status 1 for that reason alone; no
  other problems were reported.
- With `--days 14`, the calendar fits.

**If time runs out early:** no subset launches materially earlier. A
read-only launch still finishes at 7.3–11.6 days, because going live always
needs the chat API, widget, deployment, staging run, approval and release.
If the work runs high, the date moves (OD3). Scope does not shrink below the
floor.

### What-ifs run with the helper

Each row is one run of the helper on a copy of this schedule. Finish is in
working days, with a 25 % reserve.

| Change | Phase 1 hours | Finish | Calendar |
| --- | --- | --- | --- |
| As planned | 53.5–77.5 | 9.15–13.67 | 10 days: low end only; 13 days: low end only; 14 days: fits |
| All three at 4.2 focused h/day | 53.5–77.5 | 7.98–12.00 | 10 days: low end only |
| All three at 4.8 focused h/day | 53.5–77.5 | 7.11–10.75 | 10 days: low end only; 11 days: fits |
| Move operation cut to phase 2 (G03, G04, G06 smaller) | 49.5–73.5 | 8.78–13.30 | 10 days: low end only |
| Evaluation set (G09) moved to phase 2 | 48–70 | 8.96–13.48 | 10 days: low end only |
| Read-only assistant with deep links to the existing booking pages (no G01, G04, G06) | 33.5–49.5 | 7.30–11.63 | 10 days: low end only |
| OD1: no verifiable login token (G02 13–22 h) | 61.5–91.5 | 11.37–18.11 | 10 days: no; 14 days: low end only; Dev C 25–40 h of 27 |

### Changes after failing runs and review

| Change | Why it is true of the work |
| --- | --- |
| Split identity (G02) from admission (G05) | Admission is independent work once the app exists |
| Split the write path into G04 (operations service on a fake adapter) and G06 (real adapter, route mounting, operator controls) | The claim, recheck and reconcile logic does not depend on the API answers; the adapter does |
| G03 owns all six tool declarations, calling an operations interface that G04 implements | One owner for the model-facing contract |
| Review 1: W2 now waits for G10 (the staging demo) | The salon chain approves what it has seen working |
| Review 1: rehearsal split into G10 (journey and demo) and G12 (drills and staging eval, run during W2) | The approval judges the journey; the drills are the team's own evidence and must finish before G11 |
| Review 1: handoff hours added into the receiving goals' totals (G06, G07, G09, G10, G11) | The helper does not add them itself |
| Review 1: G04 blocked by G01 | G01's findings must reach G04 before it starts; no date effect |
| Review 1: operator controls over operations moved from G05 to G06 | They need the operations store from G04; G05 keeps chat-side admission |
| Review 1: day-1 production watch moved from G11 to phase 2 (G14) | It cannot be checked until a day after go-live |
| Review 1: W0 added before G08 and G09 | Live model runs and deployment need the GCP project |
| Review 1: G09 no longer waits for G04 | The live eval measures the model's proposals against G03's fake operations interface; the real service is exercised on staging in G12 |
| Review 1: widget deployment to the site's staging (G07/A6) and production (G11/A1) added | Nothing else delivers them |
| Review 1: W1 values loaded into config in G09 | Previously owned by nobody |
| Review 1: grid cells corrected (Cloud SQL rows, login key rotation G02/A8, partial move cites G01/A2 and G06/A1, new G04/A13 and G04/A14) | The cited items did not test the claim |
| Review 1: "allow 11 days" and "G02 + G03 could launch first" claims removed | The reruns did not support them |
| Rejected: removing W1 or W2, shortening them, or dropping the drills | Not true of the work |

## Implementation map

Components and integration points are in the design's decision table (D1–D12).
Each ticket names its primary skill. Unverified items:
- the ADK pin (G03/A10);
- model availability in the region (G08/A3);
- the booking API's replay and reschedule contract (G01);
- the login token (G02, OD1).

## Goals and dependencies

| ID and goal | Phase | Type | Hours | Depends on | Primary skill | Owner | State |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [G01 Booking API write contract](../tickets/salon-booking-assistant/G01-booking-api-write-contract.md) | 1 | discovery | 3–5 | — | safe-api-tool-calls | Dev A | ready |
| [G02 Signed-in chat API](../tickets/salon-booking-assistant/G02-signed-in-chat-api.md) | 1 | implementation | 5–8 | — | adk-tool-auth-and-secrets | Dev C | ready (OD1 checked first) |
| [G03 Assistant reads and proposes](../tickets/salon-booking-assistant/G03-assistant-reads-and-proposes.md) | 1 | implementation | 7–10 | — | adk-tool-interface-design | Dev B | ready |
| [G04 Confirmed operations](../tickets/salon-booking-assistant/G04-confirmed-operations.md) | 1 | implementation | 8–11 | G01 | safe-api-tool-calls | Dev A | proposed |
| [G05 Admission controls](../tickets/salon-booking-assistant/G05-admission-and-operator-controls.md) | 1 | implementation | 3.5–5 | G02 | adk-operational-guardrails | Dev C | proposed |
| [G06 Booking API write adapter and operator controls](../tickets/salon-booking-assistant/G06-booking-api-write-adapter.md) | 1 | implementation | 6–8 | G01, G02, G04 | safe-api-tool-calls | Dev A | proposed |
| [G07 Chat widget](../tickets/salon-booking-assistant/G07-chat-widget.md) | 1 | implementation | 5.5–7.5 | G02 | adk-frontend-integration | Dev B | proposed |
| [G08 Cloud Run staging and production](../tickets/salon-booking-assistant/G08-cloud-run-staging-and-production.md) | 1 | implementation | 4–6 | G02, W0 | deploy-adk-on-google-cloud | Dev C | proposed |
| [G09 Evaluation set and CI](../tickets/salon-booking-assistant/G09-evaluation-set-and-ci.md) | 1 | implementation | 5–7 | G03, W0, W1 | adk-agent-evaluation | Dev B | proposed |
| [G10 Journey on staging and demo](../tickets/salon-booking-assistant/G10-staging-rehearsal.md) | 1 | implementation | 2.5–4 | G03, G05–G09 | deploy-adk-on-google-cloud | Dev C | proposed |
| [G12 Staging failure drills](../tickets/salon-booking-assistant/G12-staging-failure-drills.md) | 1 | implementation | 2–3 | G10 | deploy-adk-on-google-cloud | Dev C | proposed |
| [G11 Go-live](../tickets/salon-booking-assistant/G11-go-live.md) | 1 | implementation | 2–3 | G10, G12, W2 | deploy-adk-on-google-cloud | Dev A | proposed |

The tickets say "ready" because their design questions are settled. The State
column is the schedule's view: a goal whose prerequisites are unfinished
shows as proposed.

**Who could take which.** The owners above assume Q14's strengths:

- **Dev A** knows the booking API. A takes discovery and the whole write path
  (G01, G04, G06), plus go-live (G11).
- **Dev B** does front end and prompting. B takes the agent and its tools
  (G03), the widget (G07) and the evaluation set (G09).
- **Dev C** does backend and GCP. C takes the chat API and admission (G02,
  G05), deployment (G08) and the staging run and drills (G10, G12).

If your developers' strengths differ, swap whole goals between people with the
same load and rerun the schedule check.

### Phase 2 goals (outline; phase 1 results will change them)

- **G13 Evaluation gate in CI and model comparison.**
  - Outcome: the live eval runs on every prompt or model change and fails the
    build below its threshold. Also compares `gemini-3.8-flash` with the
    pinned model on the frozen set.
  - Primary skill: `adk-release-engineering`. Estimate: 6–10 h.
  - Check: a deliberately broken prompt fails CI.
- **G14 First-week figures, SLOs and alerts.**
  - Outcome: first day and first week recorded (errors, uncertain operations,
    tokens per turn, p95 reply time, completed operations compared with the
    phone baseline). Alerts on the completed-operation ratio, uncertain
    operations older than 1 hour, tool error rate and tokens per completed
    operation.
  - Primary skill: `adk-agent-observability`. Estimate: 5–8 h.
  - Check: a forced `uncertain` operation raises an alert within 15 minutes.
- **G15 Threat model and adversarial suite.**
  - Primary skill: `adk-agent-security`. Estimate: 4–8 h.
  - Check: the suite runs in CI with forbidden-action assertions.
- **G16 Learn from the first weeks.**
  - Outcome: redacted production sessions become eval cases, and instruction
    fixes are measured on the set.
  - Primary skill: `adk-agent-evaluation`. Estimate: 6–10 h.
  - Check: an error-analysis table with before and after scores.
- **G17 Guest booking for new customers.**
  - Outcome: sign-in with a one-time code.
  - Primary skill: `adk-tool-auth-and-secrets`. Estimate: 8–14 h, plus any
    wait for SMS provider registration.
  - Check: a guest can book but cannot see or change anyone else's
    appointments.
- **G18 Preferences ("my usual stylist").**
  - Outcome: preferences taken from booking history, scoped to their owner.
  - Primary skill: `adk-memory-architecture`. Estimate: 4–8 h.
  - Check: the preference is used in a new session, denied across customers,
    and can be forgotten.

## Later

| Item | Trigger that brings it forward | Risk accepted while it waits | Likely primary skill |
| --- | --- | --- | --- |
| Model migration off `gemini-3.5-flash` | 1 Mar 2027 or a retirement notice (Vertex retirement 2027-05-19 or later) | None until then | adk-release-engineering |
| Content screening (Model Armor / SDP) | Health details or free-text notes appear in chats | Personal free text stored for 30 days | protect-adk-sensitive-data |
| Canary releases | More than one release per week | A bad release reaches all salons; per-salon flags and rollback limit it | adk-release-engineering |
| Streaming replies | p95 reply time above 8 s | Slower-feeling replies | adk-frontend-integration |
| Other channels (WhatsApp, phone) | Customer demand after launch | — | adk-frontend-integration |
| Performance and cost tuning | Cost per completed operation above target | Higher spend within the cap | optimise-adk-on-google-cloud |
| Secret rotation automation | A second credential or a security review | Manual rotation | adk-tool-auth-and-secrets |

## What the reviewer reads

| Document | Establishes |
| --- | --- |
| [Design](../architecture/salon-booking-assistant.md) | Decisions, guarantees, failure coverage |
| Evaluation results file from G09 and G12 (to be created) | Latest result per case |
| This plan | Schedule, cut line, deferred work |

## Open decisions for further planning

See the design's Open decisions (OD1–OD6). Only the user can settle OD3 (the
cut line), and it moves the go-live date.

## Resume here

- **Next goals:** G01, G02 and G03, which have no prerequisites. G04 follows
  G01 for Dev A.
- **Read first:** the design, this plan and the ticket.
- **Next action:** Dev A sends the W1 request to the salon chain, the user
  answers W0, and Dev A opens the booking API repository for G01.
- **Continuation prompt:**

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G01-booking-api-write-contract.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

After that goal, the same request without a goal ID continues with the next
ready one: `/adk-engineer Continue the next ready goal in docs/plans/salon-booking-assistant.md.`
