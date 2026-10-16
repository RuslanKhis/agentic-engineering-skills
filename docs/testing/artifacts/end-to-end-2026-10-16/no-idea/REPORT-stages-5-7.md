# Report: stages 5 to 7, "no use case" logistics firm

Project: scratchpad/e2e-noidea. Skills root: skills/ (S = that root; P = S/adk-presenter). Fresh agent, 16 Oct 2026, continuing after REPORT-stages-1-4.md. All phase-1 and production evidence is invented by the simulated user and labelled so in docs/plans/order-intake.md. Line numbers are from `cat -n` on the files as read. Check outputs are under docs/presentations/order-intake/checks/ (`*.first-run.txt` and the final run per deck).

## Stage 5: production approval (business for the CEO, technical for the IT firm)

**Skill files read, in order:** `P/SKILL.md` (148 lines); `P/references/storyline.md`; `P/references/stage-outlines.md` (production-approval section, 42-77); `P/assets/deck-format.md`; `P/assets/decision-memo-template.md`; `P/references/speech.md`; `P/references/audiences-and-questions.md`; `P/scripts/check_deck.py` (read in full to know the rules). Not read: `slide-craft.md` (no slide tool), `case-study.md` (stage 7). Project record re-read in the order `SKILL.md:38-46` prescribes: brief, design, plan, tickets.

**Evidence written into the plan (invented, labelled):** G02 baseline 4.4 minutes median on 318 emailed orders, 9 to 22 Nov 2026, 71% email share, corrected 2.8%; G06 live 1.7 minutes on 331 orders, corrected 3.0% (within the margin), wrong deliveries 1 and 1, complaints firm-wide unchanged, 47 edits by field, 12 "enter manually"; G05/A4 NOT RUN (no TMS test environment); G04 per-field accuracy on 50 pairs; spend USD 34.50 of 300 (model 23.40, hosting 11.10); hours: contractor 71 against 46 to 62, operations director 9, dispatcher 6; G03 the IT firm's access took 12 days, O4 closed for 20 of 300 customers.

**Friction log**
- `P/SKILL.md:44-46` says to read "tickets and their Evidence sections" and "any evaluation report, cost record or incident log the plan links". The designer's ticket files (`docs/tickets/order-intake/G0*.md`) have no Evidence section (only the run prompt says "fill in Evidence"), and the designer's plan format has no slot for results per goal (`SKILL.md:43` expects "evidence lines per contract" that the plan does not carry). I appended an "Evidence (invented...)" sentence to each goal paragraph; G06's paragraph became 230 words. The presenter and the designer disagree on where results live.
- `P/SKILL.md:29-34` ("stacking an assumption on a recorded number is not [allowed]") against `P/SKILL.md:78-80` and `storyline.md:86-88` (every deck has a cost slide "per conversation and per month"). After a one-queue pilot the only way to a four-queue monthly figure is recorded-per-order cost x assumed volume of three queues nobody measured. I did it, labelled the assumption on the slide; the checker cannot tell. The rule and the requirement contradict each other for every proof of concept that is smaller than production.
- `P/assets/deck-format.md:80-84` 40-word body budget against `stage-outlines.md:47` ("table: criterion, threshold, measured, method, sample") and `:72` (contracts table). A five-row table is 77 to 103 words. Eight of ten timed business slides and nine of ten technical slides warned. Same finding as stages 2 and 4; unchanged.
- `P/assets/deck-format.md:85-88` and `check_deck.py:289-294`: notes under half the minutes warn. For a 30-minute technical deck that is 2,250 scripted words; the trial's two-or-three-sentence notes gave 3.5 minutes. The skill never says an outline with short notes is acceptable when a demo and the linked documents fill the slot.
- `P/SKILL.md:129-132`: `decision-memo.md` and `pre-wiring.md` "in the same folder", one filename per topic, while the folder holds four stages and `:130-131` says the memo becomes the record of the decision after the meeting. Writing the December memo would have overwritten the November record. I archived it as `decision-memo.poc-approval.md` (decision record filled, invented) and did the same for pre-wiring; decks are named per stage, memos should be too.
- `P/references/audiences-and-questions.md:8` heads the technical column "Internal technical teams"; `SKILL.md:59-61` defines the audience as "hosts, depends on, is paged for", which fits an external IT firm. Cosmetic, but a reader of the reference alone would skip the IT firm.
- `P/references/speech.md:111-116` and `stage-outlines.md:69` require "the recorded demo of the measured build". The user never mentioned a recording. The technical deck's slide 4 says "the recorded demo and the numbers are the same build", which I invented beyond what the user reported. The skill should say "or that there is no demo" at that slide, as `SKILL.md:95-96` does elsewhere.
- `P/SKILL.md:64-65` wants "the one person who decides"; for the IT firm the record has no name. The checker warns only when `decider` is empty, so a role passes. Fine, but the skill does not say a role is acceptable.
- `check_deck.py:227` counts title words with `[\w'-]+`, so "1.7" is two words and "4.4" two; a results title with three decimals loses three words of its 20. Three business titles and one technical title warned mostly for that reason.
- Invented by me as the user, beyond the brief: the champion's name "Maria", the review dates (10 and 11 Dec), the January timeline on the business deck slide 10 (labelled "proposed, not yet agreed"), and option B's "about 8 hours" on the ask slide, which has no plan line (labelled estimate; see numbers below).

