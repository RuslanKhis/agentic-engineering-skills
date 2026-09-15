# Validate the selected behaviour

Use existing test tools and fresh synthetic fixtures. Inspect commands before
execution: a repository's “test” script may deploy or call a paid model. Model
substitutes belong at the external boundary, preserving in-project orchestration,
tools, callbacks and state. Prohibit network access in offline tests and make an
unexpected model request fail rather than silently returning a generic answer.

| Mode | Required meaningful cases when that behaviour changes |
| --- | --- |
| Sequential | Actual writer output reaches reviewer; exact order; reviewer failure propagates and preserves completed state without an automatic replay. |
| Parallel | A barrier requires both branches to start; distinct populated results survive; collisions or explicit merge are tested. |
| Loop | Early approval invokes the real exit tool and skips revision; exhaustion terminates; count continuations/attempts and assert the intended final artefact/status. |
| Graph | Assert the real typed node value reaches the consumer; simulated values are labelled; a deterministic node is not mistaken for an offline full workflow. |
| Dynamic | Empty, scalar/list and repeated-ID contracts; actual child orchestration; populated independent sessions where partitioning is claimed. |
| Callback/policy | Order at the real boundary; `None` passthrough; substitutes prevent the underlying action; denied repeat attempts stay denied; authorised controls work. |
| Runtime/UI | Entire event stream consumed or explicitly cancelled; selected output is correct; actual process restart if durability is claimed; failures visible; partial text differs from final commits. |

Use the real HTTP/UI route when supplied. Assert data, not only a health endpoint.
Measure from browser Submit and keep cold/warm and streaming settings explicit.
Actual paused-child recovery, tenant auth, external erasure and deployment are
NOT RUN unless independently exercised. Two session IDs in an unauthenticated
server do not prove caller authorisation or cross-tenant security.

## Bundled local checks

From the installed skill folder, with Python 3.11 or later:

```bash
python -m unittest discover -s tests -p 'test_inspect_project.py' -v
```

The optional real-ADK contract tests need the recorded ADK dependencies already
available in the selected environment; they do not install them:

```bash
python -m unittest discover -s tests -p 'test_runtime_contracts.py' -v
```

They substitute Gemini at its boundary and block network access. They exercise
real parallel scheduling/state and loop exit behaviour, not real Gemini quality.
Their explicit version gate fails on an unsupported SDK instead of silently
skipping tests. See [compatibility.md](compatibility.md) for versions and
[validation-results.md](validation-results.md) for the actual creation-time checks.

## Completion report

Report the selected pattern and result contract, changed files, commands, exact
installed/resolved versions and relevant configuration without credentials.
Give individual PASS/FAIL/BLOCKED/NOT RUN/N/A results for applicable offline,
live, browser, latency and cleanup gates. Include warnings, skipped tests,
source-vs-installed version differences and unresolved prerequisites.

Distinguish new target-project results, historical evidence and production advice.
State remaining manual steps and whether any owned resources remain. A successful
standalone component is not evidence of a combined deployed application.

For skill maintenance, also forward-test selection and actual use on a clean
greenfield request, a customised project, missing prerequisites, a consequential
request, a near miss and a second invocation. Record observed actions/artifacts;
a prose checklist alone does not establish behavioural portability.
