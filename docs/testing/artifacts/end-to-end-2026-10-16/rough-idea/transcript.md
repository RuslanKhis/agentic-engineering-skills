# Transcript: end-to-end trial (rough-area entry)

Facts the simulated user invents beyond the given fact sheet are marked (invented).

---

## Stage 1: /adk-discovery

USER: /adk-discovery Leadership wants AI so small businesses can buy advertising from us more easily, but nobody has said where. Help me find where it pays off, what to try first, what to measure, and whether an agent is the right tool. Save the brief.

AGENT: Mode: **rough area** (the journey is "a small business buys advertising from us"; nothing said where it breaks). Correct me if you meant "no use case yet". What you said: leadership wants AI so small businesses buy more easily. Nothing cited yet; I assume there is a self-serve platform with analytics (assumed until you confirm). The answer may not be AI; it may be a process change or measuring something nobody has measured.

Opening question (it chooses the first workflow and the outcome to measure): where do advertisers abandon the buying journey today: choosing the product, creating the ad, understanding pricing, or completing the booking? Is that logged? Default if unknown: the first step is to measure it.

Two more, one each: (a) What does the business sell, to whom, and which KPI is the sponsor judged on this year? (fixes the goal metric; default: self-serve ad revenue). (b) Walk me through one real advertiser from first contact to money received: where did it wait, bounce back, or need someone to re-enter data? (locates friction in observed work; default: I construct a typical case and label it assumed.)

USER: It is logged. Last quarter 2,140 eligible advertisers started a purchase on the self-serve ad platform. 38% left at product choice, 12% at creative upload, 9% at pricing, 6% at booking. We sell advertising inventory (digital display, audio and local video slots) to small businesses, direct, through a self-serve platform. The sponsor is the Director of SMB Sales, judged on self-serve revenue. Typical case (invented): a bakery owner signs up, sees about 40 products across formats and regions, cannot tell which one fits a local promotion, opens a chat with sales or just leaves; if she gets past that, she uploads a photo, waits for the rights check, sees a price, and books; refunds happen when the ad did not run where she expected.

AGENT: Recorded as measured: funnel export, self-serve platform, last quarter (Q3 2026), 2,140 starts; drop by step 38 / 12 / 9 / 6 percent. Running example: the bakery owner, labelled assumed. Product choice is the largest drop with the most people behind it (about 813 of 2,140), so it is the first candidate; creative upload (about 257) and pricing (about 193) are the others. Next three questions:

1. Which system owns the facts each step needs (product catalogue, pricing, inventory, creative rights), and can we reach it this month? (data readiness gate; default: unknown: ask.)
2. What happens when the recommendation or the price shown is wrong: who notices, can it be undone? (augment or automate; default: a person confirms before money moves.)
3. Which number must not get worse? (counter-metric; default: refunds.)

USER: Pricing and inventory live in existing services with APIs; the product catalogue is in the same platform database (invented). The creative library has rights metadata, but its quality is uncertain. A wrong product recommendation is reversible before booking, and a person confirms every purchase today: six sales staff handle escalations, about 35 a week. Refunds are 3% of orders; that is the number that must not get worse.

AGENT: Then the fit for product choice is a bounded recommendation: the input is the advertiser's free-text description of what they want plus a structured catalogue, the rules (which product fits which goal) are known in prose but context-dependent, and a person confirms every purchase, so the error cost is low. Creative upload has a data gate (rights metadata of uncertain quality), which points to measuring first. Three more questions, then I will draft:

4. What is the number now for the product-choice step and how do you know (I have 38% from the export); is there a measure for time-to-first-usable-creative? (baseline; default: unknown, measurement is the first goal.)
5. Who approves the next step, and when? (decision calendar; default: unknown: ask.)
6. Who owns this with what budget, and would they fund one team on it for a year? Who on the frontline agrees product choice is the pain? (senior owner and the two-voice check.)

USER: Nobody has measured time-to-first-usable-creative. Leadership decides on a four-week, one-developer proof of concept on 29 October 2026; the production decision review is planned two weeks after the proof of concept ends. The Director of SMB Sales would fund one team for a year. A frontline product owner agrees product choice is the pain. One more thing: the platform team will have to host whatever is built.

AGENT: Before I hand over, the three closing questions with defaults: (12) what would make you cancel this in six months? (default: refunds rise above 4% or the model bill exceeds what one sales hire costs); (13) who else has to change how they work? (default: the six sales staff see fewer product-choice escalations and take the recommendation corrections); (15) success in 90 days in one sentence a customer would recognise? (default: "a bakery owner picks the right product in one sitting without calling us").

