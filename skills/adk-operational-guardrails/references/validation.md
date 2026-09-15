# Validate the boundary that matters

Read when selecting tests for implementation, review, a version change or a paid campaign. Use the target's testing conventions. A positive wrapper return or scripted final answer does not prove a side effect was prevented or a provider succeeded.

## Local checks

From the installed skill folder, using the selected project interpreter:

```bash
python scripts/inspect_project.py --help
python scripts/inspect_project.py --project . --dry-run
python -m unittest discover -s tests -p 'test_*.py' -v
```

The inspector is read-only in ordinary and dry-run modes; dry-run is not a cloud connectivity check. The asset is an importable module, so it has no CLI or deployment mode. The test suite needs no model credentials. Review test imports before running the target project's separate integration suites, and block network boundaries for deterministic tests.

An optional [ADK integration fixture](../tests/adk_boundary.py) uses the actual runner and a fake model with ADK 2.8.0. In an existing environment with that pin, run `python -m unittest discover -s tests -p adk_boundary.py -v`. Other pins fail clearly and require adaptation; the fixture never installs dependencies. This test demonstrates terminal-repeat prevention, model-call exhaustion, per-tool parallel admission and the separate outer deadline. Its batch contract admits up to remaining capacity; the historical companion instead rejects an excessive batch as a whole.

## Select acceptance cases by mode

| Mode | Required observable evidence |
| --- | --- |
| Runtime | Side-effect counter unchanged after blocked call; legitimate read repeat succeeds; parallel calls cannot bypass cap; model that never yields is interrupted by the outer deadline; exhausted model-call budget triggers static stop; iterator cleanup completes |
| Accounting | Already-spent usage charged to every scope despite rejection; same session accumulates; a different tenant cannot reuse identity; exhausted allowance means zero model dispatch; duplicate/partial/missing usage handled explicitly |
| Shared reservations | Concurrent admission is atomic; conflicting request IDs rejected; settlement is once-only; crash/late-usage/expiry recovery tested with actual storage semantics |
| Review | Pending retry returns same durable operation; unauthorised reviewer and forged identity cause zero writes; concurrent delivery executes once; timeout persists unknown outcome and reconciles; UI distinguishes approval from completion |
| Cost policy | Kill switch prevents new dispatch; invalid/untrusted/stale billing events cannot reduce restrictions; intentional reset works; read/dry-run causes no cloud mutation; accepted asynchronous operations are reconciled |

For ADK changes, instantiate the installed real runner/session service with a scripted `BaseLlm` double. Return real `LlmResponse`/function-call objects and observe the registered tool's actual executions. Test parallel calls and the next serialised model request after tool execution. Avoid hand-built event lists as the sole proof of framework ordering. Keep event iteration and closure in the same async task.

Test the actual web/API/CLI path or inspect its wiring and explicitly mark it unverified. Ensure a framework development UI has not bypassed an application wrapper. After a shared-tool or instruction correction, a live test of one model/path does not establish another model/path; list each affected path separately.

## Optional live campaign, only with approval

Use synthetic data and an isolated target. Record exact identity/project/region, models, endpoints, operation scope, submission and provider-attempt ceilings, time window, estimated cost, allowance, stop conditions and cleanup ownership. Count attempts before HTTP, including failures, streaming and SDK retries. Keep the ledger separate from demo budgets. Stop when a limit or unexpected configuration appears; an additional retest needs authorisation if it exceeds the agreed envelope.

Observe tool results, subsequent model requests where safely instrumented, final user-visible claims and actual provider state. Distinguish model success from mock queue delivery. Keep prompts, tool arguments, customer data and credentials out of public telemetry. Use an allowlist of safe metadata.

If latency matters, measure from submission to meaningful content and final completion separately, identify cold/warm and streaming settings, and preserve failures. A spinner is not an answer, a manual observation gap is not exact latency, and a few samples do not establish p95. Latency work is optional unless requested; do not extend paid testing to manufacture a pass.

## Completion evidence

Report exact commands, versions, passed/failed/skipped counts and remaining manual steps. Mark each claim as current offline, historical live, current live, mocked or unverified production design. Record source identity where possible. Any authorised cleanup must independently confirm removal of owned resources and preserve existing resources; absence of created resources makes lifecycle testing not applicable, not passed.

Skill maintainers: run the official structural validator, test every helper's help/dry-run, check internal links/frontmatter/unfinished scaffold text, copy the whole skill to a clean temporary workspace and exercise the scenarios in [forward cases](../tests/forward-cases.md). Recheck existing implementation and second invocation before claiming portability. Exact validation records live in [validation results](validation-results.md).
