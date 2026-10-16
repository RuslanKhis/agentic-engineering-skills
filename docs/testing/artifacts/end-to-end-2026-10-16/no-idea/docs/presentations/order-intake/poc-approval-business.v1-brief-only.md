---
stage: poc-approval
audience: business
minutes: 15
title: Order intake: a four-week proof of concept
sources: docs/discovery/order-intake.md (design and plan do not exist yet; cost and scope marked pending design)
decision: Approve a four-week proof of concept with one contractor on emailed order intake for one dispatcher queue
decider: Owner-CEO
date: 2026-11-05
---

## Order intake: a four-week proof of concept
Covers: title
Evidence: n/a: title slide
Notes: I am asking for four weeks and one contractor to test whether a reading assistant cuts the dispatcher time on an emailed order from about four minutes to under two. The summary comes first and discussion after; interrupt me whenever you want to go to the decision.

---

## Re-keying orders costs an estimated 60 dispatcher hours a week; a four-week test asks whether that falls by three quarters
Covers: summary
Evidence: docs/discovery/order-intake.md §1, §2, §4; we estimate (900 orders x 4 minutes, both reported by the operations director, 15 Oct 2026, untimed)

- Today: four dispatchers re-type about 900 orders a week into the TMS, about 4 minutes each (estimate)
- Complication: nothing in intake is measured, and the email share is uncounted
- Question: fund a four-week proof of concept now, or wait
- Answer: run it on one dispatcher's queue, with a person approving every order

Notes: Situation, complication, question, answer, in that order. The sixty hours is arithmetic on two estimates from the operations director, not a measurement; the first two weeks of the proof of concept time the real figure. Everything that follows backs this one page.

---

## Today each emailed order costs about 4 dispatcher minutes of re-typing, an estimate nobody has timed
Covers: problem
Evidence: docs/discovery/order-intake.md §2 journey table; reported estimate, operations director, 15 Oct 2026

- Customer emails "3 pallets Smithfield to Albury, pick up Thursday" to the shared mailbox
- A dispatcher reads it, phones for gaps, re-keys customer, addresses, pallets, dates, instructions
- About 900 orders a week by email and phone; about 4 minutes each (estimate from watching)

Notes: Here is one real order from last Tuesday: three pallets, Smithfield to Albury. The dispatcher reads the email, rings the customer if the pickup time is missing, and types five groups of fields into the TMS. The four minutes is what the operations director saw when she watched; nobody has used a stopwatch, so I will call it an estimate every time I say it.

---

## The dispatcher who already uses AI says re-keying is the real pain, and nothing in intake is measured
Covers: problem
Evidence: docs/discovery/order-intake.md §1, §2; reported, operations director, 15 Oct 2026

- One dispatcher already pastes customer emails into a consumer chatbot to draft replies
- Her view: the replies were never the problem; the re-typing is
- Correction counts, wrong deliveries and intake time are not logged today

Notes: The complication is twofold. The person closest to the work has already reached for AI on her own, which tells us where the friction is and who will carry the change. And we cannot say today how many orders are corrected at dispatch review or delivered to the wrong place, so any promise of improvement starts by counting.

---

## We will test one hypothesis: less re-keying frees dispatcher hours without more wrong orders
Covers: hypothesis
Evidence: hypothesis; docs/discovery/order-intake.md §4 hypothesis chain

- Less effort to re-key an emailed order
- Fewer dispatcher hours on intake (we hypothesise about 60 a week to about 15)
- Hours go to phone orders and disputes, with corrected orders, wrong deliveries and complaints flat

Notes: Say the word hypothesis out loud: every arrow on this slide is untested. The assistant reads the email and proposes the fields; the dispatcher checks the draft against the email and approves it in one click; ordinary software creates the TMS order. We hypothesise the time falls to about a quarter; the proof of concept measures it.

---

## Success means under 2 minutes per emailed order, with corrected orders no worse than a two-week baseline
Covers: success-criteria
Evidence: docs/discovery/order-intake.md §4 outcome measure, baseline, threshold sentences; targets proposed, not yet agreed

- Measure: minutes from email received to TMS order created, weekly median, read by the operations director
- Weeks one and two: time the current process and count corrections (the baseline)
- Weeks three and four: the assistant on one dispatcher's queue, live emails, real orders

Notes: The measure is the clock between the email arriving and the order existing in the TMS, which both systems already stamp. The first two weeks measure the present, because the four minutes is an estimate. The target of under two minutes is proposed today, not yet agreed; you set it.

---

## We stop early if corrected orders rise above baseline or dispatchers work around it, reviewed weekly
Covers: success-criteria
Evidence: docs/discovery/order-intake.md §4 threshold sentences, counter-metric; operations director's stop conditions, 15 Oct 2026

