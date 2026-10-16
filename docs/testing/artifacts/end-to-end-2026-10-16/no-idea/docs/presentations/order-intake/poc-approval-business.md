---
stage: poc-approval
audience: business
minutes: 15
title: Order intake: a four-week proof of concept
sources: docs/discovery/order-intake.md, docs/architecture/order-intake.md, docs/plans/order-intake.md
decision: Approve a four-week proof of concept with one contractor on emailed order intake for one dispatcher queue (plan G01)
decider: Owner-CEO
date: 2026-11-05
---

## Order intake: a four-week proof of concept
Covers: title
Evidence: n/a: title slide
Notes: I am asking for four weeks and one contractor to test whether a reading assistant cuts the dispatcher time on an emailed order from about four minutes to under two, with a dispatcher approving every order. Summary first, discussion after; interrupt me whenever you want to go to the decision.

---

## Re-keying orders costs an estimated 60 dispatcher hours a week; a four-week test asks whether that falls by three quarters
Covers: summary
Evidence: docs/discovery/order-intake.md §1, §2, §4; we estimate (900 orders x 4 minutes, both reported by the operations director, 15 Oct 2026, untimed); docs/plans/order-intake.md phase 1

- Today: four dispatchers re-type about 900 orders a week into the TMS, about 4 minutes each (estimate)
- Complication: nothing in intake is measured; the email share is uncounted
- Question: fund the four-week test now, or wait
- Answer: two weeks measuring, two weeks live on one queue, a person approving every order

Notes: Situation, complication, question, answer. The sixty hours is arithmetic on two of the operations director's estimates, not a measurement; the first two weeks of the plan time the real figure before anything changes. The rest of the deck backs this page.

---

## Today each emailed order costs about 4 dispatcher minutes of re-typing, an estimate nobody has timed
Covers: problem
Evidence: docs/discovery/order-intake.md §2 journey table; reported estimate, operations director, 15 Oct 2026

- "3 pallets Smithfield to Albury, pick up Thursday" arrives in the shared mailbox
- A dispatcher reads it, phones for gaps, re-keys customer, addresses, pallets, dates, instructions
- About 900 orders a week by email and phone; about 4 minutes each (estimate from watching)

Notes: One real order from last Tuesday. The dispatcher reads the email, rings the customer if the pickup time is missing, and types five groups of fields into the TMS. The four minutes is what the operations director saw when she watched; nobody has used a stopwatch, so I call it an estimate every time.

---

## The dispatcher who already uses AI says re-keying is the real pain, and nothing in intake is measured
Covers: problem
Evidence: docs/discovery/order-intake.md §1, §2; reported, operations director, 15 Oct 2026

- One dispatcher already pastes customer emails into a consumer chatbot to draft replies
- Her view: the replies were never the problem; the re-typing is
- Correction counts, wrong deliveries and intake time are not logged today

Notes: Two complications. The person closest to the work has already reached for AI on her own, which tells us where the friction is and who will carry the change. And nobody can say today how many orders are corrected at review or delivered to the wrong place, so any promise of improvement starts by counting.

---

## We will test one hypothesis: less re-keying frees dispatcher hours without more wrong orders
Covers: hypothesis
Evidence: hypothesis; docs/discovery/order-intake.md §4 hypothesis chain; docs/architecture/order-intake.md §2 (D1)

- Less effort to re-key an emailed order
- Fewer dispatcher hours on intake (we hypothesise about 60 a week to about 15)
- Hours go to phone orders and disputes, with corrected orders, wrong deliveries and complaints flat

Notes: Say the word hypothesis out loud: every arrow here is untested. In the design, one model call reads the email and returns the fields in a fixed form or says it cannot; the dispatcher checks the draft beside the email and approves in one click; ordinary software creates the TMS order. We hypothesise the time falls to about a quarter; the test measures it.

---

## Success means under 2 minutes per emailed order, with corrected orders no worse than a two-week baseline
Covers: success-criteria
Evidence: docs/plans/order-intake.md G02/A2, G06/A1; docs/architecture/order-intake.md C1; target proposed, not yet agreed

- Measure: minutes from email received to TMS order created, weekly median, read from the system's own record
- Weeks one and two: the same clock runs silently on today's process and counts corrections (the baseline)
- Weeks three and four: live on the champion dispatcher's queue, real emails, real orders

Notes: The measure is the clock between the email arriving and the order existing in the TMS, which the design records for every order from day one. For the first two weeks it runs silently on the present process, because the four minutes is an estimate. Under two minutes is proposed today, not agreed; you set it.

---

## We stop early if corrected orders rise above baseline or dispatchers work around it, reviewed weekly
Covers: success-criteria
Evidence: docs/discovery/order-intake.md §4 threshold sentences; docs/plans/order-intake.md G06; operations director's stop conditions, 15 Oct 2026

- Same-day pause: orders corrected at dispatch review on the pilot queue rise above the measured baseline
- Stop: dispatchers bypass the approval screen, or complaints rise
- Weekly review by the operations director with the champion dispatcher; every edit kept as a test case

