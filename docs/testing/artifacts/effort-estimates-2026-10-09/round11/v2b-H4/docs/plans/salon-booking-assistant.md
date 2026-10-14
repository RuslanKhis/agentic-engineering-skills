# Implementation plan: salon booking assistant (MVP)

Status: draft, ready goals identified (assumptions unconfirmed; independent
review done and settled, see the change table)
Architecture: [docs/architecture/salon-booking-assistant.md](../architecture/salon-booking-assistant.md)
Continuation source of truth: this plan; phase 1 goals live in
[docs/tickets/salon-booking-assistant/](../tickets/salon-booking-assistant/)

## Summary for the reader

- **Profile and phase 1:** MVP. Phase 1 puts a web chat assistant in front of
  signed-in customers of all five salons. It books, moves and cancels their own
  appointments through the existing booking API, and makes each change only
  after the customer presses Confirm on a stored proposal (design D2).
- **Effort and finish:** 73–112 human hours (agent-assisted) against 112.5 h of
  capacity after a 25 % reserve over 10 working days. That fits in hours, but
  the high end uses the whole capacity. With dependencies and one goal at a
  time per person, the finish is **9.13–13.87 working days**. Day 10 fits **at
  the low end only**; day 14 fits. Schedule check run 2026-10-15 (command below).
- **Cut line (assumed answer to Q15):** phase 1 = W1–W3 and G01–G10. Every one
  of them is needed for a safe launch. **Target go-live: day 10. Committed
  go-live: day 14.** Cutting scope does not close the gap: dropping "move" or
  shrinking the evaluation set saves under 0.1 day (what-ifs below). Only the
  date or about 7 focused hours a day from all three closes it, and 7 hours a
  day for two weeks is a crunch I do not recommend. Checkpoint at the end of day
  5: if G03 is not done and G04 not started, announce day 14.
- **Largest risks:**
  1. The operations manager wants a staging demo before signing off: finish
     12.07–19.4 days. Dev B asks them on day 1 what evidence they need (W1).
  2. Our backend cannot verify the website login (Q5), so guest OTP login
     moves into phase 1: finish 11.47–18.13 days. Dev C checks a sample token
     on day 1.
  3. Model quality on real phrasing falls below the bar in G07. Dev B owns it;
     prompt iteration is inside G07's hours.
- **Decisions needed from you:** confirm day 10 target / day 14 commitment
  (Q15); confirm Q2 (5 focused h/day, new to ADK), Q5 (website token), Q16
  (website is ours) and Q17 (GCP project); approve sending the W1 request today.
- **Next prompt:** `/adk-engineer Carry out docs/tickets/salon-booking-assistant/G01-booking-api-contract.md.`

## Destination and constraints

End result of phase 1: the design's journey runs in production for signed-in
customers. Non-goals: see the design's purpose section. Accepted stack (all
proposed, no code exists yet): Python, google-adk (working assumption 2.8.0,
confirmed in G03/A8), FastAPI, Cloud Run, Cloud SQL PostgreSQL with IAM database
authentication, Secret Manager, Vertex AI `gemini-3.5-flash` (D8). Prompt:
`prompts/booking_agent/instruction.md`, versioned in git. A change to the prompt
or model is a release (G08/A6). Authorization in this session: design only.
Implementation goals need the team's GCP project (W3), the staging booking API
and the go-live sign-off (W1).

Proposed layout:

```text
app/booking/port.py          BookingPort protocol, result types, in-memory fake  (G01)
app/booking/http_adapter.py  real adapter, staging fault toggle                  (G02)
app/agent/agent.py, tools.py LlmAgent and six tools                              (G03)
app/operations/              proposals, operations, confirm service, Postgres    (G04)
app/gateway/                 FastAPI, JWT, sessions, allowance, kill switch      (G05)
app/web/                     chat page                                           (G06)
tests/eval/                  labelled cases, runner, RESULTS.md                  (G07)
deploy/                      Cloud Run, Cloud SQL, secrets, release record       (G08)
docs/runbooks/               reconciliation and kill switch                      (G10)
```

