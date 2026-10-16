---
stage: poc-approval
audience: business
minutes: 15
title: Guided product choice for small advertisers: a four-week proof of concept
sources: docs/discovery/smb-self-serve-ads.md, docs/architecture/smb-self-serve-ads.md, docs/plans/smb-self-serve-ads.md, docs/tickets/smb-self-serve-ads/G01.md
decision: Approve a four-week, one-developer proof of concept of a guided product recommendation, live on half of the self-serve starts from week two
decider: Director of SMB Sales (chairing leadership)
date: 2026-10-29
---

## Guided product choice for small advertisers: a four-week proof of concept
Covers: title
Notes: G01 in the plan; drafted from the brief, the design and the plan.

---

## We ask for one developer for four weeks to test whether a guided product choice lifts completion above 62%
Covers: summary
Evidence: docs/discovery/smb-self-serve-ads.md §2, §4; docs/plans/smb-self-serve-ads.md summary; baseline measured, lift hypothesised

- We measured: 2,140 purchase starts in Q3 2026; 62% get past product choice (funnel export)
- We hypothesise: a guided recommendation raises that share with refunds flat at 3%
- Plan: 31.5 to 57 developer hours of 72 available; live on half of starts from week two

Notes: I am asking for four weeks and one developer to test whether a guided product choice lifts completion of that step above 62 percent, the Q3 figure from our funnel export. The plan fits: the build needs between 31 and 57 of the 72 developer hours we have, and it runs on live traffic from week two. Interrupt me whenever you want to go to the decision; the summary comes first and the discussion after.

---

## Today product choice loses 38% of 2,140 purchase starts, more than every other step combined
Covers: problem
Evidence: docs/discovery/smb-self-serve-ads.md §2 funnel table; measured, funnel export Q3 2026

