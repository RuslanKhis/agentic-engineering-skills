# Compatibility and evidence provenance

This file is a dated baseline, not an instruction to install these versions.
Inspect the target's declared and installed versions first. Preserve its tooling.
An unsupported native ADK API requires a deliberate adaptation and callback
regression tests; do not substitute an unreviewed version change. A framework
upgrade is outside a narrow sensitive-data fix unless the user requests it.

## Exact environments

| Scope | Versions and limits |
| --- | --- |
| Companion declarations reopened 15 September 2026 | `google-adk[gcp]==2.8.0`, `google-cloud-dlp==3.38.0`, `google-cloud-modelarmor==0.7.1`; `pydantic>=2.12,<3`, `pytest>=9.0.3,<10`; google-genai is resolved transitively |
| Historical managed-service run, 14 September 2026 | ADK 2.8.0, DLP 3.38.0, Model Armor 0.7.1; resolved google-genai 2.23.0, Pydantic 2.13.5; Vertex ADC, `gemini-3.5-flash` at `global`; SDP/Armor `us-central1` |
| Skill creation environment, 15 September 2026 | macOS 26.6.2 arm64; Python 3.11.4; installed ADK 2.8.0, DLP 3.38.0, Model Armor 0.7.1, google-genai 2.19.0, Pydantic 2.13.4, FastAPI 0.136.3, pytest 8.4.2, PyYAML 6.0.3 |
| Bundled Python resources | Standard library only; require Python 3.11+ (`tomllib`, `asyncio.timeout_at`); actually exercised on Python 3.11.4 only |

The existing creation environment's pytest version is below the companion's
declared range. It was not repaired or represented as a clean chapter install;
new helper/controller tests use standard-library `unittest`. No dependency was
upgraded, downgraded or installed. Native SDK observations come from pinned
source and the historical companion tests, not a fresh provider integration of
this asset. See [skill-validation.md](skill-validation.md) for current outcomes.

Core instructions use open Markdown and the helper/asset use Python. The
optional `agents/openai.yaml` permits automatic invocation in Codex; removing it
does not remove the workflow. Behavioural smoke tests supplied the skill directly
to independent Codex agents in the recorded environment; installation and
automatic host discovery were not exercised. No Claude Code, Gemini CLI or other
host compatibility claim is made merely because the files parse.

## Evidence map

All companion paths below are provenance, **not runtime dependencies**. They
refer to `chapter-08-sensitive-data/` in the MIT-licensed companion repository
at revision `c909d7e5d285ae582abb3899bbe162fa55f075dd`, reopened for this task.
The September 14 run began at `59e789a53254c5fffcdd9a38bd13abeb31e454a7`;
its audit retains the exact source fingerprints. The following links are
optional further reading; this installed skill contains the required workflow.

| ID | Behaviour and source | Evidence / boundary of the claim |
| --- | --- | --- |
| E1 | `sensitive_support_agent/main.py`, `sessions.py`; `tests/test_security_invariants.py`, `test_adk_persistence_flow.py` | Historical offline canaries and actual ADK runner checks support input protection before history/model, owned sessions and bounded release; selected gateway paths also exercised live |
| E2 | `sensitive_data.py`, `infrastructure/provision_dlp.py`; `tests/test_sensitive_data.py` | Historical live SDP plus offline adapter tests support configured deny/PII policies, error summaries and bounded calls; no general detector-accuracy guarantee |
| E3 | `audit/manuscript-20260915/offline-contract-probe.json`, `CHAPTER_08_UPDATED.md` | Offline probe exposed empty/truncated inspection acceptance and weak public result constraints/reference matching. Stronger rules in this skill are production hardening; the new SDP controller has fresh offline tests. Original application remains unchanged |
| E4 | `sensitive_tool_output_plugin.py`, `composition.py`; `tests/test_gateway_adk_flow.py`, `test_tool_policy_plugin.py` | Historical actual-runner tests prove pre-persistence argument mutation, second execution check and preservation of later callbacks. New integrations must rerun these invariants |
| E5 | `model_armor.py`, `event_projector.py`, `release_gate.py`; `tests/test_model_armor.py`, `test_security_invariants.py` | Historical direct/native and gateway evidence supports guarded final release and verdict mapping. Required-filter validation even on aggregate no-match is additional hardening |
| E6 | Installed ADK 2.8.0 `integrations/model_armor/_plugin.py`; composition and gateway tests | Native latest-user/model-text screening, block-only matches and structured-payload exclusions; not a complete persistence/tool boundary |
| E7 | `agent.py`, `composition.py`; `tests/test_model_client_lifecycle.py` | Historical offline test: five runner calls reuse one model SDK client, cross-user isolation retained, shutdown handles unused/failed closes. Historical post-fix timings are measured separately |
| E8 | `infrastructure/lifecycle.py`, `runtime_identity.py`, cleanup scripts; `tests/test_lifecycle_cli.py` and runtime identity tests; dated audits | Historical repeated setup/delete and scoped IAM checks; offline ownership/partial-failure tests. API activation was not freshly exercised in the final live retest |
| E9 | `tools.py`, `order_store.py`, `tests/test_tools.py` | Historical ownership/contact checks and synthetic side-effect minimisation. Real email, production tokenisation, durable idempotency and real identity provider absent |
| E10 | Updated manuscript's production extensions | Durable/distributed state, effective residency, full telemetry audit, added secret classes, RAG/media paths and operational policy are guidance, not supplied implementations |

Optional source links: [pinned companion chapter](https://github.com/RuslanKhis/agentic-engineering-adk-gcp/tree/c909d7e5d285ae582abb3899bbe162fa55f075dd/chapter-08-sensitive-data),
[dated live audit](https://github.com/RuslanKhis/agentic-engineering-adk-gcp/blob/c909d7e5d285ae582abb3899bbe162fa55f075dd/chapter-08-sensitive-data/audit/INDEPENDENT_AUDIT_2026-09-14.md),
[manuscript comparison](https://github.com/RuslanKhis/agentic-engineering-adk-gcp/blob/c909d7e5d285ae582abb3899bbe162fa55f075dd/chapter-08-sensitive-data/audit/MANUSCRIPT_REVIEW_2026-09-15.md).
Local source/evidence was inspected; public availability of every revision-linked
page was not separately established.

## Historical results are scoped

The September 14 campaign passed 20/20 live gateway cases: 27 Gemini requests
returned HTTP 200, with 59 DLP and 92 Armor calls and no 429 or paid retries.
It used synthetic development identities through a local HTTP/SSE gateway with
managed providers. It also recorded 186 in-scope offline tests passing and
owned-resource cleanup. The local-protection-fakes plus real-Gemini combination
was not separately run live. The previous 429's cause was not proven, and an
AI Studio payment was not established as the cause of later Vertex success.

Five-sample warm medians were 3.399 seconds for simple answers and 6.152 seconds
for owned-order answers. The five-second target failed overall. Those small
samples do not establish production capacity or latency. Hosted deployment,
production identity, durable history, comprehensive security certification and
today's fresh cloud access were outside that evidence.

## Licence and authorship

The workflow and adapted controller lessons derive from Chapter 8 of *Agentic
Engineering* and its companion code. The skill is complete without the book.
No published book URL was available, so none is invented. Preserve the bundled
[MIT licence](../LICENSE), copyright © 2026 RuslanKhis, with substantial copied
material. This is an independent community project, not affiliated with or
endorsed by Google.
