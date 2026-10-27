# Triage: engineer group (batches eng1, eng2)

Loading note: eng1/eng2 were judged before the runner counted a leading `/skill` as loading it.
Prompts starting with `/adk-engineer` (missing-companion, checkpoint-after-delta, resumes,
writes-progress) did load adk-engineer by slash command (the agents opened
`adk-engineer/references/ticket-lifecycle.md`, which only SKILL.md names). The plain-prompt
runs (chosen-test-first, both guardrails continuation/escalation) loaded no skill at all: each
began with `Glob **/*` and went straight to the code.

| Scenario | A# | Votes | Class | Evidence | Proposed action |
| --- | --- | --- | --- | --- | --- |
| router-missing-specialist | A3 | FFF | c | adk-engineer loaded (Skill tool); SKILL.md "If a selected specialist is unavailable, name the missing skill and show: `npx skills@latest add ... --skill <specialist-name>`" — final.md names adk-memory-architecture but gives no command. | none (variance) |
| router-missing-specialist | A5 | FFF | c | SKILL.md: "Continue independent inspection, and resume specialist-dependent work once its instructions are available." Agent wrote app/tools/preferences.py, store and tests anyway. | none |
| router-builds-at-poc-depth | A3, A4 | PFP, PFP | c | split votes; passed by majority | none |
| engineer-ticket-with-missing-companion | A3 | FFF | b | Lint/theme checks need npm and a shell (fixture note says so); agent also chose not to theme because shadcn is absent ("no DESIGN.md tokens in index.css"). Assertion has no "or reports not run" escape. | flag the assertion (running checks is impossible here); theming skip is (c) |
| engineer-ticket-with-missing-companion | A4 | FFF | c/b | Ticket Evidence has "C3: planned ... tier not run", "SB10: planned ... tier not run" — one line each, honest since nothing ran; judge wanted a tier. Also G02's Evidence cited `tests/test_stream.py`, absent from the fixture (agent flagged it). | fixture fixed (test_stream.py added); assertion should accept "not run" as the tier when nothing ran |
| engineer-ends-with-checkpoint-after-contract-delta | A1 | PFP | c | passed by majority | none |
| engineer-ends-with-checkpoint-after-contract-delta | A2 | FFF | b | final.md: "nothing has been run ... C1/C2 Evidence cells still planned:" — correct per ticket-lifecycle (cells change only for evidenced contracts); with no shell nothing can be evidenced, so the assertion's second half cannot pass honestly. | flag the assertion: accept cells left `planned:` when no acceptance case ran |
| engineer-ends-with-checkpoint-after-contract-delta | A3 | FFP | c | Checkpoint prompt lists deltas, rulings and the 6 h overrun; omits phase fit. Judges split on whether phase fit was required. | none (variance) |
| engineer-resumes-from-progress-block | A2 | FFP | b | Worktree `../wt-G02` is outside the workspace (Read denied, permission_denials) and there is no shell for `git status` or the re-verify command; agent reported both as not possible. | fixture: put the worktree inside the workspace (`wt-G02/` with app/stream.py, tests/test_stream.py) and change the context's `../wt-G02` to `wt-G02`; flag A2 (git status needs a shell) |
| engineer-resumes-from-progress-block | A3 | FFF | b | Agent stopped because the uncommitted A1 work was unreachable ("Rewriting app/stream.py ... would have risked overwriting the uncommitted A1 work"), the behaviour the lifecycle asks for. | same fixture fix; A3 then becomes reachable |
| engineer-parallel-tickets-with-overlapping-touches | A3 | FFF | c | ticket-lifecycle.md:129-131 describes "one worktree per ticket ... `git worktree add ../wt-G03 -b G03 <base>`"; agent read that file but only said worktrees couldn't be created, and built both tickets sequentially. | none |
| chosen-test-first-workflow | A1 | FFF | b+c | The selected `tdd` skill is not in this repo (`skills_missing: [tdd]`), so "combining" it is impossible; agent also never loaded safe-api-tool-calls although its description fits ("ambiguous write outcomes, unsafe tool replay") and it globbed the SKILL.md files. | flag (external skill absent); loading miss is (c) |
| chosen-test-first-workflow | A2 | FFF | b | Test written and hand-traced; demonstrating it fails needs a shell. | flag the assertion: "or reports the red step as not run" |
| chosen-test-first-workflow | A3 | FFF | c | safe-api SKILL.md:35/63 covers "trusted business identity, payload binding" and reconciliation; skill not loaded. | none (root cause: not loaded) |
| chosen-test-first-workflow | A4 | PFF | c | safe-api SKILL.md:51 "retain a single attempt and an honest uncertain result"; not loaded; split votes. | none |
| guardrails-continuation-accounting-and-duplicates | A2 | FFF | a | Guidance exists (live-campaigns.md:66 "Atomically reserve an attempt in a shared ledger"), but the skill was never loaded. Description names "token budgets ... application cost controls" but nothing about paid continuations, attempt ledgers or lost responses. | description: add paid continuation / attempt-ledger wording |
| guardrails-continuation-accounting-and-duplicates | A4 | FFF | a | live-campaigns.md:114-117 defines reservations, unknown holds and remaining allowance separately; not loaded (same description gap). | as above |
| guardrails-escalation-two-sided-calibration | A1 | FFF | a | human-review.md:145 covers code-forced escalation and scripted-model routing tests; skill not loaded. Description has no "escalation rate", "review queue" or "reviewer fatigue" (only "risky actions awaiting review"), though SKILL.md:52 routes exactly this. | description: add escalation-rate / review-queue wording |
| guardrails-escalation-two-sided-calibration | A2 | FFF | a | evaluation-design.md:9 (adk-agent-evaluation) and human-review.md:145 define the missed/over-escalation pair; neither loaded. | as above |
| guardrails-escalation-two-sided-calibration | A3 | FFF | a | grep finds no guidance on keeping a production escalation-rate dashboard as a drift signal only (no "dashboard"/"drift" in adk-operational-guardrails or evaluation-design.md near escalation). | add one sentence to human-review.md |
| guardrails-unanswered-approval-and-screening-placement | A1 | FFF | c | Skill loaded (Skill tool) but no reference read; human-review.md:151-153 "Unanswered approvals and unreadable arguments" covers exactly this; SKILL.md:53 routes approval work to human-review.md. | none (optional: name "unanswered or stale approvals" in the SKILL.md:53 row) |
| guardrails-unanswered-approval-and-screening-placement | A2 | FFF | c | human-review.md:153 "fails closed on arguments it cannot read ... NaN"; not read. | as A1 |
| guardrails-unanswered-approval-and-screening-placement | A3 | FFF | a | Placement rule lives in adk-agent-security/references/agency-and-output.md:262-279 ("a check that must prevent an effect runs blocking, before the agent"); adk-operational-guardrails SKILL.md has no screen row or pointer, and adk-engineer's table assigns screen placement to protect-adk-sensitive-data, which has no such rule (grep finds none) and was not installed here. | point guardrails (and protect-adk-sensitive-data) at the placement rule, or move it to the skill the engineer table names |

