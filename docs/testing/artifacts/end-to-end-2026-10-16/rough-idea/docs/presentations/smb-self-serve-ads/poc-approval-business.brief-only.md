---
stage: poc-approval
audience: business
minutes: 15
title: Guided product choice for small advertisers: a four-week proof of concept
sources: docs/discovery/smb-self-serve-ads.md
decision: Approve a four-week, one-developer proof of concept of a guided product recommendation in the self-serve flow, on live traffic from week two
decider: Director of SMB Sales (chairing leadership)
date: 2026-10-29
---

## Guided product choice for small advertisers: a four-week proof of concept
Covers: title
Notes: Deck drafted from the discovery brief alone; cost and scope detail are pending the design and are marked so.

---

## We ask for one developer for four weeks to test whether a guided product choice lifts completion above 62%
Covers: summary
Evidence: docs/discovery/smb-self-serve-ads.md §1, §2, §4; measured baseline, hypothesis labelled

- We measured: 2,140 purchase starts in Q3 2026; 62% get past product choice (funnel export)
- We hypothesise: a guided recommendation raises that share without raising refunds (3% of orders)
- Decision today: run the proof of concept, or not; summary first, discussion after

Notes: I am asking for four weeks and one developer to test whether a guided product choice lifts completion of that step above 62 percent, the Q3 figure from our own funnel export. Interrupt me whenever you want to go to the decision. The summary comes first and the discussion after.

---

## Today product choice loses 38% of 2,140 purchase starts, more than every other step combined
Covers: problem
Evidence: docs/discovery/smb-self-serve-ads.md §2 funnel table; measured, funnel export Q3 2026

