# Checking skill quality

*Selection, execution and evidence are separate things to test.*

This repository has automated package/helper checks and authored model-evaluation
cases. The latter are prompts and expectations, not recorded passes. Follow
[the maintainer setup](../../CONTRIBUTING.md#run-the-repository-checks) to run:

```bash
.venv/bin/python scripts/check_repo.py
```

## What the automated checks cover

| Layer | Checked | Limits |
| --- | --- | --- |
| Skill packages | Safe YAML, duplicate keys, required metadata, folder/name agreement, local Markdown resources, bundled licences, Codex invocation metadata and Python syntax | No model-quality score, external URL fetch, Markdown anchor validation or execution of bundled Python during package inspection |
| Evaluation inputs | Valid JSON, unique IDs, known target skills, positive/negative coverage, scenario context and assertions | Labels are not predictions or measured activation results |
| Maintainer tooling | Invalid packages, broken resources, invalid cases, empty discovery and failing suites | Tests the checks themselves |
| Offline helpers | Each specialist's existing inspector/checker/asset tests in a separate process | No real-model evaluation or cloud-deployment validation |

The runner fails on a selected suite containing zero tests. Running only
`unittest discover -s skills` is insufficient: the nested directories can
produce an empty successful run. Per-suite processes also avoid collisions
between files sharing names such as `test_inspect_project.py`.

Memory's suite uses pytest. Workflow's normal job selects
`test_inspect_project.py`, the synthetic `test_review_contract.py` and
`test_draft_consistency.py` separately;
its runtime suite imports ADK. Optimization and auth
include optional SDK checks that report skips when their dependencies are
absent. The full inspector suite requires POSIX filesystem operations; Windows
compatibility has not been established.

### Optional runtime checks

When changing a runtime recipe, use its compatibility reference and a separate
environment with the recorded SDK versions. The default maintainer requirements
do not install those SDKs. Three suites outside the normal discovery tier are:

```bash
python -m unittest discover -s skills/adk-workflow-design/tests -p test_runtime_contracts.py
python -m unittest discover -s skills/adk-operational-guardrails/tests -p adk_boundary.py
python -m unittest discover -s skills/adk-fastapi-backend/tests -p runtime_contracts.py
```

The third records google-adk 2.12.0 and FastAPI 0.141.1 behaviour the backend
recipe depends on; all eight passed on 23 October 2026.

A third optional step scans the packages themselves for the skill risks a
host's scanner would flag (prompt injection in instructions, suspicious
download URLs, credential handling): `uvx snyk-agent-scan@0.6.9 --ci skills`
in an ephemeral environment with a `SNYK_TOKEN`. It uploads the skill content
to Snyk's analysis API under Snyk's terms, so it is a maintainer's choice, not
part of `check_repo.py`, and it was documented from the tool's README and CLI
reference on 23 October 2026, not run here; its output schema is declared
experimental, so only the exit code (1 when risks or failures remain) is read.

A fourth optional step cross-checks the packages against the Agent Skills
reference validator. The published wheel (`skills-ref` 0.1.1 on PyPI) installs
a command named `agentskills`, not `skills-ref`: run `agentskills validate
skills/<name>` in an ephemeral environment (exit 0 valid, 1 errors). The npm
package of the same name is an unrelated port. All 25 packages passed it on 26
October 2026 (agentskills/agentskills commit 69ef37e, Apache-2.0; the upstream
README calls the library a demonstration). `validate_skills.py` mirrors its
three stricter rules, so CI does not depend on it: no `---` inside the
frontmatter, no inline `{...}` or `[...]` YAML and no anchors or aliases.

Read their source and prerequisites first. Installing compatible SDKs also
enables optional optimization/auth checks. A skipped contract is not a passing
contract. Live evaluations remain separately scoped work. “Offline” here names
the intended dependencies and test design; the runner is not a network sandbox.

## Test natural activation

[activation.json](../../evals/activation.json) contains a positive and a nearby
negative request for each skill. `should_trigger` means that
the named skill is relevant; it does not require exclusive selection.

For each case:

1. Start a fresh coding-agent session with the candidate skill packages installed.
   Confirm the host can discover them. Use the same other installed collections
   in each compared condition.
2. Give it only the `prompt`, the necessary project context and a clean fixture.
   Keep `skill`, `should_trigger` and `rationale` in the grader's record.
