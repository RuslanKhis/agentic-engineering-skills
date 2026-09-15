# Validation workflow

## Target application acceptance

Use the target's existing environment, fixtures, test runner and build commands. Keep normal tests offline by replacing external model/HTTP boundaries while retaining as much of the actual auth, session, adapter and event machinery as practical. A pure mock of the component under test proves little about its contract.

| Boundary | Minimum meaningful checks |
| --- | --- |
| Identity and session | Missing/invalid credential, unknown ID, other-user ID, unsafe ID; rejected requests make zero model/tool calls; chosen creation/resume semantics remain stable |
| JSON | Complete result schema, thought filtering, late reported error, empty result, controlled upstream error, response validation and timeout covering response body |
| Concurrency/deadlines | Lock waiting consumes the request budget; cancellation propagates; a timed-out submit is not automatically repeated |
| AG-UI translation | Partial text plus merged aggregate appears once; partial function arguments announce one confirmed call; exact result correlation; unknown/private tool data filtered |
| AG-UI lifecycle | Text and tools start/end in order; separate result IDs; safe run failure after visible text; no ordinary successful terminal after failure |
| BFF/browser | Agent identifier and tool name agree; runtime result schema validation; safe errors; controls recover; subscriptions clean up; state remains bounded |
| Managed execution | Retained SDK owner; typed absent metadata vs permission/transport error; exact owner/resource checks; no model retry on failed query; explicit SSE run config |

Add production acceptance tests from [production.md](production.md) only for promised features. A single-process lock test is not distributed fencing evidence; a protocol-order test is not authorisation evidence.

## Read-only helper checks

From the installed skill directory, run both helpers' `--help`, then normal and `--dry-run` forms against synthetic fixtures. Inspect exit codes and JSON reports; repeat them and confirm no fixture or skill content changes. Invalid paths, oversize input and unsupported profiles must fail clearly without dumping payloads or credentials.

```text
python -m unittest discover -s tests -p 'test_*.py'
python scripts/inspect_project.py --help
python scripts/check_agui_trace.py --help
```

`check_agui_trace.py` consumes one JSON event per nonempty line, not raw SSE framing or provider events. Feed it the explicit AG-UI start/content/end profile. It validates only a local trace: success means the recorded event shape/order passed the selected expectation, not that the tool or model executed correctly. Treat a valid failed run differently from malformed protocol and from a successful run. Consult `--help` for outcome expectations, supported ancillary events and bounds.

To construct a safe trace from an application, replace message/tool text with synthetic data while preserving event types, order, IDs and argument-fragment boundaries. Validate actual payload schemas separately in controlled tests. Do not save production prompts merely to exercise this helper.

## Browser and authorised live checks

Test a synthetic successful message and a synthetic failure through the actual gateway, BFF and browser when available. For a displayed tool, inspect its structured result as well as the prose. If claiming managed persistence, restart only the local gateway, retain the conversation ID and verify recall from remote history without resending that history.

Offline browser checks and a real Gemini call establish different facts. A model catalogue/metadata response is not an inference test. A successful SDK request is not evidence that the browser displayed it. Record live request count, actual tool outcome, target/version, bounded execution and cleanup separately.

Before paid calls, use `SKILL.md`'s explicit approval process and a disposable isolated target. Count failed attempts and uncertain submissions. Do not retry to hide failures or improve reported latency. Do not create resources just to complete a skill packaging test.

## Portability and independent forward tests

Copy the completed skill to a clean temporary directory outside the companion. Run helper tests there with both the established project interpreter and a clean standard-library interpreter if available. Check all internal links, valid YAML/name, empty directories, unfinished scaffolds, personal paths, credentials and source-tree dependencies. Retain the MIT notice with redistributed material.

Give an independent evaluator only this skill, a clean fixture and a realistic request. Keep expected answers out of its prompt. Exercise these cases:

1. A greenfield app needs a local ADK JSON endpoint and browser helper, with offline tests.
2. An existing customised route needs an AG-UI or JSON correction while preserving its auth and API shape.
3. The project lacks cloud credentials or some packages; useful local work should proceed with specific remaining prerequisites.
4. A deployment/API/IAM/deletion request has not approved exact targets; preparation should produce a reviewable proposal and pause at that boundary.
5. A near-miss asks only for ordinary UI styling; the skill should not introduce an agent integration.
6. A second invocation targets the evaluator's previous output; it should reuse it without duplicate routes, dependencies or external operations.

Review actual artefacts and commands, not just the evaluator's confidence. Fix observed defects narrowly, rerun affected checks, and record the results below. Evaluation prompts can mention hypothetical project names; none is a live target or implicit approval.

## Evidence record

Historical companion results and their limitations are in [provenance.md](provenance.md). The following checks were run on **15 September 2026**, on macOS 26.6.2 arm64 with CPython 3.11.4. Tests of the helpers remain offline and do not refresh the historical cloud campaign.

