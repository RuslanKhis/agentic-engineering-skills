---
stage: final-results
audience: business
minutes: 15
title: Order intake after a quarter: 1.6 minutes an order on four queues
sources: docs/plans/order-intake.md (G08, G09 evidence, invented, labelled; G02 baseline), docs/architecture/order-intake.md, docs/discovery/order-intake.md
decision: Information on the quarter; one ask: approve a public case study and a four-week discovery on phone orders (plan Later list)
decider: Owner-CEO
date: 2027-05-06
---

## Order intake after a quarter: 1.6 minutes an order on four queues
Covers: title
Evidence: docs/plans/order-intake.md G09 (measured)
Notes: After thirteen weeks on all four queues, an emailed order takes 1.6 minutes of dispatcher time against the 4.4 we measured before, on 8,640 orders, at USD 221 a month against the 230 we estimated, with two incidents and no order lost. Summary first; the one decision today is at the end.

---

## Live on four queues: 1.6 minutes an order against 4.4, USD 221 a month, two incidents, nothing lost
Covers: summary, outcome
Evidence: docs/plans/order-intake.md G09 (measured, 25 Jan to 25 Apr 2027), G02 (baseline); cost estimate from the 10 Dec memo

- We measured: 1.6 minutes median over 8,640 emailed orders; corrected orders 2.9% against 2.8%
- We measured: USD 221 a month average, three bills; estimate was USD 230
- Two medium incidents, both contained by the alert and the pending state
- Next: a public case study and a look at phone orders, your decision today

Notes: Four lines and every one of them is from the record. The outcome held across a quarter and across three dispatchers who were not in the pilot. The rest shows the method behind each number.

---

## Every week of the quarter ran between 1.3 and 2.4 minutes an order, against 4.4
Covers: outcome
Evidence: docs/plans/order-intake.md G09 outcome (weekly medians, by queue), G02 baseline measured on the pilot queue only; measured

- Line chart: 13 weekly medians, 1.3 to 2.4, baseline line at 4.4; the one 2.4 is the TMS outage week
- By queue: 1.3, 1.6, 1.7, 2.1; n 8,640 emailed orders of 11,900 (73% by email)
- Caveat: the baseline was measured on one queue; the other three are assumed to have matched it

Notes: Thirteen weeks, same clock, same two systems as the pilot: mailbox received to TMS created. One honest caveat: we only ever measured the before on Maria's queue, so for the other three the 4.4 is an assumption, and queue four at 2.1 may have started from a different place. The counterfactual is the shadow fortnight in November, when nothing was changed and the figure was 4.4.

---

## All four dispatchers used it every week; 94% of emailed orders went through the approval screen
Covers: adoption
Evidence: docs/plans/order-intake.md G09 adoption; measured; active defined as at least one approved draft in the week

- Active: 4 of 4 dispatchers, all 13 weeks
- 8,120 of 8,640 emailed orders approved on the screen; 3.1% unreadable, 2.9% typed by choice
- Bypass on queue 4 fell to 0.8% in April after a second training hour; edits before approval 9% in April from 14% in the pilot

Notes: Adoption is the number that usually fails, so here is its definition: approved at least one draft in the week. The six percent that did not go through the screen splits into emails the system could not read and a dispatcher who preferred typing, and the second part was a training problem on one queue, fixed in March.

---

## Cost: USD 221 a month and USD 0.077 an order against the USD 230 estimate
Covers: cost
Evidence: docs/plans/order-intake.md G09 cost (billing exports Feb, Mar, Apr 2027; measured); estimate from docs/presentations/order-intake/decision-memo.md (10 Dec 2026)

- We measured: USD 221, 238, 203 for February, March, April; average 221
- We measured: USD 0.077 per emailed order all-in; the pilot was USD 0.10
- People: IT firm about 2 hours a month under the existing contract; contractor 6 hours in the quarter

Notes: Three bills, read from the billing export, not a model. The December estimate was arithmetic on one queue and it landed within four percent. The people cost is small because nothing was rebuilt: two prompt revisions and one incident review.

---

## Two medium incidents, each contained by the alert or the pending state; 41 orders typed by hand, none lost
Covers: incidents
Evidence: docs/plans/order-intake.md G09 incidents 1 and 2 (IT firm incident notes, measured); docs/architecture/order-intake.md C3, §5

