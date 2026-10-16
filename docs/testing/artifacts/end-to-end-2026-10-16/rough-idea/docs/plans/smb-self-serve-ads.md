# Implementation plan: guided product recommendation (proof of concept)

Design: `docs/architecture/smb-self-serve-ads.md`. Brief: `docs/discovery/smb-self-serve-ads.md`. Compact form: estimates in quarter hours added by hand; no schedule block, no helper run.

## Summary

Profile: proof of concept, kept. One developer, new to ADK (multiplier 1.5 on every goal), about 30 focused hours a week for four weeks: 120 hours × 0.8 focus = 96, minus a 25% reserve = **72 hours** for goals. Phase 1 developer goals G02 to G06 total **31.5 to 57 hours**, so the high end fits with 15 hours to spare; presentation goals are owned by the AI engineer and sit outside the developer's hours. Longest chain G02 → G03 → G05 → G06: 25.5 to 45 hours; the service goes live in week two (W3). Dates (invented, from the 29 Oct decision): build 2 to 27 Nov 2026, live from 9 Nov, production decision review 11 Dec 2026. Largest risks: the evaluation labels (G04) depend on the product owner's hours; the platform integration slot (W3) is outside the team; the logged sentence's retention is undecided. Decisions needed from the sponsor: G01's approval on 29 Oct; D6 thresholds agreed by the product owner.

Cut line: everything in phase 1 fits. If the work runs high, G04 shrinks to 15 cases first; if it still runs high, G06's weekly review query moves to phase 2 and the review is run by hand once.

## Goals and dependencies

| ID and goal | Phase | Type | Human hours (×1.5 applied) | Depends on | Primary skill | State |
| --- | --- | --- | --- | --- | --- | --- |
| G01 Proof-of-concept approval presentation, business | 1 | presentation | 4.5–9 | design | adk-presenter | done; approved 2 Oct 2026 (invented, early); evidence below |
| W1 Leadership decision | 1 | wait | 29 Oct 2026 | G01 | | |
| G02 Local recommendation service: filter, schema, validators, call cap | 1 | implementation | 9–15 | W1 | adk-model-and-output-contracts | done; evidence below |
| G03 Price and availability from the services, with fallbacks | 1 | implementation | 4.5–7.5 | G02 | safe-api-tool-calls | done; evidence below |
| G04 Offline evaluation set of 30 labelled cases, thresholds agreed | 1 | implementation | 6–12 | G02 | adk-agent-evaluation | done; evidence below |
| W2 Platform project access and read-only credentials | 1 | wait | 3 working days, requested 2 Nov | W1 | | |
| G05 Cloud Run service in the platform project, quota, log table | 1 | implementation | 6–10.5 | G03, W2 | deploy-adk-on-google-cloud | done; evidence below |
| W3 Platform integration slot (week two) | 1 | wait | by 9 Nov | W1 | | |
| G06 Live on 50% of starts; weekly review query; arm join checked | 1 | implementation | 6–12 | G04, G05, W3 | adk-frontend-integration | done, A3 NOT RUN; evidence below |
| G07 Production decision review presentation, business | 1 | presentation | 4.5–9 | G06 | adk-presenter | ready: `docs/presentations/smb-self-serve-ads/production-approval-business.md` |
| G08 Production decision review presentation, technical (platform team) | 1 | presentation | 4.5–9 | G06 | adk-presenter | ready: `docs/presentations/smb-self-serve-ads/production-approval-technical.md` |
| W4 Production decision | 1→2 | wait | 6 Nov 2026 (two weeks after the pilot ended 23 Oct; brief §1; invented) | G07, G08 | | approved option A, 6 Nov 2026 (invented) |
| G09 Graduate to production: scope, observability, release gate, retention | 2 | implementation | 30–60 | W4 | adk-release-engineering | done, 47 h, live 14 Dec 2026 (invented); evidence below |
| G10 Results review presentation after one quarter, business (and technical) | 2 | presentation | 4.5–9 | G09 + one quarter live | adk-presenter | ready: `docs/presentations/smb-self-serve-ads/final-results-business.md`, `final-results-technical.md` |
| G11 Case study (optional, if results may be shared) | later | presentation | 4.5–9 | G10 | adk-presenter | drafted: `docs/presentations/smb-self-serve-ads/case-study.md` (internal draft, pack not sent; sharing approved 10 Apr 2027, invented) |

