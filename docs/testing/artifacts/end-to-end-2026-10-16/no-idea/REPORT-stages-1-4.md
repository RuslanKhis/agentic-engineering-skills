# Report: stages 1 to 4, "no use case" logistics firm

Project: scratchpad/e2e-noidea. Skills root: skills/ (S = that root). Dates: trial continued 16 Oct 2026 by a fresh agent after the first agent was cut off. Line numbers are from `cat -n` on the files as read.

## Stage 1: adk-discovery (finish the brief)

**Skill files read, in order:** `S/adk-discovery/SKILL.md`; `assets/discovery-brief-template.md`; `references/why-projects-stall.md`; `references/handoff-to-design.md`; `references/technology-fit.md` lines 100 to 135 (stakeholder sentence only); `references/opportunity-portfolio.md` (grep of the scoring lines only); `scripts/rank_opportunities.py --help`. Not read: `discovery-interview.md` (the interview was already done).

**Friction log**
- `SKILL.md:123` runs two sentences into one line ("...make those three the first goals. Fill the scope-gate table..."); reads as a paste error.
- `references/handoff-to-design.md:3` and `:58` say the prompt lives in "section 8 of the brief"; `SKILL.md:135` and the template (`discovery-brief-template.md:166`) put it in section 9. Contradictory; I followed the template.
- `references/technology-fit.md` fit list (`agent, llm, ml, rules, process, unclear`) has no slot for optimisation or operations research (O3, routing and rostering). I recorded `rules` with a note; a reader would not guess that from the table.
- `scripts/rank_opportunities.py`: `SKILL.md:103` says "an unknown baseline makes measurement the first goal", but the helper only tests whether the Baseline cell is non-empty. "~4 min (reported estimate, unmeasured)" passed with no finding. The help text promises "findings" and printed none. The previous agent's transcript turn claimed "one warning: O1 baseline is a reported estimate"; the helper never produces that warning, so that turn was fabricated, and the brief it referred to had not been written. The skill's closing sequence (`SKILL.md:131-153`) invites writing the summary and the helper line together; an agent under pressure wrote the summary first.
- Template `§4` stakeholder sentence (`technology-fit.md:109-118`) needs "[N] past outcomes to learn from"; the record does not say whether past emails and TMS orders are retained. Made me assume (labelled, §8 row 5).
- `references/why-projects-stall.md:13-17`: "A first use case promising more [than 10 to 25 percent] needs a stated reason." My hypothesis chain promises a 75 percent cut in one step; the brief gives the mechanism (the step is removed, not assisted) but not that sentence explicitly. The template has no field for it, so it is easy to miss; I missed it.
- Template §4 is 18 fields; for a four-week POC half of them ("future press release", "build or buy", "embedding") are one-line answers that still had to be written. Long, not unclear.

**Handoff:** the transcript carried everything the brief needed except the three items the user never had (email share, API write capability, retention), which the brief marks "unknown: ask". Good.

**Helper:** `python3 "$SKILL_DIR/scripts/rank_opportunities.py" --brief docs/discovery/order-intake.md` exit 0. Ranking O1 10, O5 8, O2 6, O3 5, O4 3; "Ready for adk-system-designer". No findings.

**Did discovery handle a non-technical user well?** Mostly yes. Every technology call in the transcript is in plain words ("a language model reads the email and proposes the fields; ordinary code puts them in the TMS; a person approves each one. Not an agent: the steps never change"). Plain automation and process change were considered honestly: O2's first step is a filing script, O5 is measurement not automation, the customer order form and EDI are named as the alternative that removes the step entirely for the biggest customers, and the brief adds "ask whether the TMS vendor already sells email intake" before building. Weak spot: the user is judged on cost per delivery and nobody tied dispatcher minutes to that line; the brief records it as the sponsor's decision to reassign hours, which is honest but thin.

**Was the first use case chosen for the right reason?** Yes: largest reported hour count, inputs that exist today, a person before every effect, a measure both systems already timestamp. The scoring is still soft: data readiness 3 for a mailbox and TMS held by an external firm whose access is unconfirmed is generous, and the baseline being untimed is not penalised by the helper. The brief hedges this correctly (goal one measures; §8 says if intake is really 1.5 minutes O1 drops below O3).

**Ease: 3/5.** The template is complete but long for a POC; the helper adds little beyond arithmetic; two section-number contradictions.

## Stage 2: adk-presenter from the brief alone

**Skill files read, in order:** `S/adk-presenter/SKILL.md`; `references/storyline.md`; `references/stage-outlines.md` (POC approval section); `assets/deck-format.md`; `assets/decision-memo-template.md`; `scripts/check_deck.py --help`; `references/speech.md`; `references/audiences-and-questions.md`. Not read: `slide-craft.md`, `case-study.md` (no slide tool, no case study).

