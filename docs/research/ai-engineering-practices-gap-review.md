# AI-engineering practices: gap review and build record

Reviewed on **6 October 2026**, with Phases 2 and 3 completed on
**8 October 2026**. This records why seven cross-framework specialists and a
context-window reference were added, what evidence they rest on, and what the checks
establish. Upstream documentation, model line-ups and
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
| Agent security | Data screening, credentials and approval covered; no whole-agent threat model or adversarial suite | New `adk-agent-security` (Phase 2) |
| Observability | Defensive pieces, GKE-centric; Google's agents-cli has an observability skill to defer scaffolding to | New `adk-agent-observability` (Phase 2) |
| Release engineering | Seam between deploy (excludes prompt-only changes) and evaluation (excludes deployment) | New `adk-release-engineering` (Phase 2) |
| MCP and A2A | Incidental mentions only | New `adk-agent-interoperability` (Phase 3) |

All three phases are complete. Merging tool interface design into the
instructions skill remains an option if the router grows past what a coding
agent selects reliably; the activation corpus is the evidence for that call.

## What the Phase 2 sources added

A second research pass per area mined the official ADK documentation, the
ADK source at 2.8.0 and on `main`, Google's samples and blog posts, Google
Cloud documentation and the `google/adk-python` issue tracker. The findings
that changed the skills most:

- **Security.** ADK fences relayed other-agent output from 2.8.0 and
  server-supplied MCP tool descriptions from 2.10.0, but never an agent's own
  tool results or OpenAPI descriptions; the source comment says the fencing
  "raises the bar rather than closing the class". Three 2026 advisories
  (remote code execution in `adk web`, fixed 1.28.1 and 2.7.0; forged tool
  confirmations, fixed 2.5.0 and 2.6.0) and a public incident in which Google's
  own ADK triage agent was prompt-injected into triggering a privileged agent
  set the version-floor and agent-to-agent trust guidance. Open issues on
  confirmation enforcement for custom tools and approvals arriving over A2A are
  recorded as checks to run on a target. `ContainerCodeExecutor` disables
  networking by default; `BashToolPolicy` allows every command by default.
- **Observability.** The environment gates have a precedence order (an admin
  lock, then `RunConfig`, then environment) and `ADK_CAPTURE_MESSAGE_CONTENT_IN_SPANS`
  turns off only on `false` or `0`. On Agent Runtime the metric exporter is
  request-driven because CPU is throttled between requests, with a documented
  tail loss. Token accounting adds tool-use prompt tokens to input and thought
  tokens to output and takes the newest cumulative usage in a stream. The
  Telemetry API needs its own writer roles, and the BigQuery Agent Analytics
  plugin needs a job-user and table data-editor pair.
- **Release engineering.** `adk eval` returns exit code 0 even when cases
  fail; `AgentEvaluator` in pytest and `adk conformance test` fail properly.
  The evaluation judge defaults to `gemini-2.5-flash`, which Vertex retires on
  20 October 2026, so an unpinned judge silently shifts baselines. Efficiency
  metrics are informational and reject thresholds. Agent Runtime revisions can
  be queried directly, bypassing the traffic split, which is the documented
  shadow-test path.

## What the Phase 3 sources added

The interoperability pass read the MCP and A2A code paths in 2.8.0 and on
`main`, the protocol specifications, Google's Agent Platform and Gemini
Enterprise pages and the issue tracker:

- McpToolset pools sessions by a hash of the request headers, evicts idle
  sessions after fifteen minutes, caches tool lists per pool key and never
  subscribes to list-changed notifications, so a pinned tool manifest with a
  diff is the detector for a changed server. Agents and toolsets must be
  defined synchronously in the agent module for deployment. The default MCP SDK
  remains 1.x in 2.9.0 and later even though 2.x is supported.
- RemoteA2aAgent already validated card RPC targets in 2.8.0 (https or
  loopback, same origin); 2.9.0 extended the rule to the card URL itself. Task
  and context identifiers travel in event metadata under `a2a:` keys. The
  agent-card builder publishes tool descriptions and sub-agent skills and
  never the instruction. `to_a2a` only shapes the advertised URL; a served
  Workflow must emit a message event or the A2A task stays in progress.
