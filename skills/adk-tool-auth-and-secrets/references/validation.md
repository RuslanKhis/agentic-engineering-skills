# Validate the selected integration

Inspect test entrypoints before running them; collection can initialise clients. Use the target's environment and testing tools. Label assertions **offline with doubles**, **live**, **historical** or **not run**. A completed static inventory is not a security pass.

## Minimum checks for the affected branch

| Boundary | Observable checks |
| --- | --- |
| Identity/session/tool selection | Bob cannot load Alice's session/credential; client/model identity override cannot alter selection; denial precedes provider work; tenant/issuer separation where applicable |
| Public output and errors | Thought/auth/state/header canaries stay out of the public projection; model exception canaries stay out of framework logs; test each configured exporter affected by the change |
| Delegated OAuth | Wrong/expired/reused state; copied-URL/browser change; provider account/client switch; omitted refresh token; denied scope; correct owned-session continuation |
| Lifecycle | Later call, token expiry, rotating/nonrotating refresh, restart, disconnect during refresh, reconnect race; remote revocation failure cannot reactivate local access; losing versions retired |
| Failures and limits | `invalid_grant` distinct from quota/server/malformed failures; no consent erasure for transient failure; eligible retries bounded; deadlines/partial results truthful |
| GCP/managed integrations | Exact intended principal and target; approved API/secret access; scope/audience; full managed finalisation and correlated tool use; verified owned-resource cleanup |

Use a deterministic endpoint or service call that reaches the same tool backend before adding a model. Then exercise real ADK orchestration with the model boundary substituted, preserving the actual identity, session and tool dispatch. Keep the application's call policy: the source lab's one-Calendar-call guard is not a universal rule. If the product permits two calls, test both and their effects; if it permits one, verify duplicate suppression and later-invocation access.

For approved real model acceptance, assert persisted/correlated function calls and results, exact relevant arguments, synthetic ownership markers and grounded final text. HTTP 200 or closing a consent popup is insufficient. Bound model sends, tools, retries and total time separately; preserve failure evidence rather than rerunning to green.

For transport-attempt budgets and readiness diagnosis, use the [operations runbook](operations-runbook.md). Failed sends may be absent from ADK event history, and CLI counts do not establish the number of management RPCs. Report the layer actually measured. Error-response duration is not successful answer latency; a few local final-JSON responses do not establish browser responsiveness or production percentiles.

For Calendar-like features, verify the chosen scope and provider semantics rather than copying a scope string. A request about “tomorrow” requires trusted timezone/day bounds if that is the product promise. Pagination exhaustion, a result limit and incomplete search are different outcomes. These richer policies were not established by the source lab's mock-provider success.

Missing credentials should leave a usable local implementation/design and an exact prerequisite/approval list. Missing live evidence must remain visible. Do not run paid probes to make an offline verdict look complete.

## Exercise the boundary that failed

When changing provider-error handling, substitute HTTP transport and retain the real parser, broker, index/store and gateway. Inject token-endpoint 429/500/503, timeout and malformed success bodies. Assert a safe temporary failure, unchanged durable authorisation **and a successful later request**; count refreshes and provider reads across both calls. Separately test recognised `invalid_grant` and ensure it affects only the revision that failed. Resource-server 401/403 reasons need the distinct policy in [OAuth lifecycle](oauth-lifecycle.md); the historical token-endpoint tests do not cover it.

When changing model-error handling, keep actual ADK orchestration and replace only its model/transport boundary. Inject a synthetic exception canary and a final event with both thought-marked and public text. Assert real tool declaration/dispatch, correct public response and absence of the canary from formatted exception chains, framework logs and each configured exporter after flush. A replaced Runner can bypass the logging path that caused the original defect.

For restart acceptance, create populated synthetic state for two principals and record the persistent stores being tested. Disconnect one principal while retaining the other's valid connection and nonempty data. Stop and reap the process, launch a distinct process against the same intended stores with empty process-local caches, then verify:

