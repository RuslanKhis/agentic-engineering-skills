---
stage: production-approval
audience: technical
minutes: 30
title: Guided product recommendation service: proof-of-concept results and what production needs from the platform team
sources: docs/architecture/smb-self-serve-ads.md, docs/plans/smb-self-serve-ads.md (phase 1 evidence), docs/tickets/smb-self-serve-ads/G02.md to G04.md, docs/discovery/smb-self-serve-ads.md
decision: Host the recommendation service in production on all starts after G09 delivers observability, a release gate and the retention decision; the platform team lead signs off hosting by 6 November 2026
decider: Platform team lead (hosting sign-off); Director of SMB Sales decides production
date: 2026-11-06
---

## Guided product recommendation service: what the pilot measured and what production needs from your team
Covers: title
Notes: G08 in the plan. Figures from the plan's phase-1 evidence section (invented for this trial, labelled); design and contracts by path.

---

## The proof of concept passed 10 of 11 acceptance cases; production needs observability, a release gate, the retention decision and your hosting sign-off
Covers: summary
Evidence: docs/plans/smb-self-serve-ads.md phase 1 evidence table (G02 to G06); docs/architecture/smb-self-serve-ads.md §4 graduation conditions; measured

- Passed: G02/A1–A5, G03/A1–A3, G04/A1–A3, G05/A1–A3, G06/A1–A2 on build `rec-svc:poc-20261009-7f3a1c2`
- Not run: G06/A3 (switch-off without a deploy)
- Live: completion 70.8% on 312 treated sessions against 63.1% control (G06/A2)

Notes: The bottom line for this room: the service passed every acceptance case that was run, ten of eleven, on one build, and the live measure held up: 70.8 percent completion on 312 treated sessions against 63.1 in the control arm. The eleventh case, switching the recommendation off without a deploy, was never run. Production needs four things the design deferred on purpose: observability, a release gate, a retention decision on the logged sentence, and your hosting sign-off. The design is at docs/architecture, the evidence in the plan's phase-1 section; I will quote figures and link the rest.

---

## Built against the design with two deviations: the repair attempt is a second full call, and the log table has one extra column
Covers: architecture
Evidence: docs/architecture/smb-self-serve-ads.md §2, D1, D5, C4, C5; docs/plans/smb-self-serve-ads.md phase 1 evidence (G02/A3, G05/A2); deviations recorded as measured on the build

- As designed: Cloud Run in your project, platform service-account invoker, `LlmAgent` with `output_schema`, no tools, candidates filtered in code (D1, D2)
- Deviation 1: the C4 repair re-sends the full prompt rather than the error alone; still two calls at most (G02/A3)
- Deviation 2: the C5 row carries a `validator_drops` count, not in the design (G05/A2)

Notes: What was built is the design's shape: one stateless service on Cloud Run in your project, invoked only by the platform's service account, one model call over a candidate list the code built, no tools, no writes. Two deviations, listed rather than implied. First, the repair attempt on invalid output re-sends the whole prompt with the error appended instead of a shorter repair message; the two-call cap still holds, it costs more tokens per repair. Second, the log row carries one extra column counting how many ids the validator dropped, which we found useful and the design did not name. Nothing else differs.

---

## Evaluation results: 30 of 30 cases pass C1 and C3, actual product in 23 of 30, one run, on the same build the live numbers cover; no demo
Covers: evidence, criteria-results
Evidence: docs/plans/smb-self-serve-ads.md phase 1 evidence (G04/A1–A3); docs/tickets/smb-self-serve-ads/G04.md; docs/architecture/smb-self-serve-ads.md D6; measured

- Set: 30 cases from the 1,327 completed-step records, labelled with the product owner; thresholds agreed 8 October
- Results: zero out-of-region (C1); all reasons name a catalogue attribute (C3); actual product among recommendations 77%, threshold 70%
- Repeats: one run; variance not measured. Build `rec-svc:poc-20261009-7f3a1c2` for the set and the live window; there is no demo

Notes: The evaluation set is 30 cases drawn from last quarter's completed records and labelled with the product owner, with thresholds agreed on 8 October before the run. Results: zero out-of-region recommendations across the 30, every reason names a real catalogue attribute, and the advertiser's actual product was among the recommendations in 23 of 30, 77 percent against the 70 agreed. One honest limit: it was run once, so we have no variance figure; production repeats it in the gate. The set and the live window were measured on the same build, and there is no demo build: what you see in the logs is what produced the numbers.

