# Delivery constraints: before/after measurement · 9 October 2026

Real teams build agent systems inside fixed time and headcount. A five-hour
demo, an internal tool built by two people at half time, a startup MVP and a
regulated production launch need different designs. This change taught the
designer and the router to size work to the people and hours available, and
measured the effect against the previous skills.

## What changed

- `adk-system-designer` asks about capacity in its scope gate: deadline and
  what happens afterwards, people and hours, ADK/GCP familiarity, money,
  users or judge, and the data touched and effects allowed.
- New [delivery profiles](../../skills/adk-system-designer/references/delivery-profiles.md)
  reference. It covers five profiles (proof of concept, assignment, internal
  tool, MVP or pilot, production) and a table of how deep each concern goes at
  each profile. It also sets a floor of protections kept even in a POC; "don't
  worry about security" lowers the depth, never the floor. It adds a capacity
  check (people × hours × focus, setup cost, a 20–30% reserve, the high
  estimate must fit) and a phased plan: phase 1 ships, phase 2 graduates, and
  a later list keeps each item with its trigger. Short work gets a compact
  form of about 1,200 words.
- The design, plan and ticket templates carry the profile, the depth per
  concern, estimates, phases, the cut line and the later list.
- `adk-engineer` builds at the goal's profile. It keeps the floor and names in
  the evidence the specialist controls it deliberately left out, with their
  triggers.

## Method

The method is the same as the [fresh-session before/after record](before-after-2026-10-09.md).
Each scenario ran in a fresh headless Claude Code session (`claude -p`, Claude
Code 2.1.294, Opus 5.5, `--setting-sources project`) with the skills copied
into the project's `.claude/skills/`. Two conditions ran: the skills before
this change (the working tree on top of commit `73599b5`) and after it. The
[runner](artifacts/delivery-constraints-2026-10-09/run.sh),
[prompts](artifacts/delivery-constraints-2026-10-09/prompts.tsv) and session
rules were identical across conditions. Headless sessions ran with permission
checks disabled, inside scratch copies only, with network, cloud and package
installs forbidden by the prompt.

| ID | Scenario | Profile expected |
| --- | --- | --- |
| D1 | Support-email triage POC, one person, 5 hours, demo tomorrow, anonymised samples | Proof of concept |
| D2 | Finance expense assistant, 40 colleagues, two engineers at half time for three weeks | Internal tool |
| D3 | Shopping assistant that places Shopify orders, three-person startup, MVP in two weeks then continue | MVP |
| D4 | Card-dispute agent for a regulated EU bank, six engineers and a security reviewer, four months | Production |
| D5 | Gong-to-Salesforce agent with no constraints given; first reply only, user available | Must ask |
| D6 | 4-hour POC that auto-sends replies from a real inbox, "don't worry about security" | POC that keeps the floor |
| E1 | `adk-engineer` carries out a 3-hour demo ticket that cancels orders on staging | Router at POC depth |

The assertions for each scenario were written into
[`evals/scenarios.json`](../../evals/scenarios.json) before any after-change
run. A separate blind grader per scenario saw outputs labelled A and B, with
the condition randomised. It scored each assertion and five 1–5 dimensions,
and the mapping was revealed after grading
([grades and outputs](artifacts/delivery-constraints-2026-10-09/round1/),
[mapping](artifacts/delivery-constraints-2026-10-09/blind_mapping.json)).

## Round 1 results

The grader preferred the after condition in **all seven** scenarios.

| Scenario | Before (of 25) | After (of 25) | Assertions passed before → after |
| --- | --- | --- | --- |
| D1 five-hour POC | 19 | 22 | 1/5 → 4/5 |
| D2 internal tool | 17 | 24 | 1/4 → 4/4 |
| D3 MVP then backlog | 19 | 23 | 0/4 → 3/4 |
| D4 regulated production | 20 | 23 | 2/4 → 4/4 |
| D5 first reply | 18 | 23 | 1/5 → 4/5 |
| D6 POC keeps the floor | 17 | 21 | 1/4 → 3/4 |
| E1 router at POC depth | 16 | 23 | 1/4 → 4/4 |
| **Total** | **126** | **159** | **7/30 → 26/30** |

| Dimension (sum over seven, max 35) | Before | After |
| --- | --- | --- |
| Constraint fit | 21 | 33 |
| Emphasis | 26 | 31 |
| Safety floor | 32 | 33 |
| Continuation | 25 | 35 |
| Usability | 22 | 27 |

The skills were already careful about safety; the change shows up in sizing
and continuation. Points the graders cited:

- **D2:** before called a 40-person internal tool a "pilot", gave 15
  engineer-days with no reserve or estimates, and pulled production controls
  into phase 1. After named the profile, computed 54 focused hours, estimated
  phase 1 at 32–43 hours and asked the user to confirm the cut line.
- **D5:** before asked about time and money but never about team size, hours,
  familiarity or real versus sample data. After asked all of them with
  one-word defaults.
- **D6:** before planned a send mode inside the four-hour POC with the broad
  `gmail.modify` scope. After wrote no send path, used a read-only scope and
  listed graduation conditions before any automatic sending.
- **E1:** before did not state its profile or list what it deferred, and in
  the grader's run its test directory raised two collection errors without
  ADK, which its report did not mention.
  After named the profile, deferred the operation ledger, ownership check and
  reconciliation with triggers, and its 19 offline tests reproduced.

Effort: before 91 turns and 27 minutes over seven sessions; after 93 turns and
30 minutes.

## Adjustments from round 1, and round 2

The graders' remaining defects led to three changes, checked by rerunning the
affected scenarios ([round 2 outputs](artifacts/delivery-constraints-2026-10-09/round2/)):

| Defect in round 1 | Change | Round 2 check |
| --- | --- | --- |
| POC designs ran to about 3,500 words in both conditions, longer than a five-hour build warrants | Compact form for short work: one file, six sections, about 1,200 words, other template sections left out | D1 3,495 → 1,784 words and D6 3,591 → 1,495, in the six compact sections, keeping the cut line, floor and graduation conditions |
| D3 phase 2 goals had no acceptance checks | Each phase 2 goal keeps its primary skill, an estimate range and one observable acceptance check | Every D3 phase 2 goal has an estimate, a primary skill, an acceptance check and a run prompt |
| D4's high estimate exceeded capacity after the reserve without saying so, and its cut list included a per-customer allowance | The high estimate must fit, or the plan names what moves when work runs high; abuse and spend limits are floor, not scope | D4 states it fits only at the low and middle of its range, gives contingency cuts in order and asks the user to confirm |

E1 also showed that `RunConfig.max_llm_calls` does not cover a demo served
through `adk web`. The floor now says to put the spend cap on the model project
in that case.

## What this establishes and what it does not

For one model, seven scenarios and one run per condition, the change produced
work that blind graders preferred in every scenario, mainly because the work
was sized to the stated people and hours and the plan continued past the first
phase. Limits:

- Seven pairs is a small sample, and each ran once.
- The graders were models, not people.
- The headless sessions answered the designer's questions with their own
  assumptions, except D5, which measured only the first reply.
- Estimates in the generated plans are the model's judgement, not checked
  against real build time.
- Round 2 was checked directly against the three fixed defects, not
  re-graded blind against the baseline.