**Did the plan's evidence reach the slides with citations?** Yes. Every measured figure on both decks cites a G line or acceptance ID (G02, G04/A1, G05/A2 to A4, G06, G06/A2) or a contract or decision ID; the NOT RUN case is in the business "did not work" and risk slides and in the technical contracts table as "G05/A4 NOT RUN". Latency, never measured, is in the technical cost title as "not measured".

**Numbers on a slide without a source:** two, both labelled estimate but with no record behind them: option B's "about 8 hours" (business ask slide) and the January dates on slide 10 (marked proposed). Everything else cites the plan or shows its arithmetic (USD 230 a month = 0.07 x about 2,900 + about 25, assumption named).

**Helper outputs:** `check_deck.py --deck production-approval-business.md`: first run exit 0, 12 warnings (3 titles over 20 words, 8 bodies over 40, notes 4.1 of 15 minutes); after trimming titles exit 0, 9 warnings. `--deck production-approval-technical.md`: first run exit 0, 11 warnings (1 title, 9 bodies, notes 3.5 of 30); final exit 0, 10 warnings. Note: my first two runs piped through `tee`, so the printed `exit` was tee's; both outputs carry no ERROR line and the saved final runs used redirection, so the codes are real.

**Ease: 3/5.** Two decks from one record went quickly because the plan's acceptance IDs are good citation handles. Lost points: the per-month cost contradiction, the memo filename collision, and the evidence having nowhere to live in the plan.

## Stage 6: final results (business)

**Skill files read, in order:** none new; `stage-outlines.md:79-92` (final-results business) and `speech.md:84-94` (final-results skeleton) re-read; `decision-memo-template.md` re-read for the information-only case.

**Evidence written into the plan (invented, labelled):** G08 done 19 h (16 to 24), G05/A4 passed in January in the IT firm's test environment, O4 closed; G09: 25 Jan to 25 Apr 2027, 8,640 emailed orders (73% share), median 1.6 minutes (weekly 1.3 to 2.4; by queue 1.3 to 2.1), corrected 2.9% against 2.8%, wrong deliveries 11 (0.13%), 4 of 4 dispatchers active, 94% through the screen, edits 9% from 14%; cost USD 221, 238, 203 against the USD 230 estimate, USD 0.077 per order; incidents: expired mailbox consent (3 h 40, 41 orders typed, none lost) and a TMS outage (2 h 10, 17 pending, no duplicate).

**Friction log**
- `check_deck.py:239-248`: the title-slide exemption (`position == 1 and "title" in tags`) covers a missing Evidence line, not numbers. The title "1.6 minutes an order" with `Evidence: n/a: title slide` failed with "numbers without evidence". `stage-outlines.md:83` and `speech.md:86-87` put the headline number in the first sentence, so a number on the title slide is the expected case. Fixed by citing G09 on the title slide, which `deck-format.md:53-55` ("the title slide may be short") does not tell you to do.
- `P/references/speech.md:89-90` asks for "the counterfactual with its reason"; the skill does not say what counts as one when there is no control group. I used the shadow fortnight. Unclear.
- `stage-outlines.md:86` "Cost: ... against the estimate": the estimate lived only in the December deck and memo, not in the plan; `SKILL.md:132` records the decision in the plan but not the estimate being decided on. I cited the memo by path. The plan should carry the cost estimate as the number the next review measures against.
- `decision-memo-template.md:6` forces "Decision requested" when `stage-outlines.md:92` allows "information: none". I wrote "none on the system; one ask". The template could say "or: information only, and what is reported".
- The other three queues were never shadow-measured; nothing in the skill prompts for a per-user or per-queue baseline, so the deck carries an honest caveat the plan could have avoided. That is a designer or discovery gap, not a presenter one, but the presenter's "what we would do differently" slide (`stage-outlines.md:89`) is where it surfaced.

