# Report: advertiser campaign assistant, design and phased plan

## 1. Skills invoked and reference files opened, in order

1. Skill `adk-system-designer`, invoked by the user's `/adk-system-designer`
   command. Its `SKILL.md` was loaded by the invocation.
2. `.claude/skills/adk-system-designer/references/delivery-profiles.md`
3. `.claude/skills/adk-system-designer/references/design-decisions.md`
4. `.claude/skills/adk-system-designer/references/failure-review.md`
5. `.claude/skills/adk-system-designer/assets/system-design-template.md`
6. `.claude/skills/adk-system-designer/assets/implementation-plan-template.md`
7. `.claude/skills/adk-system-designer/references/implementation-handoff.md`
8. `.claude/skills/adk-system-designer/references/gcp-decisions.md`
9. `.claude/skills/adk-system-designer/assets/plan-review-prompt.md`
10. `.claude/skills/adk-system-designer/scripts/check_schedule.py`: lines 1–140, then 160–320 to learn the grid, contract and phase-matching rules, then a grep of its CLI arguments
11. `.claude/skills/adk-model-and-output-contracts/assets/model-lifecycle-2026-10-01.json`, used to choose the model ID
12. A grep across `.claude/skills/*/references/compatibility.md` for the ADK version (all say 2.8.0)
13. `.claude/skills/adk-system-designer/assets/ticket-template.md`: first 5 lines only. Tickets were not requested, so none were written

Not opened: `references/runtime-and-delivery.md`. Its trigger (context limits,
result downloads, browser streams, concurrency, release continuity) did not
apply to this journey. No specialist skill was invoked, because no code was
requested. One subagent (general-purpose) ran the independent plan review
using `assets/plan-review-prompt.md`.

## 2. Questions I would have asked, and the answers I assumed

They are also in the design's "Assumed answers" table (Q1–Q12) and open decisions (O1–O7).

| # | Question | Assumed answer |
| --- | --- | --- |
| Q1 | Is the pilot continued after three weeks? | Yes. Phase 1 code is kept |
| Q2 | Is the engineer full time? How familiar with ADK and GCP? | Full time for 15 working days at 4.8 focused h/day (8 × 0.6). Knows GCP, new to ADK (×1.5 on estimates) |
| Q3 | Model and cloud budget? | Small pilot allowance, assumed under USD 500 a month, with a billing alert |
| Q4 | Who uses and judges it? | Five external advertisers on a web page. The pilot owner judges completed purchases and support load |
| Q5 | What does a booking order commit? | A binding commercial commitment (money), so treated as irreversible |
| Q6 | How does the IdP identify an advertiser? | OIDC `sub` plus an org claim, and a reviewed pilot table from org to brands |
| Q7 | Do rights depend only on owner, brand and channel? | Yes for phase 1. Territory and dates are open decision O1 |
| Q8 | Where does asset metadata come from, and how many assets? | The rights system or DAM; under a few thousand per brand and channel |
| Q9 | Are there staging environments? | Rights read API usable for the pilot; booking staging exists |
| Q10 | Can sales ops place orders by hand during the pilot? | Yes, within one business day. **The cut line depends on this** |
| Q11 | Is there an existing advertiser portal? | No. The pilot gets a minimal page of its own |
| Q12 | Region, retention, required approvals? | One existing region; 90-day conversation retention; a security review of the design and a commercial go-live approval are required |
| O1 | Do rights also depend on territory, dates or modification? | No (phase 1) |
| O2 | Can the rights and booking APIs take per-advertiser credentials? | Unknown; service credentials are assumed |
| O3 | Catalogue size per brand and channel? | Under about 2,000 assets |
| O4 | Retention of purchase requests under the commercial terms? | Kept as commercial records; settled through W6 |
| O5 | Booking replay key, lookup and timeout semantics? | Unknown; phase-2 discovery G07 |
| O6 | Does sales ops accept manual placement in phase 1? | Yes (Q10) |
| O7 | Does the security review need the built system? | No, a design review only |
| — | Should the cut line be manual placement in phase 1, with go-live after the build window? | Recommended and assumed |
| — | Is the build window 15 or 17 days? | 15 as stated. The plan shows that 17 fits |

## 3. Files written or changed, and what was not finished

Written:
- `docs/architecture/advertiser-campaign-assistant.md`: the design. It contains assumed answers, journey, depth and floor, requirements R1–R5, contracts C1–C11 with all six fields, decisions D1–D10, model-facing interfaces, data and authority, security posture, budgets, coverage and action grids, failure scenarios, verification, and open decisions O1–O7.
- `docs/plans/advertiser-campaign-assistant.md`: the plan. It contains the summary, capacity, the machine-readable schedule (waits W1–W11, goals G01–G12), what-ifs, the implementation map, full phase-1 goals G01–G06 and G12 with acceptance cases, short phase-2 goals G07–G11, the later list, the change table and the settled plan-review findings.
- `REPORT.md`: this file.