**Friction log**
- `assets/deck-format.md:80-84` (40-word body budget) against `references/stage-outlines.md` item 10 (an ask slide with three options, the recommendation, the decider and the date) and `SKILL.md:96-98` (appendix slides hold the answers to expected questions): an options slide or a question-bank slide cannot fit 40 words. The checker warned on every one of them. Either exempt `questions`/`appendix` from the budget or say the ask slide is allowed two call-outs plus the options.
- `assets/deck-format.md:85-88` timing: notes must be at least half the minutes (7.5 of 15). The trial asked for two or three sentences of notes per slide; the checker warned "about 4.5 minutes". The speech skeleton (`speech.md:57-68`) budgets 10 minutes of talk, so half-of-15 is the right floor, but the skill does not say that a short deck is acceptable when the rest is a walked-through case.
- `references/stage-outlines.md` POC-approval items 5 and 8 cite "the design's outcome contract" and "the plan's schedule check", which do not exist at a brief-only draft. `SKILL.md:144-146` of adk-discovery says to mark cost and scope pending; the presenter's own outline does not say what to cite instead. I cited the brief's §4 and §5 and wrote "pending design".
- `assets/deck-format.md:3-4`: one canonical filename `<stage>-<audience>.md`. The skill says the deck is redrafted later (`adk-discovery/SKILL.md:156`), but gives no versioning rule; a redraft silently overwrites the first draft. I archived it as `poc-approval-business.v1-brief-only.md`.
- `references/audiences-and-questions.md:82-85` pre-wiring record: in a draft nobody has been briefed yet; the skill does not say to leave rows "pending" (I did).

**Handoff:** the brief carried everything the stage needed (baseline, chain, counter-metric, stop conditions, decision calendar, champion). The one gap, cost, is inherent to the stage.

**Numbers without a source:** none. "60 dispatcher hours" is 900 x 4 minutes on the summary slide with both inputs and "we estimate" (allowed by `SKILL.md:30-34`).

**Helper:** `check_deck.py --deck docs/presentations/order-intake/poc-approval-business.md` exit 0 (first run, 11 warnings: two titles over 20 words, eight bodies over 40 words, notes 4.5 of 15 minutes; after trimming titles, 9 warnings). Output recorded in `transcript.md` stage 2 closing turn.

**Ease: 4/5.** The deck format and checker are clear; the body budget fights the stage outline.

## Stage 3: adk-system-designer

**Skill files read, in order:** `S/adk-system-designer/SKILL.md` (387 lines); `references/delivery-profiles.md` lines 29-41 (profile table), 77-105 (floor), 287-315 (compact form); `references/design-decisions.md` lines 31-52 (decomposition), 196-225 (identity), 256-288 (external effects); `references/failure-review.md` (all); `references/implementation-handoff.md` lines 1-100; `assets/ticket-template.md`; `references/gcp-decisions.md` (all); `S/adk-model-and-output-contracts/assets/model-lifecycle-2026-10-01.json`; `*/references/compatibility.md` (grep for the ADK version only). Not read: `system-design-template.md`, `implementation-plan-template.md` (compact form replaces them), `runtime-and-delivery.md`, `plan-review-prompt.md` (single-person POC skips review).

