# Skill verification record

Initial validation: 15 September 2026. The first sections preserve that package's results; the dated depth-review section below records the 16 September revision. Neither is a new cloud deployment or live companion campaign.

## Environment

Package and forward tests used the existing isolated Python **3.11.4** environment, on **macOS / Darwin 25.6.0, arm64**, with **pytest 9.1.1** and **PyYAML 6.0.3**. Synthetic workflow fixtures used **SQLite 3.42.0** and **SQLGlot 29.0.1**. The selected interpreter also had the exact ADK/provider versions recorded in [compatibility.md](compatibility.md); no dependency installation or version changes occurred.

Agent behaviour was exercised in **Codex Desktop** using two independent agents with fresh context. Each received only the packaged skill, a clean synthetic project, a realistic request and the permitted local interpreter. Neither had access to the book, companion code or the other agent's fixture. The core `SKILL.md` SHA-256 was `96c4d6d34541cd09af04a1ff1c5ddeeef842e314de301a246d1238d279d37b6a`, matching the 15 September entrypoint before the depth-review revision.

Windows, Linux and other coding-agent environments were **NOT RUN**. Plain Markdown and optional UI metadata make the package reusable; they do not prove behavioural portability. A late inspector change added a clear failure on platforms without directory-descriptor scanning, with a new unit test and a final clean-copy run. It does not change the tested macOS workflow. No new live API, deployment, IAM or paid Gemini/BigQuery work occurred.

## Package checks

Commands below use `python` to denote the selected Python 3.11.4 interpreter. Package commands ran with the skill directory as their working directory; scenario commands ran in the corresponding temporary fixture. Paths supplied to inspection/checker options were real local fixture paths, not unresolved values.

| Command or check | Actual result |
| --- | --- |
| Official `quick_validate.py` against the skill directory | Exit 0, `Skill is valid!` |
| YAML metadata, one-skill naming, all relative links/anchors, unfinished-text and private-identifier checks | PASS; 18 internal links/anchors; automatic discovery enabled |
| Python AST parsing and whitespace checks | PASS for all bundled Python/Markdown; no project formatter or type checker was configured for this package |
| `PYTHONDONTWRITEBYTECODE=1 PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python -m pytest -q -p no:cacheprovider tests` | Exit 0; **45 passed, 88 subtests passed**, 7.14 seconds from final repository location |
| Copy package alone to a fresh temporary directory; `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH='' python -S -m unittest discover -s tests -q` | Exit 0; **45 tests passed**, 5.994 seconds; runner site packages disabled and no book/companion source in the copy |
| `python scripts/inspect_project.py --help` | Exit 0, static help |
| Inspector `--project` with `--dry-run --expect-adk 2.8.0` | Exit 0, inventory only; ADK gate explicitly `NOT_RUN_DRY_RUN`; no content reads |
| Inspector against current companion with `--expect-adk 2.8.0` | Exit 0, gate PASS; declared and interpreter ADK versions reported separately; no `.env` values read |
| `python scripts/check_results.py --help` | Exit 0, static help |
| Checker against the two JSON examples in [validation.md](validation.md), with `--expected`, `--actual` and `--dry-run` | Exit 0, `DRY_RUN`, `SHAPES_VALID_NO_VERDICT` |
| Same checker examples without `--dry-run` | Exit 0, `PASS`, `RESULTS_MATCH` |

The 30 checker tests cover explicit aliases, exact precision, missing/conflicting metrics, duplicate cohorts/JSON keys, malformed input, non-finite values, cardinality, bounded reads, symlinks, secret-safe output, dry-run behaviour and repeated read-only invocation. The 15 inspector tests cover separate version evidence, custom package managers, unchanged files, secret suppression, skipped links, bounds, malformed/unsupported manifests, version conflicts, help/dry-run, and unsupported platform handling. Exit 1/2/3 failure paths were asserted where applicable; a dry run was never counted as a successful live integration.

## Forward-use cases

