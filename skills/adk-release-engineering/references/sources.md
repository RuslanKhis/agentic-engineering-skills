# Sources

Every claim in this skill is one of: **source** (read in a local checkout of google/adk-python on 2026-10-07), **vendor** (Google or another provider's documentation, with the date printed on the page or the fetch date), **practitioner** (experience reports, not reproduced here), or **community**. Where the skill reports no verification, [compatibility](compatibility.md) says so.

## ADK source, changelog and docs

| Reference | Type | Used for |
| --- | --- | --- |
| google/adk-python tag `v2.8.0` (2026-08-25): `cli/cli_tools_click.py`, `cli/conformance/cli_test.py`, `evaluation/agent_evaluator.py`, `evaluation/eval_config.py`, `evaluation/eval_metrics.py`, `evaluation/eval_set.py`, `evaluation/eval_case.py`, `evaluation/local_eval_sets_manager.py`, `evaluation/gcs_eval_sets_manager.py`, `evaluation/local_eval_set_results_manager.py`, `agents/llm_agent.py` | source | Pinned behaviour: eval CLI, judge default, metrics, CSV output, conformance modes, deploy options, default model |
| google/adk-python main at 2.11.0 (2026-10-01): `evaluation/eval_metrics.py`, `CHANGELOG.md` | source | Efficiency metrics, judge default unchanged, `ValueError` on zero cases, `num_samples=0` rejection |
| google/adk-docs `docs/evaluate/index.md`, `docs/evaluate/criteria.md`, `docs/deploy/cloud-run.md`, `docs/deploy/agent-runtime/*.md` | vendor, fetched 2026-10-07 | CI/CD criteria recommendation, `num_samples` majority vote, conformance as PR gate, `gemini-flash-latest` in examples, efficiency metrics informational, Cloud Run deploy routes |

## Google platform documentation

| URL | Page date | Used for |
| --- | --- | --- |
| https://ai.google.dev/gemini-api/docs/deprecations | 2026-10-01 | 2.0 Flash shutdown 2026-06-01; 2.5 limited to prior users; 3.1 Flash-Lite shutdown 2027-05-07; earliest-date semantics; new-project recommendation |
| https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/model-versions | 2026-10-05 | 12-month availability; 45-day short-term migration; dates may extend, never earlier; 2.5 retirement 2026-10-20; 3.5 Flash release 2026-05-19 |
| https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/migrate | fetched 2026-10-07 | Three regression types; repeat every eval; component-level evaluation; token-count changes; re-tune hyperparameters |
| https://docs.cloud.google.com/run/docs/rollouts-rollbacks-traffic-migration | fetched 2026-10-07 | `--no-traffic --tag`, `update-traffic --to-tags`, `--to-revisions`, in-flight requests complete |
| https://docs.cloud.google.com/gemini-enterprise-agent-platform/scale/runtime/manage-revisions-and-traffic | 2026-10-05 | Pre-GA `v1beta1`; immutable revisions; manual split or always-latest; archived unrecoverable; 950 and 6,000 limits; direct revision query |
| https://docs.cloud.google.com/vertex-ai/generative-ai/docs/model-reference/prompt-classes | fetched 2026-10-07 | `vertexai.prompts` `create_version`, `list_versions`, `restore_version` |
| https://raw.githubusercontent.com/google/agents-cli/main/skills/google-agents-cli-deploy/SKILL.md (v1.8.0) and the sibling eval skill | fetched 2026-10-07 | Three-stage pipeline with environment approval; Cloud Run `update-traffic` rollback; stale "Agent Runtime doesn't support revision-based rollback"; "`eval run` exits 0 whatever the scores are"; flaky-eval guidance; `eval grade --qps 5`; absence of prompt versioning, migration and eval-gate guidance |
| Cloud Deploy canary strategy for Cloud Run | 2026-10-05, reviewed by the research pass | `automaticTrafficControl`, percentages, verify tasks, `rollouts advance` |
| Agent Platform Evaluations documentation | GA 2026-07-31, reviewed by the research pass 2026-10-07 | Offline eval over traces by version or period; online monitors with sampling; `online_evaluator/scores` metric; GCS export path |
| https://docs.cloud.google.com/gemini-enterprise-agent-platform/reference/models/prompt-classes | fetched 2026-10-07 | `client.prompts.create`, `create_version`, `get_version` |

## Other vendor documentation

| URL | Fetched | Used for |
| --- | --- | --- |
| https://langfuse.com/docs/prompt-management/overview | 2026-10-07 | Immutable versions, labels, rollback by label move, config with prompt, trace linkage |
| https://langfuse.com/resources/engineering/llm-regression-testing | 2026-10-07 | Regression testing framing for LLM applications |
| https://www.promptfoo.dev/docs/integrations/ci-cd/ | 2026-10-07 | Pass-rate gate, 24-hour response cache, `--tag` with commit SHA |
| https://docs.confident-ai.com/docs/guides-regression-testing-in-cicd | 2026-10-07 | Regression testing in CI with thresholds and repeats |
| https://developers.openai.com/api/docs/guides/evaluation-best-practices | 2026-10-07 | Discriminative evals, continuous evaluation |
| https://platform.claude.com/docs/en/docs/test-and-evaluate/develop-tests | 2026-10-07 | Test development: specific, graded, automated where possible |

## Practitioner evidence (not reproduced)

| Work | Date | Finding used |
| --- | --- | --- |
| Hamel Husain, evals FAQ https://hamel.dev/blog/posts/evals-faq/ | 2025-05 | CI set of roughly 100 purpose-built cases; assertions over judges in CI; sampled reference-free judges in production; production failures become CI cases; write evaluators for discovered errors |
| Hamel Husain, prompt versioning https://hamel.dev/blog/posts/evals-faq/how-should-i-version-and-manage-prompts.html | 2025 | Git first; registry when prompt and code owners differ |
| tianpan.co, eval set as simulator and drift https://tianpan.co/blog/2026-04-27-eval-set-as-simulator-drift | 2026-04-27 | Drift modes; per-case freshness expiry |
| Eugene Yan, evaluation process https://eugeneyan.com/writing/eval-process/ | 2025-04 | Continuous eval refresh from production |

## Community reports (not reproduced)

google/adk-python issues #4410 (no `--num_runs` on `adk eval`), #7290 (`conformance test --mode live` unimplemented, open 2026-09-25), #7258 (`safety_v1` version drift, fixed 2.10.0), #7414 (lower-is-better custom metric, open 2026-10-05), #6725 (`NOT_EVALUATED` discarded), #4155 (MCP toolset race in parallel evals), #6683 (Vertex session IDs in evals), #5503 (`App.plugins` bypassed, fixed 2.7.0), #4193 (mocking tools in CI evals), #6951 (zero cases evaluated, fixed 2.10.0), #7128 (missing recordings, fixed 2.10.0). Google staff reply on discuss.google.dev (2026-07-06) on Agent Runtime traffic splitting and instance sizing. They are listed as symptoms to test for on the target.

## Repository references

Sibling skills are cited by name: adk-agent-evaluation (`scripts/check_eval_results.py`, quality iteration, evaluation design, experiment re-entry), adk-model-and-output-contracts (`scripts/audit_model_config.py`, `assets/model-lifecycle-2026-10-01.json`, model selection, sampling), deploy-adk-on-google-cloud (traceable artefact and rollback preparation, hosting specifics), adk-agent-instructions (prompt text), adk-operational-guardrails (runtime budgets), safe-api-tool-calls (idempotent writes under shadow traffic) and the sibling in preparation adk-agent-observability (sampling, metrics, alerts).
