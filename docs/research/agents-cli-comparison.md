# Agents CLI skills: comparison and integration opportunities

Reviewed on 15 September 2026. This is a source review and a set of recommendations; no Agents CLI setup, scaffold, evaluation, deployment or cloud operation was executed for this investigation.

## Conclusion

The collections fit together well when their roles are explicit. Agents CLI supplies a prescribed project lifecycle, generated infrastructure, CLI operations and a catalog of reference implementations. Agentic Engineering supplies focused ADK design, adaptation and verification of application boundaries: who may do what, what gets stored, how work stops, and what evidence supports success.

There is substantial overlap. Google's code skill includes memory, OAuth, guardrails and orchestration recipes; its evaluation skill includes deterministic custom metrics, holdouts and result inspection. Describe our contribution as additional engineering depth and support for existing projects, rather than claiming those subjects are missing upstream. Keep Agents CLI optional. The current [`adk-engineer`](../../skills/adk-engineer/SKILL.md) can already combine a chosen development workflow with focused domain guidance.

## Evidence and snapshot limits

The local source is the user-supplied `/Users/ruslankhissamiyev/Downloads/agents-cli-main/`. It has no `.git` directory, so its exact commit cannot be established from the download. All seven reviewed skills declare version `1.5.0`. Each root `skills/<name>/SKILL.md` is byte-identical to its counterpart under `src/google/agents/cli/skills/data/`, the packaged-data location. The review read all seven files and all twelve of our `SKILL.md` files, plus relevant recipe, memory, evaluation, deployment and telemetry references.

| Downloaded skill | SHA-256 prefix of `SKILL.md` |
| --- | --- |
| `google-agents-cli-adk-code` | `e4a4c809593378d7` |
| `google-agents-cli-deploy` | `58f5ca47c93e92d3` |
| `google-agents-cli-eval` | `e5b00d959783f5d3` |
| `google-agents-cli-observability` | `c8286cf61cad4c2b` |
| `google-agents-cli-publish` | `3b8a063f6a62fc48` |
| `google-agents-cli-scaffold` | `e574ded4906e9d3c` |
| `google-agents-cli-workflow` | `3f7af2536bd7daad` |

