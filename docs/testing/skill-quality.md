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

Memory's inspector suite uses pytest. Workflow's normal job selects only
`test_inspect_project.py`; its runtime suite imports ADK. Optimization and auth
include optional SDK checks that report skips when their dependencies are
absent. The full inspector suite requires POSIX filesystem operations; Windows
compatibility has not been established.

### Optional runtime checks

When changing a runtime recipe, use its compatibility reference and a separate
environment with the recorded SDK versions. The default maintainer requirements
do not install those SDKs. Two suites outside the normal discovery tier are:

```bash
python -m unittest discover -s skills/adk-workflow-design/tests -p test_runtime_contracts.py
python -m unittest discover -s skills/adk-operational-guardrails/tests -p adk_boundary.py
```

Read their source and prerequisites first. Installing compatible SDKs also
enables optional optimization/auth checks. A skipped contract is not a passing
contract. Live evaluations remain separately scoped work. “Offline” here names
the intended dependencies and test design; the runner is not a network sandbox.

## Test natural activation

[activation.json](../../evals/activation.json) contains a positive and a nearby
negative request for each of the twelve skills. `should_trigger` means that
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

## Test composition and scope

[scenarios.json](../../evals/scenarios.json) covers missing specialists, existing
Agents CLI projects, an ordinary ADK project with optional Google skills,
Matt's test-first workflow, an unrelated edit and privacy/observability overlap.

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