## Delivery profile and capacity

Profile: **MVP** (design, delivery constraints).

| Phase | Delivers | Goals | Human hours, agent-assisted | Capacity and reserve |
| --- | --- | --- | --- | --- |
| 1, ship | Customers book, move and cancel safely in production | W1–W3, G01–G10 | 73–112 | 3 people × 5 h/day × 10 days = 150 h; 25 % reserve → 112.5 h (157.5 h by day 14) |
| 2, harden | First-week review, eval gate, SLOs, adversarial suite, guest login, automatic reconciliation | G11–G19 | 42–76 | After launch |

Estimates are human hours (hands-on plus review) for developers new to ADK.
They are the designer's starting points multiplied by **1.5** on every goal
(Q2), with handoff hours added to the receiving goal's hands-on figure.
Calendar waits are separate. Review is heaviest on G04, G05 and G02 (writes,
identity) and lightest on G06, G08 and G09.

| Person | Goals | Hours | Their capacity after reserve (10 days / 14 days) |
| --- | --- | --- | --- |
| Dev A (agent and writes) | G01, G03, G04, G09 | 24–38 | 37.5 / 52.5 |
| Dev B (booking API, evaluation, launch) | W1 request, G02, G07, G10 | 28–40 | 37.5 / 52.5 |
| Dev C (website, gateway, platform) | G05, G06, G08 | 21–34 | 37.5 / 52.5 |

Why this split: Dev A keeps the agent's tools, the confirm path and their
wiring in one head, because they share the proposal record. Dev B changes the
booking API, judges model quality and runs the launch with the salon. Dev C
owns everything between the browser and Cloud Run, including our website's
login and route (Q16). Over 10 days Dev A and Dev B are over capacity at the
high end; that is the same fact as the day-14 finish.

Day 1: Dev A starts G01. Dev B drafts the privacy line and the one-page
description, sends the W1 request, books the W2 session, then works on G02 as
soon as G01's port exists. Dev C confirms W3 and a sample website token (Q5),
then starts G05.

Schedule block (the single source of estimates; tickets copy it):

