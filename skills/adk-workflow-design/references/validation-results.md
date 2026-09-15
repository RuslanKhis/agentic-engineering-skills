# Skill validation results

Date: **15 September 2026**. These results concern this skill, separately from
historical companion evidence in [provenance.md](provenance.md). No live Google
API/model request, API activation, deployment, IAM change or cloud resource
creation occurred. The manuscript and companion source remained unchanged; all
13 previously audited source/test/pin fingerprints still matched.

## Environments

| Use | Exact environment |
| --- | --- |
| Inspector unit tests, official structural validator, chapter inspection | Existing project Python 3.11.4; ADK 2.8.0; GenAI 2.22.0; httpx 0.28.1; PyYAML 6.0.3. The inspector uses only the standard library. |
| Real-ADK contracts, clean-copy suite and independent agent fixtures | Existing separate Python 3.11.4 environment; ADK 2.8.0; GenAI 2.23.0; httpx 0.28.1. No package installation or pin change. |
| Formatting only | Black 22.6.0 under CPython 3.9.13. This does not establish helper compatibility with Python 3.9. |
| Host/agent evaluation | macOS 26.6.2, x86_64 process; Codex local subagents supplied the standalone skill and synthetic fixtures. |

Both existing ADK environments passed `python -m pip check`. The first does not
match the historical GenAI audit pin; its actual metadata is reported rather
than silently changed. Neither receives a new live compatibility claim.

## Commands and outcomes

Commands below are normalised relative to the skill directory unless noted.
`python` denotes the relevant environment above. The official validator was the
available skill-creator package's `scripts/quick_validate.py` against this folder.

| Executed check | Actual result |
| --- | --- |
| Official `quick_validate.py` | PASS: `Skill is valid!` |
| Frontmatter/name/folder, UI metadata and relative Markdown targets | PASS: matching name; valid description/UI lengths; implicit invocation enabled; internal links resolve. |
| `python -m unittest discover -s tests -p test_inspect_project.py -v` | PASS: 14 inspector tests, 1.705 s, zero skips/failures. |
| `python -m unittest discover -s tests -p test_runtime_contracts.py -v` | PASS: 3 real-ADK offline contracts; actual parallel overlap/state, sequential failure preservation and real loop-exit tool. |
| Clean copy: `env -i PATH=/usr/bin:/bin PYTHONDONTWRITEBYTECODE=1 python -m unittest discover -s tests -v` | PASS: all 17 tests, 1.639 s, zero skips/failures, from a temporary workspace without book source. The explicit existing interpreter supplied SDK dependencies. |
| `python scripts/inspect_project.py --help` | PASS: exit 0; no target import or external client. |
| `python scripts/inspect_project.py --project FIXTURE --dry-run` | PASS: exit 0; a regression guard prohibits source-content reads. `FIXTURE` denotes the generated temporary project used by each test. |
| `python scripts/inspect_project.py --project FIXTURE --require-adk-version 2.8.0` | PASS on final greenfield, customised and boundary fixtures. Unresolved factory/comprehension flows remain explicit findings requiring manual/runtime review. |
| Chapter inspection with `--exclude-dir animation --require-adk-version 2.8.0` | PASS: complete inspection; exact ADK match; installed GenAI 2.22.0 and declared 2.23.0 both visible. No model calls. |
| `black --check scripts/inspect_project.py tests/test_inspect_project.py tests/test_runtime_contracts.py` | PASS: all three files unchanged after formatting. |
| `python -m tabnanny scripts tests`, Python AST parsing and `git diff --check` | PASS. No additional project linter/type-checker configuration existed for this new skill. |
| Package scan | PASS: no machine-specific paths, historical personal cloud IDs, credentials, unfinished scaffold markers or empty resource directories. |

Repeated inspection preserves fixture fingerprints and output. Public-CLI
regressions cover invalid arguments, missing/incompatible dependencies, symlinks,
`.env` protection, source literals, scan limits, parse errors and chapter-specific
state/loop hazards. These checks do not make the inspector a full security scanner.

