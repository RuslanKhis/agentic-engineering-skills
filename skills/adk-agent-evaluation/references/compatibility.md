# Compatibility and version checks

Read this before adding ADK-dependent code, selecting an evaluation interface, or interpreting an old result. Preserve the target project's package manager and pinned dependencies. Do not change Python, ADK, models or regions simply to reproduce the historical example.

## Historical integration environment

The following versions describe the **13 September 2026 companion verification**, not a required installation or a claim about the latest release:

| Component | Recorded version or setting |
| --- | --- |
| Python | CPython 3.11.4 |
| Google ADK | `google-adk==2.8.0`, evaluation dependencies installed |
| GenAI SDK | `google-genai==2.23.0` |
| Vertex SDK | `google-cloud-aiplatform==2.1.0` |
| Test runner | `pytest==9.1.1`, `pytest-asyncio==1.4.0` |
| Supporting packages | `python-dotenv==1.2.3`, `PyYAML==6.0.3` |
| Runtime | Local Python processes and ADK Web; Vertex inference and managed scoring |
| Agent/simulator | `gemini-3.5-flash`, `global`; synthetic in-memory business data |

The recorded dependency resolution contained 113 distributions. It is an environment snapshot, not a hash-locked installer. A dated scan retained an accepted NLTK 3.10.3 advisory; acceptance was not a patch or a clean scan. Review the target's current dependency policy and advisory state instead of installing this archived resolution unquestioningly.

New skill-helper, clean-workspace and forward-test results belong in [validation.md](validation.md). Their interpreter and results are separate from this historical live integration. A standard-library helper passing locally establishes neither ADK runtime compatibility nor provider access. No new live compatibility claim follows from packaging this skill.

## Inspect the target before changing it

1. Read dependency declarations and lockfiles, test configuration, agent construction, callback registration, session identity and external client boundaries. Record both declared and installed versions using the project's existing interpreter. Distribution metadata inspection does not require importing the application or creating a provider client.
2. Confirm the installed ADK's public interfaces used by the proposed change: `BaseLlm`, `Runner`, model/tool callbacks, invocation context/state, evaluation configuration models, CSV output and conformance commands. Prefer installed source and version-matched official documentation.
3. Validate fixtures with that version's `EvalSet` and `EvalConfig` models. Exercise a real Runner with only the external model boundary replaced before claiming an adapter works. For HTTP changes, use the real application routes as a separate check.
4. If the target version differs, continue version-independent inspection and planning. Do not assume that 2.x schemas or callbacks are interchangeable. When an interface is incompatible, report the exact mismatch and stop dependent execution; propose a narrow adapter or explicit dependency decision rather than silently upgrading or downgrading.

## Version-sensitive boundaries

| Surface | Historical behaviour to recheck in the target |
| --- | --- |
| Trajectory metrics | `EXACT`, `IN_ORDER` and `ANY_ORDER` compare arguments as well as names. Relaxed ordering permits extra calls; it does not classify extra mutations as safe. |
| Result aggregation | `AgentEvaluator` can return successfully while individual repeated-trial CSV rows fail. Retain expected case/metric counts, statuses and trial provenance; CSV row order is not a reliable repetition identifier. |
| State and callbacks | ADK `temp:` state is invocation-scoped; do not treat it as a normal dict with `pop()`. A receipt callback must coexist with existing callbacks and consume only trusted current-invocation tool outcomes. |
| Provider selection | In the verified SDK route, a nonempty `GOOGLE_API_KEY` could select an unintended authentication path. Vertex ADC commands used a scoped blank-key override and `GOOGLE_GENAI_USE_ENTERPRISE=true`. Verify the target SDK's selector; do not delete stored credentials or assume CLI login establishes Python ADC. |
| Managed evaluation | Agent, simulator and scorer have distinct settings, access and usage. A simulator invocation limit does not cap model/tool work inside a turn. Successful pytest capture did not retain exact managed scores. Arrange explicit export when needed. |
| Deadlines | Synchronous grading can block an async timeout. Use a parent-owned process deadline where required, and verify worker termination and reaping on the target OS. Forced termination may leave incomplete evidence. |
| Conformance | The tested 2.8.0 workflow loaded recording and replay plugins separately, selected nonstreaming replay and checked a nonzero case count. Replay can execute ordinary tools while supplying recorded responses; it is not automatically network-isolated. |

These behaviours guide targeted checks, not mandatory rewrites of unrelated projects. Exact live permissions, current model availability, pricing and deployment compatibility require fresh evidence and approval for any billable or consequential operation.
