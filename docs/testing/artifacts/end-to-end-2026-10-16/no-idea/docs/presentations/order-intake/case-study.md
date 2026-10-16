# Case study draft: A regional logistics firm cut dispatcher time per emailed order from 4.4 to 1.6 minutes with an order-reading assistant built with Google Gemini

Status: internal draft, not yet sent; to be sent to the Google Cloud account manager who serves the IT firm's billing account (name not given) once the executive sponsor, the IT firm and the firm's own reviews below are done. The pack is an ask to be routed to customer reference marketing, not a submission.
Attribution phrase: Built with Google Gemini (one Gemini model through Vertex AI; no implementation guidance from Google)
Sources: docs/plans/order-intake.md (G02, G04 to G06, G08, G09; evidence invented and labelled for the trial), docs/architecture/order-intake.md, docs/discovery/order-intake.md

Every number cites its evidence line; every quote carries its approval status; every sentence naming a Google product uses plain text or the attribution phrase. Sentences marked `[draft]` are not yet approved by the sponsor. The customer, the IT firm and the firm's customers are unnamed until each consents.

**Subtitle:** Four dispatchers re-typed about 900 orders a week from free-text emails into the transport management system; a reading assistant now drafts each order for one-click approval, and an emailed order takes 1.6 minutes of dispatcher time instead of 4.4.

## Results

| Result | Before | After | Window | Sample | Method | Evidence | Publishable |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Dispatcher time per emailed order (median) | 4.4 min (one queue, 9 to 22 Nov 2026) | 1.6 min (four queues) | 25 Jan to 25 Apr 2027 | 8,640 emailed orders (baseline 318) | mailbox-received to TMS-created timestamps, weekly export | G02; G09 outcome | as is (sponsor to confirm) |
| Orders corrected at dispatch review | 2.8% | 2.9% | same | 8,640 (baseline 318) | planner's review flags | G02; G09 outcome | as is |
| Emailed orders through the approval screen | n/a | 94% | same | 8,640 | operation record | G09 adoption | as is |
| Model and hosting cost | USD 230 a month estimated | USD 221 a month, USD 0.077 an order | Feb to Apr 2027 | three bills | billing export | G09 cost | as a range ("about USD 200 to 250 a month") |
| Incidents | n/a | 2 medium, no order lost | same | 13 weeks | IT firm incident notes | G09 incidents | no (internal only) |

The public version shows the first four rows; the cost row as a range.

## About the customer

A regional pallet and parcel carrier serving about 300 business customers in one region, with 120 trucks and 40 office staff (docs/discovery/order-intake.md §1; figures invented for the trial). Orders arrive by email and phone into a four-person dispatch team and are planned weekly against the fleet.

## The challenge

Customers emailed orders in about 300 formats: "3 pallets Smithfield to Albury, pick up Thursday". A dispatcher read each one, phoned for missing details and re-typed five groups of fields into the transport management system. The operations director estimated 4 minutes an order and about 60 hours a week across four dispatchers, but nothing in intake was measured: not the time, not the orders corrected at review, not the wrong-place deliveries (docs/discovery/order-intake.md §2).

Earlier attempts fell short in two ways. One dispatcher had started pasting emails into a consumer chatbot to draft replies, which solved nothing because the replies were never the problem; the re-typing was (§1). And the transport management system's vendor sold no email-intake feature (G03). The first step was therefore to measure: two weeks of shadow mode put mailbox and TMS timestamps on every emailed order and gave a baseline of 4.4 minutes on 318 orders (G02).

## The solution

In the dispatchers' words: the email and a draft order sit side by side; you read one against the other, fix what is wrong, and approve; the order appears in the system; you still phone when something is missing. `[draft]`

The components, built by one contractor in about 90 hours over the pilot and the production step (G06, G08): a poller reads the shared orders mailbox through a read-only permission; one Google Cloud Agent Development Kit (ADK) `LlmAgent` with a fixed output schema and no tools, running Gemini through Vertex AI in the firm's chosen region, returns the order fields or "cannot extract" (D1, D4); the approval page shows draft beside email; ordinary code behind the approval handler creates one TMS order per approval, bound to a hash of the exact payload approved (C2, C3); a Firestore record per email holds the draft, the approval, the order ID and the timestamps; the service runs on Cloud Run with the TMS credential in Secret Manager. The model decides only what the email says; code controls which mail is read, that a draft is never acted on without approval, that one approval writes one order, and the spend stop of at most two model calls per email (C5, D6).

Guardrails and human approval: a dispatcher approves 100% of orders before creation; the planner's weekly review stays as a second check; email content never enters logs; the model path holds no TMS credential (D2). Evaluation: 50 past emails paired with their TMS orders, scored per field before go-live (G04/A1: customer 50 of 50, dates 44 of 50, instructions 41 of 50); every dispatcher edit is stored as a correction case and the set (50 plus 112 corrections by April) is rerun before any prompt or model change (G09 adoption).

Architecture diagram: one figure, to be drawn from docs/architecture/order-intake.md §2 with the trust boundary between the reading path and the writing path, scrubbed of hostnames, mailbox addresses and customer names before leaving the repository. `[draft: diagram not yet produced]`

