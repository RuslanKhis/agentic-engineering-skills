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