3. Inspect the transcript for which skills and references were actually loaded.
   A filename appearing in the answer does not establish that it was read.
4. Record the target skill's actual activation and compare it with the label.
   Review ambiguous labels; another valid specialist selection may be useful.

### Run the activation runner

[`scripts/run_activation.py`](../../scripts/run_activation.py) automates the
description-only part of this check, which the [8 October
trial](activation-trial-2026-10-08.md) did by hand. A selector model sees the
catalogue built from every `SKILL.md` frontmatter (name and description only)
and seeded, shuffled batches of prompts under neutral labels; it never sees
case ids, labels or rationales. The answers are graded with the 8 October
rules (PASS, PARTIAL, FAIL; ERROR when a batch reply cannot be read) and
written to a results JSON with the catalogue and corpus hashes, the model and
every case's grade and reason:

```bash
.venv/bin/python scripts/run_activation.py --backend claude-cli --repeat 2 --out after.json
.venv/bin/python scripts/run_activation.py --backend claude-cli --model claude-haiku-5-5 --out haiku.json
.venv/bin/python scripts/run_activation.py --compare before.json after.json
```

`claude-cli` uses the local Claude Code login through `claude -p` in an empty
directory, with tools, skills, settings, MCP servers and project instructions
switched off. No API key is used; there is no CI workflow for activation,
because it would need one. `files` writes the batch prompts to a
directory (`--export DIR`) for a person or fresh agent sessions to answer, then
grades the saved answers (`--import DIR`); keep that directory's
`manifest.json` away from the selectors, because it maps labels to case ids.
`--only skill-a,skill-b` limits the cases, never the catalogue. The default
model is `claude-sonnet-5-5`; `claude-opus-5-5` and `claude-haiku-5-5` also
work. `--compare` lists every case whose grades changed and exits 1 when a
case gained a FAIL.

