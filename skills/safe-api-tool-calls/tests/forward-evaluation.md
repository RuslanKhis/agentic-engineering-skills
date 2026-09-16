# Skill validation — 15 September 2026

This records validation of this skill package, separately from the historical
chapter results in [compatibility](../references/compatibility.md). It is an
execution record, not an assurance that every future generated integration is
safe. The installed skill needs none of the original chapter files.

## Environment and method

The skill was copied into a clean temporary directory. Independent Codex desktop
subagents with fresh conversation context received only that copy, a synthetic
fixture project, a realistic request and access to an existing interpreter.
They were not given the expected implementation or the parent's test assertions.
No original chapter source was available as an evaluation input. The parent
reviewed the outputs and ran independent behavioural probes.

Tested host: **macOS 26.6.2 arm64**. Existing chapter virtual environment:
**Python 3.11.4**, **google-adk 2.8.0**, **httpx 0.28.1**,
**tenacity 9.1.4**, resolved **google-genai 2.22.0**, **PyYAML 6.0.3**.
No packages were installed or changed. The standalone inspection helper also
passed a clean-copy smoke test on native **Python 3.11.14**, using only its
standard library. This does not extend the ADK test matrix to that interpreter.

The agent environment tested was Codex desktop with an explicitly supplied
skill path. Host-level automatic discovery, installation and other coding-agent
products were not tested. The portable Markdown format alone is not behavioural
evidence for those environments.

## Executed package checks

In the commands below, `PY` denotes the existing interpreter, `SKILL_DIR` the
installed skill directory and `VALIDATOR` the available official skill-creator
`quick_validate.py`. Paths are parameterised to avoid tying this record to a
personal checkout. These are the command forms actually executed.

| Command or check | Actual result |
| --- | --- |
| `"$PY" -B "$VALIDATOR" "$SKILL_DIR"` | Exit 0: `Skill is valid!`. Frontmatter and naming accepted. |
| `"$PY" -B -m unittest discover -s "$SKILL_DIR/tests" -v` | **12 tests passed**, no skips, 2.218 seconds. |
| `"$PY" -B "$SKILL_DIR/scripts/inspect_project.py" --help` | Exit 0; documented project, dry-run and all four bound flags. |
| Helper `--project` with and without `--dry-run`, including a second invocation | Exit 0 on clean eligible fixtures; identical repeated output and unchanged target bytes/mtimes. Source execution marker was not created. |
| Helper invalid arguments, malformed/unreadable files, symlinks, size/depth/file/entry bounds | Expected exit 2 for invalid input; exit 1 and explicit partial-scan issues for incomplete inspection. |
| Helper redaction fixtures | Credential-like source strings and dependency URLs did not appear in stdout/stderr; `.env`, secret files and dependency directories were excluded. |
| Clean copied helper on Python 3.11.14 | Exit 0, repeat output identical, no target changes; no companion source required. |
| Helper against the chapter root | Exit 1: 23 files inspected; deep animation directories hit the depth limit. This was recorded as partial, not a clean scan. |
| Helper against the selected application source directory | Exit 0: four source files inspected, eight signals, no issues. |
| `"$PY" -B -m pip check` | `No broken requirements found.` A local pip-cache permission warning did not affect the check. |
| Python `compile()` over both packaged Python files | Passed without writing bytecode. |
| Local Markdown links, whitespace, folder/name match, unfinished markers, empty directories and personal infrastructure identifiers | Passed. All local links stay within this skill. |

The chapter defines `unittest`; it has no configured formatter, linter or type
checker. None was installed for this documentation/helper task, and no such
tool pass is claimed. Static checking here means syntax, frontmatter, links and
whitespace, not a full type or security analysis.

## Forward cases and observed behaviour

1. **Greenfield integration.** Request: add bounded status lookups and robust
   refunds while preserving the fixture's signatures and pins. The supplied
   contract permits retries of read HTTP 503; its refund commits before losing
   its response and has no idempotency facility. The agent created a service,
   documentation and tests. **20 tests passed in 0.333 seconds**, using
   `"$PY" -B -m unittest discover -s tests -v` from that fixture. Reads retry
   only 503, at most three times; deadlines include actual asynchronous waits.
   Refunds make one attempt and return an uncertain, non-retryable result.
   Exact amount handling and the absence of currency, approval and durable
   storage infrastructure are explicit. No ADK agent or database was invented.

