# Compatibility and inspection

## Recorded baselines

Historical companion execution used Python **3.11.4**, `google-adk==2.8.0`,
`google-genai==2.23.0` and `httpx==0.28.1`. Its declared supported Python range is
3.11–3.13, but that is not evidence that this skill was executed on every version.
Real model samples used `gemini-3.5-flash` through Vertex/Agent Platform with ADC.
That model is evidence, not a default to impose on another project.

The installed Chapter 0 environment inspected during skill creation contained
GenAI **2.22.0**, despite its audit requirements pinning 2.23.0. Dependency
declarations, installed packages and historical results are distinct facts.
The skill-creation checks and their exact environments are recorded in
[validation-results.md](validation-results.md).

The September 16 depth review retained these pins. Its new runtime recipes target
ADK 2.8.0 specifically, including a callback-chain quirk and retained-state hazard;
reassess those assertions when deliberately migrating SDK versions. Guidance on
transport guards is conditional on the GenAI 2.23.0/HTTPX 0.28.1 path, and is not
an assertion that every SDK transport retries identically.

No claim is made for “latest ADK”, every Python version, all agent products or
API-key live behaviour. Keep the target package manager and pins. For another
release, inspect its local signatures/source or version-matched official provider
documentation; run relevant offline acceptance before claiming compatibility.
If a required surface is unavailable, fail with the missing symbol/version and
propose an explicit adaptation rather than upgrading automatically.

Useful primary references, consulted only when the selected version needs them:
[ADK source](https://github.com/google/adk-python),
[ADK documentation](https://google.github.io/adk-docs/), and
[GenAI SDK source](https://github.com/googleapis/python-genai).

## Read-only helper

Run `scripts/inspect_project.py` with the target project's Python interpreter.
It uses the standard library, does not import target modules, launch commands,
load `.env` values, contact providers or write into the project. It inventories
Python files, manifests, test/config paths and installed package metadata.
It reports simple AST findings for direct parallel-key collisions and loops
without demonstrable finite positive bounds. It does not prove correctness,
security, all data flows or environment readiness.

```bash
python /path/to/skill/scripts/inspect_project.py --help
python /path/to/skill/scripts/inspect_project.py --project . --dry-run
python /path/to/skill/scripts/inspect_project.py --project .
python /path/to/skill/scripts/inspect_project.py --project . --require-adk-version 2.8.0
```

Use the installed skill's path in place of `/path/to/skill`. Paths supplied at
runtime are configurable; no local machine path is embedded in the helper.
`--dry-run` lists intended reads without reading source/configuration contents.
All modes are read-only and safe to repeat. Source string literals and environment
values are omitted from output; inventory paths remain visible. If generated
assets exhaust the scan limit, select a smaller service root or explicitly omit
irrelevant directory names using repeatable `--exclude-dir NAME`. Exclusions apply
at every depth and are recorded in output; review their coverage before relying
on results. An incomplete scan is never a clean bill of health.

Exit codes: **0** inspection/plan completed (findings still need review), **2**
invalid input or incomplete inspection, **3** the explicitly required ADK version
does not match the installed version or declarations need reconciliation.
The compatibility option accepts only an exact numeric version. It does not
install packages or reinterpret an unresolved range as an exact lock.

Nested manifest discovery may span several services. Select the intended service
root and review the matching lockfile before interpreting a mismatch. The helper
extracts numeric ADK/GenAI/httpx requirements and selected lockfile package versions;
editable dependencies, dynamic metadata, platform markers and include semantics
still need the package manager's own resolution evidence. Symlinks and generated,
hidden or environment directories are excluded, and scan limits produce an
explicit incomplete result.

Bare and table-form Poetry versions are checked alongside lockfile versions;
a stale lock cannot hide a conflicting declaration. Unresolved declarations for
known packages are reported without their raw values and fail an explicitly
requested exact ADK check. Comments and unrelated TOML descriptions are not
dependency pins. Parser-depth failures return structured incomplete results.