```yaml
- goal: W1
  phase: 1
  hands_on: 1-2
  review: 0
  total: 1-2
  owner: Dev B
  blocked_by: []
  calendar_waits: salon chain go-live sign-off and privacy notice approval, requested day 1
  wait_days: 3-5
- goal: W2
  phase: 1
  total: 0
  blocked_by: []
  calendar_waits: front-desk walkthrough session booked with the salon, requested day 1
  wait_days: 0-1
- goal: W3
  phase: 1
  total: 0
  blocked_by: []
  calendar_waits: GCP project access, Vertex AI enabled and billing alert permissions for all three, day 1
  wait_days: 0-1
- goal: G01
  phase: 1
  hands_on: 3-4
  review: 1-2
  total: 4-6
  owner: Dev A
  blocked_by: []
  calendar_waits: none
  wait_days: 0
- goal: G02
  phase: 1
  hands_on: 8-11
  review: 3-4
  total: 11-15
  owner: Dev B
  blocked_by: [G01]
  calendar_waits: none
  wait_days: 0
  handoff: 1
- goal: G03
  phase: 1
  hands_on: 4-6
  review: 2-3
  total: 6-9
  owner: Dev A
  blocked_by: [G01]
  calendar_waits: none
  wait_days: 0
- goal: G04
  phase: 1
  hands_on: 5-9
  review: 4-6
  total: 9-15
  owner: Dev A
  blocked_by: [G01, G03]
  calendar_waits: none
  wait_days: 0
- goal: G05
  phase: 1
  hands_on: 6-8
  review: 3-5
  total: 9-13
  owner: Dev C
  blocked_by: []
  calendar_waits: none
  wait_days: 0
- goal: G06
  phase: 1
  hands_on: 5-7
  review: 1-3
  total: 6-10
  owner: Dev C
  blocked_by: [G05]
  calendar_waits: none
  wait_days: 0
- goal: G07
  phase: 1
  hands_on: 7-10
  review: 2-3
  total: 9-13
  owner: Dev B
  blocked_by: [G03, W3]
  calendar_waits: none
  wait_days: 0
  handoff: 1
- goal: G08
  phase: 1
  hands_on: 4-8
  review: 2-3
  total: 6-11
  owner: Dev C
  blocked_by: [G05, W3]
  calendar_waits: none
  wait_days: 0
- goal: G09
  phase: 1
  hands_on: 4-6
  review: 1-2
  total: 5-8
  owner: Dev A
  blocked_by: [G02, G03, G04, G05, G06, G08]
  calendar_waits: none
  wait_days: 0
  handoff: 2
- goal: G10
  phase: 1
  hands_on: 5-7
  review: 2-3
  total: 7-10
  owner: Dev B
  blocked_by: [W1, W2, G07, G09]
  calendar_waits: none beyond W1 and W2
  wait_days: 0
  handoff: 1
- goal: G11
  phase: 2
  total: 4-6
  blocked_by: [G10]
  wait_days: 5
- goal: G12
  phase: 2
  total: 4-8
  blocked_by: [G07, G08]
- goal: G13
  phase: 2
  total: 4-8
  blocked_by: [G10]
- goal: G14
  phase: 2
  total: 5-9
  blocked_by: [G07]
- goal: G15
  phase: 2
  total: 10-16
  blocked_by: [G05]
- goal: G16
  phase: 2
  total: 5-9
  blocked_by: [G04, G02]
- goal: G17
  phase: 2
  total: 4-8
  blocked_by: [G10]
- goal: G18
  phase: 2
  total: 3-6
  blocked_by: [G10]
- goal: G19
  phase: 2
  total: 3-6
  blocked_by: [G07]
```

Schedule check, run 2026-10-15 with Python 3.11:

```bash
python3.11 .claude/skills/adk-system-designer/scripts/check_schedule.py \
  --plan docs/plans/salon-booking-assistant.md \
  --tickets docs/tickets/salon-booking-assistant/ \
  --design docs/architecture/salon-booking-assistant.md \
  --days 10 --reserve 0.25 --person "Dev A=5" --person "Dev B=5" --person "Dev C=5"
```

Result: phase 1 73–112 h; capacity 112.5 h, fits; longest dependent chain
(high) G01 → G03 → G04 → G09 → G10, 12.8 working days; finish 9.13–13.87
working days; calendar fits at the low end only. Exit 1 is for that reason
alone: the ticket/plan comparison and the coverage grid check report no problems.
With `--days 14` the same plan fits.

If time runs out early, the goals stay useful in this order:
1. G01 → G03 → G04: the assistant works end to end locally with the fake.
2. G05 → G06 → G08: customers could reach it on staging.
3. G02 → G09 → G07 → G10: production.

### What-ifs

Each row is the command above with one change; figures are the helper's.

| Change | Finish (working days) | Fits 10 days? |
| --- | --- | --- |
| None (plan as written) | 9.13–13.87 | Low end only |
| Go-live day 12 / day 13 | 9.13–13.87 | Low end only |
| Go-live day 14 | 9.13–13.87 | Yes (`--days 14`) |
| Dev B (busiest) 6.5 h/day | 8.37–13.25 | Low end only |
| Dev A and Dev B 6.5 h/day | 8.06–12.76 | Low end only |
| All three 6 h/day | 8.11–11.56 | Low end only |
| All three 6.5 h/day | 7.72–10.67 | Low end only |
| All three 7 h/day | 6.29–9.9 | Yes |
| Cut "move" (G03 −1 h, G04 −2/−3 h, G06 −1 h, G07 −1 h) | 9.13–13.8 | Low end only |
| Cut "move" and a 20-case evaluation set (G07 7–10 h) | 9.13–13.8 | Low end only |
| Risk: sign-off needs a staging demo (W1 after G09) | 12.07–19.4 | No |
| Risk: Q5 wrong, guest OTP login (10–16 h, Dev C) in phase 1 | 11.47–18.13 | No; at day 14 low end only |