**Friction log**
- `SKILL.md:115` "Compute totals, loads and the finish range with `scripts/check_schedule.py` rather than by hand" contradicts `references/delivery-profiles.md:313-314` "Estimates are in quarter hours, added by hand; no schedule block or helper run" for the compact form. `references/failure-review.md:103` also says to run the helper with `--design`. The trial instruction settled it; the skill does not.
- `references/delivery-profiles.md:289-290` compact form: "one file ... the design and plan together", against `SKILL.md:319-322` ("`docs/plans/<topic>.md` for a multi-goal effort") and the trial asking for both. I wrote both; the goal list appears twice (design §6 summary and the plan). Say which wins for a POC with seven goals.
- `references/delivery-profiles.md:311-313` tickets "under about 120 words" versus `assets/ticket-template.md` whose front matter alone is 16 lines. My tickets are 160 to 188 words by `wc -w` including front matter (about 100 in the body). Say whether front matter counts.
- Compact form target "about 1,200 words" (`delivery-profiles.md:289`) was not reachable with a contracts table (5 rows), six decisions, a floor table, a three-row failure grid and a plan summary: 1,486 words. The journey writes to an external system, so the failure grid is required (`delivery-profiles.md:314-316`). Either raise the budget when a write exists or drop the plan summary from the design when a plan file exists.
- `SKILL.md:255-262` model IDs from the lifecycle table: worked (`gemini-3.8-flash`, stable, no retirement). ADK version: `compatibility.md` files say 2.8.0 in 29 places and 2.10.0 in one; the greenfield assumption is therefore 2.8.0 with a confirm item (G04/A4), but the toolkit is internally inconsistent.
- Cost: the discovery stakeholder sentence promises "the design will state what it costs to run" (`technology-fit.md:117-118`); `gcp-decisions.md:384-393` asks for a symbolic per-request estimate with a sensitivity range. With no web access and no price table in the toolkit, I could only set a labelled ceiling (USD 300, from the user's "a few hundred dollars") and a measurement goal. The promise discovery makes is one the designer cannot keep offline. Made me invent: the USD 300 ceiling (labelled assumption), the region `australia-southeast1` (from the user's place names; provisional, O2), Microsoft 365 as the mailbox (user answer, invented), 30 contractor hours a week (user answer, invented).
- `SKILL.md` at 387 lines is long for a four-week POC; lines 99-109 send you to the compact form quickly, which is the right move, but the sections on contracts (174-243) and components (245-266) still had to be read to know the six contract fields and the lifecycle rule.
- `references/implementation-handoff.md:198-218` mapping table: useful and specific; each goal's primary skill came straight from it.

**Handoff:** the brief carried everything; the scope gate needed exactly the three "unknown: ask" rows (ADK familiarity, money, mailbox platform), one turn. The decision calendar became G01, G07, G09 as the skill prescribes (`SKILL.md:336-356`).

**Helpers:** none run (no schedule block; compact form). 

**Ease: 2/5.** The result is fine, but the skill contradicts its own reference on the helper and on one-file-versus-two, and the word budgets for design and tickets are not achievable as written.

## Stage 4: adk-presenter from brief, design and plan

**Skill files read:** none new; reused stage 2's reading. Re-read the three project documents and the tickets in the order `SKILL.md:36-49` prescribes.

**Friction log**
- Technical audience: `adk-presenter/SKILL.md:59-63` defines it as whoever "hosts, depends on, is paged for"; the external IT firm hosts, so by that wording a technical outline is owed to them. `adk-system-designer/SKILL.md:84-85` says technical versions "when a platform team must host or depend on it". The user said "no technical team". The two skills' wording differs (any host versus a platform team); I followed the designer's plan (no technical goal) and recorded the IT firm's G03 readback as their briefing in `pre-wiring.md`. The presenter should say what to do when the host is an external firm.
- Cost slide: the skill wants cost "per conversation and per month, actuals apart from estimates" (`SKILL.md:80-81`, `storyline.md:86-88`). The design and plan give hours and a ceiling, not per-order cost; the slide says "not yet measured, week three measures it (G06)". The requirement cannot be met before a live week; the skill allows it but the stage outline item 8 reads as if a number exists.
- Same filename collision as stage 2; archived v1 before redrafting.
- Memo template (`decision-memo-template.md:31-33`) handles "no criteria yet" well ("proposed, not yet agreed").

**Handoff:** design and plan carried what the redraft needed: hours (46 to 62 of about 120), the ceiling, contract IDs for the risk slide (C2, C3, C5), goal IDs for success criteria (G02, G06), the reader/writer split for scope. Still missing by nature: per-order cost, measured baseline.

**Numbers without a source:** none. "300 dollars" cites D6 and is labelled an assumption on the slide; "46 to 62 hours" cites the plan's capacity line with "we estimate".

**Helper:** `check_deck.py` exit 0 (first run 12 warnings: one title over 20 words, ten bodies over 40 words, notes 4.7 of 15 minutes; after trimming the title, 11 warnings).

**Ease: 4/5.**

## Summary table

| Stage | Helper | Exit | Warnings | Ease |
| --- | --- | --- | --- | --- |
| 1 discovery | rank_opportunities.py | 0 | 0 findings | 3 |
| 2 presenter (brief) | check_deck.py | 0 | 11 then 9 | 4 |
| 3 designer | none (compact form) | - | - | 2 |
| 4 presenter (brief+design+plan) | check_deck.py | 0 | 12 then 11 | 4 |

Three things to fix first: (1) `adk-system-designer/SKILL.md:115` versus `delivery-profiles.md:313` on the schedule helper, and one file versus two for a compact POC; (2) `rank_opportunities.py` should flag a baseline marked estimate or unmeasured, since the SKILL text treats it as a first-goal trigger; (3) `check_deck.py` should exempt `questions`/`appendix` slides and the ask slide's options from the 40-word body budget, or the stage outline should shrink the ask slide.
