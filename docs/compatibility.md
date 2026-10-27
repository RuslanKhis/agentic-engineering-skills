# Compatibility matrix

Maintainer view of what each skill was actually verified against. The source of
truth is each skill's `metadata.verified-against` and its compatibility
reference; this page collects them so a re-baseline can be planned in one
place. Compiled 2026-10-27 from those files. Nothing here was re-run.

"Tested" means the skill's recipes or helpers ran against that version.
"Read" means source or CHANGELOG was read and nothing ran. Agents CLI
scaffolding `google-adk>=2.12.0` is a recommendation to new projects, not a
test of these skills.

## Skills that run ADK code

| Skill | ADK tested | Other ADK versions (how) | Key SDK pins tested alongside | Date of test | Evidence |
| --- | --- | --- | --- | --- | --- |
| adk-agent-evaluation | 2.8.0 | 2.12.0 offline spikes (Inspect AI bridge, MLflow scorer); 2.12.0 signatures read | Python 3.11.4, google-genai 2.23.0, aiplatform 2.1.0, pytest 9.1.1 | 2026-09-13; spikes 2026-10-22, 2026-10-25 | `references/compatibility.md`, `provider-compatibility.md` |
| adk-agent-instructions | none (source read only) | 2.8.0 source; 2.9 to 2.11 CHANGELOG | none | read 2026-10-06 | `references/compatibility.md` |
| adk-agent-interoperability | none at 2.8.0 (source read) | 2.12.0 tested offline: MCP conformance (44 checks), Inspector CLI | mcp 2.3.0, a2a-sdk 1.2.3 (2.12.0 trials) | read 2026-10-08; trials 2026-10-22 to 10-24 | `references/compatibility.md`, `validation.md` |
| adk-agent-observability | none (source read only) | 2.8.0 source; 2.6 to 2.11 CHANGELOG; 2.12.0 `tracing.py` read | none | read 2026-10-07; 2026-10-25 | `references/compatibility.md` |
| adk-agent-security | none (source read only) | 2.8.0 source; main at 2.11.0; 2.12.0 CHANGELOG and executor source read | none | read 2026-10-07; 2026-10-22 | `references/compatibility.md` |
| adk-fastapi-backend | **2.12.0** | none | Python 3.12.9, fastapi 0.141.1, starlette 1.9.0, pydantic 2.14.1, sqlalchemy 2.1.6, alembic 1.20.1, firebase-admin 7.7.0, google-auth 2.62.0, httpx 0.28.1 | 2026-10-23 | `references/compatibility.md` |
| adk-frontend-integration | 2.8.0 | 2.12.0 Python gateway tested offline; assistant-ui adapter read | Python 3.11.4, google-genai 2.19.0, ag-ui-adk 0.7.0, ag-ui-protocol 0.1.21, aiplatform[agent-engines] 1.153.1, fastapi 0.141.1, pydantic 2.13.5, CopilotKit 1.69.0 | 2026-09-16; gateway 2026-10-26 | `references/compatibility.md` |
| adk-memory-architecture | 2.8.0 | 2.12.0 installed source read (Memory Bank, `PreloadMemoryTool`, session schema) | Python 3.11.4, google-genai 2.19.0, aiplatform 1.153.1, pydantic 2.13.5, fastapi 0.141.1 | 2026-09-15/16; read 2026-10-23 | `references/compatibility.md` |
| adk-model-and-output-contracts | none (source read only) | 2.8.0 source; to 2.11 CHANGELOG; 2.12.0 `lite_llm.py` read | none | read 2026-10-06 | `references/compatibility.md` |
| adk-operational-guardrails | 2.8.0 | 2.12.0 CHANGELOG and source read (`function_tool.py`, `_finalizer.py`) | Python 3.11.4, google-genai 2.23.0 (companion) and 2.19.0 (skill tests), pubsub 2.39.0 | 2026-09-13; skill tests 2026-09-16 | `references/compatibility.md` |
| adk-release-engineering | none (source read only) | 2.8.0 source; `adk eval` read at v2.8.0 and v2.12.0; conformance gate observed against a 2.12.0 server | none | read 2026-10-07; 2026-10-22 | `references/compatibility.md`, `ci-eval-gates.md` |
| adk-sql-agent-engineering | 2.8.0 | 2.12.0 offline scripted-model trial ("worked unchanged") | Python 3.11.4, google-genai 2.23.0, bigquery 3.45.0, pydantic 2.13.5, sqlglot 29.0.1, fastapi 0.141.1 | 2026-09-13/16; trial 2026-10-25 | `references/compatibility.md`, `adk-runtime.md` |
| adk-tool-auth-and-secrets | 2.8.0 (67 offline tests, 6 live workflows) | 2.12.0 CHANGELOG and `auth`/`a2a` source read | Python 3.11, google-genai 2.23.0, secret-manager 2.30.0, google-auth 2.58.0, firebase-admin 7.5.0, grpcio 1.83.1 | 2026-09-13/16; read 2026-10-24 | `references/compatibility-and-evidence.md` |
| adk-tool-interface-design | none (source read only) | 2.8.0 source; 2.11 CHANGELOG; 2.12.0 signatures from the evaluation skill | none | read 2026-10-06 | `references/compatibility.md` |
| adk-workflow-design | 2.8.0 | 2.12.0 CHANGELOG; Restate plugin probed offline with stand-ins on 2.12.0 and 2.13.0 | Python 3.11.4, google-genai 2.23.0, httpx 0.28.1 | 2026-09-15/16; 2026-10-22, 10-25 | `references/compatibility.md`, `runtime.md` |
| deploy-adk-on-google-cloud | 2.8.0 (Agent Runtime `[a2a]==2.8.0`) | 2.12.0 `api_server.py` and the Agents CLI scaffold read | Python 3.11.4 / 3.12.9, aiplatform[agent_engines] 1.153.1, google-genai 2.23.0, fastapi 0.141.1, pydantic 2.13.5 | 2026-09-13/14 | `references/compatibility.md` |
| optimise-adk-on-google-cloud | 2.8.0 (Parts 1 to 3) | v2.8.0 tag and main at 2.11 source; 2.12.0 source and CHANGELOG read | Python 3.11.4, google-genai 2.19.0/2.23.0, aiplatform 1.153.1, OpenTelemetry 1.41.1/1.42.1, fastapi 0.136.3/0.141.1 | September 2026; read 2026-10-25 | `references/compatibility.md`, `context-window.md` |
| protect-adk-sensitive-data | 2.8.0 (`[gcp]`) | 2.12.0 `_config.py` and `runners.py` read; nothing executed | Python 3.11.4, dlp 3.38.0, modelarmor 0.7.1, google-genai 2.23.0/2.19.0, pydantic 2.13.5 | 2026-09-14/15; read 2026-10-22, 10-24 | `references/compatibility.md` |
| safe-api-tool-calls | 2.8.0 | 2.12.0 CHANGELOG read | Python 3.11.14 (recheck 3.11.4), httpx 0.28.1, tenacity 9.1.4, google-genai 2.23.0 | 2026-09-13 | `references/compatibility.md` |

