---
stage: production-approval
audience: technical
minutes: 30
title: Campaign assistant: what was built, what was measured, what the platform team would inherit
sources: docs/discovery/campaign-assistant.md, docs/architecture/campaign-assistant.md, docs/plans/campaign-assistant.md
decision: Agree to host the campaign assistant in production for single-business advertisers once G03/A3 and G04/A2 pass and the G05 work (observability, budgets, CI evaluation) is estimated and owned
decider: Platform team lead (hosting and on-call); production funding decided by the Director of SMB Sales on 30 October 2026
date: 2026-10-30
---

## Campaign assistant: the proof of concept against its design, the evidence, and the work production needs
Covers: title
Notes: This is the technical session. No persuasion: the design, the contracts, the plan's evidence sections and the gaps, all by path. The question for this room is whether you would host and be paged for this, and what has to exist first.

---

## Eight of ten acceptance cases passed once; two were not run; production needs observability, budgets and a CI evaluation set that do not exist yet
Covers: summary
Evidence: docs/plans/campaign-assistant.md G01 to G05; G03/A3, G04/A2; docs/architecture/campaign-assistant.md deferred controls; measured
Notes: Three sentences. The build matches the design with no recorded deviations. Eight of ten acceptance cases passed, each run once by hand, with no repeats; two were never run, and one of them is the only test of the idempotency contract. Everything in the deferred-controls table is still deferred, so what you would inherit today has no alerts, no runbook and no evaluation set in CI.

- Build `poc-0.3` (commit 4f2e1c9) measured 10 to 23 October 2026 (plan G04)
- 8 of 10 acceptance cases passed, run once each, no repeats; G03/A3 and G04/A2 NOT RUN
- Deferred and still absent: observability, on-call runbook, per-session budgets, CI evaluation set (design deferred-controls table)

---

## What was built matches the design: one agent, three tools, Cloud Run behind the portal identity; no deviations are recorded
Covers: architecture
Evidence: D1, D3, docs/architecture/campaign-assistant.md system paragraph; docs/plans/campaign-assistant.md G01 to G03
Notes: Deviations are listed, not implied, and the plan's evidence sections record none. One `LlmAgent` with `list_eligible_products`, `get_quote` and `create_order`. Identity comes from the portal's session header; the agent holds no credentials. Session state carries the current quote ID and the confirmation flag. Say that "no deviations recorded" means the plan did not record any, not that someone audited the diff; that audit is a G05 item if you want it.

- Design: docs/architecture/campaign-assistant.md (D1 one agent, three tools; D3 Cloud Run, portal identity header)
- Deviations recorded in the plan's evidence sections: none
- Not done: an independent diff of code against design

---

## Evaluation results: 8 of 10 acceptance cases passed, each run once by hand; there is no evaluation report beyond the plan's evidence sections
Covers: evidence, criteria-results
Evidence: G01/A1, G01/A2, G02/A1, G02/A2, G03/A1, G03/A2, G04/A1, G04/A3; docs/plans/campaign-assistant.md; measured
Notes: Quote the figures by goal. The evidence lives in the plan file and one log file; there is no separate evaluation report and no variance because nothing was repeated. The business-outcome cases G04/A1 and G04/A3 were measured by Analytics and finance, not by the developer.

| Case | Checks | Result | Sample |
| --- | --- | --- | --- |
| G01/A1 | only rights-filtered products named (C1) | passed | 20 advertisers, 4 regions; log `evidence/g01-a1.json` |
| G01/A2 | ineligible request refused and redirected | passed | 5 of 5 |
| G02/A1 | stated price equals signed quote (C2) | passed | 40 of 40 quotes |
| G02/A2 | "give me a discount" alters nothing | passed | 10 of 10 |
| G03/A1 | `create_order` refused without confirmation token (C3) | passed | 8 of 8 |
| G03/A2 | order matches confirmed quote | passed | 8 of 8 |
| G04/A1 | completion at or above 34% on at least 300 sessions | passed, 36% (112 of 312) | portal analytics, 10 to 23 October 2026 |
| G04/A3 | refunds at or below 3% | passed, 3% (3 of 112) | finance export, 24 October 2026 |

- Repeats: none; trajectory and response checks: by hand, not scripted
- Deviation from the evaluation plan: no scripted evaluation set exists

---

## Two cases not run: the C4 idempotency path has never been exercised, and the quote-expiry requote (D5) has never been triggered
Covers: learned
Evidence: G03/A3, G04/A2, R2, D5; docs/plans/campaign-assistant.md
Notes: Full sentences with consequences. G03/A3: a repeated confirmation after a network retry should return the first order because the checkout service keys orders on the quote ID; the sandbox could not simulate the retry, so the key is implemented and unexercised, and the consequence of a defect is a duplicate order and a refund. G04/A2: the thirty-minute quote expiry was never hit in the live window and no synthetic case was written, so an expired quote reaching `create_order` is untested; the consequence is a stale-price order. Both are root-cause "not tested", not "failed".

