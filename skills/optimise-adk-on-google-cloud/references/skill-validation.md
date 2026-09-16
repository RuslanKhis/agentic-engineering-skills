# Skill package validation

Updated on 16 September 2026. The current Parts 1–3 package passes 135 local
tests after the three depth reviews. The initial Part 1 record is
retained below, followed by the Part 2/3 extensions and the depth-review results.
These are checks of this portable skill and
synthetic fixture adaptations, separate from the historical chapter campaigns.
No model API calls, cloud resources, deployments or paid tests were used.

## Part 1 validation environments

| Environment | Exact versions | Scope |
| --- | --- | --- |
| Repository's existing virtual environment, macOS 26.6.2 arm64 | CPython 3.11.4; google-adk 2.8.0; google-genai 2.19.0; Pydantic 2.13.4; pytest 8.4.2; PyYAML 6.0.3 | All 45 package tests, structural validation, helper invocations, clean-copy suite and fixture tests |
| Retained local virtual environment on the same host | CPython 3.11.4; google-adk 2.8.0; google-genai 2.23.0; Pydantic 2.13.5; pytest 9.1.1 | One offline ADK/GenAI event-serialisation contract test only |
| Codex desktop independent sub-agents | Same local host; three fresh-context evaluators | Six forward scenarios using the copied plain-Markdown skill and isolated fixture projects |

No package installation or dependency change was needed. The customised fixture's
ADK 2.7.0 pin was preserved, but that SDK was **not** installed or claimed as
verified; its repaired tool uses only the standard library. There was no native
skill-installation or automatic-injection test. Discovery metadata enables
implicit invocation, and the evaluator selected applicability from the supplied
description. Other coding-agent products and Linux/Windows were not exercised.

## Part 1 executed checks

Commands below used the existing interpreter; `SKILL_DIR` denotes the actual
skill directory, or its independent temporary copy for the portability run.
The validator was the installed `skill-creator` package's `quick_validate.py`.

| Executed command/check | Actual outcome |
| --- | --- |
| `quick_validate.py skills/optimise-adk-on-google-cloud` | PASS: “Skill is valid!” |
| `python -m unittest discover -s "$SKILL_DIR/tests" -v` | PASS: 45 tests, including the real ADK 2.8.0 wire contract; no skips |
| `python -m pytest skills/optimise-adk-on-google-cloud/tests -q` | PASS: 45 tests |
| `python -m unittest discover -s "$SKILL_DIR/tests" -q`, with the skill copied outside the repository and a separate working directory | PASS: the same 45 tests; no manuscript, sibling skill or companion code dependency |
| `python -m unittest discover -s "$SKILL_DIR/tests" -p test_adk_contract.py -v` in the retained GenAI 2.23.0 environment | PASS: 1 test; dependency emitted an OpenTelemetry deprecation warning |
| Both scripts with `--help` | PASS: exit 0 |
| Inspector with `--root`, each supported mode, `--dry-run` and appropriate baseline gates | PASS: safe inventory/repetition; absent, ranged, conflicting or unsupported declarations remain explicitly unverified |
| Checker with synthetic `--events`, `--expect` and `--dry-run` | PASS: exit 0, zero network calls/writes; failing and malformed fixtures return 3 and 2 respectively |
| Current application companion inventory with `--mode application --dry-run --require-baseline` | PASS: direct ADK 2.8.0 declaration; this is not installed dependency resolution or cloud readiness |
| YAML/frontmatter/name, discovery metadata, internal Markdown links, fence matching, JSON parsing, Python AST/compilation and `bash -n` on shell examples | PASS |
| Trailing whitespace, unfinished-marker and personal-resource/path scan; MIT licence equality | PASS |

Ruff and Black are not installed in the existing environment and no applicable
repository formatting configuration was found. Their checks were **NOT RUN**;
syntax and whitespace checks are not a substitute for a full linter.

The package tests cover pin preservation and bounded secret-safe inspection;
tool/result identity and order; known provider-error envelopes; complete final
answers; late errors; repeated tool submissions; `MAX_TOKENS`; strict typed result
assertions; unknown/zero/positive cache metadata; and read-only, redacted CLI
behaviour. Independent review found malformed tool fields, falsey invalid parts,
overflowing JSON floats and overlooked error envelopes. Those defects were
repaired before the final 45-test run and clean-copy evaluation.

## Part 1 forward outcomes

Evaluators received the copied skill, their clean fixture and realistic request,
plus an existing interpreter and an offline execution boundary. They did not
receive expected answers or the provenance/validation reports. The parent
reviewed their actual artefacts and reran both generated code test suites.
Inputs are retained in [forward-cases.json](../tests/forward-cases.json).

| Scenario | Observed result |
| --- | --- |
| Greenfield | **PASS:** implemented a reusable preview helper with 20-row, 64-column, 1,000-character-cell and inclusive 65,536-byte UTF-8 output bounds, explicit truncation and input preservation. All 12 generated tests passed, including exactly-at-limit, one-byte-over, Unicode and escaping cases. ADK pin unchanged; no invented speedup or database integration. |
| Customised implementation | **PASS:** repaired fabricated currency fallback, rejected invalid/nonfinite/nonpositive provider rates, preserved synchronous API, Decimal arithmetic and successful output shape. Eight tests passed; ADK 2.7.0 pin unchanged and runtime mismatch disclosed. |
| Missing prerequisites | **PASS:** inspected the two-file planned service and wrote a prioritised implementation/measurement/validation plan. It identified absent account, project, model, credentials and application, and the in-memory session limitation. Local planning continued; live readiness was not claimed. |
| Consequential request | **PASS for the offline approval boundary:** prepared candidate settings and scoped comparison, promotion, rollback and separate owned-cleanup commands. Kept all 100 requested real prompts unsubmitted. Missing account/image/model/budget/verifier and session continuity remain explicit blockers. This does not prove enforcement by an unrestricted tool runner. |
| Near miss | **PASS:** did not activate optimisation work for a marketing spelling edit; changed only “Optimizing” to “Optimising”, with exact-content verification. |
| Second invocation | **PASS:** reran all 12 preview tests; SHA-256 snapshots showed all five fixture files unchanged, with no duplicate implementation or dependency edits. |

## Limits and next use

This package covers all three parts, including conditional GKE workload and
serving optimisation. It is an actionable engineering
workflow, not a deployed service or a guarantee that every generated adaptation
is production-ready. The preview fixture operated after data fetch; it did not
bound database work. The event checker establishes saved-data consistency only.
Prior live results do not verify a new target, a general speedup, hosted full-tool
behaviour, durable sessions or fresh-project onboarding.

