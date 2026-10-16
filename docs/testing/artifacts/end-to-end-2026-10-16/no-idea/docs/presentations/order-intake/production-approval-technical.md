---
stage: production-approval
audience: technical
minutes: 30
title: Order intake: what the pilot built, what it measured, and what hosting it needs
sources: docs/plans/order-intake.md (phase-1 evidence, invented, labelled), docs/architecture/order-intake.md (design, contracts C1 to C5, decisions D1 to D6), docs/discovery/order-intake.md
decision: The IT firm hosts order intake for all four queues from 25 January 2027 and provides a TMS test environment, Graph consent renewal and the paging path by 15 January
decider: External IT firm's service lead (name not given)
date: 2026-12-11
---

## Order intake: what the pilot built, what it measured, and what hosting it needs
Covers: title
Evidence: n/a: title slide
Notes: This session is for the people who will host and be paged for this system. The pilot passed eleven of twelve acceptance cases; the twelfth needs a TMS test environment only you can provide. No persuasion here: every figure links to the plan line it came from.

---

## 11 of 12 acceptance cases passed; production needs a TMS test environment, an alert and a pinned release
Covers: summary, criteria-results
Evidence: docs/plans/order-intake.md G02 to G06 acceptance lines (measured); G05/A4 NOT RUN; G08

- Passed: G02/A1 to A3, G03/A1 to A3, G04/A1 to A4, G05/A1 to A3, G06/A1 to A3
- Not run: G05/A4, lost TMS reply after approval (no test environment)
- Outcome on the pilot queue: 1.7 minutes per emailed order against 4.4 measured, 331 orders

Notes: Eleven of twelve, and the one not run is the case your team can make runnable. The outcome figure is here once so you know what the business is deciding on; the rest of this deck is the build, the tests and the operations.

---

## Built as designed: five components, no deviations in shape; two deviations in the record
Covers: architecture
Evidence: docs/architecture/order-intake.md §2 components, D1 to D6; docs/plans/order-intake.md G02 measure note, G03 O4

- Cloud Run (poller, extraction, approval page, writer); Firestore operation record; Vertex AI gemini-3.8-flash, australia-southeast1; Graph read-only; TMS credential in Secret Manager
- Deviation 1: the measure is elapsed queue time, not handling time (G02)
- Deviation 2: O4 closed for 20 customers only; 280 unchecked

Notes: Design document at docs/architecture/order-intake.md; the component list is section 2 and nothing was added or removed. The two deviations are in the record, not the code: the clock we measure on, and the customer-contract check that covered the largest twenty.

---

## Evaluation: 50 paired cases, one run, no repeats; per-field accuracy from 41 to 50 of 50
Covers: evidence, demo
Evidence: docs/plans/order-intake.md G04/A1 (measured, 21 Nov 2026, ADK 2.8.0, gemini-3.8-flash pinned)

| Field | Correct of 50 |
| --- | --- |
| Customer | 50 |
| Pickup address | 47 |
| Delivery address | 46 |
| Pallet count | 49 |
| Dates | 44 |
| Instructions | 41 |

- The recorded demo and the numbers are the same build (pilot build of 21 Nov); one run, variance not measured

Notes: Fifty paired emails and orders, one pass, no repeats, so there is no variance figure and the title says so. Dates and instructions are the weak fields and they match the live corrections on the next slide. The demo you will see is a recording of the same build that produced these numbers.

---

## Failure analysis: 47 live edits, 12 "enter manually", 3 "cannot extract" in the test set, one safety case untested
Covers: learned
Evidence: docs/plans/order-intake.md G06 (edits by field), G04/A1 (cannot extract), G05/A4 NOT RUN; measured

- Edits before approval, 331 orders: dates 19, instructions 15, addresses 9, other 4; all stored as correction cases
- "Enter manually" 12 of 331: invalid schema after one repair or two calls spent (C4, D6)
- "Cannot extract" 3 of 50 test cases: all lacked a delivery address
- G05/A4 not run: pending state and TMS lookup exist, untested

Notes: Root causes as far as the record goes: date formats in free text, and instruction fields that mix delivery notes with commercial chatter. The twelve manual entries are the contract working as written, not a fault. The untested case is the one we need your environment for.

---

## Cost per emailed order: USD 0.07 model, USD 0.10 all-in; latency and tokens per call not measured
Covers: cost
Evidence: docs/plans/order-intake.md G06 spend (billing export 7 Dec 2026, measured); latency: not measured, G08 adds traces; monthly: we estimate, arithmetic on the slide

- Measured: Vertex USD 23.40 for about 640 calls; Cloud Run and Firestore USD 11.10; 331 orders, two weeks
- Not measured: p95 latency, tokens per call; no traces in the pilot by design (deferred, G08)
- We estimate: about USD 230 a month at four queues (0.07 x about 2,900 orders, plus about USD 25 hosting)

Notes: The pilot ran without tracing on purpose, so there is no latency figure and the slide says not measured rather than guessing. Cost is from your own billing export. The monthly estimate assumes the other three queues look like the pilot queue; the first production bill replaces it.

---

## Production changes: traces, a missed-mail alert, a release manifest with pinned model and prompt, all four queues
Covers: architecture, production-scope
Evidence: docs/plans/order-intake.md G08 (16 to 24 hours, estimate); docs/architecture/order-intake.md §4 deferred-control table