- Product choice: 38% leave (about 813 of 2,140; our arithmetic from the export's percentage)
- Creative upload 12%, pricing 9%, booking 6%
- Source: funnel export, Q3 2026, read by the platform product owner

Notes: Here is the funnel for last quarter, measured by the self-serve platform's own export. Of 2,140 advertisers who started a purchase, 38 percent left at product choice; creative upload, pricing and booking lose 12, 9 and 6 percent. The 813 is our arithmetic from the percentage, not a count from the export. Pause there: product choice is where the money leaves.

---

## The complication: about 40 products across formats and regions, and no way to tell which one fits
Covers: problem
Evidence: docs/discovery/smb-self-serve-ads.md §1, §2; typical case assumed, escalations reported by the user

- A bakery owner sees about 40 products, cannot tell which fits a local promotion, opens a sales chat or leaves (assumed typical case)
- Six sales staff take about 35 escalations a week (reported, Q3 2026)
- The product owner agrees product choice is the pain

Notes: Picture the bakery owner we used as the running case; she is a constructed example, labelled as such in the brief. She signs up, sees about forty products across formats and regions, and cannot tell which one fits a weekend promotion in her part of town. She opens a chat with sales, who take about 35 such escalations a week, or she leaves. The product owner who runs the platform agrees this is the step that hurts.

---

## We will test one hypothesis: less effort to choose lifts completion, and refunds stay flat
Covers: hypothesis
Evidence: hypothesis; docs/discovery/smb-self-serve-ads.md §4 hypothesis chain

- We hypothesise: the advertiser types the promotion in a sentence, sees one to three fitting products with a reason, and picks one
- Expected: more starts reach creative upload (from 62%); bookings and self-serve revenue follow
- Every arrow is a hypothesis until the proof of concept measures it

Notes: Say the word hypothesis out loud. We hypothesise that if the advertiser can describe the promotion in her own words and see one to three fitting products with a reason for each, more of them reach creative upload than the 62 percent today, and bookings follow. Nothing on this slide is measured yet; that is what the four weeks are for.

---

## Success means product-choice completion above 62% in the window, with refunds no higher than 4%
Covers: success-criteria
Evidence: docs/discovery/smb-self-serve-ads.md §4 outcome measure, baseline, counter-metric, threshold sentences

- Measure: share of purchase starts reaching creative upload, from the funnel export, read by the product owner
- Baseline: 62% of 2,140 starts, Q3 2026 (measured)
- Counter-metric: refund rate, 3% of orders today (reported)
- Sample and region: pending the design (not yet decided)

Notes: Success has one number and one guardrail. The number is the share of purchase starts that reach creative upload, read from the same funnel export that gave us the 62 percent baseline, by the same product owner. The guardrail is the refund rate, three percent of orders today. How many starts the pilot covers, and in which region, is a design decision we have not taken yet, so the margin on the result is not yet known.

---

## We stop early if completion does not move or refunds pass 4%; leadership reviews two weeks after the pilot ends
Covers: success-criteria
Evidence: docs/discovery/smb-self-serve-ads.md §4 threshold sentences, §6 decision calendar

- Stop rule 1: completion does not rise above 62% in the window; no production proposal
- Stop rule 2: refunds above 4% of orders; recommendation switched off, cases reviewed
- Production decision review: two weeks after the four weeks end; results review after one quarter in production

Notes: Two stop rules, agreed now so nobody argues about them later. If completion does not rise above 62 percent in the window, we do not propose production. If refunds rise above four percent, we switch the recommendation off and review the cases. The production decision comes to this room two weeks after the pilot ends, and a results review follows a quarter in production.

---

## Scope: a guided product recommendation only; no creative, no pricing change, no automatic booking; a person confirms every purchase
Covers: scope
Evidence: docs/discovery/smb-self-serve-ads.md §4 first use case, permission scope, embedding; detail pending the design

- In: advertiser describes the promotion; code filters the catalogue by region and format; the model ranks one to three with reasons; the advertiser picks
- Out: creative generation, pricing changes, automatic booking, any write to any system
- Kept: a person confirms 100% of purchases, as today; live traffic from week two for one region or a share of starts (pending)

Notes: The scope is deliberately small. In: the advertiser types what she wants, our code narrows the catalogue by region and format, the model ranks one to three products with a reason tied to a catalogue field, and she picks. Out: anything to do with creative, pricing, or booking on her behalf; it reads and never writes. A person confirms every purchase exactly as today, and from week two the pilot runs on live traffic in a slice the design will fix.

---

## The proof of concept costs one developer for four weeks; model and cloud cost is not yet estimated
Covers: cost
Evidence: docs/discovery/smb-self-serve-ads.md §4 unit economics, §5 constraints; hours confirmed, money pending the design

- People: one developer, four weeks (confirmed); hours per week not yet set
- Model and cloud: not yet estimated; the design states cost per start and per month
- We estimate volume at about 700 model calls a month, from 2,140 starts a quarter at one call per start
- Ceiling agreed: less than one sales hire; hosting by the platform team (confirmed)

Notes: The cost we can state is one developer for four weeks. The model and cloud bill is not yet estimated; the design will state it per start and per month, and the volume behind it is about 700 calls a month, which is 2,140 starts a quarter divided by three at one call per start. The agreed ceiling is less than one sales hire, and the platform team hosts whatever is built. Who pays the model bill after the pilot is still open and sits with the sponsor.

---

## Three risks, each with a control and an owner
Covers: risks
Evidence: docs/discovery/smb-self-serve-ads.md §4 permission scope and harms, correction loop; §8 open questions

- A product that cannot run in the advertiser's region: code filters by region before the model sees the list; owner: the developer, checked by the platform team
- A wrong price or availability: prices come from the pricing and inventory services, never the model; owner: platform team
- Refunds rise: 4% switch-off rule, weekly review of flagged cases; owner: platform product owner

Notes: Three risks, and what stops each. First, a product that cannot run where the advertiser is: our code filters the catalogue by region before the model sees anything, and the acceptance set allows zero out-of-region recommendations. Second, a wrong price or availability: those never come from the model, only from the existing services. Third, refunds rising: the four percent rule switches it off, and the product owner reviews flagged cases weekly with sales. One thing that did not hold up in discovery: catalogue read access this month is assumed, not confirmed; the platform team confirms it before the 29th, or the pilot waits.

---

## Decision: do nothing, run the four-week proof of concept, or run a wider pilot; we recommend the proof of concept
Covers: ask
Evidence: docs/discovery/smb-self-serve-ads.md §5, §6 decision calendar; options are the presenter's framing

- A. Run the proof of concept: one developer, four weeks, live traffic from week two, measured report at the end (recommended)
- B. Wider pilot across all starts and regions: more signal, but no hosting sign-off yet and no cost estimate
- C. Do nothing: product choice keeps losing 38%; sales keeps about 35 escalations a week
- Decider: Director of SMB Sales, chairing leadership, 29 October 2026; if nothing is decided, the developer is not booked and the window slips

Notes: Three options. Do nothing, and product choice keeps losing 38 percent of starts. Run a wider pilot across all traffic, which gives more signal but has no hosting sign-off and no cost estimate behind it yet. Or run the four-week proof of concept with one developer, live from week two, ending in a measured report against the 62 percent, not only a demo; that is our recommendation. The decision is yours, today, and if nothing is decided the developer is not booked and the window slips.

---

## Questions we expect, with the record's answer
Covers: questions
Evidence: docs/discovery/smb-self-serve-ads.md §4, §5, §8; "not measured" where the record is silent

- Baseline, who, when: 62% of 2,140 starts, funnel export Q3 2026, product owner
- Cost per month at full adoption: not estimated; the design's cost section will state it
- Model price or behaviour changes: the filters are code and acceptance is on completion rate, so a model swap is re-run against the same cases
- Accountable for a wrong answer: the confirming person at booking, as today; the product owner owns the review loop
- Who signed off: the product owner agrees on the problem; the Director of SMB Sales sponsors; the platform team hosts (hosting sign-off at the production review)
- How people's work changes: sales staff review flagged recommendations, about an hour a week (assumed); one training session (assumed)

Notes: Appendix; not spoken unless asked.

---

## Why this use case and not the others in the portfolio
Covers: appendix
Evidence: docs/discovery/smb-self-serve-ads.md §3 portfolio and helper ranking

- O1 product choice: score 11; largest drop, data at hand, reversible
- O3 explain the price: score 8; cheap but small (9% drop)
- O4 draft escalation replies: score 5; helps staff, not the KPI
- O2 creative wait: score 4; no baseline and rights data of uncertain quality; waits for one quarter of measurement

Notes: Appendix; the ranking helper's output is pasted in the brief.