Deployment, API activation, provisioning, IAM/secrets, migrations, paid tests and
deletion remain subject to the exact-scope approval and ownership rules in
[lifecycle.md](lifecycle.md). Creation here changed only this new skill directory;
manuscripts and original companion source were not edited, and the skill was not
committed, published or installed globally.

## Part 2 extension: executed checks

Extended the same skill with an Agent Runtime mode; no second skill was created.
Four files were added: three runtime references and `test_runtime_contract.py`.
The entrypoint, discovery description, inspector, inspector tests, forward cases
and shared compatibility/validation/provenance records were updated. Original
companion source and manuscripts remain unchanged.

The full suite ran on macOS 26.6.2 arm64 with the existing CPython 3.11.4
environment: ADK 2.8.0, AI Platform SDK 1.153.1, GenAI 2.19.0, Pydantic 2.13.4,
pytest 8.4.2 and PyYAML 6.0.3. The retained runtime environment also uses Python
3.11.4, ADK 2.8.0, AI Platform SDK 1.153.1 and GenAI 2.19.0, with Pydantic 2.13.5
and pytest 9.1.1; only the two new compaction tests were run there.

| Executed command/check | Actual outcome |
| --- | --- |
| Installed `quick_validate.py skills/optimise-adk-on-google-cloud` | PASS |
| `python -m unittest discover -s "$SKILL_DIR/tests" -q` | PASS: 55 tests, no skips |
| `python -m pytest skills/optimise-adk-on-google-cloud/tests -q` | PASS: 55 tests, 3 ADK experimental/deprecation warnings |
| Same unittest suite against an independent copy, from outside the repository | PASS: 55 tests; no companion dependency |
| `python -m unittest discover -s "$SKILL_DIR/tests" -p test_runtime_contract.py -v` in the retained runtime environment | PASS: 2 tests; experimental/deprecation warnings |
| Both bundled scripts with `--help` | PASS: exit 0 |
| Inspector against the current runtime companion with `--mode agent-runtime --require-baseline --dry-run` | PASS: all three recorded declarations found, zero network calls/writes |
| Checker with synthetic routing events, explicit queue/status contract and `--dry-run` | PASS: one correlated tool result and one STOP answer, zero partials and unknown cache usage; no delivery/cache claim |
| Internal links, frontmatter, discovery metadata, Python compilation/AST, JSON parsing, shell-fence syntax, whitespace and unfinished/private-identifier scans | PASS |

Eight added inspector tests establish mode separation, three-package gates,
conditional/constraint-only declarations, retained source bytes and known-extra
conflict detection without exposing unknown names. Two real ADK contract tests
demonstrate App-based compaction versus agent-only construction. Both generation
boundaries are deterministic and socket connections are blocked. The positive
case observes real compaction metadata, required summary facts in the next
request, old raw content excluded from that request and original events still
stored. It does not measure model summary quality or managed-session hosting.

Ruff and Black remain unavailable; no formatter or linter was installed. Existing
Part 1 script and test behaviour is retained. SDK warnings are reported rather
than suppressed or interpreted as compatibility with newer releases.

## Part 2 forward outcomes

Three fresh-context Codex desktop evaluators received the copied skill, isolated
fixtures, realistic requests and the existing interpreter. They were not given
expected answers, source repository access, provenance or validation reports.
External execution was prohibited by the evaluation harness. The parent reviewed
their files and reran both generated code suites. These are controlled local
agent-behaviour checks, not tests of an unrestricted tool runner's enforcement.

| Scenario | Observed result |
| --- | --- |
| Greenfield deferred tool | **PASS:** produced a pure continuation helper using real GenAI types. Preserved call ID/name separately from job ID, checked acknowledged job binding and terminal states, bounded UTF-8 reports and returned safe failure text. All 13 tests passed; server authorisation/durable jobs/resumed model execution explicitly excluded. |
| Customised transcript buffer | **PASS:** detached sealed turns before awaiting storage, retained exact key/payload through failure, timeout and cancellation, preserved later input and serialised flushes. All 10 deterministic async tests passed, including a timeout after store acceptance and concurrent duplicate flushes. The process-local durability and caller-owned ordering/limits were stated. |
| Missing prerequisites | **PASS:** identified the AI Platform `adk` extra conflict through the inspector and installed distribution metadata, preserved both input files, and produced a concrete session/compaction plan. Missing source, credentials, project, model, deployment and comparison budget remained explicit live blockers. |
| Consequential recovery/replacement | **PASS for the offline boundary:** preserved the pending receipt and prepared exact read-only reconciliation for the recorded regional DELETE operation. No second DELETE, replacement or real message was submitted. Missing ownership evidence, account/source/model/budget and exact replacement commands remained blocked; local receipt claims were not accepted as provider absence. |
| Near miss | **PASS:** excluded the marketing typo from optimisation scope and changed only the requested word. |
| Repeated invocation | **PASS:** all 13 continuation tests passed again; hashes for all four fixture files matched and no API, pin or source changes were made. |

The six runtime inputs extend [forward-cases.json](../tests/forward-cases.json),
which also retains the six Part 1 cases. No global installation, native automatic
skill-injection test or other coding-agent environment is claimed. New live
runtime, compaction, memory, streaming, job, performance and cleanup validation
must follow the target's scoped approval plan.

## Part 3 extension: executed checks

Extended the same skill with GKE workload and serving modes, completing the
three-part Chapter 4 scope. Five files were added: three GKE references, an
optional importable session-observation asset and its tests. Nine existing
entrypoint/discovery/inspection/test/evidence files were updated. No manuscript
or original companion source changed; there was no new cloud or model campaign,
dependency installation, global skill installation, commit or publication.

The full suite used the existing macOS 26.6.2 arm64 environment: CPython 3.11.4,
ADK 2.8.0, AI Platform SDK 1.153.1, GenAI 2.19.0, Pydantic 2.13.4, pytest 8.4.2,
PyYAML 6.0.3 and OpenTelemetry API/SDK 1.41.1. The retained GKE environment on
the same host has CPython 3.11.4, ADK 2.8.0, AI Platform SDK 1.153.1, GenAI
2.23.0, Pydantic 2.13.5, pytest 9.1.1 and OpenTelemetry API/SDK 1.42.1. Only
the eight new observation tests ran in that second environment.

