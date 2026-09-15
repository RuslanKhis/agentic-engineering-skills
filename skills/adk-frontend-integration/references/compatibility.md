# Compatibility and version decisions

## Recorded integration baseline

These versions identify the companion implementation and prior evidence reopened on 15 September 2026. They are not instructions to replace a target's dependency choices.

| Layer | Declared or recorded versions |
| --- | --- |
| Python | Minimum 3.11; executed with CPython 3.11.4 on macOS |
| Core ADK | `google-adk==2.8.0`, `google-genai==2.19.0` |
| Python AG-UI | `ag-ui-adk==0.7.0`, `ag-ui-protocol==0.1.21` |
| Managed SDK | `google-cloud-aiplatform[agent-engines]==1.153.1` |
| Other resolved Python packages | FastAPI 0.141.1, Pydantic 2.13.5, HTTPX 0.28.1, google-auth 2.58.0, Uvicorn 0.52.4, pytest 9.1.1 |
| Manual browser | React/React DOM 18.3.1, Vite 6.4.3, TypeScript 5.7.3; declared Node ≥18.18 |
| Copilot browser/BFF | `@copilotkit/react-core` and `@copilotkit/runtime` 1.69.0, `@ag-ui/client` 0.0.57, Next 15.5.24, React/React DOM 19.2.1, Zod 3.25.76, TypeScript 5.7.3; declared Node ≥22.12 |
| Historical frontend execution | Node 24.19.0, npm 10.7.0, macOS |

The companion pins the five Python integration packages exactly; other Python requirements use bounded ranges. Its resolved versions are evidence snapshots, not a complete reproducible Python lock. Frontend lockfiles pin the resolved npm graphs. Preserve the target's own lockfile and existing override rationale. Matching a few direct versions does not prove the full environment matches.

**Known incompatibility:** the recorded `google-cloud-aiplatform[adk]==1.153.1` extra requires ADK below 2.0.0. The integration deliberately uses `[agent-engines]` alongside the explicit ADK 2.8.0 pin. Do not add the `[adk]` extra to that stack or silently downgrade ADK to satisfy it. Report the conflict and prepare the smallest explicit dependency decision.

## Inspect without changing versions

Run the inspector using the target's selected interpreter. Its installed metadata describes that interpreter, while manifest declarations describe the project being inspected. A script launched from another virtual environment cannot certify the target's installed packages.

```text
python scripts/inspect_project.py --project . --mode json --dry-run
python scripts/inspect_project.py --project . --mode managed-agui --require-tested-stack
```

Run these paths from the installed skill directory, or resolve them there and set `--project` to the target. The first command is read-only evidence gathering; the second deliberately fails if its relevant invoking-interpreter package versions are missing or differ from the recorded baseline. It does not install anything. Read the helper's `--help` for scan bounds and precise exit codes.

Classify a target difference as one of:

- **Matched baseline:** exact relevant package versions are present. Still run the selected contract tests; this is not an all-dependencies or security certification.
- **Unverified version:** different or unresolved pins. Inspect that installed SDK's public signatures and source, run focused import/event/session tests and adapt using the existing pins. State what was actually verified.
- **Known incompatible:** Python lacks required syntax/API support, a resolver conflict exists, or a required interface is demonstrably absent. Stop the dependent path, explain the exact mismatch and ask for the decision needed to change versions or choose another supported design. Continue independent design/offline work where possible.

Never solve incompatibility with an unrequested upgrade. Use the target package manager and lockfile workflow if an explicit version change is approved. Treat installing application dependencies separately from cloud authorisation.

## Skill helper and agent-environment scope

The two helpers use the Python standard library and require Python 3.11+. They do not import the target application, invoke package managers, install dependencies, contact a model or call cloud APIs. `--dry-run` repeats their read-only operation.

The skill core is ordinary Markdown following the [Agent Skills specification](https://agentskills.io/specification). Optional `agents/openai.yaml` enables normal implicit selection in compatible clients; the core does not require it. Behavioural evaluation records belong in [validation.md](validation.md). Do not claim Claude Code, Gemini CLI, Cursor, Windows or Linux execution from Markdown validity alone; only environments actually exercised are supported by the recorded evidence.