**Did the plan's evidence reach the slides with citations?** Yes; G09 outcome, adoption, cost and incidents lines are cited slide by slide; the one-queue baseline is cited to G02 and stated as a caveat on the outcome slide body; the estimate is cited to the memo file.

**Numbers on a slide without a source:** one: the ask slide's "about 8 hours of my time plus 3 to 4 for the study" (labelled estimate, no plan line). The "400 dispatcher hours" is arithmetic shown on the slide (2.8 x 8,640) with "we estimate" and "not reassigned". The 2 Dec example order in the stage-5 chart notes is marked invented and sits in notes, not the body.

**Helper outputs:** `check_deck.py --deck final-results-business.md`: first run exit 1, one error (title-slide numbers, above); after the fix and four title trims, exit 0, 9 warnings (8 bodies over 40 words, notes 3.4 of 15 minutes).

**Ease: 4/5.** The final-results outline is short and its slides are new material; the only real snag was the title-slide error.

**Distinct from production approval?** Yes, mostly. Adoption with a definition of active, incidents with fixes and owners, the team slide and the lessons slide are material the production deck did not have, and the ask is light. The summary and cost slides repeat the production deck's shape with new numbers, which is the point. The decision memo felt repetitive: the options table is forced even when the recommendation is "keep running".

## Stage 7: public case study for the Google Cloud account team

**Skill files read, in order:** `P/SKILL.md:105-108` (case-study paragraph); `P/references/case-study.md` (117 lines); `P/assets/case-study-template.md` (73 lines); `stage-outlines.md:109-115`; `check_deck.py:79-87` (banned wording) re-read. Project files: the plan (G02, G04 to G06, G08, G09), the design §2 and §3, the brief §1 and §2, and the final-results deck as the internal write-up the public text derives from (`case-study.md:74-76`).

**Friction log**
- `P/SKILL.md:105-108` says the case study "uses the case-study template instead of a deck", while `stage-outlines.md:109-115` and `check_deck.py:45` define a `case-study` deck stage with required tags. Deck or prose? The reference's pack item 9 (`case-study.md:107-110`) lists derived assets without a deck. I produced the prose (the deliverable) and an 8-slide companion deck for the meeting; the skill should say when each is wanted.
- `P/references/case-study.md:91-112` lists ten pack items including the timeline (item 6) and contacts (item 10); `case-study-template.md:62-73` has ten rows that omit both and split others. I added two rows. The reference and the template disagree.
- `case-study-template.md:1`: the headline template reads "<Customer> <verb> <outcome> with AI agents built with Google Cloud". Two problems: "Built with Google Cloud" is the phrase for "several products, some guidance from Google" (`case-study.md:28`), not for a Gemini-only build, so the template nudges the wrong attribution; and "AI agents" is wrong for a system the design calls one `LlmAgent` with no tools and no loop (D1), after the discovery skill rejected "agent" on purpose. The headline template contradicts the record it is filled from.
- `case-study.md:41-42` and `case-study-template.md:71` ("wording lint passed"): no lint exists for the prose; `check_deck.py` needs front matter and slides. I grepped by hand and recorded that in the pack row. Either add a `--prose` mode or say "grep by hand" in the reference.
- `case-study.md:13-19` and `:44-53` assume the customer holds the Google Cloud agreement. Here the billing account is the IT firm's (a reseller or managed-service shape the brief set up in stage 1). The reference's only guidance is "ask"; it does not say who may consent to publicity, whose account manager is the contact, or whether the IT firm must be named. I improvised the first pack row; a one-line "when a third party holds the account" would have saved it.
- `case-study.md:107-110`: derived assets (talk proposal with 150-word abstract, blog draft, sanitised sample with CLA) read as expected for every case study. For a 40-person firm with no marketing function they are noise; only the sample is marked optional. Over-long for the small-customer case.
- `case-study.md:114-117` interview "questions from the gaps": good, did it; six questions at the end of the draft.
- Invented beyond what the user reported: the CEO's approval in principle on 6 May; the Google account manager's approach; the review dates in the pack; Maria's quote text (marked draft, not approved). The reference's "approved in writing by <name>, <date>" (`case-study.md:85-86`) is unmeetable at drafting time, which the template handles with "draft, not approved"; fine.

