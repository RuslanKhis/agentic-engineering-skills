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

For Calendar-like features, verify the chosen scope and provider semantics rather than copying a scope string. A request about “tomorrow” requires trusted timezone/day bounds if that is the product promise. Pagination exhaustion, a result limit and incomplete search are different outcomes. These richer policies were not established by the source lab's mock-provider success.

Missing credentials should leave a usable local implementation/design and an exact prerequisite/approval list. Missing live evidence must remain visible. Do not run paid probes to make an offline verdict look complete.

## Validate this skill package

From this skill directory with Python 3.11+:

```bash
python -m unittest discover -s tests -v
python scripts/inspect_project.py --help
python scripts/inspect_project.py . --dry-run
```

The package has no mandatory third-party dependency. Tests optionally check a real installed ADK event shape; when absent, that one check is skipped and must be reported. The public-text canary assertions use synthetic events and never call a provider. Projection deliberately preserves a canary already in allowed final text, proving the documented redaction limit.

The inspector exits **0** for a completed static inventory, **2** for invalid input, unsupported Python or an incomplete inventory, and **3** when `--expect-adk X.Y.Z` cannot establish matching static pins. Incomplete inspection takes precedence over a pin mismatch. The expectation checks declarations/locks, including unresolved requirement directives; it does not check installed packages. `--help` reports configurable file/byte bounds; traversal also caps depth at 32 and visited entries at `min(100000, max(1000, max_files * 20))`. It skips hidden/dependency/data directories, environment files and symlinks. It is not a sandbox for a hostile process changing the filesystem concurrently.

Also run the host's Agent Skill structural validator, validate internal links/metadata and copy the entire skill into a clean temporary directory. Run it there against fixtures with no book files. Use the repository's existing formatter/static checks when present; syntax compilation and behavioural tests are the baseline when no such tooling exists. The script's `--dry-run` is an explicit read-only run, not a provisioning preview.

Forward-test realistic requests independently: greenfield, customised project, missing prerequisites, an approval-required cloud operation, an unrelated near miss, and a repeated invocation. Give the evaluator only this package, the raw fixture and request. Retain actual actions/artifacts and limitations; a model-selected simulation is not a new live cloud test or evidence about other coding-agent products. Package execution results are recorded in [skill-validation.md](skill-validation.md).
