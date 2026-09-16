# Fixed and managed live evaluations

Use this mode when actual model decisions, response quality or multi-turn behaviour must be measured. Read-only inspection and offline preparation come first. Permission to implement evaluation code does not authorise paid calls, API activation, deployment or cleanup.

## Prepare a reviewable run

1. Record the target Python, ADK and model-client versions from its existing environment. Inspect the installed public `AgentEvaluator` signature, configuration schema and CLI help. Preserve pins. The tested ADK 2.8.0 path uses `AgentEvaluator.evaluate(agent_module=..., eval_dataset_file_path_or_dir=..., num_runs=..., output_file=...)`; optional arguments and result-export facilities must be verified before use. Do not invent missing wrapper scripts or silently migrate public facades.

2. Select reviewed synthetic cases and explicit criteria. Use trajectory `EXACT`, `IN_ORDER` or `ANY_ORDER` according to the workflow, with stable argument checks and independent forbidden-action assertions. ROUGE measures lexical overlap, not factual completion or authorisation. Rubrics require human-labelled positive and negative calibration examples. Validate assets locally against installed schemas before spending money.

3. Declare fixture isolation. Fresh sessions do not reset business stores. An evaluator that resets once before `num_runs` can measure idempotent repeats rather than independent creations. For independent trials, initialise a fresh backend per trial or use separate processes. Preserve existing workflow state when continuity is the intended test.

4. Present the exact account/authentication route, project, region, models, test targets, data, commands, case/trial counts, deadlines, retry limits and cost bound. Obtain explicit approval for paid tests on an isolated target; reuse prior approval only within that same scope. Changes to IAM, billing, APIs, resources or deployment require their own exact proposal and approval. Never disable a working API to manufacture activation coverage.

## Assemble assets from the real task

For the verified ADK 2.8.0 fixed-case shape, construct these fields from the target's tools and rules:

| Field | What to put there and check |
| --- | --- |
| `eval_set_id`, `eval_cases[].eval_id` | Stable dataset/case identities used by exported evidence and coverage checks. |
| `session_input.app_name`, `user_id`, `state` | Actual importable app name, synthetic session user and separately supplied trusted business identity. A user ID in dialogue is not authentication. |
| `conversation[].invocation_id`, `user_content` | Ordered turns, each with its own identity and real user message shape. Keep prior turns when reproducing stale state or a correction. |
| `conversation[].intermediate_data.tool_uses` | Expected names and arguments from the actual tool contract; an empty list expresses a no-tool expectation. |
| `conversation[].final_response` | A reviewed reference appropriate to that outcome; relationships to dynamic tool receipts may need separate deterministic assertions. |

The companion keeps `test_config.json` beside each eval set. Check the installed evaluator's discovery rules or explicit config argument before adopting that layout, and verify the exported criteria match what was selected. A file existing on disk does not prove the evaluator loaded it. Validate every selected set with `EvalSet.model_validate_json` and config with `EvalConfig.model_validate_json`; require a nonempty selection. Semantic review still needs to catch impossible cases, wrong identities and unsafe reference traces.

Choose fixed multi-turn cases when the user's sequence itself is the regression, such as correction after a refusal. Choose `conversation_scenario` when the user should adapt to the agent. Its `starting_prompt` supplies the initial request; its `conversation_plan` specifies facts withheld until asked, permitted disclosures, the observable goal and a stop condition. For a synthetic scheduling example: initially ask for a booking without a day; reveal a supplied available day only when asked; finish after the actual reservation is confirmed with its identifier. Bind trusted identity in session state independently of the simulator's story.

Inspect the resulting transcript for clarification, permitted disclosure, tool effects and truthful terminal status. A cooperative simulator can hide missing product capabilities; varied personas and real-user cases require separate review. Use [evaluation-design.md](evaluation-design.md) for solvability, dataset ownership, holdouts and judge calibration.

## Authentication and execution

For Vertex, distinguish the active CLI account from Python ADC and its quota project. Verify identity, selected project/API readiness and credential refresh without printing credentials. Refresh alone does not establish model or scorer access. Missing credentials are a blocker for live execution, not a reason to create keys or grant broad roles.

ADK 2.8.0's tested managed-metric facade can prefer `GOOGLE_API_KEY` when both routes are present. Its verified Vertex invocation uses a process-local blank `GOOGLE_API_KEY` with `GOOGLE_GENAI_USE_ENTERPRISE=true`, explicit project/location and ADC. Inspect the target client's routing before applying version-specific variables. Preserve stored keys; do not print or overwrite them. Developer API inference and Vertex managed scoring have different prerequisites.

For concrete project switching, dotenv precedence, read-only project/API queries, unknown activation outcomes and cleanup claims, use [environment-and-troubleshooting.md](environment-and-troubleshooting.md).

Run the approved command in a worker process with a parent-owned wall-clock deadline. Synchronous grading can block an asyncio timeout. Terminate only the owned worker/process group on deadline and reap it; surface nonzero exits. Validate positive runs/timeouts. Test the deadline offline with a deliberately blocked grading boundary and enough startup budget to reach it. Local termination cannot cancel already accepted provider requests or guarantee their cost.

## Managed simulation

Record three roles separately: agent model, simulated-user model and managed scorer. Do not assume the scorer uses either model identifier or shares their settings. Use scenario-based metrics compatible with generated conversations, such as multi-turn task success and tool-use quality; fixed-answer comparisons may be unsuitable. Set simulator turns, model/tool calls, output and elapsed-time bounds where supported, and disclose unimplemented limits. Turn limits are not call or currency limits.

Make score persistence an acceptance item before paid execution: inspect the installed results/export interface, exercise local serialisation with controlled data where possible, and verify the intended destination retains case/metric identifiers, status and numeric scores. Console capture or pytest `-s` is not a durable export contract. The historical managed run passed its thresholds but did not retain exact scores; report that limit instead of reconstructing values from a pass.

Use [execution-evidence.md](execution-evidence.md) for worker-deadline tests, logical-call versus transport-attempt accounting and usage deduplication; use [evaluation-design.md](evaluation-design.md) when implementing additional pre-dispatch budgets. Neither the historical campaign's observer nor a simulator turn limit is a shipped, universal spending cap.

## Completion and provenance

Require every expected case/trial/metric result, evaluated status and configured threshold; aggregate success or exit zero can hide failed rows. Keep failed and incomplete trials. Separate infrastructure failure from product failure, and never retry a quality failure merely to obtain green.

Retain sanitised results, source/config/dataset/fixture hashes, resolved dependencies, requested/returned model versions, generation settings, authentication mode and timestamps. Report unavailable managed scores as unavailable. Captured-response replay proves conditional application behaviour, not a new live run. Separate cleanup, confirm its exact owned targets, and verify deletion without touching pre-existing resources or credentials.
