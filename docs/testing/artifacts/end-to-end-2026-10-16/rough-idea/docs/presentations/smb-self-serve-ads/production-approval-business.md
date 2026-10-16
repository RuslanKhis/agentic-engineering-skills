---
stage: production-approval
audience: business
minutes: 15
title: Guided product choice: proof-of-concept results and the production decision
sources: docs/discovery/smb-self-serve-ads.md, docs/architecture/smb-self-serve-ads.md, docs/plans/smb-self-serve-ads.md (phase 1 evidence), docs/tickets/smb-self-serve-ads/G04.md
decision: Build the guided product recommendation for production on all self-serve starts, hosted by the platform team, at an estimated model and cloud cost of about $330 a month
decider: Director of SMB Sales (chairing leadership)
date: 2026-11-06
---

## Guided product choice: what the proof of concept measured, and the production decision
Covers: title
Notes: G07 in the plan; every number comes from the plan's phase-1 evidence section, recorded 24 October 2026 and labelled invented for this trial.

---

## The proof of concept met three of three criteria; we recommend building for production at about $330 a month
Covers: summary
Evidence: docs/plans/smb-self-serve-ads.md phase 1 evidence (G06/A2, G04/A1–A3, refunds); cost estimate from $142 over 312 sessions

- We measured: completion 70.8% on 312 treated sessions, 10 to 23 October, against 62% baseline
- We measured: refunds 3.0%, unchanged; zero out-of-region recommendations in 30 cases
- We estimate: about $330 a month at full adoption; one acceptance case not run

Notes: I am asking you to approve building the guided product choice for production on every self-serve start, at an estimated model and cloud cost of about 330 dollars a month. The proof of concept met all three criteria we agreed in October: completion of the product-choice step was 70.8 percent on 312 treated sessions against the 62 percent baseline, refunds stayed at 3 percent, and the offline set showed zero out-of-region recommendations. One acceptance case was not run; I will name it. Interrupt me whenever you want to go to the decision; the summary comes first and the discussion after.

---

## Criteria agreed on 2 October and what we measured: three thresholds, three passes
Covers: criteria-results
Evidence: docs/discovery/smb-self-serve-ads.md §4 thresholds; docs/architecture/smb-self-serve-ads.md D6; docs/plans/smb-self-serve-ads.md phase 1 evidence (G06/A2, G04/A1, G04/A2); measured

| Criterion | Threshold | Measured | Method, sample |
| --- | --- | --- | --- |
| Completion above 62% | above 62% | 70.8% | funnel export per arm, 312 sessions |
| Refunds at or under 4% | 4% | 3.0% | 2 of 67 orders |
| Out-of-region recommendations | zero | zero; actual product in 77% | 30 labelled cases, threshold 70% |

Notes: Here is the table we agreed before the build, with what we measured beside each line. Completion of the product-choice step: the threshold was anything above 62 percent, and we measured 70.8 percent on 312 treated sessions, read from the funnel export joined per arm by the product owner. Refunds: the guardrail was 4 percent, and we measured 3.0 percent, two of 67 orders in the window. The offline set of 30 cases labelled with the product owner showed zero out-of-region recommendations and the advertiser's actual product among the recommendations in 77 percent of cases, against the agreed 70. Three of three.

---

## Completion moved from 62% to 70.8% on 312 treated sessions; the control arm measured 63.1% in the same weeks
Covers: criteria-results
Evidence: docs/plans/smb-self-serve-ads.md phase 1 evidence (G06/A2); baseline docs/discovery/smb-self-serve-ads.md §2; measured, margin estimated

- Chart: three bars on one scale, baseline 62% (Q3 2026, 2,140 starts), control 63.1% (298 sessions), treatment 70.8% (312 sessions); treatment coloured, baseline drawn flat
- We estimate the margin from chance at about 5.7 points on 312; the lift of 7.7 over control is above it; no significance test was run

