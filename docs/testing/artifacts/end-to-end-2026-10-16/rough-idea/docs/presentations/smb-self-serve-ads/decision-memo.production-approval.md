# Decision memo: guided product choice, production decision

One page, sent before the meeting of 6 November 2026 as the pre-read and after it as the record. Everything here is in the decks' evidence (`production-approval-business.md`, `production-approval-technical.md`); nothing new appears in a memo. The proof-of-concept approval memo is `decision-memo.poc-approval.md`. All measured figures are from the plan's phase-1 evidence section, invented for this trial and labelled so.

**Decision requested:** build the guided product recommendation for production on all self-serve starts, hosted by the platform team, after G09 delivers observability, a release gate and the retention rule.
**Deadline for the decision:** 6 November 2026 (W4); G09's 30 to 60 hours and the platform team's hosting sign-off wait on it.
**Owner:** the AI engineer, for the Director of SMB Sales (sponsor).

## What we found

Product-choice completion rose from the 62% baseline (funnel export, Q3 2026) to 70.8% on 312 treated sessions, 10 to 23 October 2026, against 63.1% on 298 control sessions in the same weeks (plan, G06/A2); we estimate the margin from chance at about 5.7 points on 312, so the lift is above it, though no significance test was run. Refunds were unchanged at 3.0%, 2 of 67 orders (plan, phase 1 evidence). The 30-case offline set showed zero out-of-region recommendations and the advertiser's actual product among the recommendations in 77% of cases against the agreed 70% (G04/A1, G04/A2). Model and cloud spend was $142 for the phase, build runs included; developer hours 58 against 31.5 to 57 estimated. Not run: G06/A3, the switch-off without a deploy. Not measured: latency, tokens and the live-only cost per start (no traces in the pilot); escalations per week.

## Options

| Option | What it means | Cost (hours, money) | Risk | Recommendation |
| --- | --- | --- | --- | --- |
| A. Build for production, all starts | G09: observability, release gate, retention rule, hosting sign-off; go-live in December | 30 to 60 developer hours (estimate); about $330 a month model and cloud (estimate from $142 over 312 sessions, upper figure) | The switch-off has not been exercised (dry run in G09); cost per start not separated from build spend | Recommended because three of three criteria were met above the margin and every contract has a passing test |
| B. Extend the pilot one quarter at 50% | Same build, larger sample | Same running cost; no build hours | Revenue effect delayed a quarter; no owner for operations | |
| C. Stop | Keep the code, the 30-case set and the findings | None | Product choice keeps losing 38% | |

## If approved

- **Scope:** G09 (plan, phase 2): traces and cost per start, evaluation gate in CI from the 30 cases, retention rule for the logged sentence, credential rotation, runbook and alerts, dry run of the switch-off; the platform team names an on-call owner. Nothing new for the model to do; a person still confirms every purchase.
- **Success criteria for the next review:** completion above 62% over the first production quarter on all starts, from the funnel export; refunds at or under 4%; cost per start at or under the $0.46 estimate (proposed, not yet agreed); the release gate blocking a release that fails D6.
- **Kill criteria:** refunds above 4% switch the recommendation off; completion at or below 62% over the quarter ends production.
- **Next review:** results review after one quarter in production, business and technical (G10).

## Decision record (filled after the meeting)

| Decision | Owner | Date | Conditions |
| --- | --- | --- | --- |
| Option A approved: build for production on all starts (invented, recorded at stage 6) | Director of SMB Sales; platform team lead signed off hosting | 6 Nov 2026 (invented) | G09 delivers the gate, traces and the retention rule before go-live; on-call owner named |

Open questions raised, with who answers each and by when: retention of the logged sentence (platform team, before go-live); on-call owner (platform team lead, before go-live); escalations measure (product owner, first production month).
