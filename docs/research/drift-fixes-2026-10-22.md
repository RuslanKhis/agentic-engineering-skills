# Fourteen drifted facts, re-verified and corrected — 22 October 2026

*Phase B of the external-sources integration. Input: the drift table in the
[research memo of 21 October](external-sources-integration-report-2026-10-21.md).
Every row was checked against its primary source on 22 October 2026 before
any text changed; where the memo and the source disagree, the source wins and
the row says so. Nothing was executed against a cloud project.*

## Method

For each row: grep the repository (`skills/`, `README.md`,
`docs/integrations/`, `evals/`) for every place that carries the claim; read
the primary source today; write the correction in place with the citation in
the form `(<source> <version or commit>, <file>, read 2026-10-22)`. Sources
read: a `--filter=blob:none` clone of google/adk-python at main commit
`ed76f94` (2026-10-21) with tags `v2.8.0`, `v2.12.0` and commit `c2ff634`;
the raw `CHANGELOG.md` or README of Arize-ai/openinference (google-adk
instrumentation), open-telemetry/opentelemetry-python-contrib
(`instrumentation-genai`), ag-ui-protocol/ag-ui (adk-middleware and the 1.0
spec changelog), a2aproject/A2A, google/adk-recipes (long-horizon-harness),
googleapis/mcp-toolbox, CopilotKit/with-adk, GoogleCloudPlatform/agent-starter-pack,
google/agents-cli, snyk/agent-scan, microsoft/PyRIT and
modelcontextprotocol/python-sdk (`docs/whats-new.md`); PyPI release metadata
for `mcp`, `ag-ui-adk`, `ag-ui-protocol`, `openinference-instrumentation-google-adk`,
`opentelemetry-instrumentation-google-genai`, `toolbox-adk`, `a2a-sdk` and
`google-adk`; and the Vertex model versions page
(https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/model-versions,
last updated 2026-10-21). No `last-tested` date changed.

## The rows

