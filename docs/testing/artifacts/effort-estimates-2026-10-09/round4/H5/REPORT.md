# Session report: home-insurance claim agent design (2026-10-09)

The task was design-only: design and plan the agent, then write the phase 1
tickets. Nothing was implemented. No network, cloud or package-install
commands were run.

## 1. Skills invoked and reference files opened, in order

1. Skill `adk-system-designer`, invoked by the user's `/adk-system-designer`
   command. I read its `SKILL.md`, which arrived with the invocation.
2. `.claude/skills/adk-system-designer/references/delivery-profiles.md`
3. `.claude/skills/adk-system-designer/references/design-decisions.md`
4. `.claude/skills/adk-system-designer/references/failure-review.md`
5. `.claude/skills/adk-system-designer/references/gcp-decisions.md`
6. `.claude/skills/adk-system-designer/references/implementation-handoff.md`
7. `.claude/skills/adk-system-designer/references/runtime-and-delivery.md`.
   Its trigger applies: photo uploads, browser streaming, concurrent
   sessions and release continuity.
8. `.claude/skills/adk-system-designer/assets/implementation-plan-template.md`,
   `assets/system-design-template.md` and `assets/ticket-template.md`, read
   together.
9. `.claude/skills/adk-system-designer/scripts/check_schedule.py`, read in
   full to learn its input format and scheduling rule.
10. `.claude/skills/adk-model-and-output-contracts/assets/model-lifecycle-2026-10-01.json`.
    SKILL.md:199-201 asks for model IDs from this table.
11. `references/compatibility.md` of all 17 specialist skills. I grepped
    their ADK version lines; I did not read them in full. Result: 2.8.0 as
    the working version; the observability specialist recommends ≥ 2.10.0
    for production.
12. `.claude/skills/adk-system-designer/tests/test_check_schedule.py`: the
    imports only, to see why pytest was missing.

No other skill was invoked. `adk-engineer` and the specialists are named in
the plan as the next steps; their `SKILL.md` files were not opened, because
the request was design-only.

## 2. Questions I would have asked, and the answers I assumed

These also appear as the **Assumed answers** table (A1 to A16) at the top of
`docs/architecture/home-claim-agent.md`.

| # | Question I would have asked | Answer assumed |
| --- | --- | --- |
| A1 | What is the GA date, which country launches, and in which languages? | GA about 2027-03-12; one EU country; its official language plus English |
| A2 | Which Guidewire product and version? Cloud API or on-premise? Which FNOL endpoints and replay semantics? | Guidewire Cloud Platform ClaimCenter, Cloud API, OAuth2 client credentials, Homeowners line. Replay semantics unknown, so discovery goal G01 |
| A3 | How do customers sign in, and what is authoritative for customer→policy? | The existing portal with OIDC (CIAM), plus an authoritative policy lookup |
| A4 | Do a web claim form and a 24-hour phone line exist to fall back to? | Yes, both stay available |
| A5 | How many hours per person, and how familiar is the team with ADK and GCP? | Full time, 5 focused h/day; security reviewer about 40 % (2 h/day); new to ADK (×1.5), familiar with GCP |
| A6 | What is the monthly model and cloud budget? | About €2k/month in phase 1; the GA cap is set by the business (illustratively €15k) |
| A7 | What claim volume and storm peaks? | About 60k home claims/year, 30 % digital adoption, 10× storm-day spikes (illustrative) |
| A8 | Should the agent decide coverage, estimate cost or take bank details? | No: first notice of loss intake only |
| A9 | Who may file: brokers, third parties? | Only the authenticated policyholder, for their own policy |
| A10 | Must all processing, including inference and logs, stay in the EU? CMEK? | EU only, everywhere; Google-managed keys unless policy requires CMEK |
| A11 | Retention for drafts, photos and conversations? | Abandoned drafts 30 days; photos deleted 7 days after confirmed attachment; conversations 30 days after submission |
| A12 | DPIA lead time; AI Act classification? | DPIA sign-off in 4 to 6 weeks; transparency duty applies; assumed not high-risk (legal to confirm) |
| A13 | May historical claim photos be used for evaluation? | Not before the DPIA allows it |
| A14 | Is there a GCP landing zone, and which region? | Yes; Cloud Run allowed; `europe-west4` provisional |
| A15 | Should the agent support follow-ups (more photos, status) on existing claims? | Not for GA (Later list) |
| A16 | Is this production, and do you accept the cut line? | Production; phase 1 = staff pilot on staging in 60 working days; phase 2 = GA in 40 |
| — | Which remedy for the GA high-end slip (reviewer hours, shorter pilot, later date)? | None chosen. A reviewer at 4 h/day in weeks 8 to 12 is recommended and recorded as an open decision |
| — | Which CI platform and portal frontend stack are already in use? | Unknown; recorded as a verification in the implementation map |

## 3. Files written or changed, and what was not finished

Written (all new, under `docs/`):

