# Read-only inspection helper

Use `scripts/inspect_project.py --project PATH` to locate dependency declarations and safety-related source signals without executing target code. `--dry-run` performs the same read-only inspection and explicitly reports that no changes were made. `--help` describes its bounded traversal.

The helper requires Python 3.11+ for its own TOML reader. This does not impose Python 3.11 on the target project. Select an already available compatible interpreter; never upgrade the target just to run an inventory helper.

Exit codes:

- `0`: the eligible files within the configured traversal were inspected; this is not a safety verdict.
- `1`: the scan was partial because of bounds, unreadable/malformed eligible files or skipped symlinks. Inspect the reported area before drawing conclusions.
- `2`: invalid arguments or an inaccessible project root.

Only source paths, numeric dependency constraints and fixed signal names are emitted. The helper ignores credential files and never prints source strings, provider URLs, prompts or environment values. It does not import modules, execute tests, invoke package managers or contact services.

Supported declaration inputs are `pyproject.toml` project dependencies, Poetry dependency entries, requirement files and `.python-version`. Lockfile names identify the likely package manager, but locked resolution must be read with that manager's tooling. Dynamic dependencies, includes, aliases, indirect function calls and generated configuration need manual inspection.

Signals include common retry/deadline/client calls, confirmation configuration and blocking calls within async functions. A UUID call inside a retry-decorated function deserves review because retries may generate distinct operation identities. A signal is a syntactic observation: it cannot prove that the provider deduplicates, that confirmation covers every entry point, or that every retry/cancellation path is safe. Absence of a signal proves none of those properties either.

The scan excludes common dependency, build, Git and cache directories and skips symlink entries. It bounds depth, eligible file count, per-file size and total directory entries, including excluded names. `--max-entries` stops globally at the configured count and conservatively marks the scan partial. Those exclusions are reported as limits; for a monorepo, point at the selected application and inspect relevant shared libraries separately. Repeat output is deterministic for unchanged input. Preserve raw JSON locally if useful, after confirming that target filenames themselves are suitable to share.

Use a stable local checkout. The helper is not a security sandbox for an adversarial filesystem that changes directories or symlinks during inspection; its bounds limit inspected input, not a hard wall-clock execution deadline.
