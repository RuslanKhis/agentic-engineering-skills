# Report: stages 2 to 4 (presenter from brief; designer; presenter from brief + design + plan)

Project: `scratchpad/e2e-rough/`. Transcript: `transcript.md`. Skills read, never modified. All helper runs with `python3` (3.9+), outputs under `docs/presentations/smb-self-serve-ads/checks/`. "S:L" means `SKILL.md` line; other files are relative to the skill folder.

## Stage 2: /adk-presenter, proof-of-concept approval, business, brief only

**Skill files read, in order:** `SKILL.md` (whole); `references/storyline.md`; `references/stage-outlines.md`; `assets/deck-format.md`; `references/speech.md`; `references/audiences-and-questions.md`; `assets/decision-memo-template.md`; `scripts/check_deck.py` (constants and the numeric rule, to know what fails). Not read: `references/slide-craft.md` (no slide-building tool offered), `references/case-study.md`, `assets/case-study-template.md` (not a case study).

**Outputs:** `docs/presentations/smb-self-serve-ads/poc-approval-business.brief-only.md` (13 slides, 10 timed; renamed at stage 4 so the redraft could take the canonical name), `decision-memo.md`, `pre-wiring.md`.

**Helper:** `check_deck.py` exit 0, 12 warnings: every slide body over the 40-word budget (45 to 123 words; appendix slides included at that time), and "notes hold 782 words, about 5.2 minutes for a 15-minute slot". Output: `checks/stage2-poc-approval-business.txt`.