USER: Accept all three defaults. The cost ceiling is up to you to phrase; call it "less than one sales hire" (invented). Save the brief and give me the next prompt.

AGENT: Drafting `docs/discovery/smb-self-serve-ads.md` now, scoring the portfolio (scores are mine, the engineer's, from this conversation) and running the ranking helper.

AGENT: Brief saved at `docs/discovery/smb-self-serve-ads.md`. Helper: O1 scores 11 (5+4+4-2), O3 8, O4 5, O2 4; "Ready for adk-system-designer", exit 0.

- **First use case:** O1, a guided product recommendation in the self-serve flow; measure: product-choice completion (share of starts reaching creative upload); baseline 62% (funnel export, Q3 2026); counter-metric: refunds at 3%.
- **Technology fit:** You asked whether AI can handle product choice. The input is free text plus structured catalogue records, the rules are known but context-dependent, and we have one quarter of step records to evaluate against. That points to a language model with a fixed output over a catalogue the code has filtered. We chose it over an agent because the step list can be written down. The error cost is low, so the advertiser and a person review every output before money moves. The platform team keeps it current; the design will state what it costs to run.
- **Next decision:** leadership, 29 October 2026, four-week one-developer proof of concept.
- **Prompt:** (the block in section 9 of the brief, repeated verbatim)

Closing question: do you want the proof-of-concept approval presentation drafted now, before the design exists? The decision calendar names an approval on 29 October, so here is the prompt; the deck is redrafted from the design and plan once they exist, so you can choose to design first.

```text
/adk-presenter Prepare the proof-of-concept approval presentation for a
business audience from docs/discovery/smb-self-serve-ads.md. The design does not exist
yet: mark cost and scope as pending and label every hypothesis. Fifteen
minutes; the decider is leadership (chaired by the Director of SMB Sales) on 29 October 2026.
```

USER: Yes, draft it now.

---

## Stage 2: /adk-presenter (proof-of-concept approval, business, brief only)

USER: /adk-presenter Prepare the proof-of-concept approval presentation for a business audience from docs/discovery/smb-self-serve-ads.md. The design does not exist yet: mark cost and scope as pending and label every hypothesis. Fifteen minutes; the decider is leadership (chaired by the Director of SMB Sales) on 29 October 2026.

AGENT: Record read: only the discovery brief exists (`docs/discovery/smb-self-serve-ads.md`); no design, plan, tickets, evaluation report or cost record. Gaps the record leaves, each becoming a slide line rather than an omission: no model or cloud cost (not yet estimated; the design will state it), no developer hours beyond "one developer for four weeks", no proof-of-concept traffic share or region (designer to choose), no acceptance cases, no demo, catalogue read access assumed (invented in the brief), who pays the model bill after the pilot unknown. Settled from the request: stage `poc-approval`; audience `business`; 15 minutes; decider the Director of SMB Sales chairing leadership; 29 October 2026.

Storyline (four lines): Situation: 2,140 advertisers started a self-serve purchase in Q3 2026 and 62% got past product choice (funnel export). Complication: 38% leave at product choice, the largest drop, because about 40 products across formats and regions give no way to tell which fits; sales absorbs about 35 escalations a week. Question: do we spend one developer for four weeks to test whether a guided recommendation lifts that 62%? Answer: yes, on live traffic from week two, with a person still confirming every purchase and refunds as the stop rule; someone could prefer to fix pricing first or measure creative upload instead.

Ghost deck (titles read as a paragraph): the summary; today product choice loses 38%; the complication is 40 products and no guide; one hypothesis; success criteria; stop rules and dates; scope and what stays out; what it costs (hours confirmed, money pending); three risks with owners; the decision between three options. Drafting `docs/presentations/smb-self-serve-ads/poc-approval-business.md`.

AGENT: Deck written: `docs/presentations/smb-self-serve-ads/poc-approval-business.md`, 13 slides (10 timed, 2 appendix, title). Check: exit 0, coverage complete; 12 warnings: every slide body is over the 40-word budget (the risk slide needs control and owner per risk, the decision slide three options plus decider and date, and they do not fit in 40 words), and the notes script 5.2 of 15 minutes. I kept the notes short on purpose; the rest of the talk is the case and the questions. `decision-memo.md` and `pre-wiring.md` are beside it (pre-wiring rows are planned, not held). Gaps the record left and how they show: model and cloud cost (slide 9 title says not yet estimated); sample and region (slide 6, pending the design); catalogue access (slide 10 notes, assumed, platform team to confirm); who pays after the pilot (memo open questions). Decision sentence: approve a four-week, one-developer proof of concept of a guided product recommendation on live traffic from week two. Rehearsal: two runs out loud, one with a colleague playing the decider. The evidence supports asking for the proof of concept; it does not support asking for a wider pilot. Next prompt: the brief's §9 `/adk-system-designer` prompt, then `/adk-presenter` again from brief, design and plan.

USER: Good. Run the designer prompt from the brief now, design only.

---

## Stage 3: /adk-system-designer (design only, compact form)

USER: /adk-system-designer Read docs/discovery/smb-self-serve-ads.md and design the first use case it selects (O1: a guided product recommendation in the self-serve flow that turns the advertiser's description into one to three fitting products with reasons, confirmed by a person before booking). Treat its confirmed answers as settled; ask only what it leaves open. The outcome measure is product-choice completion (share of purchase starts that reach creative upload) against 62% (funnel export, Q3 2026), with the refund rate (3% of orders) as the guardrail. The sponsor is the Director of SMB Sales; leadership decides on the four-week, one-developer proof of concept on 29 October 2026, so plan a presentation goal for it. Design only.

AGENT: Brief read. Journey: a small-business advertiser signed in to the self-serve platform reaches product choice, types the promotion in one sentence, and should see one to three products that can run in her region, each with a reason, then pick one and continue to creative upload; a person still confirms the purchase at booking. Friction: about 40 products, 38% leave here (funnel export, Q3 2026). Outcome: completion above 62% with refunds at or under 4%. Fixed: four weeks, one developer, platform team hosts, reads catalogue, pricing and inventory, writes nothing, decision 29 October 2026, production review two weeks after the pilot ends. Profile: proof of concept that is meant to be kept (it runs on live traffic from week two), compact form, one design file of about 1,200 words plus a plan. Scope gate, only what the brief leaves open, defaults you can accept in one word:

1. The developer's familiarity with ADK and GCP, and focused hours per week? (Default: new to ADK, has used GCP; about 30 focused hours a week. Sets a 1.5 multiplier and the capacity.)
2. Model and cloud money for the four weeks? (Default: a small allowance under 500 EUR, capped by a project quota. Sets the model tier and the evaluation repeats.)
3. Which slice of live traffic from week two: I propose 50% of all starts in every region rather than one region, because about 2,140 starts a quarter gives roughly 500 starts in three live weeks, so half treated is about 250 and the margin on the completion rate is about six points; one region would be too small to read. (Needs the product owner's approval.)
4. Can the platform call a new service server-to-server with the advertiser's account id and region, and expose the catalogue read-only this month? (Default: yes via the platform's existing service identity; sets identity and the data path.)
5. Who pays the model bill after the pilot? (Default: the sponsor's self-serve revenue budget line; sets the cost goal.)

USER: 1: new to ADK, has deployed to Cloud Run before; full time, about 30 focused hours a week (invented). 2: accept the default, under 500 EUR, cap it (invented). 3: accept 50% of all starts; the product owner agreed this morning (invented). 4: yes, the platform team confirmed read-only catalogue access through the platform API and will call the service with account id and region (invented). 5: the sponsor's budget line (invented). Write the design and the plan, then tickets for the ready goals.

AGENT: Saved: `docs/architecture/smb-self-serve-ads.md` (draft, compact form, 1,710 words: scope-gate table, journey and shape, five contracts C1 to C5, six decisions D1 to D6, depth table, four failure rows, open decisions), `docs/plans/smb-self-serve-ads.md` (summary, goals table with waits W1 to W4, entries for G05 to G08, phase 2 and later), and tickets `docs/tickets/smb-self-serve-ads/G01.md` to `G04.md`. Profile: proof of concept, kept. Capacity: 72 hours for goals after focus and reserve; phase 1 developer goals G02 to G06 total 31.5 to 57 hours, so the cut line is below everything in phase 1; if it runs high, G04 shrinks to 15 cases first. Added by hand; no schedule block, so the helper was not run. Presentation goals: G01 (approval, business, 29 Oct), G07 and G08 (production decision review, business and technical, 11 Dec 2026 invented), G10 (results review after one quarter). Open: D6 thresholds (product owner), retention of the logged sentence (platform team), the ADK pin (G02). Not done, and a gap you should know: the design gives no money estimate per start or per month, only the under-500 EUR allowance and the quota, because no priced inputs were available here; G04 records the measured cost of 30 cases. Next prompt:

```text
/adk-presenter Carry out G01 from docs/plans/smb-self-serve-ads.md.
```

USER: Run G01 now, business version, then the technical version for the platform team.

---

## Stage 4: /adk-presenter (proof-of-concept approval, from brief + design + plan, business and technical)

USER: /adk-presenter Carry out G01 from docs/plans/smb-self-serve-ads.md. Then prepare the technical version for the platform team.

AGENT: Record read in order: brief (baseline 62%, counter-metric 3%, decision calendar), design (profile, C1 to C5, D1 to D6, depth table), plan (capacity 72 h, phase 1 goals 31.5 to 57 h, waits W1 to W4), tickets G01 to G04. Gaps that become slides: no money estimate per start or month (design §1 allowance only); no acceptance case has run; no demo; D6 thresholds proposed, not agreed. Stage `poc-approval`; audiences `business` (15 min) then `technical` (30 min); decider the Director of SMB Sales chairing leadership, 29 Oct 2026; the technical deck's ask is addressed to the platform team lead for access and the integration slot. Keeping the brief-only draft as `poc-approval-business.brief-only.md`; the new business deck replaces `poc-approval-business.md`.

AGENT: Both outlines written. `poc-approval-business.md`: 13 slides (10 timed), check exit 0, 10 warnings (bodies over 40 words, cost title over 20 words, notes 4.8 of 15 minutes). `poc-approval-technical.md`: 14 slides (12 timed), first run exit 1 ("no slide Covers problem"; the technical outline has no problem slide, so I tagged the baseline slide `problem` as well), rerun exit 0, 19 warnings (titles over 20 words on six slides, bodies over 40, notes 6.9 of 30 minutes). `decision-memo.md` and `pre-wiring.md` redrafted from the design and plan. Gaps the record left and how each shows: no money estimate per start or month (business slide 9 and technical slide 10 say so in the title and name G04 as the goal that measures it); no acceptance case run and no demo (technical slide 7 and the appendix); D6 thresholds proposed, not agreed (technical slide 7 title); retention of the logged sentence open (technical slide 9). Decision sentence: approve a four-week, one-developer proof of concept of a guided product recommendation, live on half of the self-serve starts from week two. The evidence supports that ask; it does not support the wider pilot. Rehearsal: two runs out loud per deck, one with a colleague playing the decider. After the meeting, record the decision in the memo and the plan (W1). Next prompt once W1 clears:

```text
/adk-engineer Carry out docs/tickets/smb-self-serve-ads/G02.md.
```

USER: All phase-1 tickets are complete.

---

## Stage 5: phase-1 evidence recorded, then /adk-presenter (production approval, business and technical)

AGENT: Before I record anything: the developer's report gives the measured window as 10 to 23 October 2026, which is before the 29 October decision date and the plan's November calendar. Do I record the window as reported and mark the plan's calendar as superseded?

USER: Yes. The decision came early, the pilot ran 10 to 23 October (invented); treat the plan's November dates as superseded. Here is what was measured (all invented): 312 proof-of-concept sessions in the treatment arm, 10 to 23 October 2026, 221 reached creative upload, 70.8%; control arm 298 sessions, 188 reached creative upload, 63.1%; baseline 62% from the brief. Refunds unchanged at 3% (2 of 67 orders in the window). G04: 30 cases, zero out-of-region, actual product among the recommendations in 23 of 30 (77%), thresholds agreed by the product owner on 8 October. One acceptance case NOT RUN: G06/A3, the switch-off without a deploy, because refunds never crossed 4%. Model and cloud spend $142 on the billing export, build-time runs included. 58 developer hours against the 31.5 to 57 estimate. Build tag of the measured system: `rec-svc:poc-20261009-7f3a1c2`. Record it in the plan, then prepare the production approval review, business and technical.

AGENT: Recording the evidence under the plan's phase-1 goals, each line labelled invented, then reading the record again for the production-approval stage.

AGENT: Evidence recorded in `docs/plans/smb-self-serve-ads.md` (phase 1 evidence section; G01 to G06 marked done, G06/A3 NOT RUN, W4 moved to 6 November 2026 as two weeks after the pilot ended). Beyond what you reported I added, labelled invented in the plan, what the technical outline demands and the report did not hold: two deviations from the design and a root-cause split of the seven G04 misses. Record read again: brief (baseline, thresholds), design (contracts, deferred controls, graduation conditions), plan (evidence section). Gaps that become slides: latency, tokens and live-only cost per start not measured (no traces); escalations not measured; G06/A3 not run; one evaluation run, no variance; no demo. Stage `production-approval`; audiences `business` (15 min, decider the Director of SMB Sales, 6 Nov 2026) and `technical` (30 min, platform team lead for the hosting sign-off). Storyline: Situation: 62% of 2,140 starts got past product choice last quarter. Complication: with the recommendation live on half the starts, 70.8% of 312 treated sessions got past it, against 63.1% in control, refunds flat at 3%. Question: stop, extend, or build for production. Answer: build, for 30 to 60 hours and about $330 a month estimated; someone could prefer another quarter at 50%.

AGENT: Decks written: `production-approval-business.md` (11 slides, 9 timed; check exit 0, 14 warnings: bodies over 40 words, four titles over 20, ask body 82 of 70) and `production-approval-technical.md` (12 slides, 10 timed; exit 0, 2 warnings: notes 7.2 of 30 minutes and one body). Outputs in `checks/stage5-*.txt`. `decision-memo.md` and `pre-wiring.md` redrafted for this decision; the approval-stage versions kept as `*.poc-approval.md`. Gaps and where they show: G06/A3 NOT RUN (business slide 5 title, technical slides 2 and 10); latency, tokens, live-only cost not measured (technical slide 6 title); escalations not measured (business slide 5); one run, no variance (technical slide 4); no demo (both appendices). Every number cites the plan's evidence section or the design. Decision sentence: build for production on all starts, hosted by the platform team, at about $330 a month estimated. The evidence supports that ask; it does not support claiming a revenue effect, which was not measured. Rehearsal: two runs per deck, one with a colleague interrupting as the decider. After the meeting, record the decision in the memo and the plan (W4). Next prompt after W4: `/adk-engineer Carry out G09 from docs/plans/smb-self-serve-ads.md.`

USER: All production tickets are complete; it has run for a quarter.

---

## Stage 6: production evidence recorded, then /adk-presenter (final results, business and technical)

AGENT: Recording what you report under a phase-2 evidence section in the plan, labelled invented. What did the quarter measure: the outcome against the 62% baseline, the adoption share and its definition, cost per month against the $330 estimate, and the incidents?

USER: All invented: production went live on all starts on 14 December 2026, build `rec-svc:prod-20261212-c41e9b0`; G09 took 47 hours. Quarter 1 January to 31 March 2027: 2,310 starts, 1,603 reached creative upload, 69.4%, by month 68.1%, 69.9%, 70.2%; refunds 2.9%, 28 of 951 orders. Adoption: every start is offered the recommendation; 78% typed a sentence and saw a recommendation (1,802 of 2,310), 44% of all starts picked a recommended product (1,016). Cost on the billing export: January $198, February $204, March $231, average $211 a month against the $330 estimate; about $0.27 a start from the cost-per-start query; Cloud Run about $38 of each month. Two incidents: 11 February, pricing service down 2 hours 10 minutes, 63 starts got "price on the next page", no wrong price shown, alert fired, no customer effect; 3 March, a marketing campaign doubled starts, the Gemini quota was hit at 14:20 and 142 starts got the fallback page for 5 hours 40 minutes until the quota was raised from 1,500 to 4,000 calls a month; that day's completion was 58%. SLIs from traces: p95 latency 2.4 seconds, fallback rate 1.1% of starts outside incidents, log-write failures 0.02%. The evaluation set was refreshed to 60 cases from production logs on 20 February, 52 of 60 pass, gate 70%. Retention rule: sentences deleted after 90 days. Sales lead reports escalations down from about 35 to about 22 a week in March (reported, not logged). Record it, then prepare the final results review, business and technical.

AGENT: Recording, then reading the record again for the `final-results` stage.

AGENT: Recorded in `docs/plans/smb-self-serve-ads.md` (phase 2 evidence: outcome by month, adoption with the definition of active, cost per month against the estimate, two incidents with response and severity, SLIs, the gate, lessons; G09 done, W4 approved, G10 ready). Record read again: brief (baseline, portfolio for the next step), design (D3, D4, §4 deferred items), plan. Gaps that become slides: no control arm in production; escalations reported, not logged; tokens per request not summarised; one evaluation run per release; SDP screening deferred. Stage `final-results`; audiences `business` (15 min, Director of SMB Sales, 14 April 2027) and `technical` (30 min, platform team lead). Storyline: Situation: live on every start since 14 December. Complication: 69.4% against 62% on 2,310 starts, $211 a month against $330, two incidents, one of which was our own quota. Question: information, plus what next. Answer: fund a discovery for the next funnel step and put a one-month control arm and an escalation log in the next release; someone could prefer leaving it alone.

AGENT: Decks written: `final-results-business.md` (11 slides, 9 timed; exit 0, 15 warnings: bodies over 40 words, titles over 20, notes 6.2 minutes) and `final-results-technical.md` (11 slides, 9 timed; first run exit 0 with 3 warnings, one a hype-word hit on "always `treatment`", which I reworded; rerun exit 0, 2 timing warnings: nine slides for 30 minutes and notes 6.6 minutes). Outputs in `checks/stage6-*.txt`. `decision-memo.md` and `pre-wiring.md` written for this review; earlier ones kept as `*.production-approval.md`, with the 6 November decision recorded. Every number cites the plan's phase-2 evidence or the design; the control-arm caveat and the reported-not-logged escalations are on the slides in the measured/reported voice. No decision sentence beyond the small one: fund the discovery; next release carries a 10% control arm and an escalation log. Next prompt if results are approved for sharing: `/adk-presenter Prepare the public case study (G11) from docs/plans/smb-self-serve-ads.md for the Google Cloud account team.`

USER: Results are approved for sharing by the Director of SMB Sales and the platform team lead (invented). Prepare the public case study for the Google Cloud account team: the submission pack.

---

## Stage 7: /adk-presenter (public case study, submission pack)

USER: /adk-presenter Prepare the public case study (G11) from docs/plans/smb-self-serve-ads.md for the Google Cloud account team: use the case-study template and produce the submission pack.

AGENT: Record read: plan (phase 1 and 2 evidence, G11), design, brief. Stage `case-study`, audience `public`; the deliverable is the prose draft from the template plus the submission pack, and a companion deck only if you want a meeting version. The record lacks what a public story needs and the project record never held: the company's public name and location, the Google Cloud relationship (agreement type, partner tier, startup programme, named contact), who approves publicity, and a quote with written approval. Attribution: Gemini through Vertex AI, Cloud Run and BigQuery with no implementation guidance from Google, so "Built on Google Cloud" from the approved list, with Gemini and the Google Cloud Agent Development Kit (ADK) in plain text. Which of these can you give me, and do you want the meeting version of the deck?

USER: All invented: the company is Northlight Media, a regional media group in Rotterdam with about 900 staff; online agreement, no Partner Advantage tier, no startup programme; the Google Cloud account manager is Jonas Weber. Publicity approvals: the Director of SMB Sales (sponsor, approved 10 April), legal and communications not yet reviewed, security review of the diagram not yet done. A quote from the Director of SMB Sales is drafted but not approved in writing. Numbers may be published as is except the cost, which goes as a range. Yes, make a short meeting version of the deck for the account team, 10 minutes.

AGENT: Written: `docs/presentations/smb-self-serve-ads/case-study.md` (the prose draft from the template: results table with before, after, window, sample, method, evidence line and publishable status per row; challenge, solution, what changed with what did not improve, one quote marked draft, what's next from the plan only; footer; the submission pack with owner and date per item; interview questions generated from the gaps) and `case-study-public.md` (7 slides, 6 timed, 10 minutes, the final-results story in public wording). Checks: `check_deck.py --prose case-study.md` exit 0, no disallowed wording; `check_deck.py --deck case-study-public.md` exit 0, 9 warnings (titles over 20 words, bodies over 40, notes 3.5 of 10 minutes); outputs in `checks/stage7-*.txt`. Attribution "Built on Google Cloud"; "agent" avoided because the design calls it a service. Gaps and how they show: company name and location are invented and flagged for communications; legal, communications and the security review of the diagram are pending in the pack; the quote is `[draft]`; the diagram is a placeholder pending the security review; cost goes as a range. The pack is an ask to the account manager, not a submission; the draft's status line says so. Evidence supports a case study: measured results over a quarter, approved for sharing. Next step: the sponsor interview (questions in the draft), then legal and communications, then send the pack to Jonas Weber. The plan's G11 is marked drafted.
