# Compatibility and version decisions

## Recorded integration baseline

These versions identify the companion implementation and prior evidence reopened on 16 September 2026. They are not instructions to replace a target's dependency choices.

| Layer | Declared or recorded versions |
| --- | --- |
| Python | Minimum 3.11; executed with CPython 3.11.4 on macOS |
| Core ADK | `google-adk==2.8.0`, `google-genai==2.19.0` |
| Python AG-UI | `ag-ui-adk==0.7.0`, `ag-ui-protocol==0.1.21` |
| Managed SDK | `google-cloud-aiplatform[agent-engines]==1.153.1` |
| Other resolved Python packages | FastAPI 0.141.1, Pydantic 2.13.5, HTTPX 0.28.1, google-auth 2.58.0, Uvicorn 0.52.4, pytest 9.1.1 |
| Manual browser | React/React DOM 18.3.1, Vite 6.4.3, TypeScript 5.7.3; declared Node ≥18.18 |
| Copilot browser/BFF | `@copilotkit/react-core` and `@copilotkit/runtime` 1.69.0, `@ag-ui/client` 0.0.57, Next 15.5.24, React/React DOM 19.2.1, Zod 3.25.76, TypeScript 5.7.3; declared Node ≥22.12 |
| assistant-ui | `@assistant-ui/react-google-adk` 0.0.40 read, not run, against a Python gateway tested offline on google-adk 2.12.0 (2026-10-26); its `assistant-cloud` dependency is unpinned (`*`) |
| Historical frontend execution | Node 24.19.0, npm 10.7.0, macOS |

The companion pins the five Python integration packages exactly; other Python requirements use bounded ranges. Its resolved versions are evidence snapshots, not a complete reproducible Python lock. Frontend lockfiles pin the resolved npm graphs. Preserve the target's own lockfile and existing override rationale. Matching a few direct versions does not prove the full environment matches.

The September 16 depth-review checks found all five integration pins unchanged, with google-auth **2.57.1** in the invoking environment rather than historical 2.58.0. The private-service helper branch was inspected at that installed version. The new frontend recipe checks used bundled Node **24.19.0** and the recorded TypeScript/CopilotKit/Zod dependencies; the shell's default Node 18.20.4 is below this Next app's declared minimum. No packages were upgraded or downgraded by the skill review.

**Known incompatibility:** the recorded `google-cloud-aiplatform[adk]==1.153.1` extra requires ADK below 2.0.0. The integration deliberately uses `[agent-engines]` alongside the explicit ADK 2.8.0 pin. Do not add the `[adk]` extra to that stack or silently downgrade ADK to satisfy it. Report the conflict and prepare the smallest explicit dependency decision.

## Upstream since the baseline (read 2026-10-22)

The recorded `ag-ui-adk==0.7.0` and `ag-ui-protocol==0.1.21` pins are the tested stack, not the current line. AG-UI 1.0 is a normative specification (`docs/spec/1.0`; `ag-ui-protocol` 1.0.0 on PyPI 2026-09-17): `RUN_FINISHED` carries an optional `outcome` (success, interrupt or cancelled) with resume entries on the run input, delegated work is attributed with `subagentRunId`, the `THINKING_*` events are retired in favour of the reasoning family, every `RUN_STARTED` carries `protocolVersion`, and an unknown event is dropped with a warning while a malformed known value is fatal (1.0 changelog, informative page). `ag-ui-adk` 0.7.1 (2026-10-01) added the opt-in `emit_interrupt_outcome` (default `False`); 0.8.0 (2026-10-07) raised the floor to `ag-ui-protocol>=1.0.0` and declares `protocolVersion` on every `RUN_STARTED`; 0.9.0 persists the processed-message ledger in session state; 0.11.0 (2026-10-21, current on PyPI) fixes an access-control flaw in which client-supplied `app:` and `user:` state keys could modify shared ADK state (#2927, "upgrading is recommended"), discards those keys at the HTTP endpoint, and keeps `google-adk>=1.28.1,<3.0.0` (`integrations/adk-middleware/python/CHANGELOG.md`, read 2026-10-22). Moving a 0.7.0 project onto this line is one version decision for the Python package, the protocol package and the JavaScript client together; [the AG-UI reference](ag-ui.md) describes the 0.7.0 API that was exercised, and the inspector's `--require-tested-stack` still compares against that baseline. Until the move, do what the 0.11.0 fix does: strip client-supplied `app:` and `user:` keys before merging state. The inspector's `reference_status: "unverified"` on a project pinned to the 1.0 line (ag-ui-adk 0.11.0, `@ag-ui/client` 1.0.x, CopilotKit 1.79.0) says only that the recipe was exercised on the 0.7.0 line; it is not a finding, and the `--require-tested-stack` gate is skipped for such a project with the reason recorded. The CopilotKit example that replaced the archived `CopilotKit/with-adk` repository (its README now says the project was consolidated into the monorepo at `examples/integrations/adk`; CopilotKit/CopilotKit commit 54dddf7, read 2026-10-22) shows how mixed the generations are even upstream: its Python agent pins `ag-ui-adk==0.7.0` and `ag-ui-protocol==0.1.18` while its web app pins `@ag-ui/client` and `@ag-ui/core` 1.0.2 with `@copilotkit/react-core` and `@copilotkit/runtime` 1.79.0 (`agent/pyproject.toml`, `package.json`), so a 0.x Python middleware already serves a 1.0 JavaScript client there; the [CopilotKit recipe](copilotkit-recipe.md) in this skill targets the 1.69.0 line it exercised.

Re-checked on PyPI on 2026-10-23: ag-ui-adk 0.11.0 is still current, it requires `ag-ui-protocol>=1.0.0` (the floor since 0.8.0), and its `dependencies=` keyword reaches only the run route (see [ag-ui.md](ag-ui.md)). The recorded 0.7.0 pin is unchanged; the move remains an explicit decision.

A2UI packages, on PyPI on 2026-10-24: `a2ui-adk` 0.1.0 requires `a2ui-agent-sdk>0.8.0` (0.8.0 still shipped `a2ui.adk`), `google-adk>=1.28.1` and `google-genai>=1.27.0`; its `[a2a]` extra adds `a2ui-a2a` 0.1.0, which pins `a2a-sdk>=0.3.0,<0.4.0`. That extra therefore holds an ADK 2.12 project on the 0.3 A2A SDK and conflicts with an `a2a-sdk>=1.0,<2` pin for exposing the same agent over A2A 1.0; resolve it before choosing the route, with `adk-agent-interoperability` owning the A2A pin. The AG-UI route adds no A2A constraint and pins `a2ui-agent-sdk>=0.9.0,<0.10.0` with `a2ui-core>=0.4.0,<0.5.0` (ag-ui `integrations/adk-middleware` README). Pin released versions: A2UI's main branch carries unreleased breaking changes.

## Browser stack since the baseline (read 2026-10-23)

The exercised manual-browser recipe stays on React 18.3.1 and Vite 6.4.3. The current line on npm is Vite 8.3.5 with `@vitejs/plugin-react` 6.1.2 (plugin v6 drops Babel; React Compiler is enabled through `@rolldown/plugin-babel` and its preset), React 19.3.1, Tailwind CSS 4.3.3, `@tanstack/react-query` 5.104.5, zod 4.6.7 and `eslint-plugin-react-hooks` 7.1.1. The web application defaults in `adk-system-designer` (shadcn on Base UI, Tailwind 4, TanStack Query) assume that line, so a new project starts there and records its own resolved versions; this skill's recorded recipe does not move until the change is exercised and recorded here. That is a version decision, not an upgrade of an existing project.

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