| Command or check | Actual result |
| --- | --- |
| Available `quick_validate.py` against this skill | PASS. Its older frontmatter allowlist excludes the standard optional `compatibility` field, so compatibility is documented in a reference rather than that optional field. |
| `python -B -m unittest discover -s tests -p 'test_*.py'` in the established project environment | 53 passed: 27 inspector tests and 26 trace tests. |
| Same suite after copying the skill outside the repository, with `python -I -S -B -m unittest discover` | 53 passed with site packages disabled; no companion, ADK installation or book access required. |
| Same detached suite in a fresh `venv --without-pip`, using `python -I -B -m unittest discover` | 53 passed with no third-party packages installed, including subprocess CLI checks. |
| Both scripts' `--help`, normal and `--dry-run` invocations | PASS. Repeated dry runs preserved fixture contents and produced the same report. |
| Inspector on the current companion, including `--mode managed-agui --require-tested-stack` | Exit 0; four manifests, two lockfiles and all five relevant invoking-interpreter pins matched. No credentials or package-manager commands were run. |
| Valid synthetic tool/text trace | Exit 0 in normal and dry-run modes. |
| Answer followed by `RUN_ERROR` | Exit 3 under the default success expectation; exit 0 with `--expect-outcome error`. A failed run was not labelled successful. |
| Actual companion translator and installed AG-UI encoder, with synthetic provider events | One confirmed tool call despite an earlier partial call; partial `Bill` + `ing.` plus aggregate `Billing.` displayed `Billing.` once; the ten encoded events passed the new checker. No provider invocation. |
| Current companion's focused HTTP, translator, session, SDK-lifetime and streaming regressions | 62 passed, six existing SDK/ADK warnings. These overlap historical suites and must not be added to their counts. |
| YAML, name, metadata, automatic discovery policy and relative file links | PASS. |
| Python AST parsing, whitespace/final-newline checks, scaffold/personal-path scan | PASS. No repository Python formatter or Ruff installation was available; syntax and explicit formatting checks were used, without claiming a full lint/type check. |
| Source integrity | All 77 recorded companion file hashes matched the final September 13 manifest. The skill creation did not change the companion or manuscript. |

The focused companion command selected `test_backend_http.py`, `test_runtime_translator.py`, `test_runtime_client_lifetime.py`, `test_runtime_model_streaming.py`, `test_runtime_session_metadata.py`, `test_runtime_session_roundtrips.py`, `test_runtime_chapter3_contract.py` and `test_adk_api_events.py` through the existing pytest environment. Exact integration versions are listed in [compatibility.md](compatibility.md).

### Independent forward-test results

Two independent Codex subagents received detached skill copies, synthetic fixture projects and the user requests below. They did not receive the manuscript, companion source or expected answers. They could use the existing interpreter only as a dependency runtime. Network access, installation and external mutations were outside the evaluation scope. The evaluators exercised a 51-test snapshot; final input-safety hardening added two inspector regressions, with the final 53-test package checked separately above. The task instructions and mode references were unchanged.

| Case | Actual observed result |
| --- | --- |
| Greenfield JSON integration | Created a FastAPI route, dependency-free browser helper and tests while retaining the original agent and dependency pins. 31 Python tests and nine Node tests passed; one test used the actual ADK Runner and original tool with only the model replaced. Authentication remained explicitly fail-closed pending a real verifier. |
| Existing customised route | Changed the existing `/v2/assist` collector and added seven passing HTTP tests. Preserved the request/response contract, auth dependency, React choice and pnpm declaration. A late reported error remained failed even if another final-looking answer followed. |
| Missing prerequisites and older pins | Preserved ADK 1.16.0. Inspected installed candidate metadata and found `ag-ui-adk 0.7.0` requires ADK ≥1.28.1 and <3.0.0. Prepared the connection plan and two passing synthetic success/error traces without installing an incompatible adapter or claiming that CopilotKit was connected. |
| Consequential request with unknown targets | Prepared an intent record, local preflight and deployment/cutover plan; three offline tests passed. The incomplete preflight returned expected exit 2. Requested the missing exact targets and separate deletion confirmation; no cloud command ran and no inventory was assumed empty. |
| Styling-only near miss | Changed only the requested button styling for that request and explicitly did not use the integration skill. No backend, dependency or agent work was introduced by the styling request. |
| Second invocation | Reused the greenfield implementation. Fresh 31-test Python and nine-test Node runs passed again; SHA-256 comparison confirmed zero fixture file changes. |

The greenfield evaluator's first run caught a cancellation bug in its generated disconnect polling. It corrected that code and reran the affected tests before the successful result. This demonstrates the validation workflow's value; it is not evidence that every generated implementation is correct on its first attempt.

Forward tests used CPython 3.11.4, FastAPI 0.141.1, ADK 2.8.0, GenAI 2.19.0, Pydantic 2.13.5, HTTPX 0.28.1, pytest 9.1.1, pytest-asyncio 1.4.0 and Node 18.20.4. The older fixture's declared ADK 1.16.0 was assessed, not installed or executed. Browser-helper tests ran under Node; a live browser UI was not created or tested in these fixtures.

This is an explicit-path Codex behavioural smoke test, not a test of automatic installation/discovery in every client. No Claude Code, Gemini CLI, Cursor, Linux or Windows smoke test was performed. No fresh cloud deployment, inference, API activation, production identity, distributed ownership, replay or human-approval service was tested during skill creation.