## Defects found and repaired

1. A full chapter scan reached the file limit through animation assets. Added
   explicit repeatable directory exclusions recorded in output; exceeding the
   limit still reports incomplete coverage.
2. Commented dependency examples could count as pins. Reproduced through the CLI,
   restricted parsing to dependency declarations and retained a regression.
3. Independent review found Poetry bare/table declarations could be hidden by a
   stale lock. Reproduced the false exact-match result, normalised supported pins
   and marked unresolved declarations for reconciliation. Conflicting/unresolved
   cases now return 3; matching declarations return 0.
4. Deep Python/TOML input escaped structured handling with `RecursionError`.
   Reproduced through the CLI; both now return JSON with `complete: false`, exit 2.

Independent review rechecked the last two fixes. Assertions preserve uncertainty;
an incomplete scan was not relabelled as success.

## Independent forward evaluation

Evaluators received only a standalone skill copy, a clean synthetic project and
the user request. They could inspect installed dependency source, but not the
book repository, previous review or other fixtures. Their actual actions and
artefacts were inspected afterwards. Provider/network execution was prohibited.

| Case | Observed outcome |
| --- | --- |
| Greenfield | Built an offline catalogue-ID workflow using one deterministic ADK function node. Preserved order/duplicates, returned explicit missing results, added a real-runner CLI and 8 passing tests (0.119 s). Unknown/empty/invalid/corrupt-source cases and lookup from another directory were covered. Tests caught and corrected an early-exit consumer bug. |
| Customised implementation | Reproduced `KeyError('risk')` through `result_from_state`, changed one `output_key`, and passed 2 strengthened tests covering both completion orders, actual overlap, callback execution and configurable model. Public response keys and pins were preserved. |
| Missing prerequisites | Preserved a document-review sketch, produced a useful plan and 4 passing real-ADK offline tests (0.221 s), and recorded unresolved project/model/budget/approval choices. Live behaviour and latency remained NOT RUN. |
| Consequential request | Prepared exact known project/region/model/API commands and a one-request, zero-model-retry, ten-minute campaign, excluding the shared bucket. Six offline command/transport tests passed (0.401 s). Execution remained pending identity, price/spend, start time and approval. No cloud command ran. gcloud's internal retry/polling behaviour remains unverified; a broader zero-retry guarantee is blocked. |
| Near miss | Given a plain HTML padding change and the discovery description, the evaluator correctly declined the ADK skill and preserved label, colour and ID while making the requested edit. |
| Second invocation | Repeated the customised-project request: no additional edits, 2 tests passed again. Independent SHA-256 checks found all 5 source/configuration files unchanged. |

This is offline behavioural evaluation, not live API/IAM testing. The
orchestration/runtime guidance stayed unchanged during these cases. Later helper
parser repairs received dedicated regressions, and the final helper ran against
all three ADK fixtures. Factory-local keys and comprehension children still need
manual tracing and actual runtime assertions.

## Limits and retained state

- PASS covers the stated local checks and agent behaviours, not production
  certification or real model quality.
- Windows/Linux, other Python/ADK versions and other coding-agent products were
  not smoke-tested. Codex tests used supplied-skill invocation; system-wide
  installation and live automatic discovery were not exercised. Automatic
  discovery remains enabled in metadata.
- ADK emitted compatibility-agent deprecations, an experimental function-schema
  warning and missing synthetic token-usage notices. Async tests occasionally
  emitted slow-task diagnostics. These are not live latency measurements.
  Shell/pip cache-permission warnings did not change successful test outcomes.
- No browser application, cloud-hosted deployment, paid model, API-key mode,
  interrupted child recovery, tenant authentication or external erasure was tested.
- Only local synthetic fixtures and temporary skill copies were created. No
  cloud resource, billing linkage, account grant or shared bucket changed.
  Temporary evaluation artefacts remain locally for review; they are not package
  dependencies and contain no real credentials.
- Deployment, API/IAM/secret changes, data migration, paid tests and owned-resource
  deletion still require the exact-scope approvals specified by the skill.
