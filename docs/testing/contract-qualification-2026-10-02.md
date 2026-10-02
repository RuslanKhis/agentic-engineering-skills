# Pre-inference contract qualification — 2 October 2026

Applied the second field-feedback request to evaluation, workflow and retrieval
guidance, preserving the previous progressive-validation and spending boundaries.

| Feedback | Change |
| --- | --- |
| Prompt, schema and validator agreement before inference | [Contract qualification](../../skills/adk-agent-evaluation/references/contract-qualification.md) traces mandatory requirements to authoritative sources and rendered/serialized boundaries, with honest valid fixtures and discriminating negatives |
| Realistic document representability | Qualification and [local-document coverage](../../skills/adk-memory-architecture/references/local-document-coverage.md#qualify-the-source-representation-before-generation) cover hierarchy, continuations, footnotes, repeated cells, dense tables, images, missing neighbours and physical versus pack adjacency |
| Deterministic bookkeeping versus interpretation | Source text/coordinates remain server-owned; permissible paraphrase and substantive support are separate from identity, native/Pydantic acceptance and provider-enforced wire schema |
| Earliest-stage repair and dependency-aware reuse | Progressive validation and [checkpoint reuse](../../skills/adk-workflow-design/references/checkpoint-reuse.md) classify defective producers and bind parser/representation versions alongside existing dependencies |
| Normal-route qualification | Workflow validation requires actual orchestration/storage wiring with denied external access and provider substitution; correction probes cannot establish served-route acceptance |

The [source pack](../../skills/adk-agent-evaluation/assets/contract-qualification.json)
and [18 executable examples](../../skills/adk-agent-evaluation/tests/test_contract_qualification.py)
demonstrate failures before repair and passing controls afterward. They count actual
provider-double calls and check reopened file contents. Unchanged saved stages reuse
with zero additional calls; stale parser/settings/projection changes fail without
rewriting retained evidence. The fixture support oracle is an authored test control,
not a proposed production semantic judge. Dense and large-envelope examples remain
small synthetic exercises, not target-workload qualification.

Three new [scenario definitions](../../evals/scenarios.json) retain future trials
for full contract qualification, document-shape diagnosis and deterministic literal
binding. Their assertions are **not measured fresh-agent passes**.

## Executed evidence

Used the existing isolated CPython 3.12.9 maintainer environment from the previous
update, with PyYAML 6.0.3, markdown-it-py 4.0.0 and pytest 9.1.1. No packages or
dependency pins changed for this update.

- `python -B scripts/check_repo.py`: exit 0; **448 passed, 59 optional SDK tests
  skipped**, including the first 15 new examples.
- After adding the final three saved-stage controls, the affected evaluation
  suite passed **44 tests** (18 new), zero skips. Unaffected suites were not rerun.
- All **13 skill packages** validated with zero errors/warnings; official
  skill-creator validation passed for all three modified packages.
- Evaluation-case structure, Markdown resources and `git diff --check` passed.

Retained [repository output](artifacts/contract-qualification/repo-checks.txt),
[final evaluation output](artifacts/contract-qualification/evaluation-checks.txt)
and [modified-source hashes](artifacts/contract-qualification/source-manifest.json)
identify the executed evidence. Final evidence-note edits received structural and
link checks, rather than another runtime suite.

No fresh-agent trial, real-ADK contract execution, Pydantic integration, provider
call, provider capability/pricing lookup or independently source-reviewed domain
assessment ran. The fixtures contain authored extraction records and an image
placeholder, not PDFs or image bytes. Production storage, authentication and
normal served ADK wiring still require target-project checks. Historical SDK
compatibility and `last-tested` dates remain unchanged.
