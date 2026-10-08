# Select or escalate the model

Read this when choosing a model for a new agent, replacing one that is retiring, or deciding whether a stronger model would help. Model IDs, statuses and dates below are a snapshot; verify them at use time against the pages cited. The bundled `assets/model-lifecycle-2026-10-01.json` carries the same snapshot for `scripts/audit_model_config.py`.

## Current Gemini text models

From the Gemini API models page (https://ai.google.dev/gemini-api/docs/models, page dated 2026-10-06) and deprecations page (https://ai.google.dev/gemini-api/docs/deprecations, page dated 2026-10-07; both re-read 2026-10-08), both vendor documentation:

| Model ID | Status (Gemini API) | Release | Shutdown or note |
| --- | --- | --- | --- |
| `gemini-3.8-flash` | Stable | 2026-09-02 | None announced; the page's recommended Flash for new work |
| `gemini-3.7-flash` | Stable | 2026-08-13 | None announced |
| `gemini-3.6-flash` | Stable | 2026-07-21 | None announced |
| `gemini-3.5-flash` | Stable | 2026-05-19 | None announced; `LlmAgent.DEFAULT_MODEL` in ADK 2.8.0 |
| `gemini-3.5-flash-lite` | Stable | 2026-07-21 | None announced |
| `gemini-3.1-flash-lite` | Stable, retiring | 2026-05-07 | Shutdown 2027-05-07, replacement `gemini-3.5-flash-lite` |
| `gemini-3.1-pro-preview` | Preview | 2026-02-19 | None announced |
| `gemini-3-flash-preview` | Preview | 2025-12-17 | None announced; replacement listed as `gemini-3.6-flash` |
| `gemini-2.5-pro`, `gemini-2.5-flash`, `gemini-2.5-flash-lite` | Limited | 2025 | Served only to users who have actively used them; "For any new projects, use our latest models: 3.5 Flash-Lite or 3.8 Flash" |
| `gemini-2.0-flash`, `-001`, `gemini-2.0-flash-lite`, `-001` | Shut down | 2025 | Shutdown 2026-06-01 |

Shutdown dates on the deprecations page "indicate the earliest possible dates on which a model might be retired". The Vertex AI model lifecycle page (https://docs.cloud.google.com/vertex-ai/generative-ai/docs/learn/model-versions, page dated 2026-10-07, vendor documentation) commits to at least 12 months of availability after release and states that retirement dates "may be extended" and "won't be moved to an earlier date". Its table lists `gemini-3.5-flash` retiring 2027-05-19 or later, `gemini-3.5-flash-lite` 2027-07-21 or later, `gemini-3.1-flash-lite` 2027-05-07 or later, and `gemini-2.5-pro`, `gemini-2.5-flash` and `gemini-2.5-flash-lite` retiring **2026-10-20** with `gemini-3.8-flash` among the replacements. A 2.5 model in a Vertex deployment is therefore an urgent finding at the time of writing. The same page's shorter-availability table lists `gemini-3.6-flash` retiring 2026-11-19 and `gemini-3.7-flash` 2027-01-28, replacement `gemini-3.8-flash`, although the Gemini API announces no shutdown for either; the JSON carries these as `vertex_retirement`.

Use explicit version strings. An alias ending in `-latest` moves without a code change; the audit flags it. Models reached through `projects/.../publishers/google/models/...` paths force enterprise mode in `Gemini` (verified in `models/google_llm.py`).

## Decide with measurements, in this order

1. **Quality on the development set.** Run adk-agent-evaluation's two-stage escalation ("Escalate the model on the plainest contract"): stage 1 compares candidates on the plainest contract, stage 2 runs the winner through the full workflow. Record model, `thinking_level`, temperature, `max_output_tokens`, prompt version and backend with every run; the provider's defaults are part of the experiment.
2. **The four output metrics.** Schema validity, answer accuracy, executable accuracy and wrong-valid-schema, each separately ([validation](validation.md)). A model that improves validity while raising wrong-valid-schema is a regression.
3. **Finish reasons and thought tokens.** Read `finish_reason` and `usage_metadata.thoughts_token_count` per run. A cheaper model that hits `MAX_TOKENS` or needs a higher thinking level to match accuracy may cost more for the mix; adk-operational-guardrails' token-budgets reference records that stance.
4. **Lifecycle.** Prefer a stable model with no announced shutdown. A preview model is acceptable for an experiment and a finding in production.
5. **Capabilities you depend on.** Native schema with tools depends on the backend, not the model ([output schema and tools](output-schema-and-tools.md)); `thinking_level` support and defaults differ per model ([reasoning and sampling](reasoning-and-sampling.md)).

## Treat tiered routing as a hypothesis

FrugalGPT (Chen, Zaharia, Zou, 2023, independent evidence) reported up to 98% cost reduction on its benchmarks with a learned cascade; RouteLLM (2024, updated 2025, independent evidence) reported more than 2x cost reduction with a trained router at matched quality. Both results depend on a labelled development set, a quality threshold chosen in advance and a router trained or tuned for the task. Without those, routing by "cheap first" is a cost experiment with an unknown quality effect. ADK 2.8.0 has no router; `FallbackModel` (2.9.0) fails over on errors and does not route by cost or task ([failover and providers](failover-and-providers.md)). `RoutedLlm` exists in ADK TypeScript only. Build the labelled set first, then decide whether a second model earns its place.

## Record what the audit cannot see

The audit reads code. It cannot see the model chosen at runtime from an environment variable (`model_kwarg: dynamic`), the actual backend, or whether a `-latest` alias resolved to a retiring version yesterday. Record the resolved model from `LlmResponse.model_version` in logs or evaluation output and compare it with the intended ID at review time.