Phase 1 developer hours (G02–G06): 31.5–57. Presentation hours (G01, G07, G08): 13.5–27, AI engineer, with one review hour each from the developer counted inside G02–G06's review time.

## Phase 1 goals without a ticket yet

Goals G01 to G04 live in their tickets. The rest, four to six lines each:

### G05 — Cloud Run service in the platform project, quota, log table
- Outcome: the service from G03 runs in the platform team's project, invoked only by the platform's service account; the Gemini quota caps monthly calls; the C5 table exists. Contracts C4, C5; decisions D2, D5.
- Estimate 6–10.5 h; waits W2; owner developer.
- Primary skill: deploy-adk-on-google-cloud. Supporting: adk-tool-auth-and-secrets (read-only credentials in Secret Manager).
- Acceptance: A1 an unauthenticated call is refused and the platform identity succeeds (D2); A2 a request writes one log row with start id, arm and build tag, and a failed write still returns a response (C5); A3 the project quota is set and a call over it falls back to today's page (C4), live, bounded.
- Run: `/adk-engineer Carry out G05 from docs/plans/smb-self-serve-ads.md.`

### G06 — Live on 50% of starts; weekly review query; arm join checked
- Outcome: the platform routes half of the starts to the service from 9 Nov; the weekly query reads completion per arm from the funnel export joined on start id. Contract C5; decision D4.
- Estimate 6–12 h; waits W3; owner developer with the platform team.
- Primary skill: adk-frontend-integration. Supporting: adk-agent-evaluation (weekly review of flagged cases).
- Acceptance: A1 both arms appear in the log within one day of go-live (D4); A2 the join returns per-arm completion for the first week with fewer than 2% unmatched starts (C5); A3 the switch-off (refunds above 4%, brief §4) takes effect without a deploy.
- Run: `/adk-engineer Carry out G06 from docs/plans/smb-self-serve-ads.md.`

### G07 and G08 — Production decision review presentations (business; technical)
- Outcome: the deck for the review two weeks after the pilot ends, from G04's offline result and G06's live measure against 62% and the refund guardrail; G08 adds the design, contracts table, evaluation report and runbook by path for the platform team that must host it.
- Estimate 4.5–9 h each; wait W4 (11 Dec 2026, invented); owner AI engineer.
- Primary skill: adk-presenter. Acceptance: A1 `check_deck.py` passes on `docs/presentations/smb-self-serve-ads/production-approval-<audience>.md`; A2 every number cites G04 or G06 evidence recorded in this plan; A3 cases not run are named on a slide.
- Run: `/adk-presenter Prepare the production decision review from docs/plans/smb-self-serve-ads.md for a business audience` (and `technical`).

## Phase 1 evidence (recorded 24 October 2026; every figure invented for this trial and labelled so)

Recorded by the AI engineer from the developer's report (user said, 24 Oct 2026). The plan's November calendar in the summary is superseded: the decision came early and the pilot ran 10 to 23 October 2026 (user said, invented). Build measured: `rec-svc:poc-20261009-7f3a1c2` (invented), `google-adk==2.8.0`, `gemini-3.8-flash`; the same build served the whole window; there is no separate demo build. Currency note: the allowance was set in EUR (design §1); the billing export reports USD, recorded as billed.

