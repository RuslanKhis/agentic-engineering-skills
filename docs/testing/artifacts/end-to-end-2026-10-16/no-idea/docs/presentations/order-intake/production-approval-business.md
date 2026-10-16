---
stage: production-approval
audience: business
minutes: 15
title: Order intake: the pilot result and the production decision
sources: docs/plans/order-intake.md (phase-1 evidence, invented, labelled), docs/architecture/order-intake.md, docs/discovery/order-intake.md
decision: Build order intake for all four dispatchers' emailed orders, a dispatcher approving every order, at about USD 230 a month (plan G08)
decider: Owner-CEO
date: 2026-12-10
---

## Order intake: the pilot result and the production decision
Covers: title
Evidence: n/a: title slide
Notes: I am asking you to approve order intake for all four dispatchers, because on Maria's queue an emailed order went from 4.4 minutes to 1.7 on 331 orders with no rise in corrected orders. Summary first, discussion after; interrupt me whenever you want to go to the decision.

---

## Three of three criteria met, 1.7 minutes against 4.4, corrections flat; we recommend production
Covers: summary
Evidence: docs/plans/order-intake.md G02, G06 (measured); cost: we estimate from G06 spend, see cost slide

- We measured: 1.7 minutes per emailed order against a 4.4-minute baseline, 331 orders, two weeks
- We measured: corrected orders 3.0% against 2.8%, within the margin; wrong deliveries 1 and 1
- We estimate: about USD 230 a month at four queues; the pilot cost USD 34.50
- Ask: build for all four dispatchers, decided today

Notes: Situation, complication, question, answer on one page. The two-week baseline we promised you in November was measured, and the live weeks beat it on the same clock and the same queue. The rest of the deck is the method behind each of these numbers.

---

## Criteria agreed on 5 November, and what we measured against each
Covers: criteria-results
Evidence: docs/plans/order-intake.md G02 (baseline), G06/A1 (weekly report), G06/A3; thresholds from docs/discovery/order-intake.md §4 and the 5 Nov decision memo

| Criterion | Threshold | Measured | Method, sample |
| --- | --- | --- | --- |
| Minutes per emailed order | under 2 | 1.7 (week 4: 1.4) | mailbox to TMS timestamps, 331 orders |
| Corrected at dispatch review | no worse than baseline | 3.0% vs 2.8% | planner's review flags, 331 vs 318 |
| Wrong-place deliveries | no worse | 1 vs 1 | TMS redelivery records |

Notes: Three criteria, all from the memo you approved in November. Each number comes from the same two systems, the mailbox and the TMS, read by the contractor's weekly export and checked by me. The third row is one event in each period, so it says nothing either way; the second row is the one that matters and it did not move.

---

## Minutes per emailed order fell from 4.4 to 1.7 on Maria's queue, week by week, with corrections flat
Covers: criteria-results
Evidence: docs/plans/order-intake.md G02 (weeks 1 and 2), G06 (weeks 3 and 4); measured

- Column chart, weekly median: 4.6, 4.2 (shadow) then 2.1, 1.4 (live); baseline line at 4.4; n per week 151, 167, 160, 171
- Beside it: corrected orders 9 of 318 then 10 of 331

Notes: Two weeks of watching with nothing changed, then two weeks live. Week three was the training week and still came in at 2.1; week four, 1.4. One real order: on 2 December a Smithfield email arrived at 9:14, Maria approved the draft at 9:15 and the TMS order existed at 9:16 (invented example from the live weeks); before, she would have typed five groups of fields.

---

## What did not work: 14% of drafts edited, 3.6% unreadable, one safety case never run
Covers: learned
Evidence: docs/plans/order-intake.md G06 (edits, enter-manually), G04/A1 (fields), G05/A4 NOT RUN; measured

- 47 of 331 drafts edited before approval: dates 19, instructions 15, addresses 9, other 4
- 12 of 331 came back "enter manually"; 3 of the 50 test emails lacked a delivery address
- G05/A4, a lost TMS reply after approval, was not run: no test environment

Notes: Three things did not work, each with its answer. The edits cluster on dates and free-text instructions, so those two fields get the prompt work and the evaluation cases in production. The one untested case is what happens when the TMS does not answer after approval; the code for it exists, and the IT firm will set up a test environment before all four queues go live.

---

## Four lessons change the production plan: the clock, the weak fields, the IT firm's lead time and the hours
Covers: learned
Evidence: docs/plans/order-intake.md G02 (measure note), G03 (12-day wait), G05 (hours), capacity line; measured

- The measure is elapsed time on the queue; the old 4-minute figure was handling time; we keep the measured clock
- Dates and instructions are the weak fields; every edit is now a test case
- The IT firm's access took 12 days, not 7; production asks for it first
- The pilot took 71 contractor hours against 46 to 62 estimated

Notes: What we learned, first. The baseline we asked you to accept as an estimate turned out to be 4.4 on a stopwatch nobody can argue with. Second, the overrun in hours sits in one place, the approval page, and that page is built; the production estimate counts only what remains.