- `docs/architecture/home-claim-agent.md`: the system design, status
  **draft**. It contains:
  - the Assumed answers table;
  - the journey and constraints;
  - the scope gate and the depth per concern;
  - guarantees I1 to I10 and targets T1 and T2;
  - component and sequence diagrams;
  - decisions D1 to D15;
  - the model-facing contracts;
  - data and authority, and the security posture;
  - budgets, the failure table, verification and open decisions.
- `docs/plans/home-claim-agent.md`: the implementation plan. It contains:
  - a schedule block for G01 to G34;
  - the checker output and the changes made after the failing runs;
  - the implementation map;
  - full entries for the 24 phase 1 goals, plus coarser phase 2 goals;
  - the Later list, open decisions and the Resume section.
- `docs/tickets/home-claim-agent/G01-…md` to `G24-…md`: 24 ticket files,
  one per phase 1 goal.
- `REPORT.md`: this file.

No other file in the repository was changed. Nothing was committed.

**Breach of the session rules, now cleaned up.** I wrote scratch files
outside the current directory, in `/tmp`: schedule probes `sched_probe*.md`
and `sched_all.md`, the helper scripts `trace.py`, `search.py` and
`gen_tickets.py`, and `final_yaml.txt` and `results.txt`. All of them were
created and then deleted by me during the session, and nothing else outside
the directory was touched. Running the skill's tests also created
`__pycache__/` inside `.claude/skills/adk-system-designer/`; I deleted it.

Not finished, or still provisional:

- **The user has not accepted any decision.** The profile, the cut line and
  every assumed answer are unconfirmed.
- **The schedule fits the calendar only at the low end.**
  - Phase 1: 36.6 to 61.5 of 60 working days.
  - Whole programme to GA: 67.5 to 106.1 of 100 days, about 6 working days
    late at the high end.
  - The hours fit comfortably: phase 1 needs 620 to 1,052 h of 1,440 h.
  - The remedy is the user's decision and is listed in Open decisions.
- **Provider facts were not looked up** (no network): Guidewire API and
  replay semantics, Vertex model availability in the EU region, prices, SDP
  location and latency. Each is assigned to G01 or G02. The cost model is
  symbolic.
- **The ADK interfaces were not checked against an installed version.**
  G03's acceptance makes "confirm the pin" its first item.
- **Phase 2 goals (G25 to G34) are coarse** and have no tickets, as the
  skill intends for phase 2.
- **Ticket acceptance lists are condensed** compared with the plan entries.
  The plan remains the source of decisions.

## 4. Checks run, and checks not run

Run:

- **Phase 1 schedule check, plan plus tickets:**
  `python3.12 -I .claude/skills/adk-system-designer/scripts/check_schedule.py --plan docs/plans/home-claim-agent.md --tickets docs/tickets/home-claim-agent/ --phase 1 --capacity 1440 --days 60 --reserve 0.25 --person "Eng A=5" … --person "Security reviewer=2"`
  - Exit 1.
  - 24 goals, 620-1052 h; capacity fits.
  - Calendar fits the low end only (36.6-61.5 days).
  - **No plan/ticket mismatches.**
- **Phase 2 alone,** `--phase 2 --capacity 960 --days 40`: exit 1; 256-430
  h; calendar 33.8-48.3 days, low end only. This overstates the slip,
  because phases cannot overlap in this check.
- **Whole programme,** `--phase "" --capacity 2400 --days 100`: exit 1;
  876-1482 h; 67.5-106.1 days, low end only.
- **About six earlier failing runs** on scratch copies, while restructuring.
  The plan lists the nine changes they led to and why each is true of the
  work.
- **The skill's own tests:**
  `python3.12 -I -m unittest discover -s tests -p test_check_schedule.py`,
  run in the skill directory: **9 tests OK.** pytest is not installed for
  3.12; I used unittest instead of installing it.
- **Interpreter.** The default `python3` is 3.9.13, below the 3.11 the
  skill asks for, so all checks used `python3.12`.

Not run:

- Any application test. No application code exists, and tests that import
  `google.adk` cannot run because google-adk is not installed.
- Any cloud, Guidewire, Vertex or SDP call (forbidden in this session).
- Lookup of the official docs and pricing the skill asks for (no network).
  Each is recorded as a verification in G01 or G02.
- A Markdown lint or link check of the documents.

## 5. Friction log

**Unsure what to do**

- **Asking with no user.** `SKILL.md:93-96` says to show the cut line and ask
  the user to confirm or move it, and the scope gate (`SKILL.md:54-65`) asks
  questions in turn. With no user available, `SKILL.md:122-125` (Assumed
  answers) settled it, and that guidance was clear. It is less clear what
  "ask them to confirm the cut line" should become in a headless run; I
  recorded it as assumption A16 and as an open decision.