| # | Claim in the repository before today | True on 22 October 2026 (source) | Change | Files |
| --- | --- | --- | --- | --- |
| 1 | Eleven files cited `google/adk-samples` | Already corrected on 22 October by the Agents CLI 1.11.0 alignment; `grep adk-samples` over `skills/`, `README.md`, `docs/integrations/`, `evals/` returns nothing | None; row already done | — |
| 2 | Toolbox named only as "MCP Toolbox for Databases" with `toolbox-adk`; no repository name | `googleapis/genai-toolbox` is renamed `googleapis/mcp-toolbox` (README banner; latest tag v1.14.0); `toolbox-adk` 1.4.0 (PyPI 2026-09-01) lives in `googleapis/mcp-toolbox-sdk-python` | Repository and client location added where Toolbox is selected; source entry added. The SQL skill never names Toolbox, so its Toolbox branch belongs to the mcp-toolbox source in Phase C, not to this fix | interoperability `references/selection.md`, `references/sources.md` |
| 3 | Memo: with-adk archived, Azure/PyRIT moved, mcp-scan renamed, Agent Starter Pack in maintenance | All four confirmed (with-adk README: "consolidated into the CopilotKit monorepo", new location `examples/integrations/adk`; PyRIT README at microsoft/PyRIT; agent-scan README `uvx snyk-agent-scan`; ASP README "maintenance mode — switch to `agents-cli`"). No file in this repository cites with-adk, Azure/PyRIT, mcp-scan or Agent Starter Pack; PyRIT is named without a URL | PyRIT's current repository recorded in the security sources; nothing else to correct. The CopilotKit example, agent-scan and PyRIT content are Phase C sources | security `references/sources.md` |
| 4 | Security and auth compatibility stopped at 2.11.0; no 2.12.0 facts anywhere | 2.12.0 (2026-10-13) CHANGELOG: `after_tool_callback` screens tool output (fdda17c); workflow nodes take `require_confirmation` (988fd1a); a confirmed tool runs once per approval (bfdeb4a, #7434); OAuth2 secrets no longer leak over `/run`, `/run_sse`, `/run_live`, dev_server and session endpoints (63aed55); ADK user id only from an authenticated principal (d0c4060); mutating `/dev` and agent-builder endpoints loopback-only by default (97f9379), built-in agents only on loopback `adk web` (eca36ac); trigger delivery id exposed (74cd0ef, #7322); compaction skipped when summarisation errors (5c54055); AFC disabled in `LlmAsJudge` requests (cc339e0, #7146); tool sub-branch events kept out of the caller's LLM context (2e06fdc); auth credentials kept out of caller tool args (d8483a0, #7162); non-OAuth credential secrets redacted from the auth request event (82af2ef) | Version table rows and a 2.12.0 floor ("at least 2.12.0 when the agent serves several users over ADK's HTTP endpoints or holds delegated OAuth credentials") in security; a dated paragraph and the same floor in auth, with the output projection reframed as a second guard; one-run-per-approval, node confirmation and trigger redelivery in guardrails; node confirmation and the compaction facts in workflow and optimise; the judge AFC row in evaluation | security `SKILL.md`, `references/compatibility.md`, `references/sources.md`; auth `SKILL.md`, `references/compatibility-and-evidence.md`, `references/identity-and-output.md`; guardrails `references/human-review.md`, `references/compatibility.md`; workflow `references/orchestration.md`, `references/compatibility.md`; optimise `references/context-window.md`; evaluation `references/compatibility.md` |
| 5 | "`adk eval` exits 0 in 2.8.0 and on main" | Exits 0 at every tag through `v2.12.0` (`cli/cli_tools_click.py` at `v2.12.0` has no `total_failed` exit). Main commit `c2ff634` (2026-10-15, "fix: adk eval process exit code now reflects passed/failed", `git tag --contains` empty) ends with `sys.exit(1 if total_failed or not eval_run_summary else 0)`. No `--num_runs` on main | Version-conditional wording: 0 through 2.12.0, 1 on failures from `c2ff634`; "run one deliberately failing case on the pinned version and record the exit code"; pytest gate kept primary | release-engineering `SKILL.md`, `references/ci-eval-gates.md`, `references/compatibility.md`, `references/sources.md`, `assets/eval-gate.github-actions.yml`; `README.md` (skill description); `evals/scenarios.json` (`release-model-retirement-and-ci-gate` assertion) |
| 6 | `runtime.md` described `rerun_on_resume` only; nothing on failed-node rerun | 2.9.0 CHANGELOG (91573eb): "A node that failed now runs again when the workflow resumes, where before it replayed as though it had completed. Make node bodies idempotent". The memo's claim, from promptfoo's guide, that 2.9.2 deprecates `SequentialAgent` is in neither the CHANGELOG nor `sequential_agent.py`; not imported | Rule added to the workflow runtime reference (with the 2.8.0 baseline behaving the old way), cross-referenced from the graph section; safe-api-tool-calls now treats a node body that writes as a retry site carrying the idempotency key, in the reference and the entry skill | workflow `references/runtime.md`, `references/orchestration.md`, `references/compatibility.md`; safe-api `SKILL.md`, `references/writes-and-confirmation.md` |
| 7 | "Pin the instrumentor to a version tested with the pinned ADK"; open report that it suppresses `invoke_workflow` spans (#3844) | `openinference-instrumentation-google-adk` 1.0.0 (2026-09-29) "require google-adk >= 2.10" (breaking); 1.0.3 (2026-10-08) forwards ADK 2.x `invoke_workflow` and `invoke_node` spans (#3846), which closes the #3844 report; 1.0.4 (2026-10-09) current | Version gate written: below 1.0 for ADK 2.8.0 and 2.9.x, 1.0 or later from 2.10; #3844 marked closed | observability `SKILL.md`, `references/export-paths.md`, `references/compatibility.md`, `references/sources.md` |
| 8 | `opentelemetry-instrumentation-google-genai` cited without a home | opentelemetry-python-contrib `instrumentation-genai/README.md`: GenAI instrumentations "have been moved to the opentelemetry-python-genai repository ... copies ... only receive security patches and will be removed"; supports `google-genai >= 1.32.0`; PyPI 1.2b0 (2026-09-24) | New home cited beside the pin rule | observability `references/export-paths.md`, `references/compatibility.md`, `references/sources.md` |
| 9 | Baseline `ag-ui-adk==0.7.0`, `ag-ui-protocol==0.1.21` with no note on the current line | AG-UI 1.0 spec is normative (`RUN_FINISHED.outcome`, resume, subagents, reasoning events replace thinking, `protocolVersion` on `RUN_STARTED`); `ag-ui-adk` 0.8.0 (2026-10-07) requires `ag-ui-protocol>=1.0.0`; current is 0.11.0 (2026-10-21), not the memo's 0.10.0, and it carries a security fix for client-supplied `app:`/`user:` state (#2927) | "Upstream since the baseline" section added; the 0.7.0 baseline kept as the tested stack; the 0.11.0 fix stated as a rule to apply on any version. The two approval contracts belong to the ag-ui source in Phase C | frontend `references/compatibility.md` |
| 10 | Memo: seven files mention `GOOGLE_GENAI_USE_VERTEXAI` | agents-cli 1.9.0 (2026-10-06) moved new projects to `GOOGLE_GENAI_USE_ENTERPRISE=true`. Our mentions are all deliberate: the model-contracts skill records the deprecation and the `DeprecationWarning`; `audit_model_config.py` and its tests detect the deprecated name; the frontend runbook command unsets the deprecated name and sets the new one; one workflow SDK test fixture sets the old name to `false` | None. The SDK test fixture is outside the normal tier and would need a re-run to change, so it is left as is and noted here | — |
| 11 | "retires on Vertex 2026-10-20" (future tense); GEPA default unrecorded | Vertex model versions page (updated 2026-10-21): `gemini-2.5-pro`, `gemini-2.5-flash`, `gemini-2.5-flash-lite` retirement date October 20, 2026, replacements `gemini-3.8-flash` or `gemini-3.5-flash` (Pro) and `gemini-3.8-flash` or `gemini-3.5-flash-lite` (Flash). Main `eval_metrics.py` L113-114 still defaults `judge_model` to `gemini-2.5-flash`; `optimization/gepa_root_agent_prompt_optimizer.py` and `simple_prompt_optimizer.py` default `optimizer_model` to `gemini-2.5-flash`, `gepa_root_agent_optimizer.py` to `gemini-3.5-flash` | Tense corrected to "retired ... (date now past)"; the unpinned judge on the Vertex route described as already failing; GEPA `optimizer_model` pin rule added where the optimiser is introduced. The dated lifecycle asset (`model-lifecycle-2026-10-01.json`) is a snapshot and was not edited | release-engineering `SKILL.md`, `references/model-migration.md`, `references/compatibility.md`; evaluation `references/live-evaluations.md`, `references/compatibility.md`; instructions `references/prompt-as-code.md` |
| 12 | "main pins `mcp>=1.24,<3`"; `to_mcp_server` builds a `FastMCP` server | `pyproject.toml` at `v2.12.0` and main: `mcp>=1.24,<3` (2.8.0: `<2`). python-sdk `docs/whats-new.md`: v2 renames `FastMCP` to `MCPServer`, "the old import path is gone rather than deprecated", serves 2025-11-25 and 2026-07-28 from one app, advises `mcp>=1.28,<2` for unmigrated libraries; v2.3.0 (PyPI 2026-10-02) | Rename and import-path removal recorded; the rule that a ticket states both the `mcp` major version and the spec revision added to the entry skill and the compatibility table | interoperability `SKILL.md`, `references/compatibility.md`, `references/mcp-exposure.md`, `references/sources.md` |
| 13 | Only A2A 1.0.0 cited | A2A `CHANGELOG.md`: 1.0.1 (2026-05-26) prefers `application/a2a+json` in the HTTP binding (#1753); 1.0.0 (2026-03-12) removed implicit and password OAuth flows and added device code and PKCE (#1303), renamed `supportsAuthenticatedExtendedCard` and moved `extendedAgentCard` (#1222, #1307); a2a-sdk 1.2.3 (PyPI 2026-10-19) | Fact row added; the auth skill is named as owner of the flow the client implements rather than given a duplicate paragraph, because it never discusses A2A cards | interoperability `references/a2a-contracts.md`, `references/sources.md` |
| 14 | `context-window.md` labels long-horizon-harness "ADK 2.8.x" twice | Horizon README stack table: "Runner | ADK 2.5.x" | Both labels corrected with the source | optimise `references/context-window.md` |

## What stays the way this repository has it

The pytest gate remains primary (row 5); the memo's suggestion that the gate
"becomes redundant" from `c2ff634` is not adopted, because that commit still
offers no repetition and no pass threshold below 100%. Row 6's promptfoo
claim about `SequentialAgent` deprecation was not found and is not imported.
Temperature, identity, private-by-default and approval rules are untouched.

## Checks

`.venv/bin/python scripts/check_repo.py` and `git diff --check` were run
after the edits; the counts are recorded in the README entry for this date.
No helper script, test or `last-tested` date changed. Nothing was executed
against the pinned ADK: the exit-code statement for `adk eval` is read from
source at three points in history and is written to be confirmed by a
deliberately failing case on the installed version.