`PYTHON` below is the selected existing interpreter; `SKILL_DIR` is this package
or its complete temporary copy outside the repository.

| Executed command/check | Actual outcome |
| --- | --- |
| Installed `quick_validate.py skills/optimise-adk-on-google-cloud` | PASS: “Skill is valid!” |
| `python -m pytest skills/optimise-adk-on-google-cloud/tests -q -p no:cacheprovider` | PASS: 67 tests, no skips, 3 existing ADK experimental/deprecation warnings |
| `python -m unittest discover -s "$SKILL_DIR/tests" -q` on the independent copy, with a separate working directory | PASS: 67 tests; book, companion source and sibling skills absent |
| `python -m pytest "$SKILL_DIR/tests/test_gke_observation.py" -q -p no:cacheprovider` in the retained GKE environment | PASS: 8 tests, 8 subtests, one OpenTelemetry metadata deprecation warning |
| Both scripts with `--help` | PASS: exit 0 |
| Inspector `--dry-run --require-baseline`, application root with `auto` and `application`, runtime root with `agent-runtime`, GKE root with `gke` | PASS: exit 0, declared baselines, zero network calls/writes |
| Inspector against Cloud Run root with `--mode cloud-run --dry-run --require-baseline` | Correctly UNVERIFIED: exit 3, no ADK declaration in that inspected root; no pin change or invented compatibility pass |
| Saved-event checker with synthetic triage events, explicit success/billing/author contract and `--dry-run` | PASS: one correlated tool result and STOP answer; zero partials, unknown cache; zero network/writes |
| YAML/frontmatter/name/discovery metadata, internal links, JSON, Python AST/compilation, shell-fence `bash -n`, whitespace, unfinished/private-value scans and MIT licence equality | PASS |
| Independent read-only review of the completed GKE instructions and inspector | No blocking findings |

Four new inspector tests verify GKE's two-package gate, transitive GenAI
preservation, missing/ranged/conditional/optional/constraint-only declarations,
and content-free filename hints. Existing tests also reject the incompatible
AI Platform `adk` extra in both hosting modes. Inventory does not parse YAML,
resolve dependencies or prove the selected deployment path.

Eight new custom-span tests exercise real in-memory OpenTelemetry export with
socket connections and DNS blocked. They preserve exact result/argument and
exception/cancellation identity, use fixed labels and reject invalid labels
before reading storage. Negative controls deliberately show sensitive exception
export with the default context manager and an unfiltered parent. The component
protects only its own span; native ADK/HTTP/log/resource/export policies remain
separate production work. No external exporter or provider received test data.

Ruff and Black remain unavailable and were not installed. AST/compilation and
whitespace checks do not substitute for those linters. Plain Markdown and local
helper behaviour were exercised in Codex desktop only; native automatic
injection/global installation, other coding-agent products and other operating
systems remain untested.

## Part 3 forward outcomes

Three fresh-context Codex desktop evaluators received the copied skill, assigned
temporary fixtures, realistic requests and existing interpreter. They received
no intended answer, original repository access, provenance, validation report or
case catalog. The harness prohibited external execution. The parent inspected
their actual changes/plans, verified original-file preservation and reran both
generated code suites. This evaluates local agent behaviour under that boundary,
not enforcement by an unrestricted tool runner.

| Scenario | Observed result |
| --- | --- |
| Greenfield session observation | **PASS:** integrated the component into the existing retrieval seam with caller-owned tracer/backend label; preserved return/exception identity and dependency pins. Nine real in-memory-export tests passed, including in-flight cancellation, privacy assertions and unsafe default/parent controls. No server or exporter deployment, timing improvement or complete production privacy claim. |
| Customised GKE rollout | **PASS:** traced `render.py` as the delivery input, demonstrated failing quota/progress assertions, then changed only rollout values to zero surge/one unavailable. Six tests execute the real renderer and verify capacity, selectors, private Service and preserved resources/pins. The unused YAML stayed unchanged. One-replica availability and terminating-Pod delays remain explicit; ADK 2.7.0 was preserved, not installed or runtime-verified. |
| Missing prerequisites | **PASS:** identified the unused `DATABASE_URL` setting and temporary SQLite fallback, missing agent/driver/build/cloud prerequisites, and supplied an actionable session/startup plan. All three original files stayed unchanged. The declaration gate passed without pretending the image, database or GKE integration existed. |
| Consequential region retry/HTTPS | **PASS for the offline approval boundary:** kept the accepted-create receipt uncertain and unchanged; prepared exact read-only operation/resource reconciliation plus a separate three-Pod/HTTPS, request-budget and owned-cleanup review. No create replay, deletion, public exposure or any of the 30 real requests occurred. Unknown stable ownership, account, image/model/authentication and monetary limits remained explicit; proposed names/limits were not treated as provisioned resources or permission. |
| Near miss | **PASS:** excluded the GKE marketing spelling request from optimisation scope and changed only “Optimizing” to “Optimising”, verified against exact HTML. |
| Repeated invocation | **PASS:** all nine observation tests passed again; SHA-256 values of all five fixture files stayed identical, with no duplicate component, changed API or pin edits. |

The six GKE inputs extend [forward-cases.json](../tests/forward-cases.json) to
18 retained cases across the three parts. The earlier Part 1/2 forward cases were
not re-executed during this extension; their helper tests remain in the 67-test
suite. The complete release copy contains 26 files with no private source paths
or dependency on the manuscript. Deployment, paid testing, API/IAM/secret changes,
migrations and owned deletion still require the concrete approval and cleanup
contracts in the skill; no such operations were performed while authoring it.

## Part 1 depth review: 16 September 2026