- Observability: OpenTelemetry traces to Cloud Trace; alert when no mail is read for 60 minutes
- Release: manifest with model ID, prompt version and ADK pin; rollback is the previous Cloud Run revision
- Scope: all emailed orders in the shared mailbox; same Cloud Run service; no new components
- Identity and secrets unchanged: Graph read-only, TMS credential in Secret Manager

Notes: Nothing new in shape; the deferred rows of the design's depth table come forward. Four queues are the same mailbox read in full instead of one dispatcher's filter, so the change is a filter and the alert, not an architecture.

---

## Contracts your services will depend on: five invariants, each enforced in code you can read
Covers: contracts
Evidence: docs/architecture/order-intake.md §3 contracts table C1 to C5; tests: docs/plans/order-intake.md G02/A1, G05/A2 to A4, G04/A2 to A3

| Contract | Invariant | Enforced where | Test |
| --- | --- | --- | --- |
| C1 | timestamps per order | poller, writer | G02/A1 pass |
| C2 | write only from a payload-hash approval | approval handler | G05/A2, A3 pass |
| C3 | one order per approval, pending reconciled | writer, Firestore record | G05/A4 NOT RUN |
| C4 | validated schema or "enter manually" | extraction boundary | G04/A2 pass |
| C5 | pinned model, region, no email in logs, 2 calls | Runner config, quota | G04/A3, G03/A1 pass |

Notes: Five contracts, four proven, one waiting on your environment. The TMS API sees one create call per approval keyed by message ID; if you change the API's response shape or timeouts, C3 is the contract that notices.

---

## Security and data boundaries: four tests passed, one contract question open; email text never reaches logs
Covers: risks
Evidence: docs/plans/order-intake.md G05/A3 (injection), G04/A3 (logs, call cap), G03/A1 (readback), G03 O4 open; docs/architecture/order-intake.md C5, D2

- Injected instruction in an email produced a draft and no write (G05/A3); the reader holds no TMS credential (D2)
- No email text in logs; at most 2 model calls per email; quota at USD 300 (G04/A3, C5)
- Readback of model, region and credential names without values (G03/A1)
- Open: customer data terms for 280 of 300 customers (O4); owner the operations director; consequence if a clause is found: that customer's mail is routed to manual entry

Notes: Risk as threat, control, test, and what is still open. The open item is contractual and has an owner and a consequence written down. Model Armor and Sensitive Data Protection were not in the pilot and are not in the production scope; the design's floor is the call cap, the log policy and the reader-writer split.

---

## Operations: one alert within the hour, your on-call paged for mail and TMS, rollback by revision
Covers: operations
Evidence: docs/plans/order-intake.md G06/A2 (missed-mail drill, 40 minutes), G08; docs/architecture/order-intake.md §5 failure review

- Alert: no mail read for 60 minutes, or Graph permission revoked; the page shows "mail paused"; your on-call is paged (owner to name)
- TMS unavailable: approvals queue as pending, retried, visible; reconciled by lookup (C3)
- Vertex unavailable: "enter manually"; nothing lost; no page
- Release: manifest pinned; rollback to the previous revision; the 50 cases and the 47 corrections rerun on any model or prompt change

Notes: Three failure rows from the design, each with what the dispatcher sees and whether anyone is paged. The one drill we ran showed the backlog on the page in 40 minutes without an alert; the alert is what production adds. We need a name for who receives it.

---

## Decision: we need a TMS test environment, Graph consent renewal, a paging owner and the hosting agreement by 15 January
Covers: ask, production-scope
Evidence: docs/plans/order-intake.md G03 (12-day lead time), G05/A4, G08; dates proposed, not yet agreed

- By 15 January: TMS test environment (to run G05/A4); Graph consent renewal owner; on-call name for the alert
- By 22 January: hosting under your existing contract at about USD 230 a month (estimate); Secret Manager and quota ownership
- What you inherit: one Cloud Run service, a Firestore collection, a runbook (to be written in G08), 50 test cases plus corrections

Notes: Four things with dates, chosen because access took twelve days last time. If the test environment cannot exist by mid-January, the alternative is a scripted timeout against a staging copy of the TMS, which you would need to tell us is possible. Credit: the contractor built it; your team gave access and confirmed the region.

---

## Appendix: the technical questions we expect, answered from the record
Covers: questions, appendix
Evidence: docs/plans/order-intake.md G04, G05, G06; docs/architecture/order-intake.md D1, D4, D6, §5

- Worst failure modes covered: injected instruction (G05/A3), malformed output (G04/A2), repeated click (G05/A4 not run); each run once
- Demo same build as the numbers: yes, pilot build of 21 Nov
- Identity: Graph read-only on the mailbox; the model writes nothing; the writer runs only from the approval handler (D2)
- Runaway loop: no agent loop; max_llm_calls 2 per email (D6)
- Rollback: previous Cloud Run revision; prompt and model in one manifest (G08)
- Pinned model: gemini-3.8-flash, stable, no retirement date in the lifecycle table checked 8 Oct 2026 (D4)
- p95 latency, tokens per turn: not measured; G08 traces

Notes: Held for questions. Unknowns are answered as "not measured" with the goal that measures them.