**Did the plan's evidence reach the text with citations?** Yes. The results table cites G02 and G09 per row with window, sample, method and a publishable status; the prose cites G03, G04/A1, G06, G08, G09, D1, D2, D4, C2, C3, C5, D6. The deck cites the same lines.

**Numbers on a slide without a source:** none on the deck; "about 90 contractor hours" is 71 + 19 from G06 and G08. In the prose, the "about 300 customers, 120 trucks, 40 office staff" line is the brief's invented firm description, cited to §1.

**Helper outputs:** `check_deck.py --deck case-study-public.md`: exit 0, 6 warnings (5 bodies over 40 words, notes 1.7 of 10 minutes); wording lint: no error. Probe: the same deck with "GCP" injected gave `ERROR line 25: wording not allowed in a public story: GCP (write Google Cloud in full)` (exit 1 by `check_deck.py:328`), so the lint works. Prose lint by `grep -i -E` for the six banned patterns: no match.

**Ease: 3/5.** The reference is the most useful document in the skill (what you may say, what needs consent, there is no form) and it answered the user's "I have no idea what Google needs". Lost points: template and reference disagree, the headline template contradicts the attribution rule, deck-or-prose is unsettled, and the reseller case is unhandled.

**Distinct from production approval and final results?** In content, yes: the approval trail per sentence, the publishable status per number, the attribution phrase and the pack are work no other stage does, and the user learned something new from it. The companion deck, however, is the final-results deck in public wording, slide for slide (challenge, solution, results, what did not improve, next); that is what `case-study.md:74-76` prescribes ("derived from the full draft, never written first"), so it is repetition by design. If the deck is not wanted, the skill should say so and the repetition disappears.

## Summary table

| Stage | Files produced | Check exit (final) | Warnings | Ease |
| --- | --- | --- | --- | --- |
| 5 production-approval, business | production-approval-business.md, decision-memo.md, pre-wiring.md (+ .poc-approval archives) | 0 | 9 | 3 |
| 5 production-approval, technical | production-approval-technical.md | 0 | 10 | 3 |
| 6 final-results, business | final-results-business.md, decision-memo.md, pre-wiring.md (+ .production-approval archives) | 0 (first run 1) | 9 | 4 |
| 7 case-study | case-study.md (template + pack), case-study-public.md | 0 | 6 | 3 |

Across all four decks: 30 of 34 timed slides warned on the 40-word body budget; every deck warned on spoken minutes; no deck warned on hype words or missing decider.

## The three changes I would make first

1. **Fix the body budget against the outlines, or exempt what the outlines require.** `deck-format.md:80-84` and `check_deck.py:253-256` warn at 40 words; `stage-outlines.md` asks for a criteria table, a contracts table, an options slide and an appendix question bank, none of which fit. Thirty of thirty-four timed slides warned across stages 5 to 7, which makes the warning noise nobody reads. Exempt tables, `ask`, `questions` and `appendix` slides, or count a table row as one call-out, and say in the deck format that a warning on those slides is expected.
2. **Resolve the per-month cost contradiction for pilots smaller than production.** `SKILL.md:29-34` forbids stacking an assumption on a recorded number; `SKILL.md:78-80` requires a per-month cost on every deck. Write the allowed form: "we estimate <per-unit measured> x <volume assumed, named> = <per month>", with the assumption in the Evidence line, and let the checker accept `assumption` beside a citation on `cost` slides. Otherwise every honest production-approval deck breaks one rule or the other.
3. **Name memos and pre-wiring per stage, and let the title slide carry the headline number.** `SKILL.md:129-132` writes `decision-memo.md` and `pre-wiring.md` once per topic folder while the folder holds four stages and the memo is the decision record; use `<stage>-decision-memo.md` and `<stage>-pre-wiring.md` as decks already do. And in `check_deck.py:239-248` extend the slide-1 `title` exemption to the numbers rule (or tell the author in `deck-format.md:53-55` to cite on the title slide), because `stage-outlines.md:83` and `speech.md:86` put the measured number in the first sentence.

Next after those: make `case-study-template.md` match `case-study.md`'s pack (timeline and contacts rows), change its headline line to use the attribution phrase the rule selects and drop "AI agents" when the design says otherwise, state whether a case-study deck is wanted, add a prose mode to the wording lint, and give the plan a slot for results per goal so the presenter's "tickets and their Evidence sections" has something to read.