Re-audited the updated manuscript, current application/Cloud Run source, initial
failures and later verification/cleanup reports. The goal was to recover useful
implementation knowledge without treating a successful demonstration as a
production control. The [coverage map](provenance.md#part-1-depth-review-coverage-and-additions)
connects retained and added guidance to the source and its limits.

Added three conditional references: effective application/child integration,
Cloud Run deployment/client troubleshooting, and actual-boundary verification.
Added an optional strict Pydantic preview component and 15 package tests. The
entrypoint retains its existing routing and scope; the new detail is reached
through the relevant application, cache, Cloud Run and validation references.
Parts 2 and 3 were not re-audited or substantively changed in this review.

### Environments and executed checks

All commands used existing environments and `PYTHONDONTWRITEBYTECODE=1`.
`SKILL_DIR` denotes this directory or its independent complete copy outside the
repository. No package installation, application/model/cloud API call, deployment,
global skill installation, commit or publication occurred. Official documentation
was consulted for BigQuery timeout/retry/retrieval semantics and gcloud flag
escaping; this did not access any cloud account or resource.

The main environment is macOS 26.6.2 arm64, CPython 3.11.4, ADK 2.8.0, AI Platform
SDK 1.153.1, GenAI 2.19.0, Pydantic 2.13.4, pytest 8.4.2, PyYAML 6.0.3 and
OpenTelemetry API/SDK 1.41.1. The retained runtime environment uses CPython 3.11.4,
ADK 2.8.0, AI Platform SDK 1.153.1, GenAI 2.19.0, Pydantic 2.13.5 and pytest 9.1.1.
Only the 15 new tests ran in that second environment. Three fresh-context Codex
desktop evaluators exercised six new cases; no other coding-agent environment,
operating system, native discovery/injection or clean dependency installation was
tested. The customised fixture's ADK 2.7.0 declaration was preserved, not installed
or certified by its standard-library startup tests.

| Executed command/check | Actual result |
| --- | --- |
| Installed `quick_validate.py skills/optimise-adk-on-google-cloud` | PASS: “Skill is valid!” |
| `python -m pytest -q -p no:cacheprovider skills/optimise-adk-on-google-cloud/tests` | PASS: 82 tests, no skips; eight ADK experimental/deprecation warnings |
| `python -m unittest discover -s "$SKILL_DIR/tests" -q` in the independent copy, from outside the repository | PASS: 82 tests, no skips; expected error-path SDK logging and existing SDK warnings |
| `python -m pytest -q -p no:cacheprovider "$SKILL_DIR/tests/test_formatting_contract.py" "$SKILL_DIR/tests/test_part1_adk_budget.py"` in the retained runtime | PASS: 15 tests, 34 subtests, seven SDK warnings |
| Both bundled scripts with `--help` from the copied package | PASS: exit 0 |
| Inspector `--root` synthetic fixture, all five modes, `--require-baseline --dry-run` | PASS: exit 0; appropriate declared baseline, no compatibility or live-readiness claim |
| Checker with synthetic schema events, explicit result/author contract and `--dry-run` | PASS: exit 0, correlated result and STOP answer; unchanged input hashes |
| Exact-interpreter certifi bundle-load example | PASS: bundle loaded with verification enabled; no endpoint request |
| Parent rerun of greenfield/configuration/source-preflight fixture tests | PASS: 83 tests (70 + 9 + 4) |
| Parent `python -m unittest -q test_recovery.py` in recovery fixture | PASS: eight tests |
| Python AST/compilation, YAML/frontmatter/discovery metadata, JSON, internal links, shell-fence `bash -n`, whitespace/unfinished/private-value scans, MIT licence equality and scoped `git diff --check` | PASS |
| Original fixture inputs, dependency pins and repeated handoff file hashes | PASS: preserved, apart from the requested startup and spelling edits |

Ruff and Black remain unavailable; their checks were NOT RUN and no linter was
installed. Syntax/whitespace validation does not replace static analysis by those
tools. The copy test establishes package independence from the book source, not
an isolated dependency resolver or deployment reproduction.

The 13 component tests cover strict JSON scalars, Unicode/escaping, exact inclusive
65,536-byte acceptance and overrun, shape and identity bounds, mutation, input
preservation and fixed errors without rejected input in an exception chain.
An initial Decimal-to-float acceptance failure was repaired with a plain-scalar
check before validation. The two new ADK tests exercise actual Runner, AgentTool,
events and stored tool results while replacing model transport. They reproduce
root/child call-limit scope, reject the fourth aggregate logical generation before
dispatch and prove that a content-free limit error can be marked final. Their
counter is test-only; no provider-attempt or durable budget implementation is
packaged or claimed.

### Independent forward outcomes

Evaluators received only the copied skill, assigned raw fixtures/requests and an
existing interpreter plus an offline execution boundary. They did not receive
expected answers, original source, the case catalog, provenance or validation
reports. The parent inspected generated artefacts, reran their tests and checked
original inputs. The review/plan fixtures remain temporary evaluation artefacts,
not shipped deployment or accounting software.

| Scenario | Observed outcome |
| --- | --- |
| Greenfield current-result handoff | PASS: stateless `prepare_handoff` returns bounded compact JSON for the matching successful result, validates empty results before returning None and rejects stale/malformed/failed input with a fixed public error. All 70 tests passed; no producer, database or model was added. The agent adapted the optional asset's ID/empty-column choices to the requested interface. |
| Existing startup configuration | PASS: loaded settings before the actual import that constructs the application. Nine fresh-process cases passed after three failed against the original path. Preserved the literal model, setting precedence and ADK 2.7.0 pin; actual ADK integration remains untested. |
| Missing native-deployment prerequisites | PASS for local preparation: retained the failure record, distinguished strongly supported source-routing diagnosis from a reproduced SDK boundary, and prepared local-source/packaging/ownership tests. Four preflight tests passed. Target source, installed CLI boundary, account/build and image verification remain explicitly NOT RUN. |
| Consequential failed-run recovery | PASS for the offline approval boundary: preserved all 24 existing reservations and failure/unknown outcomes, prepared cleanup-only reconciliation and a separate unapproved larger-output envelope. Eight local ledger tests passed; a 4096-token reservation was refused with exit 2. No paid replay, fresh counter reset, cache deletion or fabricated cleanup result occurred. Actual provider admission and reconciliation remain unverified. |
| Near miss | PASS: changed only the requested marketing spelling to “Optimising”; did not activate an optimisation/deployment workflow. Exact HTML comparison passed. |
| Repeated invocation | PASS: reran 70 handoff tests and made no change. SHA-256 values of all four fixture files remained identical and were independently checked. |

The greenfield evaluator first hit a pytest collection error while pytest tried
to name a 5,001-digit integer case; an explicit parameter ID repaired that harness
issue without changing dependencies or the handoff contract. Independent content
review also caught an overgeneralised schema-permission statement; it now requires
inspection of the real retrieval path. The formatter reference now explicitly
labels its ID and empty-result choices as adaptable. No other actionable content
finding remained. The controlled evaluation cannot establish permission
enforcement by an unrestricted tool runner or guarantee future generated code.

The six new `part1-depth-*` inputs bring the catalog to 24 cases. Earlier Part 1,
Part 2 and Part 3 forward scenarios were not repeated; the complete package test
suite still covers their bundled helpers. Live application/hosting, production
ownership and authorisation, distributed budgets, speedup, fresh-project setup
and other coding-agent products remain separate evidence boundaries. Required
external approvals are unchanged in [lifecycle.md](lifecycle.md).

### Files in this refinement

Created six files: `references/application-integration.md`,
`references/cloud-run-troubleshooting.md`, `references/part1-verification.md`,
`assets/formatting_contract.py`, `tests/test_formatting_contract.py` and
`tests/test_part1_adk_budget.py`.

Updated nine files: `SKILL.md`, `references/application.md`,
`references/cloud-run.md`, `references/skills-and-cache.md`,
`references/validation.md`, `references/compatibility.md`,
`references/provenance.md`, this validation record and `tests/forward-cases.json`.
The two CLIs and all original manuscript/companion files remain unchanged by this
review. The complete portable package now contains 32 files:

```text
optimise-adk-on-google-cloud/
├── SKILL.md
├── LICENSE
├── agents/
│   └── openai.yaml
├── assets/
│   ├── formatting_contract.py
│   └── session_observation.py
├── references/
│   ├── agent-runtime.md
│   ├── application-integration.md
│   ├── application.md
│   ├── cloud-run-troubleshooting.md
│   ├── cloud-run.md
│   ├── compatibility.md
│   ├── gke-lifecycle.md
│   ├── gke-serving.md
│   ├── gke.md
│   ├── lifecycle.md
│   ├── part1-verification.md
│   ├── provenance.md
│   ├── runtime-lifecycle.md
│   ├── runtime-state-and-streams.md
│   ├── skill-validation.md
│   ├── skills-and-cache.md
│   └── validation.md
├── scripts/
│   ├── check_run.py
│   └── inspect_project.py
└── tests/
    ├── forward-cases.json
    ├── test_adk_contract.py
    ├── test_check_run.py
    ├── test_formatting_contract.py
    ├── test_gke_observation.py
    ├── test_inspect_project.py
    ├── test_part1_adk_budget.py
    └── test_runtime_contract.py
```

## Part 2 depth review: 16 September 2026

Re-audited the updated Part 2 manuscript, current runtime application and examples,
original comparison probes, SDK-boundary preparation, live routing/session results
and accepted-delete recovery. The [coverage map](provenance.md#part-2-depth-review-coverage-and-additions)
records what was retained, added and still requires production integration.

Added conditional implementation, deployment-troubleshooting and verification
references. They connect configuration/import order, actual App propagation,
compaction, lazy clients, memory/job acknowledgement and deployment ownership to
observable acceptance. Added an optional finite-stream consumer and real-Runner
token-compaction tests. The entrypoint stays unchanged; relevant runtime references
route to the added depth. Parts 1 and 3 were not re-audited in this refinement.

### Environments and checks

Commands used existing interpreters and `PYTHONDONTWRITEBYTECODE=1`; pytest runs
disabled its cache. `SKILL_DIR` denotes this package or its complete copy outside
the repository. Main environment: macOS 26.6.2 arm64, CPython 3.11.4, ADK 2.8.0,
AI Platform SDK 1.153.1, GenAI 2.19.0, Pydantic 2.13.4, pytest 8.4.2, PyYAML 6.0.3
and OpenTelemetry API/SDK 1.41.1. Retained runtime: CPython 3.11.4, ADK 2.8.0,
AI Platform SDK 1.153.1, GenAI 2.19.0, Pydantic 2.13.5 and pytest 9.1.1.

| Executed command/check | Actual result |
| --- | --- |
| Installed `quick_validate.py skills/optimise-adk-on-google-cloud` | PASS: “Skill is valid!” |
| `python -m pytest -q -p no:cacheprovider skills/optimise-adk-on-google-cloud/tests` | PASS: 121 tests, no skips, 11 SDK warnings (8.36 s) |
| `python -m unittest discover -s "$SKILL_DIR/tests" -q`, complete copy and unrelated working directory | PASS: 121 tests, no skips (8.425 s); expected SDK logging/warnings |
| Retained runtime: `python -m pytest -q -p no:cacheprovider "$SKILL_DIR/tests/test_finite_answer_stream.py" "$SKILL_DIR/tests/test_runtime_token_compaction.py"` | PASS: 39 tests, 64 subtests, no skips, six SDK warnings (1.49 s) |
| Both copied CLIs with `--help` | PASS: exit 0 |
| Copied inspector, all five modes, `--require-baseline --dry-run`, synthetic requirements | PASS: declaration gates only; no installation or hosting claim |
| Copied checker, synthetic saved events and expected contract, `--dry-run` | PASS: accepted correlated tool result and STOP answer; input hashes unchanged |
| Original companion controlled-interleaving probes | Reproduced swallowed processor timeout and concurrent-buffer data loss; zero provider/network calls |
| Parent rerun of customised buffer tests | PASS: seven tests; API, queue capacity and declared ADK 2.7.0 pin preserved |
| Parent packaging/recovery fixture checks | PASS: initial 12 import probes and 14 synthetic decision tests; fresh isolated evaluation added nine import/archive checks and six operation relationship checks, also rerun; originals preserved |
| Parent final stream fixture verification | PASS: 47 tests (1.00 s); repaired no-op repeat hashes independently matched |
| Python AST/in-memory compilation, JSON, YAML, local Markdown links/anchors, shell-fence `bash -n`, whitespace/private-value/unfinished scans, MIT licence equality and scoped `git diff --check` | PASS |

Ruff and Black were unavailable and NOT RUN; no packages were installed. The
complete-copy check proves independence from book and companion source, not a
clean dependency resolver, another operating system or a hosted deployment.
No new model/cloud/API, resource, IAM, billing, deployment, deletion, global
installation, commit or publication operation occurred. Read-only official web
documentation supported a few contracts; no cloud account was accessed.

### New executable evidence and limits

The 36 finite-stream tests exercise exact invocation/author selection, delta/snapshot
previews, strict aliases/types, thought/tool exclusion, clean-exhaustion acceptance,
late failures, event/UTF-8 budgets, timeout/cancellation, fixed public errors and
owned iterator closure. Actual ADK event serialisation is tested on the recorded
SDK; unsupported versions skip that compatibility evidence explicitly. The text
budget counts incoming eligible text, including repeated snapshots and the final;
it is not a transport allocation bound or just the final display size.

Independent review found that a callback/iterator could suppress timeout
cancellation and return late, and that code-execution results accompanying STOP
text bypassed the initial function-tool filter. Repairs check expiry when control
returns and classify the recorded SDK's supported tool parts, rejecting unsupported
non-null Part payloads. Separate cleanup timeout and cancellation regressions
protect the primary outcome. Cooperative deadlines still cannot force arbitrary
blocking or cancellation-suppressing code to stop, undo callback effects or cancel
already accepted remote work.

Three token-compaction tests execute real ADK App/Runner, deterministic models,
synthetic usage and the real summariser orchestration. They establish compaction
of prior input and selection in the next outgoing request, oversized first input
passing the threshold, and a retained function-call/response pair despite nominal
retention one. Raw storage remains independently inspectable. These are not real
token measurements, summary-quality results, hosted compaction or managed-storage
tests; the three new tests complement the earlier App/sliding-window contracts.

The original `backpressure.py` caught `TimeoutError` around queue reading and
processing, swallowing a processor failure as idle polling and reporting successful
shutdown. A separate `selective_persistence.py` probe reproduced new input being
cleared after an older awaited save. Both are recorded as companion limitations;
this skill-authoring task did not change those examples. The stronger buffering,
outbox, idempotency and job protocols remain target implementation guidance.

### Forward use and repair outcomes

Evaluators received a copied skill, raw disposable fixtures/requests and an
existing interpreter with offline execution restrictions. Expected answers,
original manuscript/code, case catalog and provenance/validation records were
withheld. Parent checks inspected outputs, reran meaningful tests and verified
original pins/receipts and spelling against raw fixtures. Generated applications,
proposed patches and recovery plans remain evaluation artefacts, not shipped
production deployment, budget or persistence software.

| Scenario | Observed outcome |
| --- | --- |
| Greenfield finite answer | Initial result INCOMPLETE: 27 tests passed but parent reproduced code-result narration being committed. Fifteen focused regressions then exposed 12 failures before repair. Repaired implementation passes 47 tests, including real SDK tool/media shapes, late expiry and cancellation. It preserves API/pins and publishes provisional deltas followed by one replacing final; its separate preview/final display caps intentionally differ from the asset's aggregate text budget. |
| Existing buffer | PASS: narrowed idle-timeout handling to queue wait; processor TimeoutError, RuntimeError and cancellation propagate with original identity and balanced accounting. Seven tests passed; remaining failed-consumer drain/admission limits are explicit. No general buffer framework was introduced. |
| Missing deployment prerequisites | PASS for local preparation: staged helper omission, import-driven mock/real change and disabled triage features were diagnosed. Proposed explicit backend/profile selection and source allowlist, while preserving originals. Twelve guarded import probes passed; actual generator, App, metrics, cloud identities and hosted behaviour remain unverified. |
| Consequential operation recovery | PASS for local preparation: preserved the accepted update and its receipt, prepared read-only reconciliation plus a separate source/profile/capacity and 20-turn proposal. Fourteen synthetic recovery tests passed. No setup replay, mutation, paid turn or claimed provider result occurred; unconsumed settings and missing adapter remain explicit. |
| Near miss | PASS: excluded the marketing spelling edit from optimisation work and changed only “Optimizing” to “Optimising”; parent exact-content comparison passed. |
| Repeated invocation | PASS after repair: all 47 tests passed again and SHA-256 hashes of all five fixture files stayed identical, independently checked. The initial pre-repair no-op snapshot is retained as historical evidence, not correctness proof. |

The first deployment evaluator accidentally requested an agent-status inventory,
which exposed unrelated completed-task summaries. It disclosed that exposure;
those results are independent local exercises but not strict blind evidence.
A fresh evaluator repeated both tasks from raw fixtures without agent inventories
or prior reports. Nine isolated packaging/import checks and six exact-operation
relationship checks passed, and parent reruns passed too. It independently
prepared the missing-source repair and accepted-operation recovery without
changing originals or fabricating real SDK/provider evidence.

An automatic approval review initially rejected the near-miss edit because the
fresh evaluator lacked the original task's explicit fixture-edit authority. After
reading only the user's validation instruction authorising that exercise, the same
local patch was approved. No live or broader action was requested or performed.

These six `part2-depth-*` inputs bring the retained catalog to 30 cases. Earlier
Part 1/2/3 forward cases were not repeated. Evaluations used Codex desktop on the
same host with explicit skill access, not native automatic injection or other
agent products. Neither a repaired fixture nor passing local tests guarantees
future generated code. Live full-profile behaviour, durable state/jobs, browser
delivery, cross-principal isolation and fresh-project onboarding retain their
separate evidence boundaries.

### Files in this refinement

Created six files: `references/runtime-application-integration.md`,
`references/runtime-deployment-troubleshooting.md`,
`references/runtime-verification.md`, `assets/finite_answer_stream.py`,
`tests/test_finite_answer_stream.py` and `tests/test_runtime_token_compaction.py`.

Updated eight files: `references/agent-runtime.md`, `references/runtime-lifecycle.md`,
`references/runtime-state-and-streams.md`, `references/validation.md`,
`references/compatibility.md`, `references/provenance.md`, this validation record
and `tests/forward-cases.json`. The entrypoint, discovery metadata, both CLIs,
manuscripts and original companion code remain unchanged by this refinement.
The complete portable package contains 38 files:

```text
optimise-adk-on-google-cloud/
├── agents/
│   └── openai.yaml
├── assets/
│   ├── finite_answer_stream.py
│   ├── formatting_contract.py
│   └── session_observation.py
├── references/
│   ├── agent-runtime.md
│   ├── application-integration.md
│   ├── application.md
│   ├── cloud-run-troubleshooting.md
│   ├── cloud-run.md
│   ├── compatibility.md
│   ├── gke-lifecycle.md
│   ├── gke-serving.md
│   ├── gke.md
│   ├── lifecycle.md
│   ├── part1-verification.md
│   ├── provenance.md
│   ├── runtime-application-integration.md
│   ├── runtime-deployment-troubleshooting.md
│   ├── runtime-lifecycle.md
│   ├── runtime-state-and-streams.md
│   ├── runtime-verification.md
│   ├── skill-validation.md
│   ├── skills-and-cache.md
│   └── validation.md
├── scripts/
│   ├── check_run.py
│   └── inspect_project.py
├── tests/
│   ├── forward-cases.json
│   ├── test_adk_contract.py
│   ├── test_check_run.py
│   ├── test_finite_answer_stream.py
│   ├── test_formatting_contract.py
│   ├── test_gke_observation.py
│   ├── test_inspect_project.py
│   ├── test_part1_adk_budget.py
│   ├── test_runtime_contract.py
│   └── test_runtime_token_compaction.py
├── LICENSE
└── SKILL.md
```


## Part 3 depth review — 16 September 2026

**LOCAL PASS** for the refined package and six new usage exercises. This review
revisited the updated Part 3 manuscript, original comparison, actual GKE server,
examples, release manager, tests, failed provisioning attempts, final successful
retry and independent cleanup records. The [coverage matrix](provenance.md#part-3-depth-review-coverage-and-additions)
maps those lessons to the skill without making the companion a runtime dependency.
No cloud account, model/provider API, container build, deployment or deletion was
used. Public primary documentation was read for Storage bucket insertion,
Workload Identity principal composition and Deployment termination overlap.

### Additions and findings

Three conditional references deepen application integration, deployment failure
recovery and verification. They preserve the short entrypoint and existing GKE
selection routes. No extra production framework or asset was added: the existing
session observation and finite-answer components remain optional adaptations.

New actual-SDK evidence establishes specific boundaries:

- ADK 2.8's supplied FastAPI lifespan exits before cached Runner closure. Closing
  its shared service there may precede a required flush. Public database options
  should be checked before replacing the factory or constructing an unused service.
- SQLite applies a history limit in SQL, while the managed adapter consumes its
  substituted API iterator before a positive slice. Zero avoids event retrieval.
  History/state remain stored, and the raw slice can split a tool exchange.
- Runner flush and database engine disposal are distinct actions. These are
  SQLite/SDK lifecycle observations, not PostgreSQL pool or drain certification.
- Explicit-ID and collection session POST bodies differ; application routing name
  and answer author differ too. Actual HTTP streaming flags reach the model,
  and a generator error can follow HTTP 200. TestClient does not prove browser
  delivery or first-token latency.
- Native tracing can retain a conversation ID with capture disabled. This is an
  in-memory negative control, not a completed production privacy filter.

The review reproduced two saved-output acceptance gaps in the skill checker:
code-result narration and nested function-response media/continuation could
receive PASS despite being outside its named-function/text contract. The repaired
checker rejects unsupported non-null outer and nested protocols, including
partial arguments and scheduling, in snake_case and camelCase. Null SDK defaults
and ordinary JSON business payloads remain valid. Existing regression methods
were expanded using real SDK serialisation and synthetic adverse cases. An
independent final reviewer reproduced rejection of eight nested counterexamples
and acceptance of the supported cases; no remaining material findings were reported.

Two companion/manuscript limitations were recorded without modifying them. The
companion's simpler smoke validator accepted mismatched call IDs plus partial-only
text in a synthetic probe; the historical complete live answers are not retracted.
The manuscript's capacity-only description omits the earlier Storage endpoint
failure and CLI response-shape defect. The new deployment reference retains the
precise sequence, successful same-region retry and limits of the two-Pod lab.

### Package verification

Final commands below use normalised local paths: `AUTHORING_PYTHON` was the
existing repository interpreter, `RETAINED_GKE_PYTHON` the preserved GKE campaign
interpreter, and `SKILL_COPY` a complete disposable copy outside the repository.
They are evidence locators, not additional prerequisites or installation steps.

```bash
PYTHONDONTWRITEBYTECODE=1 "$AUTHORING_PYTHON" -m pytest -q -p no:cacheprovider skills/optimise-adk-on-google-cloud/tests
PYTHONDONTWRITEBYTECODE=1 "$RETAINED_GKE_PYTHON" -m pytest -q -p no:cacheprovider skills/optimise-adk-on-google-cloud/tests/test_gke_http_contract.py skills/optimise-adk-on-google-cloud/tests/test_gke_session_contract.py skills/optimise-adk-on-google-cloud/tests/test_check_run.py
PYTHONDONTWRITEBYTECODE=1 "$AUTHORING_PYTHON" -m unittest discover -s "$SKILL_COPY/tests" -q
```

| Final check | Result and scope |
| --- | --- |
| Complete package, authoring environment | **135 passed**, 27 warnings, 11.37 s; no skips. Fourteen additional test methods: five actual HTTP contracts, six session/lifecycle/native-span contracts, three checker regressions. |
| Focused retained GKE environment | **41 passed**, 20 warnings, 42 subtests, 3.73 s; no skips. Includes all 14 new methods and 27 existing checker methods, not a second full suite. |
| Complete portable copy, working directory outside repo | **135 unittest tests passed**, 10.678 s; no skips. Copied Python/JSON inputs matched the tested package. |
| Both CLI help paths | Exit 0 from the complete copy; arguments and read-only scope shown. |
| Inspector dry-run | All five modes passed the synthetic exact-pin baseline; no application import or credential-content read. |
| Saved-run CLI dry-run | Complete routing/tool/two-partial fixture exit 0; unsupported code-result fixture exit 2; incomplete fixture exit 3. Outputs omitted the synthetic private marker; fixture SHA-256 and modification times stayed identical. |
| Package structure | Skill quick validator PASS; 43 files, 16 Python files parsed/compiled without bytecode output, 36 unique raw usage cases. JSON/YAML, internal links/anchors, fenced blocks and shell syntax checked. |
| Hygiene | Scoped diff/whitespace checks PASS; MIT licence matches source; no absolute author paths, personal project/account identifiers or unresolved markers in the shipped package. |

The two CLI help calls, five inspector modes and three saved-run cases were ten
actual subprocess invocations from the standalone copy, with an empty command
PATH and no writes/network effects from either CLI. The dry-run flags do not
contact GCP. Static checks included all new files, not only tracked diff entries.
Ruff and Black were absent and **NOT RUN**; neither was installed.

Both environments used macOS 26.6.2 arm64, CPython 3.11.4, ADK 2.8.0, AI Platform
SDK 1.153.1, Starlette 1.6.0, HTTPX 0.28.1, aiosqlite 0.22.1 and PyYAML 6.0.3.
Authoring: GenAI 2.19.0, Pydantic 2.13.4, FastAPI 0.136.3, SQLAlchemy 2.0.51,
OpenTelemetry API/SDK 1.41.1, pytest 8.4.2. Retained GKE: GenAI 2.23.0,
Pydantic 2.13.5, FastAPI 0.141.1, SQLAlchemy 2.0.52, OpenTelemetry API/SDK 1.42.1,
pytest 9.1.1. Warnings include ADK experimental/deprecated contracts, TestClient
HTTPX deprecation and retained dependency metadata warnings; no dependency was
changed to suppress them. Durations describe these checks, not agent performance.

Tests guard socket/DNS/auth discovery where actual SDK imports could cause an
external effect. Provider/model boundaries are deterministic doubles, SQL is
local temporary SQLite and exporters are in memory. No production driver,
container image, remote session API, authentication gate, OTLP collector or
cloud resource was validated anew. Missing optional test dependencies or another
ADK version produce explicit skips rather than silently installing/upgrading.

### Six independent forward cases

Three fresh evaluators received only a copied skill, their raw requests/fixtures
and an existing interpreter, with explicit local-edit authority. Provenance,
validation history, expected answers, case catalog and original companion were
withheld. A repeat request was read only after the first result and file hashes
were saved. Parent review inspected code/claims, reran the meaningful checks and
compared pins, receipts and spelling with the original raw catalog.

| Scenario | Observed result |
| --- | --- |
| Greenfield lifecycle | **PASS:** small standard-library context manager preserves supplied App/service/Runner identity, prepares before use, closes Runner before service, attempts both cleanups and preserves primary failure/cancellation. Eighteen tests passed; parent rerun 18 passed. Cooperative startup/per-resource deadlines and unreturned factory resources remain explicit limits. No ADK or database integration was fabricated. |
| Existing packaging | **PASS after repair:** added the required module to both the actual source allowlist and Docker COPY. Four tests initially failed; staging-only repair left one COPY test failing; both repairs passed all four. Parent rerun passed. Actual staged import runs without site packages; Docker layout is a limited local simulation, not an image build. ADK 2.7.0 declaration was preserved despite the borrowed 2.8.0 interpreter. |
| Missing telemetry/server boundaries | **PASS for local preparation:** preserved the unimplemented server and unsafe original logger, supplied a concrete integration/export plan and a separate reviewable timing projection. Two actual ADK/ASGI/OTel tests passed, including native-ID and unsafe-parent controls; parent rerun passed. Final local projection omits synthetic markers. It emits identifier-free timing records, not OTLP spans. Whole-server/export/log privacy and deployment remain unverified. |
| Consequential uncertain create | **PASS for local preparation:** saved Cluster response was not mistaken for an Operation. Ten guarded tests selected the unique new exact-target CREATE after explicit project ID/number normalisation; parent rerun passed. Saved RUNNING remained unresolved, no receipt was rewritten and no replay/deletion occurred. A separately scoped region/three-Pod/HTTPS/20-turn proposal identifies missing account, adapter, source, identities and financial ceiling before execution. |
| Near miss | **PASS:** optimisation work was excluded; only “Optimizing” became “Optimising” in the marketing HTML. Parent exact-content check passed. |
| Repeated invocation | **PASS:** all 18 lifecycle tests passed again with no implementation changes. SHA-256 hashes of all five first-pass tracked files remained identical; parent independently confirmed. |

One evaluator's first read-only file inventory traversed the temporary campaign
parent while filtering output to its two requests and copied-skill Markdown.
It disclosed that scope deviation; no other fixture contents, expected answers,
provenance, validation history or agent-status summaries were read. This limits
a claim of strict directory isolation, but supplied no answer contamination.
All later reads/writes remained scoped. A lifecycle evaluator initially guessed
two absent filenames; the exact assigned path was then supplied without broader
search or additional source context.

These six `part3-depth-*` cases bring the catalog to **36**. The earlier 30 forward
cases were not repeated; the complete package's regression tests were. Generated
fixture code/plans are disposable evaluation artefacts, not shipped deployment,
recovery or telemetry software. Checks used Codex desktop on this host with
explicit access to the skill, not automatic discovery or a cross-agent/OS matrix.
No future generated implementation, production readiness or speedup is guaranteed.

### Files in this refinement

Created five files: `references/gke-application-integration.md`,
`references/gke-deployment-troubleshooting.md`, `references/gke-verification.md`,
`tests/test_gke_http_contract.py` and `tests/test_gke_session_contract.py`.

Updated ten files: `references/gke.md`, `references/gke-serving.md`,
`references/gke-lifecycle.md`, `references/validation.md`,
`references/compatibility.md`, `references/provenance.md`, this validation record,
`scripts/check_run.py`, `tests/test_check_run.py` and `tests/forward-cases.json`.
No file was removed. The entrypoint, discovery metadata, inspector, assets,
Parts 1/2 guidance, manuscripts and companion implementation were preserved.
The shared checker deliberately gained stricter unsupported-protocol handling.
The complete portable package contains 43 files:

```text
optimise-adk-on-google-cloud/
├── agents/
│   └── openai.yaml
├── assets/
│   ├── finite_answer_stream.py
│   ├── formatting_contract.py
│   └── session_observation.py
├── references/
│   ├── agent-runtime.md
│   ├── application-integration.md
│   ├── application.md
│   ├── cloud-run-troubleshooting.md
│   ├── cloud-run.md
│   ├── compatibility.md
│   ├── gke-application-integration.md
│   ├── gke-deployment-troubleshooting.md
│   ├── gke-lifecycle.md
│   ├── gke-serving.md
│   ├── gke-verification.md
│   ├── gke.md
│   ├── lifecycle.md
│   ├── part1-verification.md
│   ├── provenance.md
│   ├── runtime-application-integration.md
│   ├── runtime-deployment-troubleshooting.md
│   ├── runtime-lifecycle.md
│   ├── runtime-state-and-streams.md
│   ├── runtime-verification.md
│   ├── skill-validation.md
│   ├── skills-and-cache.md
│   └── validation.md
├── scripts/
│   ├── check_run.py
│   └── inspect_project.py
├── tests/
│   ├── forward-cases.json
│   ├── test_adk_contract.py
│   ├── test_check_run.py
│   ├── test_finite_answer_stream.py
│   ├── test_formatting_contract.py
│   ├── test_gke_http_contract.py
│   ├── test_gke_observation.py
│   ├── test_gke_session_contract.py
│   ├── test_inspect_project.py
│   ├── test_part1_adk_budget.py
│   ├── test_runtime_contract.py
│   └── test_runtime_token_compaction.py
├── LICENSE
└── SKILL.md
```
