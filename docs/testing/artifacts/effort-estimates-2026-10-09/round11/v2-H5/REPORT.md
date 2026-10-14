# Report: home-insurance claim intake agent, design and phase 1 tickets

Design and plan only. No application code was written, nothing was
installed, and no network or cloud command was run.

## 1. Skills invoked and reference files opened, in order

Skill invoked: `adk-system-designer`, through the user's slash command; its
`SKILL.md` was loaded. No other skill was invoked through the Skill tool.

Files opened, in order (paths under `.claude/skills/`):

1. `adk-system-designer/references/delivery-profiles.md`
2. `adk-system-designer/references/design-decisions.md`
3. `adk-system-designer/references/failure-review.md`
4. `adk-system-designer/references/gcp-decisions.md`
5. `adk-system-designer/references/implementation-handoff.md`
6. `adk-system-designer/assets/system-design-template.md`
7. `adk-system-designer/assets/implementation-plan-template.md`
8. `adk-system-designer/assets/ticket-template.md`
9. `adk-system-designer/assets/plan-review-prompt.md`
10. `adk-system-designer/scripts/check_schedule.py` (read in full, then run many times)
11. `adk-system-designer/references/runtime-and-delivery.md`
12. `adk-model-and-output-contracts/assets/model-lifecycle-2026-10-01.json`
13. The first matching lines of every `*/references/compatibility.md`, from a grep for the ADK version pin (all say `google-adk` 2.8.0)
14. `adk-system-designer/tests/test_check_schedule.py` (header only, then run)

The independent plan review was sent to a general-purpose subagent with a
fresh context, using `assets/plan-review-prompt.md` with the paths filled in.

## 2. Questions I would have asked, and the answers I assumed

Q1–Q14 are recorded with the decisions that depend on them in the design's
"Assumed answers" table (`docs/architecture/home-claim-intake.md`).

| # | Question | Assumed answer |
| --- | --- | --- |
| Q1 | Start and GA dates; continued after GA? | Start 2026-10-19, GA 2027-03-15, 95 working days; continued |
| Q2 | ADK/GCP familiarity; full time? | Experienced on GCP, new to ADK (×1.5); 5 focused h/day each; security reviewer about 1 h/day |
| Q3 | Which Guidewire product and version, and how do we reach it? | ClaimCenter on Guidewire Cloud, Cloud API; non-prod access by request |
| Q4 | Markets and languages at GA? | Germany only; German and English |
| Q5 | Sign-in and channel? | Existing OIDC customer identity provider (CIAM) and React portal, which the team may change |
| Q6 | Volume and peaks? | About 2,000 claims/month; storm peaks of 10× for 2–3 days |
| Q7 | Budget? | Non-prod capped at €3,000/month; production cost per claim approved before GA |
| Q8 | Data allowed? | FNOL fields and photos only; no bank or health details |
| Q9 | What may it change? | Creates one claim per confirmed draft and attaches its photos; no coverage, payment or liability decisions |
| Q10 | Who approves GA? | Claims operations, the DPO, security and the change board |
| Q11 | GCP landing zone and region? | Existing organisation with an EU-only location policy |
| Q12 | AI Act classification? | Not high-risk; transparency duty applies; legal to confirm |
| Q13 | Is there a classic form to fall back to? | Yes; it can accept a prefilled draft after a small portal change |
| Q14 | CMEK required? | No at GA |
| Q15 | Accept residual risks R1–R3 (coverage statements prevented by instruction and evaluation only; no photo-authenticity check; single region)? | Assumed accepted as provisional, with owners named in the design |
| Q16 | How long do the outside waits take (W1–W18)? | The ranges in the plan; all are assumptions |
| Q17 | The plan fits 95 days only at the low end. Move GA to 2027-03-25, or accept the risk? | Not decided. GA on 2027-03-25 is recommended; the date stays an open decision |
| Q18 | Move the cut line up (G30, G32 into phase 1)? | Not moved; offered |
| Q19 | Can Guidewire non-prod be reached through the integration team's existing network path? | Yes, for G25 only; staging needs its own allowlist (W15) |
| Q20 | How long does a CIAM access token live (this bounds how long a revoked token works)? | 5 minutes or less; G39/A2 records the real value |

