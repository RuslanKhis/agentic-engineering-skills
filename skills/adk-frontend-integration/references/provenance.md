# Provenance and evidence limits

Evidence reviewed: **16 September 2026**. The source companion is the MIT-licensed [Agentic Engineering repository](https://github.com/RuslanKhis/agentic-engineering-adk-gcp). Paths below are relative to its `chapter-05-frontend-integration/` directory. They identify provenance; installing or using this skill does not require that repository, the manuscript, or this conversation. Preserve applicable MIT notices when redistributing adapted source code.

This reference records historical companion evidence, not validation results for the new skill or the user's project. “Offline” means the stated application or SDK boundary ran with its external model, provider transport, or command boundary replaced. It does not mean Google Cloud was exercised.

## Rules supported by implementation and tests

| Reusable rule | Companion evidence | Strength and limits |
| --- | --- | --- |
| Choose the public contract independently of execution location. Use JSON for final answers and AG-UI when streamed text or tool displays improve the interface. | `manual_api/local_backend.py`, `manual_api/adk_api_gateway.py`, `manual_api/agent_runtime_gateway.py`, `agui_backend/local_server.py`, `agui_backend/runtime_bridge.py` | Both frontend contracts worked against managed Runtime. Cloud Run/GKE gateways had offline HTTP coverage, not live deployment evidence. |
| Specify request, response, and conversation creation together. Validate successful HTTP responses in the browser. | `common/models.py`, `manual_frontend/src/lib/api.ts`, `manual_frontend/tests/api.test.mjs` | JSON uses `message`, optional `session_id`, then `session_id` and `response`. No request ID or strict extra-field rejection is implemented. Local backends may create a supplied missing ID; managed JSON treats it as resume-only. |
| Derive identity on the server and distinguish end-user identity from a service credential. | `common/auth.py`, `copilot_frontend/src/app/api/copilotkit/[[...slug]]/route.ts`, `tests/test_backend_http.py`, `audit/evidence-2026-09-13/live-auth.json` | Missing/invalid demo tokens were rejected live without model execution. The shared demo user and loopback BFF do not implement production sign-in or multi-user isolation. |
| Include lock waiting, session operations, query consumption, and failure diagnosis inside the overall deadline. Never silently resubmit an uncertain message. | JSON gateway modules, `manual_frontend/src/lib/api.ts`, `tests/test_backend_http.py`, `tests/test_runtime_session_roundtrips.py`, `manual_frontend/tests/api.test.mjs` | Offline tests cover queued deadlines, stalled response headers/body, cancellation, and one request without retry. Process-local locks and browser warnings are not durable ownership or idempotency. |
| Retain the owning SDK client while remote objects use its transport. | `manual_api/agent_runtime_client.py::_runtime_connection`, `tests/test_runtime_client_lifetime.py` | Actual SDK/HTTP/garbage-collection regression plus successful live retrieval. The companion retains the client; explicit graceful shutdown remains additional work. |
| Treat only confirmed absence as permission to create. Validate exact session resource identity and owner. | `manual_api/agent_runtime_client.py::get_remote_session`, `agui_backend/runtime_sessions.py`, `tests/test_runtime_session_metadata.py` | Managed query RPC returned generic HTTP 400 for absence; direct metadata returned 404. Live owned/missing reads and offline wrong-owner, wrong-name, 400/403 and unsafe-ID cases support this distinction. |
| Remove a redundant successful-session lookup only after proving the exact runner checks ownership before invoking the model. | `manual_api/agent_runtime_gateway.py`, `tests/test_runtime_session_roundtrips.py` | Installed AdkApp/Runner tests replace the model boundary. Failure-only metadata diagnosis stays within the deadline and does not retry the query. This optimisation is implementation/version dependent. |
| Request model streaming explicitly and avoid duplicating the final aggregate after partial text. | `agui_backend/runtime_bridge.py`, `tests/test_runtime_model_streaming.py`, `tests/test_runtime_translator.py` | Actual ADK/AdkApp offline tests observe default non-streaming versus explicit SSE; live browsers displayed partial answer text. An SSE response alone does not prove model streaming or responsiveness. |
| Validate the actual tool contract and correlate calls/results. Emit confirmed calls once. | `tests/test_runtime_chapter3_contract.py`, `tests/test_runtime_translator.py`, `tests/test_backend_http.py`, `agui_backend/runtime_bridge.py` | Offline wire checks and live cards cover three queues. Accepting both explicit statuses, `routed` and `success`, repaired a deployed/local mismatch. Partial function calls previously produced duplicate cards. |
| Define success and public/logging policies separately. | `tests/test_adk_api_events.py`, `tests/test_backend_http.py`, `audit/evidence-2026-09-15-manuscript/manual-contract-probe-results.json` | Managed JSON rejects event-level errors, but allows partial-text fallback and only logs tool-error envelopes. The local JSON probe returned earlier text after a later reported error; raised exceptions were publicly sanitised but privately logged with traceback and identifiers. |

## Gaps that must remain explicit

`copilot_frontend/src/app/tool-renderers.tsx` casts parsed results rather than validating them. Its parameter schema does not validate results; a completed JSON `null` can break rendering. The skill's [CopilotKit recipe](copilotkit-recipe.md) supplies a stronger parsing pattern; that does not retroactively repair or certify the companion renderer. Its separate validation is recorded in [validation.md](validation.md).

The managed bridge selects an earlier nonempty user message, allowlists one state key without validating its value, and uses generated IDs/name-order fallback for limited tool correlation. It does not implement strict continuation admission, durable replay, arbitrary parallel-tool correlation, distributed fencing, resumable approvals, or durable unknown-outcome protection. `copilot_frontend/src/app/telemetry-monitor.tsx` retains 50 selected entries, without a byte budget or whole-SDK memory bound. The routing tool only classifies; it performs no external ticket write.

Provisioning principles come from `scripts/runtime_bootstrap.py`, `scripts/runtime_lab.py`, `scripts/runtime_smoke.py` and their corresponding tests: read-only preflight, exact approved changes, saved operation intent, ownership-bound reconciliation, and separate cleanup. These scripts contain companion/campaign dependencies and are not portable assets unchanged. Injected recovery and missing-prerequisite branches were offline.

## Depth review: where the practical lessons now live

The September 16 review compared the current skill with implementation, test records, `MANUSCRIPT_COMPARISON_2026-09-15.md` and the updated manuscript. The following additions make earlier lessons actionable; they do not expand the historical live-test claim.

| Lesson and destination | Source of the rule | Evidence boundary |
| --- | --- | --- |
| Complete Next.js route, provider, CSS, renderer and observer wiring: [CopilotKit recipe](copilotkit-recipe.md) | `copilot_frontend/src/app/`, `audit/evidence/browser-checks.md` | Recorded package versions and historical local-browser production build; new recipe checked separately. No cloud-hosted frontend evidence. |
| Validate tool results independently of hook parameters, and distinguish invalid completion from pending work: [CopilotKit recipe](copilotkit-recipe.md) | Renderer defect; `agui_backend/runtime_bridge.py` public result model; `tests/test_runtime_chapter3_contract.py` | Backend projection tested; stronger frontend parser is a skill improvement, not a companion feature. |
| SDK event encoding and HTTP versus in-band errors: [AG-UI](ag-ui.md) | `agui_backend/runtime_bridge.py`, `tests/test_backend_http.py` | Offline HTTP assertions and historical browser streaming; a collected ASGI response alone does not prove incremental delivery. |
| Reject unsupported browser tools/state/continuation before invocation: [AG-UI](ag-ui.md) | Updated manuscript §12.4; comparison findings | Stronger production admission guidance; companion earlier-user-message fallback does not implement it. |
| ADK application naming, session paths, `/run` payload and private-service credentials: [JSON API](json-api.md) | `manual_api/adk_api_gateway.py`, `tests/test_adk_api_events.py`, README private Cloud Run instructions | Offline URL/payload/error tests and installed google-auth source; no live workstation impersonation or Cloud Run/GKE gateway check. |
| Exact managed service identity, external deployment configuration, child environment and independent readback: [deployment runbook](deployment-runbook.md) | `scripts/RUNTIME_BOOTSTRAP.md`, `scripts/RUNTIME_LAB.md`, `runtime_lab.py`, `tests/test_runtime_lab.py` | Identity correction and bounded existing-resource updates live; injection/refusal branches offline; fresh API activation unverified. |
| SDK plus transport attempt bounds and operation-state recovery: [deployment runbook](deployment-runbook.md) | `runtime_smoke.py`, `tests/test_runtime_smoke.py`, `tests/test_runtime_lab.py` | Successful smoke and ordinary provision/delete repeats live; uncertain-operation and retry faults injected offline. |
| Boundary-driven diagnosis, real model substitution and cancellation phases: [troubleshooting](troubleshooting.md) | `tests/offline_server.py`, `tests/test_runtime_model_streaming.py`, frontend HTTP tests, manuscript §13.8, prior skill forward-test cancellation failure | Some phases tested; complete managed stalled-producer/socket-disconnect coverage remains a requirement, not an accomplished test. |
| First event versus visible answer/tool/final timing: [troubleshooting](troubleshooting.md) | `tests/BROWSER_TIMING.md`, September 13 audit | Historical target misses and inconclusive stall cause remain visible; no latency promise. |
| Persistent-storage readiness, collision-safe provider identities and thread mapping: [production](production.md) | Updated manuscript §§12.1, 13.1–13.2 | Managed history recall after gateway restart live; local schema migration/readiness and production identity mapping remain advice requiring new tests. |

This review deliberately keeps project-wide RAG, VM, database and storage teardown outside a frontend integration skill. The transferable lesson is ownership-scoped cleanup with explicit inventory limits, not a universal deletion script.

## Recorded compatibility

Core declared pins: `google-adk==2.8.0`, `ag-ui-adk==0.7.0`, `ag-ui-protocol==0.1.21`, `google-cloud-aiplatform[agent-engines]==1.153.1`, `google-genai==2.19.0`. The recorded resolution includes FastAPI 0.141.1, HTTPX 0.28.1, Pydantic 2.13.5, google-auth 2.58.0 and Uvicorn 0.52.4; these are historical resolutions, not all exact manifest pins.

Copilot uses Node ≥22.12, CopilotKit React/runtime 1.69.0, AG-UI client 0.0.57, Next.js 15.5.24, React 19.2.1 and Zod 3.25.76. The manual frontend uses Node ≥18.18, React 18.3.1 and Vite 6.4.3. Both declare TypeScript 5.7.3. The fresh audit used macOS, Python 3.11.4, Node 24.19.0 and npm 10.7.0.

At aiplatform 1.153.1, the separate `[adk]` extra requires ADK below 2.0. Do not substitute it into this ADK 2.8 environment. Inspect the target's versions and preserve its dependency conventions.

## Historical verification scope

`audit/2026-09-13.md` records **153 Python tests passed, 52 warnings, no skips**, plus separate historical evidence for seven frontend tests and both builds. Overlapping test counts must not be summed. Real managed runs demonstrated three routing queues, tool cards, streamed answers, session recall after gateway restart, and completed provision/repeat/delete/repeat.

Fresh-project API activation, local Developer API inference, cloud-hosted frontends and live production multi-user/recovery tests remained unverified. Five-second first-answer targets were missed in 2/5 corrected warm JSON samples and 5/5 Copilot samples; tool finals stayed within 30 seconds. No underlying cause for two model-stage stalls was established.

`audit/2026-09-15-cloud-cleanup.md` records empty active audit inventories where accessible, with retained deleted storage and visibility limits. Cleanup is not a zero-cost or physical-erasure guarantee. New deployments, paid tests, and cleanup require their own scoped authorisation.
