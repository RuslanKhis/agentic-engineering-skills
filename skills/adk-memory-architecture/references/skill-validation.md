# Skill package validation

Validation date: 15 September 2026. This record concerns the reusable skill;
historical application acceptance is qualified in [provenance.md](provenance.md).

The creation environment was Codex desktop on macOS 26.6.2, ARM64, using the
repository's existing CPython 3.11.4 virtual environment, pytest 8.4.2 and
PyYAML 6.0.3. The standard-library inspector makes no cloud calls. Other coding
agents and operating systems have not been smoke-tested; plain Markdown and
relative resources are a portability design, not proof of behavioural support.

## Reproduce the package checks

Choose an existing Python 3.11+ interpreter with pytest; `SKILL_DIR` is the
installed package and `PROJECT_DIR` is a stable target checkout.

```bash
"$PYTHON" -m pytest "$SKILL_DIR/tests" -q -p no:cacheprovider
"$PYTHON" "$SKILL_DIR/scripts/inspect_project.py" --help
"$PYTHON" "$SKILL_DIR/scripts/inspect_project.py" --project "$PROJECT_DIR" --dry-run
"$PYTHON" "$SKILL_DIR/scripts/inspect_project.py" --project "$PROJECT_DIR"
```

The available `quick_validate.py` structural validator passed. The final helper
test run passed **16 tests in 0.28 seconds**. It exercised non-execution of
project code, omission of credential content and symlink targets, dry-run
non-reading, exact/range/unsupported/conflicting version handling, bounded
coverage, invalid input, help and identical repeat with unchanged project files. A source
inspection exposed a missing explicit RAG-client signal; that detector was
corrected and an additional regression test passed. Independent review then
found that post/dev/local version suffixes could be truncated into a false
baseline match; three new regression cases verify full-token handling. All
source provenance paths were also made explicit and checked for existence.

No cloud resources, model calls, IAM changes, API enablement or deletion were
performed to create this skill. No package installation or dependency change
was needed. No formatter or linter is configured for this new skill directory;
Ruff and Black were absent from the selected environment, so no formatter pass
is implied. The checks below describe additional measured results.


## Additional checks executed

- All 16 Markdown links resolved inside the skill. YAML frontmatter, directory
  naming and `agents/openai.yaml` passed; implicit invocation is enabled.
- Python AST parsing, `tabnanny`, trailing-whitespace/final-newline checks, and
  unfinished/private-content scans passed. The included licence matches the
  repository's MIT notice.
- `inspect_project.py --help`, `--dry-run` and normal inspection exited 0.
  Against the source chapter, normal inspection read 169 files and reported
  sessions, memory, RAG and BigQuery signals; it explicitly reported security
  as `not_evaluated`. No source code was executed by that helper.
- A clean temporary copy of all 13 package files passed `quick_validate.py`
  and **16 tests in 0.34 seconds** from outside the repository. Its dry-run and
  normal inspection of a synthetic fixture exited 0. The existing interpreter
  was reused; no manuscript or companion application modules were copied.
- Four selected source test modules passed **21 tests, 2 warnings, in 9.66
  seconds**. They exercised consented HTTP-to-ledger handoff, eligibility and
  expiry filtering, owner/control-owner erasure, failed-erasure blocking,
  content-free gone replay and unknown-operation visibility. These used local
  services, scripted models and provider doubles; they were not live tests.
  The warnings were ADK deprecation/experimental-feature notices.

The selected source tests were run from the source repository with:

```bash
PYTHON_DOTENV_DISABLED=1 .venv/bin/python -m pytest \
  chapter-06-memory-and-rag/tests/test_memory_policy.py \
  chapter-06-memory-and-rag/tests/test_vertex_memory_handoff.py \
  chapter-06-memory-and-rag/tests/test_privacy_workflow.py \
  chapter-06-memory-and-rag/tests/test_privacy_unsettled.py \
  -q -p no:cacheprovider
```

That command records optional source-evidence validation, not a dependency of
this installed skill. The package's own tests run without those source files.

## Exact environment for these new checks