## 3. Files written or changed, and what was not finished

Written (all new; nothing outside `docs/` and this file was changed):

- `docs/architecture/home-claim-intake.md`: the design. Draft status;
  decisions D1–D16; invariants I1–I7 and targets T1–T3; coverage and
  action grids; security posture; open decisions.
- `docs/plans/home-claim-intake.md`: the plan. Summary; load table; 18
  calendar waits; schedule block for phases 1 and 2; change and what-if
  table; implementation map; goals table; phase 2 goals; later list;
  continuation prompt.
- `docs/tickets/home-claim-intake/`: 33 phase 1 tickets (G01–G26,
  G33–G39).
- `REPORT.md`: this file.

A temporary `tests/__pycache__/` that the unit-test run created inside the
skill folder was deleted. Scratch copies are under `/tmp/h5sched` and
`/tmp/planreview`, outside the repository.

Not finished:

- **The plan does not fit the stated date at the high end.** It finishes in
  67.27–102.47 working days against 95. The user has to choose: GA on
  2027-03-25 (fits), or accept the risk.
- Every provider fact is unverified because no network lookup was allowed:
  - Vertex AI regional availability of `gemini-3.8-flash` and Model Armor
    in the EU;
  - the Guidewire Cloud API endpoints and dedup header;
  - prices.

  Each fact is assigned to an acceptance item: G02/A6, G12/A2, G01, G25 and
  G20/A1.
- Phase 2 goals have no tickets; per the skill, they wait until phase 1 has
  run.
- The plan is unreviewed by the user. The independent review was settled
  once and was not repeated after its fixes.
- No commit was made.

## 4. Checks run and checks not run

Run:

- **`check_schedule.py` on the final plan.** Command:
  `python3.11 .claude/skills/adk-system-designer/scripts/check_schedule.py --plan docs/plans/home-claim-intake.md --tickets docs/tickets/home-claim-intake/ --design docs/architecture/home-claim-intake.md --days 95 --reserve 0.25 --person "Eng A=5" … --person "SecRev=1"`.
  Result:
  - 51 phase 1 entries (33 goals and 18 waits), 573–853 h;
  - capacity 2,208.75 h, fits;
  - finish 67.27–102.47 working days, **calendar fits at the low end only**;
  - no PROBLEM lines; every grid cell cites an existing acceptance item;
    tickets match the plan;
  - **exit 1**.

  The same command with `--days 103` exits 0.
- **Earlier helper runs and what-ifs.** About 25, all recorded one row each
  in the plan's change table. The first draft passed (62.93–94.87). It was
  revised after the independent review.
