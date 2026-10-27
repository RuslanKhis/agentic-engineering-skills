# Quality phases: integration and activation · 27 October 2026

Five branches from the 27 October quality plan were merged into one
integration branch, in this order: `phase-6-readme`,
`phase-5-helper-conventions`, `phase-2-boundaries`, `phase-1-evals`,
`phase-3-shared-guidance`. The README branch cut the README from 3,849 to
446 lines. It moved the per-skill detail to `docs/skills.md`, the journeys
to `docs/journeys.md` and this testing log to `docs/testing/index.md`, all
verbatim, and a link check found 0 broken links. The other branches have
their own records:
[helper conventions](helper-conventions-2026-10-27.md),
[skill boundaries](skill-boundaries-2026-10-27.md),
[eval runners](eval-runners-2026-10-27.md) and
[shared guidance and context](shared-guidance-and-context-2026-10-27.md).

## Merge

Conflicts appeared in `CONTRIBUTING.md`, `scripts/check_repo.py` and five
SKILL.md helper invocations (fastapi, frontend, guardrails, tool-auth,
deploy). Each was resolved by keeping both sides:
- phase 5's command form (`"$SKILL_DIR"`, `--project`, `--gcp-project`,
  exit 3);
- phase 3's link to `references/operating-rules.md`;
- phase 3's correction that ADK 2.12.0's user-id fix covers A2A requests
  only.

`scripts/check_repo.py` passes on the result: 26 packages, 0 errors, and
word-budget warnings for adk-engineer (2,506 words), adk-governance-pack and
adk-system-designer. Shared snippets: 7 in use, 0 drifted. Boundaries: every
exclusion is either reciprocal or allowlisted.

## Activation before and after

Method: `scripts/run_activation.py` with the `claude-cli` backend. The
selector sees only the name and description catalogue and neutral prompt
labels.
- Baseline: 114 cases on main at 16ea7fa, from the phase 1 branch.
- After: 154 cases on the integration branch, including 40 boundary cases
  from phase 2.

| Run | Cases × repeats | PASS | PARTIAL | FAIL |
| --- | --- | --- | --- | --- |
| Before, Sonnet 5.5 | 114 × 2 | 222 | 4 | 2 |
| After, Sonnet 5.5 | 154 × 2 | 298 | 9 | 1 |
| Before, Haiku 5.5 | 114 × 1 | 111 | 1 | 2 |
| After, Haiku 5.5 | 154 × 1 | 145 | 7 | 2 |

### Sonnet: the 114 original cases

`--compare` found 0 new FAIL.
- Now pass in both repeats:
  - `designer-checkpoint-positive` (was PASS/PARTIAL)
  - `portability-migration-build-near-miss` (was FAIL/PASS)
  - `presenter-rollout-ui-near-miss` (was PARTIAL/PASS)
- `observability-eval-handoff-positive` moved from PARTIAL/PARTIAL to
  PASS/PARTIAL; its label is still in question (phase 1 record).
- `tool-interface-toolset-positive` moved from PASS/PASS to PASS/PARTIAL.

### Haiku: the 114 original cases

- Now pass: `engineer-positive`, `practice-profile-host-memory-near-miss`
  and `tool-interface-toolset-positive`.
- Two new FAILs:
  - `memory-ingestion-positive` was already unstable on Sonnet before the
    change. No description mentioned document ingestion, although
    adk-memory-architecture ships `references/document-ingestion.md` and
    `qualify_ingestion.py`. The description now names per-page ingestion
    triage, OCR or vision routing and coverage checks.
  - `fastapi-backend-plain-crud-near-miss`.

A targeted re-run over memory's and fastapi's cases after the description
change (`*-memory-fastapi-recheck.json`):
- Sonnet ×2: 30 PASS, 2 PARTIAL, 0 FAIL.
- Haiku ×3: 42 PASS, 6 PARTIAL, 0 FAIL.
- `memory-ingestion-positive` passed in all five runs.
- `fastapi-backend-plain-crud-near-miss` passed in all three Haiku runs, so
  the earlier failure was a single unstable answer.

### PARTIAL results that remain

Every remaining PARTIAL is a near-miss. In each, the owner named in
`skills/adk-engineer/references/ownership.md` was chosen as primary, and the
neighbour was loaded only as supporting:
- approval vs the write side of confirmation
- CI gate vs writing eval cases
- session endpoints vs domain routes
- confirmation tiering vs approval mechanics
- cross-user access through a tool

The 8 October grading counts that as PARTIAL, not FAIL.

## What this does not establish

These runs measure selection from descriptions only. They do not measure
how well a skill does the task once it is chosen.

The 40 phase 2 cases were written together with the ownership map, so they
are not a held-out test.

Scenario execution still needs fixtures: 126 of 152 scenarios have none.
Two skills ship grader-side files that an agent read during the phase 1
smoke run: memory's `inventory.json` and evaluation's expectations file.
Both are follow-up work.

Artifacts: [before](artifacts/activation-2026-10-27/),
[after](artifacts/activation-2026-10-27-after/).