| Goal and case | Result | Method and sample | Build | Status |
| --- | --- | --- | --- | --- |
| G01/A1–A3 | pass: check exit 0; decision recorded in `docs/presentations/smb-self-serve-ads/decision-memo.poc-approval.md` | leadership approved on 2 Oct 2026 (invented, early) | n/a | done |
| G02/A1–A5 | pass: 17 offline tests with a stubbed model; pin `google-adk==2.8.0` confirmed; `max_llm_calls=2` | pytest, offline (invented) | poc-20261009-7f3a1c2 | done |
| G03/A1–A3 | pass: pricing-down path serves "price on the next page"; catalogue timeout serves today's page plus a sales link; a price in a reason is rejected | pytest with stubbed services (invented) | poc-20261009-7f3a1c2 | done |
| G04/A1 | pass: zero out-of-region recommendations in 30 cases (C1) | offline set of 30 labelled cases, one run, thresholds agreed by the product owner on 8 Oct (invented) | poc-20261009-7f3a1c2 | done |
| G04/A2 | pass: actual product among the recommendations in 23 of 30 cases, 77%, threshold 70% (D6, agreed) | same set, one run (invented) | poc-20261009-7f3a1c2 | done |
| G04/A3 | pass: all 30 reasons pass the C3 validator; no case skipped | same set (invented) | poc-20261009-7f3a1c2 | done |
| G05/A1–A3 | pass: unauthenticated call refused, platform identity succeeds; log row per request with start id, arm and build tag; quota set, over-quota call served the fallback page | live checks in the platform project, 9 Oct (invented) | poc-20261009-7f3a1c2 | done |
| G06/A1 | pass: both arms in the log within one day of go-live (10 Oct) | C5 log table (invented) | poc-20261009-7f3a1c2 | done |
| G06/A2 | pass: per-arm completion from the funnel export joined on start id; 1.3% unmatched starts | weekly query, weeks of 10 and 17 Oct (invented) | poc-20261009-7f3a1c2 | done |
| G06/A3 | **NOT RUN**: the switch-off without a deploy was never exercised because refunds stayed under 4%; a dry run is scheduled before production (G09) | n/a | n/a | not run |

**Outcome measure (we measured, invented):** product-choice completion in the treatment arm 70.8% (221 of 312 sessions) against 63.1% in the control arm (188 of 298) and the brief's baseline of 62% (funnel export, Q3 2026). Window 10 to 23 October 2026; method: funnel export joined on start id per arm (C5, G06/A2), read by the product owner. Margin from chance alone on 312 sessions is about 5.7 points (one over the square root of n), so the lift of 7.7 points over control and 8.8 over baseline is above the margin; no significance test was run.

**Counter-metric (we measured, invented):** refunds 3.0% of orders in the window, 2 of 67 orders, unchanged from the 3% baseline (brief §4); escalations not measured in the window.

**Cost (we measured, invented):** model and cloud spend $142 for the whole phase on the billing export, 1 to 23 October 2026, build-time and the 30-case evaluation runs included; the allowance was under 500 EUR. We estimate $142 over 312 treated sessions is about $0.46 a session, build-time spend included; the live-only share is not separated in the export. Developer hours 58 against the estimate of 31.5 to 57 (one hour over the high end; 72 available). Presentation hours not yet totalled.

**Developer's notes (invented, added for G08 because the technical outline asks for deviations and failure analysis; not in the user's report):** deviations from the design: (1) the C4 repair attempt re-sends the full prompt with the error appended rather than a shorter repair message, two calls at most still hold; (2) the C5 log row carries an extra `validator_drops` count. Failure analysis of G04/A2's 7 misses: 4 near-duplicate products differing only by region, 2 sentences with no region word, 1 unexplained; 0 validator drops of an out-of-region id in the live window. The pilot's log review found no personal data in the sentences (one manual pass, 50 rows sampled).

**Open after phase 1:** G06/A3 not run; retention of the logged sentence still undecided (platform team); production per-month cost is an estimate until G09 separates live spend from build spend.

## Phase 2 and later

- G09 (30–60 h, adk-release-engineering): per-advertiser scope if account data is read; traces and cost per start; evaluation gate in CI from the pilot's logs; retention for the logged sentence; platform hosting sign-off. Acceptance: the gate blocks a release that fails D6's thresholds.
- G10 (4.5–9 h, adk-presenter): results review after one quarter in production against 62% and the refund rate; acceptance as G07.
- Later: SDP screening of the sentence (trigger: personal data found in logs); per-month shared budget (trigger: more than one consumer); model migration (trigger: a shutdown date for `gemini-3.8-flash`); cost tuning (trigger: measured cost per start above the estimate); case study G11 (trigger: results approved for sharing).

## Phase 2 evidence (recorded 3 April 2027; every figure invented for this trial and labelled so)