## Suspected skill defects

1. **adk-operational-guardrails, description:** three of four primary runs never loaded the
   skill. The description (SKILL.md:3-11) names loops, budgets, approval and cost shutdown but
   not escalation rates/review queues or paid continuations/attempt ledgers, although the body
   routes both (SKILL.md:52, 56). Evidence: guardrails-escalation A1-A3, guardrails-continuation
   A2, A4.
2. **adk-operational-guardrails, human-review.md:** no guidance to keep a production
   escalation-rate dashboard as a drift signal rather than a target (escalation A3).
3. **Screen placement ownership (adk-operational-guardrails / protect-adk-sensitive-data /
   adk-engineer):** the only placement rule is in adk-agent-security agency-and-output.md:262-279;
   adk-engineer's routing table says protect-adk-sensitive-data owns "where a response screen
   sits relative to tool dispatch", but that skill has no such rule, and guardrails has no pointer
   (unanswered-approval A3).

Not defects but worth noting: four runs on plain prompts loaded no skill (safe-api-tool-calls,
guardrails x2) after starting with `Glob **/*`; for safe-api the description fits the prompt
well, so this is agent behaviour rather than description.

## Fixture or assertion defects

- **engineer-ticket-with-missing-companion (fixed):** G02 (verified_local) cited
  `tests/test_stream.py`, which the fixture lacked. Added
  `evals/fixtures/engineer-ticket-with-missing-companion/tests/test_stream.py` (scripted-runner
  stream tests that skip without fastapi/google-adk; composed suite: 5 tests, OK, 2 skipped).
- **engineer-resumes-from-progress-block:** the Progress block's worktree `../wt-G02` is outside
  the confined workspace, so the uncommitted A1 work is unreachable and A2/A3 cannot pass.
  Fix: ship `wt-G02/app/stream.py` and `wt-G02/tests/test_stream.py` inside the overlay, change
  the block to `worktree wt-G02` and the context to "in worktree wt-G02". A2's git status still
  needs a shell: flag it.
- **Shell-dependent assertions without an escape (flag):** missing-companion A3 (lint/theme
  checks), chosen-test-first A2 (red test), resumes A2 (git status, re-verify),
  checkpoint-after-delta A2 (Evidence cells can only change after something ran).
- **chosen-test-first-workflow A1:** depends on the `tdd` skill, which this repository does not
  ship; the run cannot represent "the installed test-first skill". Flag, or install a minimal
  stand-in test-first skill as part of the fixture.
- **engineer-ticket-with-missing-companion A4:** with nothing run, "not run" is the honest tier;
  the assertion should say so.