Other structures tried with the helper did not shorten the finish. These were:
G04 not waiting for G03 (with its Runner test moved to G09), splitting
evaluation into labelling and running, splitting go-live, and every owner
assignment. The best assignment found was 9.13–13.33 days, but it gives Dev A
the agent's API adapter and Dev C the agent, so I kept the coherent split above.

## Implementation map

| Decision | Component and integration point (proposed) | GCP responsibility | Primary skill | Verification still needed |
| --- | --- | --- | --- | --- |
| D1, D12 | `LlmAgent` in `app/agent/agent.py` run by the gateway's `Runner` | Vertex AI model endpoint | `adk-tool-interface-design` | ADK 2.8.0 names vs the chosen pin (G03/A8) |
| D2, D4 | `app/operations/confirm.py` behind `POST /api/proposals/{id}/confirm`; Postgres row lock | Cloud SQL | `safe-api-tool-calls` | Booking API replay semantics (G01, G02) |
| D3 | FastAPI dependency verifying the JWT and writing `customer_id` to session state before `Runner.run_async` | — | `adk-tool-auth-and-secrets` | Website token format (Q5) |
| D5 | `BookingPort.reschedule` or compensating pair | — | `safe-api-tool-calls` | G01/A4 |
| D6 | `DatabaseSessionService` and app tables through the Cloud SQL Python Connector, IAM DB auth | Cloud SQL | `adk-memory-architecture` (supporting) | Session service compatibility with the pin |
| D7, D11 | Cloud Run service, `sa-assistant`, Cloud Trace exporter, content capture off | Cloud Run, Trace, Logging, Secret Manager | `deploy-adk-on-google-cloud` | Content-capture gates in the pin |
| D9 | `app/web/` page on our website's `/assistant` route | Same Cloud Run service | `adk-frontend-integration` | — |
| D10 | `RunConfig(max_llm_calls=10)`; allowance table; `KILL_SWITCH` env | Billing alerts | `adk-operational-guardrails` | Allowance numbers after week 1 (G11) |
| Wiring | Gateway composes real agent, confirm service and adapter per environment | Cloud Run config | `adk-workflow-design` | G09/A1 |

## Goals and dependencies

Phase 1 goals live in their tickets (scope, route, acceptance); this table only
links them.