- Agent Runtime serves the A2A card only behind authentication; Gemini
  Enterprise registration speaks A2A 0.3 and streaming, authenticates Cloud Run
  agents with a Google-signed OIDC header, bypasses Agent Gateway, and is
  limited to the same project. The a2a-sdk 1.x card shape differs from 0.3,
  so the card checker accepts both.

## Aligning the designer and the router

The seven specialists only help if the two entry points route to them and the
designer raises their decisions early. On 8 October 2026 three alignment
changes were made and checked:

- **Router.** `adk-engineer` carries one routing row per specialist, an
  extended row for context-window work, a paragraph on how the seven relate,
  and composition guidance for the overlap with Google's agents-cli
  observability, deploy, eval and publish skills (this toolkit decides, Google's
  skill operates the adopted mechanism).
- **Designer.** `adk-system-designer` gained eight handoff rows, design-level
  lessons in its decision reference (topology by boundary, tool source, "what
  the model sees is its only interface", the per-agent lethal-trifecta check,
  context-window shaping, model and judge and prompt versions as release
  artefacts, structured output as a backend-dependent contract, observability
  as a design obligation), five failure-review scenarios, a release-unit and
  observability section in the runtime reference, and template blocks for
  model-facing contracts, security posture, and observability and release. SDK
  recipes, parameter names and version tables stayed in the specialists. The
  decision reference grew by 38 percent, slightly over the intended third;
  trimming further would have dropped a tradeoff or a verification.
- **Selection trial.** A description-only trial over the 56-case activation
  corpus passed 55 cases with one soft miss, and a second model agreed on every
  primary; see the [record](../testing/activation-trial-2026-10-08.md). A
  scenario case for the designer covering the new concerns was added to the
  corpus but has not been run.

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
SDK installed) on 6 and 8 October 2026:

| Check | Result |
| --- | --- |
| `scripts/validate_skills.py` | 20 packages, 0 errors, 0 warnings (16 after Phase 1, 19 after Phase 2) |
| `scripts/check_repo.py` | 638 tests passed, 59 optional SDK checks skipped (562 after Phase 1, 607 after Phase 2) |
| Phase 1 helper suites | `adk-agent-instructions` 12, `adk-tool-interface-design` 18, `adk-model-and-output-contracts` 18, optimise context helpers 15 |
| Phase 2 helper suites (8 October) | `adk-agent-security` 15, `adk-agent-observability` 20, `adk-release-engineering` 10 |
| Phase 3 helper suite (8 October) | `adk-agent-interoperability` 31, against loopback fake MCP and card servers |
| `git diff --check` | clean |
| Activation trial (8 October) | 55 of 56 cases PASS, 1 PARTIAL, 0 FAIL from descriptions alone; repeat run on a second model agreed on every primary; see [the record](../testing/activation-trial-2026-10-08.md) |

What this does not establish: live model behaviour, provider acceptance of a
schema, cache or compaction effects in a running session, skill selection by
any coding agent, or improvement over the previous instructions. The pinned
package could not be installed in the review environment (its package index
served google-adk up to 1.18.0), so ADK behaviour was verified by reading the
`v2.8.0` tag and `main` rather than by execution. The new activation and
scenario cases in `evals/` are written and structurally valid but have not been
run against a model.

## Follow-ups

1. Run the scenario cases, and the activation cases inside real host sessions,
   per the [quality evaluation guide](../testing/skill-quality.md); the
   description-only trial is recorded but is not host behaviour.
2. Keep tool interface design and agent instructions separate; the trial
   showed no confusion between them. The one soft miss was the evaluation
   loop versus instruction work, which the descriptions already separate.
3. Re-verify the dated model, deprecation and documentation pages before the
   next revision; the model-contracts skill bundles a dated lifecycle table that
   must be refreshed.
