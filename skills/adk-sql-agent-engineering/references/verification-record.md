# Skill verification record

Validation date: 15 September 2026. This record concerns the portable skill package, not a new cloud deployment or a new live companion campaign.

## Environment

Package and forward tests used the existing isolated Python **3.11.4** environment, on **macOS / Darwin 25.6.0, arm64**, with **pytest 9.1.1** and **PyYAML 6.0.3**. Synthetic workflow fixtures used **SQLite 3.42.0** and **SQLGlot 29.0.1**. The selected interpreter also had the exact ADK/provider versions recorded in [compatibility.md](compatibility.md); no dependency installation or version changes occurred.

Agent behaviour was exercised in **Codex Desktop** using two independent agents with fresh context. Each received only the packaged skill, a clean synthetic project, a realistic request and the permitted local interpreter. Neither had access to the book, companion code or the other agent's fixture. The core `SKILL.md` SHA-256 was `96c4d6d34541cd09af04a1ff1c5ddeeef842e314de301a246d1238d279d37b6a`, matching the delivered entrypoint.

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