| ID and goal | Type | Human hours | Depends on | Owner | Primary skill | State |
| --- | --- | --- | --- | --- | --- | --- |
| W1 Go-live sign-off and privacy notice | wait 3–5 days after a 1–2 h request | 1–2 | — | Dev B | — | send day 1 |
| W2 Front-desk walkthrough session booked | wait 0–1 day | 0 | — | Dev B | — | book day 1 |
| W3 GCP project, Vertex AI, billing alert access | wait 0–1 day | 0 | — | Dev C | — | check day 1 |
| [G01 Booking API contract, port and fake](../tickets/salon-booking-assistant/G01-booking-api-contract.md) | discovery + implementation | 4–6 | — | Dev A | `safe-api-tool-calls` | ready |
| [G02 Real adapter and idempotent writes](../tickets/salon-booking-assistant/G02-booking-api-adapter-idempotency.md) | implementation | 11–15 | G01 | Dev B | `safe-api-tool-calls` | blocked by G01 |
| [G03 Agent that reads and proposes](../tickets/salon-booking-assistant/G03-agent-read-and-propose.md) | implementation | 6–9 | G01 | Dev A | `adk-tool-interface-design` | blocked by G01 |
| [G04 Confirmed, idempotent writes](../tickets/salon-booking-assistant/G04-confirm-and-execute.md) | implementation | 9–15 | G01, G03 | Dev A | `safe-api-tool-calls` | blocked |
| [G05 Gateway: identity, sessions, allowance](../tickets/salon-booking-assistant/G05-gateway-identity-sessions.md) | implementation | 9–13 | — | Dev C | `adk-tool-auth-and-secrets` | ready (Q5 assumed) |
| [G06 Chat page with proposal cards](../tickets/salon-booking-assistant/G06-chat-page.md) | implementation | 6–10 | G05 | Dev C | `adk-frontend-integration` | blocked by G05 |
| [G07 Evaluation set and quality bar](../tickets/salon-booking-assistant/G07-evaluation-set.md) | implementation | 9–13 | G03, W3 | Dev B | `adk-agent-evaluation` | blocked |
| [G08 Staging and production on Cloud Run](../tickets/salon-booking-assistant/G08-cloud-run-deploy.md) | implementation | 6–11 | G05, W3 | Dev C | `deploy-adk-on-google-cloud` | blocked |
| [G09 Integrated staging build](../tickets/salon-booking-assistant/G09-integrated-staging-build.md) | implementation | 5–8 | G02, G03, G04, G05, G06, G08 | Dev A | `adk-workflow-design` | blocked |
| [G10 Staging end to end and go-live](../tickets/salon-booking-assistant/G10-staging-e2e-and-go-live.md) | implementation | 7–10 | W1, W2, G07, G09 | Dev B | `deploy-adk-on-google-cloud` | blocked |

### Phase 2 goals (written now, refined after phase 1 runs)

### G11 — First-week review of production operations
Primary: `safe-api-tool-calls`; supporting `adk-agent-observability`. 4–6 h
spread over the five working days after go-live (wait 5 days); this is the
launch-week rota from design Q11. Outcome: every operation compared with the
booking API daily; allowance and kill-switch thresholds tuned. Acceptance A1:
a dated log of five daily comparisons with zero unexplained differences.
Run: `/adk-engineer Carry out G11 from docs/plans/salon-booking-assistant.md.`

### G12 — Evaluation gate in CI and release record
Primary: `adk-release-engineering`; supporting `adk-agent-evaluation`. 4–8 h.
Outcome: every merge runs the scripted tests and the evaluation set; a drop
below the bar fails the build. Acceptance A1: a prompt change that breaks a
labelled case fails CI by exit code.
Run: `/adk-engineer Carry out G12 from docs/plans/salon-booking-assistant.md.`

### G13 — SLIs, dashboard and alerts
Primary: `adk-agent-observability`. 4–8 h. Outcome: the design's proposed SLIs
with targets from the first week's baseline; an alert on any unknown outcome
older than 30 min. Acceptance A1: a forced unknown in staging pages the on-call
developer, and the alert links to the session.
Run: `/adk-engineer Carry out G13 from docs/plans/salon-booking-assistant.md.`

### G14 — Threat model and adversarial suite
Primary: `adk-agent-security`. 5–9 h. Outcome: a threat model and 20+
adversarial cases with deterministic forbidden-action assertions. Acceptance
A1: no case produces a proposal for another customer's appointment or any write.
Run: `/adk-engineer Carry out G14 from docs/plans/salon-booking-assistant.md.`

### G15 — Guest booking with phone verification
Primary: `adk-tool-auth-and-secrets`; supporting `adk-operational-guardrails`.
10–16 h plus SMS provider setup. Outcome: customers without an account verify a
phone number by one-time code before they can see or change appointments.
Acceptance A1: an unverified caller cannot list, or propose a change to, any
appointment.
Run: `/adk-engineer Carry out G15 from docs/plans/salon-booking-assistant.md.`