- Same-day pause: orders corrected at dispatch review on the pilot queue rise above the measured baseline
- Stop: dispatchers bypass the approval screen, or complaints rise
- Reviewed weekly by the operations director with the champion dispatcher

Notes: The operations director named the two things that would make her cancel: more wrong orders, or dispatchers working around it. Both are on this slide as stop rules with a weekly review, so the test cannot drift. Wrong-place deliveries are counted from week one for the same reason.

---

## Scope: emailed orders on one dispatcher's queue, a person approves every order; not phone orders, scheduling or disputes
Covers: scope
Evidence: docs/discovery/order-intake.md §4 chosen, embedding, permission scope; detailed scope pending design

- In: read the orders mailbox, draft the TMS fields, one-click approval, create the order
- Out: phone orders, driver scheduling, proof-of-delivery disputes, any reply to a customer
- Pending design: exact field set and the approval screen

Notes: One queue, one mailbox, one kind of order, and a dispatcher reads every draft before an order exists. The assistant never emails a customer and never touches scheduling or disputes; those stay in the portfolio with their triggers. The design, which does not exist yet, fixes the exact fields and the screen.

---

## The proof of concept costs four weeks of one contractor; model and cloud cost is pending design
Covers: cost
Evidence: docs/discovery/order-intake.md §5 scope-gate table (four weeks, one contractor: confirmed); model and cloud: not yet estimated, the design estimates it

- People: one contractor for four weeks (confirmed as plausible by the operations director)
- Model and cloud: pending design; expected to scale with about 900 orders a week
- Hosting afterwards: the external IT firm; who pays the monthly bill: to confirm

Notes: The only cost I can state today is the contractor's four weeks, which the operations director has confirmed is plausible; I will not put a model figure on a slide until the design has estimated it per order and per month. What I can say is the volume it scales with, about 900 orders a week, and that the IT firm hosts it afterwards.

---

## Three risks, each with a control and an owner
Covers: risks
Evidence: docs/discovery/order-intake.md §4 permission scope and harms, §8 open questions

- Wrong field approved unread: dispatch review stays as the second check; stop rule on corrections; owner: operations director
- Missed email: daily count of emails against drafts; owner: champion dispatcher
- TMS access or customer data terms block the pilot: IT firm answers before the start; owner: operations director

Notes: What could go wrong, and the answer. A tired dispatcher approves a wrong address: the planner's dispatch review stays in place and the correction rule stops the pilot the same day. An email is missed: a daily count catches it. And the one that could stop us before we start: the IT firm must confirm TMS write access and the data terms, which we ask this week.

---

## Decision: do nothing, run the four-week proof of concept, or go wider; we recommend the proof of concept
Covers: ask
Evidence: docs/discovery/order-intake.md §6 decision calendar; §4 chosen

- A. Do nothing: the 60 estimated hours a week continue, unmeasured
- B. Four-week proof of concept, one contractor, one queue (recommended): a measured report, not just a demo
- C. Wider pilot on all four dispatchers now: faster, but no baseline and no stop rule proven
- Decider: owner-CEO, by 5 November 2026; if nothing is decided, intake stays as it is

Notes: Three options. Do nothing and the hours continue uncounted. Run the four-week test on one queue and you get a measured number against a measured baseline, with the stop rules proven. Go wider now and you risk the wrong-order rate before anyone has counted it. We recommend B; the decision is yours by the fifth of November.

---

## Questions we expect, with the answers the record holds
Covers: questions
Evidence: docs/discovery/order-intake.md §4, §5, §8; "not measured" where the record is silent

- Baseline, who measured, when: an estimate from watching; not measured; weeks one and two measure it
- Cost per month at full adoption: not estimated; the design will
- Who is accountable for a wrong order: the approving dispatcher, as today; the operations director owns the pilot
- What if the model's price or behaviour changes: the TMS write is ordinary software; acceptance is minutes per order, re-run on any swap
- Why not larger: no baseline yet; why not smaller: one queue is the smallest live test

Notes: Each answer in one sentence, then the evidence, then back to the recommendation. Where the record is silent the answer is "not measured" and the goal that measures it.

---

## What we considered instead, and why not
Covers: appendix
Evidence: docs/discovery/order-intake.md §3 portfolio, §8 assumptions

- A customer order form for the five largest customers: a process change the operations director owns, run in parallel, does not cover phone orders or the long tail
- The TMS vendor's own email intake, if it exists: asked through the IT firm before anything is built
- An agent that works through the steps itself: rejected, the steps never vary
- Disputes, scheduling, invoice queries, complaint causes: ranked lower; in the portfolio with triggers

Notes: These are the honest alternatives. If the TMS vendor already sells email intake, we buy it and this proof of concept is not needed; that question goes to the IT firm this week.