Notes: The operations director named the two things that would make her cancel: more wrong orders, or dispatchers working around it. Both are stop rules with a weekly review in the plan, so the test cannot drift. Wrong-place deliveries are counted from week one for the same reason.

---

## Scope: emailed orders on one queue; the assistant drafts, a dispatcher approves, software writes; nothing else
Covers: scope
Evidence: docs/architecture/order-intake.md §1, §2, D1, D2; docs/plans/order-intake.md phase 1 and later list

- In: read the orders mailbox, draft the fields, one-click approval, create the TMS order
- Out: phone orders, driver scheduling, proof-of-delivery disputes, any reply to a customer
- The part that reads emails cannot write to the TMS; only the approval step can

Notes: One queue, one mailbox, one kind of order. The design splits reading from writing: the piece that reads customer emails has no access to the TMS at all, and the only path to a new order runs through the dispatcher's click. Scheduling, disputes and phone orders stay in the portfolio with their triggers.

---

## The proof of concept costs 46 to 62 contractor hours and at most 300 dollars of model spend
Covers: cost
Evidence: docs/plans/order-intake.md capacity (46 to 62 h of about 120 h; we estimate); docs/architecture/order-intake.md D6 (USD 300 ceiling, assumption from "a few hundred dollars"); per-order model cost not yet measured

- We estimate: 46 to 62 contractor hours, within the four weeks
- Assumed ceiling: 300 dollars of model and cloud spend for the trial, enforced by a quota that stops calls
- Not yet measured: model cost per order and per month; week three measures it

Notes: Two numbers and one gap. The hours are the plan's estimate for one contractor. The three hundred dollars is a ceiling we chose from your "a few hundred", and a quota stops the calls when it is reached, so it cannot be exceeded by accident. What we cannot give you yet is cost per order and per month; the first live week measures it, and the next review states it.

---

## Three risks, each with a control and an owner
Covers: risks
Evidence: docs/architecture/order-intake.md C2, C3, C5 and §5 failure review; docs/plans/order-intake.md G03, O1 to O4

- Wrong field approved unread: dispatch review stays as the second check; same-day pause on corrections; owner: operations director
- Order created twice or not at all: each approval is tied to the exact draft and creates at most one order; owner: contractor
- IT firm access or customer data terms block the start: asked in week one, before any build; owner: operations director

Notes: What could go wrong, and the answer. A tired dispatcher approves a wrong address: the planner's review stays in place and the correction rule pauses the pilot. A click lands twice or the TMS does not answer: the design creates at most one order per approval and shows "pending" until it is sure. And the one that could stop us before we start: the IT firm must confirm TMS access and the data terms in week one; that is the first ticket.

---

## Decision: do nothing, run the four-week proof of concept, or go wider; we recommend the proof of concept
Covers: ask
Evidence: docs/discovery/order-intake.md §6 decision calendar; docs/plans/order-intake.md G01, G07

- A. Do nothing: the estimated 60 hours a week continue, uncounted
- B. Four-week proof of concept, one contractor, one queue (recommended): a measured report at the review, not just a demo
- C. All four dispatchers now: faster, but no baseline and no stop rule proven
- Decider: owner-CEO by 5 November 2026; if nothing is decided, intake stays as it is

Notes: Three options. Do nothing and the hours continue uncounted. Run the test on one queue and you get a measured number against a measured baseline, with the stop rules proven, and a second decision at the review. Go wider now and you risk the wrong-order rate before anyone has counted it. We recommend B; the decision is yours by the fifth of November.

---

## Questions we expect, with the answers the record holds
Covers: questions
Evidence: docs/discovery/order-intake.md §4, §5, §8; docs/architecture/order-intake.md D4, D6; docs/plans/order-intake.md G02, G08

- Baseline, who measured, when: an estimate from watching; weeks one and two measure it
- Cost per month at full adoption: not yet measured; the first live week measures per order; the review states it
- Who is accountable for a wrong order: the approving dispatcher, as today; the operations director owns the pilot
- If the model's price or behaviour changes: the model is pinned; the TMS write is ordinary software; acceptance is minutes per order, re-run on any swap
- Why not larger: no baseline yet; why not smaller: one queue is the smallest live test

Notes: Each answer in one sentence, then the evidence, then back to the recommendation. Where the record is silent the answer is "not measured" and the goal that measures it.

---

## What we considered instead, and why not
Covers: appendix
Evidence: docs/discovery/order-intake.md §3 portfolio, §8 assumptions; docs/architecture/order-intake.md D1

- A customer order form for the five largest customers: a process change the operations director owns, in parallel; does not cover phone orders or the long tail
- The TMS vendor's own email intake, if it exists: asked through the IT firm in week one, before anything is built
- An agent that works through the steps itself: rejected, the steps never vary
- Disputes, scheduling, invoice queries, complaint causes: ranked lower; in the portfolio with triggers

Notes: These are the honest alternatives. If the TMS vendor already sells email intake, we buy it and this proof of concept is not needed; that question goes to the IT firm in week one.