Notes: One chart, three bars on the same scale. The grey bar on the left is last quarter's baseline, 62 percent of 2,140 starts. The middle bar is the control arm in the same two weeks, 63.1 percent on 298 sessions, which tells us the quarter did not simply get easier. The coloured bar is the treatment arm, 70.8 percent on 312 sessions. We estimate the margin from chance alone at about 5.7 points on a sample this size, so the lift of 7.7 points over control is above it; we did not run a formal significance test, and the production quarter will give a larger sample. Now what did not work.

---

## What did not work: one acceptance case was never run, and the build took 58 hours against 57 estimated
Covers: learned
Evidence: docs/plans/smb-self-serve-ads.md phase 1 evidence (G06/A3 NOT RUN; hours); measured

- Not run: G06/A3, switching the recommendation off without a deploy, because refunds never crossed 4%; a dry run is scheduled before production
- Hours: 58 against 31.5 to 57 estimated; one hour over the high end, inside the 72 available
- Escalations per week were not measured in the window

Notes: Three things did not work, each with the answer. First, one acceptance case was never run: the switch-off that turns the recommendation off without a deploy. It was never needed because refunds stayed under 4 percent, so it remains unproven, and the production work includes a dry run of it before go-live. Second, the build took 58 developer hours against an estimate of 31.5 to 57, one hour over the top of the range and inside the 72 we had. Third, we did not measure escalations to sales in the window, so the secondary benefit is still a hypothesis.

---

## What we learned that changes the plan: the offline threshold holds, the live spend is not separated from the build spend
Covers: learned
Evidence: docs/plans/smb-self-serve-ads.md phase 1 evidence (G04/A2, cost); docs/architecture/smb-self-serve-ads.md D6, §4 depth table

- D6's 70% threshold was agreed on 8 October and met at 77%; it becomes the release gate in production
- The billing export holds one figure, $142, for build runs and live traffic together; production separates cost per start
- The logged sentence's retention is still undecided; it is now a condition of go-live

Notes: Two findings change the plan. The offline threshold the product owner agreed, the advertiser's actual product among the recommendations in 70 percent of cases, was met at 77 percent, so it becomes the gate every production release must pass. And the billing export gives us one figure for the whole phase, 142 dollars, with the build-time runs and the live traffic mixed together; production will measure cost per start on its own. One open item from the design stays open: how long we keep the sentence the advertiser types. The platform team decides it before go-live.

---

## Production scope: every self-serve start, all regions, with the person still confirming every purchase; built in 30 to 60 hours by December
Covers: production-scope, timeline
Evidence: docs/plans/smb-self-serve-ads.md G09; docs/architecture/smb-self-serve-ads.md §4 graduation conditions; W4; estimated

- Workflow change: unaided browsing and the product-choice escalation go; the advertiser types one sentence; sales reviews flagged cases weekly
- G09: observability, release gate, retention, hosting sign-off; 30 to 60 hours (estimate)
- Checkpoints: decision 6 November; go-live after the platform team's sign-off; results review after one quarter

Notes: The production scope is the same service on every start, in every region, with nothing added to what the model may do. The workflow change is the one we tested: the advertiser types a sentence instead of browsing forty products, sales staff review flagged recommendations once a week, and a person still confirms every purchase at booking. The remaining work, goal nine in the plan, is what production needs and the pilot deferred on purpose: observability, a release gate from the evaluation set, the retention decision, and the platform team's hosting sign-off. We estimate 30 to 60 hours. Checkpoints: your decision today, go-live after sign-off, and a results review after one quarter.

---

## Production cost: we estimate about $0.46 a session and about $330 a month; the pilot cost $142 and 58 hours
Covers: cost
Evidence: docs/plans/smb-self-serve-ads.md phase 1 evidence (cost, hours); docs/discovery/smb-self-serve-ads.md §4 unit economics (about 700 starts a month); estimate from measured inputs

- We measured: $142 model and cloud, 1 to 23 October, build runs included; 58 developer hours
- We estimate: $142 over 312 sessions is about $0.46 a session; at about 713 starts a month (2,140 a quarter) about $330 a month, an upper figure because build spend is inside it
- Not measured: the platform team's operating hours (G09)