| Request | Observed behaviour and actual validation |
| --- | --- |
| Greenfield offline SQL assistant with supplied model/warehouse interfaces | Created a small application boundary with reviewed revenue, generated sales/support and refusal paths. Used actual SQLite rather than imposing BigQuery syntax. **81 tests passed**, compileall exit 0. Exact revenue A=50/B=40; selective schemas; no author/schema call on template path; denied write and unsupported queries before execution. |
| Existing customised implementation with all-schema authoring | Preserved `answer(question, model, warehouse)`, Acme output fields, original legacy author-only test and dependency pins. Added selection, scoped SQL policy and database read-only enforcement. **73 tests passed**, including the unchanged original test. |
| Missing credentials/prerequisites | Inspected settings before import, distinguished installed SDKs from connectivity, and added local settings checks: **4 tests passed**. Reported absent agent/provider adapters and required configuration; no credential access or live claim. |
| Consequential provisioning/testing/cleanup request | Recorded the supplied project/location/resource names and proposed finite test limits. Identified unresolved model, quota and spend decisions; recorded the future exact-command approval and owned-cleanup boundary. No consequential operation ran. This was an offline approval-boundary replay, not a validated cloud lifecycle script. |
| Ordinary PostgreSQL indexing question | Declined skill activation, gave bounded general advice and requested query/plan evidence. No SQL-agent architecture or cloud work was introduced. |
| Second invocation on the customised project | Reinspected and reran tests: **73 passed**. SHA-256 comparison found **zero changed files across 31 files**; application data also remained unchanged on repeat reads. |

The chapter-specific behaviour was exercised through actual public `answer()` calls with a scripted model and an in-memory SQLite database: selected-schema-only retrieval, bound values, exact fixture answers and rejected writes with zero query submissions. The tests also checked an independent database read-only boundary. They are **OFFLINE VERIFIED**, not evidence of Gemini quality, BigQuery compatibility or a universal SQL sandbox.

Both independent implementations initially exposed SQLite's optimised `COUNT(*)` authorisation event. Their fixture-specific corrections passed subsequent tests. No resulting defect in the skill instructions required a rewrite. The greenfield slice deliberately supports a small single-table grammar; the customised fixture evaluates its own supported CTE/aggregate subset. These generated applications remain temporary evaluation artefacts and are not shipped as production runtime templates.

## Scope and remaining checks

The original manuscript and companion source were unchanged. All 44 source files still match the recorded follow-up fingerprints. Existing repository skills and concurrent work were preserved. No commit, push, publication, deployment, new cloud resource or secret was produced.

The skill entrypoint, scripts, tests, conditional references, MIT licence and optional discovery metadata are the complete deliverable. The historical live behaviour remains separately dated in [compatibility.md](compatibility.md). Before using a new production target, verify its model/SDK contract, authenticated scope, provider SQL policy, cumulative budgets, output completeness and separately approved live lifecycle. The skill's local results do not supply those target-specific guarantees.

## 16 September 2026 — implementation depth review

Re-opened the current manuscript, source, unit/integration tests, independent audit,
both live campaign records and later cleanup evidence. Three parallel source audits
covered lifecycle, semantics/evaluation and ADK/runtime integration. Their findings
were incorporated and checked locally against the source. The expanded entrypoint's
SHA-256 is `9009167cdbfd6a4afaf3cc057a640a29d96cd9caa72e156558582e186613ef19`.

The change adds five conditional references and one runnable test asset:

- Metric contracts, adversarial fixture mutations, field-specific value resolution,
  exact context, nested-schema limits and relationship-policy checks.
- Actual ADK graph/event wiring, wire/runtime models, trusted invocation interfaces,
  shared credential construction, configuration lifetime and concurrency limits.
- Read-only prerequisite inspection, API/IAM matrices, durable operation state,
  stable loads, token readiness, interrupted deletion and independent closure.
- Public Runner/HTTP/browser acceptance, outcome mutation controls, telemetry,
  follow-up semantics and managed-tool responsibility boundaries.
- Failure signatures, concrete parser/value regressions and reviewed-template
  promotion from generated traces.
- A synthetic ADK contract asset that retains the actual SDK serializer and blocks
  ADC discovery and socket/DNS operations during its test fixture.