- G03/A3 NOT RUN: idempotency key = quote ID at the checkout service (C4); sandbox cannot simulate a retry; consequence of a defect: duplicate order, refund
- G04/A2 NOT RUN: expired quote must be requoted before confirmation (D5); no live session hit expiry; no synthetic case; consequence: stale-price order
- Failure analysis of passed cases: no failures recorded, so no failure-mode counts exist

---

## The demo is build poc-0.3 and the numbers cover build poc-0.3; the demo runs on the same inputs only where it uses the test advertisers
Covers: evidence
Evidence: docs/plans/campaign-assistant.md G04 (build measured); G01/A1 (test advertisers)
Notes: Same build, commit 4f2e1c9. The live numbers come from real advertisers in the measurement window; the demo uses the twenty test advertisers from G01, so the demo shows the same code on different inputs. Say that sentence exactly.

- Measured: `poc-0.3`, commit 4f2e1c9, live advertisers, 10 to 23 October 2026
- Demo: `poc-0.3`, same commit, the 20 G01 test advertisers

---

## Measured cost: $142 model and cloud for the whole project; per-session, latency and token figures were not measured
Covers: cost
Evidence: docs/plans/campaign-assistant.md cost record; G04/A1; estimate
Notes: The only spend figure in the record is the billing total for the project, which covers build and measurement together. Dividing it by the 312 assisted sessions gives about forty-six cents a session as an upper bound; that is an estimate by arithmetic, not a per-session measurement. There are no traces, so no p95 latency and no tokens per turn; observability is a deferred control. Production cost per month is not estimated.

- We measured: $142 model and cloud, Cloud Billing project `campaign-poc`, 15 September to 24 October 2026; 58 human hours
- We estimate: about $0.46 per assisted session ($142 ÷ 312; includes build-time spend)
- Not measured: p95 latency, tokens per turn, cost per conversation from traces; not estimated: cost per month at full adoption (G05)

---

## Production architecture changes: everything in the deferred-controls table, plus agency exclusion at the identity boundary
Covers: architecture, production-scope
Evidence: docs/architecture/campaign-assistant.md deferred controls and open decision; docs/plans/campaign-assistant.md G05; R3
Notes: Phase 2 decisions are not made yet; this slide lists what the design says must be brought forward, by name, and the one open decision. Hosting stays Cloud Run unless this room says otherwise; memory stays session state; identity stays the portal header, with agency logins refused at that boundary until delegation exists in the rights service.

- Bring forward: observability, alerts and an on-call runbook; per-session token and invocation budget; evaluation set in CI with repeats
- Identity: refuse agency logins at the portal header until the rights service has a delegation model (open decision, owner Ad Products lead)
- Not in scope: Model Armor on creative text (the agent does not read uploads)
- Hosting, memory and model pin: unchanged from the design unless this review decides otherwise

---

## Contracts your services depend on: four contracts, three with a passed case behind them, one (C4) untested
Covers: contracts
Evidence: C1, C2, C3, C4, docs/architecture/campaign-assistant.md contracts table; G01/A1, G02/A1, G03/A1, G03/A3
Notes: The contracts table by path, with the enforcement point and the evidence. The pricing service owns the signed-quote format; the rights service owns eligibility; the checkout service owns the idempotency key. Changes to any of these are changes to a contract and need the owner named here.

| Contract | Enforced where | Owner of changes | Evidence |
| --- | --- | --- | --- |
| C1 only eligible products shown | tool result shaping; `before_model_callback` strips unlisted names | Ad Products lead (rights service) | G01/A1 passed |
| C2 price only from the pricing service | signed quote; response check rejects any price not in the quote | Head of Pricing | G02/A1 passed |
| C3 purchase only after confirmation bound to the quote | `create_order` requires a confirmation token for the quote | checkout service owner | G03/A1 passed |
| C4 one confirmed purchase, at most one order | idempotency key = quote ID at the checkout service | checkout service owner | G03/A3 NOT RUN |

---

## Security and sensitive data: identity is the portal's header, the agent writes only orders, and none of this has an adversarial test
Covers: risks
Evidence: D3, docs/architecture/campaign-assistant.md floor and deferred controls; C3; assumption
Notes: What is proven and what is assumed. Proven by acceptance case: the agent cannot create an order without a confirmation token. Assumed, with no test: that the portal header cannot be forged by a client, that prompt injection through the advertiser's own messages cannot reach a tool call that matters, and that there is no runaway loop, since there is no budget. Those are G05 tests, and this room should say which must exist before hosting.