The official [skills reference](https://google.github.io/agents-cli/reference/skills/) currently lists the same seven names and roles. Live raw-source retrieval returned version `1.5.0` for [workflow](https://raw.githubusercontent.com/google/agents-cli/main/skills/google-agents-cli-workflow/SKILL.md) and [evaluation](https://raw.githubusercontent.com/google/agents-cli/main/skills/google-agents-cli-eval/SKILL.md), but version `1.3.1` for [observability](https://raw.githubusercontent.com/google/agents-cli/main/skills/google-agents-cli-observability/SKILL.md). These web responses may reflect different cached revisions; they do not identify the downloaded commit. Detailed findings below refer to the supplied snapshot unless stated otherwise. Links to upstream `main` identify the source to recheck, not an immutable version guarantee.

The downloaded skill instructions were read as material being evaluated. Their commands, approval rules and workflow requirements were not activated for this research task.

## How the responsibilities fit

| Agents CLI skill | What it contributes | Agentic Engineering contribution |
| --- | --- | --- |
| [`workflow`](https://github.com/google/agents-cli/blob/main/skills/google-agents-cli-workflow/SKILL.md) | Understand → study recipes → scaffold → build → evaluate → deploy → publish → observe; project conventions and troubleshooting. | [`adk-engineer`](../../skills/adk-engineer/SKILL.md) selects the ADK specialist for the current feature or defect, preserving the project's conventions and the user's chosen process. |
| [`scaffold`](https://github.com/google/agents-cli/blob/main/skills/google-agents-cli-scaffold/SKILL.md) | Create, enhance and upgrade the generated project; prototype, hosting, CI/CD, session and A2A wiring. | [`adk-workflow-design`](../../skills/adk-workflow-design/SKILL.md) chooses application control flow; [`deploy-adk-on-google-cloud`](../../skills/deploy-adk-on-google-cloud/SKILL.md) assesses identity, package, state and lifecycle contracts. |
| [`adk-code`](https://github.com/google/agents-cli/blob/main/skills/google-agents-cli-adk-code/SKILL.md) | API cheatsheets and topic-indexed implementations to study. Recipes include cross-session memory, OAuth, safety plugins and durable approval. | [`adk-memory-architecture`](../../skills/adk-memory-architecture/SKILL.md), [`safe-api-tool-calls`](../../skills/safe-api-tool-calls/SKILL.md), [`adk-operational-guardrails`](../../skills/adk-operational-guardrails/SKILL.md) and [`adk-tool-auth-and-secrets`](../../skills/adk-tool-auth-and-secrets/SKILL.md) adapt those patterns to the actual identity, persistence, failure and replay requirements. |
| [`eval`](https://github.com/google/agents-cli/blob/main/skills/google-agents-cli-eval/SKILL.md) | Dataset/trace formats, generation and grading, managed or custom metrics, simulation, comparison and optional optimization. | [`adk-agent-evaluation`](../../skills/adk-agent-evaluation/SKILL.md) adds real-Runner tests with a scripted model, effect assertions, isolated state and strict evidence/coverage requirements. |
| [`deploy`](https://github.com/google/agents-cli/blob/main/skills/google-agents-cli-deploy/SKILL.md) | CLI deployment, infrastructure, CI/CD, service accounts, recovery and binding to an existing Agent Gateway. | Our deployment specialist checks the chosen delivery path, ownership, identity and actual hosted behavior; it should preserve the generated project's delivery mechanism. |
| [`observability`](https://github.com/google/agents-cli/blob/main/skills/google-agents-cli-observability/SKILL.md) | Tracing, prompt/response export, BigQuery Agent Analytics and provider integrations. | [`optimise-adk-on-google-cloud`](../../skills/optimise-adk-on-google-cloud/SKILL.md) turns measurements into tested performance changes; [`protect-adk-sensitive-data`](../../skills/protect-adk-sensitive-data/SKILL.md) checks every enabled content sink. |
| [`publish`](https://github.com/google/agents-cli/blob/main/skills/google-agents-cli-publish/SKILL.md) | Gemini Enterprise ADK/A2A registration and Agent Registry guidance. | No direct equivalent is needed. Our auth and data specialists can verify relevant caller and disclosure boundaries around publication. |

Our [`adk-frontend-integration`](../../skills/adk-frontend-integration/SKILL.md) adds custom JSON/AG-UI browser contracts, session ownership and safe output release. Our [`adk-sql-agent-engineering`](../../skills/adk-sql-agent-engineering/SKILL.md) adds reviewed business semantics, selective schema context and application-controlled query execution. Google's A2A support and analytics logging solve different interface/data tasks; they do not replace these specialists.

## Composition needs an explicit scope

### 1. A lifecycle skill is more than an API reference

The upstream workflow describes itself as always active. It requires a spec approval and scaffolding/enhancement before code, mandates evaluation, and prescribes `uv`. The ADK code skill loads this workflow before implementation. Our skills preserve the current package manager, ask only for unresolved decisions and support focused changes without adopting a scaffold. Merely installing another named skill does not resolve these policy differences. [Upstream workflow](https://github.com/google/agents-cli/blob/main/skills/google-agents-cli-workflow/SKILL.md), [code skill](https://github.com/google/agents-cli/blob/main/skills/google-agents-cli-adk-code/SKILL.md), [our router](../../skills/adk-engineer/SKILL.md)

**Recommendation:** distinguish two routes in user guidance: an Agents CLI project using its lifecycle, and an existing ADK project using our specialists with selected upstream material as reference. State the user's intended route and scope in the prompt. Do not automatically run `scaffold enhance` because an installed skill recommends it. In an adopted Agents CLI project, use its generated conventions and one agreed spec; avoid creating a second competing interview or project structure.

### 2. Separate deterministic evidence from real-model evaluation

Upstream discourages pytest assertions about unpredictable LLM wording. Our scripted-model Runner tests exercise deterministic application behavior: a denied operation executes zero writes, a tool cannot select another user's credential, or a repeated request preserves one operation. These are compatible forms of evidence. Upstream also supports local Python metrics and recommends holdouts, so neither is a missing upstream feature. Its local custom metric runs in the CLI process and can itself make network calls; “local” does not establish a hermetic test. [Upstream eval skill](https://github.com/google/agents-cli/blob/main/skills/google-agents-cli-eval/SKILL.md), [our deterministic tests](../../skills/adk-agent-evaluation/references/deterministic-tests.md)

The snapshot writes native result JSON/HTML and explicitly warns when errors are excluded from mean scores. It still does not turn every below-threshold score into command failure. Our existing helper accepts ADK detailed CSV, not this JSON. Do not recommend passing Agents CLI artifacts directly to it. [Grade command](https://github.com/google/agents-cli/blob/main/src/google/agents/cli/eval/cmd_grade.py), [our result checker contract](../../skills/adk-agent-evaluation/references/result-auditing.md)

### 3. Decide deployment ownership and logging together

Upstream deployment says `infra single-project` is optional; its observability skill says to run that infrastructure step before the first Agent Runtime deployment when choosing the Terraform-managed route. Read together, these describe different ownership paths. A later switch can affect existing resources and sessions. Our lifecycle review can make the choice explicit before execution and retain deployment metadata and operation identities. [Deployment skill](https://github.com/google/agents-cli/blob/main/skills/google-agents-cli-deploy/SKILL.md), [observability skill](https://github.com/google/agents-cli/blob/main/skills/google-agents-cli-observability/SKILL.md), [our lifecycle guidance](../../skills/deploy-adk-on-google-cloud/references/lifecycle.md)

The snapshot's observability skill distinguishes trace/event content capture from a separate completion-upload path to GCS/BigQuery. Setting `OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT=NO_CONTENT` does not disable uploads controlled by `OTEL_INSTRUMENTATION_GENAI_COMPLETION_HOOK=upload` and `LOGS_BUCKET_NAME`. Our general instruction to inspect exporters separately is a good foundation for a concrete Agents CLI check. [Upstream logging reference](https://github.com/google/agents-cli/blob/main/skills/google-agents-cli-observability/references/cloud-trace-and-logging.md), [our data boundaries](../../skills/protect-adk-sensitive-data/references/boundaries.md)

## Prioritized enhancements to our skills

These are proposals, not changes implemented by this review. Keep CLI syntax and complete upstream workflows in their owning collection.

| Priority | Enhancement | Concrete acceptance evidence |
| --- | --- | --- |
| 1 | **Recognize Agents CLI projects in the router and relevant inspectors.** Detect `agents-cli-manifest.yaml`, the declared agent directory, project guidance and an existing spec. Identify the user's selected lifecycle. Keep the collection optional and use only available skills. | A plain ADK project gets a focused edit without scaffold conversion; an Agents CLI project retains its manifest, runtime/A2A wiring and conventions; missing optional skills are reported without blocking independent work. |
| 1 | **Add an Agents CLI result adapter to evaluation.** Parse a recorded, versioned native result schema; check expected case/trial/metric coverage, duplicates, missing/error/nonfinite scores and configured threshold directions. Keep it separate from the existing CSV parser. | Synthetic fixtures reject an omitted case, duplicate observation, error hidden by a high average, malformed result and below-threshold score; a complete valid result passes. Record producer/schema versions and fixture provenance. |
| 1 | **Add an exporter-specific privacy checklist and tests.** Cover trace spans/events, completion uploads, BigQuery Analytics and any third-party exporter independently. Include content access, retention and user-erasure implications. | A synthetic canary is absent from each forbidden export payload. A disabled trace capture setting with an enabled upload path is detected. Tests do not need live customer content or cloud uploads. |
| 2 | **Add a delivery-path adapter to deployment.** Read the scaffold's build context, generated server/A2A files, manifest, deployment metadata and Terraform ownership before suggesting native ADK commands. Reconcile existing operations rather than starting a competing delivery path. | A fixture project preserves generated transport and identity wiring; repeated adaptation creates no duplicate resources/configuration; an uncertain prior operation produces a reconciliation plan. |
| 2 | **Add small, versioned recipe maps to memory, auth, guardrails and workflow references.** Point to matching upstream recipes and identify the seam worth adapting, while retaining our requirement-specific checks. | A memory example first distinguishes an exact user setting from semantic recall, then verifies consent, trusted scope, restart persistence and forgetting. An OAuth example tests disconnect/refresh ownership; a guarded write tests replay and uncertainty. |
| 2 | **Define an observability-to-evaluation handoff.** Let upstream establish the supported telemetry path; let our optimization/evaluation guidance select sanitized evidence, compare equivalent workloads and check quality alongside cost/latency. | A documented before/after case preserves the required result, identifies its clock/workload boundaries, retains failures and has explicit privacy treatment. |

Memory is a strong first integration example. Google's catalog points to `cross-session-memory` for Memory Bank wiring and recall. Our [memory reference](../../skills/adk-memory-architecture/references/memory-bank.md) distinguishes exact profile settings from semantic facts; requires consent at the actual write boundary; separates acceptance, completion and retrievability; and checks erasure against pending writes and replay. Link the recipe and add those acceptance cases. Do not claim that the catalog alone proves whether every recipe already implements or omits each control. [Upstream recipe catalog](https://github.com/google/agents-cli/blob/main/skills/google-agents-cli-adk-code/references/samples.md)

## Recommended next step

Publish concise guidance for using the collections together, with practical prompts and separate install instructions. Then implement the router detection and one memory/evaluation integration example before extending every specialist. A later combined smoke test should use a fresh installed coding-agent session, an isolated Agents CLI prototype, deterministic local checks and an explicit record of what was and was not exercised. The previous Codex/Claude tests of this collection alone do not establish combined compatibility.