## What changed

Over thirteen weeks on all four queues, the median dispatcher time per emailed order was 1.6 minutes on 8,640 orders, weekly medians between 1.3 and 2.4, against the 4.4 measured in shadow mode on one queue before anything changed (G02; G09). The counter-metric held: 2.9% of orders were corrected at dispatch review against 2.8% before, and wrong-place deliveries were 11 in the quarter, 0.13% (G09). All four dispatchers used it every week and 94% of emailed orders went through the approval screen; the rest were unreadable emails or, early on, a dispatcher who preferred typing until a second training hour (G09 adoption). Model and hosting cost USD 221 a month on average, USD 0.077 per emailed order, against an estimate of USD 230 (G09 cost).

What did not improve or is still being measured: the baseline was measured on one queue only, so the other three queues' before is assumed equal; complaints are counted firm-wide, not by queue, and did not move (55 to 63 a week, reported); the dispatcher hours freed (we estimate about 400 in the quarter, 2.8 minutes times 8,640) have not yet been reassigned, so no cost line has changed (G09). Two medium incidents, an expired mailbox permission and a two-hour TMS outage, were contained by the missed-mail alert and the pending state; 41 orders were typed by hand that morning and none were lost (G09 incidents; internal row, not for publication).

> "When an order email comes in now, the system has already read it; my job is to check it against what the customer wrote and press approve. The phone call for a missing pickup time is still mine." — Maria (surname withheld), Dispatcher. Approval: draft, not approved. `[draft]`

> "We measured for two weeks before we changed anything, and that is the only reason I can say what this did." — Operations Director (name withheld). Approval: draft, not approved. `[draft]`

## What's next

From the plan's later list (docs/plans/order-intake.md): a four-week discovery on phone orders, which are 27% of the four queues' orders (G09), approved on 6 May 2027; a structured order form for the five largest customers as a process change, owned by the operations director; no further build is promised. The system keeps its pinned model and prompt version, rerunning the evaluation set before any change (G08).

---

Industry: transport and logistics · Location: one region (country withheld until approved) · Products: Google Cloud Agent Development Kit (ADK), Gemini, Vertex AI, Cloud Run, Firestore, Secret Manager, Cloud Trace

## Submission pack (not published)

| Item | Status | Owner | Date |
| --- | --- | --- | --- |
| Relationship and Google contact | Unknown: the billing account is the IT firm's, so the agreement type (online terms or negotiated) and any Partner Advantage tier are the IT firm's to state; the Google account manager who contacted them is the route; no startup program | IT firm's service lead, with the operations director | ask by 20 May 2027 |
| Executive sponsor approval | Case study approved in principle by the owner-CEO on 6 May 2027 (invented); this draft not yet read by him | Operations director | 27 May 2027 |
| Legal review | Not started; the firm has no in-house counsel (ask who reviews; customer anonymity keeps customer contracts out of scope) | Owner-CEO to name | 3 Jun 2027 |
| Communications review | Not started; the firm has no communications function; the operations director reviews with the CEO | Operations director | 3 Jun 2027 |
| Security review of diagram and data flows | Diagram not yet drawn; the IT firm reviews it for hostnames and mailbox addresses | IT firm | 10 Jun 2027 |
| Numbers: publishable status per row | Proposed in the results table (three as is, cost as a range, incidents omitted); sponsor to confirm | Operations director | 27 May 2027 |
| Quotes: written approval | Two drafts, neither approved; Maria's needs her consent and the CEO's; media clearance not discussed | Operations director | 3 Jun 2027 |
| Attribution language chosen; wording lint passed | "Built with Google Gemini" chosen; the deck check's wording lint passed on the companion deck (case-study-public.md); no lint exists for this prose, reviewed by hand | Operations director | 2027-05-07 |
| Open asks for Google (logo, announcement, story, Next session, Marketplace) | requires Google consent: whether Google would produce the story; logo use for the firm's own site; no announcement, session or Marketplace interest (the system is not a product) | Google account manager via the IT firm | after the pack is sent |
| Derived assets: internal write-up, talk proposal, blog draft, one-pager, sanitised sample (CLA) | Internal write-up: the final-results deck (final-results-business.md); one-pager: the companion deck's summary slide; talk proposal, blog draft and sanitised sample: not planned unless Google asks; no CLA signed | Operations director | not planned |
| Timeline | Start 9 Nov 2026; pilot live 23 Nov 2026; production 25 Jan 2027; measurement window 25 Jan to 25 Apr 2027; publication target: none set until Google answers | Operations director | |
| Contacts | Spokesperson: operations director; technical lead: the contractor (availability to confirm); marketing owner: none (operations director); Google contact: the account manager via the IT firm; sent to: not yet sent | Operations director | |

Sponsor interview, 30 to 60 minutes, questions from the gaps above: why intake and not scheduling or disputes; what the dispatchers said in week one and in April; what she would tell another operations director about measuring first; what the freed hours will become; whether the firm's customers noticed anything; whether the firm would be named.
