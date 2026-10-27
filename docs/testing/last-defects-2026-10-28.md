# The last defects from the Phase 10 triage · 28 October 2026

The [skill defect fixes record](skill-defect-fixes-2026-10-27.md) left three
suspected skill defects, four fixture or assertion defects, and nine
scenarios unrun. This records the fixes, activation on both splits, and the
scenario runs that measure them. Branch `phase-11-last-defects`, from `main`
at `827ceeb`.

## Skill defects

Each was checked against the skill text on `main` before it was changed.

| # | Defect | Verdict | Fix | Where |
| --- | --- | --- | --- | --- |
| 1 | The adk-workflow-design description names none of saved-stage reuse, resume versus a durable engine, multi-day approval waits, checkpoint storage limits, draft consistency checks or warning-only correction, though the body routes all six (SKILL.md mode table; "Validate and finish") | Confirmed | The description adds "checkpoints" to its scope and names "reusing saved stages after an input changed, a checkpoint too large for its store, a run waiting days for approval across restarts (ADK resume or a durable engine), draft consistency checks in code and warning-only corrections". Its exclusions are unchanged, so no reciprocal clause changed. Two rows in `ownership.md` record the split the bodies already draw: workflow owns the checkpoint contract and evaluation the validation plan around a failed stage; workflow owns resume versus a durable engine, guardrails which actions wait and the review record, safe-api the idempotency key. `docs/skills.md` matches | `skills/adk-workflow-design/SKILL.md:3-17` (description); `skills/adk-engineer/references/ownership.md:44-45`; `docs/skills.md:484-495` |
| 2 | Deploy's Agent Identity notes (`agent-runtime.md:37-44`) give no hand-off to adk-tool-auth-and-secrets | Confirmed | A paragraph after the Agent Identity bullets: which identity the agent runs as and the roles its tools need are tool-auth's decision; deploy applies `identity_type` or `--agent-identity`, grants the agreed roles, journals the IAM edit and verifies `spec.effectiveIdentity`; without tool-auth installed the decision is recorded as owed, and a manifest default is the current setting, not the decision | `skills/deploy-adk-on-google-cloud/references/agent-runtime.md:45` |
| 3 | Deploy SKILL.md:48 tells a ticket loaded straight into deploy only that "adk-engineer explains how to get" a missing google/skills product skill | Confirmed | SKILL.md:48 now states the rule and the step: a `google/skills:<name>` operates the product while deploy decides; if missing, give `npx skills@latest add google/skills --skill <name>` (a restart loads it), invent none of its instructions, finish the local work and record the product step in Evidence as an execution-scope prerequisite. The five other "adk-engineer explains" pointers in deploy (SKILL.md:30, `agent-runtime.md:49`, `cloud-run.md:96`, `:98`, `:133`, `production.md:99`) now give the install step too (`uvx google-agents-cli setup` for the Agents CLI skills) | `skills/deploy-adk-on-google-cloud/SKILL.md:30`, `:48`; references above |

### Description lengths

| Skill | Before | After |
| --- | --- | --- |
| adk-workflow-design | 763 | 944 |

No other description changed. `scripts/check_boundaries.py` passes.

## Fixtures and assertions

