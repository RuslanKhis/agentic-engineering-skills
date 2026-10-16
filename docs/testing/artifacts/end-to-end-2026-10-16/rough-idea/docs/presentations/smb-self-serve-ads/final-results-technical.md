---
stage: final-results
audience: technical
minutes: 30
title: Guided product recommendation service: the first production quarter, operations and handover
sources: docs/plans/smb-self-serve-ads.md (phase 2 evidence), docs/architecture/smb-self-serve-ads.md, docs/discovery/smb-self-serve-ads.md
decision: Information on the quarter; one decision asked: keep a 10% control arm for one month on the next release, and log escalations
decider: Platform team lead; Director of SMB Sales for the control arm's traffic share
date: 2027-04-14
---

## Guided product recommendation service: production over Q1 2027, operations and handover
Covers: title
Notes: G10, technical version. Figures from the plan's phase-2 evidence section (invented for this trial, labelled).

---

## Production over Q1 2027: p95 2.4 s, fallback on 1.1% of starts, $211 a month, two incidents, one release blocked by the gate
Covers: summary
Evidence: docs/plans/smb-self-serve-ads.md phase 2 evidence (SLIs, cost, incidents, G09 acceptance); measured

- SLIs from traces: p95 latency 2.4 s; fallback page 1.1% of starts outside incidents; log-write failures 0.02%; 0 out-of-region drops
- Cost $211 a month average (billing export); completion 69.4% on 2,310 starts
- Incidents: pricing outage 11 Feb (low); quota hit 3 Mar (medium); CI gate blocked one release on 17 Feb

Notes: The bottom line for this room: over the first quarter in production the service ran at a p95 of 2.4 seconds, served the fallback page on 1.1 percent of starts outside the two incidents, failed 0.02 percent of log writes and never shipped an out-of-region id. It cost 211 dollars a month on average. Two incidents, one low and one medium, and the CI gate blocked one release in February. The outcome the business reads is 69.4 percent completion on 2,310 starts. I will go through what shipped, what the gate holds, the incidents, the handover and the one decision.

---

## Architecture as shipped matches the production-approval plan, with one deviation: the arm field stayed mandatory
Covers: architecture
Evidence: docs/architecture/smb-self-serve-ads.md §2, D1 to D5; docs/plans/smb-self-serve-ads.md phase 2 evidence (G09 acceptance); production-approval-technical.md slide 8

- Shipped: Cloud Run in the platform project, platform service-account invoker, one `LlmAgent` with `output_schema`, no tools; traces; cost-per-start query; 90-day retention on the sentence; rotated read-only credentials
- Builds: `prod-20261212-c41e9b0` (go-live), `prod-20270220-9d02aa4` (eval refresh, near-duplicate rule)
- Deviation: the `arm` request field stayed mandatory, fixed to `treatment`; the join query was not changed

Notes: What shipped is what the November review approved: the same service, the same identity path, the same pinned model, with traces, a cost-per-start query, a 90-day retention rule on the sentence and rotated credentials. Two builds served the quarter: the go-live build from 12 December and one release on 20 February that refreshed the evaluation set and added the near-duplicate filter rule. One deviation from what I told you in November: the arm field in the request stayed mandatory and is fixed to treatment, because we never changed the join query. It matters for the decision at the end.

---

## Evaluation and release gates in force: 60 cases refreshed from production logs, 52 pass at a 70% gate, run on every release; model pinned, no retirement date
Covers: evidence, operations
Evidence: docs/plans/smb-self-serve-ads.md phase 2 evidence (evaluation gate, model rows; G09 acceptance); docs/architecture/smb-self-serve-ads.md D3, D6; measured

- Gate: D6's 70% on the actual-product check plus zero out-of-region; 52 of 60 pass, 87%, one run per release
- Blocked once: 17 Feb, 61% on the refreshed set before the near-duplicate rule; shipped 20 Feb at 87%
- Refresh: 60 cases from production logs on 20 Feb 2027; next refresh due when the set is a quarter old; `gemini-3.8-flash` checked 31 Mar 2027, no shutdown announced

