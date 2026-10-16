# Order intake from email: system design (proof of concept)

Status: **draft**; provisional where marked. Source: docs/discovery/order-intake.md (brief, 15 Oct 2026). Compact form: design and plan summary in one file; goal detail in docs/plans/order-intake.md.

## 1. Constraints and profile

Profile: proof of concept, one contractor, four weeks, live emails on one dispatcher's queue, a person before every write.

| Scope-gate question | Answer (status) |
| --- | --- |
| Deadline and continuation | CEO go-ahead 5 Nov 2026; four weeks after; one team for a year if it works (confirmed) |
| Builder | One contractor, Python, some GCP, new to ADK, ~30 h/week (invented, user) |
| Money | A few hundred dollars for the trial; no monthly figure yet (user); spend stop at USD 300 assumed, sets D6 |
| Users and judge | Four dispatchers use it; the operations director judges on minutes per order; the CEO reads a measured report (confirmed) |
| Data and effects | Reads the shared orders mailbox (Microsoft 365, assumed, IT firm confirms; sets D4); writes one TMS order per approval; never contacts a customer (confirmed) |
| Reviews | POC approval 5 Nov (business); POC review after week four (business); results review after production (business); no technical audience, no platform team (confirmed) |

Assumed: TMS API can create orders and the IT firm grants a credential within week one (open decision O1); Vertex AI with gemini-3.8-flash is available in australia-southeast1 (O2, verify before G04); past emails pair with TMS orders for a 50-case evaluation set (O3).

## 2. Journey and shape

A customer emails "3 pallets Smithfield to Albury, pick up Thursday" to the mailbox. Today a dispatcher reads it, phones for gaps and re-keys customer, addresses, pallets, dates and instructions into the TMS (about 4 minutes, estimate). After: a poller reads new mail, one model call returns the fields as a fixed schema or a "cannot extract" result, the dispatcher sees draft beside email, fixes or approves in one click, and ordinary code creates the TMS order and records the timestamps.

The model decides only what the email says; code controls everything else: which mail is read, that a draft is shown and not acted on, that an approval is bound to the exact payload, that one approval writes one order, and the spend stop. There is no agent loop and no tool for the model: an `LlmAgent` with `output_schema` and no tools, run once per email through the application's `Runner`.

Components: Cloud Run service (poller, extraction, approval page, TMS writer); Firestore (operation record per email: message ID, draft, approval, TMS order ID, timestamps; provisional, cheapest durable store); Vertex AI gemini-3.8-flash (stable, no retirement date in the lifecycle table checked 8 Oct 2026); Microsoft Graph read-only mailbox permission; TMS API credential in Secret Manager. The extraction code path holds no TMS credential; the writer runs only from the approval handler.

## 3. Contracts and decisions

Requirements: R1 the measure is observable (confirmed); R2 no TMS order without a dispatcher's approval (confirmed); R3 wrong orders no more frequent than baseline (confirmed); R4 customer data stays within agreed boundaries (open, O4); R5 spend bounded (floor).

| ID | Invariant and scope | Enforced where | Check |
| --- | --- | --- | --- |
| C1 (R1) | Every emailed order on the pilot queue has mailbox-received and TMS-created timestamps in the operation record | Poller and writer, code | G02/A1 offline; weekly report |
| C2 (R2) | A TMS order is created only from an approval bound to the hash of the exact payload shown; a changed draft needs a new approval | Approval handler, code the model cannot reach; rechecked at write | G05/A2, A3 offline |
| C3 (R2, R3) | One approval creates at most one TMS order, keyed by message ID; an unknown write outcome is shown as pending and reconciled by TMS lookup | Writer with durable operation record | G05/A4 offline, G06 live |
| C4 (R3) | Fields reach the dispatcher only as a validated schema; prose or invalid output after one repair becomes "enter manually", never a draft | Extraction boundary, code | G04/A2 offline |
| C5 (R4, R5) | Email content goes only to the pinned model in the chosen region and never into logs; at most 2 model calls per email; project quota stops calls at the ceiling | Runner config, log policy, project quota | G04/A3 offline; G03 live readback |

Decisions (requirement, contract, choice, tradeoff, check):

