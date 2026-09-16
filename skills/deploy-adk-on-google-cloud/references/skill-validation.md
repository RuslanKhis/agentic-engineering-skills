# Validation of this skill package

This record concerns the portable skill and its offline helper, not another cloud campaign. Creation uses the existing repository environment without changing its packages. Historical Google Cloud evidence is described separately in [evidence.md](evidence.md).

## Environment

Local authoring environment: macOS 26.6.2 on arm64; Python 3.11.4 in the existing project virtual environment. Installed metadata was `google-adk==2.8.0`, `google-cloud-aiplatform==1.153.1`, `google-genai==2.19.0`, `fastapi==0.136.3`, `pydantic==2.13.4`, `uvicorn==0.49.0`, `SQLAlchemy==2.0.51`, `aiosqlite==0.22.1`, `httpx==0.28.1`, `pytest==8.4.2` and `PyYAML==6.0.3`. The Runtime fixture also used `a2a-sdk==0.3.26`. The helper itself uses only the standard library. This environment differs from the chapter's historical resolved integration libraries; no dependency-resolution or repeated live-integration claim is made.

The installed `adk deploy cloud_run --help` and `adk deploy agent_engine --help` both completed successfully and confirmed the recorded 2.8.0 CLI shapes. No authentication, deployment, model request or cloud resource mutation was performed to create this package.

## Reproducible checks

From the installed skill directory, use a Python 3.11+ interpreter:

```bash
python -B -m unittest discover -s tests -p 'test_inspect_project.py' -v
python scripts/inspect_project.py --help
python scripts/inspect_project.py --root . --dry-run
```

The skill's structural validator is supplied by the authoring environment, not required at runtime. Its checks are supplemented by relative-link resolution, frontmatter/metadata checks, code-fence parsing, secret-pattern inspection and independent forward testing. The source repository has no skill-specific formatter configuration; `ruff` was unavailable in the existing environment, and packages were not installed just to add one.

## Recorded results — 15 September 2026

| Check actually performed | Result |
| --- | --- |
| Skill-creator `quick_validate.py` on this folder | PASS, exit 0 |
| Bundled helper unittest suite, existing Python environment | 23 tests PASS |
| Helper `--help`, default inspection and `--dry-run` | PASS; identical non-mutating inspection behaviour |
| Offline `--require-baseline` on the chapter's Run, Runtime and GKE directories using the corresponding mode | All three exit 0; required direct pins match; no installed-version or cloud inference claim |
| Skill copied alone into a clean temporary directory; helper help, dry run and full suite repeated | PASS; 23 tests; no companion source dependency |
| Markdown links/frontmatter, Python AST, JSON examples and Bash `-n` on command fragments | PASS; commands were parsed, not deployed |
| Source snapshot targets and limited secret/private-path scan | PASS; 14 source targets present; scan is not a comprehensive security audit |
| Whitespace validation and original chapter changes | `git diff --check` PASS; original chapter code/manuscript unchanged |

The unit suite includes explicit project/account/quota scope on every planned command, the selected region on regional commands, refusal of partial/unsafe targets, no execution with missing tools, dry-run/repeat no-write checks, secret redaction, symlink/include bounds, pin conflicts and a simulated unsupported-Python refusal. That last case changes version metadata in a child process to test the guard; Python 3.10 itself was not run.

A manual regression probe initially demonstrated that a conflicting `-c constraints.txt` pin could be missed. The helper now inspects local constraints and refuses a conflicting required baseline; a constraints-only pin is not mistaken for a runtime dependency. Both cases are covered by the passing suite. No package version was changed.

## Forward-test cases

[forward-cases.json](../tests/forward-cases.json) contains six realistic requests and minimal synthetic fixtures. Copy the skill alone to a clean temporary location, materialise one case's files in a separate fixture directory, and give an evaluator only that skill, the fixture, the request and the offline side-effect boundary. The final case reuses the first case's completed output. The fixture project IDs, names and account are fictional and must never be used for live deployment.

The cases cover local Cloud Run preparation, a customised shared-GKE project on a different ADK pin, missing Runtime credentials/access, concrete approval-gated cloud commands, an unrelated spelling edit and a repeated invocation. Judge generated artefacts and actual commands; matching a prescribed answer is not a behavioural test.

All six cases passed independent forward evaluation. [forward-results.json](../tests/forward-results.json) records outcomes and raw evaluator-report hashes. Three fresh evaluators received only the copied skill, assigned fixture/request and offline execution boundary; an existing interpreter/package environment was supplied, without permission to inspect companion source. The parent checked the actual outputs and verified original-file preservation.

- Greenfield preparation produced a functioning API-only serving layer and seven passing tests with real ADK/FastAPI/session components and a fake model. Source exclusions, tool result, final grounded answer, explicit recall, HTTP negatives and local SQLite app recreation were exercised. A container was defined but not built.
- The shared-GKE review preserved ADK 2.7.0, `/ready`, names and pre-existing KSA/cluster ownership. Its version stayed unverified; no migration or replacement cluster was proposed.
- Missing Runtime access still allowed local planning and actual SDK packaging through fake provider boundaries. Literal unresolved target placeholders were correctly rejected by the helper with exit 2; no live target was invented.
- The consequential case prepared reviewable native-generated source and commands, with two passing offline packaging tests. Deployment and deletion stayed pending explicit approval.
- The near-miss changed only the requested spelling and did not activate the deployment workflow.
- The repeat passed the same seven tests and `pip check`, while preserving all 13 completed fixture files, previous report and staged-source hashes. This establishes local preparation idempotency, not new live lifecycle evidence.

