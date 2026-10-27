# Evaluation runners and a baseline · 27 October 2026

Until today the 114 activation cases and 152 scenarios (671 assertions) were
only structure-checked, and the one measured activation run was the hand-run
[8 October trial](activation-trial-2026-10-08.md) over 20 skills and 56 cases.
This records two runners that make those measurements repeatable, the first
baseline over the whole activation corpus, a five-scenario smoke run, and a
rewrite of 51 scenario prompts into the words a user would use.

## What was built

- [`scripts/run_activation.py`](../../scripts/run_activation.py) builds the
  catalogue from every `skills/*/SKILL.md` frontmatter (name and description,
  stdlib parser checked against PyYAML for all 26 packages), shuffles the cases
  with a seed into near-equal batches of at most 14, and asks a selector for a
  primary skill or `none`, up to two supporting skills and a one-sentence
  reason per prompt. Prompts carry neutral labels (`R01`...); the selector
  never sees case ids, labels or rationales. Grading follows the 8 October
  rules, plus ERROR for a batch whose reply cannot be read (one retry first).
  Backends: `claude-cli`, `anthropic` (urllib, no SDK) and `files`
  (export/import). `--repeat`, `--model`, `--only`, `--compare`.
- [`scripts/run_scenarios.py`](../../scripts/run_scenarios.py) with
  subcommands `list`, `prepare`, `agent`, `judge` and `run`; see
  [checking skill quality](skill-quality.md#run-the-scenario-runner).
- [`scripts/model_backends.py`](../../scripts/model_backends.py), the shared
  model calls.
- [`evals/scenario-fixtures.json`](../../evals/scenario-fixtures.json), which
  scenarios can run as they stand.
- 31 offline tests in `tests/test_run_activation.py` and
  `tests/test_run_scenarios.py`, picked up by `check_repo.py`'s existing
  discovery of `tests/` (no wiring change). They cover grading, batching
  determinism, catalogue extraction, the results and compare formats, the
  files round trips for both runners, fixture classification and the
  workspace layout, with fake subprocess and HTTP openers.
- [`.github/workflows/activation.yml`](../../.github/workflows/activation.yml),
  on request only (a weekly schedule is written but commented out), running
  the anthropic backend with the `ANTHROPIC_API_KEY` secret and uploading the
  results. `validate.yml` is unchanged and stays offline.

## Activation baseline

**Method.** `claude-cli` backend: Claude Code 2.1.306, `claude -p` run in an
empty temporary directory with `--system-prompt` (the selector instructions in
`run_activation.py`), `--tools ""`, `--safe-mode`, `--disable-slash-commands`,
`--setting-sources ""` and `--strict-mcp-config`. A probe before the run asked
the same configuration to list its skills, tools and project instructions; it
reported none, with a 583-token context. Default effort. Seed `20261027`;
each repeat reshuffles (`20261027:1`, `20261027:2`). Commit `16ea7fa`,
catalogue SHA-256 `0d93b63db2ea4b1a` (26 skills,
[catalogue.json](artifacts/activation-2026-10-27/catalogue.json)), corpus
SHA-256 `f51ed02934672ec3` (114 cases, none marked with a split).

| Run | Cases | PASS | PARTIAL | FAIL | ERROR | Cost |
| --- | --- | --- | --- | --- | --- | --- |
| claude-sonnet-5-5, repeat 1 | 114 | 111 | 2 | 1 | 0 | |
| claude-sonnet-5-5, repeat 2 | 114 | 111 | 2 | 1 | 0 | |
| claude-sonnet-5-5, both | 228 | 222 | 4 | 2 | 0 | $0.78 |
| claude-haiku-5-5 | 114 | 111 | 1 | 2 | 0 | $0.03 |

One Sonnet batch returned unparsable text on its first attempt and parsed on
the retry. The two Sonnet repeats chose the same primary for 111 of 114 cases;
all three runs agreed on 106. Results with every case's grade and reason:
[sonnet-5-5.json](artifacts/activation-2026-10-27/sonnet-5-5.json),
[haiku-5-5.json](artifacts/activation-2026-10-27/haiku-5-5.json), and the
printed summaries beside them.

### Cases that did not pass

| Case | Target, kind | Grades | What the selector did |
| --- | --- | --- | --- |
| `memory-ingestion-positive` | adk-memory-architecture, positive | Sonnet PASS, FAIL; Haiku PASS | Repeat 2 chose `none`: page classification and OCR routing read as document ingestion that no description covers. The memory description does not mention ingestion. |
| `portability-migration-build-near-miss` | adk-portability-planning, near-miss | Sonnet FAIL, PASS; Haiku PASS | Repeat 1 chose portability planning for "rewrite in LangGraph and deploy on AWS", while noting that the skill only plans. |
| `observability-eval-handoff-positive` | adk-agent-observability, positive | Sonnet PARTIAL, PARTIAL; Haiku PASS | Evaluation primary, observability and sensitive-data supporting: building the eval set read as the main job. |
| `designer-checkpoint-positive` | adk-system-designer, positive | Sonnet PASS, PARTIAL; Haiku PASS | Repeat 2 chose adk-engineer primary with the designer supporting. "Checkpoint" is not in the designer's description. |
| `presenter-rollout-ui-near-miss` | adk-presenter, near-miss | Sonnet PARTIAL, PASS; Haiku PASS | Frontend primary, presenter supporting for the disclosure wording. |
| `engineer-positive` | adk-engineer, positive | Sonnet PASS, PASS; Haiku FAIL | Haiku chose memory primary with frontend and instructions supporting. |
| `practice-profile-host-memory-near-miss` | practice-profile, near-miss | Sonnet PASS, PASS; Haiku FAIL | Haiku chose practice-profile for a `~/.claude/CLAUDE.md` edit while saying the description excludes it. |
| `tool-interface-toolset-positive` | adk-tool-interface-design, positive | Sonnet PASS, PASS; Haiku PARTIAL | Haiku chose interoperability primary for a 40-tool MCP server, tool interface supporting. |

The three Sonnet cases that flip between repeats (`memory-ingestion-positive`,
`portability-migration-build-near-miss`, `designer-checkpoint-positive`) are
the boundary cases to work on first; with two repeats they sit at a 0.5 rate.

### Labels worth reviewing

No label was changed (`evals/activation.json` belongs to another branch).
`observability-eval-handoff-positive` is the only label the selectors
consistently disagree with: both Sonnet repeats put adk-agent-evaluation
primary, and the evaluation skill's description owns building eval sets from
labelled cases. The case is a hand-off between two skills, so either accepting
evaluation as primary (observability supporting) or rewording the prompt
towards the trace-sampling side would make it a fairer test. The other
non-passing cases look correctly labelled; their misses point at descriptions
(ingestion and checkpoint wording) or at model strength (Haiku), not labels.

### Limits

Selection from descriptions only, as on 8 October: no host loader, no project
context, no execution. Two Sonnet repeats and one Haiku run are small; the
protocol asks for three fresh runs per case and a train/held-out split, and
the corpus has no split yet. The prompts are the corpus's own wording.

## Scenario smoke run

**Runnable set.** `run_scenarios.py list`
([runnable-list.md](artifacts/scenarios-2026-10-27/runnable-list.md)): 21
scenarios run in an empty workspace (most are design conversations), 5 need a
fixture copied from this repository (`evaluation-review-contract-solvability`,
`evaluation-selected-source-support`, `memory-local-document-completeness`,
`memory-ingestion-scan-detection`, `memory-retrieval-second-round`), and 126
are `fixture-missing`: their context describes a project, ticket, plan or data
that no fixture supplies. Eight of those have a nearby fixture that lacks what
the context needs (named under `partial` in the fixture file); for example the
journeys fixture has tickets T-101 to T-105 but not T-201 or T-202. No
scenario with `expected_primary` adk-engineer or safe-api-tool-calls is
runnable today.

**Method.** Agent `claude-sonnet-5-5` through `claude -p` in each workspace
with `--setting-sources project`, tools `Read,Write,Edit,Glob,Grep,Skill` (no
shell), `--max-turns 30`, a 900-second timeout and `--max-budget-usd 3`.
Each workspace held the scenario's installed `available_skills` only; the
session's catalogue also listed Claude Code's built-in skills (recorded in each
`agent.json`). Judge `claude-sonnet-5-5` through the isolated `claude -p`
call. The five prompts were left unrewritten so that this run used the
authored wording. Agent cost $1.21 in total; runs took 51 to 262 seconds; none
timed out.

| Scenario | Assertions (judge pass 1) | Judge pass 2 | Primary SKILL.md loaded | Primary's files read |
| --- | --- | --- | --- | --- |
| system-design-contracts-stay-small-when-read-only | 3/4 | 3/4 | yes | yes |
| estimate-poc-tickets | 3/4 | 4/4 | yes | yes |
| evaluation-selected-source-support | 4/5 | 4/5 | no | yes |
| memory-ingestion-scan-detection | 3/5 | 3/5 | no | yes |
| memory-local-document-completeness | 3/4 | 4/4 | no | yes |

Judge pass 2 re-graded the same evidence after the runner learned to record
skill files read; two of 22 verdicts flipped (calendar waits in
`estimate-poc-tickets`, the governed review path in
`memory-local-document-completeness`), so single judge verdicts on borderline
assertions are not stable. Two pass-1 quotes in the ingestion case were not
found verbatim in the evidence; the runner flags these as `quote_found:
false`. Results, final answers, judge replies and the files each agent wrote
are under [artifacts/scenarios-2026-10-27](artifacts/scenarios-2026-10-27/);
transcripts and the copied skills were left out of the repository.

**Observations.**

- In three of five runs the agent never loaded its primary skill's `SKILL.md`:
  it globbed the workspace, saw `.claude/skills/...`, and read references and
  scripts directly. The runner now records `skill_files_read` beside
  `skills_loaded`, because a host loading the skill and an agent reading its
  files are different events.
- The memory ingestion agent read the installed skill's
  `assets/ingestion-fixture/inventory.json`, which is the generator's own
  knowledge that the scenario keeps with the grader. The evaluation skill
  likewise ships `source-support-expectations.json`. Results for scenarios
  whose fixture lives inside an installed skill are contaminated until those
  assets are separated or the expectations moved out of the package.
- Tool restrictions held: a `Bash` call was refused, and a search under the
  user's home `.claude` directory was refused because nobody grants
  permissions in a headless run. A glob of the session's own (empty)
  auto-memory directory was allowed. The file tools are therefore not
  confined to the workspace by the runner itself; a stricter run would add
  Claude Code's `--restricted` mode once its effect on project skills is
  checked.

## Prompt rewrites

51 scenario prompts were rewritten in plain words, keeping each case's id,
context, assertions, available skills and expected primary unchanged (checked
by script). Some now leave details vague, as users do. Before and after text
is in [prompt-rewrites.json](artifacts/scenarios-2026-10-27/prompt-rewrites.json).
Changed ids:

evaluation-preinference-contract-qualification,
memory-document-shape-and-source-coordinates,
evaluation-bound-spans-versus-model-paraphrase,
evaluation-progressive-downstream-repair,
workflow-checkpoint-dependency-invalidation,
guardrails-continuation-accounting-and-duplicates,
workflow-realistic-checkpoint-storage-preflight,
workflow-warning-only-correction-preservation,
evaluation-recovery-is-not-full-route-acceptance,
evaluation-reviewer-coverage-versus-uncertainty,
evaluation-review-contract-solvability, evaluation-recurring-failures-reentry,
router-resumes-accepted-goal, router-missing-specialist,
existing-agents-cli-focused-memory, plain-adk-no-scaffold,
chosen-test-first-workflow, privacy-with-observability,
system-design-review-existing-proposal,
system-design-runtime-and-release-review, system-design-practical-handoff,
evaluation-generalization-and-deliverable-budget,
evaluation-improve-decisions-error-analysis,
sql-toolbox-read-only-and-secure-tenant,
release-post-launch-quality-loop-aqua, memory-write-back-loop-from-horizon,
sql-acceptance-metric-names-and-spider2-bigquery-probe,
release-bigquery-analytics-score-gate-and-drift,
security-code-execution-environment-selection,
optimise-compaction-atomic-groups-three-points, designer-handed-over-web-poc,
presenter-monthly-value-report, presenter-rollout-pack-go-live,
observability-handover-and-postmortem, presenter-poc-review-evidence-only,
memory-retrieval-second-round, engineer-google-skills-supporting-missing,
engineer-ticket-creates-cloud-sql, engineer-agents-cli-deploy-ticket,
designer-poc-teardown-goal, designer-names-google-product-skills,
engineer-gcp-goal-unaffected-by-portability, portability-ticket-carried-out,
estimate-experienced-team, estimate-new-team, estimate-mvp-three-people,
estimate-production-waits, workflow-content-safeguards-in-code,
mcp-rug-pull-runtime-pin-and-mcp-ids,
observability-semconv-drift-and-evaluation-events,
frontend-agui-approval-contract-declared.

## Checks

`.venv/bin/python scripts/check_repo.py` passed on Python 3.12.9 (109
repository tests, including the 31 new ones). The 31 new tests also passed on
Python 3.11.4 without PyYAML installed (the YAML comparison skips).