- 10 Feb: mailbox consent expired; mail paused 3 h 40 min; paged at 60 min; 41 orders typed; fix: renewal reminder at 80 days (IT firm)
- 8 Mar: TMS unavailable 2 h 10 min; 17 approvals pending, retried, no duplicate order; fix: pending count on the page, vendor calendar

Notes: Both incidents were the two failure rows the design wrote down in October, and both behaved as written: the page said mail paused, the approvals waited, nobody created a second order. The March one was the first real test of the case we could not run in the pilot, and it passed on live orders. Each has a fix with an owner.

---

## The workflow changed as promised: dispatchers check a draft instead of typing; the planner's review stayed
Covers: outcome
Evidence: docs/discovery/order-intake.md §4 workflow before and after; docs/plans/order-intake.md G09 adoption (edits 9%), G08 (training)

- Removed: re-keying five groups of fields; kept: the phone call for gaps, the planner's review, approval on every order
- Training: one hour per dispatcher by Maria, a second hour for queue 4
- About 400 dispatcher hours over the quarter (we estimate: 2.8 minutes x 8,640), not reassigned yet

Notes: One real case: Maria's year. In November she typed every order; on 23 November she started checking drafts; by April she edits one draft in eleven, and on 8 March she watched seventeen approvals sit pending for two hours and none of them doubled. The freed hours are an estimate and are mine to reassign; that is a decision, not a result.

---

## What we would do differently: measure every queue's baseline, test the lost-reply case before going live, train twice
Covers: next
Evidence: docs/plans/order-intake.md G09 outcome caveat, G08 (G05/A4 run in January), G09 adoption (queue 4); recorded lessons

- Shadow-measure all four queues, not one: the other three baselines are assumptions
- Ask the host for a test environment at the start: the lost-reply case waited two months
- Plan two training hours, not one: the bypass on queue 4 was a training gap

Notes: Three lessons, each from a number on an earlier slide. None of them changes the result, but all three would have made it cheaper to defend.

---

## The team: one contractor, four dispatchers, the IT firm, and the operations director
Covers: team
Evidence: docs/plans/order-intake.md G08, G09 cost (people hours); docs/discovery/order-intake.md §6

- The contractor: built the pilot (71 h) and production (19 h), two prompt revisions
- Maria: ran the pilot queue and trained the other three; all four dispatchers: 8,120 approvals
- The IT firm: access, hosting, both incidents; the operations director: sponsor and weekly reviews

Notes: Credit before the ask. The contractor is named in the plan; the dispatchers did the real work of 8,120 approvals; the IT firm answered both pages.

---

## Next: keep running as is; approve a public case study and a four-week discovery on phone orders; owner-CEO today
Covers: next, ask
Evidence: docs/plans/order-intake.md Later list (phone orders trigger met: email share 73%; case study trigger: G09 result); hours: estimate

- A. Keep running, publish a case study, run discovery on phone orders (recommended): about 8 hours of my time plus 3 to 4 for the study; no build
- B. Keep running, no case study, no new work: nothing changes
- C. Build phone-order intake now without discovery: not recommended; nothing is measured on phone orders

Notes: No decision is needed to keep what runs; the only ask is whether we tell the story outside and whether we look at the 27 percent of orders that still arrive by phone. We recommend A because the trigger we wrote in October has been met and discovery costs no build. If nothing is decided today, the system keeps running and the case study waits.

---

## Appendix: the questions we expect, answered from the record
Covers: questions, appendix
Evidence: docs/plans/order-intake.md G02, G09; docs/architecture/order-intake.md D4, D6

- Baseline: 4.4 minutes, 318 orders, 9 to 22 Nov 2026, timestamps, pilot queue only
- Cost at full adoption: this is full adoption; USD 221 a month measured
- Model changes: pinned; two prompt revisions rerun on 50 cases plus 112 corrections before release
- Accountable for a wrong order: the approving dispatcher and the operations director; wrong deliveries 11 in the quarter (0.13%)
- What would make us stop: corrected orders above 2.8% on a queue pauses it; never triggered
- Not measured: complaints by queue; the other three queues' own baselines; dispatcher hours actually reassigned

Notes: Held for questions. Answer protocol: restate, one sentence, evidence with its sample, bridge to option A.