Forward evaluators ran `python -m pip check` successfully in the supplied environment. Their native SDK generators printed deployment-like status text, but provider calls were replaced by fakes; those messages are not live evidence. The Runtime evaluator also found the SDK's conditional failure-cleanup branch, now described with its approval requirement in the Runtime reference. Existing SDK deprecation/experimental warnings and the deliberately injected model-failure traceback were reported without being represented as test failures.

Only the Codex environment used for these tests can have direct behavioural evidence here. Plain Markdown and an optional `agents/openai.yaml` support portability by design; other coding agents, Windows, other Python interpreters and real cloud execution of the newly generated adaptations remain untested.

## Depth recheck — 16 September 2026

The same existing environment and exact package versions listed above were rechecked and preserved. The Chapter 3 source tree was unchanged between its original skill provenance snapshot and HEAD `51b41e83cdf6adc8904d7039b283c292989203fc`. No manuscript or companion code was edited and no cloud deployment, resource mutation or paid test was performed. Public official provider documentation was consulted for IAP topology; that is not cloud integration evidence.

| Check actually performed | Result and scope |
| --- | --- |
| Skill-creator `quick_validate.py` | PASS |
| Updated inspector unittest suite | **27 tests PASS**; four added Python-pin/redaction/symlink/limit regressions, with repeat/no-write coverage extended |
| Entire skill copied alone into a fresh temporary directory | Same **27 tests PASS**, helper `--help` and `--dry-run` PASS; no companion-source dependency |
| Inspector `--dry-run --require-baseline` on Run, Runtime and GKE chapter directories | All exit 0; declaration evidence only |
| Installed Runtime generator with synthetic files and replaced Vertex client | **10 assertions PASS**: Python base, enterprise/hosting-location defaults, env-file precedence, dependency augmentation, basename ignore, symlink copying, extra-package boundary and captured source package list; zero provider requests |
| Production positive model-limit construction fragment | **8 local checks PASS**; this fragment check alone does not exercise the runner |
| Metadata, relative links, all code fences and Python/JSON files | PASS; nine Bash fragments parsed with `bash -n`, three Python fragments with AST, three JSON examples, and one YAML block as three documents. GKE KSA/selector/port/probe relationships checked locally. No deployment commands executed. |
| Source link targets, limited secret/private-path scan and whitespace | PASS; provenance targets exist in the stated local commit; scan is not a comprehensive security audit |

The added helper pin field reports declarations separately from the inspection interpreter and constraints; it neither chooses Python nor evaluates version compatibility. Its package baseline gate is unchanged.

### Additional independent forward evaluations

[recheck-cases.json](../tests/recheck-cases.json) supplies three realistic requests and complete synthetic inputs. Materialise one case in its own directory and copy the skill independently; give an evaluator only that skill, its assigned fixture/request and the stated offline boundary. Use the existing compatible interpreter without installing packages or giving access to companion sources. Assess actual file changes, commands and results. [recheck-results.json](../tests/recheck-results.json) records the outcomes, original-file preservation and report/instruction hashes.

All three fresh evaluators completed after an initial account-usage interruption. The parent inspected the resulting code/reports and checked the changes against the original fixtures. They were not given the intended answers.

| Request | Observed behaviour | Evidence |
| --- | --- | --- |
| Prepare an existing custom Run app's execution limit and review six-user/two-replica readiness | Replaced caller-controlled unlimited settings with a finite server-owned limit, refused request overrides and returned a controlled limit-exhaustion outcome. Traced unused model/session configuration and identified authentication, onboarding and shared-state blockers while preserving agent, tools and pins. | **22 local tests PASS** through FastAPI ASGI, actual ADK Runner/counter, original tool and session service; only the model was replaced. Exact exhaustion tested at 1, 3, 4 and 16 calls. No live IAM, container, browser or replica test. |
| Recover an HTTP-200 Runtime verification failure using saved evidence | Fixed NDJSON parsing and turn-specific routing/recall assertions; correlated invocation/call IDs and saved session receipts. Both original recordings passed, so neither accepted turn was resubmitted. | **26 local tests PASS**; malformed/partial/error/stale or mismatched evidence refused. Saved synthetic schemas, single-line SSE and lexical grounding checks only. |
| Review two late GKE cleanup blockers | Recognised the original-controller candidate as pending fresh proof, refused a descendant of an exact-object-only receipt, and kept the whole batch blocked with no new receipts or baseline changes. | **12 local tests PASS** against saved/mutated metadata; no cloud inventory, production receipt writer, deletion or atomic-commit integration was exercised. |

These are three new offline evaluations, separate from the six historical forward cases above. They demonstrate useful application of the deeper instructions, not a new claim that all proposed production features are implemented. Other coding-agent products, live execution of the generated adaptations and the production contracts in [production.md](production.md) remain outside this validation.
