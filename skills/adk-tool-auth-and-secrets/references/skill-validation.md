# Skill validation record — 15 September 2026

This records package checks, separate from the historical companion evidence.

## Environment

Codex desktop on macOS, Darwin 25.6.0 arm64; existing repository virtual environment with Python **3.11.4**, pytest **8.4.2**, PyYAML **6.0.3**, google-adk **2.8.0** and google-genai **2.19.0**. Installed versions were read from distribution metadata. No packages were installed or pins changed. The historical chapter campaign used different resolved versions; see [compatibility-and-evidence.md](compatibility-and-evidence.md).

The helper and adapter require only Python 3.11's standard library. The installed ADK/GenAI pair was used for one optional real event-shape assertion, not a live model call or a new orchestration acceptance run. Default Python **3.9.13** was also checked: the inspector exited 2 with `PYTHON_3_11_REQUIRED` rather than a missing-`tomllib` traceback.

## Package commands and actual results

Here `python` denotes the selected Python 3.11.4 interpreter. Commands were run from the package directory unless stated otherwise. `TARGET_PROJECT` was the optional current Chapter 9 checkout; `SKILL_VALIDATOR` was the host's official Skill Creator `quick_validate.py`, not a package dependency.

| Command/check | Result |
| --- | --- |
| `python -m pytest -q tests` | Exit 0; **24 passed**, including the installed ADK event-shape check |
| `python -I -S -m unittest discover -s tests -v` in a separate clean copy | Exit 0; **23 passed, 1 skipped**; only optional ADK check skipped because site packages were disabled |
| `python scripts/inspect_project.py --help` | Exit 0 |
| `python scripts/inspect_project.py . --dry-run` | Exit 0; complete read-only package inventory |
| `python scripts/inspect_project.py "$TARGET_PROJECT" --dry-run --expect-adk 2.8.0` | Exit 0; 49 candidate files, static pins matched; runtime and security explicitly not assessed |
| Same target with `--expect-adk 9.9.9` | Exit 3; mismatch reported without changing dependencies |
| Inspector with an absent project root | Exit 2; `INVALID_PROJECT_ROOT` |
| `python "$SKILL_VALIDATOR" .` | Exit 0; `Skill is valid!` |
| Frontmatter, folder/name, automatic activation, relative links, Python syntax and unfinished-marker checks | Passed across all 14 package files |
| Compare current companion files with the final campaign's SHA-256 manifest | All **37** fingerprinted source files still matched; historical evidence was not silently applied to changed source |

Unit tests exercise repeatable `--dry-run` inspection, private-file and dependency-URL canaries, prevention of target-code execution, symlink/size/traversal bounds and uncertain versions. Adapter tests exercise thought/non-public metadata exclusion, malformed event rejection, size/event/time bounds and later-invocation independence. An allowed-text canary deliberately remains visible: this proves the documented limit, not a redaction guarantee. No repository-wide formatter or linter configuration applied to this package; AST/compilation checks and behavioural tests supplied local static validation.

## Independent forward evaluations

Three independent Codex evaluators received only a clean package copy, synthetic fixture projects and realistic requests. They had no manuscript, prior findings or intended answers. The existing interpreter was available as a runtime; book source was not an input. External services and installation were excluded from these offline evaluations. Actual fixture changes and test output were reviewed, including preserved-input and repeat-invocation hashes.

| Scenario | Observed result and limit |
| --- | --- |
| Greenfield notes assistant; remote sign-in/cloud later | Created an injected-verifier boundary, owned sessions, operation permission and a tool without identity arguments. **16 unittest tests passed**. Preserved Python/ADK declarations and the supplied store. Real sign-in, ADK orchestration and persistent/distributed sessions remained explicitly unverified. |
| Customised notes tool, ADK pinned to 2.7.0, custom response envelope | Removed the model-selected user argument; scoped lookup to trusted context and projected final public text. Preserved `message`/`request_tag`, unittest conventions and the **2.7.0 pin**. **12 tests passed**, independently rerun successfully. Installed runtime was 2.8.0; actual 2.7.0 tool injection/orchestration was correctly reported unverified. |
| Calendar request without OAuth client, ADC or project | Produced a local access plan with identity, browser/account binding, custody, lifecycle and validation prerequisites. No credential fabrication or live-success claim. |
| Secret Manager/IAM plus two Gemini checks on synthetic inputs | Prepared reviewable proposed commands and ownership/cleanup gates, preserved the existing shared resource and two-send ceiling, and recorded unresolved real target/model/credential inputs. Paused external execution; zero sends, token operations or resources. Distinguished model smoke checks from tool acceptance. |
| Unrelated README title change | Changed only the heading to `Team Notes`; did not apply authentication guidance. |
| Second identical greenfield request | **No changes** across all five fixture files, verified by SHA-256; **16 tests passed again**. No duplicate boundary or test scaffolding. |

The greenfield evaluators ran `python -m unittest discover -s tests -v`; the customised evaluator ran `python -m unittest discover -v`. Their Python compilation checks also passed. A separate standard-library assertion script confirmed the plan's valid JSON, preserved original fields, empty creation ledger and two-send cap, plus the exact near-miss edit and unchanged repeat-invocation files.

## Claims this record does not make

These are offline package and coding-agent behaviour checks, not new live OAuth, Secret Manager, Firebase, managed authentication or hosted-deployment evidence. No paid model/provider calls, credential reads, cloud changes or deployments were performed for packaging. Historical six-workflow Gemini evidence remains labelled historical in the provenance reference. Other coding-agent products and operating systems were not smoke-tested; plain Markdown and a clean-copy test alone do not establish their behavioural compatibility.

Use [validation.md](validation.md) to reproduce checks. Static observations do not certify runtime authorisation, and public-text projection is not secret redaction.
