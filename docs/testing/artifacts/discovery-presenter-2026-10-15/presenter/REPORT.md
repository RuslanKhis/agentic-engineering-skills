# Trial report: adk-presenter on the campaign-assistant record

Trial root: this directory. Skill: `skills/adk-presenter/` in the repo (read only).
Outputs: `docs/presentations/campaign-assistant/{production-approval-business.md,
production-approval-technical.md, decision-memo.md, pre-wiring.md}`, `helper-output.txt`.
Clock in this sandbox: 15 October 2026, 16:57 to about 17:07 AEDT.

## 1. Skill files read, in order

1. `SKILL.md` (131 lines)
2. `references/storyline.md` (118)
3. `references/stage-outlines.md` (117)
4. `assets/deck-format.md` (98)
5. `references/audiences-and-questions.md` (89)
6. `assets/decision-memo-template.md` (37)
7. `scripts/check_deck.py` (261; read in full to know what the check enforces)

Not read: `references/case-study.md`, `assets/case-study-template.md` (SKILL.md line 94 scopes them to the case-study stage), `tests/test_check_deck.py`, `agents/openai.yaml`.

Stage settled as `production-approval`; audiences `business` (15 min, given) then `technical` (30 min, the skill's default at SKILL.md:49; the user did not say). Decider and date: Director of SMB Sales, 30 October 2026, which the record also holds (brief §6, plan schedule check).

## 2. Friction log (file:line)

- **SKILL.md:33-36 vs 52-62, ordering.** "Settle three things ... asking only for what the request and the record do not say" comes before "Then read the record". The decider (sponsor, brief §6) and the date (plan schedule check) were in the record; following the order literally, an agent asks the user before reading the file that answers it. Reverse the two sections or say "after reading the record, ask for what is still missing".
- **SKILL.md:29-31 vs 74-77, derived numbers.** "A number the record does not hold does not go on a slide" against "a cost slide (per conversation and per month ...)". The record holds $142 total and 312 sessions, not a per-session figure. Nothing says whether arithmetic on recorded numbers is allowed. I divided, labelled it "we estimate", and showed the division on the slide. Say explicitly: derived figures are allowed when the arithmetic and both inputs are on the slide and the voice is "estimate".
- **storyline.md:70-73 vs check_deck.py:219-222, appendix size.** "Roughly one summary slide for every ten slides of appendix" for an executive audience; the checker warns when content slides exceed minutes. An 11-slide business deck for 15 minutes can hold at most 3 appendix slides before the warning fires. One of the two must give; I capped the appendix at 3 and dropped several question-bank answers into the memo instead.
- **SKILL.md:48-50 vs deck-format.md:45-47, front matter.** The decider and date are required inputs but have no front-matter key; the format lists `stage, audience, minutes, title, sources, decision`. I added `decider:` and `date:` keys; the checker tolerates unknown keys silently. Either document the keys or tell the author to fold decider and date into `decision`.
- **SKILL.md:110-113 and audiences-and-questions.md:83-89, pre-wiring table location.** "Keep it in the presentation folder beside the outline; the decision memo links to it" gives no filename. I invented `pre-wiring.md`. The premortem's answers also have no stated home beyond "the appendix"; I put the premortem table in the same file.
- **SKILL.md:115 and decision-memo-template.md, memo filename.** Not specified. I used `decision-memo.md` and cited it from the ask slides, which also made the ask slide's Evidence line a path citation; a reviewer could see that as circular.
- **decision-memo-template.md:28-29, kill and success criteria.** The template demands "Kill criteria" and "Success criteria for the next review" but the record (as a production-approval record usually will) holds neither for the production phase. I proposed them from G04's thresholds and wrote "proposed, not yet agreed". The template should say what to do when the record has none; otherwise this is the one place the skill pushes an author to invent.
- **SKILL.md:113, "time a rehearsal against the minutes".** An agent cannot rehearse. Either say "tell the user to rehearse" or give a word-count rule for the notes (for example, about 130 spoken words a minute) so the agent can estimate.
- **SKILL.md:85-86 and stage-outlines.md:64, demo build.** "State the build the demo shows and the build the numbers cover" assumes a demo exists. The user never mentioned one and a business slot of 15 minutes has none. Say what to do when there is no demo (I wrote "no demo in the business slot" only in the pre-wiring file). Note also that the record only answered the question because I, as the record's author, put the build tag in G04's evidence; a plan written by the engineer skill may not carry it, and the skill should name it as something to ask for.
- **SKILL.md:81-86, three voices on one slide.** The cost slide must hold measured actuals and an estimate; the deck format has one `Evidence:` line per slide, and the checker classifies any line with a G-ID as `cited`, so a mixed slide passes with no signal. I appended `; estimate` to the Evidence line and split the bullets by voice. Give a pattern for mixed slides, or require a voice word per bullet.
- **stage-outlines.md:58-72, technical outline vs the family's own proof-of-concept profile.** Slides 6 (latency, tokens, cost per conversation from traces), 10 (observability, who is paged), 11 (release and rollback) and half of 9 (tests proving security) are, by the system-designer skill's deferred-controls convention, exactly what a 4-week proof of concept does not have. Four of thirteen technical slides therefore say "does not exist; G05". That is honest and probably intended, but the outline reads as if the record will hold them; a sentence saying "for a proof-of-concept review most of these will be 'not yet built' slides; keep them, they are the inherited work" would stop an author from feeling the deck is failing.
- **Duplication.** The value/cost/risk rule appears at SKILL.md:74-77 and storyline.md:84-92; the premortem at SKILL.md:110-113, storyline.md:102-109 and audiences-and-questions.md:69-81; the two-decks-not-one rule at SKILL.md:46-47, audiences-and-questions.md:3-4 and storyline.md:94. storyline.md:3-12 is a 10-line source bibliography before the first instruction. None of it contradicts, but about a quarter of the reading is repeat.
- **stage-outlines.md:55 vs deck-format.md:61-62, `timeline` tag.** The outline tags "Timeline and checkpoints" as `production-scope`; `timeline` is an accepted tag in the format. Harmless; I used both.
- **check_deck.py:53, `W\d+`.** The citation regex accepts `W` IDs that no document defines. check_deck.py:58-63: `NUMERIC_CLAIM` misses "8 of 10 acceptance cases", "112 of 312" and dates, and prints "$500" as "$5" in the error text (currency alternative captures one digit). Cosmetic, but an author relying on the checker to catch unsourced counts will be under-served.
- **No guidance on statistical uncertainty.** Nothing in the skill asks whether a measured lift is distinguishable from its baseline. 36% on 312 sessions against 31% has a margin of roughly five points; the only reason the deck says so is that I wrote "no significance test was run" into the plan. If the plan had been silent, the skill's "method and sample in one clause" rule would have let a within-noise lift headline a funding ask. Add a line: when the lift is small relative to the sample, say so in the title or ask the user for the test.
- **Trial-setup oddity, not the skill's fault.** The sandbox date is 15 October 2026 and the record's measurement runs to 23 October. I ignored it.

## 3. Traceability: every number on the slides, and how the gaps were shown

Business deck, by slide (all sources are in the trial record):

| Number | Slide(s) | Source |
| --- | --- | --- |
| 31% baseline, 663 of 2,140, Q2 2026 | 2, 3, 4, 13 | brief §2 table; plan G04/A1 |
| 38% product choice, 12% creative, 19% payment | 13 | brief §2 table |
| 36%, 112 of 312, 10 to 23 Oct 2026 | 2, 3, 4, 14 | plan G04/A1 |
| 30% unassisted, same window | 4 | plan G04/A1 context line |
| 34% threshold, 300 sessions | 3 | plan G04/A1 criterion |
| 3% refunds, 3 of 112, 24 Oct finance export | 2, 3, 14 | plan G04/A3; brief §5 baseline |
| 8 of 10 cases passed | 5 | plan Summary |
| 58 h (planned 56), $142, 15 Sep to 24 Oct | 8 | plan cost record |
| $0.46 per session | 8 | derived: $142 ÷ 312, labelled estimate, arithmetic shown |
| 8 of 8, 40 of 40, 0 of 20 | 10 | plan G03/A1, G02/A1, G01/A1 |
| 30-minute expiry | 5 (via D5) | design D5 |
| 12 September, 9 September, 14 August dates | 3, 13, 15 | plan header; design header; brief §2 |
| 30 October 2026 | 1, 2, 11, 12 | plan schedule check |
| 13 November 2026 | 11, 12, memo | invented: two weeks after the decision, labelled estimate |

Technical deck: the same figures plus the per-case table (plan G01 to G04), build `poc-0.3` / commit 4f2e1c9 (plan G04), the contract enforcement points (design contracts table). No figure on either deck lacks a row above. Monthly production cost, G05 hours, p95 latency, tokens per turn, sales-desk effect and significance are shown as "not measured" or "not estimated" with G05 named, as SKILL.md:29-31 requires.

NOT RUN cases: G03/A3 (duplicate order on retry, C4) and G04/A2 (expired quote requoted, D5) appear by ID in the business summary (slide 2), in their own `learned` slide (5) with the reason each was not run and the consequence, in the risk table (9, R2, owner Russ), and as the two conditions of the ask (12) and of the memo's option A. In the technical deck they are in the summary (2), the evaluation table's absence (4), their own slide (5), the contracts table (9, C4 marked NOT RUN), and the ask (14). Nowhere are they counted as passed or folded into a pass rate without the "of 10" denominator.

Open decision (agency delegation): business slide 6 (what changed the plan, R3), slide 7 (production scope excludes agencies), slide 9 (risk with owner Ad Products lead), the memo's scope line and the pre-wiring row; technical slide 8 (refuse agency logins at the identity boundary until the rights service has delegation). The deck does not claim what share of advertisers are agencies, because the record does not say.

## 4. Temptations to invent, and what the skill said

- **Cost per month at production.** The stage outline (stage-outlines.md:52) and SKILL.md:75 want "per month". 2,140 advertisers a quarter and $0.46 a session invite a "$300-odd a month" figure. I did not write it: advertisers per quarter are not assisted sessions per month, so it would be two assumptions stacked, and SKILL.md:29-31 says the slide says "not yet measured" and names the goal (G05). Done that way on business slide 8 and technical slide 7.
- **Cost per session.** I did derive $142 ÷ 312 = $0.46. The skill is silent on derivation (friction item 2); I labelled it "we estimate ... upper bound, build-time spend included".
- **A confidence interval.** I was tempted to put "±5 points" on slide 4. The record does not hold it, so it stays off the slides; the plan's "no significance test was run" line is cited instead and spoken in the notes.
- **Demo result.** No demo exists in the record. The skill's "state the build the demo shows" (SKILL.md:85) made me want one; the technical deck says the demo is the same build on the G01 test advertisers and the business deck has none. I did not describe a demo outcome anywhere.
- **Kill criteria, next-review criteria, 13 November date, build dates.** The memo template demands the first two; I proposed them from G04's thresholds and labelled "proposed, not yet agreed". The 13 November date is my invention (two weeks after the decision), labelled "estimate" on slides 11 and 12. Build and launch dates: refused, "set by the G05 estimate, not yet known".
- **Sales-desk effect.** The brief hints that product-choice questions dominate the desk's tally; I wrote "not measured" on slide 7 rather than a reduction claim.
- **Recommendation.** The user asked to "decide whether we fund the production build"; the record has no production estimate, so an unconditional funding ask is not supported. Per SKILL.md:128-129 I changed the ask to a conditional one and say so here before the deck does. Answers I invented for the user: technical slot 30 minutes; no live demo in the business slot; decider for the technical deck is the Platform team lead for hosting (the record names the role, not that it decides).

## 5. Time and ease

About ten minutes of wall clock from first read to final check (16:57 to 17:07 sandbox time), roughly half of it reading the seven files and the checker. Both outlines passed `check_deck.py` on the first run with no errors and no warnings; a deliberate probe (in `helper-output.txt`) confirmed the checker fails numbers without evidence and warns on measured-sounding hypothesis slides.

Ease: **4 of 5.** The stage outline plus the deck format plus the checker make the drafting almost mechanical, and the "not measured, name the goal" rule answered every temptation above except derivation. The point lost is for the small gaps that each forced an invention: where the pre-wiring and memo files live, whether arithmetic on recorded numbers is allowed, what to do when the memo template wants criteria the record lacks, and the appendix-size contradiction between the storyline and the checker.
