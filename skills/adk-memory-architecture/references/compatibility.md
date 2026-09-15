# Compatibility and project inspection

Use this file before changing a version-sensitive integration or interpreting
the bundled inspector. Preserve the target's selected Python, ADK and package
manager. Do not install or upgrade packages merely to match this skill's source.

## Source baseline is a reference, not a target lockfile

The companion's 15 September 2026 evidence records Python **3.11, ARM64**; that
snapshot does not preserve the interpreter patch version. Earlier 14 September
records explicitly contain Python **3.11.4**. The 15 September resolved snapshot
contains these versions (selected from 120 distributions):

| Distribution | Historical resolved version |
| --- | --- |
| `google-adk` | 2.8.0 |
| `google-cloud-aiplatform` | 1.153.1 |
| `google-genai` | 2.19.0 |
| `google-cloud-bigquery` / `google-cloud-bigquery-storage` | 3.45.1 / 2.41.0 |
| `google-cloud-storage` | 3.14.1 |
| `google-cloud-dlp` / `google-cloud-modelarmor` | 3.38.0 / 0.7.1 |
| `google-cloud-secret-manager` | 2.30.0 |
| `redis` | 6.4.0 |
| `fastapi` / `uvicorn` | 0.141.1 / 0.53.0 |
| `firebase_admin` | 7.5.0 |
| `pydantic` | 2.13.5 |
| `pytest` / `pytest-asyncio` | 9.1.1 / 1.4.0 |
| `httpx` | 0.28.1 |

The helper uses the Python standard library and requires Python 3.11+. The
skill's own tests require pytest; their actual environment is recorded in
[skill-validation.md](skill-validation.md). These are separate environments.
Plain Markdown remains usable without running the helper.

## Verify the target before applying SDK details

1. Identify the environment that runs the chosen service. Compare declared
   Python/ADK requirements and resolved locks with its interpreter/package
   metadata. Resolve stale environments, markers and multi-package workspaces.
2. Inspect the installed version's supported session constructors and event
   schema, `App`/`Runner` assembly, tool context and callback signatures.
   Inspect managed-memory generation/operation/expiry schemas and BigQuery
   query APIs only when entering those modes. Read local package code before
   making version-specific changes; consult official provider documentation
   for missing facts. Do not claim compatibility with “the latest ADK”.
3. ADK 1.x and unverified future major versions are outside this source's API
   baseline. Stop applying baseline-specific code, report the mismatch and
   validate an adaptation against the pinned target, or obtain a separate
   migration decision. Architecture review can continue. A different 2.x
   release also needs interface and contract tests; a matching version alone
   does not establish correct assembly or cloud compatibility.
4. Keep exact API identifiers even when provider marketing names change;
   `VertexAiSessionService`, `VertexAiMemoryBankService` and `reasoningEngines`
   occur in this baseline. Verify the selected service, location, model,
   enabled API and IAM permissions for the actual target.

## Inspector contract

Run using the already selected interpreter and supplied paths:

```bash
"$PYTHON" "$SKILL_DIR/scripts/inspect_project.py" --help
"$PYTHON" "$SKILL_DIR/scripts/inspect_project.py" --project "$PROJECT_DIR" --dry-run
"$PYTHON" "$SKILL_DIR/scripts/inspect_project.py" --project "$PROJECT_DIR"
```

The helper emits JSON to stdout and never executes project code, loads `.env`,
creates files or calls cloud services. Dry run reports the plan and interpreter
metadata without reading project files. Normal inspection reads bounded Python
files and dependency manifests, emits identifier-based mode signals and extracts
simple version declarations. It excludes hidden directories, dependency/build
trees, evidence directories, nested skills, symlinks and non-source config.

The limits are 2,000 visited files, 512 KiB per candidate and 8 MiB total reads.
It reports omitted coverage, malformed Python and unreadable candidates without
echoing source or exception contents. Paths and package versions are reported;
review paths before sharing an inventory. This is not a hostile-filesystem
sandbox; run against a stable checkout, not files concurrently changed by an
untrusted process. It does not inspect cloud credentials or establish access.

| Exit | Meaning | Next action |
| --- | --- | --- |
| 0 | Inspection/plan completed, possibly with warnings | Read coverage and compatibility; this is not a security or readiness pass |
| 2 | Invalid arguments, missing directory or unsupported helper interpreter | Correct the input; use manual inspection rather than changing target pins |
| 3 | Conflicting ADK declarations, declared/installed mismatch, or unsupported ADK major | Select the intended environment and resolve compatibility before SDK implementation |

Declaration extraction is deliberately partial: it is not a requirements or
lockfile resolver. It does not evaluate environment markers, include files,
Poetry tables, URLs or complete range constraints. Tests can produce mode
signals and comments can contain version declarations. Missing signals do not
establish absent features. Manually inspect relevant manifests, locks and
runtime seams before drawing conclusions. The helper never changes a pin.