| Change | Where |
| --- | --- |
| Ten shell-dependent assertions carry a "reported as not run" escape in the assertion text: interop conformance A1, signed card A3, resumes A2, missing companion A3 and A4, google-skills A3, checkpoint dependency A5, portability A2 and A7, presenter value report A3. Four of them already had the escape in their grader `situation.md`, and the Phase 10 judges still failed them on the assertion's literal "Runs ...", so the wording belongs in the assertion; each `situation.md` gains a dated note on what the escape credits | `evals/scenarios.json`; `evals/graders/<id>/situation.md` |
| `engineer-agents-cli-deploy-ticket` A5 said Agent Runtime has no revision rollback, which contradicts adk-release-engineering `staged-rollout.md` ("Agent Runtime: revisions and manual traffic split (Pre-GA)"). It now asks for a rollback that does not depend on Agents CLI (redeploy the previous known-good source, since Agents CLI 1.11.0 has no revision or traffic flags and the platform's revisions are Pre-GA) | `evals/scenarios.json`; its `situation.md` |
| `guardrails-unanswered-approval-and-screening-placement` installs protect-adk-sensitive-data, which owns screen placement | `evals/scenarios.json` |
| `sensitive-data-local-tool-result-screen-llamafirewall`'s `expected_primary` is protect-adk-sensitive-data | `evals/scenarios.json` |

## Activation

`scripts/run_activation.py --backend claude-cli --model claude-sonnet-5-5
--repeat 2`, each split separately, compared with Phase 10's runs
(`--compare`). Six dev cases were added, written without reading any
held-out case: positives for checkpoint invalidation, checkpoint storage, a
durable wait and a warning-only correction; near-misses for approval tiering
(guardrails) and a staged repair plan (evaluation). The held-out split was
run once, after the edits.

| Split | Cases × repeats | PASS | PARTIAL | FAIL | Phase 10 |
| --- | --- | --- | --- | --- | --- |
| dev | 178 × 2 | 344 | 10 | 2 | 172 × 2: 331 / 12 / 1 |
| dev, the 172 cases Phase 10 ran | 172 × 2 | 332 | 10 | 2 | 331 / 12 / 1 |
| held-out | 78 × 2 | 155 | 1 | 0 | 156 / 0 / 0 |

- The six new dev cases passed in both repeats.
- **designer-checkpoint-positive**: PARTIAL, FAIL before; FAIL, PASS now.
  Three more repeats of the designer cases alone gave FAIL, FAIL, PASS, the
  same as Phase 10's run on `main`. Every FAIL chose adk-engineer as primary;
  adk-workflow-design was never primary or supporting in the five answers, so
  "checkpoints" in its description did not draw this request. It remains the
  designer-versus-engineer instability Phase 10 recorded.
- **observability-eval-handoff-positive**: PARTIAL, PASS to PARTIAL, FAIL,
  adk-agent-evaluation primary both times. Its label is parked by the owner
  (routing-gaps record); no description it involves changed.
- Other dev changes were between PASS and PARTIAL in both directions.
- **Held-out**: `model-output-heldout-4` (a near-miss) went from PASS, PASS
  to PARTIAL, PASS. adk-workflow-design was primary in all four answers,
  before and after; the PARTIAL comes from model-output being named as
  supporting once.

Artifacts: [activation/](artifacts/last-defects-2026-10-28/activation/)
(`dev-designer-only.json` is the three-repeat designer run).

## Scenario runs

Settings as Phases 9 and 10: `run_scenarios.py run`, agent and judge
`claude-sonnet-5-5` through `claude-cli` (Claude Code 2.1.306), three judge
repeats with majority verdicts, `--max-turns 30`, 900 s, `--max-budget-usd 3`,
default confinement (no shell), project skill install, skills at `19e51e3`.
The cap for this phase was $12, spent in the order asked: the seven workflow
scenarios, the guardrails placement scenario, then the governance packs and
the rollout pack. The governance agents cost $0.80-1.57 each, so the
governance batch was stopped after its fourth agent, the four finished runs
were judged on their unchanged evidence (`judge --run-dir`, manifest cut to
those four), and the rollout pack ran on its own. Evidence per scenario
and each batch's manifest and results are under
[last-defects-2026-10-28/](artifacts/last-defects-2026-10-28/);
[summary.md](artifacts/last-defects-2026-10-28/summary.md) has every vote.

### Workflow scenarios before and after the description change

Before: Phase 10's run (skills at `c297ef1`).

| Scenario | Before | After | Primary loaded before → after |
| --- | --- | --- | --- |
| workflow-checkpoint-dependency-invalidation | 1/5 (A1-A2 FFF, A3 FFP, A4 PPP, A5 FFF) | 1/5 (A1-A3 FFF, A4 FPP, A5 PFF) | no → yes |
| workflow-engine-restate-or-dapr-keeps-adk-contract | 0/5 | 0/5 (A4 FPF) | yes → yes |
| workflow-realistic-checkpoint-storage-preflight | 0/5 | 1/5 (A5 PFP) | no → yes |
| workflow-warning-only-correction-preservation | 1/4 | 1/4 | no → yes |
| plain-adk-no-scaffold | 3/5 | 5/5 | yes → yes |
| workflow-content-safeguards-in-code | 3/5 | 3/5 | no → yes |
| workflow-durable-refund-resume-or-engine | 0/4 | 1/4 (A2 now PPP) | no → yes |
| **All** | 8/33, 4 split | 12/33, 5 split | 2/7 → 7/7 |

The description fix did what it was for: the skill now loads in every
workflow run, and in five of seven the agent opened the reference that holds
the failed rule (checkpoint-reuse, runtime twice, review-contracts,
content-safeguards). Assertions moved less than loading did: most remaining
failures are answers that read the rule and left it out. The storage
scenario is the exception: the skill loaded, but its mode table does not
route a checkpoint over its store's size limit to `checkpoint-reuse.md`, so
no reference was read (new suspected defect 1 below). The checkpoint
dependency scenario's A5 escape worked as intended: one judge credited the
tests reported as not run, and the two FAILs are on coverage, not on running.

### Other scenarios

| Scenario | Result | Notes |
| --- | --- | --- |
| guardrails-unanswered-approval-and-screening-placement (re-run with protect installed) | 1/4, as in Phase 10 | protect-adk-sensitive-data loaded and `boundaries.md` read; A3 still fails: the screen stayed in a non-blocking callback. A1 and A2 fail for the third run in a row because `human-review.md` is not opened |
| governance-pack-annex-iii-pilot | 4/6 | A6 needs a shell; A2 split |
| governance-pack-au-hr-internal | 5/6 | A6 needs a shell |
| governance-pack-uk-bank-chatbot | 3/5 | A5's checker half needs a shell; A3 missed SCHUFA; A4 split pass |
| governance-pack-us-hiring-screener | 5/6 | A6 needs a shell |
| presenter-rollout-pack-go-live | 2/4 | A2 uncited statements, A3 no Article 50 date; A4 split pass |

First runs: 19 of 27 assertions; the governance skill loaded in all four and
the agents read the jurisdiction references and templates. Two governance
content rows failed (annex A2 on a split vote, uk-bank A3); the four checker
rows are the same shell defect as the ten fixed above (the grader notes
already credit naming the command, and the judges still failed them).

Not run: four governance packs (`nsw-agency-chatbot`,
`commonwealth-dta-assessment`, `auckland-singapore-retailer`,
`quebec-ontario-hr-assistant`) and the scenarios whose assertions changed in
this phase (step iv), for the cost cap.

### Triage

36 failed or split rows over 12 scenarios
([triage.md](artifacts/last-defects-2026-10-28/triage.md)):

| Class | Rows |
| --- | --- |
| (a) skill defect | 4 (all in the storage scenario) |
| (b) fixture or assertion defect | 4 (the governance checker rows) |
| (c) run variance | 28 |

The lead agent classified the rows from the judges' reasons, the agents'
`skill_files_read` and the skill text, and spot-checked the classifications
that decide a fix (the storage routing gap, the guardrails reference, the
SCHUFA citation, the runtime facts).

New suspected defects, not fixed here:

1. **adk-workflow-design, SKILL.md mode table**: the checkpoint row routes
   "saved-stage continuation or changed dependencies during recovery" to
   `checkpoint-reuse.md`, but a checkpoint that fails its store's size limit
   is not named, though `checkpoint-reuse.md:85-96, :110` covers it and the
   description now draws the request.
2. **adk-operational-guardrails, SKILL.md human-review row** (minor): three
   runs of the placement scenario loaded the skill and never opened
   `human-review.md`, whose "Unanswered approvals and unreadable arguments"
   (:151-153) holds A1 and A2. Naming unanswered approvals and unreadable
   arguments in that row is the Phase 9 triage's optional suggestion.

Fixture and assertion defects found: the governance checker assertions
(annex A6, au-hr A6, us-hiring A6, uk-bank A5 and the same A5/A6 in the four
unrun packs) need the same "reported as not run" escape in their text;
`workflow-engine-restate-or-dapr-keeps-adk-contract` A4 could also accept a
rejection of Dapr on its licence (Phase 10's note).

## Follow-up fixes (not measured)

Made after this record on branch `phase-12-small-fixes`, with no new model runs:

- adk-workflow-design SKILL.md mode table: the checkpoint row now also covers a
  checkpoint or saved artifact too large for its store, and sends it to
  `checkpoint-reuse.md` for the storage-limit check (the four skill-defect rows).
- adk-operational-guardrails SKILL.md: the human-review row now names
  unanswered approvals and unreadable arguments and points to that section of
  `human-review.md`.
- The `check_governance.py` assertion in all eight governance packs now carries
  the "reported as not run" escape in its text, with a dated note in each
  grader `situation.md`.

Not changed: engine-restate A4 (accepting a Dapr licence rejection) and the
designer-versus-engineer activation instability.

## Cost

Recorded: agent $8.77, judge $2.94, **$11.70** for 13 graded scenarios. Not
recorded: the fifth governance agent (`nsw-agency-chatbot`), stopped seconds
after it started, which wrote no result. Activation runs go through the same
CLI and are not part of the scenario cap.

## Left

- Four governance packs and every scenario whose assertions changed here:
  the ten with the new escape, `engineer-agents-cli-deploy-ticket` and
  `sensitive-data-local-tool-result-screen-llamafirewall` (at this run's
  $0.90 per scenario, about $14; the governance packs alone about $6).
- The two new suspected skill defects and the governance checker escapes
  above.
- The designer-versus-engineer activation instability on
  `designer-checkpoint-positive`, for the designer's owner.
- `observability-eval-handoff-positive`, whose label is parked.

## Limits

One run per scenario, so a changed verdict says what happened in this run,
not how often; 9 of 64 assertions had split votes. The agent had no shell.
The workflow before-and-after compares single runs a day apart; the only
skill changes between them are this phase's (the workflow description, the
ownership rows and the deploy hand-offs). Loading went from 2 of 7 to 7 of 7,
which is unlikely to be chance; the assertion change (8 to 12 of 33) is
within what one re-run can move. The
triage was done by the agent that made the fixes.

## Checks

`.venv/bin/python scripts/check_repo.py` passed on Python 3.12.9, including
`check_boundaries.py` and `sync_shared.py --check`.