---

## Failure analysis: 7 of 30 cases missed the actual product, 4 of them because the catalogue gave two near-identical products
Covers: learned
Evidence: docs/plans/smb-self-serve-ads.md phase 1 evidence (G04/A2, G06/A2 unmatched starts); counts measured, root causes recorded by the developer

- 7 misses: 4 near-duplicate products (same format, two regions), 2 sentences with no region word, 1 unexplained
- Live: 1.3% of starts unmatched in the funnel join; 0 validator drops of an out-of-region id in the window
- Not measured: escalations per week; latency and tokens per request (no traces in the pilot)

Notes: Seven of the thirty cases missed the actual product. Four of them are the same root cause: the catalogue holds pairs of near-identical products that differ only by region, and the model picked the sibling; that is a data shape, not a model fault, and a filter rule handles it. Two cases had a sentence with no region word at all, where the recommendation was reasonable but not the one bought. One we could not explain. Live, 1.3 percent of starts did not match in the funnel join, under the 2 percent limit. Latency and tokens per request were not measured: the pilot had no traces, by design, and production adds them.

---

## Measured cost: $142 for the phase on the billing export; latency, tokens and the live-only share are not measured until G09 adds traces
Covers: cost
Evidence: docs/plans/smb-self-serve-ads.md phase 1 evidence (cost); docs/architecture/smb-self-serve-ads.md §4 observability row; measured spend, estimate labelled

- We measured: $142 model and cloud, 1 to 23 October, build runs and the 30-case evaluation included
- We estimate: about $0.46 a session over 312 treated sessions; about $330 a month at 713 starts a month, an upper figure
- Not measured: p95 latency, tokens per request, cost per start live-only; G09 adds traces and a cost-per-start query

Notes: Cost, without persuasion. The billing export says 142 dollars for the whole phase, which includes the build-time runs and the evaluation set, so it is an upper bound on the live spend. Dividing by the 312 treated sessions gives about 46 cents a session, and at 713 starts a month about 330 dollars; both are estimates from that one figure. What we cannot tell you: p95 latency, tokens per request, or the cost of a live start on its own, because the pilot ran without traces. Goal nine adds traces and a cost-per-start query before go-live.

---

## Production changes: all starts, traces and cost per start, a release gate, retention for the sentence; you inherit one service, one table, one quota
Covers: architecture, production-scope
Evidence: docs/plans/smb-self-serve-ads.md G09 (30 to 60 hours, estimated); docs/architecture/smb-self-serve-ads.md §4 depth table, §6 open decisions

- No change to hosting, identity or the model path (D2, D3); the arm split goes, all starts treated
- Added by G09: traces and cost per start; evaluation gate in CI; retention rule for the logged sentence; rotation of the read-only credentials
- You inherit: the Cloud Run service, the BigQuery log table, the Gemini quota; about 30 to 60 developer hours to get there

Notes: Production changes nothing in the hosting, the identity path or the model: Cloud Run in your project, your service account as the only invoker, the same pinned model. The arm split goes and every start is treated. Goal nine adds what the design deferred: traces and a cost-per-start query, an evaluation gate in CI that re-runs the 30 cases on every release, a retention rule for the sentence the advertiser types, and rotation of the read-only credentials. What your team inherits is one service, one log table and one quota, and the estimate for getting there is 30 to 60 developer hours.

---

## Contracts your services will depend on: five, unchanged from the design, each with a test that proved it on the pilot build
Covers: contracts
Evidence: docs/architecture/smb-self-serve-ads.md §3 contracts table C1 to C5; docs/plans/smb-self-serve-ads.md phase 1 evidence (G02, G03, G05, G06)

- C1 region filter, C3 reason validator: G02/A2, G02/A4, G04/A1; C2 price from your services only: G03/A1–A3
- C4 two calls a start, quota: G02/A5, G05/A3 proven live; C5 log row per start with build tag: G05/A2, G06/A2
- Request shape `POST /recommend {account, region, sentence, start_id, arm}`; the `arm` field becomes optional in production

Notes: The contracts table in the design, section three, is unchanged, and every row now has a test that proved it on the pilot build. The region filter and the reason validator were proven offline and in the 30-case set. The price contract, that no price ever comes from the model, has three tests including the pricing-service-down path. The two-call cap and the quota fallback were proven live in your project. The log contract was proven by the join itself. One wire change for production: the arm field in the request becomes optional, since every start is treated; the platform side keeps sending it until the join query changes.