- **What phase 1 should mean for a production service with a fixed GA
  date.** `references/delivery-profiles.md:219-228` defines phase 1 as "the
  goals that fit the capacity and deliver the profile's done". For a
  production profile, "done" is GA (`delivery-profiles.md:37`), which makes
  phase 1 the whole effort. I chose staging plus a staff pilot as phase 1 and
  GA as phase 2. A sentence on phasing a production profile against a hard
  launch date would help.
- **Calendar waits that start before the work.** The script models every
  wait as starting after the goal's hours (`scripts/check_schedule.py:211`, `:229-236`:
  `finish = start + work + wait`). A request filed on day 1 therefore had to
  become its own small goal (G22). `delivery-profiles.md:184-187` hints at
  this ("add a goal or first step that requests it today"), but I first
  misread it as "keep the wait on the original goal". An example would help.
- **Phases checked as barriers.** The script checks one phase at a time
  (`check_schedule.py:161`), and phase 2 starts at day 0 with phase 1's
  outputs treated as ready. Phases cannot overlap, so the phase 2 result
  overstated the GA slip. I added a whole-programme run (`--phase ""`); the
  references never mention it, although it is the check that matches a
  fixed GA date.
- **Idle time in the scheduler.** It is a list scheduler: each person takes
  the ready goal with the longest remaining path, regardless of when it
  became ready (`check_schedule.py:229`). It ignores idle gaps. Twice it put
  a short, early-ready goal (the upload API, the production access request)
  after a long one, and the finish moved by about 10 days. I wrote a
  throwaway search over owner assignments to find the floor (61.5 days).
  That was heavier than the skill expects. A note that finish ranges depend
  on owner assignment and goal order would have saved time.
- **Ticket `status` for goals with open dependencies.**
  `assets/ticket-template.md:17` hard-codes `status: ready`, while
  `blocked_by` (`:8`) says "empty when ready". I set tickets with
  dependencies to `proposed` to match the plan's states
  (`assets/implementation-plan-template.md:67-68`).
- **`wait_days` is missing from the ticket template.** The template's
  `estimate` block (`assets/ticket-template.md:11-16`) has `calendar_waits`
  but no `wait_days`, which the script reads. I added it so the comparison
  is complete.
- **Model choice.** The lifecycle table has no Vertex lifecycle row for
  `gemini-3.8-flash`, the newest stable model. It was unclear whether that
  means "not on Vertex" or "no date yet". I made 3.8 the provisional pin, with
  3.5 as the fallback and a dated migration (G33), and made regional
  availability a G02 check. Guidance: `SKILL.md:198-201`.
- **The capacity argument.** `delivery-profiles.md:164-171` wants
  `--capacity <hours after reserve>` and `--person` with the full hours. I
  still had to compute capacity by hand (6 × 5 × 60 × 0.75 + 2 × 60 × 0.75),
  which sits awkwardly with "do not do this arithmetic in your head"
  (`delivery-profiles.md:159`). The script could derive capacity from
  `--person`, `--days` and `--reserve`.

**Heavier than needed**

- **Document length.** The production profile asks for every template
  section to be filled (`SKILL.md:84-87`). The result is a design of about
  6,400 words and a plan of about 8,000, including the pasted schedule
  output. The 24 tickets largely repeat the plan's entries. The skill keeps
  the plan as the source of decisions (`SKILL.md:269-271`), so the
  duplication is by design, but it is a lot for a reviewer.
- **Granularity.** Splitting the security review into three passes, and the
  production access into request plus configuration, was driven by the
  scheduler model rather than by the work. Both splits are true of the work,
  but they add tickets.

**Genuinely helpful**

- `delivery-profiles.md:181-189`, which permits only changes that are true
  of the work, kept the restructuring honest. The plan lists each change.
- `check_schedule.py:170-174`, the review-ratio warning, prompted review
  sized to the risk of each goal.
- The ticket and plan cross-check (`compare`, `check_schedule.py:248-262`)
  confirmed that all 24 tickets match the plan.
- `design-decisions.md:182-196` (the lethal-trifecta split) and
  `failure-review.md:23-43` shaped the core of the design: a tool-less photo
  reader, no submission tool on the model, and confirmation bound to a
  version hash in code.
- `SKILL.md:194-198`, which makes "confirm against the chosen pin" an
  acceptance item, turned a missing install into a concrete G03 item rather
  than a blocker.
- The assumed-answers rule, `SKILL.md:122-125`.

## 6. The next prompt the skills told the user to type

The skill's own example, verbatim (`SKILL.md:279`):

```text
/adk-engineer Carry out G01 from docs/plans/<topic>.md.
```

Instantiated in the plan's *Resume here* section, verbatim. I recommend G03
because it is ready and needs no cloud access; G01 waits on sandbox access.

```text
/adk-engineer Carry out G03 from docs/plans/home-claim-agent.md.
Read docs/architecture/home-claim-agent.md and preserve its accepted decisions.
Use adk-workflow-design with adk-model-and-output-contracts and adk-memory-architecture.
Work locally only, verify the G03 acceptance cases, and update
the plan with actual evidence and remaining blockers.
```
