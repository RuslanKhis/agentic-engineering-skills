# Compatibility and inspection

## Dated baseline, not a version migration policy

| Component | Historical chapter evidence |
| --- | --- |
| Python, local Runtime and Cloud Run tests | 3.11.4 |
| Python, local GKE tests | 3.12.9 |
| Custom container base | `python:3.12.11-slim-bookworm` |
| Google ADK | `google-adk==2.8.0`; Runtime declares `google-adk[a2a]==2.8.0` |
| Runtime SDK | `google-cloud-aiplatform[agent_engines]==1.153.1` |
| Resolved integration libraries | `google-genai==2.23.0`, `fastapi==0.141.1`, `pydantic==2.13.5` |
| Model/backend | `gemini-3.5-flash`, enterprise mode with global inference; hosting region configured separately |
| Live evidence dates | 13–14 September 2026; see [evidence.md](evidence.md) for scope |

The example guides allow Python 3.11–3.13; that range is not a claim that every Python/OS combination was tested. Direct version pins are not a transitive lock. Availability of a model, backend, region or SDK contract must be rechecked when adopting the pattern later. Never use the phrase “latest ADK” as a compatibility promise.

## Inspect the target, then apply the appropriate contract

Select the target's existing interpreter from its documented environment. Read `.python-version`, `pyproject.toml`, requirements/constraints/includes, lockfiles and Docker base together; check the installed environment separately. A project version declaration and the interpreter running the inspector can differ. For example, run this using the selected interpreter, without importing the agent:

```python
import importlib.metadata
import sys

print(sys.version)
for name in ("google-adk", "google-cloud-aiplatform"):
    try:
        print(name, importlib.metadata.version(name))
    except importlib.metadata.PackageNotFoundError:
        print(name, "not installed")
```

Use the corresponding installed `adk deploy cloud_run --help` or `adk deploy agent_engine --help` to verify command flags before generating or executing them. Inspect installed SDK signatures and real event fixtures for session/query integrations. Preserve required dependency extras. An old optional `a2a` import failure was recorded on ADK 2.2.0; the 2.8.0 Runtime baseline retains the extra, which is not evidence the older failure recurred on 2.8.0.

If a pinned target differs from the baseline, label it **unverified against this skill's baseline** and validate its actual contracts before using version-sensitive examples. Do not declare it incompatible based on version inequality alone. If a required method/flag/schema is absent, report that concrete incompatibility and stop the dependent operation. Local planning or unrelated edits can continue. Propose a version change only with rationale and approval for that scope.

## Bundled helper

Run `scripts/inspect_project.py` with an explicit project root. It uses only the Python 3.11+ standard library and never imports target code, executes cloud tools, reads `.env` values or edits the target. `--help` describes its limits and exit statuses. `--dry-run` explicitly selects the same non-mutating inspection behaviour as the default.

`--mode` selects `auto`, `cloud-run`, `agent-runtime` or `gke`. Architecture signals help discovery; they do not choose the user's platform or replace inspection of customised deployment code. `--require-baseline` is a strict evidence gate: missing, ranged, conflicting or different required pins cause a nonzero result. It does not install packages or prove that a different version cannot work.

Read the three Python fields separately: `python.interpreter` is the process running the helper, `python.declared_requirements` contains parsed `pyproject.toml` constraints, and `python.version_pins` contains `.python-version` declarations. Pin records point to manifest IDs with root/nested provenance. One or more nonblank numeric `major.minor[.patch]` lines are reported in their declared order. A file containing a named environment, path, unsupported syntax or no version is marked `unparsed` with its values omitted; inspect it privately if relevant. These files use the same bounded, nonsymlink manifest reader. The helper neither selects an interpreter nor evaluates Python compatibility, and Python declarations do not change the package baseline gate.

With a selected mode and all of `--project`, `--region`, `--account`, the helper prints read-only `gcloud` argument arrays for project, billing, enabled-API and applicable build-identity checks. It never runs them. Inspect the arrays before executing only the intended reads. Project-level reads have no region scope; regional reads include the selected region. API listings still require comparison with the mode's actual dependencies, and neither a plan nor a successful lookup establishes model access.

The helper deliberately reports only constrained metadata and configuration presence. It is not a secret scanner, environment resolver, lockfile resolver, Terraform parser or full source audit. Review its coverage/limits and inspect the remaining relevant files without printing sensitive contents. [skill-validation.md](skill-validation.md) records the environments actually used to test this package, separately from the chapter's cloud evidence.