The shared tool-confirmation block was reconciled on 2026-10-27 against the
google-adk 2.8.0 and 2.12.0 wheels (source read, not run).

## Skills that run no ADK code

adk-engineer (router), adk-system-designer, adk-discovery, adk-presenter,
adk-governance-pack, adk-portability-planning (reads google-adk 2.13.0 source
and `pyproject.toml` for its framework comparison) and practice-profile carry
`verified-against: "not applicable: …"`.

## Version floors that matter

| Floor | Why | Recorded in |
| --- | --- | --- |
| 2.7.0 minimum | `adk web` remote code execution and path traversal CVE ranges fixed; stdio MCP blocked in YAML configs; agent-card RPC-target constraint | adk-agent-security `references/compatibility.md`; adk-agent-interoperability `references/compatibility.md` |
| 2.10.0 minimum | Server-supplied MCP tool descriptions fenced; confirmation held in the framework (only on a hook answering exactly `True`); agent authorship required before resume dispatch | adk-agent-security `references/compatibility.md` |
| 2.11.0 preferred | `ToolCallIntegrityPlugin` HMAC stamps for writable session stores | adk-agent-security `references/compatibility.md` |
| 2.12.0 minimum for multi-user HTTP serving or delegated OAuth | OAuth2 secrets no longer leak over `/run`, `/run_sse`, `/run_live`, the dev server and session endpoints; `/dev` endpoints loopback-only; a confirmed tool runs once per approval; `after_tool_callback` can filter tool output; credentials kept out of tool args. The "user id only from an authenticated principal" fix covers the A2A request converter only: the HTTP routes still take `user_id` from the request | adk-agent-security `references/compatibility.md`; adk-tool-auth-and-secrets `references/compatibility-and-evidence.md`; `shared/verified-principal.md` |

## What re-baselining to 2.12.0 would require

Do not change a `verified-against` value until the run behind it exists. Per
the skills' own notes:

1. Live and companion campaigns: every one ran on 2.8.0. Re-run the interface
   and contract tests per skill (memory `compatibility.md` asks for these on
   any other 2.x), and reassess the workflow skill's callback-chain quirk and
   retained-state assertions.
2. Runner signatures: `InMemoryRunner(plugins=)` warns on 2.12.0 (register
   plugins on an `App`, pass `app=`); scripted-model failures arrive wrapped
   as `DynamicNodeFailError`; `ToolContext` is an alias of `Context`
   (evaluation `deterministic-tests.md`).
3. Moved imports: `EventsCompactionConfig` from `google.adk.apps.app`; the
   `instructions.py` and `contents.py` flow modules are shims (optimise
   `context-window.md`); `_fencing.py` moved to `context/` (security).
4. Deprecations: `SequentialAgent` in favour of `Workflow` (security
   `injection-patterns.md`).
5. Dependency conflicts: 2.12.0 caps `opentelemetry-api` at 1.42.1, which
   holds FastAPI at 0.141.1 or below; `aiplatform[adk]` 1.153.1 needs ADK
   below 2.0; ag-ui-adk 0.11 needs ag-ui-protocol 1.0 or later; the A2UI
   `[a2a]` extra pins a2a-sdk 0.3; google-genai resolves to 2.32 or 2.33,
   which changes environment-variable backend selection; Agents CLI needs
   `aiplatform>=2.2`.
6. Behaviour to retest: the evaluation judge no longer runs automatic function
   calling; `adk eval` still exits 0 on failure; a plugin
   `before_model_callback` short-circuit skips `max_llm_calls` counting; the
   `call_llm` span duplicates usage attributes and the trace shape changed at
   2.10; the Runner rejects a message mixing function responses and text;
   Model Armor screens tool output; the 2.10.0 template escapes.
7. Metadata and gates: update `verified-against` only for skills actually
   re-run; the `--expect-adk 2.8.0`, `--require-baseline` and
   `--require-tested-stack` inspector options need new baselines (sql,
   frontend). adk-operational-guardrails' `last-tested: 2026-10-22` has no
   recorded test on that date (only an adk-recipes review).