**Friction log:**
- `assets/deck-format.md:81-84` and `check_deck.py:60`: a 40-word body budget on every slide contradicts `references/stage-outlines.md:24-25` (a risk slide needs "a control and an owner" per risk, three risks) and `references/storyline.md:75-80` (the ask slide needs two or three options, the recommended one marked, the decider and the date). Three risks with control and owner cannot be said in 40 words; the checker warned on all ten timed slides. (The checker changed between my stage 2 and stage 4 runs; see stage 4.)
- `SKILL.md:120-121` "fix every error and read every warning" plus `assets/deck-format.md:85-88` (notes should fill half to all of the minutes) against the trial's own constraint of two or three sentences of notes per slide: 10 timed slides at three sentences gave 782 words, 5.2 minutes, below the 7.5-minute floor. The skill offers no guidance for a short-notes deck other than the warning. Not a skill bug, but the two rules pull against each other: `references/speech.md:57-67` budgets 10 minutes of talk for a 15-minute slot, so the floor of 50% of `minutes` (7.5) is already above what the skeleton's talk time implies if "minutes" is the slot (the front matter comment says "the speaking time agreed, not the meeting length", which conflicts with the skeleton's 10 talk + 5 questions).
- `SKILL.md:36-49` tells me to read the design, plan, tickets and evaluation report; at this stage none exist and the skill handles it well ("those gaps become slides"). No invention needed; cost and sample were marked pending. Good.
- `references/stage-outlines.md:16` executive-summary placeholder says "<Process> costs <baseline> today" in money terms; the brief holds no money baseline, so the summary had to be in completion-rate terms. Minor.
- `references/storyline.md:14-16` and `SKILL.md:52` ask for the decider; the request said "leadership (chaired by the Director of SMB Sales)" and the brief says leadership decides, the sponsor funds. I wrote "Director of SMB Sales (chairing leadership)". Not invented, but the brief's §6 table could have named the single decider.
- `assets/decision-memo-template.md:31-33`: the "proposed, not yet agreed" instruction is placed between two bullets and reads like a bullet; small formatting trap.
- `references/audiences-and-questions.md:82-86`: the pre-wiring table has no "not yet briefed" state; I had to invent "pending" rows (labelled as planned, not held).

**Handoff:** the brief carried everything the stage needed except money (expected) and the single decider's name. The brief's closing offer prompt (stage 1) was complete and ran as written.

**Numbers on slides without a source:** none; every figure cites the brief by section. Derived counts (813, 700 calls a month) show their arithmetic on the slide.

**Ease: 4/5.** The sequence read-record, SCQA, ghost deck, draft, check is clear and the checker catches real gaps. The body budget and notes-timing warnings are noise at this length.

## Stage 3: /adk-system-designer, design only, compact form

**Skill files read, in order:** `SKILL.md` (whole); `references/delivery-profiles.md` (whole, 4,228 words); `scripts/check_schedule.py --help`; `assets/ticket-template.md`; `references/failure-review.md` (whole); `references/gcp-decisions.md` (whole); headings of `references/design-decisions.md`, `references/implementation-handoff.md`, `assets/implementation-plan-template.md`; then `design-decisions.md:31-90` (decompose, size the first slice); `implementation-handoff.md:67-118`; `implementation-plan-template.md:77-126`; `adk-model-and-output-contracts/assets/model-lifecycle-2026-10-01.json` (for the model id, as `SKILL.md:255-260` requires); the ADK pin from the specialists' `references/compatibility.md` (2.8.0). Not read: `references/runtime-and-delivery.md` (no streaming, downloads or concurrency contracts), `assets/system-design-template.md` (compact form replaces it), `assets/plan-review-prompt.md` (single-person proof of concept skips review, `SKILL.md:312`), the rest of `design-decisions.md`.

**Outputs:** `docs/architecture/smb-self-serve-ads.md` (1,710 words), `docs/plans/smb-self-serve-ads.md` (1,183 words), `docs/tickets/smb-self-serve-ads/G01.md` to `G04.md` (145 to 191 words each with front matter; bodies under 120).

**Helper:** `check_schedule.py` not run: compact form has no schedule block (`delivery-profiles.md:311-312`). Capacity added by hand: 120 h × 0.8 focus, minus 25% reserve = 72 h; phase 1 developer goals 31.5 to 57 h.

**Friction log:**
- `SKILL.md:112-115` "Compute totals, loads and the finish range with `scripts/check_schedule.py` rather than by hand" contradicts `references/delivery-profiles.md:311-312` "Estimates are in quarter hours, added by hand; no schedule block or helper run" for the compact form. The SKILL.md sentence should say "except in the compact form".
- `SKILL.md:102-104` and `delivery-profiles.md:289-290`: "one file of about 1,200 words: the design and plan together", but `SKILL.md:321-323` names separate `docs/architecture/` and `docs/plans/` files, and the presenter (`adk-presenter/SKILL.md:39-45`) reads the plan at `docs/plans/<topic>.md`. I wrote two files. With the compact form's required content (scope-gate table, journey, three to five six-field contracts, up to six five-part decisions, depth table, failure rows, open decisions) the design alone came to 1,710 words; 1,200 is not reachable without dropping a required part. Either raise the number or shorten the required list.
- `delivery-profiles.md:287-307` compact form has no failure grid, but `SKILL.md:291-294` says every cross-cutting design builds the coverage grid and `failure-review.md:40` says "a proof of concept fills the rows it touches in a few words each". I did a four-column version; the compact form should say which columns a proof of concept keeps.
- `SKILL.md:255-260`: choosing the model from `adk-model-and-output-contracts/assets/model-lifecycle-*.json` works, but the designer skill does not say the file is a dict keyed by model id; a one-line schema hint would save a read. Fine otherwise: `gemini-3.8-flash` stable, checked 2026-10-08.
- `delivery-profiles.md:158-160` "For a team new to ADK, multiply by about 1.5 ... apply it to every goal, hands-on and review alike": applying it to the presentation goals (not ADK work) and to the product owner's labelling session is odd; I applied it everywhere as written and said so in the plan. Suggest "every implementation goal".
- `delivery-profiles.md:156` presentation estimate is "3–6 h, plus the review date as a wait"; `SKILL.md:339-352` says the approval goal "depends on nothing but the design" and "the goals that need the decision depend on that wait, not on the deck". Clear, and it carried into the plan as G01 → W1 → G02. Good.
- `delivery-profiles.md:311` says tickets "under about 120 words: front matter, outcome, acceptance and run prompt"; the ticket template's front matter alone is about 60 words, so 120 total is not realistic; my tickets are 145 to 191 with front matter. Say "body under 120 words".
- `references/gcp-decisions.md:55-62` asks for a per-request cost estimate with model mix, token sizes and pricing date; with no web access and no price in any reference, the design could only state the allowance, the bound (C4, quota) and a measurement goal (G04). The skill does not say what to do when prices are unavailable beyond "symbolic estimate" (line 63); a token-count template would have let me give one. This is the gap the stage 4 cost slides had to carry.
- Made me invent (all marked in the transcript): developer familiarity and hours, the 500 EUR allowance, the platform's confirmation of access and caller identity, who pays after the pilot, the calendar dates (2 to 27 Nov, 9 Nov live, 11 Dec review). All were brief §8 open questions, asked in one scope-gate turn as the skill says; none invented silently.
- `SKILL.md:66-89` scope-gate list and `delivery-profiles.md:16-22` table duplicate each other with slightly different wording (the SKILL.md adds the presentations question; the table does not). One home would be better.

**Handoff:** the brief carried the use case, measure, baseline, counter-metric, data register, permission scope, harms, stakeholders and decision calendar into the design without re-asking; the five open items in brief §8 were exactly the scope-gate questions. The design's presentation goals (G01, G07, G08, G10) came from the brief's §6 "presentation milestones" line and `SKILL.md:80-89`.

**Ease: 3/5.** The compact form is the right idea, but the word count, the schedule-helper sentence and the ticket length contradict the main text, and the cost estimate has no fallback when prices are unknown.

## Stage 4: /adk-presenter, proof-of-concept approval from brief + design + plan, business and technical

**Skill files read, in order:** `SKILL.md` and the same references as stage 2 (already in context; re-read `references/stage-outlines.md:27-40` for the technical outline and `assets/deck-format.md:59-65` for the technical tags). Record read in the skill's order: brief, design, plan, tickets G01 to G04.

**Outputs:** `docs/presentations/smb-self-serve-ads/poc-approval-business.md` (13 slides, 10 timed), `poc-approval-technical.md` (14 slides, 12 timed), `decision-memo.md` and `pre-wiring.md` updated in place.

**Helper outputs:**
- Business: `check_deck.py` exit 0; 10 warnings (eight bodies over 40 words, 45 to 63; the ask slide 74 over its 70; cost title 22 words; notes 722 words, 4.8 of 15 minutes). `checks/stage4-poc-approval-business.txt`.
- Technical, first run: exit 1, one error "coverage: no slide Covers problem (required for poc-approval, technical)"; 18 warnings. `checks/stage4-poc-approval-technical.txt`.
- Technical, rerun after tagging the baseline slide `success-criteria, problem`: exit 0; 19 warnings (six titles over 20 words, eleven bodies over 40, notes 1,029 words, 6.9 of 30 minutes). `checks/stage4-poc-approval-technical-rerun.txt`.

**Friction log:**
- `assets/deck-format.md:61` requires `problem` for every audience, but `references/stage-outlines.md:29-40` (technical, poc-approval) has no problem slide; line 39 offers "`problem` or `hypothesis` context" on the "what you get back if it stops" slide, which is not a problem statement. A deck written from the outline fails the checker. Either add a baseline-and-problem slide to the technical outline or drop `problem` from the technical requirement.
- `scripts/check_deck.py` changed between my stage 2 run and stage 4 (uncommitted edits in the repo: an ask-slide budget of 70 words at line 61, appendix and questions slides now unbudgeted at line 258). The 40-word budget still fires on every substantive slide: the technical contracts slide (82 words for five contracts, one line each, as `SKILL.md:98-100` asks "quote the figures") and the evaluation-plan slide (69) cannot meet it. Suggest 40 for business, 80 for technical, or warn only when a slide has no `Notes:`.
- Title budget of 20 words (`check_deck.py:59`) against `references/storyline.md:97-98` "uncertainty goes in the title ('two acceptance cases not yet run')" and `SKILL.md:100` "qualifiers go in the title": a technical title that carries claim plus qualifier runs over 20 words six times here. The two rules compete; the technical deck should get a longer title budget or the qualifier rule should allow a sub-title line.
- `references/stage-outlines.md:37-40`: the technical deck's ask ("we need access, environment, reviewer by date; owner") has a different decider from the business deck (platform team lead versus the sponsor); the front matter has one `decider` field. I wrote both names in it. Add a sentence saying the technical front matter names the person who grants the dependencies.
- `references/speech.md:57`: a 30-minute technical slot budgets 18 minutes of talk, but the checker's floor is 15 minutes of notes (50% of 30); at three sentences per slide the notes reach 6.9 minutes. Same tension as stage 2, worse at 30 minutes.
- Cost slides (`stage-outlines.md:23`, `:37`): "the plan's schedule check and spend assumptions" assumed a per-start money figure that the design did not produce (stage 3 friction). The skill's rule "the slide says not yet measured and names the goal" (`SKILL.md:29-31`) handled it honestly, but the business cost slide is now the weakest slide in the deck, and the premortem says so.
- `SKILL.md:129-132`: the memo is "in the same folder" and one per folder; the stage 2 draft and the stage 4 redraft of the same stage share `decision-memo.md` and `pre-wiring.md`, so I updated in place and renamed the stage 2 deck to `.brief-only.md`. The skill should say whether a redraft replaces the earlier outline or sits beside it.
- `assets/ticket-template.md` and plan G01 acceptance A3 ("the cost slide carries the plan's hours and the design's cost estimate, labelled"): met for hours, not for a money estimate; recorded on the slide as not yet estimated. The ticket's Evidence section was not filled because the presenter skill never mentions tickets' Evidence sections, only the plan (`SKILL.md:130-132` "record the decision ... in it and in the plan").

**Handoff:** the plan's presentation goals carried into the decks: G01 is the deck being written; W1 is the decision wait on both decision slides; G07/G08 give the production review date (11 Dec, invented in stage 3) and the "measured report, not only a demo" promise; G04 and G06 supply the evidence plan and the arm measure; the design's C1 to C5 and D1 to D6 are cited by ID on the technical deck as `SKILL.md:98-100` asks. What did not carry: a money estimate (design gap) and the review hours the platform team spends (not in the plan; marked assumption on technical slide 11).

**Numbers on slides without a source:** none without an `Evidence:` citation. Two figures rest on my own estimates rather than the record and are labelled "we estimate" or "assumption": "about four review hours" from the platform team (technical slide 11, assumption, not in the plan) and "about 250 treated starts, margin about six points" (D4 in the design, arithmetic shown). All dates after 29 October are invented and say so in the evidence line.

**Ease: 3/5.** Writing from a full record is faster than from the brief alone, and the ID citations make the technical deck honest. The checker's coverage rule for the technical audience contradicts the outline, and the word budgets and timing floor fire on every substantive slide, so the "read every warning" instruction becomes a wall of noise.

## Summary

| Stage | Helper | Exit | Warnings | Ease |
| --- | --- | --- | --- | --- |
| 2 presenter, brief only | check_deck.py | 0 | 12 | 4 |
| 3 designer, compact | check_schedule.py not run (no schedule block, compact form) | n/a | n/a | 3 |
| 4 presenter, business | check_deck.py | 0 | 10 | 3 |
| 4 presenter, technical | check_deck.py | 1 then 0 | 18, 19 | 3 |

The three fixes with the most leverage: (1) make the technical poc-approval outline and the `problem` coverage rule agree; (2) reconcile the compact form with `SKILL.md` on the schedule helper, the 1,200 words and the ticket length; (3) give the designer a cost template that works without live prices, so the presenter's cost slide is never "not yet estimated" after a design exists.