### G16 — Automatic reconciliation of unknown and partial operations
Primary: `safe-api-tool-calls`. 5–9 h. Outcome: a scheduled job settles
`unknown` operations by lookup and lists `partial` ones for the front desk.
Acceptance A1: a lost-response drill settles within 10 min without a person.
Run: `/adk-engineer Carry out G16 from docs/plans/salon-booking-assistant.md.`

### G17 — Feedback and production-to-evaluation loop
Primary: `adk-agent-observability`; supporting `protect-adk-sensitive-data`.
4–8 h. Outcome: thumbs up/down on each reply, and a weekly sample of redacted
sessions becomes evaluation cases. Acceptance A1: a thumbs-down session appears
as a redacted candidate case.
Run: `/adk-engineer Carry out G17 from docs/plans/salon-booking-assistant.md.`

### G18 — Sensitive-data review of free text and retention audit
Primary: `protect-adk-sensitive-data`. 3–6 h. Outcome: decide whether
appointment notes reach the model at all, and verify 30-day session deletion
in production. Acceptance A1: no session older than 30 days exists.
Run: `/adk-engineer Carry out G18 from docs/plans/salon-booking-assistant.md.`

### G19 — Compare gemini-3.8-flash and re-baseline
Primary: `adk-model-and-output-contracts`; supporting `adk-agent-evaluation`.
3–6 h. Outcome: a side-by-side run on the frozen evaluation set. Switch only if
the new model is better at equal or lower cost, and ship the switch as its own
release. Acceptance A1: both results recorded with model IDs and dates.
Run: `/adk-engineer Carry out G19 from docs/plans/salon-booking-assistant.md.`

## Later

| Item | Trigger that brings it forward | Risk accepted while it waits | Likely primary skill |
| --- | --- | --- | --- |
| Streaming replies | Median reply time > 5 s in SLI data | Slower-feeling replies | `adk-frontend-integration` |
| "Book my usual" preferences | Repeated requests in feedback | Customers restate preferences | `adk-memory-architecture` |
| SMS/WhatsApp channel | Business asks; web adoption measured | Web only | `adk-agent-interoperability` |
| Staff-facing assistant | Front-desk request | — | `adk-system-designer` (new design) |
| Canary releases | Second customer-visible release per week | Whole-revision rollback only | `adk-release-engineering` |
| Shared budget across instances | > 1,000 conversations/day | Per-customer allowance only | `adk-operational-guardrails` |
| Model migration off gemini-3.5-flash | Vertex retirement notice; re-check by 2027-03 | — | `adk-release-engineering` |
| Cost and latency tuning | Cost above Q3 or latency complaints | — | `optimise-adk-on-google-cloud` |

## What the reviewer reads

| Document | Establishes |
| --- | --- |
| [Design](../architecture/salon-booking-assistant.md) | Decisions, invariants, failure grids |
| `tests/eval/RESULTS.md` (created in G07) | Latest evaluation result per case |
| This plan | Schedule, cut line, deferred work |

## Open decisions for further planning

| Decision / question | Known facts and alternatives | Evidence or decision needed | Blocks |
| --- | --- | --- | --- |
| Day 10 target, day 14 commitment (Q15) | What-ifs above | User | Cut line |
| Website token (Q5) and website ownership (Q16) | JWT + JWKS on our own site assumed; otherwise G15 enters phase 1 | User / sample token on day 1 | G05 |
| Booking API capabilities (Q6) | Idempotency, reschedule, lookup unknown | G01 | G02, G04 |
| Sign-off evidence (Q10) | One page + privacy wording assumed | Operations manager, day 1 | G10 |
| Hours and ADK familiarity (Q2) | 5 h/day, ×1.5 | User | All estimates |

## Change table

First draft → independent review (fresh-context subagent, 2026-10-15) →
this version. Every finding is settled here.