---

## Security and data boundary: no writes, no tools, no end-user identity, proven by tests; the sentence's retention is the open item
Covers: risks
Evidence: docs/architecture/smb-self-serve-ads.md §4 depth table, §5 failure rows, D2; docs/plans/smb-self-serve-ads.md phase 1 evidence (G02/A2, G05/A1); measured where a case is cited

- Injected instruction in the sentence changes nothing: no tools, no writes (G02/A2, passed)
- Unauthenticated call refused; only the platform identity succeeds (G05/A1, passed)
- Open: retention of the logged free-text sentence (platform team decides before go-live); SDP screening deferred until personal data appears in the logs

Notes: The security boundary is narrow by construction and the tests say so. A sentence carrying an injected instruction changes nothing, because the model has no tools and the service writes only its own log row; that case passed. An unauthenticated call is refused and only your service account succeeds; that case passed live. The one open item is yours: how long the free-text sentence stays in the log table. The design deferred screening it for personal data until any appears; the review of the pilot's logs found none, but nobody is looking continuously, which is why the retention rule is a go-live condition.

---

## Operations: no traces, alerts or runbook exist today; G09 adds them, pins the model, and makes rollback of image, prompt and schema one step
Covers: operations
Evidence: docs/architecture/smb-self-serve-ads.md §4 observability and release rows, D3; docs/plans/smb-self-serve-ads.md G09, phase 1 evidence (G06/A3 NOT RUN); planned

- Today: Cloud Run logs and the C5 table; a weekly failed-write count; no pager
- G09: traces, cost per start, an alert on fallback-page rate and on log-write failures; a runbook; on-call owner to be named by your team
- Release: `gemini-3.8-flash` pinned, no shutdown announced; image, prompt and schema roll back together; the switch-off without a deploy (G06/A3) gets its dry run

Notes: Operations today is honest and thin: Cloud Run logs, the log table, and a weekly count of failed writes; nobody is paged. Goal nine adds traces, a cost-per-start query, and two alerts: the rate of fallback pages served, and log-write failures. It writes the runbook, and it needs your team to name the on-call owner. Release: the model is pinned and has no shutdown announced; image, prompt and schema are versioned together so a rollback is one step; and the switch-off without a deploy, the case we never ran, gets its dry run before go-live.

---

## Decision: we need your hosting sign-off, the retention rule and an on-call owner by 6 November; owner: platform team lead
Covers: ask
Evidence: docs/plans/smb-self-serve-ads.md W4, G09; docs/architecture/smb-self-serve-ads.md §4 graduation conditions, §6

- A. Sign off hosting now, conditional on G09's gate, traces and retention rule (recommended): go-live in December after 30 to 60 hours
- B. Sign off after G09 is reviewed: adds one review cycle; go-live slips into January
- C. Decline hosting: the pilot stays at 50% on the current build with no owner
- Needed from you by 6 November: the retention rule, an on-call owner, about four review hours; the Director of SMB Sales decides production the same day

Notes: Three options for your team. A, sign off hosting now, conditional on goal nine delivering the gate, the traces and the retention rule; go-live in December. B, sign off only after reviewing goal nine's output; that adds a cycle and go-live slips to January. C, decline, and the pilot stays at half the traffic with no owner. We recommend A because every contract has a passing test and what remains is operational work with a known estimate. From you by 6 November: the retention rule, an on-call owner and about four review hours. The Director of SMB Sales decides production the same day. Credit: the developer, the product owner for the labels, and your team for access in three days.

---

## Questions we expect, with the record's answer
Covers: questions, appendix
Evidence: docs/plans/smb-self-serve-ads.md phase 1 evidence; docs/architecture/smb-self-serve-ads.md C1 to C5, D3; docs/tickets/smb-self-serve-ads/G02.md

- Worst failure modes and how often run? Out-of-region id and injected sentence (G02/A2), invalid output (G02/A3), pricing down (G03/A1); pytest, run on every build; the 30-case set once
- p95 latency and tokens per turn? Not measured; G09 traces
- Which model version, retired when? `gemini-3.8-flash`, stable, lifecycle checked 2026-10-08, no shutdown announced (D3)
- Rollback of prompt, model and schema together? One image tag today; G09 makes the gate block a release that fails D6
- What deviated from the design? Two items on slide 3; both recorded

Notes: Appendix for the question period; answers use the protocol: restate, one sentence, evidence with sample, bridge.
