# Skill package validation

Recorded on 15 September 2026. The current Parts 1–3 package passes 67 local
tests. The initial Part 1 record is retained below, followed by the Part 2 and
Part 3 extension results. These are checks of this portable skill and
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