Not changed: anything outside `docs/` and this report. The scratch copies
for what-ifs went to `/tmp/k1-whatif*`, and the review subagent's copies to
`/tmp/k1-review/`. Both are outside the project.

Not finished:
- **The plan does not fit a 15-day calendar at the high end.** The build finishes in 9.4–16.5 working days. A 17-day window fits. Go-live, which comes after the approval wait, falls at 12.7–22.3 days. The user has not confirmed the cut line or the window.
- Both documents are **draft**. No assumption was confirmed by the user.
- Provider facts were not verified, because network access was not allowed: Vertex prices and regions, the Vertex lifecycle row for `gemini-3.8-flash`, ADK API names at the pin (`DatabaseSessionService`, `RunConfig.max_llm_calls`, `ToolContext.state`), and the ADK tool-confirmation limitations. Each is an acceptance item in G01 or G02.
- No tickets were written, because none were requested. No code was written, because none was requested.

## 4. Checks run and checks not run

Run:
- `python3.11 -I .claude/skills/adk-system-designer/scripts/check_schedule.py --plan docs/plans/advertiser-campaign-assistant.md --design docs/architecture/advertiser-campaign-assistant.md --days 15 --reserve 0.25 --person "Engineer=4.8"`:
  - First run: 33–55 h of 54 h, finish 9.39–16.06 days, exit 1.
  - After the cuts: 32–53 h, 9.11–15.5 days, exit 1.
  - After settling the review findings (final): **33–53 h of 54 h, fits on hours; finish 9.39–16.5 working days; calendar fits at the low end only; exit 1**. The grid citations are valid, and all 11 of 11 contracts are cited.