2. **Existing customised integration.** Request: repair a flaky status function
   while preserving its public signature, result keys and pins. The starting
   function retried every exception and lacked a complete-operation deadline.
   The agent retained the scalar client timeout, three-attempt cap, 20 ms delay
   and `ok`/`payload`/`reason` keys. It added selective HTTP 503/ConnectTimeout
   retries, attempt/operation deadlines and cancellation propagation.
   **12 tests passed in 0.175 seconds**, using `"$PY" -B -m unittest -v`.
   Unrelated native timeouts and programming errors remained distinguishable.

3. **Missing prerequisites.** Request: prepare the safe API example for a live
   Gemini check. Only Python/dependency declarations and a synthetic project
   description were supplied. The helper returned exit 0 with two declaration
   files inspected. The agent reported the missing application, tests,
   client/session route and credentials; it did not treat declared pins as
   installed packages or claim live readiness. It requested the inputs needed
   to prepare a bounded live plan. No model call or setup operation ran.

4. **Consequential operation.** Request: prepare a Vertex activation step and
   its effects before any cloud change. A synthetic fixture specified the
   project, `global` runtime location, disabled `aiplatform.googleapis.com`, a
   120-second command bound and one permitted activation submission. The agent
   produced explicit `gcloud services list` / `gcloud services enable` commands
   with that target, distinguished project-wide activation from regional
   deployment, preserved an already-enabled baseline and required read-only
   reconciliation after an ambiguous submission. It stopped at the concrete
   plan pending credentials, a real authorised target and approval. An earlier,
   underspecified deployment request also stopped without inventing a platform
   or executable setup. These are plan-level observations; cloud execution and
   enforcement by a host approval system were not tested.

5. **Near miss.** Request: change a CSS heading colour to `#222`. The agent
   recognised the skill's UI-only exclusion, made the single requested CSS
   edit and did not impose the API safety workflow.

6. **Second invocation.** The greenfield request was repeated against the
   completed fixture. The agent reread the implementation and made no changes.
   Its **20 tests passed again in 0.372 seconds**. The parent independently
   compared SHA-256 hashes of all seven fixture files before and after: all
   matched. This checks repeat use of the skill, not durable provider
   deduplication across separate business operations.

## Independent behavioural probes

The parent loaded the generated service against the original local provider,
with socket connections blocked. One HTTP 503 followed by success produced
the correct status data in **two calls**. A refund that committed and lost its
response produced **one provider call and one side effect**, with
`outcome="unknown"` and `retryable=False`. Invalid `NaN` input produced no
additional provider call. This is the chapter-specific unsafe-replay test.

For the customised implementation, a separate adapter used real HTTPX
`AsyncClient` and `MockTransport`: 503 then 200 required two calls; HTTP 400
required one. Signature and result keys were preserved. A genuinely stalled
coroutine was cancelled by the total budget, and explicit caller cancellation
propagated. The caller-owned HTTPX client closed correctly. No network transport
or real provider was exercised.

Generated service SHA-256 identities for this evaluation:

- Greenfield: `8b773731afd470147937fa8ca7467f8d6277c9f1dab1ea2a95bdcd359e8181d2`.
- Customised: `99ebcd1a8661ef95a09f17827b74c81bb31323b56ad5963bd53921a73d9cdc58`.

These generated applications were disposable evaluation outputs, not bundled
production templates. The packaged CLI tests are self-contained and repeatable;
repeating the agent evaluation requires recreating the described fixtures and
issuing the requests to an agent.

The subsequent [retained evaluation cases](forward-cases.md) provide exact
inputs, requests and independent assertions for the implementation-depth
recheck. They extend the package without claiming to reconstruct this earlier
temporary evaluation exactly.

## Source verification and limits

The unchanged chapter suite was rerun with
`PYTHON_DOTENV_DISABLED=1 PYTHONDONTWRITEBYTECODE=1 "$PY" -B -m unittest discover -s tests -v`
from the chapter directory: **59 passed, no skips, in 3.601 seconds**. Its
HTTP/session tests use a scripted model and block socket connections. ADK
experimental confirmation/schema warnings remained. All 14 source hashes
matched the prior verification manifest; the manuscript was unchanged.
These tests recheck provenance and are not dependencies of this skill.

No paid model tests, real refunds, API activation, deployment, IAM/secret
mutation or cloud cleanup occurred in this skill task. Durable recovery,
concurrent workers, provider idempotency and production confirmation/session
support remain integration-specific implementation and validation work.
Historical live observations are described separately in the compatibility
reference and were not promoted into current live passes.