The [coverage map](compatibility.md#depth-review-coverage) connects the chapter's
sections and campaign findings to these procedures. Production extensions remain
labelled, including caller isolation, complete SQL policy, cumulative deadlines,
semantic follow-ups and cloud frontend hosting. The failed historical latency gate
and original checker failures remain recorded.

### Current test environment

Used the existing repository Python **3.11.4** environment on **macOS 26.6.2 /
Darwin 25.6.0, arm64**, with `google-adk` **2.8.0**, `google-genai` **2.19.0**,
`pydantic` **2.13.4**, `google-auth` **2.57.0**, `httpx` **0.28.1**, `pytest`
**8.4.2**, `PyYAML` **6.0.3** and SQLite **3.42.0**. BigQuery **3.42.0** and
API Core **2.31.0** were installed but were not exercised by the synthetic asset.
No dependencies were installed or changed.

This is a different SDK stack from the historical GenAI 2.23.0 live campaign.
The old isolated environment no longer supplied its full dependencies, so it was
not silently reused or repaired. The new asset was **NOT RUN on GenAI 2.23.0**.
The test result is limited to the synthetic integration on the versions above;
it is not a new whole-companion compatibility result.

### Commands and observed results

Commands use `python` for that selected interpreter and run from the skill root
unless stated otherwise. The official validator is supplied by the installed
skill-creator guidance; it is not a dependency of the delivered skill.

| Command or check | Actual result |
| --- | --- |
| Official `quick_validate.py` against this skill | Exit 0, `Skill is valid!` |
| `PYTHONDONTWRITEBYTECODE=1 PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python -m pytest -q -p no:cacheprovider tests` | Exit 0; **45 passed**, 6.88 seconds |
| Same pytest invocation targeting `assets/test_adk_contract.py` | Exit 0; **10 passed**, one upstream ADK `BaseAgentConfig` deprecation warning, 2.94 seconds |
| Standalone copy; `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH='' python -S -m unittest discover -s tests -q` | Exit 0; **45 tests passed**, 5.904 seconds; site packages disabled |
| Standalone copy; same offline pytest asset invocation with empty `PYTHONPATH` | Exit 0; **10 passed**, same upstream warning, 1.91 seconds; no companion/book files in copy |
| Both helper `--help` and `--dry-run` invocations | Exit 0; plans reported no correctness/connectivity verdict |
| Inspector on a synthetic project with declared ADK 2.8.0 and a private canary `.env` | Exit 0; strict ADK gate PASS; no secret value in output |
| Checker on the two bundled validation JSON examples | Exit 0; exact PASS; no model or database involved |
| Semantic recipe replay in SQLite | PASS: baseline plus six independent mutations, both Sydney-to-UTC endpoints, follow-up selection versus presentation example |
| Python AST, YAML/discovery metadata, internal relative links/anchors, private-identifier/unfinished-text scans and scoped whitespace check | PASS |
| Source preservation | All **44** companion files still match the follow-up fingerprints; all **42** files in the additional source/manuscript snapshot remained unchanged |

The ADK asset's ten cases establish four branch trajectories, required/nullable
provider fields, exact synthetic metadata delivery, two null-bearing refusal
statuses, incomplete READY rejection, a removed-callback negative control and
active ADC/network guards. The “execution” node is a spy with fixed synthetic
rows; no SQL is executed. HTTP responses are doubles, and the model transport is
non-streaming while the actual asynchronous Runner event stream is consumed.
It does not test live Gemini, BigQuery, credentials, SQL policy, HTTP/SSE serving,
browser interaction or the target application's integration.

Fresh independent agent forward-use evaluation of the expanded revision was
**NOT RUN**: follow-up worker turns stopped at the account usage limit. The earlier
six forward-use cases remain dated evidence for the previous entrypoint, not a
new behavioural PASS for this revision. Local review and the new executable
framework checks completed after those workers stopped. No reset was purchased
or consumed, and no cloud operation was used to compensate for that limitation.

### Delivered package

```text
adk-sql-agent-engineering/
├── SKILL.md
├── LICENSE
├── agents/
│   └── openai.yaml
├── assets/
│   └── test_adk_contract.py
├── references/
│   ├── acceptance-and-extensions.md
│   ├── adk-runtime.md
│   ├── compatibility.md
│   ├── execution-safety.md
│   ├── implementation.md
│   ├── lifecycle-runbook.md
│   ├── semantic-contracts.md
│   ├── troubleshooting.md
│   ├── validation.md
│   └── verification-record.md
├── scripts/
│   ├── check_results.py
│   └── inspect_project.py
└── tests/
    ├── test_check_results.py
    └── test_inspect_project.py
```

Changed the entrypoint, optional UI prompt and five existing references; added the
five detailed references and test asset. The original two helpers, their tests and
the licence are unchanged. The skill remains self-contained and automatically
discoverable. Other repository work was preserved. No manuscript/source changes,
commit, push, installation, deployment, API activation, IAM change, paid call or
cloud resource creation/deletion occurred in this revision.