Recorded by the AI engineer from the platform team's quarterly report and the billing export (user said, 3 Apr 2027). Production decision: option A approved 6 Nov 2026 (W4). Go-live on all starts 14 December 2026, build `rec-svc:prod-20261212-c41e9b0`; the same build served the whole quarter apart from one release on 20 Feb 2027 (`prod-20270220-9d02aa4`, evaluation-set refresh and the near-duplicate filter rule). G09 took 47 developer hours against 30 to 60 estimated.

| Item | Result | Method and sample | Source |
| --- | --- | --- | --- |
| G09 acceptance | pass: the CI gate blocked one release that failed D6 on 17 Feb (61% on the refreshed set before the filter rule); traces and a cost-per-start query live; retention rule: sentences deleted after 90 days; credentials rotated; runbook and two alerts; on-call: the platform team rota; G06/A3 dry run passed 12 Dec | CI log, platform project (invented) | G09 |
| Outcome (we measured) | product-choice completion 69.4% over Q1 2027, 1,603 of 2,310 starts, against the 62% baseline (funnel export, Q3 2026); by month 68.1% (Jan, 740 starts), 69.9% (Feb, 731), 70.2% (Mar, 839) | funnel export, all starts, read by the product owner; no control arm in production, so the counterfactual is the Q3 2026 baseline and the pilot's control arm (63.1%) | G06/A2 query kept in production |
| Counter-metric (we measured) | refunds 2.9% of orders, 28 of 951; baseline 3% | order system, Q1 2027 | brief §4 |
| Adoption (we measured) | 100% of starts offered; active: a start where the advertiser typed a sentence and saw at least one recommendation: 78%, 1,802 of 2,310; picked a recommended product: 44% of all starts, 1,016 | C5 log table joined on start id | C5 |
| Cost per month (we measured) | $198 (Jan), $204 (Feb), $231 (Mar); average $211 against the $330 estimate; about $0.27 a start live-only; Cloud Run about $38 a month of each | billing export; cost-per-start query from traces | G09 |
| People (we measured) | platform on-call 3 hours over the quarter; product owner review about 1 hour a week; sales review of flagged cases about 1 hour a week (reported) | time reported by owners (invented) | brief §6 |
| SLIs (we measured) | p95 latency 2.4 s; fallback page served on 1.1% of starts outside incidents; log-write failures 0.02%; 0 validator drops of out-of-region ids | traces and the C5 table, Q1 2027 | G09 |
| Evaluation gate | refreshed to 60 cases from production logs on 20 Feb 2027; 52 of 60 pass, 87%, gate 70%; run on every release | CI, one run per release | G09, D6 |
| Model | `gemini-3.8-flash` pinned; lifecycle checked 31 Mar 2027, no shutdown announced | lifecycle table | D3 |
| Escalations (reported) | about 22 a week in March 2027 against about 35 a week in Q3 2026; not logged | sales lead, reported | brief §2 |

**Incidents (we measured):**

| Date | What happened | Effect | Response | Severity |
| --- | --- | --- | --- | --- |
| 11 Feb 2027 | pricing service down 2 h 10 min | 63 starts saw "price on the next page" (C2 fallback); no wrong price shown; fallback-rate alert fired | no customer action; postmortem added the pricing service's health to the dashboard | low |
| 3 Mar 2027 | a marketing campaign doubled starts in one day; the Gemini project quota (1,500 calls a month, set from pilot traffic) was hit at 14:20 | 142 starts got the fallback page for 5 h 40 min; that day's completion 58% | alert fired; quota raised to 4,000 calls a month by 20:00; postmortem: quota now set from the forecast, alert threshold reviewed | medium |

**Lessons recorded:** the quota set from pilot traffic was the one control that failed under a normal marketing event; the near-duplicate filter rule removed the largest miss type (4 of 7 in the pilot); the CI gate caught a bad release once; escalations need a log, not a report.

**Open after the quarter:** no control arm, so the lift over the quarter is against the Q3 2026 baseline, not a concurrent control; escalations unlogged; per-advertiser personalisation would reopen the design (identity and data scope, §4).

## Resume here

Next ready goal: G10 (results review after one quarter), then G11 (case study) if results are approved for sharing.

```text
/adk-presenter Carry out G10 from docs/plans/smb-self-serve-ads.md.
```
