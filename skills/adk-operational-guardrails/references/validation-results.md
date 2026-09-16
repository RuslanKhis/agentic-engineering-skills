# Validation records

## Baseline — 15 September 2026

The skill was developed and tested locally on macOS 26.6.2 arm64 with CPython 3.11.4. Current project virtual environment: `google-adk==2.8.0`, `google-genai==2.19.0`, `google-cloud-pubsub==2.39.0`, `google-api-python-client==2.197.0`, `PyYAML==6.0.3`. No dependency versions were changed. Historical live evidence used `google-genai==2.23.0` and is recorded separately in [compatibility](compatibility.md).

## Commands and actual results

Commands below use the selected project interpreter, abbreviated as `python`, from the skill directory unless another working directory is stated. No dependencies were installed.

| Command/check | Actual result |
| --- | --- |
| Installed official `quick_validate.py` against `skills/adk-operational-guardrails` | PASS, exit 0: “Skill is valid!” |
| `python -m unittest discover -s tests -p 'test_*.py' -v` | 29 passed, zero failures/skips: 13 inspector tests and 16 guard tests |
| `python -m unittest discover -s tests -p adk_boundary.py -v` | 4 passed, zero failures/skips; real ADK runner, scripted model, no provider |
| `python scripts/inspect_project.py --help` | Exit 0; argument and dry-run help displayed |
| `python scripts/inspect_project.py --project . --dry-run --require-adk 2.8.0` | Exit 0 in the clean copied skill; exact installed ADK match |
| Inspector on the companion runtime directory with `--dry-run --require-adk 2.8.0` | Exit 0; relevant runtime, budget, payment and usage hints found |
| Inspector on the whole chapter | Exit 1, explicit file-count limit caused by animation assets; not represented as complete |
| `python -m pip check` | Exit 0: no broken requirements; local pip-cache permission warning only |
| Python AST parsing, whitespace/frontmatter/naming/link/scaffold checks | PASS; all 5 Python files parse; 24 relative Markdown links resolve; 17 packaged files, no empty scaffolds or embedded credentials/personal resource identifiers |
| SHA-256 comparison with latest companion source manifest | All 27 source files match; no companion source or manuscript edits |

The guard tests prove admission occurs before the counted effect, equivalent terminal repeats execute once, valid reads can repeat, identical in-flight calls block, uncertain/successful writes are not blindly repeated, deadlines include idle time, late results are rejected, and errors/configuration validation do not expose arguments. They do not prove remote cancellation or durable business idempotency.

The ADK fixture separately proves model-call exhaustion, terminal-repeat prevention at actual tool execution, a per-tool parallel capacity bound and an outer timeout before the first model event. ADK emits expected cancellation/error logs and an experimental function-schema warning on these negative paths. Those are not hidden skips.

## Clean copy and independence

Copied the entire skill to a fresh temporary directory without the chapter, manuscript, source checkout or credentials. Ran both suites, inspector help and dry-run there using only the existing interpreter's installed packages. Results: **29 tests passed in 1.603s, four ADK tests passed in 1.463s**, both CLI checks exit 0. Credential variables were removed from the child environment, dotenv loading disabled and ADC pointed at an absent path. The optional ADK suite still requires its stated installed dependency baseline; the standard-library suite does not.

Two independent Codex agents received only the copied skill, clean fixture projects and realistic requests. They could edit those fixtures and run local checks, with internet/cloud operations prohibited. The fixtures and raw working logs were kept in temporary evaluation directories, not added as companion code or installation dependencies.

| Forward case | Observed result |
| --- | --- |
| Greenfield support starter, no credentials | Implemented an actual ADK runner with a scripted model, three-model/two-tool bounds, a 0.15-second cooperative invocation deadline and deterministic no-payment review text. Final 13 offline tests passed, no skips. |
| Existing custom implementation | Reproduced two failing terminal-retry regressions, then fixed one condition. All six support tests passed while preserving public response types, refund threshold 75 and signatures. |
| Missing provider credentials/shared store | Completed a two-instance audit identifying absent admission, durable review and trusted identity; did not claim distributed or live success. |
| Consequential cloud preparation | Produced an offline resource/design plan with unresolved project/region explicit; deferred exact live commands and approval until targets were selected. Zero external mutations. This tests decision behaviour under an offline restriction, not actual IAM enforcement. |
| Unrelated single HTTP GET | Declined this ADK skill and used an ordinary HTTP-client workflow. Five separate offline weather tests passed; combined custom fixture suite passed 11 tests. |
| Second invocation | Adapted the existing greenfield files rather than duplicating the project; no files added/removed and pins unchanged. Two consecutive review invocations reused one local review ID/record and reported no payment. Startup preparation also remained idempotent. |

## Observed failures and resulting corrections

- The structural validator rejected top-level `compatibility`; moved that information into supported `metadata` and the compatibility reference. Final validator passes.
- The first optional ADK cap test hit a one-second incidental test timeout during cold framework setup. Increased only the non-deadline fixture allowance to ten seconds; the dedicated 20ms stalled-model deadline assertion remains. Four integration tests then passed. This is a test-fixture correction, not evidence for a production latency claim.
- The greenfield trial initially failed from cold SDK imports and a test searching descriptions rather than schema properties. Its first workaround imported private workflow/provider modules. Review rejected that coupling. Added guidance to [runtime bounds](runtime-bounds.md) about public startup preparation, unchanged invocation limits and honest cold-start scope; the second pass removed private eager imports and used a public runner callback that dispatches zero model/tool work during preparation.