- **The helper's own unit tests.** `python3.11 -m unittest discover -s
  .claude/skills/adk-system-designer/tests`: 16 tests, OK.
- **Independent plan review (subagent).** It found 17 missing
  prerequisites, 4 mention-only problems, 7 unsupported claims and 10
  coverage gaps. All were settled in the plan's change table, rows R-…; the
  helper was rerun afterwards.
- **Relative-link check** over the design, plan and tickets: 0 broken links.

Not run:

- **Application tests.** There is no application code, and `google-adk` is
  not installed, so nothing that imports `google.adk` could run.
- **Every acceptance item in every ticket.** They are planned, not executed.
- **Provider and documentation lookups.** Network was disallowed.
- **A second independent review** of the revised plan.
- **The helper under the default `python3` (3.9.13).** I used
  `python3.11`, which was available.

## 5. Friction log

- **Unsure: is phase 1 all of GA, or a pilot first?** For a fixed GA date,
  `delivery-profiles.md:254-261` ("Phase 1, ship: the goals that fit the
  capacity") doesn't say whether phase 1 should be an earlier pilot or the
  whole GA. I chose phase 1 = GA, which made 33 tickets.
- **Unsure: where does a goal's route live?** `delivery-profiles.md:155-158`
  says each ticket "links to the plan for the route and rationale instead of
  repeating them". `delivery-profiles.md:313-316` says the ticket is the
  home of "scope, route and acceptance". I followed the second. The ticket
  template has no route or integration-points field
  (`assets/ticket-template.md:27-32`), so routes went into Scope.
- **Unsure: what goes in a ticket's `calendar_waits` field?** The template
  asks for "<none, or what and how long>" (`assets/ticket-template.md:15`),
  but `delivery-profiles.md:124-127` models waits as separate W entries. I
  wrote `none` in the tickets and kept the waits as W entries.
- **Unsure: which Python?** `delivery-profiles.md:173` shows `python3`, and
  `delivery-profiles.md:223-224` says to report the schedule as unchecked
  without Python 3.11. The default `python3` here is 3.9.13; I found
  `python3.11` and used it. A shebang or version note in the command would
  remove the doubt.
- **Heavier than needed: false-positive approval matches.** The mention
  scan matched "credentials from" in "OAuth client credentials from Secret
  Manager" (`scripts/check_schedule.py:34`) and "security review" inside
  "security reviewer" (`scripts/check_schedule.py:32`). Each needed a
  `mentions_only: [wait]` entry.
- **Heavier than needed: every "Out: … (G12)" pointer.** Each one also
  needed a `mentions_only` entry (`delivery-profiles.md:213-222`). There
  were 13 settled entries by the end.
- **Heavier than needed: document length.** The design is about 5,900 words
  and the plan about 5,500 including the schedule block. That is long next
  to `delivery-profiles.md:323-333`, though most of it is the grid, the
  waits and the schedule block. 51 schedule entries are hard to read in
  YAML.
- **Gap: the helper can't model partial overlap.** "Build against a fake,
  verify live later" had to become separate goals (G01/G25, G03/G39,
  G16/G37, G08/G34) to show in the schedule. That multiplied the tickets.
- **Gap: the helper's checks can't see the worst missing dependencies.**
  They never caught the reviewer's most damaging finding: the production
  egress IP was only applied in G22, after the W7 it was needed for. They
  can't see a prerequisite stated only inside one goal's verification line.
- **Genuinely helpful: the "Assumed answers" rule.** `SKILL.md:124-128` told
  me exactly what to do with no user present.
- **Genuinely helpful: the dated lifecycle table.** `SKILL.md:200-203` and
  `adk-model-and-output-contracts/assets/model-lifecycle-2026-10-01.json:13-14`
  showed that `gemini-3.7-flash` (Vertex retirement 2027-01-28) and
  `gemini-3.6-flash` (2026-11-19) retire before GA. A default from memory
  would have picked one of them.
- **Genuinely helpful: the schedule helper and its rules.**
  `delivery-profiles.md:165-203` and the helper turned "fits" into a checked
  claim. Its REVIEW lines found three real hidden prerequisites: G12 needed
  G09, G14 needed G15, and the pen-test retest W8 was missing.
- **Genuinely helpful: the grid checker.** `failure-review.md:29-35` with
  `--design` caught stale citations (G12/A6) after a goal split.
- **Most valuable: the independent review.** `SKILL.md:248-254` and
  `assets/plan-review-prompt.md:8-35` produced the review. It overturned a
  "fits" that I would otherwise have reported, moving 94.87 days to
  102.47. It took about 8 minutes of subagent time.

## 6. The next prompt the skills told the user to type

The plan's "Resume here" section and the G02 ticket (from
`assets/ticket-template.md:53-57`) give it verbatim:

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G02-agent-service-skeleton.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