Notes: The release gate is the one the November review asked for. It runs the evaluation set on every release and blocks when fewer than 70 percent of cases have the actual product among the recommendations or any case is out of region. It did its job once: on 17 February the set refreshed from production logs scored 61 percent, below the gate, because the new cases carried more near-duplicate products; the filter rule fixed it and the release shipped on the 20th at 87 percent, 52 of 60. The set is one run per release, so no variance figure. The model is pinned and had no retirement date on the lifecycle table as of 31 March.

---

## Production quality over the quarter: p95 2.4 s, fallback 1.1%, log-write failures 0.02%, completion 69.4% with no control arm
Covers: outcome, adoption
Evidence: docs/plans/smb-self-serve-ads.md phase 2 evidence (SLIs, outcome, adoption rows); C5; measured

- Traces, Q1 2027: p95 latency 2.4 s; tokens per request not summarised in the report
- Fallback page 1.1% of starts outside incidents; log-write failures 0.02%; 1.3% unmatched starts in the join held from the pilot
- Adoption from the C5 table: 78% typed a sentence and saw a recommendation; 44% of starts picked one; completion 69.4%, by month 68.1, 69.9, 70.2

Notes: Production quality, from the traces and the log table. P95 latency 2.4 seconds across the quarter; I do not have tokens per request summarised in the quarterly report, only in the traces, so I will not quote a number. The fallback page was served on 1.1 percent of starts outside the incidents, mostly pricing-service timeouts. Log writes failed 0.02 percent of the time. From the log table: 78 percent of starts typed a sentence and saw a recommendation, 44 percent picked one, and completion was 69.4 percent, steady by month. The caveat for this room: no control arm, so that is against last year's baseline.

---

## Incidents: a pricing outage the fallback absorbed, and a quota set from pilot traffic that a marketing day exhausted
Covers: incidents
Evidence: docs/plans/smb-self-serve-ads.md phase 2 evidence (incidents table); docs/architecture/smb-self-serve-ads.md C2, C4, §5 failure rows; measured

- 11 Feb, low: pricing service down 2 h 10 min; 63 starts served "price on the next page" (C2); alert fired; fix: pricing-service health on the dashboard
- 3 Mar, medium: starts doubled; quota of 1,500 calls a month hit at 14:20; 142 starts got the fallback page over 5 h 40 min; completion 58% that day; quota raised to 4,000 by 20:00; now set from the forecast

Notes: Two incidents, with root causes. On 11 February the pricing service was down for two hours ten; the C2 fallback served 63 starts with "price on the next page", the fallback-rate alert fired, and the fix was to put the pricing service's health on our dashboard so we see it before the alert. On 3 March a marketing campaign doubled the day's starts; the Gemini quota, 1,500 calls a month set from the pilot's traffic, ran out at 14:20, and 142 starts got the fallback page over five hours forty until the quota was raised to 4,000 that evening. Root cause: a control sized from the pilot, not from a forecast. It is now set from the forecast and the alert threshold was reviewed.

---

## Cost breakdown: $211 a month, of which model about $173 and Cloud Run about $38; about $0.27 a live start; 47 build hours
Covers: cost
Evidence: docs/plans/smb-self-serve-ads.md phase 2 evidence (cost and people rows); production-approval-technical.md slide 6 (estimate); measured, arithmetic shown

- Billing export: $198, $204, $231 by month; Cloud Run about $38 of each; model is the rest, about $173 on the $211 average (our subtraction)
- Cost-per-start query: about $0.27 a live start against the $0.46 estimate, which carried build spend
- People: 47 developer hours for G09 (estimate 30 to 60); platform on-call 3 hours in the quarter; product owner and sales about 1 hour a week each (reported)

Notes: Cost from the billing export: 198, 204 and 231 dollars by month, 211 on average, of which Cloud Run is about 38 and the model the rest, about 173 by subtraction. The cost-per-start query from the traces gives about 27 cents a live start, against the 46 cents we estimated in November, which we said then carried the build-time runs. People: 47 developer hours to graduate it, inside the 30 to 60 estimate; the platform team logged three on-call hours in the quarter; the product owner and the sales reviewer report about an hour a week each.

---