**After any change to a description or to routing** (an exclusion, a
supporting-skill hand-off, adk-engineer's selection table), re-run activation
on at least the default model and compare it with the last recorded run: the
change must introduce no new FAIL. Record a new PARTIAL with the reason the
selector gave. A description-only selector still says nothing about a host's
own loader, which the steps above test.

Use explicit `/skill-name` or `$skill-name` separately to test execution after
invocation. An explicit-invocation pass says nothing about natural discovery.
The current corpus is a small starting set; add paraphrases and held-out
requests when a real misrouting appears.

One run per case does not measure activation. Run each query three times in
fresh sessions and score its trigger rate: a positive passes at 0.5 or above, a
negative below 0.5. Mark each activation case `"split": "train"` or `"split":
"held-out"`. When a description is revised to fix misses, revise against the
training cases only and choose the version by its held-out pass rate, which may
not be the last version written; keep it under 1,024 characters, since
descriptions grow during this work, and keep its "Do not activate for"
exclusions, which an optimisation for triggering tends to erode. Three
descriptions are already within 20 characters of the limit
(adk-agent-interoperability, adk-agent-security, adk-presenter); to make room,
cut wording that restates the coverage list before any exclusion, never an
exclusion (the Agent Skills description guide and anthropics/skills
`skill-creator`'s optimisation loop, agentskills commit 69ef37e and
anthropics/skills commit dbd4588, read 2026-10-26; the guide is CC BY 4.0 and
paraphrased here; the automated loop itself needs Claude Code and live model
calls and is not used).

## Test composition and scope

[scenarios.json](../../evals/scenarios.json) covers missing specialists, existing
Agents CLI projects, an ordinary ADK project with optional Google skills,
Matt's test-first workflow, an unrelated edit, privacy/observability overlap,
and system-design conversations and architecture reviews.

Provide the `prompt`, a fixture matching `context`, and only the declared
`available_skills`. Keep `expected_primary` and `assertions` with the grader.
For missing-skill cases, verify the skill is unavailable both in the catalogue
and on disk. Ensure global installations cannot supply it accidentally.

Grade observable work: preserved files, actual effects, executed checks and
loaded instructions. An agent that writes a sound plan has completed a design
case, not an implementation case. Store the fixture alongside any published
result so others can check that distinction.

### Run the scenario runner

[`scripts/run_scenarios.py`](../../scripts/run_scenarios.py) runs a chosen
subset in throwaway workspaces and grades the assertions with a separate judge:

```bash
.venv/bin/python scripts/run_scenarios.py list
.venv/bin/python scripts/run_scenarios.py run --ids estimate-poc-tickets,memory-ingestion-scan-detection \
  --max-turns 30 --timeout 900 --max-budget-usd 3
```

Each scenario gets a fresh directory under `--tmp-root` (default: the system
temporary directory) holding its fixture and only those of its
`available_skills` that exist in this repository, under `.claude/skills/`. The
`claude-cli` agent runs headless with project settings only, so a global
installation cannot supply a skill, and without a shell by default
(`--agent-tools` changes that); `AGENTIC_ENGINEERING_HOME` points into the run
directory. The prompt is given with the context as the situation and a note
that nobody will answer questions. The judge (`--judge-backend claude-cli`
or `files`) sees the assertions, the final answer, the files the
agent wrote and the skills it loaded, and returns PASS or FAIL with a quote;
the runner records whether each quote occurs in the evidence. With
`--backend files`, `run` only prepares the workspaces for a person or another
agent, and `judge --run-dir DIR` grades what they saved.

[scenario-fixtures.json](../../evals/scenario-fixtures.json) says which
scenarios are runnable in an empty workspace, which need a fixture copied from
this repository, and (by omission) which describe fixtures that do not exist
yet. Those are reported as `fixture-missing` and never run against nothing;
`list` prints all three groups. Building a missing fixture and moving its
scenario into the file is how the runnable set grows.

## Compare execution against a baseline

Start with a representative task; the existing
[memory](artifacts/memory/README.md), [refund](artifacts/api/README.md) and
[workflow](artifacts/workflow/README.md) artifacts provide previous prompts,
starting code and independent acceptance checks. Their historical runs were
skill-enabled smoke tests, not paired proof of improvement.

1. Copy the same initial fixture into separate temporary projects. Keep model,
   host configuration, dependencies, task, permissions and acceptance checks
   fixed. Snapshot the old skill before editing it.
2. Run the candidate and either the previous version or a no-skill baseline in
   fresh sessions. For a no-skill condition, remove or disable discovery of this
   collection in that session; omitting an explicit command alone is insufficient.
3. Keep the executing agent separate from the acceptance grader. Retain outputs
   and transcripts for each condition, including failures and incomplete runs.
   Blind the grader: label the two conditions A and B at random per task,
   write the mapping to a `blind_mapping.json` before grading, remove session
   reports and tool folders that name the condition, score the pre-registered
   assertions per pair first and a holistic preference second, and allow
   ties. An assertion that passes in both conditions shows nothing about the
   skill; report it as non-discriminating (anthropics/skills commit dbd4588,
   `skills/skill-creator/agents/analyzer.md`, Apache-2.0, read 2026-10-26; its
   comparator writes its rubric after reading both outputs, which this
   procedure does not adopt).
4. Repeat according to a plan chosen before examining scores. Keep held-out
   cases out of the improvement loop. Start small and expand where findings
   warrant it; there is no required universal number of trials.
5. Compare outcome quality and scope preservation alongside latency and token
   usage where available. A slower, more expensive skill needs a corresponding
   benefit. Report missing usage data as unavailable.

### Record each trial

Keep a record under `docs/testing/` for results worth retaining; put large raw
artifacts in an appropriately controlled location. Record:

- Case ID, unchanged prompt and fixture location/hash.
- Candidate or baseline condition; skill commit/content hash and actual installed
  files; other active skills, coding-agent version, model and reasoning setting.
- Trial number, start/end time and available usage data.
- Transcript and output artifacts, with sensitive content removed.
- Each assertion's pass/fail/unverified result and the supporting observation.
- Test commands and results, skipped checks, permission/network limits and any
  manual grading decision.

Report raw counts when samples are small. Do not turn “all inputs are valid” or
“the agent mentioned the skill” into a success rate. A comparison with no
baseline cannot establish improvement; a scope walkthrough cannot establish
working ADK or cloud integration.

The [research note](../research/skill-quality-practices.md) links to the primary
specification, authoring guidance and studies informing this protocol.

The initial [executed check results](skill-quality-results.md) record the local
test counts and a single independent composition walkthrough, including their
limits and retained synthetic artifacts.
