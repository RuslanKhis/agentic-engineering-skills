# Scenario runner fixes and grader material · 27 October 2026

The [phase 1 smoke run](eval-runners-2026-10-27.md#scenario-smoke-run) left
four problems: two skills shipped grader-side answers that an agent read,
three of five agents never loaded their primary `SKILL.md`, reads outside the
workspace were refused only because nobody answered a prompt, and re-judging
the same evidence flipped 2 of 22 verdicts. This records the fixes, the
removal of the API-key backend and a re-run of the same five scenarios.

## Grader material moved out of skill packages

Every file under `skills/*/` was checked for expected answers, labels, gold
outputs or assertions belonging to a scenario in `evals/scenarios.json` or to
a trial, as opposed to assets a helper needs at run time or a helper's own
unit-test data.

| Moved from | To | Why |
| --- | --- | --- |
| `skills/adk-memory-architecture/assets/ingestion-fixture/inventory.json` | `evals/graders/memory-ingestion-scan-detection/inventory.json` | Generator knowledge, the answer key for the ingestion scenario; an agent read it on 27 October |
| `skills/adk-agent-evaluation/assets/source-support-expectations.json` | `evals/graders/evaluation-selected-source-support/source-support-expectations.json` | The labels the source-support scenario's agent is asked to produce |
| `skills/safe-api-tool-calls/tests/acceptance/` | `evals/trials/safe-api-tool-calls/acceptance/` | The trial's independent oracle ("give the candidate only its request and fixture inputs") |
| `skills/safe-api-tool-calls/tests/forward-cases.md`, `tests/fixtures/` | `evals/trials/safe-api-tool-calls/` | Trial protocol and grading rubric (it says to withhold itself) and the trial's inputs |
| `skills/adk-operational-guardrails/tests/forward-cases.md` | `evals/trials/adk-operational-guardrails/forward-cases.md` | Trial cases with what the evaluator observes |
| `skills/safe-api-tool-calls/tests/forward-evaluation.md`, `depth-recheck.md` | `docs/skill-evidence/safe-api-tool-calls/` | Trial results |
| `skills/deploy-adk-on-google-cloud/tests/forward-results.json`, `recheck-results.json` | `docs/skill-evidence/deploy-adk-on-google-cloud/` | Trial results describing what a passing agent did |

Follow-on changes: `check_source_support.py` now needs `--expectations PATH`
(the skill has no labels of its own) and its tests read the labels from
`evals/graders/` (skipped where they are absent); `make_ingestion_fixture.py`
needs `--output` and its tests regenerate the inventory in a temporary
directory; the ingestion reference no longer prints the expected route per
page; references that linked the moved files now name their repository
paths in plain text. Two scenario contexts say the labels or inventory are
held back for grading.

Checked and left in place: `document-coverage.json` (its `required_sections`
are the golden queries the coverage scenario asks the agent to build checks
around; the context keeps them from the retriever, not from the agent),
`retrieval-gold.json` (the user asks for recall on "our gold set"),
`contract-qualification.json` (its `fixture_meanings` serve the skill's own
unit test, but they double as answers for the fixture-missing
`evaluation-preinference-contract-qualification`, so that scenario needs its
own pack), `adversarial-cases.json` (a seed suite users adopt; no scenario
uses it), `evaluation-expectations.json` (an eval-config example),
`semconv-expected-violations.adk-2.11.0.json` (a helper's runtime baseline),
the deploy and optimise `forward-cases.json` and `recheck-cases.json` (inputs
only) and the unit-test fixtures under `tests/fixtures/` of the designer and
portability skills (no answers in them).

**Runner and check.** `scenario-fixtures.json` lists grader files under a
`grader` key; `run_scenarios.py` refuses any outside `evals/graders/`,
copies them to `<case>/grader/` beside the workspace and puts them in the
judge's prompt only. [`tests/test_grader_material.py`](../../tests/test_grader_material.py)
fails when a listed grader file is missing, a grader file is listed for no
scenario, a fixture copies from `evals/graders` or `evals/trials`, a file
anywhere under `skills/` has the name of a grader file or the content of any
grader or trial file, or the committed inventory drifts from its generator.

## Skill installation and confinement

Phase 1 already copied the skills into `<workspace>/.claude/skills/` and ran
with `--setting-sources project`, and its sessions' catalogues listed them,
so the skills were real project skills. The transcripts show why `SKILL.md`
was skipped: the agent's first call was `Glob **/*` over the workspace, which
lists every skill file, and it opened the reference it needed directly.

Probes (Claude Code 2.1.306, Sonnet 5.5, `claude --help` checked for every
flag):

| Configuration | Skill catalogue | Reads outside the workspace |
| --- | --- | --- |
| `--setting-sources project` | installed skill plus Claude Code's built-ins; nothing from `~/.claude/skills` (which links to this repository) | refused as "not granted yet" |
| `--restricted` | the project skill is gone ("Unknown skill") | refused as outside the working directory |
| project settings file with allow rules + `dontAsk` | installed skill | rules ignored: "this workspace has not been trusted" |
| `dontAsk` + `--allowedTools` with a bare `Glob` | installed skill | `Glob ~/.claude/skills` **allowed** (447 files) |
| `dontAsk` + `--permission-prompts none` + `Read(./**),Edit(./**),Write(./**),Skill` | installed skill | all refused by the mode; workspace reads, writes and skill references work |

The runner now uses the last row: `claude -p --setting-sources project,local
--strict-mcp-config --no-session-persistence --tools Read,Write,Edit,Glob,Grep,Skill
--permission-mode dontAsk --permission-prompts none --allowedTools
Read(./**),Write(./**),Edit(./**),Skill`, with
`CLAUDE_CODE_DISABLE_AUTO_MEMORY=1` (run A below showed an agent globbing its
own auto-memory directory under `~/.claude/projects/`, which dontAsk allows;
a probe confirmed the variable removes it from the session). Skills are copied
with symlinks resolved and `tests/` left out; the run directory may not sit
inside the repository. Adding Bash would be recorded as unconfined.

A probe through the runner's own command in a prepared
`memory-ingestion-scan-detection` workspace
([probe-project.json](artifacts/scenarios-2026-10-27-runner-fix/probe-project.json)):
catalogue = `adk-agent-evaluation`, `adk-memory-architecture` and the
built-ins, no repository skill leaked; the Skill tool loaded
`adk-memory-architecture`; refused were the repository README, `Glob
~/.claude/skills`, `~/.claude/CLAUDE.md`, `Glob ~/.claude/projects`, the
case's `grader/inventory.json` and a write beside the workspace; the workspace
write succeeded; no `CLAUDE.md` content was in context.
[probe-add-dir.json](artifacts/scenarios-2026-10-27-runner-fix/probe-add-dir.json)
shows the same for `--skill-install add-dir`, where a workspace glob lists
only `pack/`.

Each `agent.json` now records the command, the confinement, the catalogue
and `catalogue_check` (installed skills missing, repository skills leaked),
`skill_md_loaded` per installed skill (Skill tool or a `SKILL.md` read, and
how many other files of the skill were read) and every refused call.
Built-in skills (for example `run`, `code-review`, `dataviz`) stay in the
catalogue; only `--disable-slash-commands` removes them, and it removes the
project skills too. One agent invoked the built-in `run`.

## Judge repeats

`--judge-repeats N` (default 3) runs the model judge N times in parallel on
identical prompts. Each assertion is PASS only on a strict majority (UNGRADED
likewise), otherwise FAIL; the results keep every vote, the agreement (share
of votes for the final verdict) and an `unstable` list, also shown in the
summary table. A reply that cannot be parsed is asked for once more: the
first re-judging below lost one repeat to malformed JSON.

## No API keys

`.github/workflows/activation.yml` and the `anthropic` backend (Messages API
with `ANTHROPIC_API_KEY`) are removed from `model_backends.py`,
`run_activation.py` and `run_scenarios.py` with their tests; a test fails if
either runner offers it again. `claude-cli` and `files` remain.
`CONTRIBUTING.md` and [skill-quality.md](skill-quality.md) were updated and
the [eval-runners record](eval-runners-2026-10-27.md) carries a dated note.

## Smoke re-run

The five phase 1 scenarios, agent and judge `claude-sonnet-5-5` through
`claude-cli`, `--max-turns 30`, 900-second timeout, `--max-budget-usd 3`,
`--judge-repeats 3`, tools without a shell. Three runs: **run A** (the new
runner before auto-memory was switched off and before the judge retry),
**add-dir** (same code as A, `--skill-install add-dir`) and **final** (the
committed runner, project install). The phase 1 evidence was also re-judged
three times with the new judge. Agent cost: run A $1.11, add-dir $1.17,
final $1.15; runs took 35 to 172 seconds; none timed out or hit a cap.

**Primary SKILL.md loaded natively**

| Scenario | Phase 1 | Run A | Add-dir | Final |
| --- | --- | --- | --- | --- |
| system-design-contracts-stay-small-when-read-only | yes | yes | yes | yes |
| estimate-poc-tickets | yes | yes | yes | yes |
| evaluation-selected-source-support | no | no | yes | no |
| memory-ingestion-scan-detection | no | yes | yes | yes |
| memory-local-document-completeness | no | no | no | yes |
| Total | 2/5 | 3/5 | 4/5 | 4/5 |

Every load was through the Skill tool. The misses still start with a glob
that lists the skill's files (in the add-dir miss, the agent globbed the
added directory by name) and then read a reference directly. No catalogue
leaked a skill, no agent read a grader file, and in the final run no tool
call was refused.

**Per assertion.** Phase 1 columns are its two single judge passes; the
others are the three votes (P, F, U = ungraded), majority first in the
totals.

| Scenario | A | Phase 1 | Phase 1 evidence ×3 | Run A | Add-dir | Final |
| --- | --- | --- | --- | --- | --- | --- |
| contracts-stay-small | A1 | P / P | PPP | FFF | FFF | PPP |
| contracts-stay-small | A2 | F / F | FFF | PPP | FFF | FFP |
| contracts-stay-small | A3 | P / P | PFP | PPP | PPP | FPP |
| contracts-stay-small | A4 | P / P | PPP | FPF | PPP | PPP |
| estimate-poc-tickets | A1 | P / P | PPP | PPP | FFP | PPP |
| estimate-poc-tickets | A2 | P / P | PPP | PPP | PPP | PPP |
| estimate-poc-tickets | A3 | F / P | PPP | PFP | FPP | PPP |
| estimate-poc-tickets | A4 | P / P | PPP | PPP | PPP | FPF |
| selected-source-support | A1 | P / P | PP | PPP | PPP | PPP |
| selected-source-support | A2 | P / P | PP | PPP | PPF | FFF |
| selected-source-support | A3 | P / P | PP | FFF | FPP | FFP |
| selected-source-support | A4 | P / P | PP | PPP | PPP | FPP |
| selected-source-support | A5 | F / F | FF | FFF | FFF | FFF |
| ingestion-scan-detection | A1 | P / P | PPP | PPP | PPP | PPP |
| ingestion-scan-detection | A2 | P / P | PPP | PPP | PPP | PPP |
| ingestion-scan-detection | A3 | F / F | FFF | PPP | PPP | PPP |
| ingestion-scan-detection | A4 | F / F | FFF | PPF | FFF | FFF |
| ingestion-scan-detection | A5 | P / P | PPP | PPP | PPP | PPP |
| local-document-completeness | A1 | P / P | PPP | PPP | FPP | PPP |
| local-document-completeness | A2 | P / P | PPP | PPP | FPP | PPP |
| local-document-completeness | A3 | F / P | UFF | FFF | FFF | FFF |
| local-document-completeness | A4 | P / P | PPF | PPP | PPP | PPP |
| **Passed (majority)** | | 16 / 18 | 17 | 17 | 16 | 15 |
| **Unstable assertions** | | 2 flipped | 3 | 3 | 6 | 5 |
| **Mean agreement** | | | 0.95 | 0.96 | 0.91 | 0.93 |

**Reading it.**

- Judge stability: on the phase 1 evidence the three-vote majority matches
  each earlier single pass on 21 of 22 assertions; the two phase 1 flips came
  out PPP (estimate A3) and UFF (completeness A3, flagged unstable). Across the
  new runs 3 to 6 of 22 assertions are unstable, so a single judge pass would
  have reported roughly one in five of them by chance. The unstable ones are
  the judgement-heavy assertions (calendar waits, the governed review path,
  the five-dimension labels).
- Run-to-run variation of the agent is larger than the judge's: the same
  scenario and runner gave contracts-stay-small A1 FFF in two runs and PPP in
  the third. Five scenarios once each cannot show whether skill loading
  changes outcomes; the pass totals (15 to 17) are within that noise.
- The judge now sees the grader material. For selected-source-support it
  grades against the expected labels (A2 and A3 fail in the final run on
  `s05` "unsupported rather than contradicted" and `s11`, the labels the
  calibration reference itself calls provisional conventions), which phase 1's
  judge, without the key, could not do. For ingestion the inventory confirmed
  the agent's dimension and scale extraction (A3 now passes).
- Quotes: 5 of 22 final quotes were not found verbatim, mostly elided JSON
  excerpts (`"case_id": "s03", ... "support": ...`) in the source-support
  case; `quote_found` flags them as before.

Artifacts: [final](artifacts/scenarios-2026-10-27-runner-fix/final/),
[run A](artifacts/scenarios-2026-10-27-runner-fix/run-a-memory-on/),
[add-dir](artifacts/scenarios-2026-10-27-runner-fix/add-dir/) (results,
`agent.json`, final answers, every judge reply and the files each agent wrote;
transcripts and copied skills left out),
[phase 1 evidence re-judged](artifacts/scenarios-2026-10-27-runner-fix/phase1-evidence-rejudged-x3.json)
and the two probes.

## For the fixture-building phase

- A scenario entry is `{"status": "runnable" | "repo-fixture", "copy":
  [{"from": "<repo path>", "to": "<workspace path>"}], "grader": [{"from":
  "evals/graders/<id>/<file>"}], "note": "..."}`. Copy sources must not come
  from `evals/graders` or `evals/trials`; grader files must be listed (the
  check fails on an unlisted one) and must not share a name with any file in
  `skills/`.
- The workspace is plain files: no `.git`, no setup step and no shell for the
  agent by default. Scenarios that need git history, a running test suite or
  measured recall need either a fixture that does not depend on them or a
  deliberate `--agent-tools` choice, which the results record as unconfined.
- Two runnable scenarios reuse a skill's own worked example
  (selected-source-support's cases and the ingestion pack, whose generator
  script and reference describe the pages). They are not blind; a separate
  pack per scenario would make them so. The same applies to any new fixture
  built from `skills/*/assets` or `skills/*/tests/fixtures`.
- Scenario contexts are shown to the agent verbatim as the situation, so a
  context should not name grader paths; say the answers are "held back".
- Prefer `--skill-install add-dir` when comparing loading behaviour: it kept
  skill files out of the workspace glob (4 of 5 loads in one run) while
  leaving the project install as the default the brief asked for.

## Checks

`.venv/bin/python scripts/check_repo.py` passed on Python 3.12.9 (153
repository tests, including the new grader-material, confinement,
skill-loading and judge-repeat tests).