## Security and data boundary: no writes, no tools, platform identity only, all verified in CI; retention enforced at 90 days; SDP screening still deferred
Covers: evidence
Evidence: docs/architecture/smb-self-serve-ads.md §4 depth table, D2; docs/plans/smb-self-serve-ads.md phase 2 evidence (G09 acceptance); G02/A2, G05/A1 run in CI

- Verified on every release: injected sentence changes nothing (G02/A2); unauthenticated call refused (G05/A1); schema has no price field (G03/A3)
- Retention: sentences deleted after 90 days, enforced by a scheduled job; credentials rotated once in the quarter
- Open: SDP screening of the sentence stays deferred; the manual log review found no personal data (one pass, 50 rows, invented in the record)

Notes: The security boundary did not move and the tests that prove it now run in CI on every release: an injected instruction in the sentence changes nothing, an unauthenticated call is refused, and the output schema has no price field. Retention of the sentence is enforced at 90 days by a scheduled job, and the read-only credentials were rotated once. One item stays open on purpose: screening the sentence for personal data; the one manual review of fifty rows found none, and the trigger in the design is unchanged, so this is a known gap rather than a finding.

---

## Handover: runbook, two alerts and the on-call rota are yours; known limitations: one eval run per release, no control arm, escalations unlogged
Covers: handover
Evidence: docs/plans/smb-self-serve-ads.md phase 2 evidence (G09 acceptance, open after the quarter, lessons); docs/architecture/smb-self-serve-ads.md §4

- In place: runbook; alerts on fallback-page rate and log-write failures; on-call: the platform team rota; dashboard with pricing-service health
- Limitations: evaluation set runs once per release, no variance; no control arm since go-live; escalations not logged; tokens per request not summarised
- Debt: the `arm` field and the join query; the quota alert threshold needs a forecast each quarter

Notes: What your team holds now: the runbook, two alerts, the dashboard with the pricing service's health on it since February, and the on-call rota that took the two incidents. The limitations I want on the record: the evaluation set runs once per release, so we have no variance; there has been no control arm since go-live; escalations are still not logged; and tokens per request are in the traces but not summarised. Debt: the arm field and the join query, and a quota alert whose threshold needs a forecast every quarter rather than a fixed number.

---

## Decision: keep 10% of starts in a control arm for one month on the next release and add an escalation log; owners: platform team lead and product owner, 14 April
Covers: next, ask
Evidence: docs/plans/smb-self-serve-ads.md phase 2 evidence (open after the quarter); docs/architecture/smb-self-serve-ads.md D4; estimated

- A. Next release: `arm` honoured again, 10% control for one month, escalation log written by the sales tool (recommended): about 8 to 12 developer hours (estimate)
- B. Control arm only, no escalation log: about 4 to 6 hours (estimate)
- C. Nothing: the quarter's lift stays against last year's baseline
- Decider: the platform team lead for the release; the Director of SMB Sales for the 10% share; 14 April

Notes: One decision for your team. A, on the next release honour the arm field again, hold ten percent of starts in control for one month, and have the sales tool write an escalation log; we estimate eight to twelve developer hours. B, the control arm only, four to six hours. C, nothing, and the lift stays measured against last year. We recommend A: the control arm answers the question the business will keep asking, and the escalation log turns a reported number into a measured one. The platform team lead decides the release; the Director of SMB Sales decides whether ten percent of starts may lose the recommendation for a month. Credit: the developer, the product owner for sixty labels, and your rota for the two incidents.

---

## Questions we expect, with the record's answer
Covers: questions, appendix
Evidence: docs/plans/smb-self-serve-ads.md phase 2 evidence; docs/architecture/smb-self-serve-ads.md D3, C1 to C5

- Which cases cover the worst failure modes, how often run? G02/A2 injection, G02/A3 invalid output, G03/A1 pricing down; in CI on every release; the 60-case set once per release
- p95 and tokens per turn? p95 2.4 s (traces); tokens not summarised, measured per request in traces
- Model pinned, retired when? `gemini-3.8-flash`, no shutdown announced as of 31 Mar 2027 (D3)
- Rollback? Image, prompt and schema in one tag; the gate blocked one release on 17 Feb
- What deviated? The arm field, slide 3

Notes: Appendix for the question period.
