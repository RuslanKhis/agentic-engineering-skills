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