| Change or finding | What changed and why |
| --- | --- |
| Draft: G08 blocked by G03 | Removed before review: infrastructure does not need the agent |
| Review P1: G08 acceptance needed the agent and chat page | G08/A1 now uses curl and a stub agent with the real model; the chat-page and real-agent checks moved to the new G09 (A2, A4). G08 stays blocked by G05 only, plus W3 |
| Review P2: G04/A9 is a Runner test of G03's tools | G04 blocked by G01 and G03 |
| Review P3: no goal wired the real parts together | New G09 "Integrated staging build" (5–8 h, Dev A). The draft's G09 became G10, and phase 2 goals shifted to G11–G19 |
| Review P4: region tied to W1 | Region is the booking API's, known to the team (design Q9); only the privacy wording waits on W1 |
| Review P5: booking API changes never released | Staging release added to G02 (A7, +2 h with P6); production release added to G10 (A3) |
| Review P6: no fault toggle for the drill | Staging-only toggle in G02 scope and A7 |
| Review P7: go-live acceptance needed five days of production | First-week review moved out of go-live into phase 2 G11, which has a 5-day wait. **Weakened:** go-live no longer proves a clean first week; G11/A1 does |
| Review P8, P9: website token audience and same-origin route | Assumed our own website (design Q16): +1 h in G05 and +1 h in G06, no outside wait. If wrong, these become waits |
| Review P10: W1 had no owner or inputs | W1 now has Dev B and 1–2 h for the privacy line and one-page description. Sign-off evidence assumed in design Q10; the demo-first risk is a what-if |
| Review P11: front-desk session | New wait W2 (0–1 day), blocks G10 |
| Review P12: GCP project access | New wait W3 (0–1 day), blocks G07 and G08 |
| Review P13: kill switch with confirm before a confirm service exists | G05/A4 uses the mock; G09/A3 rechecks it with the real service |
| Review claim: cut-move row description | Row now states the exact hours removed; rerun gives 9.13–13.8 |
| Review claim: "G01 and G02 can swap" | Sentence removed (helper: worse) |
| Review claim: "more focused time in week 2" not modelled | Removed. The what-ifs only add hours from day 1 |
| Review claim: "every other goal except G05 waits on G01" | Corrected in "Resume here" |
| Review claim: remedies only fit the draft | All what-ifs rerun on this version |
| Grid: Cloud SQL untrusted content n/a | Now cites G03/A5 and G07/A1: stored history is replayed into the prompt |
| Grid: Cloud SQL credential n/a | D6 specifies IAM DB auth; new G08/A7 tests a removed grant |
| Grid: Vertex duplicate cited G03/A3 | New G05/A10, concurrent turns on one session |
| Grid: Cloud SQL rejects cited G04/A3 | New G04/A11, lock timeout and constraint error at confirm |
| Grid: Move over-broad | G03/A3 extended with an ambiguous move that asks which appointment |
| Grid: Book over-broad cited G03/A2 | Now cites G03/A7 (unknown salon, slot not offered) |
| Grid: JWKS key rotation; 401/429 on a write | G05/A7 and G04/A4 extended; the grid cites them |

## Resume here

- **Next goal:** G01 Booking API contract, port and fake. It has no
  prerequisites. G02, G03, G04, G07, G09 and G10 wait on it, directly or
  through others. G05 (Dev C) can start in parallel.
- **Read first:** the design, this plan, the G01 ticket, the booking API's code.
- **Next action:** list the booking API endpoints that the six tools and the
  confirm path need, and answer Q6 from the code.
- **Continuation prompt:**

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G01-booking-api-contract.md.
Read docs/architecture/salon-booking-assistant.md and preserve its accepted decisions.
Use safe-api-tool-calls with adk-tool-interface-design.
Work locally only, verify G01's acceptance cases, and record evidence in the ticket.
```

After that goal: `/adk-engineer Continue the next ready goal in docs/plans/salon-booking-assistant.md.`
Dev C starts G05 in parallel with that ticket's run prompt.