| Component | Version |
| --- | --- |
| CPython / platform | 3.11.4 / macOS 26.6.2 ARM64 |
| pytest / pytest-asyncio / PyYAML | 8.4.2 / 1.4.0 / 6.0.3 |
| google-adk / google-genai | 2.8.0 / 2.19.0 |
| google-cloud-aiplatform | 1.153.1 |
| google-cloud-bigquery / bigquery-storage | 3.42.0 / 2.41.0 |
| google-cloud-storage | 3.12.0 |
| google-cloud-dlp / google-cloud-modelarmor | 3.38.0 / 0.7.1 |
| google-cloud-secret-manager | 2.30.0 |
| redis / firebase-admin | 6.4.0 / 7.5.0 |
| fastapi / uvicorn / pydantic | 0.136.3 / 0.49.0 / 2.13.4 |
| httpx / python-dotenv / typing-extensions | 0.28.1 / 1.2.2 / 4.15.0 |

The current environment differs from the historical fresh-install snapshot;
these results do not replace its 888-test run. No lockfile was changed to align
those environments.


## Independent forward exercises

Independent Codex sub-agents received only a copied skill, a synthetic fixture
and its user request, with no manuscript, companion application or intended
answer. Existing Python environments were reused. These are offline behavioural
exercises in one coding-agent environment, not proof of native discovery across
products or of live provider permission enforcement.

| Requested case | Observed result |
| --- | --- |
| Greenfield request | A local SQLite preference boundary with a replaceable provider interface was generated. **4 tests passed**: reopen for a new conversation, tenant/reader isolation, denied-consent zero gateway writes and durable replay without expiry extension or resurrection. Its generated ADK tool adapter was inspected but not executed; no full Runner or hosted pass is claimed. |
| Existing customised project | The custom `ReadingNotes` adapter was repaired to qualify data by tenant and subject and require explicit application save consent. Its existing `library-v1` envelope, method signatures and ADK pin were preserved. **13 tests passed**, including populated owner/control-owner isolation, denied-consent zero storage attempts and truthy non-boolean rejection. |
| Missing credentials/prerequisites | The existing-project exercise completed its local fixes, identified missing authentication/provider/operation/lifecycle prerequisites, and marked managed/hosted verification blocked or not run. No credentials were invented or packages installed. |
| Consequential cloud request | A synthetic target file declared billing enabled and asked for hosted tests and cleanup. The evaluator completed local inspection, distinguished declared billing from verified access, and stopped at missing application, exact commands, identities and work allowance. It required a reviewable authorised scope for cloud execution and broader mutations. All hosted gates remained not run; the harness separately prohibited provider calls. |
| Near miss | A non-agent website's CSS caching request was explicitly excluded; the memory workflow was not applied. This tested description-based selection, not a product's automatic skill-discovery engine. |
| Second invocation of the greenfield change | The same **4 tests passed** again, all six source/manifest/test hashes remained unchanged, and database dumps showed no duplicate persistence effects. |
| Second invocation of the existing change | The same **13 tests passed** again, with unchanged project-file hashes and the original dependency-manifest hash. This proves no local file churn for that exercise, not global exactly-once provider writes. |

The fixture metadata reports Python 3.11.4, ADK 2.8.0 and pytest 8.4.2. The existing
fixture suite used `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 PYTHONDONTWRITEBYTECODE=1
.venv/bin/python -m pytest -q -p no:cacheprovider`. The greenfield run used
`PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 .venv/bin/python -m pytest -q
-p no:cacheprovider test_preferences.py`; its repeat also disabled bytecode
writing. The greenfield runs passed in 0.04 and 0.03 seconds respectively.
The independent existing-project suite passed in 0.01 seconds and its repeat
in 0.02 seconds. The cloud-boundary inspector was run twice with identical
reports and no project changes. No proposed cloud command was executed.


### Limits of the forward evidence

The greenfield fixture implemented exact enum preferences in a deterministic
profile, not semantic retrieval; this was an intentional store-selection
outcome. SQLite locking/failure recovery, complete erasure and the generated
ADK tool adapter were not executed in that exercise. The existing fixture
assumed a trusted application principal and did not implement authentication.
Their passing tests verify the named local boundaries only. A consuming
application still needs its own authentication, SDK/Runner, real-provider and
hosted acceptance tests. The fixture implementations are evaluation artefacts,
not bundled production templates.