- Proven: no order without a confirmation token (C3, G03/A1); prices and eligibility never model-computed (C2, C1)
- Assumed, untested: portal identity header integrity (D3); injection via advertiser messages; no loop or budget control (deferred)
- Sensitive data: advertiser business details pass through the session; no SDP or Model Armor screening in the proof of concept (deferred; not in scope while the agent does not read uploads)

---

## Operations today: no alerts, no runbook, no on-call; the SLIs and who is paged are G05 decisions this room owns
Covers: operations
Evidence: docs/architecture/campaign-assistant.md deferred controls; docs/plans/campaign-assistant.md G05; n/a: nothing operational has been built, so there is nothing to cite beyond the deferral
Notes: Uncertainty in the title. There is no observability and the developer has been the only on-call. The questions for this room are which SLIs, which dashboards and who is paged, and the answer goes into G05 as owned items, not into this deck.

- Exists: nothing operational (deferred-controls table)
- Needed before hosting: SLIs (order creation success, quote relay errors), alerts, a runbook, a named on-call owner

---

## Release and rollback: the model is pinned in the plan, but there is no evaluation gate, no staged promotion and no joint rollback of prompt, model and schema
Covers: operations
Evidence: docs/architecture/campaign-assistant.md deferred controls (evaluation set in CI); docs/plans/campaign-assistant.md G05; assumption
Notes: Release engineering does not exist for the proof of concept. The record says the model is pinned and that a CI evaluation set is deferred. Everything else on this slide is a requirement we propose, labelled as such, not a thing that exists.

- Exists: pinned model (design paragraph); hand-run acceptance cases
- Proposed for G05 (assumption until estimated): evaluation gate in CI with repeats, staged promotion, rollback of prompt, model and tool schema together

---

## What your team inherits: one agent, three tools, ten acceptance cases, a design and a plan; the hours to make it operable are not estimated
Covers: production-scope
Evidence: docs/plans/campaign-assistant.md G05 and cost record; docs/architecture/campaign-assistant.md
Notes: The documents by path, the code by tag, the gap in hours. Fifty-eight hours built the proof of concept; the record holds no estimate for G05, and that estimate is the first thing this room should produce.

- Code: tag `poc-0.3`; documents: docs/discovery/campaign-assistant.md, docs/architecture/campaign-assistant.md, docs/plans/campaign-assistant.md; log evidence/g01-a1.json
- Built in 58 human hours; G05 hours: not estimated
- Skills needed for G05: ADK evaluation, observability on Cloud Run, release gating

---

## Decision: name the on-call owner, estimate G05, and run G03/A3 and G04/A2 by 13 November 2026, or say this cannot be hosted at that scope
Covers: ask
Evidence: G03/A3, G04/A2, G05; docs/presentations/campaign-assistant/decision-memo.md; estimate
Notes: Two options for this room. Option A, agree to host once the two cases pass and G05 is estimated and owned, with the Platform team lead naming the on-call owner and the estimate landing by 13 November; recommended because nothing measured argues against it and every gap is a named piece of work. Option B, decline to host until a CI evaluation set and adversarial tests exist, which pushes the funding decision back by the time those take. Stopping is the business review's option, not this room's.

- A. Host once G03/A3 and G04/A2 pass and G05 is estimated and owned; on-call owner named by the Platform team lead (recommended)
- B. Decline until CI evaluation and adversarial tests exist; funding decision waits
- Date for the G05 estimate and the two cases: 13 November 2026 (estimate); funding decision: Director of SMB Sales, 30 October 2026

---

## Appendix: answers from the record to the questions this room will ask
Covers: questions
Evidence: docs/plans/campaign-assistant.md; docs/architecture/campaign-assistant.md; G03/A3
Notes: Read only when asked.

- Which cases cover the worst failure modes and how many times were they run? C4 duplicate order: G03/A3, run zero times. Wrong price: G02/A1, run once on 40 quotes.
- Is the demo the same build as the numbers? Yes, `poc-0.3`, commit 4f2e1c9; different inputs.
- p95 latency, tokens per turn? Not measured; no traces (deferred observability).
- What stops a runaway loop or an injection? Nothing measured; budgets and adversarial tests are deferred.
- How do we roll back prompt, model and schema together? No mechanism exists; proposed for G05.
- Which model version is pinned and when is it retired? Pinned in the plan; retirement date not recorded.
- What deviated from the design? Nothing recorded; no independent diff.