- D1. R1 to R3; C4. One `LlmAgent` with `output_schema` and no tools, instead of an agent with mailbox and TMS tools. Tradeoff: no multi-step reasoning, which the step list does not need. Check: G04/A1 on 50 paired cases.
- D2. R2; C2, C3. Reader and writer split: the extraction path holds no TMS credential; the writer is ordinary code behind the approval handler. Tradeoff: one more component. Check: G05/A3 (injected instruction in an email never produces a write).
- D3. R1; C1, C3. Firestore operation record per message, provisional over Cloud SQL (no fixed cost, enough for 900 docs a week). Tradeoff: no relational reporting; export weekly to a sheet. Check: G02/A1.
- D4. R4; C5. Vertex AI, gemini-3.8-flash pinned, australia-southeast1 (provisional; O2) over the Gemini API, for data location and the IT firm's existing Google Cloud billing. Tradeoff: Vertex retirement calendar must be watched. Check: G03 live readback of region and model.
- D5. R1; C1. Weeks one and two run in shadow mode: timestamps recorded, no drafts shown, so the baseline is measured on the same clock. Tradeoff: two weeks before dispatchers see anything. Check: G02/A2.
- D6. R5; C5. `RunConfig.max_llm_calls=2` per email and a Vertex quota sized to USD 300 for the trial (assumed ceiling). Tradeoff: a quota outage during a burst; emails then queue for manual entry. Check: G04/A3.

## 4. Floor, depth and deferred

| Concern | Depth now | Trigger to deepen |
| --- | --- | --- |
| Secrets | Secret Manager, none in source or prompts (floor) | None |
| Spend stop | max_llm_calls and project quota (floor) | Monthly bill before all four queues |
| Approval before write | 100% of orders, payload-bound (floor) | Never removed; sampling only after a measured corrected-order rate |
| Personal data | Live emails, scoped to the pilot queue, out of logs (floor) | Customer contract check (O4) before scaling |
| Observability | Weekly export of the operation record | Any second queue: traces and an alert on missed mail |
| Evaluation | 50 paired cases offline, rerun on any model change | Production: cases refreshed from corrections |
| Release | Pinned model, single Cloud Run revision | Production: manifest, canary, rollback |

Graduation conditions: measured minutes per order under the agreed target with corrected orders flat; O1 to O4 closed; missed-mail alert in place; the IT firm accepts the runbook.

## 5. Failure review (rows the journey touches)

| Integration | Unavailable or slow | Rejects | Write outcome unknown | Untrusted content |
| --- | --- | --- | --- | --- |
| Mailbox (Graph) | Poller retries next minute; backlog visible on the page (G06/A2) | Permission revoked: page shows "mail paused", IT firm paged (G06/A2) | n/a: read only | Injected text is data; the reader has no tools (G05/A3) |
| Vertex model | Draft marked "enter manually" after 2 calls (G04/A3) | Same (G04/A3) | n/a: no write | Invalid schema handled by C4 (G04/A2) |
| TMS API | Approval queued, retried, visible as pending (G05/A4) | Shown to dispatcher with the TMS reason (G05/A4) | Pending; reconciled by TMS lookup on message ID (G05/A4) | n/a: structured response |

Action "create TMS order": wrong target or stale confirmation is refused by the payload hash (G05/A2); repeated click is absorbed by the operation record (G05/A4).

## 6. Plan summary, open decisions and next prompt

Phase 1 (about 46 to 60 contractor hours of ~120 available; fits with reserve): G01 POC approval presentation; G02 baseline shadow mode, two weeks; G03 access and 50 paired samples (IT firm); G04 extraction call and offline evaluation; G05 approval page and TMS writer; G06 live pilot on one queue, two weeks; G07 POC review presentation. Phase 2: G08 all four dispatchers with observability and release controls; G09 results review presentation. Later: phone orders (trigger: email share measured); customer order forms (process change, operations director); case study.

Open decisions: O1 TMS API write and credential (IT firm, week one); O2 model and region availability (contractor, before G04); O3 paired samples retained (IT firm); O4 customer data terms for a cloud model (operations director). Next prompt:

```text
/adk-presenter Prepare the proof-of-concept approval presentation for a business audience from docs/discovery/order-intake.md, docs/architecture/order-intake.md and docs/plans/order-intake.md (goal G01). Fifteen minutes; the decider is the owner-CEO on 5 November 2026.
```