Notes: Second, the cost. We measured 142 dollars of model and cloud spend for the whole phase, build-time runs included, and 58 developer hours. From that we estimate about 46 cents a session, and at about 713 starts a month, which is 2,140 a quarter spread evenly, about 330 dollars a month at full adoption. That is an upper figure, because the build-time runs are inside the 142. The build for production is 30 to 60 developer hours. What we have not measured is the platform team's operating time once they host it; goal nine records it. Pause here if you want the arithmetic; it is on the slide.

---

## Three risks, each contained by a control with an owner; a person validates every purchase before money moves
Covers: risks
Evidence: docs/architecture/smb-self-serve-ads.md C1, C2, C4, §4; docs/plans/smb-self-serve-ads.md phase 1 evidence (G04/A1, G05/A3); measured and planned controls

- Wrong product for the region: code filters before the model sees the list; zero in 30 cases; owner: developer
- Wrong price: prices come from the pricing service, never the model; owner: platform team
- Spend runs away: two calls a start, project quota, fallback page proven live; owner: platform team lead
- Validation: the advertiser picks; a person confirms 100% of purchases; the product owner reviews flagged cases weekly

Notes: Third, the risks, spoken as confidence: what the service cannot do and who answers for each. It cannot recommend a product that cannot run in the advertiser's region, because our code filters the list before the model sees it, and the 30-case set showed zero; the developer owns that validator. It cannot state a price, because prices come from the pricing service; the platform team owns that path. It cannot run up the bill: two model calls a start and a project quota, and we proved the fallback page under quota live; the platform team lead owns the quota. And a person confirms every purchase before any money moves, as today. The product owner is accountable for the weekly review of flagged cases.

---

## Decision: stop, extend the pilot, or build for production on all starts; we recommend building; Director of SMB Sales, 6 November
Covers: ask
Evidence: docs/plans/smb-self-serve-ads.md W4, G09; docs/presentations/smb-self-serve-ads/decision-memo.md; measured results above, cost estimated

- A. Build for production (recommended): G09, 30 to 60 hours, about $330 a month estimated; go-live after the platform team's sign-off
- B. Extend the pilot one more quarter on 50% of starts: same cost, a larger sample, revenue effect delayed
- C. Stop: keep the code and the 30-case set; product choice keeps losing 38%
- Decider: Director of SMB Sales, 6 November 2026; nothing decided means the pilot stays switched on at 50% with no owner for the bill

Notes: Three options. A, build for production on all starts: 30 to 60 developer hours, about 330 dollars a month estimated, go-live when the platform team signs off. B, extend the pilot for a quarter at half the traffic: the same running cost, a larger sample, and the revenue effect delayed by a quarter. C, stop: we keep the code and the evaluation set, and product choice keeps losing 38 percent. We recommend A, because three of three criteria were met above the margin and the controls held. The Director of SMB Sales decides today, 6 November. If nothing is decided, the pilot stays on at half the traffic with nobody owning the bill. Credit: the developer built it in four weeks; the product owner labelled every case; the platform team gave access in three days.

---

## Questions we expect, with the record's answer
Covers: questions, appendix
Evidence: docs/plans/smb-self-serve-ads.md phase 1 evidence; docs/architecture/smb-self-serve-ads.md D3, D4, §4; docs/discovery/smb-self-serve-ads.md §4

- How many users is this based on? 312 treated and 298 control sessions, 10 to 23 October; 67 orders for the refund rate (G06/A2; measured)
- What if the model's price or behaviour changes? Model id pinned, no shutdown announced (D3); the release gate re-runs the 30 cases (G09)
- Who is accountable for a wrong recommendation? The confirming person at booking, as today; the product owner for the weekly review (brief §4)
- Vanity count: 312 sentences typed in the window; not an outcome (measured)
- Is the demo the measured build? There is no demo; the numbers cover build `rec-svc:poc-20261009-7f3a1c2`
- What would make you stop? Refunds above 4% switch it off; the switch-off is the case not yet run (G06/A3)

Notes: Appendix for the question period; each answer is restated, given in one sentence, then the evidence with its sample, then the bridge to the recommendation.
