# Version prompts, configuration and the release manifest

Read this when a prompt, model ID, judge ID or eval set changes and the question is where the version lives, how it is named, and what the changelog must say. Prompt wording itself belongs to adk-agent-instructions; this reference versions whatever that skill produces.

## Decide where prompt versions live

| Situation | Store | Why |
| --- | --- | --- |
| The people who edit prompts also deploy code (the common case for an ADK team) | Git, beside the agent. Prompt constants in `prompt.py` or files under `prompts/`, reviewed in the same pull request as the code and eval changes | One commit is one release unit; the eval gate sees prompt and code together; rollback is `git revert` plus the deploy reference. Hamel Husain's evals FAQ (prompt-versioning page, 2025, practitioner) recommends git first and a registry only when prompt iteration and deployment are owned by different people |
| Prompt authors cannot ship code (domain experts, a separate team, many agents sharing prompts) | A registry with immutable versions and environment labels: Langfuse prompt management (immutable versions, `production` and `staging` labels, rollback by moving a label, config stored with the prompt, versions linked to traces; docs fetched 2026-10-07, vendor) or Vertex AI Prompt Management (`vertexai.prompts`: `create_version(prompt, prompt_id=None, version_name=None)`, `get(prompt_id, version_id=None)`, `list_versions(prompt_id)`, `restore_version(prompt_id, version_id)`, `delete(prompt_id)`; the Agent Platform reference uses `client.prompts.create`, `create_version` and `get_version`; reference pages fetched 2026-10-07, vendor; whether a stored version is immutable was not confirmed from the narrative docs and must be verified before relying on it for rollback) | The label is the release; the trace link gives attribution; the config travels with the prompt |

A registry adds a runtime dependency and a second rollback surface. Record the resolved prompt version and its content hash at startup (log line and manifest), so a label move is visible as a release, and run the eval gate against the labelled version before the label moves, not after.

## Name versions so the manifest can carry them

- **Prompt**: `sha256` of the exact literal text that reaches `LlmAgent.instruction` or `global_instruction` after templating constants are resolved, plus a human label (`billing-v12`). The inventory helper reports the hash of each literal and constant it finds; a dynamic `instruction` (a callable or a value from a registry) is reported as `dynamic`, and the release must record the resolved hash some other way (a startup log, a registry version ID).
- **Model**: the exact string passed to `model=`, or to `Gemini(model=...)`, `LiteLlm(model=...)` and `FallbackModel(models=[...])`. Record one row per model, including the ADK default when `model=` is omitted (`LlmAgent.DEFAULT_MODEL` is `gemini-3.5-flash` in 2.8.0, verified in `agents/llm_agent.py`).
- **Judge**: every `judge_model` and `num_samples` in `test_config.json`, in `EvalConfig` literals and in `JudgeModelOptions(...)` calls. A criterion that relies on the default is recorded as `gemini-2.5-flash (ADK default, unpinned)` and treated as a finding.
- **Tool schema**: a hash of the function declarations the model sees. Produce it from a scripted-model test that captures `llm_request.config.tools` in a `before_model_callback`, serialised with sorted keys. A hash change without an intended tool change is a release event (a dependency changed the generated schema).
- **Eval set**: `sha256` of each `*.evalset.json` and `*.test.json` file, plus the `eval_set_id` and case count. The gate's expectations file names the same `eval_set_id` and case IDs.
- **Deploy reference**: the Cloud Run image digest and revision name, the Agent Runtime resource and revision ID, or the GKE image digest. A tag is not a reference; deploy-adk-on-google-cloud's production reference explains why.
- **Secrets**: Secret Manager version numbers (`projects/P/secrets/S/versions/7`), never values. `versions/latest` is an alias and a finding.

## Keep the changelog as data the next release can read

Use [assets/PROMPT_CHANGELOG.md](../assets/PROMPT_CHANGELOG.md). One row per release with date, prompt hash and label, model ID, judge ID and `num_samples`, eval-set hash, development-set delta by error category (adk-agent-evaluation's quality-iteration categories, or the project's own), holdout result (score and the date it was last used), rollback target (the previous row's manifest), approver and the evidence tier (local, mocked, live, not run). A row whose holdout field says "not run" is a valid row; a row whose holdout field is blank is not.

The development-set delta is a table of category counts before and after, not a single percentage, because a percentage hides which defect moved. Keep rows immutable; append a correction row rather than editing history.

## Treat these as release events

- A `-latest`, `-preview` or `-exp` alias in any model or judge field. Replace it with the concrete ID the alias resolves to today (log `LlmResponse.model_version` from one recorded run), then schedule upgrades as deliberate releases.
- An unset `model=` on an `LlmAgent`, which inherits the ADK default and therefore changes when `google-adk` is upgraded.
- A `google-adk` or `google-genai` upgrade: it can change the default model, the eval metric set and the judge default; re-run the gate and record the new pins.
- A judge change: it moves every judge-metric baseline. Run the old and new judge side by side on the frozen development set and record the disagreement rate before adopting the new judge.
- A tool schema hash change, a retrieval corpus refresh, or a secret rotation that the agent's behaviour depends on (a new API version behind the same secret name).

## Completion

The manifest for the release has a value for every component listed above or an explicit `unknown` with an owner and date; the changelog row exists; the previous row is identified as the rollback target; aliases are either removed or listed as accepted risks with a review date.
