# frontend-agui-approval-contract-declared: what the fixture holds

Bases: support-assistant, support-web, support-plan. Overlay:

- `app/agent.py`: `FunctionTool(issue_refund, require_confirmation=True)`.
- `app/agui.py`: the direct `ADKAgent(adk_agent=root_agent, ...)` constructor (the deprecated
  fire-and-forget HITL path; A3 expects `ADKAgent.from_app` with `ResumabilityConfig(is_resumable=True)`),
  `emit_interrupt_outcome` not passed (default `False`), no stripping of client-supplied `app:` /
  `user:` state keys (A3), and a `user_id_extractor` that reads `forwarded_props.userId` (client
  input; an extra identity finding, not asserted).
- `app/server.py`: mounts the AG-UI endpoint at `/api/agent` behind the IAP principal dependency.
- `pyproject.toml`: `ag-ui-adk==0.9.0`, `ag-ui-protocol==1.0.0`.
- `web/package.json`: `@ag-ui/client` 1.0.2, CopilotKit 1.79.0; `web/src/chat/RefundApproval.tsx`
  answers `adk_request_confirmation` with `useHumanInTheLoop` → `respond(...)`, i.e. a tool
  message; `web/runtime/server.ts` forwards to the Python endpoint with `HttpAgent`.
- `docs/tickets/support/G06.md`: the approval ticket, in progress, declares no approval contract
  (A1: the agent should make the ticket declare one: tool-message answers with the flag off, or
  interrupt outcomes answered by resume with the flag on); Evidence records the symptom after the
  @ag-ui/client upgrade. `docs/architecture/support.md` has C6 for approvals.

Diagnosis the assertions expect: a 1.0 client that expects interrupt outcomes answered by resume
against middleware answering with tool messages (A1); keep the flag off with tool messages, or
turn `emit_interrupt_outcome` on and move the client to resume, with a test that a tool-message
answer under the flag returns `INTERRUPT_RESUME_REQUIRED` (A2); backend confirmation gate stays
the control, UI decision is permission not completion; SDK tests reported as not run (A4).

Original context (unchanged): "An ADK 2.12 agent behind ag-ui-adk with emit_interrupt_outcome left
at its default, a CopilotKit app on @ag-ui/client 1.0 that answers approvals with useHumanInTheLoop
tool messages, require_confirmation on the refund tool. No network in the session."