---

## Production scope: all four dispatchers' emailed orders, a dispatcher approving every order, and a missed-mail alert
Covers: production-scope
Evidence: docs/plans/order-intake.md G08; docs/architecture/order-intake.md §4 graduation conditions, C2; sponsor from docs/discovery/order-intake.md §6

- In: the three other queues, one hour of training each, the alert when mail stops, pinned model and prompt version
- Out: phone orders, scheduling, disputes, customer replies, any order without approval
- Workflow change: dispatchers check a draft instead of typing; the planner's review stays
- Sponsor: the operations director; Maria trains the other three

Notes: The workflow change is the one Maria already lives with: read the draft against the email, fix or approve, still phone for gaps. Nothing else in the office changes, and the planner's weekly review stays as the second check. That is the scope I am asking for, no wider.

---

## Production: about USD 230 a month and 16 to 24 build hours; the pilot cost USD 34.50
Covers: cost
Evidence: docs/plans/order-intake.md G06 spend (measured, billing export 7 Dec); G08 hours (estimate); monthly figure: we estimate, arithmetic shown; assumption: the other three queues carry the pilot queue's volume

- We measured: USD 34.50 for two live weeks on one queue (model 23.40, hosting 11.10), USD 0.10 per emailed order
- We estimate: USD 0.07 model x about 2,900 emailed orders a month at four queues, plus about USD 25 hosting, about USD 230 a month
- We estimate: 16 to 24 contractor hours to build (G08); pilot actual 71 hours

Notes: The pilot's bill is thirty-four dollars and fifty cents, from the billing export, not a model. The monthly figure is arithmetic on that, times four queues, and assumes Maria's queue is typical; the first production month replaces the estimate with the bill. People cost is the only large number: 16 to 24 contractor hours for the build, then the IT firm's hosting under their existing contract.

---

## Three risks, each with a control and an owner
Covers: risks
Evidence: docs/architecture/order-intake.md C2, C3, C5; docs/plans/order-intake.md G05/A4 NOT RUN, G03 O4 open, G06/A2

- A wrong draft approved without reading: dispatcher approval on 100% of orders, planner review second; owner the operations director (C2)
- A lost TMS reply makes two orders: one order per approval by design (C3); the untested case is run before four queues; owner the IT firm
- Customer data terms: 20 largest customers checked, the rest not; owner the operations director (O4)

Notes: Three risks spoken as confidence: what the system cannot do, who approves what, and the test that proves it. The second one is the untested case from the previous slide, and it is the IT firm's first production task. The third is a contract question, not a technical one, and it is mine.

---

## Build in January: three weeks of work, four queues live by 25 January, results review after 90 days
Covers: production-scope, timeline
Evidence: docs/plans/order-intake.md G08, G09; dates proposed (not yet agreed)

- Week of 11 January: IT firm access and the TMS test environment; the untested case run
- 18 to 22 January: alert, pinned versions, training; 25 January: four queues live
- Weekly corrected-orders count to you, as in the pilot; results review late April

Notes: Dates are proposed today and agreed in the memo. The IT firm's lead time is the first item because it was the slow one in the pilot. You keep getting the weekly count you asked for in November.

---

## Decision: stop, extend the pilot to a second queue, or build for all four; we recommend build; owner-CEO, 10 December
Covers: ask
Evidence: docs/plans/order-intake.md G07, G08; options and costs from the cost slide and G06

- A. Build for all four dispatchers (recommended): 16 to 24 hours, about USD 230 a month; the one untested case run first
- B. Extend the pilot to a second queue for four weeks: about 8 hours, the result arrives in February
- C. Stop: Maria's queue returns to typing; the code and 50 test cases are kept

Notes: Three options. We recommend A because the number held for two weeks on the same clock as the baseline and the counter-metric did not move. If nothing is decided today, Maria's queue keeps running on the pilot build and the January slots with the IT firm are lost. Credit: the contractor built it, Maria ran it, the IT firm gave access.

---

## Appendix: the questions we expect, answered from the record
Covers: questions, appendix
Evidence: docs/plans/order-intake.md G02, G03, G06; docs/architecture/order-intake.md D4, D6; docs/discovery/order-intake.md §4

- Baseline, who, when: 4.4 minutes, 318 emailed orders, 9 to 22 Nov, from the timestamps; the email share of the queue was 71%
- Model price or behaviour changes: model pinned (D4); the 50 cases and the 47 corrections are rerun on any change; a quota stops spend (D6)
- Accountable for a wrong order: the dispatcher who approved it and the operations director; no order is created without approval
- Stop rule in production: corrected orders above 2.8% on any queue pauses that queue the same day
- Hours freed: we estimate 2.7 minutes x 331 orders, about 15 hours over two weeks on one queue; not yet reassigned, my decision
- Not measured: complaints by queue (counted firm-wide only); cost at four queues (first production bill)

Notes: Held for questions, not spoken. Answer protocol: restate, one sentence, the evidence with its sample, bridge to option A.
