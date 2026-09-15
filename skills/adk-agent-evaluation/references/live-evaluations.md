# Fixed and managed live evaluations

Use this mode when actual model decisions, response quality or multi-turn behaviour must be measured. Read-only inspection and offline preparation come first. Permission to implement evaluation code does not authorise paid calls, API activation, deployment or cleanup.

## Prepare a reviewable run

1. Record the target Python, ADK and model-client versions from its existing environment. Inspect the installed public `AgentEvaluator` signature, configuration schema and CLI help. Preserve pins. The tested ADK 2.8.0 path uses `AgentEvaluator.evaluate(agent_module=..., eval_dataset_file_path_or_dir=..., num_runs=..., output_file=...)`; optional arguments and result-export facilities must be verified before use. Do not invent missing wrapper scripts or silently migrate public facades.

2. Select reviewed synthetic cases and explicit criteria. Use trajectory `EXACT`, `IN_ORDER` or `ANY_ORDER` according to the workflow, with stable argument checks and independent forbidden-action assertions. ROUGE measures lexical overlap, not factual completion or authorisation. Rubrics require human-labelled positive and negative calibration examples. Validate assets locally against installed schemas before spending money.

3. Declare fixture isolation. Fresh sessions do not reset business stores. An evaluator that resets once before `num_runs` can measure idempotent repeats rather than independent creations. For independent trials, initialise a fresh backend per trial or use separate processes. Preserve existing workflow state when continuity is the intended test.

4. Present the exact account/authentication route, project, region, models, test targets, data, commands, case/trial counts, deadlines, retry limits and cost bound. Obtain explicit approval for paid tests on an isolated target; reuse prior approval only within that same scope. Changes to IAM, billing, APIs, resources or deployment require their own exact proposal and approval. Never disable a working API to manufacture activation coverage.

## Authentication and execution

For Vertex, distinguish the active CLI account from Python ADC and its quota project. Verify identity, selected project/API readiness and credential refresh without printing credentials. Refresh alone does not establish model or scorer access. Missing credentials are a blocker for live execution, not a reason to create keys or grant broad roles.

ADK 2.8.0's tested managed-metric facade can prefer `GOOGLE_API_KEY` when both routes are present. Its verified Vertex invocation uses a process-local blank `GOOGLE_API_KEY` with `GOOGLE_GENAI_USE_ENTERPRISE=true`, explicit project/location and ADC. Inspect the target client's routing before applying version-specific variables. Preserve stored keys; do not print or overwrite them. Developer API inference and Vertex managed scoring have different prerequisites.

Run the approved command in a worker process with a parent-owned wall-clock deadline. Synchronous grading can block an asyncio timeout. Terminate only the owned worker/process group on deadline and reap it; surface nonzero exits. Validate positive runs/timeouts. Test the deadline offline with a deliberately blocked grading boundary and enough startup budget to reach it. Local termination cannot cancel already accepted provider requests or guarantee their cost.

## Managed simulation

Record three roles separately: agent model, simulated-user model and managed scorer. Do not assume the scorer uses either model identifier or shares their settings. Use scenario-based metrics compatible with generated conversations, such as multi-turn task success and tool-use quality; fixed-answer comparisons may be unsuitable. Set simulator turns, model/tool calls, output and elapsed-time bounds where supported, and disclose unimplemented limits. Turn limits are not call or currency limits.

## Completion and provenance

Require every expected case/trial/metric result, evaluated status and configured threshold; aggregate success or exit zero can hide failed rows. Keep failed and incomplete trials. Separate infrastructure failure from product failure, and never retry a quality failure merely to obtain green.

Retain sanitised results, source/config/dataset/fixture hashes, resolved dependencies, requested/returned model versions, generation settings, authentication mode and timestamps. Report unavailable managed scores as unavailable. Captured-response replay proves conditional application behaviour, not a new live run. Separate cleanup, confirm its exact owned targets, and verify deletion without touching pre-existing resources or credentials.