The final greenfield cold CLI checks succeeded, but full process times were 3.363s and 1.908s, explicitly including imports/startup. Separate prepared invocations took 0.0157s and 0.0055s; these small offline observations do not establish real-model latency. No 150ms cold-process guarantee is claimed.

## Limits and external authority

Smoke-tested a Codex desktop agent workflow with the skill explicitly supplied by path. Automatic selection/installation and other coding-agent products were not smoke-tested; plain Markdown portability is a format property, not proof of behavioural compatibility everywhere. Optional OpenAI metadata leaves implicit invocation enabled by default.

No paid model call, cloud mutation, deployment, IAM change, secret creation, commit or publication was performed. Shared reservations, durable review/outbox, actual human delivery, payment execution, provider reconciliation, billing notification deployment and managed cleanup are production guidance, not services delivered by this skill. Cloud mutations, billable/destructive testing and owned-resource cleanup require the explicit, scoped confirmation described in SKILL.md. Local test success is not a hard spending cap or an audit of a live project.

## Depth review — 16 September 2026

Expanded the conditional references after re-reading the manuscript, source, original failures, corrected campaigns and cleanup evidence. No executable, dependency, chapter source or manuscript was changed. New references cover service integration/lifecycle and bounded live campaigns; the existing references now give more concrete state, transaction, crash-recovery, traffic, accounting and testing decisions.

### Fresh local validation

Used the same CPython 3.11.4/macOS 26.6.2 arm64 environment and exact package versions recorded above, without installation or pin changes. Copied the complete skill to a new temporary directory without companion sources or credentials. Removed credential variables from the child environment, disabled dotenv/telemetry and pointed ADC at an absent file.

| Check | Actual result |
| --- | --- |
| Official `quick_validate.py` | PASS: “Skill is valid!” |
| `python -m unittest discover -s tests -p 'test_*.py' -v` | 29 passed in 0.958s, no failures or skips |
| `python -m unittest discover -s tests -p adk_boundary.py -v` | 4 passed in 1.165s, no failures or skips; real ADK, fake model |
| Inspector help and clean-copy `--project . --dry-run --require-adk 2.8.0` | Both exit 0; the latter intentionally checks the skill as a helper smoke test, not a target application |
| `python -m pip check` | Exit 0; no broken requirements |
| Final structure, links, AST, whitespace and sensitive/scaffold-pattern scan | 19 packaged files, 5 Python files parse, 34 relative Markdown links resolve; no errors |
| Companion source manifest | All 27 SHA-256 hashes still match |

### Fresh forward exercises

Two fresh evaluators received only isolated skill copies, synthetic fixtures and requests, with provider/cloud execution prohibited. They did not receive the original chapter or conversation as an answer source.

| Exercise | Observed result and boundary |
| --- | --- |
| Three replicas, two workers each; existing service adapter | Evaluator produced 16 offline defect-reproduction tests, including two real-ADK/fake-model cases with socket connections blocked. Maintainer inspected and reran them: 16 passed in 2.450s. Passing here confirms deliberately flawed fixture behaviour, not service readiness. |
| Cleanup gaps and a new campaign across two servers plus CLI | Evaluator produced an actionable audit and proposed 12-submission/24-attempt/30-minute envelope. It preserved retained storage, denied/disabled inventories, pagination, unresolved activation and nonfinal billing as incomplete evidence; required one shared ledger and a current estimate before approval. Only static inspection and fixture-integrity checks ran; no application or live tests were claimed. |

The service reproductions confirmed lost final-event/tail usage, per-turn counter reset, tenant-key collision, duplicate/missing usage problems, unbounded waiting, absent outer timeout, empty-stream success and unsupported payment prose. A real ADK final response carrying 17 tokens left the fixture's counter at zero; repeated terminal tool failure executed twice. Six separate worker processes each admitted four requests and started with empty counters, establishing the scope problem and potential aggregate capacity of 24—not a measured simultaneous fleet peak. Early iterator exit also emitted context-detachment errors. These findings reinforce the same-task iterator cleanup and complete-consumption guidance.

The service evaluator supplied tests and intermediate findings but did not complete its final narrative report. The maintainer completed the test review and rerun; no independent remediation pass or deployed-service result is claimed. Temporary fixtures are evaluation evidence, not additional skill dependencies or production implementations.

### Corrections from these exercises

- Corrected the validation command to inspect `"$PROJECT_ROOT"`, distinguishing target application tests from bundled skill tests. Running `--project .` from the skill folder is now explicitly a helper smoke test.
- Added an interpreter fallback for source-free fixtures and a warning that a successful scan with zero relevant files establishes no application coverage. The inspector's existing JSON schema remains unchanged.
- Added concrete coverage allocation, admission/closeout timing and current-price worksheet guidance. Kept illustrative numbers separate from authority; no turnkey campaign ledger or current monetary estimate is claimed supplied.
- Clarified operation-key granularity for legitimate repeated partial refunds and Cloud Run's attached runtime identity rather than shipped credential files.

Final documentation-only corrections were structurally checked after the test run; executable files did not change. No paid model calls, deployment, resource creation/deletion, credential changes, commit or push occurred in this review. Production recommendations remain acceptance requirements until implemented and exercised in the target system.