- Each owned conversation retains its history; foreign and unknown sessions give non-enumerating denials.
- The disconnected principal stays disconnected and cannot reach the provider.
- The connected control principal still receives its own populated result.
- Credential references/version states agree with the intended lifecycle result, checked separately from an integration-status response.

Credential-index persistence, ADK conversation persistence and cross-replica invalidation are different assertions. Test another warm replica separately if that architecture exists. An empty control response or a new object in the same process is insufficient restart evidence. When reusing an encrypted local backend, preserve its encryption key with the ciphertext; generating a new key is a fresh store, not recovery.

For distributed identity, assert that a valid service caller cannot forge a user, select a foreign session or replay an expired/wrong-audience assertion. Denials for ambiguous mapping or unavailable policy must occur before provider work; no privileged credential fallback is permitted. Confirm generated tool declarations cannot override the trusted principal and validate non-integer limits/malformed timestamp types at the real dispatch boundary. These are conditional production gates, not a requirement to introduce a second service into a local app.

## Conditional Calendar semantics

If implementing promises such as “first meeting tomorrow”, derive the IANA timezone from trusted application preference. Calculate tomorrow's local midnight and the following local midnight independently, then convert both to instants; daylight-saving days need not last 24 hours. Choose and document all-day/non-default event handling, and verify the selected provider's filter semantics. A provider overlap filter is not automatically the requested event-start interval.

Follow continuation tokens through empty/short pages; detect repeated tokens and cap pages, bytes and retained text under the shared deadline. Apply the product's interval/filter/sort rules before declaring the first matching event. Return a trusted explicit incomplete/limit outcome when work stops before exhaustion, and carry it to the UI even if model prose is absent. Test DST/midnight boundaries, empty pages with tokens, repeated tokens, quota versus permission errors and exhaustion. The mock companion establishes neither these semantics nor bounded pagination; this is production implementation guidance.

## Validate this skill package

From this skill directory with Python 3.11+:

```bash
python -m unittest discover -s tests -v
python scripts/inspect_project.py --help
python scripts/inspect_project.py . --dry-run
```

The package has no mandatory third-party dependency. Tests optionally check real installed ADK events; when absent, those checks are skipped and must be reported. The public-text canary assertions use synthetic events and never call a provider. Projection deliberately preserves a canary already in allowed final text, proving the documented redaction limit.

The projection also requires non-partial model content without function calls
or responses. ADK 2.8.0 can mark partial/tool-bearing events final through
`skip_summarization` or `long_running_tool_ids`; user events can also be final.
Optional real-ADK regressions exercise these cases directly and through the
collector, proving they cannot replace an approved public answer. Report all
optional skips when ADK is absent; no provider calls are made.

The inspector exits **0** for a completed static inventory, **2** for invalid input, unsupported Python or an incomplete inventory, and **3** when `--expect-adk X.Y.Z` cannot establish matching static pins. Incomplete inspection takes precedence over a pin mismatch. The expectation checks declarations/locks, including unresolved requirement directives; it does not check installed packages. `--help` reports configurable file/byte bounds; traversal also caps depth at 32 and visited entries at `min(100000, max(1000, max_files * 20))`. It skips hidden/dependency/data directories, environment files and symlinks. It is not a sandbox for a hostile process changing the filesystem concurrently.

Also run the host's Agent Skill structural validator, validate internal links/metadata and copy the entire skill into a clean temporary directory. Run it there against fixtures with no book files. Use the repository's existing formatter/static checks when present; syntax compilation and behavioural tests are the baseline when no such tooling exists. The script's `--dry-run` is an explicit read-only run, not a provisioning preview.

Forward-test realistic requests independently: greenfield, customised project, missing prerequisites, an approval-required cloud operation, an unrelated near miss, and a repeated invocation. Give the evaluator only this package, the raw fixture and request. Retain actual actions/artifacts and limitations; a model-selected simulation is not a new live cloud test or evidence about other coding-agent products. Package execution results are recorded in [skill-validation.md](skill-validation.md).