- Product choice: 38% leave (about 813 of 2,140; our arithmetic from the export's percentage)
- Creative upload 12%, pricing 9%, booking 6%
- Read by the platform product owner from the funnel export

Notes: Here is last quarter's funnel, measured by the platform's own export. Of 2,140 advertisers who started a purchase, 38 percent left at product choice; the later steps lose 12, 9 and 6 percent. The 813 is our arithmetic from the percentage. Product choice is where the money leaves.

---

## The complication: about 40 products across formats and regions, and no way to tell which one fits
Covers: problem
Evidence: docs/discovery/smb-self-serve-ads.md §1, §2; typical case assumed, escalations reported

- A bakery owner sees about 40 products, cannot tell which fits a local promotion, opens a sales chat or leaves (assumed typical case)
- Six sales staff take about 35 escalations a week (reported, Q3 2026)
- The product owner agrees this is the step that hurts

Notes: Picture the bakery owner, a constructed case labelled as such. She sees about forty products across formats and regions and cannot tell which fits a weekend promotion in her part of town, so she opens a chat with sales, who take about 35 such escalations a week, or she leaves. After the pilot, she types one sentence and sees one to three products that can run where she is, with a reason each; that is the hypothesis, and the next slide says so.

---

## We will test one hypothesis: less effort to choose lifts completion, and refunds stay flat
Covers: hypothesis
Evidence: hypothesis; docs/discovery/smb-self-serve-ads.md §4 hypothesis chain; docs/architecture/smb-self-serve-ads.md §2

- We hypothesise: one sentence in, one to three fitting products with reasons out, the advertiser picks
- Expected: more starts reach creative upload (from 62%); bookings follow
- The model only ranks a list our code built; price and availability come from our services

Notes: Say the word hypothesis out loud. We hypothesise that an advertiser who describes the promotion in her own words and sees one to three fitting products with a reason reaches creative upload more often than 62 percent of the time. The model ranks a list our code has already narrowed to her region; it never states a price. Nothing here is measured yet.

---

## Success means completion above 62% on about 250 treated starts, with refunds no higher than 4%
Covers: success-criteria
Evidence: docs/discovery/smb-self-serve-ads.md §4 measure and thresholds; docs/architecture/smb-self-serve-ads.md D4 (sample, estimated)

- Measure: share of starts reaching creative upload, funnel export, read per arm by the product owner
- We estimate the sample: about 500 starts in three live weeks (2,140 a quarter), half treated, margin about six points
- Counter-metric: refunds, 3% of orders today (reported)

Notes: Success has one number and one guardrail, both read from the funnel export we already have. Half of the starts get the recommendation and half do not, so we compare like with like. We estimate about 500 starts in the three live weeks, from 2,140 a quarter, which puts the margin on the result at about six points; a lift smaller than that will be reported as within the margin, not as a win.

---

## We stop early if completion does not move or refunds pass 4%; the production decision is 11 December
Covers: success-criteria, timeline
Evidence: docs/discovery/smb-self-serve-ads.md §4 threshold sentences; docs/plans/smb-self-serve-ads.md summary (dates invented from the 29 Oct decision)

- Stop rule 1: completion not above 62% in the window; no production proposal
- Stop rule 2: refunds above 4%; the recommendation is switched off without a deploy
- Build 2 to 27 Nov; live from 9 Nov; production decision review 11 Dec 2026; results review after one quarter

Notes: Two stop rules, agreed now. If completion does not rise above 62 percent, we do not propose production. If refunds pass four percent, the recommendation is switched off the same day, without a deploy. Build runs the four weeks of November, live from the ninth, and the production decision comes back to this room on the eleventh of December.

---

## Scope: a recommendation only; no creative, no pricing change, no booking; a person confirms every purchase
Covers: scope
Evidence: docs/architecture/smb-self-serve-ads.md §1, §2, §4 depth table; docs/discovery/smb-self-serve-ads.md §4

- In: one sentence in, code filters by region and format, one to three products with reasons out
- Out: creative, pricing changes, automatic booking; the service writes nothing
- Kept: a person confirms 100% of purchases, as today

Notes: The scope is small by design. In: the sentence, our filter, one to three products with a reason each. Out: anything to do with creative, pricing or booking on her behalf; the service reads and never writes. A person confirms every purchase exactly as today.

---

## The proof of concept costs 31.5 to 57 developer hours of 72; model and cloud under 500 EUR, per start not yet estimated
Covers: cost
Evidence: docs/plans/smb-self-serve-ads.md summary (hours, estimated); docs/architecture/smb-self-serve-ads.md §1 (allowance, user said); G04 measures the cost of 30 cases

- We estimate: 31.5 to 57 developer hours for the build; 13.5 to 27 hours of presentations by the AI engineer
- Model and cloud: allowance under 500 EUR, capped by a quota; cost per start and per month not yet estimated; G04 records it on 30 cases
- Volume: about 700 starts a month, so about 350 treated (2,140 a quarter, halved)

Notes: The cost we can state is hours: between 31 and 57 developer hours for the build out of 72 available, and up to 27 hours of presentations from me. The model and cloud bill is capped by a quota under 500 euros and is not yet estimated per start; the first thing the evaluation goal records is what 30 cases cost, and the review in December carries the measured figure. Who pays after the pilot is settled: the sponsor's budget line.

---

## Three risks, each with a control and an owner
Covers: risks
Evidence: docs/architecture/smb-self-serve-ads.md C1, C2, C4; docs/plans/smb-self-serve-ads.md summary risks

- Out-of-region product: code filters before the model and checks after (C1); owner: the developer; acceptance: zero in 30 cases
- Wrong price: prices come only from the pricing and inventory services (C2); owner: platform team
- Refunds rise: 4% switch-off, weekly review of flagged cases; owner: platform product owner

Notes: Three risks. A product that cannot run where she is: our code filters before the model and checks again after, and the evaluation set allows zero such cases. A wrong price: the model never sees a price; the services supply it. Refunds rising: the four percent rule and a weekly review with sales. What did not hold up: we have no money estimate per start yet, and the evaluation thresholds are proposed, not agreed; both are closed inside the four weeks.

---

## Decision: do nothing, run the four-week proof of concept, or run a wider pilot; we recommend the proof of concept
Covers: ask
Evidence: docs/plans/smb-self-serve-ads.md G01, W1; options are the presenter's framing

- A. Run the proof of concept: one developer, four weeks, half of starts from week two, measured report on 11 Dec (recommended)
- B. Wider pilot on all starts: more signal, no hosting sign-off, no cost measured yet
- C. Do nothing: product choice keeps losing 38%; sales keeps about 35 escalations a week
- Decider: Director of SMB Sales, 29 Oct 2026; undecided means the developer is not booked for 2 Nov

Notes: Three options. Do nothing, and product choice keeps losing 38 percent of starts. A wider pilot on all starts, with more signal but no hosting sign-off and no measured cost behind it. Or the four-week proof of concept, half of starts from week two, ending in a measured report against the 62 percent on the eleventh of December, not only a demo; that is our recommendation. The decision is yours today; if nothing is decided the developer is not booked for the second of November.

---

## Questions we expect, with the record's answer
Covers: questions
Evidence: docs/discovery/smb-self-serve-ads.md §4, §8; docs/architecture/smb-self-serve-ads.md §4, §6; docs/plans/smb-self-serve-ads.md

- Baseline: 62% of 2,140 starts, funnel export Q3 2026, product owner
- Cost per month at full adoption: not estimated; G04 measures 30 cases; the December review carries it
- Model price or behaviour changes: the model is pinned; filters are code; the 30 cases are re-run on a swap
- Accountable for a wrong recommendation: the confirming person at booking; the product owner owns the review loop
- Who signed off: product owner (problem and 50% split); platform team (access, hosting at the production review); sponsor's budget line pays after the pilot
- Change for people: sales review flagged cases about an hour a week (assumed); one training session (assumed)

Notes: Appendix; not spoken unless asked.

---

## Why this use case and not the others in the portfolio
Covers: appendix
Evidence: docs/discovery/smb-self-serve-ads.md §3 portfolio and helper ranking

- O1 product choice: score 11; largest drop, data at hand, reversible
- O3 explain the price: score 8; cheap but small (9% drop)
- O4 draft escalation replies: score 5; helps staff, not the KPI
- O2 creative wait: score 4; no baseline, rights data uncertain

Notes: Appendix; the ranking helper's output is pasted in the brief.