- The same command with `--days 17`: fits, **exit 0**.
- The same command with `--phase ""` (all phases): 56–96 h, no grid or contract problems, exit 0.
- What-if runs on copies (quoted in the plan's what-if table): 16 days, 17 days, 0.7 focus, go-live inside phase 1, automated booking in phase 1, and an earlier W5 (not adopted, because shortening a wait is not allowed without its owner).
- `python3.11 -m unittest discover -s tests` in the designer skill: 18 tests, OK. pytest is not installed, so I used unittest.
- Independent plan review by a fresh-context subagent: 18 findings, all settled in the plan's change table.

Not run:
- Any test that imports `google.adk`. ADK is not installed and no application code exists.
- Any live, cloud, network or IdP check.
- `python3` (the default 3.9.13) was not used for the helper. I used `python3.11` from `/opt/homebrew/bin` instead.

## 5. Friction log

- **Unsure about the scope gate in a headless run.** `SKILL.md:54` says to open with the scope gate, and `SKILL.md:52` says to let the user answer. `SKILL.md:125` ("keep asking nothing further: put an **Assumed answers** table") resolved it. Helpful once found, but it comes about 70 lines after the gate instruction.
- **Unsure whether to run the independent review.** `SKILL.md:280` requires it for "several people or a production service", and `SKILL.md:286` exempts "a single-person proof of concept". A single-person *pilot* with external users and money falls between the two. I ran it, and it was the most valuable step: it found the W6 ordering and the W1-needs-URL dependency, which moved go-live from about 16 to about 22 days.
- **Tension in the fit rule.** `references/delivery-profiles.md:248` says phase 1 fits only when the high end is within capacity. `delivery-profiles.md:249` allows "If only the low end fits, say so and name the goals that move". The helper's exit 1 on "calendar: low end only" made me treat it as not fitting. I then had to choose between more cuts and a stated remedy. I chose the remedy (17 days) and the moved cut line (go-live after the build).
- **Python version.** `delivery-profiles.md:233` asks for Python 3.11 or later. The default `python3` was 3.9, and I had to find `python3.11` myself. The command at `delivery-profiles.md:180` uses `$SKILL_DIR`, which was not set, so I substituted the path.
- **Undocumented helper format details.** I had to read `scripts/check_schedule.py` around lines 180–255 to learn that goal text comes only from headings that start with the goal ID, and that acceptance items must start a line (`- A1`). I also learned that `--phase` matches exactly, so `1b` works for a go-live sub-phase. Without that read, a plain "A1:" inside a paragraph would silently fail the grid check.
- **Helpful but suspiciously close.** `references/design-decisions.md:35–44` has a worked contract decomposition for this exact domain: an advertiser's assistant with rights, quote, confirmation, idempotency and status. It sped up C1–C6 a lot. It also includes territory and dates, which the request does not, so I recorded that difference as O1 rather than copying it.
- **Helpful.** `delivery-profiles.md:200–212` ("Do not remove a dependency, shorten a wait…"; "run every remedy … as a what-if") stopped me from adopting the W5-shortening what-if as a fix. The `n/a: <reason>` rule at `failure-review.md:30` made the reviewer's wrong-n/a findings (#12, #14) easy to locate.
- **Heavier than needed.** The plan reached about 6,100 words and the design about 5,000. The review settlement and what-if tables add length. `delivery-profiles.md` sets no word count for a pilot, but the "one page summary" was hard to keep short with three caveats on the finish date.
- **Template placeholder.** The run prompt at `assets/implementation-plan-template.md:111` says "verify its acceptance cases locally". That does not fit G02, G06 and G12, which need hosted or live evidence. I kept the wording for G01–G05 and dropped "locally" for G12.

## 6. The exact next prompt the skills told the user to type

The skill (`SKILL.md`, "Deliver and hand off") gives the template
`/adk-engineer Carry out G01 from docs/plans/<topic>.md.` Filled in for this plan:

```text
/adk-engineer Carry out G01 from docs/plans/advertiser-campaign-assistant.md.
```

---

# Revision 2 (2026-10-15): rights also depend on territory, flight dates and modification

## R2-1. Skills invoked and files opened, in order

No new skill was invoked. Work continued under the already-loaded
`adk-system-designer` instructions, specifically "Contracts evolve" (revise C1
in place with a one-line note and list what it changes) and "When revising an
existing design or plan … list every … item you removed or weakened".

1. `docs/architecture/advertiser-campaign-assistant.md`: reread in full, because the harness reported it changed on disk. The content matched my last edits.
2. `docs/plans/advertiser-campaign-assistant.md`: the goal sections G01, G03 and G05, and grep-located lines.
3. `.claude/skills/adk-system-designer/scripts/check_schedule.py`: run only, not reread.
4. `.claude/skills/adk-system-designer/assets/plan-review-prompt.md`: reused (adapted to focus on revision 2) for a second fresh-context review subagent.

No reference file was reopened. The relevant guidance (`delivery-profiles.md`
on waits, what-ifs and the change table; `failure-review.md` on grid cells;
`design-decisions.md:48–51` on revising C1) was already in context.

## R2-2. Questions I would have asked, and the answers I assumed

| # | Question | Assumed answer |
| --- | --- | --- |
| Q13 / O8 | Are grant and flight dates inclusive, and in what timezone? | Calendar dates, both ends inclusive, no timezone conversion. The boundary tests are provisional until W12 answers |
| Q14 / O8 | How are territories expressed? | ISO 3166-1 alpha-2 codes, no regions, with an alias table for names like "UK" |
| Q15 / O9 | Is modification a yes/no flag or levels? Do pilot campaigns need it? | Yes/no. **Pilot campaigns use creatives as-is**, so modification requests move to phase-2 G13 |
| Q16 / O10 | Does the rights API return grant records or a coverage check? | Grant records; coverage is computed in our code (D11) |
| Q17 / O12 | Does booking price and hold inventory per territory? | Yes |
| O11 | Who acts when rights are revoked during a live flight? | Outside the assistant (rights and delivery teams) |
| — | Does "approval required" also apply to rights? | No. The user's update named only territory, dates and modification |
| — | How long does the new wait W13 (aligned rights and booking test data) take? | 3–5 days, matching the other inter-team waits. This is an assumption; the reviewer modelled 3–8 days |
| — | Accept a 19-day build window, 17 days with 0.7 focus confirmed, or a cut? | Not decided. Recommended: 19 days. No 15-day option keeps the rights checks and their evidence |

## R2-3. Files changed, and what was not finished

- `docs/architecture/advertiser-campaign-assistant.md`:
  - Status note; Q7 is marked as answered by the user; new Q13–Q17.
  - Journey, facts and model/code split; R1 widened and new R6.
  - C1 revised in place: six fields, one function, recheck at propose and export, no search before the terms are known.
  - C4 payload widened; C7 now defines confirm and export outage behaviour; new C12 (the rights terms snapshot travels with the request).
  - D8 revised; new D11 (union-coverage function) and D12 (as-is only in phase 1).
  - Diagram, sequence, tool signatures and instruction updated.
  - Four failure scenarios replace one; the action grid cites the new G05/A10.
  - O1 resolved; new O8–O12; new "Revision 2" table.
- `docs/plans/advertiser-campaign-assistant.md`:
  - Status line, summary, phase table and what-if table recomputed.
  - Schedule: G01 7–11, G03 7–13, G05 6–9, G06 5–8. New waits W12 (rights semantics) and W13 (aligned test data). W2, W3 and W9 widened.
  - New phase-2 goal G13 (modification requests).
  - Acceptance widened: G01/A2, G01/A5, G03/A1, G03/A2, G03/A5, G05/A2, G05/A3, G05/A8, G06/A1. New: G01/A6, G03/A6, G05/A10.
  - Evaluation set 20–25 cases with a cap of 25 × 3. Export runs as a Cloud Run job.
  - Later list: the built "territory/date/modification" row removed and a takedown row added. Map and open-decision pointers updated.
  - Revision-2 change table and the settled review table (16 findings); the resume prompt now says A1–A6.
- `REPORT.md`: this appendix.

Not finished:
- The plan **does not fit 15 days**: build 10.6–18.5 working days, go-live 13.8–24.3. Both documents remain draft, pending the user's choice of window and confirmation of Q13–Q17.
- No provider facts were verified, because network access was not allowed.

## R2-4. Checks run, and checks not run

Run, all `python3.11 -I .claude/skills/adk-system-designer/scripts/check_schedule.py --plan … --design … --reserve 0.25 --person "Engineer=4.8"`:
- After the first revision-2 edit (`--days 15`): 38–58 h of 54 h; finish 10.56–17.33; low end only; exit 1. One review item: G01 mentions W12. It was settled as `mentions_only`, because G01 builds on the assumptions.
- After settling the review (final, `--days 15`): **38–63 h of 54 h; finish 10.56–18.5; low end only; exit 1**; 12 of 12 contracts cited; no grid problems.
- `--days 19`: fits, **exit 0**. `--phase ""`: no grid or contract problems, exit 0.
- What-ifs on copies in `/tmp/k1-r2b-*.md`: 18 and 19 days; 0.7 focus at 15, 16 and 17 days; modification in phase 1 with G06 waiting for G13 (15, 20 and 21 days); go-live inside phase 1 (15, 24 and 25 days); automated booking in phase 1 (15, 24, 25, 26 and 27 days). Figures are quoted in the plan's what-if table.
- Independent review of revision 2 by a fresh-context subagent: 16 findings, all settled in the plan's revision-2 review table.

Not run: any `google.adk` test (not installed, and no code exists), any live, network or cloud check. The designer's own unittest suite was not rerun, because the helper script did not change.

## R2-5. Friction log (revision 2)

- **Helpful.** `.claude/skills/adk-system-designer/SKILL.md` ("Contracts evolve", line 186) told me exactly what to do: revise C1 in place, add a one-line note, and list the decisions, goals and tests it changes. The original design already had a "C1 note" anticipating this revision, which made the blast radius easy to enumerate.
- **Helpful.** `references/design-decisions.md:48–51` ("When a later discovery adds a rights condition … revise C1, note the revision, and update the filter, the recheck and their tests together") is nearly this exact scenario.
- **Unsure.** The skill does not say whether a *revision* needs another independent review. `SKILL.md:280–286` covers handing over a plan, and the revision section covers only the change table. I ran one, and it was worth it: two wrong what-if claims (19 versus 21 days; 0.7 focus), an untested check point (`propose_purchase`), undefined outage behaviour at confirm and export, missing test data (W13), and a stale continuation prompt (A1–A5) that my own "nothing weakened" note had missed.
- **Unsure.** Settling a mention that hides assumption risk (G01 builds on Q13 and Q14 while W12 is pending). `delivery-profiles.md:229–232` covers "does either goal need the other" but not "proceeds on an assumption with rework risk". I kept `mentions_only` and put the rework hours on G03 (0–2 h) with a re-verification item (G03/A6).
- **Heavier than needed.** The plan now carries three change and review tables (revision 1 cuts, revision 1 review, revision 2 plus its review), about 60 rows. `delivery-profiles.md:340` says one row per change, which I followed, but the plan keeps growing with each revision.
- **Friction.** A multi-replace Python edit failed on its final assert (a sentence already inside a replaced block), so nothing was written. Asserting before writing protected the file, but cost one rerun.

## R2-6. The exact next prompt

Unchanged from the skill's template in "Deliver and hand off":
`/adk-engineer Carry out G01 from docs/plans/<topic>.md.`. Filled in:

```text
/adk-engineer Carry out G01 from docs/plans/advertiser-campaign-assistant.md.
```
