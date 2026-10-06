# AI-engineering practices: gap review and Phase 1 record

Reviewed on **6 October 2026**. This records why three cross-framework
specialists and a context-window reference were added, what evidence they rest
on, and what the checks establish. Upstream documentation, model line-ups and
issue trackers change; every dated URL below should be re-read before it is
relied on for a new target.

## Method and conclusion

Eight parallel reviews compared current practice in general AI engineering
with the thirteen existing skills: agent instructions (prompt engineering),
context engineering, tool interface design, observability, agent security,
release engineering, MCP and A2A interoperability, and structured output with
model configuration. Each review read the relevant skill files first, then
primary sources (Google, Anthropic and OpenAI guidance, the official ADK
documentation, peer-reviewed studies) and practitioner material. A second pass
per Phase 1 area mined ADK-specific sources: the `adk-docs` repository, the
ADK Python source at the pinned 2.8.0 tag and on `main`, Google samples and
blog posts, and the `google/adk-python` issue tracker.

The existing skills were deep on **boundaries and evidence** (workflow control,
safe external calls, budgets and approval, deployment, memory, evaluation,
sensitive data, credentials, SQL). The gaps clustered around **what the model
sees and emits** and the **production lifecycle**: instruction text,
tool declarations, output contracts and model configuration, context-window
composition, observability, security threat modelling, release engineering and
cross-process interoperability. Prompt guidance, for example, existed as three
fragments across the evaluation and workflow skills with no owner.

## Gaps and decisions

| Area | State before | Decision |
| --- | --- | --- |
| Agent instructions | Prompt skeleton inside the evaluation skill; document delimiting in the workflow skill; router sent prompt design to evaluation | New `adk-agent-instructions` (Phase 1) |
| Tool interface design | Nothing; `safe-api-tool-calls` covers the HTTP call only | New `adk-tool-interface-design` (Phase 1) |
| Output contracts and model configuration | Scattered across five skills | New `adk-model-and-output-contracts` (Phase 1) |
| Context engineering | Runtime levers already tested in the optimise skill, unnamed as a mode | New `references/context-window.md`, `scripts/context_budget.py` and a bounded tool-result asset in `optimise-adk-on-google-cloud` (Phase 1) |
| Agent security | Data screening, credentials and approval covered; no whole-agent threat model or adversarial suite | Proposed `adk-agent-security` (Phase 2) |
| Observability | Defensive pieces, GKE-centric; Google's agents-cli has an observability skill to defer scaffolding to | Proposed `adk-agent-observability` (Phase 2) |
| Release engineering | Seam between deploy (excludes prompt-only changes) and evaluation (excludes deployment) | Proposed `adk-release-engineering` (Phase 2) |
| MCP and A2A | Incidental mentions only | Proposed `adk-agent-interoperability` (Phase 3) |

Phase 2 and 3 proposals are recorded here as decisions to make, not as work
done. Their research notes (modes, reference lists, helper ideas, trigger and
near-miss prompts) are summarised in the review conversation and should be
re-verified before implementation.

## What the ADK sources changed

Checking against the 2.8.0 source corrected or sharpened several points that
the generic guidance would have got wrong:

- **No per-parameter descriptions reach the model on 2.8.0.** Both declaration
  paths send the whole docstring as the tool description; `Annotated` metadata
  is preserved from 2.10.0. Parameter meaning therefore lives in the name and
  the docstring body (`tools/_automatic_function_calling_util.py`).
- **Instruction templating honours no escape on 2.8.0.** The pattern
  `{+[^{}]*}+` treats `{{key}}` like `{key}`; backslash and `${var}` escapes
  are left alone only from 2.10.0. Literal braces need an `InstructionProvider`
  or optional placeholders (`utils/instructions_utils.py`; issues #628, #3527,
  #4606, #5706).
- **Schema with tools is gated by backend, not model.** Native response schema
  alongside tools applies when the Google LLM variant is Vertex and the model is
  Gemini; the API-key backend always uses the `set_model_response` workaround.
  The docs say "specific models, including Gemini 3.0" (`models/_capabilities.py`,
  `flows/llm_flows/basic.py`).
- **`static_instruction` moves `instruction` out of the system instruction**
  into request content, labelled with a preamble from 2.9.0; the dynamic tail
  must stay small and stable for caching (`flows/llm_flows/instructions.py`;
  issues #6062, #6216, #6652).
- **Sub-agent descriptions are rendered verbatim** into the parent's transfer
  instruction, so description quality is routing quality
  (`flows/llm_flows/agent_transfer.py`).
- **`FallbackModel` does not exist in 2.8.0**; it arrived in 2.9.0. The
  model-contracts skill says so and offers application-level alternatives.
- **Compaction and caching thresholds are source facts.** Config pairs must be
  set together; caching starts on the second turn and needs 2,048 tokens on
  Gemini 2.5 or 4,096 on Gemini 3; `min_tokens` gates on the previous request
  (`apps/_configs.py`, `agents/context_cache_config.py`).

Two web checks also mattered. Google's agents-cli deploy skill (v1.8.0) still
states that Agent Runtime lacks revision-based rollback, while the Agent Runtime
documentation updated 5 October 2026 describes revisions and traffic splitting
in Pre-GA on the v1beta1 API. The Gemini model and deprecation pages dated
1 October 2026 list `gemini-3.8-flash` as current, restrict the 2.5 line to
existing users, and retire `gemini-2.5-pro` on Vertex on 20 October 2026.

## Evidence quality

Most practices in this area are vendor guidance measured on each vendor's own
models, and vendors disagree on points such as instruction placement and
example count. Independent evidence exists for few-shot order and format
sensitivity, context rot with input length, the reasoning cost of strict format
constraints, and the multi-agent failure taxonomy. The skills label each claim
as vendor guidance, documented behaviour, independent evidence or
source-verified, and keep the repository's posture: inspect the target, keep
its pins, and measure before claiming improvement.

## Validation record

Executed in the clean maintainer environment (CPython 3.12.9, no ADK or GenAI
SDK installed) on 6 October 2026:

| Check | Result |
| --- | --- |
| `scripts/validate_skills.py` | 16 packages, 0 errors, 0 warnings |
| `scripts/check_repo.py` | 562 tests passed, 59 optional SDK checks skipped |
| New helper suites | `adk-agent-instructions` 12, `adk-tool-interface-design` 18, `adk-model-and-output-contracts` 18, optimise context helpers 15 |
| `git diff --check` | clean |

What this does not establish: live model behaviour, provider acceptance of a
schema, cache or compaction effects in a running session, skill selection by
any coding agent, or improvement over the previous instructions. The pinned
package could not be installed in the review environment (its package index
served google-adk up to 1.18.0), so ADK behaviour was verified by reading the
`v2.8.0` tag and `main` rather than by execution. The new activation and
scenario cases in `evals/` are written and structurally valid but have not been
run against a model.

## Follow-ups

1. Run the new activation and scenario cases in fresh sessions and record
   selection separately from execution, per the
   [quality evaluation guide](../testing/skill-quality.md).
2. Decide on Phase 2 (security, observability, release engineering) and
   whether to merge tool interface design into the instructions skill if the
   collection grows past what the router can hold.
3. Re-verify the dated model, deprecation and documentation pages before the
   next revision; the model-contracts skill bundles a dated lifecycle table that
   must be refreshed.
